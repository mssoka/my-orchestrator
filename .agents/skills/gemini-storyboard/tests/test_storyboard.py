import copy
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys

from google.genai import errors, types
import httpx
import pytest

from conftest import SCRIPT, live, png, save, sb


def leaves(v):
    if isinstance(v, dict):
        return [x for item in v.values() for x in leaves(item)]
    if isinstance(v, list):
        return [x for item in v for x in leaves(item)]
    return [v]


def test_contrasting_conditioning(project, tmp_path, fake_sdk):
    plans = []
    for variant in ("paper", "neon"):
        m, path = project(variant)
        run = sb.plan(path, tmp_path / "runs")
        _, p, blobs = sb.load_run(run)
        plans.append(p)
        before = copy.deepcopy(p)
        live(run, tmp_path / (variant + "-budget"))
        req = [v for k, v in fake_sdk[0] if k == "request"][-1]
        assert req["model"] == "gemini-3.1-flash-image"
        assert len(req["contents"]) == 1
        parts = req["contents"][0].parts
        payload = json.loads(parts[0].text.split("\n", 1)[1])
        for key in ("video", "style", "revision"):
            assert payload[key] == m[key]
        assert payload["shot"] == m["shots"][0]
        assert all(str(v) in parts[0].text for v in leaves(m["style"]))
        assert parts[1].text == "Reference ID: ref-0"
        assert parts[2].inline_data.data == blobs["ref-0"]
        assert parts[2].inline_data.mime_type == "image/png"
        assert req["config"].response_modalities == ["TEXT", "IMAGE"]
        assert req["config"].image_config.aspect_ratio == m["config"]["aspect_ratio"]
        assert req["config"].image_config.image_size == m["config"]["image_size"]
        assert req["config"].max_output_tokens == 4096
        client_args = [v for k, v in fake_sdk[0] if k == "client"][-1]
        assert client_args["vertexai"] is False
        assert client_args["api_key"] == "synthetic-sdk-boundary-key"
        # Exact SDK serialization; no client transport or incompatible response_format.
        wire = req["config"].model_dump(mode="json", exclude_none=True)
        assert wire["image_config"] == {"aspect_ratio": m["config"]["aspect_ratio"], "image_size": m["config"]["image_size"]}
        assert "response_format" not in wire
        assert payload["references"][0]["role"] == "character"
        options = client_args["http_options"]
        assert options.timeout == 120000
        assert options.retry_options.attempts == 1
        assert p == before
        assert p["selected"] == ["shot-0"] and len(p["excluded"]) == 2
    assert plans[0]["namespace"] != plans[1]["namespace"]
    assert plans[0]["conditioning_sha256"] != plans[1]["conditioning_sha256"]
    assert plans[0]["references"][0]["sha256"] != plans[1]["references"][0]["sha256"]


REQUIRED = [
    ("video",), ("style",), ("references",), ("shots",), ("approval",), ("config",), ("budget",), ("sampling",), ("revision",), ("run_id",),
    *(("video", k) for k in ("id", "title", "story")),
    *(("config", k) for k in ("model", "aspect_ratio", "image_size", "max_output_tokens", "timeout_ms")),
    *(("approval", k) for k in ("approved", "reviewer", "reviewed_at")),
    *(("shots", 0, k) for k in ("id", "status", "selected", "direction", "section", "timing", "reference_ids")),
    *(("references", 0, k) for k in ("id", "role", "path", "mime_type", "provenance", "external_use_allowed")),
    *(("style", k) for k in ("medium", "shape_language", "palette", "materials", "lighting", "camera", "composition", "mood", "continuity", "exclusions")),
    *(("shots", 0, "direction", k) for k in ("story_beat", "subjects", "action", "location", "framing", "lighting")),
    ("budget", "limit_usd"), ("budget", "max_attempts"), ("sampling", "stage"), ("sampling", "review_path")]


@pytest.mark.parametrize("keys", REQUIRED)
def test_required_omissions(project, tmp_path, keys):
    m, path = project()
    parent = m
    for k in keys[:-1]:
        parent = parent[k]
    del parent[keys[-1]]
    save(path, m)
    with pytest.raises(sb.StoryboardError, match="missing fields"):
        sb.plan(path, tmp_path / "runs")
    assert not (tmp_path / "runs").exists()


@pytest.mark.parametrize("keys,value,field", [
    (("shots", 0, "status"), "started", "shots.status"),
    (("shots", 0, "status"), "unknown", "shots.status"),
    (("shots", 0, "selected"), "yes", "shots.selected"),
    (("shots", 0, "reference_ids"), ["missing"], "reference_ids"),
    (("shots", 0, "reference_ids"), [], "reference_ids"),
    (("shots", 0, "start_frame"), "missing", "start_frame"),
    (("references", 0, "external_use_allowed"), False, "external_use_allowed"),
    (("references", 0, "external_use_allowed"), 1, "external_use_allowed"),
    (("references", 0, "provenance"), "", "provenance"),
    (("references", 0, "mime_type"), "image/jpeg", "MIME mismatch"),
    (("references", 0, "mime_type"), "text/plain", "mime_type"),
    (("references", 0, "path"), "missing.png", "references.path"),
    (("approval", "approved"), False, "approval.approved"),
    (("style",), {}, "style"),
    (("video", "story"), {"empty": ""}, "video.story.empty"),
    (("config", "model"), "gemini-other", "config.model"),
    (("config", "aspect_ratio"), "7:7", "aspect_ratio"),
    (("config", "image_size"), "8K", "image_size"),
    (("config", "max_output_tokens"), 32769, "max_output_tokens"),
    (("config", "timeout_ms"), True, "timeout_ms"),
    (("budget", "limit_usd"), "NaN", "limit_usd"),
    (("budget", "limit_usd"), "-1", "limit_usd"),
    (("budget", "max_attempts"), 0, "max_attempts"),
    (("run_id",), "../escape", "run_id"),
    (("shots", 0, "timing"), {"status": "unknown", "start_seconds": 3}, "timing"),
    (("shots", 0, "timing"), {"status": "explicit", "start_seconds": 4, "end_seconds": 2}, "timing"),
])
def test_invalid_manifest(project, tmp_path, keys, value, field):
    m, path = project()
    parent = m
    for k in keys[:-1]:
        parent = parent[k]
    parent[keys[-1]] = value
    save(path, m)
    with pytest.raises(sb.StoryboardError, match=field):
        sb.plan(path, tmp_path / "runs")


def test_malformed_reference(project, tmp_path):
    m, path = project()
    (path.parent / "ref-0.png").write_bytes(b"not PNG")
    with pytest.raises(sb.StoryboardError, match="malformed image"):
        sb.plan(path, tmp_path / "runs")


def test_duplicates_and_extra(project, tmp_path):
    for key in ("shots", "references"):
        m, path = project()
        m[key].append(copy.deepcopy(m[key][0]))
        save(path, m)
        with pytest.raises(sb.StoryboardError, match="duplicate ID"):
            sb.plan(path, tmp_path / "runs")
    m, path = project()
    m["config"]["response_format"] = "png"
    save(path, m)
    with pytest.raises(sb.StoryboardError, match="unknown fields"):
        sb.plan(path, tmp_path / "runs")
    path.write_text('{"style":{},"style":{}}')
    with pytest.raises(sb.StoryboardError, match="duplicate field"):
        sb.read_json(path)


def test_all_official_ratios_sizes(project, tmp_path):
    m, _ = project()
    for ratio in sorted(sb.RATIOS):
        for size in sorted(sb.SIZES):
            m["config"].update(aspect_ratio=ratio, image_size=size)
            p = sb.build_plan(m, {"ref-0": png("red")})
            req = sb.request(p, p["prompts"][0], {"ref-0": png("red")})
            assert req["config"].image_config.aspect_ratio == ratio
            assert req["config"].image_config.image_size == size
    assert len(sb.RATIOS) == 14


def test_deterministic_plan_and_revision(project, tmp_path):
    m, path = project()
    a = sb.plan(path, tmp_path / "a")
    b = sb.plan(path, tmp_path / "b")
    assert (a / "plan.json").read_bytes() == (b / "plan.json").read_bytes()
    with pytest.raises(sb.StoryboardError, match="already exists"):
        sb.plan(path, tmp_path / "a")
    m["revision"] = "v2"
    save(path, m)
    with pytest.raises(sb.StoryboardError, match="already exists"):
        sb.plan(path, tmp_path / "a")
    m["run_id"] = "revision-2"
    save(path, m)
    c = sb.plan(path, tmp_path / "a")
    assert sb.load_run(c)[1]["manifest_sha256"] != sb.load_run(a)[1]["manifest_sha256"]


@pytest.mark.parametrize("target", ["manifest", "plan", "reference"])
def test_immutable_input(planned, target):
    run, _, budget = planned
    if target == "reference":
        (run / "references/ref-0.png").write_bytes(png("blue"))
    else:
        path = run / (target + ".json")
        m = sb.read_json(path)
        m["tampered"] = True
        save(path, m)
    with pytest.raises(sb.StoryboardError, match="immutable"):
        live(run, budget)
    assert not (budget / "attempts.jsonl").exists()


def response(parts=(), finish="STOP", usage=None):
    return types.GenerateContentResponse(candidates=[types.Candidate(finish_reason=finish, content=types.Content(parts=list(parts)))], usage_metadata=usage)


def test_final_not_thought(planned, monkeypatch):
    run, _, budget = planned
    final, thought = png("red"), png("blue")
    monkeypatch.setattr(sb, "mock_response", lambda: response([
        types.Part(thought=True, text="SECRET THOUGHT"),
        types.Part(thought=True, inline_data=types.Blob(data=thought, mime_type="image/png")),
        types.Part.from_text(text="final <script>"), types.Part.from_bytes(data=final, mime_type="image/png")],
        usage=types.GenerateContentResponseUsageMetadata(prompt_token_count=10, candidates_token_count=20, thoughts_token_count=3, total_token_count=33)))
    receipts = sb.generate(run, budget, mock=True)
    r = receipts[0]
    base = run / "attempts" / r["reservation"]["attempt_id"]
    assert r["status"] == "success" and r["mode"] == "MOCK"
    assert r["thought_parts_ignored"] == 2
    assert r["usage"]["thoughts_token_count"] == 3 and r["usage_state"] == "reported"
    assert (base / "final.png").read_bytes() == final
    assert r["output"]["sha256"] == sb.digest(final)
    card = (base / "card.html").read_text()
    assert "MOCK" in card and 'href="final.png"' in card
    assert "&lt;script&gt;" in card and "<script>" not in card and "SECRET THOUGHT" not in card
    assert all(p.read_bytes() != thought for p in base.iterdir())
    before = {p.name: p.read_bytes() for p in base.iterdir()}
    assert sb.generate(run, budget, mock=True, resume=True) == []
    assert before == {p.name: p.read_bytes() for p in base.iterdir()}
    with pytest.raises(sb.StoryboardError, match="mock/dry"):
        sb.review_run(run, "Human", "approve", "Saw images", True)


@pytest.mark.parametrize("case,status", [("thought_only", "no_image"), ("text", "no_image"), ("refusal", "refusal"), ("blocked", "refusal"), ("malformed", "malformed"), ("mime", "malformed"), ("multiple", "malformed"), ("truncated", "incomplete"), ("empty", "no_image"), ("language", "refusal"), ("spii", "refusal"), ("image_other", "refusal"), ("image_recitation", "refusal"), ("other", "incomplete"), ("no_image_finish", "incomplete")])
def test_response_failures(planned, monkeypatch, case, status):
    run, _, budget = planned
    part = types.Part.from_bytes(data=png("red"), mime_type="image/png")
    responses = {
        "thought_only": response([types.Part(thought=True, inline_data=part.inline_data)]),
        "text": response([types.Part.from_text(text="No image available")]),
        "refusal": response([part], finish="SAFETY"),
        "blocked": types.GenerateContentResponse(prompt_feedback=types.GenerateContentResponsePromptFeedback(block_reason="SAFETY")),
        "malformed": response([types.Part.from_bytes(data=b"bad", mime_type="image/png")]),
        "mime": response([types.Part.from_bytes(data=png("red"), mime_type="image/jpeg")]),
        "multiple": response([part, part]), "truncated": response([part], finish="MAX_TOKENS"),
        "language": response([part], finish="LANGUAGE"), "spii": response([part], finish="SPII"),
        "image_other": response([part], finish="IMAGE_OTHER"), "image_recitation": response([part], finish="IMAGE_RECITATION"),
        "other": response([part], finish="OTHER"), "no_image_finish": response([part], finish="NO_IMAGE"),
        "empty": types.GenerateContentResponse()}
    monkeypatch.setattr(sb, "mock_response", lambda: responses[case])
    r = sb.generate(run, budget, mock=True)[0]
    assert r["status"] == status and r["output"] is None and r["usage_state"] == "unknown"
    assert not list(run.glob("attempts/*/final.*"))
    assert len((budget / "attempts.jsonl").read_text().splitlines()) == 1


@pytest.mark.parametrize("exc,status", [(TimeoutError(), "timeout"), (httpx.ReadTimeout("secret"), "timeout"), (httpx.ConnectError("secret"), "transport_error"), (errors.ServerError(503, {"error": {"message": "secret"}}), "transient_response"), (errors.ClientError(400, {"error": {"message": "secret"}}), "api_error")])
def test_error_no_implicit_retry(project, tmp_path, fake_sdk, exc, status):
    m, path = project(selected=(0, 1))
    run = sb.plan(path, tmp_path / "runs")
    budget = tmp_path / "budget"
    fake_sdk[1].append(exc)
    r = live(run, budget)[0]
    assert r["status"] == status and r["usage_state"] == "unknown" and r["output"] is None
    assert len([c for c in fake_sdk[0] if c[0] == "request"]) == 1
    assert "secret" not in json.dumps(r)
    assert len((budget / "attempts.jsonl").read_text().splitlines()) == 1
    if status != "transient_response":
        with pytest.raises(sb.StoryboardError, match="only recorded transient"):
            live(run, budget, retry_attempt=r["reservation"]["attempt_id"], allow_transient_retry=True)
    follow = live(run, budget, resume=True)
    assert [x["reservation"]["shot_id"] for x in follow] == ["shot-1"]


def test_manual_transient_retry(planned, fake_sdk):
    run, _, budget = planned
    fake_sdk[1].append(errors.ServerError(503, {"error": {"message": "unavailable"}}))
    first = live(run, budget)[0]
    aid = first["reservation"]["attempt_id"]
    with pytest.raises(sb.StoryboardError, match="permission"):
        live(run, budget, retry_attempt=aid)
    second = live(run, budget, retry_attempt=aid, allow_transient_retry=True)[0]
    assert second["status"] == "success" and second["reservation"]["retry_of"] == aid
    assert len(list(run.glob("attempts/*/receipt.json"))) == 2
    assert len((budget / "attempts.jsonl").read_text().splitlines()) == 2
    with pytest.raises(sb.StoryboardError, match="latest"):
        live(run, budget, retry_attempt=aid, allow_transient_retry=True)


def test_crash_after_reservation(project, tmp_path, fake_sdk):
    m, path = project(selected=(0, 1))
    run = sb.plan(path, tmp_path / "runs")
    budget = tmp_path / "budget"
    fake_sdk[1].append(KeyboardInterrupt())
    with pytest.raises(KeyboardInterrupt):
        live(run, budget)
    rows = [json.loads(x) for x in (budget / "attempts.jsonl").read_text().splitlines()]
    assert len(rows) == 1 and rows[0]["usage_state"] == "unknown"
    assert rows[0]["reserve_usd"] == "2.031616"
    assert not list(run.glob("attempts/*/receipt.json"))
    with pytest.raises(sb.StoryboardError, match="cannot read"):
        live(run, budget, retry_attempt=rows[0]["attempt_id"], allow_transient_retry=True)
    assert live(run, budget, resume=True)[0]["reservation"]["shot_id"] == "shot-1"


@pytest.mark.parametrize("cap,attempts,field", [("2", 9, "limit_usd"), ("20", 1, "max_attempts")])
def test_shared_budget(project, tmp_path, cap, attempts, field):
    budget = tmp_path / "shared"
    for i in range(2):
        m, path = project(run_id=f"run-{i}")
        m["budget"] = {"limit_usd": cap, "max_attempts": attempts}
        save(path, m)
        run = sb.plan(path, tmp_path / "runs")
        if cap == "2" or i == 1:
            with pytest.raises(sb.StoryboardError, match=field):
                sb.generate(run, budget, mock=True)
        else:
            sb.generate(run, budget, mock=True)
    assert sb.RESERVE == Decimal("2.031616")
    if (budget / "attempts.jsonl").exists():
        assert len((budget / "attempts.jsonl").read_text().splitlines()) == (0 if cap == "2" else 1)


def test_budget_binding_lock_corruption(planned, tmp_path):
    run, _, budget = planned
    sb.generate(run, budget, mock=True)
    with pytest.raises(sb.StoryboardError, match="binding mismatch"):
        sb.generate(run, tmp_path / "other", mock=True, resume=True)
    with sb.lock(budget):
        with pytest.raises(sb.StoryboardError, match="busy"):
            sb.generate(run, budget, mock=True, resume=True)
    with (budget / "attempts.jsonl").open("ab") as f:
        f.write(b'{"partial":')
    with pytest.raises(sb.StoryboardError, match="interrupted journal"):
        sb.generate(run, budget, mock=True, resume=True)


@pytest.mark.parametrize("kwargs", [{}, {"live": True}, {"live": True, "approved_by": "", "approval_id": "x", "accept_cost": True}, {"live": True, "approved_by": "executor", "approval_id": "x"}])
def test_live_positive_approval(planned, kwargs):
    run, _, budget = planned
    with pytest.raises(sb.StoryboardError, match="mode|live.approval"):
        sb.generate(run, budget, **kwargs)
    assert not (budget / "attempts.jsonl").exists()


def test_small_sample(project, tmp_path):
    m, path = project(selected=(0, 1, 2))
    extra = copy.deepcopy(m["shots"][0])
    extra["id"] = "fourth"
    m["shots"].append(extra)
    save(path, m)
    with pytest.raises(sb.StoryboardError, match="at most three"):
        sb.plan(path, tmp_path / "runs")


def expansion(project, tmp_path, review):
    m, path = project(run_id="expansion", stage="expansion", selected=(0, 1, 2))
    m["sampling"]["review_path"] = str(review)
    save(path, m)
    return sb.plan(path, tmp_path / "runs")


def test_expansion_rejects_dry_mock_missing(project, planned, tmp_path):
    sample, _, budget = planned
    target = expansion(project, tmp_path, sample / "review.json")
    with pytest.raises(sb.StoryboardError, match="cannot read"):
        live(target, budget)
    sb.generate(sample, budget, mock=True)
    sb.put_json(sample / "review.json", {"mode": "MOCK", "decision": "approve", "human_look_confirmed": True})
    with pytest.raises(sb.StoryboardError, match="approved real"):
        live(target, budget)


def test_real_shape_review_gate(project, planned, tmp_path, fake_sdk):
    sample, _, budget = planned
    live(sample, budget)
    with pytest.raises(sb.StoryboardError, match="actual human"):
        sb.review_run(sample, "Test human", "approve", "synthetic inspection")
    record = sb.review_run(sample, "Test human", "approve", "synthetic inspection", True)
    with pytest.raises(FileExistsError):
        sb.review_run(sample, "Test human", "approve", "cannot overwrite", True)
    target = expansion(project, tmp_path, sample / "review.json")
    assert len(live(target, budget)) == 3
    assert record["outputs"][0]["sha256"]


@pytest.mark.parametrize("mutation", ["reject", "output", "receipt", "scope", "reference", "mock_disguise"])
def test_review_tamper(project, planned, tmp_path, fake_sdk, mutation):
    sample, _, budget = planned
    live(sample, budget)
    sb.review_run(sample, "Test human", "approve", "synthetic inspection", True)
    m, path = project(run_id="expansion", stage="expansion", selected=(0, 1, 2))
    m["sampling"]["review_path"] = str(sample / "review.json")
    if mutation == "scope":
        m["style"]["lighting"] = "different"
    elif mutation == "reference":
        (path.parent / "ref-0.png").write_bytes(png("pink"))
    elif mutation == "output":
        next(sample.glob("attempts/*/final.png")).write_bytes(png("pink"))
    elif mutation == "receipt":
        rp = next(sample.glob("attempts/*/receipt.json"))
        data = sb.read_json(rp)
        data["usage"] = {"tamper": 1}
        save(rp, data)
    elif mutation == "mock_disguise":
        ep = sample / "execution.json"
        data = sb.read_json(ep)
        data["mode"] = "MOCK"
        save(ep, data)
    else:
        rp = sample / "review.json"
        data = sb.read_json(rp)
        data["decision"] = "reject"
        save(rp, data)
    save(path, m)
    target = sb.plan(path, tmp_path / "runs")
    before = len([c for c in fake_sdk[0] if c[0] == "client"])
    with pytest.raises(sb.StoryboardError, match="review"):
        live(target, budget)
    assert len([c for c in fake_sdk[0] if c[0] == "client"]) == before


@pytest.mark.parametrize("corruption", ["missing", "empty", "policy"])
def test_lost_budget_fails_closed(planned, corruption):
    run, _, budget = planned
    sb.generate(run, budget, mock=True)
    if corruption == "missing":
        (budget / "attempts.jsonl").unlink()
    elif corruption == "empty":
        (budget / "attempts.jsonl").write_bytes(b"")
    else:
        data = sb.read_json(budget / "policy.json")
        data["max_attempts"] = 999
        save(budget / "policy.json", data)
    with pytest.raises(sb.StoryboardError, match="budget"):
        sb.generate(run, budget, mock=True, resume=True)


def test_crash_before_local_attempt(project, tmp_path, monkeypatch):
    m, path = project(selected=(0, 1))
    run = sb.plan(path, tmp_path / "runs")
    budget = tmp_path / "budget"
    original = sb.put_json
    def crash(path, value):
        if Path(path).name == "reservation.json":
            raise KeyboardInterrupt()
        return original(path, value)
    monkeypatch.setattr(sb, "put_json", crash)
    with pytest.raises(KeyboardInterrupt):
        sb.generate(run, budget, mock=True)
    assert not (run / "attempts").exists()
    assert len((budget / "attempts.jsonl").read_text().splitlines()) == 1
    monkeypatch.setattr(sb, "put_json", original)
    follow = sb.generate(run, budget, mock=True, resume=True)
    assert [r["reservation"]["shot_id"] for r in follow] == ["shot-1"]


def test_plan_does_not_need_sdk(project, tmp_path, monkeypatch):
    _, path = project()
    def denied():
        raise AssertionError("SDK should not load for a plan")
    monkeypatch.setattr(sb, "sdk_types", denied)
    assert sb.plan(path, tmp_path / "runs").is_dir()


def test_run_lock_exclusion(planned):
    run, _, budget = planned
    with sb.lock(run):
        with pytest.raises(sb.StoryboardError, match="busy"):
            sb.generate(run, budget, mock=True)
    assert not budget.exists()


def test_explicit_timing_reaches_request(project, tmp_path):
    m, path = project()
    m["shots"][0]["timing"] = {"status": "explicit", "start_seconds": 1.5, "end_seconds": 3.0}
    save(path, m)
    _, p, blobs = sb.load_run(sb.plan(path, tmp_path / "runs"))
    req = sb.request(p, p["prompts"][0], blobs)
    payload = json.loads(req["contents"][0].parts[0].text.split("\n", 1)[1])
    assert payload["shot"]["timing"] == m["shots"][0]["timing"]


def test_cross_cwd_cli(project, tmp_path):
    _, path = project()
    # Minimal environment contains NO copied keys; sitecustomize denies every socket.
    trap = tmp_path / "trap"
    trap.mkdir()
    (trap / "sitecustomize.py").write_text('import socket\ndef deny(*a,**k): raise RuntimeError("NETWORK FORBIDDEN")\nsocket.socket.connect=deny\nsocket.create_connection=deny\nsocket.getaddrinfo=deny\n')
    env = {"PATH": str(Path(sys.executable).parent), "PYTHONPATH": str(trap), "PYTHONNOUSERSITE": "1"}
    def cli(*args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=tmp_path, env=env, capture_output=True, text=True)
    assert cli("--help").returncode == 0
    result = cli("plan", "--manifest", str(path), "--output-root", str(tmp_path / "runs"))
    assert result.returncode == 0, result.stderr
    run = result.stdout.strip()
    failed = cli("generate", "--run", run, "--budget-dir", str(tmp_path / "budget"), "--live")
    assert failed.returncode == 2 and "live.approval" in failed.stderr
    mocked = cli("generate", "--run", run, "--budget-dir", str(tmp_path / "budget"), "--mock")
    assert mocked.returncode == 0 and '"mode":"MOCK"' in mocked.stdout
