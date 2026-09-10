#!/usr/bin/env python3
"""Offline-first, single-turn storyboard look targets. See references/contract.md."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import sys
import uuid
import warnings

MODEL = "gemini-3.1-flash-image"
SDK_VERSION = "2.22.0"
RATIOS = {"1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"}
SIZES = {"512", "1K", "2K", "4K"}
MIMES = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
# Full model ceilings, ALL output priced at the higher image rate. Never refunded.
RESERVE = Decimal("131072") * Decimal("0.50") / 1000000 + Decimal("32768") * Decimal("60") / 1000000
CAVEAT = "Conservative reservation, NOT a bill or guaranteed price. Usage may be unknown. No free image tier. Prices checked 2026-09-10; reapprove if rates change. Targets are not animation/native-production proof."


class StoryboardError(ValueError):
    pass


def require(ok, field, message):
    if not ok:
        raise StoryboardError(f"{field}: {message}")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def object_fields(value, required, optional, field):
    require(isinstance(value, dict), field, "must be an object")
    require(not (set(required) - value.keys()), field, f"missing fields: {sorted(set(required) - value.keys())}")
    require(not (value.keys() - set(required) - set(optional)), field, f"unknown fields: {sorted(value.keys() - set(required) - set(optional))}")


def text(value, field):
    require(isinstance(value, str) and bool(value.strip()), field, "must be nonempty text")


def identifier(value, field):
    require(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", value), field, "must be a safe 1-64 character ID")


def direction(value, field):
    require(isinstance(value, dict) and bool(value), field, "must be a nonempty direction object")
    def visit(v, key):
        if isinstance(v, dict):
            require(bool(v), key, "empty object")
            for k, item in v.items():
                text(k, key)
                visit(item, key + "." + k)
        elif isinstance(v, list):
            require(bool(v), key, "empty list")
            for i, item in enumerate(v):
                visit(item, f"{key}[{i}]")
        else:
            text(v, key)
    visit(value, field)


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "json", f"duplicate field {key}")
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda v: (_ for _ in ()).throw(StoryboardError(f"json: invalid {v}")))
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise StoryboardError(f"json: cannot read {path} ({type(exc).__name__})") from exc


def validate(m):
    object_fields(m, ("schema_version", "video", "run_id", "revision", "approval", "style", "references", "shots", "config", "budget", "sampling"), (), "manifest")
    require(type(m["schema_version"]) is int and m["schema_version"] == 1, "schema_version", "must be 1")
    object_fields(m["video"], ("id", "title", "story"), (), "video")
    identifier(m["video"]["id"], "video.id")
    text(m["video"]["title"], "video.title")
    direction(m["video"]["story"], "video.story")
    identifier(m["run_id"], "run_id")
    text(m["revision"], "revision")
    direction(m["style"], "style")
    object_fields(m["style"], ("medium", "shape_language", "palette", "materials", "lighting", "camera", "composition", "mood", "continuity", "exclusions"), (), "style")
    a = m["approval"]
    object_fields(a, ("approved", "reviewer", "reviewed_at"), (), "approval")
    require(a["approved"] is True, "approval.approved", "approved direction required")
    text(a["reviewer"], "approval.reviewer")
    text(a["reviewed_at"], "approval.reviewed_at")
    c = m["config"]
    object_fields(c, ("model", "aspect_ratio", "image_size", "max_output_tokens", "timeout_ms"), (), "config")
    require(c["model"] == MODEL, "config.model", f"must be {MODEL}")
    require(isinstance(c["aspect_ratio"], str) and c["aspect_ratio"] in RATIOS, "config.aspect_ratio", "unsupported ratio")
    require(isinstance(c["image_size"], str) and c["image_size"] in SIZES, "config.image_size", "unsupported size")
    for key, maximum in (("max_output_tokens", 32768), ("timeout_ms", 3600000)):
        require(type(c[key]) is int and 1 <= c[key] <= maximum, "config." + key, f"integer 1..{maximum} required")
    b = m["budget"]
    object_fields(b, ("limit_usd", "max_attempts"), (), "budget")
    require(isinstance(b["limit_usd"], str), "budget.limit_usd", "decimal string required")
    try:
        amount = Decimal(b["limit_usd"])
    except InvalidOperation as exc:
        raise StoryboardError("budget.limit_usd: invalid decimal") from exc
    require(amount.is_finite() and amount >= 0, "budget.limit_usd", "nonnegative finite amount required; live execution needs positive budget")
    require(type(b["max_attempts"]) is int and b["max_attempts"] > 0, "budget.max_attempts", "positive integer required")
    require(isinstance(m["references"], list) and bool(m["references"]), "references", "nonempty list required")
    ids = set()
    for r in m["references"]:
        object_fields(r, ("id", "role", "path", "mime_type", "provenance", "external_use_allowed"), (), "references")
        require(r["role"] in ("character", "environment", "style", "object", "revision"), "references.role", "character/environment/style/object/revision required")
        identifier(r["id"], "references.id")
        require(r["id"] not in ids, "references.id", "duplicate ID")
        ids.add(r["id"])
        text(r["path"], "references.path")
        text(r["provenance"], "references.provenance")
        require(isinstance(r["mime_type"], str) and r["mime_type"] in MIMES, "references.mime_type", "PNG/JPEG/WebP required")
        require(type(r["external_use_allowed"]) is bool, "references.external_use_allowed", "boolean required")
    require(isinstance(m["shots"], list) and bool(m["shots"]), "shots", "nonempty list required")
    shot_ids, selected = set(), []
    for s in m["shots"]:
        object_fields(s, ("id", "status", "selected", "direction", "section", "timing", "reference_ids"), ("start_frame", "end_frame", "illustration"), "shots")
        text(s["section"], "shots.section")
        require(s.get("illustration", "single") in ("single", "start", "end"), "shots.illustration", "single/start/end required")
        if s.get("illustration", "single") != "single":
            require("transformation" in s["direction"], "shots.direction", "transformation state required for start/end illustrations")
        identifier(s["id"], "shots.id")
        require(s["id"] not in shot_ids, "shots.id", "duplicate ID")
        shot_ids.add(s["id"])
        require(type(s["selected"]) is bool, "shots.selected", "boolean required")
        require(s["status"] in ("not_started", "started", "unknown"), "shots.status", "not_started/started/unknown required")
        direction(s["direction"], "shots.direction")
        object_fields(s["direction"], ("story_beat", "subjects", "action", "location", "framing", "lighting"), ("emotion", "transformation"), "shots.direction")
        t = s["timing"]
        object_fields(t, ("status",), ("start_seconds", "end_seconds"), "shots.timing")
        require(t["status"] in ("unknown", "explicit"), "shots.timing.status", "unknown/explicit required")
        if t["status"] == "unknown":
            require(set(t) == {"status"}, "shots.timing", "unknown timing must not carry inferred values")
        else:
            for k in ("start_seconds", "end_seconds"):
                require(type(t.get(k)) in (int, float) and 0 <= t[k] < 1e9, "shots.timing." + k, "explicit finite nonnegative number required")
            require(t["end_seconds"] > t["start_seconds"], "shots.timing", "end must follow start")
        require(isinstance(s["reference_ids"], list) and bool(s["reference_ids"]), "shots.reference_ids", "nonempty list required")
        for rid in s["reference_ids"]:
            require(isinstance(rid, str) and rid in ids, "shots.reference_ids", "missing reference ID")
        require(len(s["reference_ids"]) == len(set(s["reference_ids"])), "shots.reference_ids", "duplicate ID")
        selected_refs = [r for r in m["references"] if r["id"] in s["reference_ids"]]
        characters = sum(r["role"] == "character" for r in selected_refs)
        require(len(selected_refs) <= 14 and characters <= 4 and len(selected_refs) - characters <= 10,
                "shots.reference_ids", "maximum 14 references: 4 character and 10 other images")
        for key in ("start_frame", "end_frame"):
            if key in s:
                require(isinstance(s[key], str) and s[key] in s["reference_ids"], "shots." + key, "must be a selected reference ID")
        if s["selected"]:
            require(s["status"] == "not_started", "shots.status", f"selected shot {s['id']} is not explicitly unstarted")
            selected.append(s)
    require(bool(selected), "shots.selected", "at least one shot required")
    used = {rid for s in selected for rid in s["reference_ids"]}
    for r in m["references"]:
        if r["id"] in used:
            require(r["external_use_allowed"] is True, "references.external_use_allowed", f"cloud permission required for {r['id']}")
    p = m["sampling"]
    object_fields(p, ("stage", "review_path"), (), "sampling")
    require(p["stage"] in ("sample", "expansion"), "sampling.stage", "sample/expansion required")
    if p["stage"] == "sample":
        require(len(selected) <= 3, "sampling", "initial sample is at most three illustrations")
        require(p["review_path"] is None, "sampling.review_path", "sample cannot cite a review")
    else:
        text(p["review_path"], "sampling.review_path")
        require(Path(p["review_path"]).is_absolute(), "sampling.review_path", "absolute path required")
    return selected, used


def image_bytes(data, mime, field):
    from PIL import Image
    require(mime in MIMES, field, "unsupported MIME")
    require(isinstance(data, bytes) and 0 < len(data) <= 20 * 1024 * 1024, field, "image must contain 1..20MiB bytes")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as im:
                require(Image.MIME.get(im.format) == mime, field, "bytes/MIME mismatch")
                im.verify()
            with Image.open(io.BytesIO(data)) as im:
                im.load()
    except StoryboardError:
        raise
    except Exception as exc:
        raise StoryboardError(f"{field}: malformed image ({type(exc).__name__})") from exc


def build_plan(m, blobs):
    selected, used = validate(m)
    refs = [{**r, "sha256": digest(blobs[r["id"]]), "stored_path": "references/" + r["id"] + MIMES[r["mime_type"]]} for r in m["references"] if r["id"] in used]
    conditioning = {"video": m["video"], "style": m["style"], "revision": m["revision"],
                    "references": [{k: v for k, v in r.items() if k not in ("path", "stored_path")} for r in refs]}
    prompts = []
    for shot in selected:
        payload = {"video": m["video"], "style": m["style"], "revision": m["revision"], "shot": shot,
                   "references": [{k: v for k, v in r.items() if k not in ("path", "stored_path")} for r in refs if r["id"] in shot["reference_ids"]]}
        prompt = ("Create ONE final storyboard image: a reference-conditioned look target, NOT animation or native-production proof. "
                  "Follow all supplied story, style, shot and frame direction. Timing marked unknown remains unknown; do not infer audio timing. "
                  "Reference labels identify the following image byte parts.\n" + canonical(payload).decode())
        require(len(prompt.encode()) + sum((len(blobs[rid]) + 2) // 3 * 4 for rid in shot["reference_ids"]) < 19 * 1024 * 1024,
                "request", "inline request too large; use smaller selected references (20MiB API limit, overhead reserved)")
        prompts.append({"shot_id": shot["id"], "text": prompt, "sha256": digest(prompt.encode()), "reference_ids": shot["reference_ids"]})
    # Gate binds the complete shot inventory (except selection), all references, and config.
    gate = {"video": m["video"], "style": m["style"], "revision": m["revision"], "config": m["config"],
            "shots": [{k: v for k, v in s.items() if k != "selected"} for s in m["shots"]],
            "references": [{k: v for k, v in r.items() if k != "path"} for r in m["references"]]}
    return {"schema_version": 1, "mode": "DRY_RUN_NOT_GENERATED_IMAGES", "manifest_sha256": digest(canonical(m)), "namespace": f"{m['video']['id']}/{m['run_id']}",
            "config": m["config"], "conditioning_sha256": digest(canonical(conditioning)), "look_scope_sha256": digest(canonical(gate)),
            "selected": [s["id"] for s in selected], "excluded": [{"shot_id": s["id"], "status": s["status"], "reason": "not selected"} for s in m["shots"] if not s["selected"]],
            "references": refs, "prompts": prompts, "reserve_per_attempt_usd": str(RESERVE),
            "initial_reserve_usd": str(RESERVE * len(selected)), "budget": m["budget"], "caveat": CAVEAT,
            "pricing": {"checked_at": "2026-09-10", "source": "https://ai.google.dev/gemini-api/docs/pricing", "actual_bill_usd": None}}


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def exclusive(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    sync_dir(path.parent)


def put_json(path, value):
    exclusive(path, canonical(value) + b"\n")


@contextmanager
def lock(directory):
    # POSIX advisory lock survives as a file; the kernel releases it on process death.
    import fcntl
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a+b") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise StoryboardError(f"lock: busy {directory}") from exc
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def plan(manifest_path, output_root):
    source = Path(manifest_path).resolve()
    m = read_json(source)
    _, used = validate(m)
    blobs = {}
    for r in m["references"]:
        if r["id"] not in used:
            continue
        try:
            data = (source.parent / r["path"]).read_bytes()
        except OSError as exc:
            raise StoryboardError(f"references.path: missing/unreadable {r['id']}") from exc
        image_bytes(data, r["mime_type"], "references." + r["id"])
        blobs[r["id"]] = data
    p = build_plan(m, blobs)
    run = Path(output_root).resolve() / m["video"]["id"] / m["run_id"]
    run.parent.mkdir(parents=True, exist_ok=True)
    try:
        run.mkdir()
    except FileExistsError as exc:
        raise StoryboardError("run_id: already exists; generate to resume, new run ID for revisions") from exc
    sync_dir(run.parent)
    put_json(run / "manifest.json", m)
    for r in p["references"]:
        exclusive(run / r["stored_path"], blobs[r["id"]])
    put_json(run / "plan.json", p)
    put_json(run / "seal.json", {"manifest_sha256": digest(canonical(m)), "plan_sha256": digest(canonical(p))})
    cards = ''.join('<article><h2>' + html.escape(q['shot_id']) + '</h2><pre>' + html.escape(q['text']) + '</pre></article>' for q in p['prompts'])
    exclusive(run / 'plan.html', ('<!doctype html><meta charset="utf-8"><h1>DRY RUN — NOT generated images</h1>' + cards).encode())
    return run


def load_run(run):
    run = Path(run).resolve()
    m, p, seal = (read_json(run / name) for name in ("manifest.json", "plan.json", "seal.json"))
    require(seal == {"manifest_sha256": digest(canonical(m)), "plan_sha256": digest(canonical(p))}, "run", "immutable input hash mismatch")
    _, used = validate(m)
    blobs = {}
    for r in m["references"]:
        if r["id"] in used:
            path = run / "references" / (r["id"] + MIMES[r["mime_type"]])
            try:
                blobs[r["id"]] = path.read_bytes()
            except OSError as exc:
                raise StoryboardError("run.references: missing snapshot") from exc
            image_bytes(blobs[r["id"]], r["mime_type"], "run.references")
    require(p == build_plan(m, blobs), "run", "immutable reference/plan mismatch")
    return m, p, blobs


def sdk_types():
    from importlib.metadata import version
    require(version("google-genai") == SDK_VERSION, "sdk", f"requires google-genai=={SDK_VERSION}")
    from google.genai import types
    return types


def request(p, prompt, blobs):
    types = sdk_types()
    refs = {r["id"]: r for r in p["references"]}
    parts = [types.Part.from_text(text=prompt["text"])]
    for rid in prompt["reference_ids"]:
        parts.append(types.Part.from_text(text="Reference ID: " + rid))
        parts.append(types.Part.from_bytes(data=blobs[rid], mime_type=refs[rid]["mime_type"]))
    c = p["config"]
    return {"model": MODEL, "contents": [types.Content(role="user", parts=parts)],
            "config": types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"], candidate_count=1,
                max_output_tokens=c["max_output_tokens"], image_config=types.ImageConfig(aspect_ratio=c["aspect_ratio"], image_size=c["image_size"]))}


def require_key():
    # Opaque in-process mapping; never read shell files, log or persist this value.
    key = os.environ.get("GOOGLE_AI_API_KEY")
    require(isinstance(key, str) and bool(key.strip()), "credentials", "GOOGLE_AI_API_KEY must be inherited from the configured shell")
    return key


def create_client(timeout_ms):
    # Only reached after positive live authorization, look gate, and durable reservation.
    from google import genai
    types = sdk_types()
    return genai.Client(api_key=require_key(), vertexai=False, http_options=types.HttpOptions(timeout=timeout_ms, retry_options=types.HttpRetryOptions(attempts=1)))


def mock_response():
    from PIL import Image
    types = sdk_types()
    buf = io.BytesIO()
    Image.new("RGB", (32, 32), "#627e91").save(buf, format="PNG")
    return types.GenerateContentResponse(candidates=[types.Candidate(finish_reason="STOP", content=types.Content(parts=[
        types.Part(thought=True, inline_data=types.Blob(data=buf.getvalue(), mime_type="image/png")),
        types.Part.from_text(text="MOCK synthetic image; no aesthetic acceptance."),
        types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png")]))])


def extract(response):
    usage = getattr(response, "usage_metadata", None)
    usage = usage.model_dump(mode="json", exclude_none=True) if usage is not None else None
    result = {"status": "no_image", "usage": usage, "usage_state": "reported" if usage else "unknown", "text": [], "thought_parts_ignored": 0}
    feedback = getattr(response, "prompt_feedback", None)
    result["prompt_safety_ratings"] = [v.model_dump(mode="json", exclude_none=True) for v in getattr(feedback, "safety_ratings", None) or []]
    block = getattr(feedback, "block_reason", None)
    if block and str(getattr(block, "value", block)) != "BLOCKED_REASON_UNSPECIFIED":
        result.update(status="refusal", block_reason=str(getattr(block, "value", block)))
        return result, None
    candidates = getattr(response, "candidates", None) or []
    if len(candidates) != 1:
        result["status"] = "malformed" if candidates else "no_image"
        return result, None
    candidate = candidates[0]
    result["safety_ratings"] = [v.model_dump(mode="json", exclude_none=True) for v in getattr(candidate, "safety_ratings", None) or []]
    finish = getattr(candidate, "finish_reason", None)
    finish = str(getattr(finish, "value", finish))
    result["finish_reason"] = finish
    if finish != "STOP":
        result["status"] = "refusal" if finish in {"SAFETY", "PROHIBITED_CONTENT", "BLOCKLIST", "RECITATION", "LANGUAGE", "SPII", "IMAGE_SAFETY", "IMAGE_PROHIBITED_CONTENT", "IMAGE_OTHER", "IMAGE_RECITATION"} else "incomplete"
        return result, None
    images = []
    for part in getattr(getattr(candidate, "content", None), "parts", None) or []:
        if getattr(part, "thought", False):
            result["thought_parts_ignored"] += 1
            continue
        if getattr(part, "text", None):
            result["text"].append(part.text)
        blob = getattr(part, "inline_data", None)
        if blob is not None:
            try:
                image_bytes(blob.data, blob.mime_type, "response.image")
            except StoryboardError:
                result["status"] = "malformed"
                return result, None
            images.append((blob.data, blob.mime_type))
    if len(images) == 1:
        result["status"] = "success"
        return result, images[0]
    if images:
        result["status"] = "malformed"
    return result, None


def journal(budget_dir, policy):
    policy_path = budget_dir / "policy.json"
    path = budget_dir / "attempts.jsonl"
    if not policy_path.exists():
        require(not path.exists(), "budget", "journal without policy")
        put_json(policy_path, policy)
        exclusive(path, b"")
    require(read_json(policy_path) == policy, "budget", "shared policy mismatch; do not change caps/mode")
    require(path.exists(), "budget", "missing journal; reconcile manually, never reset reservations")
    raw = path.read_bytes()
    require(not raw or raw.endswith(b"\n"), "budget", "interrupted journal; reconcile manually, never discard reservations")
    try:
        rows = [json.loads(line) for line in raw.splitlines()]
    except ValueError as exc:
        raise StoryboardError("budget: corrupt journal; reconcile manually") from exc
    expected_keys = {"sequence", "attempt_id", "run_path", "manifest_sha256", "shot_id", "mode", "reserve_usd", "reserved_at", "usage_state", "retry_of"}
    for index, row in enumerate(rows):
        require(set(row) == expected_keys, "budget", f"unknown reservation fields: {sorted(set(row) ^ expected_keys)}")
        require(type(row["sequence"]) is int and row["sequence"] == index + 1 and row["reserve_usd"] == str(RESERVE), "budget", "invalid reservation sequence/amount")
        for key in ("attempt_id", "run_path", "manifest_sha256", "shot_id", "mode"):
            text(row[key], "budget." + key)
    require(len({r["attempt_id"] for r in rows}) == len(rows), "budget", "duplicate attempt")
    return rows


def append_reservation(budget_dir, row):
    with (budget_dir / "attempts.jsonl").open("ab") as f:
        f.write(canonical(row) + b"\n")
        f.flush()
        os.fsync(f.fileno())
    sync_dir(budget_dir)


def evidence(run, m, p):
    binding = read_json(run / "execution.json")
    require(binding["mode"] == "LIVE", "review", "mock/dry evidence cannot authorize expansion")
    require(m["sampling"]["stage"] == "sample", "review", "real initial sample required")
    bdir = Path(binding["budget_dir"])
    require(bdir.is_dir(), "budget", "shared budget directory missing; reconcile manually, never re-fabricate reservations")
    with lock(bdir):
        rows = journal(bdir, {**m["budget"], "mode": "LIVE", "reserve_per_attempt_usd": str(RESERVE)})
    own = [r for r in rows if r["run_path"] == str(run) and r["manifest_sha256"] == p["manifest_sha256"]]
    outputs = []
    for sid in p["selected"]:
        attempts = [r for r in own if r["shot_id"] == sid]
        require(bool(attempts), "review", "sample not complete")
        latest = attempts[-1]
        base = run / "attempts" / latest["attempt_id"]
        receipt = read_json(base / "receipt.json")
        require(receipt["status"] == "success" and receipt["mode"] == "LIVE" and receipt["reservation"] == latest, "review", "sample lacks successful live receipt")
        output = receipt["output"]
        require(output["path"] == "final" + MIMES.get(output["mime_type"], "!"), "review", "invalid output path")
        data = (base / output["path"]).read_bytes()
        require(digest(data) == output["sha256"], "review", "output hash mismatch")
        image_bytes(data, output["mime_type"], "review.output")
        outputs.append({"shot_id": sid, "attempt_id": latest["attempt_id"], "sha256": output["sha256"], "receipt_sha256": digest(canonical(receipt))})
    return outputs


def expansion_gate(m, p):
    if m["sampling"]["stage"] != "expansion":
        return
    path = Path(m["sampling"]["review_path"]).resolve()
    require(path.name == "review.json", "sampling.review_path", "must reference immutable review.json")
    review = read_json(path)
    sample = path.parent
    sm, sp, _ = load_run(sample)
    require(review.get("decision") == "approve" and review.get("human_look_confirmed") is True and review.get("mode") == "LIVE", "review", "approved real human look review required")
    text(review.get("reviewer"), "review.reviewer")
    text(review.get("notes"), "review.notes")
    require(review.get("manifest_sha256") == sp["manifest_sha256"] and review.get("look_scope_sha256") == sp["look_scope_sha256"] == p["look_scope_sha256"], "review", "look scope changed; new sample required")
    require(review.get("outputs") == evidence(sample, sm, sp), "review", "sample evidence mismatch")
    # Any references shared with the sample must still match exact bytes.
    current = {r["id"]: r["sha256"] for r in p["references"]}
    for r in sp["references"]:
        if r["id"] in current:
            require(current[r["id"]] == r["sha256"], "review", "sample reference changed")


def review_run(run, reviewer, decision, notes, human_look_confirmed=False):
    run = Path(run).resolve()
    require((run / "manifest.json").is_file(), "run", "missing run snapshot; plan first")
    text(reviewer, "review.reviewer")
    text(notes, "review.notes")
    require(decision in ("approve", "reject"), "review.decision", "approve/reject required")
    require(human_look_confirmed is True, "review.human_look_confirmed", "actual human inspection must be confirmed")
    with lock(run):
        m, p, _ = load_run(run)
        outputs = evidence(run, m, p)
        record = {"decision": decision, "reviewer": reviewer, "notes": notes, "human_look_confirmed": True,
                  "reviewed_at": now(), "mode": "LIVE", "manifest_sha256": p["manifest_sha256"],
                  "look_scope_sha256": p["look_scope_sha256"], "outputs": outputs}
        put_json(run / "review.json", record)
    return record


def card(base, m, prompt, receipt):
    esc = html.escape
    output = receipt.get("output")
    image = f'<a href="{esc(output["path"], quote=True)}"><img alt="Storyboard look target" src="{esc(output["path"], quote=True)}" style="max-width:100%"></a>' if output else "<p>No output board.</p>"
    body = f'<!doctype html><meta charset="utf-8"><title>{esc(m["video"]["title"])}</title><h1>{receipt["mode"]} — {esc(prompt["shot_id"])} — {esc(receipt["status"])}</h1><p>{esc(CAVEAT)}</p>{image}<h2>Exact request prompt</h2><pre>{esc(prompt["text"])}</pre><h2>Receipt</h2><pre>{esc(canonical(receipt).decode())}</pre>'
    exclusive(base / "card.html", body.encode())


def generate(run, budget_dir, *, mock=False, live=False, approved_by=None, approval_id=None,
             accept_cost=False, resume=False, retry_attempt=None, allow_transient_retry=False):
    require(mock != live, "mode", "choose exactly one of --mock or --live")
    if mock:
        require(approved_by is None and approval_id is None and accept_cost is False, "mode", "approval/accept-cost flags are live-only")
    if live:
        require(isinstance(approved_by, str) and bool(approved_by.strip()) and isinstance(approval_id, str) and bool(approval_id.strip()) and accept_cost is True,
                "live.approval", "named authorized executor, approval ID and explicit cost acceptance required")
    require(bool(budget_dir) and Path(budget_dir).is_absolute(), "budget_dir", "explicit absolute shared budget directory required")
    run, bdir = Path(run).resolve(), Path(budget_dir).resolve()
    require((run / "manifest.json").is_file(), "run", "missing run snapshot; plan first")
    mode = "MOCK" if mock else "LIVE"
    with lock(run):
        m, p, blobs = load_run(run)
        require(Decimal(m["budget"]["limit_usd"]) > 0, "budget.limit_usd", "positive approved budget required for execution")
        expansion_gate(m, p)
        if live:
            require_key()  # Pre-flight before any reservation: a missing key must never spend an attempt.
        # Build official SDK objects for every selected shot before client creation/reservation.
        requests = {prompt["shot_id"]: request(p, prompt, blobs) for prompt in p["prompts"]}
        binding = {"budget_dir": str(bdir), "mode": mode, "approved_by": approved_by, "approval_id": approval_id, "accept_cost": accept_cost}
        if (run / "execution.json").exists():
            require(read_json(run / "execution.json") == binding, "run", "immutable execution/budget binding mismatch")
        else:
            put_json(run / "execution.json", binding)
        policy = {**m["budget"], "mode": mode, "reserve_per_attempt_usd": str(RESERVE)}
        with lock(bdir):
            rows = journal(bdir, policy)
        own = [r for r in rows if r["run_path"] == str(run)]
        local_attempts = {entry.name for entry in (run / "attempts").iterdir()} if (run / "attempts").exists() else set()
        require(local_attempts <= {r["attempt_id"] for r in own}, "budget", "local attempts missing from shared journal; reconcile manually")
        require(all(r["manifest_sha256"] == p["manifest_sha256"] for r in own), "run", "reservation manifest mismatch")
        require(not own or resume or retry_attempt, "resume", "existing attempts; use --resume for unattempted work only")
        retry_shot = None
        if retry_attempt:
            require(allow_transient_retry is True and not resume, "retry", "explicit transient retry permission required; cannot combine with resume")
            prior = next((r for r in own if r["attempt_id"] == retry_attempt), None)
            require(prior is not None, "retry", "attempt not found in this run")
            require(prior == [r for r in own if r["shot_id"] == prior["shot_id"]][-1], "retry", "only latest attempt is eligible")
            receipt = read_json(run / "attempts" / retry_attempt / "receipt.json")
            require(receipt["reservation"] == prior and receipt["status"] == "transient_response", "retry", "only recorded transient response; never timeout/unknown/transport")
            retry_shot = prior["shot_id"]
        else:
            require(not allow_transient_retry, "retry", "--retry-attempt required")
        attempted = {r["shot_id"] for r in own}
        work = [q for q in p["prompts"] if (q["shot_id"] == retry_shot if retry_shot else q["shot_id"] not in attempted)]
        receipts = []
        for prompt in work:
            with lock(bdir):
                rows = journal(bdir, policy)
                require(len(rows) < m["budget"]["max_attempts"], "budget.max_attempts", "shared attempt limit exhausted")
                require(RESERVE * (len(rows) + 1) <= Decimal(m["budget"]["limit_usd"]), "budget.limit_usd", "conservative reserve exceeds shared budget")
                reservation = {"sequence": len(rows) + 1, "attempt_id": uuid.uuid4().hex, "run_path": str(run),
                               "manifest_sha256": p["manifest_sha256"], "shot_id": prompt["shot_id"], "mode": mode,
                               "reserve_usd": str(RESERVE), "reserved_at": now(), "usage_state": "unknown", "retry_of": retry_attempt}
                append_reservation(bdir, reservation)
            base = run / "attempts" / reservation["attempt_id"]
            put_json(base / "reservation.json", reservation)
            put_json(base / "request.json", {"model": MODEL, "prompt": prompt, "config": p["config"], "reference_hashes": {rid: digest(blobs[rid]) for rid in prompt["reference_ids"]}})
            client = None
            image = None
            try:
                if mock:
                    response = mock_response()
                else:
                    client = create_client(m["config"]["timeout_ms"])
                    response = client.models.generate_content(**requests[prompt["shot_id"]])
                result, image = extract(response)
            except Exception as exc:
                import httpx
                from google.genai import errors
                if isinstance(exc, (TimeoutError, httpx.TimeoutException)):
                    status = "timeout"
                elif isinstance(exc, errors.APIError):
                    status = "transient_response" if exc.code in (429, 500, 502, 503, 504) else "api_error"
                else:
                    status = "transport_error"
                # Do not persist exception strings: SDK/auth failures can include sensitive material.
                result = {"status": status, "error_type": type(exc).__name__, "usage": None, "usage_state": "unknown"}
                if isinstance(exc, errors.APIError):
                    result["http_status"] = exc.code
            finally:
                if client is not None:
                    try:
                        client.close()
                    except Exception:
                        pass  # No new request, no retry, no loss of the generation outcome.
            receipt = {**result, "mode": mode, "model": MODEL, "sdk_version": SDK_VERSION,
                       "config": p["config"], "reference_hashes": {rid: digest(blobs[rid]) for rid in prompt["reference_ids"]},
                       "pricing": p["pricing"], "review_disposition": "pending_actual_look" if live else "MOCK_NOT_REVIEWABLE",
                       "reservation": reservation, "prompt_sha256": prompt["sha256"], "finished_at": now(), "output": None}
            if image is not None:
                data, mime = image
                name = "final" + MIMES[mime]
                exclusive(base / name, data)
                receipt["output"] = {"path": name, "mime_type": mime, "sha256": digest(data)}
            put_json(base / "receipt.json", receipt)
            card(base, m, prompt, receipt)
            receipts.append(receipt)
            if receipt["status"] != "success":
                break
        return receipts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("plan", help="validate and snapshot offline; never creates a client")
    p.add_argument("--manifest", required=True)
    p.add_argument("--output-root", required=True)
    g = commands.add_parser("generate", help="explicit MOCK or separately approved LIVE single-turn requests")
    g.add_argument("--run", required=True)
    g.add_argument("--budget-dir", required=True)
    modes = g.add_mutually_exclusive_group(required=True)
    modes.add_argument("--mock", action="store_true")
    modes.add_argument("--live", action="store_true")
    g.add_argument("--approved-by")
    g.add_argument("--approval-id")
    g.add_argument("--accept-cost", action="store_true")
    g.add_argument("--resume", action="store_true")
    g.add_argument("--retry-attempt")
    g.add_argument("--allow-transient-retry", action="store_true")
    r = commands.add_parser("review", help="record actual human inspection of a successful LIVE sample only")
    r.add_argument("--run", required=True)
    r.add_argument("--reviewer", required=True)
    r.add_argument("--decision", choices=("approve", "reject"), required=True)
    r.add_argument("--notes", required=True)
    r.add_argument("--human-look-confirmed", action="store_true")
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        if command == "plan":
            print(plan(args["manifest"], args["output_root"]))
        elif command == "review":
            print(canonical(review_run(**args)).decode())
        else:
            receipts = generate(**args)
            print(canonical(receipts).decode())
            return 0 if all(r["status"] == "success" for r in receipts) else 1
    except (StoryboardError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ImportError as exc:
        print(f"error: missing dependency ({exc.name}); install requirements.txt first", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
