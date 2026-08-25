#!/usr/bin/env python3
"""seed-refcheck-fixture.py — refcheck verification fixture (RESPAWN).

Creates a landlord vacancy + 5 applications (each with a UNIQUE submit email)
whose reference calls are put in the states the reference_checks scenarios
need, then prints a JSON report. Every application is resolved by its OWN
submit email (never by "latest application" — sibling jobs race those).

Scenario -> state map (the issue set being re-verified):
  panel-renders        : landlord_ref=contact_initiated (2 attempts), employer_ref=queued
  panel-correct (#611) : employer_ref=awaiting_correction (failed-delivery attempt)
  panel-substitute     : landlord_ref=objected (terminal, can_substitute_referee)
  panel-export (#615)  : employer_ref=contact_initiated (2 delivered attempts)
  referee-form-complete: landlord_ref=contact_initiated + live form_token

Usage:
  python3 seed-refcheck-fixture.py
Env: TEST_USER_EMAIL / TEST_USER_PASSWORD (read from the worktree root .env),
  BUG_HUNT_BASE_URL (default http://localhost:4100).
DB: connects to the local sandbox Postgres container via docker exec (the
  container name is passed with --db-container; default
  rt-refcheck-verification-rerun-dev-db).
"""
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid
from io import BytesIO

BASE = os.environ.get("BUG_HUNT_BASE_URL", "http://localhost:4100")
DB_CONTAINER = os.environ.get("DB_CONTAINER", "rt-refcheck-verification-rerun-dev-db")
DB_NAME = os.environ.get("DB_NAME", "righttenantry_dev")
TEST_EMAIL = os.environ.get("TEST_USER_EMAIL", "")
TEST_PASSWORD = os.environ.get("TEST_USER_PASSWORD", "")

VACANCY = {
    "property_name": "Refcheck Verification Flat",
    "address_line_1": "12 Verification Road",
    "city": "Dublin",
    "county": "Dublin",
    "eircode": "D01 F5RT",
    "monthly_rent_cents": 180000,
    "bedrooms": 2,
    "property_type": "apartment",
    "pets_policy": "no",
    "smoking_policy": "no",
    "available_from": "2026-09-01",
    "lease_term": "12 months",
    "status": "active",
}

# Base form fields for an employed applicant (never_rented_before unset →
# landlord_ref + employer_ref slots are minted on the viewed transition).
BASE_FORM = {
    "first_name": "Refcheck",
    "last_name": "Fixture",
    "phone": "0851234567",
    "current_address": "8 Test Terrace",
    "current_city": "Dublin",
    "current_county": "Dublin",
    "current_living_situation": "renting",
    "reason_for_moving": "Verification fixture",
    "num_occupants": "1",
    "has_pets": "no",
    "is_smoker": "no",
    "has_eviction_history": "no",
    "has_ccjs": "no",
    "reference_contact_choice": "attested",
    "employment_status": "employed",
    "monthly_income_cents": "2800",
    "job_title": "Fixture Officer",
    "employer_name": "Fixture Labs",
    "employment_duration": "2 years",
    "employer_ref_name": "FIXTURE Employer Ref",
    "employer_ref_phone": "0861112222",
    "employer_ref_email": "employer.ref@fixture.test",
    "landlord_ref_name": "FIXTURE Landlord Ref",
    "landlord_ref_phone": "0863334444",
    "landlord_ref_email": "landlord.ref@fixture.test",
    "personal_statement": "[bug-hunt fixture data — auto-generated] Verification fixture applicant.",
    "gdpr_consent": "on",
    "desired_move_in_date": "2026-10-01",
    "_website": "",
}

SCENARIOS = ["renders", "correct", "substitute", "export", "form-complete"]


def psql(sql: str) -> str:
    """Run SQL against the sandbox DB; return stdout."""
    cmd = ["docker", "exec", "-i", DB_CONTAINER, "psql", "-U", "test", "-d", DB_NAME, "-t", "-A", "-c", sql]
    r = subprocess.run(cmd, capture_output=True, text=True, input="")
    if r.returncode != 0:
        raise RuntimeError(f"psql failed: {r.stderr}\nSQL: {sql}")
    return r.stdout.strip()


def gen_pdf_bytes(name: str, role: str) -> bytes:
    """Minimal deterministic PDF carrying the fixture banner (reportlab)."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(f"BUG-HUNT FIXTURE — {name}")
    c.drawString(72, 800, "BUG-HUNT FIXTURE — NOT A REAL PERSON")
    c.drawString(72, 780, f"Referee document: {role}")
    c.drawString(72, 760, f"Subject: {name}")
    c.showPage()
    c.save()
    return buf.getvalue()


def multipart(fields: dict, files: dict) -> tuple:
    """Build a multipart/form-data body. Returns (body, content_type)."""
    boundary = "----refcheckfixture" + uuid.uuid4().hex
    chunks = []
    for k, v in fields.items():
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        )
    for k, (filename, content) in files.items():
        ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{filename}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n".encode()
        )
        chunks.append(content + b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def http(method: str, path: str, data=None, headers=None, cookies=None, files=None) -> tuple:
    url = BASE + path
    body = None
    hdrs = {"User-Agent": "refcheck-fixture/1.0"}
    if files is not None:
        body, ctype = multipart(data or {}, files)
        hdrs["Content-Type"] = ctype
    elif data is not None:
        if isinstance(data, (dict, list)):
            body = json.dumps(data).encode()
            hdrs["Content-Type"] = "application/json"
        else:
            body = urllib.parse.urlencode(data).encode()
            hdrs["Content-Type"] = "application/x-www-form-urlencoded"
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    if cookies:
        req.add_header("Cookie", cookies)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            set_cookie = ",".join(v for k, v in resp.headers.items() if k.lower() == "set-cookie")
            return resp.status, raw, set_cookie
    except urllib.error.HTTPError as e:
        sc = ",".join(v for k, v in e.headers.items() if k.lower() == "set-cookie")
        return e.code, e.read().decode(), sc


def parse_cookies(set_cookie: str) -> dict:
    out = {}
    for part in set_cookie.split(","):
        m = re.search(r"([a-z_]+)=([^;]+)", part)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def main() -> int:
    cookie_jar = {}
    csrf = None

    # 1. Login
    code, body, setc = http("POST", "/api/v1/auth/login",
                            {"email": TEST_EMAIL, "password": TEST_PASSWORD})
    if code != 200:
        print(f"LOGIN FAILED: HTTP {code}: {body[:400]}", file=sys.stderr)
        return 1
    login = json.loads(body)
    csrf = login.get("csrf_token") or login["data"].get("csrf_token")
    cookie_jar.update(parse_cookies(setc))
    cookie_str = "; ".join(f"{k}={v}" for k, v in cookie_jar.items())
    print(f"login ok (landlord {login['data']['id']})")

    def auth_headers():
        return {"x-csrf-token": csrf} if csrf else {}

    # 2. Vacancy (idempotent by property name)
    code, body, _ = http("POST", "/api/v1/vacancies", VACANCY,
                         headers=auth_headers(), cookies=cookie_str)
    if code not in (200, 201):
        print(f"VACANCY FAILED: HTTP {code}: {body[:400]}", file=sys.stderr)
        return 1
    vac = json.loads(body)["data"]
    vac_id, short_code = vac["id"], vac["short_code"]
    print(f"vacancy {short_code} ({vac_id})")

    # 3. Fetch the live form once (ground truth for the POST field set)
    code, html, _ = http("GET", f"/apply/{short_code}")
    if code != 200:
        print(f"APPLY FORM FAILED: HTTP {code}", file=sys.stderr)
        return 1
    known_names = set(re.findall(r'name="([^"]+)"', html))
    print(f"form fields seen: {len(known_names)}")

    applications = {}
    for tag in SCENARIOS:
        email = f"refcheck-{tag}-{uuid.uuid4().hex[:8]}@fixture.test"
        form = dict(BASE_FORM)
        form["first_name"] = f"Refcheck{tag.capitalize()}"
        form["email"] = email
        form["_form_loaded_at"] = str(int(time.time() * 1000) - 5000)
        payload = {k: v for k, v in form.items() if k in known_names or k.startswith("_")}
        name = form["first_name"] + " " + form["last_name"]
        files = {
            "landlord_ref_primary": ("landlord_ref.pdf", gen_pdf_bytes(name, "landlord reference")),
            "employer_ref_primary": ("employer_ref.pdf", gen_pdf_bytes(name, "employer reference")),
        }
        code, body, _ = http("POST", f"/apply/{short_code}", payload,
                             headers=auth_headers(), cookies=cookie_str, files=files)
        if code not in (200, 201, 302):
            print(f"APPLY SUBMIT {tag} FAILED: HTTP {code}: {body[:300]}", file=sys.stderr)
            return 1
        row = psql(
            "SELECT id FROM application WHERE email = '%s' ORDER BY created_at DESC LIMIT 1" % email
        )
        if not row:
            print(f"APPLICATION ROW NOT FOUND for {email} (submit may have 500'd)", file=sys.stderr)
            return 1
        applications[tag] = {"email": email, "application_id": row}
        print(f"  {tag}: {email} -> application {row}")
        time.sleep(1.1)  # keep the timing gate honest between submits

    # 4. Walk each application to `viewed` (fires the RC2.3 trigger)
    for tag, app in applications.items():
        aid = app["application_id"]
        for status in ("under_review", "shortlisted", "viewed"):
            code, body, _ = http(
                "PATCH",
                f"/api/v1/vacancies/{vac_id}/applications/{aid}/status",
                {"status": status},
                headers=auth_headers(), cookies=cookie_str)
            if code not in (200, 201):
                print(f"STATUS {status} for {tag} FAILED: HTTP {code}: {body[:300]}", file=sys.stderr)
                return 1
        time.sleep(0.5)

    # 5. Reference calls should now exist (landlord_ref + employer_ref each)
    calls = {}
    for tag, app in applications.items():
        rows = psql(
            "SELECT ref_slot, id, status FROM reference_call "
            "WHERE application_id = '%s' ORDER BY ref_slot" % app["application_id"]
        ).splitlines()
        calls[tag] = {}
        for line in rows:
            if not line:
                continue
            slot, cid, status = line.split("|")
            calls[tag][slot] = {"id": cid, "status": status}
        print(f"  calls for {tag}: {calls[tag]}")

    # 6. Per-scenario state configuration (SQL)
    fmt_now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def call_id(tag, slot):
        return calls[tag][slot]["id"]

    # -- panel-renders: landlord_ref in-flight w/ attempts, employer_ref queued
    rid = call_id("renders", "landlord_ref")
    psql(
        "UPDATE reference_call SET status='contact_initiated', "
        "attempts='[{\"at\":\"%s\",\"channel\":\"email\",\"outcome\":\"delivered\",\"detail\":\"Invitation sent\"},"
        "{\"at\":\"%s\",\"channel\":\"email\",\"outcome\":\"delivered\",\"detail\":\"Reminder 1\"}]'::jsonb, "
        "attempt_count=2, next_attempt_at=now() + interval '10 days', "
        "form_token='fixture-renders-%s', form_token_expires_at=now() + interval '10 days' "
        "WHERE id='%s'" % (fmt_now, fmt_now, uuid.uuid4().hex[:12], rid)
    )

    # -- panel-correct (#611): employer_ref awaiting_correction (failed attempt)
    cid = call_id("correct", "employer_ref")
    psql(
        "UPDATE reference_call SET status='awaiting_correction', "
        "attempts='[{\"at\":\"%s\",\"channel\":\"email\",\"outcome\":\"failed\",\"detail\":\"Bounced — bad address\"}]'::jsonb, "
        "attempt_count=1, correction_cycles=0, next_attempt_at=now() + interval '10 days' "
        "WHERE id='%s'" % (fmt_now, cid)
    )

    # -- panel-substitute: landlord_ref objected (terminal, can substitute)
    sid = call_id("substitute", "landlord_ref")
    psql(
        "UPDATE reference_call SET status='objected', outcome='objected', "
        "terminal_reason='stop_received', attempts='[{\"at\":\"%s\",\"channel\":\"email\",\"outcome\":\"delivered\",\"detail\":\"Invitation sent\"}]'::jsonb, "
        "attempt_count=1, objected_at=now(), terminalized_at=now(), "
        "next_attempt_at=now() + interval '10 days' "
        "WHERE id='%s'" % (fmt_now, sid)
    )

    # -- panel-export (#615): employer_ref in-flight with 2 delivered attempts
    eid = call_id("export", "employer_ref")
    psql(
        "UPDATE reference_call SET status='contact_initiated', "
        "attempts='[{\"at\":\"%s\",\"channel\":\"email\",\"outcome\":\"delivered\",\"detail\":\"Invitation sent\"},"
        "{\"at\":\"%s\",\"channel\":\"sms\",\"outcome\":\"delivered\",\"detail\":\"Reminder 1\"}]'::jsonb, "
        "attempt_count=2, next_attempt_at=now() + interval '10 days' "
        "WHERE id='%s'" % (fmt_now, fmt_now, eid)
    )

    # -- referee-form-complete: landlord_ref contact_initiated + LIVE form token
    fid = call_id("form-complete", "landlord_ref")
    form_token = "fixture-form-" + uuid.uuid4().hex[:24]
    psql(
        "UPDATE reference_call SET status='contact_initiated', "
        "attempts='[{\"at\":\"%s\",\"channel\":\"email\",\"outcome\":\"delivered\",\"detail\":\"Invitation sent\"}]'::jsonb, "
        "attempt_count=1, next_attempt_at=now() + interval '10 days', "
        "form_token='%s', form_token_expires_at=now() + interval '10 days' "
        "WHERE id='%s'" % (fmt_now, form_token, fid)
    )

    report = {
        "base_url": BASE,
        "vacancy_id": vac_id,
        "short_code": short_code,
        "landlord_id": login["data"]["id"],
        "applications": {
            tag: {
                "email": apps["email"],
                "application_id": apps["application_id"],
                "calls": calls[tag],
            }
            for tag, apps in applications.items()
        },
        "form_token": form_token,
    }
    with open("/tmp/refcheck-fixture-report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nFIXTURE REPORT: /tmp/refcheck-fixture-report.json")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
