#!/usr/bin/env python3
"""pr_ready_core — pure readiness evaluator for check-pr-ready (packet A).

Stdlib only. NO subprocess, NO env, NO filesystem: every input is a plain
dict/list captured by the collector (bin/check-pr-ready). This module is the
single source of decision truth so the readiness policy is unit-testable
without faking tools (2026-09-12 audit R01–R04).

Contract (2026-09-12 selected-fixes commission):
  verdict ∈ {READY, NOT_READY, UNKNOWN}   (a definite blocker > an evidence
  gap > ready: NOT_READY wins when both exist)
  exit     0 = READY (qualified-ready stays 0 with an explicit banner)
           1 = NOT_READY (blockers)
           2 = UNKNOWN  (evidence/tool gaps — never affirmative)
  reason codes: CI_FAILED, CI_PENDING, CI_UNKNOWN, REVIEW_REQUIRED,
      REVIEW_STALE, REVIEWER_MISMATCH, IDENTITY_MISMATCH, TOOL_ERROR,
      STATE_INVALID, DRAFT, CONFLICTED, JOB_INVALID, QUALIFIED
      (informational). EVIDENCE_MISSING is emitted in BOTH classes — as a
      blocker (exit 1: null/UNKNOWN mergeability, required-check evidence
      missing) and as an unknown (exit 2: sparse payloads) — consumers
      must key on the verdict/exit, not on that code alone.

Preserved-current-policy decisions (deliberate, not regressions):
  - ALL reported failing checks block (not required-only; R05 not selected).
  - NEUTRAL/SKIPPED conclusions pass; CANCELLED fails (current behavior).
  - Same-reviewer newer APPROVED clears their older CHANGES_REQUESTED; a
    different reviewer's outstanding CHANGES_REQUESTED still blocks.
  - pr_review=0 keeps the ordinary-review route (any known-actor APPROVED at
    the current head); pr_review=1 or --require-perkins requires the
    canonical Perkins actor EXACTLY (never substring).
"""
from __future__ import annotations

import re

READY = "READY"
NOT_READY = "NOT_READY"
UNKNOWN = "UNKNOWN"

# Canonical Perkins reviewer: the `perkins-review` GitHub App posts reviews
# with author.login == "perkins-review[bot]" (bin/perkins-token contract,
# playbook 'Perkins', nefario REVIEW_ACTIONS). EXACT match only — R03.
PERKINS_ACTOR = "perkins-review[bot]"

_PR_URL = re.compile(r"^https?://([^/]+)/([^/]+)/([^/]+)/pull/(\d+)", re.I)
_SEG = re.compile(r"^[A-Za-z0-9_.-]+$")
_SCP_LIKE = re.compile(r"^[^@/\s]+@([^:/\s]+):(.+)$")
_URL_LIKE = re.compile(
    r"^[a-zA-Z][a-zA-Z0-9+.-]*://(?:[^@/\s]+@)?([^/:\s]+)(?::\d+)?[/:](.+)$"
)

CHECKRUN_FAIL = {
    "FAILURE",
    "TIMED_OUT",
    "CANCELLED",
    "ERROR",
    "ACTION_REQUIRED",
    "STARTUP_FAILURE",
    "STALE",
}
CHECKRUN_PASS = {"SUCCESS"}
CHECKRUN_SKIP = {"NEUTRAL", "SKIPPED"}
SC_PASS = {"SUCCESS"}
SC_FAIL = {"FAILURE", "ERROR"}
SC_PENDING = {"PENDING", "EXPECTED"}


class Result:
    """Aggregated evaluation outcome. blockers→NOT_READY, unknowns→UNKNOWN,
    warns are informational only."""

    def __init__(self):
        self.blockers: list[tuple[str, str]] = []  # (reason, message)
        self.unknowns: list[tuple[str, str]] = []
        self.warns: list[str] = []
        self.info: list[str] = []
        self.qualified = False
        self.needs_required_gates = False  # CI looks clean; collector should establish required gates

    @property
    def status(self) -> str:
        if self.blockers:
            return NOT_READY
        if self.unknowns:
            return UNKNOWN
        return READY

    @property
    def reasons(self) -> list[str]:
        return [r for r, _ in self.blockers] + [r for r, _ in self.unknowns]

    def exit_code(self) -> int:
        return {READY: 0, NOT_READY: 1, UNKNOWN: 2}[self.status]


# ── identity (R04) ────────────────────────────────────────────────────


def parse_remote(url: str | None) -> tuple[str, str, str] | None:
    """origin remote URL -> (host, owner, repo) or None.

    Handles https://, http://, ssh://, git://, scp-like git@host:path, and
    bare owner/repo. Common forms must NOT collapse to the repo segment
    (the old double-rsplit bug: every common remote returned None).
    """
    if not url:
        return None
    u = url.strip().rstrip("/")
    if u.endswith(".git"):
        u = u[:-4]
    host: str | None = None
    path: str | None = None
    m = _URL_LIKE.match(u)
    if m:
        host, path = m.group(1), m.group(2)
    else:
        m = _SCP_LIKE.match(u)
        if m:
            host, path = m.group(1), m.group(2)
        elif "/" in u and "://" not in u and ":" not in u:
            host, path = "github.com", u
    if not host or not path:
        return None
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[-2], parts[-1]
    if not _SEG.match(owner) or not _SEG.match(repo):
        return None
    return host.lower(), owner, repo


def parse_pr_ref(value) -> dict | None:
    """Ledger `pr` field -> {'kind','number',[host,owner,repo]} or None."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    if re.fullmatch(r"\d+", s):
        return {"kind": "number", "number": s}
    m = _PR_URL.match(s)
    if m:
        return {
            "kind": "url",
            "number": m.group(4),
            "host": m.group(1).lower(),
            "owner": m.group(2),
            "repo": m.group(3),
        }
    return None


def resolve_identity(
    job: dict, remote_url: str | None
) -> tuple[dict | None, list[tuple[str, str]], list[str]]:
    """One validated identity across ledger repo / remote / PR URL.

    Returns (pr_ref-with-slug, identity-problems, info-lines). Bare numbers
    resolve from the remote or a full-slug ledger `repo`; they NEVER inherit
    an ambient repo. Conflicting identities are rejected, not trusted.
    """
    problems: list[tuple[str, str]] = []
    info: list[str] = []
    ref = parse_pr_ref(job.get("pr"))
    if ref is None:
        problems.append(
            ("IDENTITY_MISMATCH",
             f"pr field '{job.get('pr')}' is neither a GitHub PR URL nor a bare number")
        )
        return None, problems, info

    remote = parse_remote(remote_url)
    remote_slug = f"{remote[1]}/{remote[2]}" if remote else None
    if remote:
        info.append(f"origin remote: {remote[0]} {remote_slug}")

    ledger_repo = (str(job.get("repo") or "")).strip()
    ledger_slug = None
    if "/" in ledger_repo:
        segs = ledger_repo.split("/")
        if len(segs) == 2 and _SEG.match(segs[0]) and _SEG.match(segs[1]):
            ledger_slug = ledger_repo

    if ref["kind"] == "url":
        if ref["host"] != "github.com":
            problems.append(
                ("IDENTITY_MISMATCH",
                 f"PR URL host '{ref['host']}' is not github.com (IDENTITY_MISMATCH)")
            )
        url_slug = f"{ref['owner']}/{ref['repo']}"
        if remote_slug and remote_slug.lower() != url_slug.lower():
            problems.append(
                ("IDENTITY_MISMATCH",
                 f"identity conflict: PR URL says {url_slug} but repo_root origin says {remote_slug} (IDENTITY_MISMATCH)")
            )
        if ledger_slug and ledger_slug.lower() != url_slug.lower():
            problems.append(
                ("IDENTITY_MISMATCH",
                 f"identity conflict: PR URL says {url_slug} but ledger repo says {ledger_slug} (IDENTITY_MISMATCH)")
            )
        ref["slug"] = url_slug
        return ref, problems, info

    # bare number: needs an explicit canonical slug — never ambient
    slug = None
    if remote_slug and remote and remote[0] == "github.com":
        slug = remote_slug
    if remote and remote[0] != "github.com":
        # R04 host integrity: the origin remote lives on a non-github host —
        # resolving a bare PR number against github.com would be a silent
        # host coercion (possibly a different repo with the same slug).
        problems.append(
            ("IDENTITY_MISMATCH",
             f"origin remote is on non-github host '{remote[0]}' ({remote_slug}) — refusing to "
             "resolve a bare PR number against github.com")
        )
        return None, problems, info
    if not slug and ledger_slug:
        slug = ledger_slug
        info.append(f"bare PR number: using full-slug ledger repo {slug}")
    if not slug:
        problems.append(
            ("IDENTITY_MISMATCH",
             "bare PR number but owner/repo cannot be derived (repo_root origin "
             "unreadable/non-github and ledger repo is not a full owner/repo slug) "
             "(IDENTITY_MISMATCH) — refusing ambient-repo lookup")
        )
        return None, problems, info
    if remote_slug and ledger_slug and remote_slug.lower() != ledger_slug.lower():
        problems.append(
            ("IDENTITY_MISMATCH",
             f"identity conflict: origin says {remote_slug} but ledger repo says {ledger_slug} (IDENTITY_MISMATCH)")
        )
        return None, problems, info
    ref["slug"] = slug
    return ref, problems, info


# ── CI classification (R01) ───────────────────────────────────────────


def classify_check(item) -> tuple[str, str, str]:
    """One rollup item -> (name, outcome, detail). outcome ∈
    PASS/PENDING/FAIL/SKIP/UNKNOWN. Normalizes BOTH schemas:
    CheckRun {__typename,name,status,conclusion} and
    StatusContext {__typename,context,state}."""
    if not isinstance(item, dict):
        return "unknown", "UNKNOWN", "rollup item is not an object"
    tname = item.get("__typename")
    name = str(item.get("name") or item.get("context") or "unknown")
    if tname == "StatusContext" or (tname is None and isinstance(item.get("state"), str)):
        state = (item.get("state") or "").upper()
        if state in SC_PASS:
            return name, "PASS", f"StatusContext {name} state=SUCCESS"
        if state in SC_FAIL:
            return name, "FAIL", f"StatusContext {name} state={state} (legacy status FAILURE/ERROR)"
        if state in SC_PENDING:
            return name, "PENDING", f"StatusContext {name} state={state}"
        return name, "UNKNOWN", f"StatusContext {name} state={state or 'missing'}"
    # CheckRun (by __typename, or by shape when typename absent)
    status = (item.get("status") or "").upper()
    concl = (item.get("conclusion") or "").upper()
    if status and status != "COMPLETED":
        return name, "PENDING", f"CheckRun {name} status={status}"
    if not status:
        return name, "UNKNOWN", f"CheckRun {name} status missing"
    if concl in CHECKRUN_PASS:
        return name, "PASS", f"CheckRun {name} conclusion=SUCCESS"
    if concl in CHECKRUN_SKIP:
        return name, "SKIP", f"CheckRun {name} conclusion={concl} (permitted)"
    if concl in CHECKRUN_FAIL:
        return name, "FAIL", f"CheckRun {name} conclusion={concl}"
    return name, "UNKNOWN", f"CheckRun {name} conclusion={concl or 'missing'}"


def classify_rollup(rollup):
    """rollup -> (passes, pending, fails, unknowns, skips) as (name, detail)."""
    passes, pending, fails, unknowns, skips = [], [], [], [], []
    for item in rollup or []:
        name, outcome, detail = classify_check(item)
        {
            "PASS": passes,
            "PENDING": pending,
            "FAIL": fails,
            "UNKNOWN": unknowns,
            "SKIP": skips,
        }[outcome].append((name, detail))
    return passes, pending, fails, unknowns, skips


# ── reviews (R02 head binding + R03 actor policy) ─────────────────────


def evaluate_reviews(
    reviews, head_oid: str | None, require_perkins: bool, review_decision
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[str]]:
    """-> (blockers, unknowns, info).

    An approval counts ONLY when: known actor, APPROVED is the reviewer's
    latest stance, AND it is bound to the exact current head via
    review.commit.oid. Missing actor never counts as approval (R03).
    """
    blockers: list[tuple[str, str]] = []
    unknowns: list[tuple[str, str]] = []
    info: list[str] = []

    if not isinstance(reviews, list):
        return blockers, [("EVIDENCE_MISSING", "reviews payload is not a list (schema)")], info
    if not all(isinstance(r, dict) for r in reviews):
        return blockers, [("EVIDENCE_MISSING", "reviews payload contains a non-object entry (schema)")], info

    # per-reviewer LATEST stance (correct current semantics — preserved).
    # Defensive sort key: a non-dict entry (schema drift) must not crash.
    latest: dict[str, dict] = {}
    for r in sorted(
        reviews,
        key=lambda r: (r.get("submittedAt") or "") if isinstance(r, dict) else "",
    ):
        if not isinstance(r, dict):
            continue
        state = r.get("state")
        if state not in ("APPROVED", "CHANGES_REQUESTED"):
            continue
        author = r.get("author")
        login = author.get("login") if isinstance(author, dict) else None
        who = login or "?"
        latest[who] = {"state": state, "login": login, "review": r}

    outstanding_cr = [w for w, s in latest.items() if s["state"] == "CHANGES_REQUESTED"]
    if outstanding_cr:
        blockers.append(
            ("REVIEW_REQUIRED",
             f"an outstanding CHANGES_REQUESTED review exists (latest verdict by: {', '.join(outstanding_cr)})")
        )

    valid_approvals: list[str] = []
    for who, s in latest.items():
        if s["state"] != "APPROVED":
            continue
        if not s["login"]:
            unknowns.append(
                ("EVIDENCE_MISSING",
                 "an APPROVED review has a missing author login — cannot attribute, does not count as approval")
            )
            continue
        if head_oid is None:
            unknowns.append(
                ("EVIDENCE_MISSING",
                 f"APPROVED by {who} but the PR head could not be established — cannot bind review provenance")
            )
            continue
        commit = s["review"].get("commit")
        oid = commit.get("oid") if isinstance(commit, dict) else None
        if oid is None:
            unknowns.append(
                ("EVIDENCE_MISSING",
                 f"APPROVED by {who} carries no commit provenance — cannot bind to head {head_oid[:7]}")
            )
        elif oid != head_oid:
            blockers.append(
                ("REVIEW_STALE",
                 f"APPROVED by {who} is at head {oid[:7]}, current head is {head_oid[:7]} (REVIEW_STALE)")
            )
        else:
            valid_approvals.append(who)

    # aggregate reviewDecision (authoritative branch-protection signal)
    rd = review_decision.upper() if isinstance(review_decision, str) else ""
    if rd == "CHANGES_REQUESTED":
        blockers.append(
            ("REVIEW_REQUIRED",
             "aggregate reviewDecision=CHANGES_REQUESTED (branch protection reports changes requested)")
        )
    elif rd == "REVIEW_REQUIRED":
        blockers.append(
            ("REVIEW_REQUIRED",
             "aggregate reviewDecision=REVIEW_REQUIRED (branch protection still requires review)")
        )

    if require_perkins:
        if PERKINS_ACTOR in valid_approvals:
            info.append(f"canonical Perkins actor {PERKINS_ACTOR} APPROVED at the current head")
        elif valid_approvals:
            # a current-head approval exists but from the wrong actor — the
            # definite mismatch case (R03)
            blockers.append(
                ("REVIEWER_MISMATCH",
                 f"approval at the current head is from {', '.join(valid_approvals)}, not the canonical {PERKINS_ACTOR} (REVIEWER_MISMATCH — exact actor required, never substring)")
            )
        elif PERKINS_ACTOR in latest:
            # Perkins approved but stale/unbound — the REVIEW_STALE /
            # EVIDENCE_MISSING entries above already describe that gap
            pass
        else:
            blockers.append(
                ("REVIEW_REQUIRED",
                 f"no APPROVED review at the current head — pr_review=1/--require-perkins requires the canonical {PERKINS_ACTOR} actor exactly")
            )
    elif not valid_approvals:
        blockers.append(
            ("REVIEW_REQUIRED",
             "no APPROVED review verdict at the current head — the minion's step-04 review must have posted one, or run Perkins")
        )
    return blockers, unknowns, info


# ── top-level evaluation ──────────────────────────────────────────────


def evaluate(
    job: dict,
    view: dict | None,
    reviews_payload: dict | None,
    remote_url: str | None,
    required_checks: list[str] | None,
    allow_pending: bool,
    require_perkins: bool,
) -> Result:
    """Pure policy evaluation. `view`/`reviews_payload` are parsed gh JSON
    (None = collection failed). `required_checks`: the established
    required-gate list ([] = positively none, None = could not establish)."""
    res = Result()

    # 1. job row
    status = job.get("status")
    if status not in ("in-review", "done"):
        res.blockers.append(
            ("JOB_INVALID", f"job status is '{status}', expected 'in-review' or 'done'")
        )
    if not job.get("pr"):
        res.blockers.append(
            ("JOB_INVALID", "no 'pr' recorded for this job (was it dispatched with pr=PR-number?)")
        )
    pr_review = job.get("pr_review")
    if pr_review is None or pr_review == "":
        pr_review = 0
    elif isinstance(pr_review, bool):
        res.unknowns.append(
            ("TOOL_ERROR", f"ledger pr_review value {pr_review!r} is not an integer (schema)")
        )
        return res
    elif isinstance(pr_review, int):
        pass
    elif isinstance(pr_review, str) and re.fullmatch(r"-?\d+", pr_review):
        pr_review = int(pr_review)
    else:
        res.unknowns.append(
            ("TOOL_ERROR", f"ledger pr_review value {pr_review!r} is not an integer (schema)")
        )
        return res
    if pr_review == 0:
        res.warns.append(
            "pr_review=0 — this job wasn't flagged for Perkins; if it's a large/risky change it should be 1"
        )

    # 2. identity
    ref, id_problems, id_info = resolve_identity(job, remote_url)
    res.info.extend(id_info)
    if id_problems:
        res.unknowns.extend(id_problems)
        return res

    # 3. PR state/schema (strict — sparse evidence is not affirmative)
    if view is None:
        res.unknowns.append(
            ("TOOL_ERROR", "PR lookup failed (gh error/non-JSON/timeout)")
        )
        return res
    if not isinstance(view, dict):
        res.unknowns.append(("EVIDENCE_MISSING", "PR view payload is not an object (schema)"))
        return res
    state = view.get("state")
    if not isinstance(state, str) or not state:
        res.unknowns.append(("EVIDENCE_MISSING", "PR view has no state field (sparse evidence)"))
        return res
    if state != "OPEN":
        res.blockers.append(("STATE_INVALID", f"PR state is '{state}', not OPEN"))
    if "isDraft" not in view or view.get("isDraft") is None:
        res.unknowns.append(("EVIDENCE_MISSING", "PR view has no isDraft field (sparse evidence)"))
    elif view.get("isDraft"):
        res.blockers.append(("DRAFT", "PR is a draft"))
    if "mergeable" not in view:
        res.unknowns.append(("EVIDENCE_MISSING", "PR view has no mergeable field (sparse evidence)"))
    else:
        mb = view.get("mergeable")
        if mb is None:
            res.blockers.append(
                ("EVIDENCE_MISSING",
                 "mergeable is null — GitHub has not established mergeability (not affirmative proof)")
            )
        elif mb == "UNKNOWN":
            res.blockers.append(
                ("EVIDENCE_MISSING", "mergeable=UNKNOWN — GitHub is still computing mergeability")
            )
        elif mb is False or mb == "CONFLICTING":
            res.blockers.append(("CONFLICTED", f"PR mergeable='{mb}' — has conflicts"))
        elif mb is not True and mb != "MERGEABLE":
            res.unknowns.append(
                ("EVIDENCE_MISSING", f"PR mergeable={mb!r} is an unrecognized value (schema)")
            )
    head_oid = view.get("headRefOid")
    if not isinstance(head_oid, str) or not head_oid:
        res.unknowns.append(
            ("EVIDENCE_MISSING",
             "PR view has no headRefOid — reviews and CI cannot be bound to a head (R02)")
        )

    # 4. CI (R01)
    if "statusCheckRollup" not in view or view.get("statusCheckRollup") is None:
        res.unknowns.append(
            ("EVIDENCE_MISSING", "PR view has no statusCheckRollup evidence (absent or null)")
        )
    else:
        passes, pending, fails, unknowns, _skips = classify_rollup(view.get("statusCheckRollup"))
        for n, d in fails:
            res.blockers.append(("CI_FAILED", f"CI check '{n}' failed — {d}"))
        if not fails:
            for n, d in unknowns:
                res.unknowns.append(
                    ("CI_UNKNOWN", f"CI check '{n}' outcome unknown — {d} (conservative UNKNOWN; not a pass)")
                )
            if not unknowns and pending:
                if allow_pending:
                    res.qualified = True
                    res.warns.append(
                        "QUALIFIED: pending check(s) tolerated via --allow-pending: "
                        + ", ".join(n for n, _ in pending)
                        + " — CI green is NOT established"
                    )
                else:
                    for n, d in pending:
                        res.blockers.append(
                            ("CI_PENDING",
                             f"CI check '{n}' is pending — {d} (use --allow-pending to tolerate explicitly)")
                        )
            # required gates (R01: no-gates-configured ≠ absent evidence).
            # --allow-pending applies here too: a REQUIRED gate that is
            # currently PENDING is the flag's exact use case — tolerated as
            # QUALIFIED (exit 0 + banner), never a silent blocker (the
            # I/O matrix's qualified-ready row).
            if not fails and not unknowns and not (pending and not allow_pending):
                pending_names = {n for n, _ in pending}
                if required_checks is None:
                    res.unknowns.append(
                        ("CI_UNKNOWN",
                         "required-gate set could not be established (branch protection/rulesets unreadable) "
                         "— cannot distinguish 'no gates configured' from 'required evidence missing'")
                    )
                    res.needs_required_gates = True
                else:
                    passed_names = {n for n, _ in passes}
                    missing = [
                        c for c in required_checks
                        if c not in passed_names
                        and not (allow_pending and c in pending_names)
                    ]
                    tolerated = [
                        c for c in required_checks
                        if c not in passed_names and allow_pending and c in pending_names
                    ]
                    if tolerated:
                        res.qualified = True
                        res.warns.append(
                            "QUALIFIED: required check(s) still pending, tolerated via --allow-pending: "
                            + ", ".join(tolerated)
                            + " — CI green is NOT established"
                        )
                    if missing:
                        res.blockers.append(
                            ("EVIDENCE_MISSING",
                             "required check(s) with no passing evidence: " + ", ".join(missing))
                        )

    # 5. reviews (R02/R03)
    if reviews_payload is None:
        res.unknowns.append(("TOOL_ERROR", "reviews lookup failed (gh error/non-JSON/timeout)"))
    else:
        reviews = (
            reviews_payload.get("reviews") if isinstance(reviews_payload, dict) else None
        )
        if not isinstance(reviews, list):
            res.unknowns.append(
                ("EVIDENCE_MISSING", "reviews payload has no reviews list (schema)")
            )
        else:
            rb, ru, ri = evaluate_reviews(
                reviews,
                head_oid if isinstance(head_oid, str) else None,
                require_perkins or pr_review == 1,
                view.get("reviewDecision"),
            )
            res.blockers.extend(rb)
            res.unknowns.extend(ru)
            res.info.extend(ri)

    return res
