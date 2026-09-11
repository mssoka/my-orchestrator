"""Parent acceptance gaps: input semantics, opaque auth mapping, safe metadata."""
import copy
import json
from pathlib import Path
import re

from google.genai import types
import pytest

from conftest import live, png, save, sb


def test_opaque_key_mapping(planned, fake_sdk):
    run, _, budget = planned
    receipt = live(run, budget)[0]
    args = next(v for k, v in fake_sdk[0] if k == "client")
    assert args["api_key"] == "synthetic-sdk-boundary-key"
    for path in run.rglob("*"):
        if path.is_file():
            assert b"synthetic-sdk-boundary-key" not in path.read_bytes()
    assert receipt["model"] == "gemini-3.1-flash-image"
    assert receipt["sdk_version"] == "2.22.0"
    assert receipt["reference_hashes"]["ref-0"]
    assert receipt["pricing"]["actual_bill_usd"] is None


def test_no_sdk_credential_fallback(planned, fake_sdk, monkeypatch):
    """Pre-flight: a missing/misnamed key must never reserve or mislabel an attempt."""
    run, _, budget = planned
    monkeypatch.setattr(sb.os, "environ", {"GEMINI_API_KEY": "wrong-variable-test"})
    with pytest.raises(sb.StoryboardError, match="credentials"):
        live(run, budget)
    assert not fake_sdk[0]
    assert not (run / "attempts").exists()
    assert not (budget / "attempts.jsonl").exists()


def test_mock_rejects_live_flags_and_missing_run(planned, tmp_path):
    run, _, budget = planned
    with pytest.raises(sb.StoryboardError, match="live-only"):
        sb.generate(run, budget, mock=True, approved_by="x", approval_id="y", accept_cost=True)
    stray = tmp_path / "no-such-run"
    with pytest.raises(sb.StoryboardError, match="missing run snapshot"):
        sb.generate(stray, budget, mock=True)
    assert not stray.exists()
    with pytest.raises(sb.StoryboardError, match="--retry-attempt required"):
        sb.generate(run, budget, mock=True, allow_transient_retry=True)
    with pytest.raises(sb.StoryboardError, match="absolute"):
        sb.generate(run, "relative-budget", mock=True)


def test_template_rejected_as_shipped():
    template = Path(__file__).resolve().parents[1] / "templates" / "video.json"
    with pytest.raises(sb.StoryboardError):
        sb.validate(sb.read_json(template))


def test_main_exit_codes(project, tmp_path, monkeypatch):
    _, path = project()
    run = sb.plan(path, tmp_path / "runs")
    budget = tmp_path / "budget"
    assert sb.main(["generate", "--run", str(run), "--budget-dir", str(budget), "--mock"]) == 0
    _, path2 = project(run_id="exit-1")
    run2 = sb.plan(path2, tmp_path / "runs")
    failing = types.GenerateContentResponse(candidates=[types.Candidate(finish_reason="STOP", content=types.Content(parts=[types.Part.from_text(text="no image")]))])
    monkeypatch.setattr(sb, "mock_response", lambda: failing)
    assert sb.main(["generate", "--run", str(run2), "--budget-dir", str(budget), "--mock"]) == 1


def test_journal_schema_strict(planned):
    run, _, budget = planned
    sb.generate(run, budget, mock=True)
    path = budget / "attempts.jsonl"
    original = path.read_bytes()
    row = json.loads(original.splitlines()[0])
    row["extra"] = 1
    path.write_bytes(json.dumps(row).encode() + b"\n")
    with pytest.raises(sb.StoryboardError, match="unknown reservation fields"):
        sb.generate(run, budget, mock=True, resume=True)
    row = json.loads(original.splitlines()[0])
    row["sequence"] = 1.0
    path.write_bytes(json.dumps(row).encode() + b"\n")
    with pytest.raises(sb.StoryboardError, match="invalid reservation sequence"):
        sb.generate(run, budget, mock=True, resume=True)
    path.write_bytes(original)


def test_missing_budget_dir_not_refabricated(planned):
    run, _, budget = planned
    sb.generate(run, budget, mock=True)
    binding = sb.read_json(run / "execution.json")
    binding["mode"] = "LIVE"
    save(run / "execution.json", binding)
    import shutil
    shutil.rmtree(budget)
    with pytest.raises(sb.StoryboardError, match="missing; reconcile manually"):
        sb.review_run(run, "Human", "approve", "x", True)
    assert not budget.exists()


def test_oversized_request_rejected(project, tmp_path):
    import os
    import io as _io
    from PIL import Image
    m, path = project()
    buf = _io.BytesIO()
    Image.frombytes("RGB", (2800, 2000), os.urandom(2800 * 2000 * 3)).save(buf, format="PNG", compress_level=1)
    assert 19 * 1024 * 1024 < (len(buf.getvalue()) + 2) // 3 * 4 and len(buf.getvalue()) <= 20 * 1024 * 1024
    (path.parent / "ref-0.png").write_bytes(buf.getvalue())
    save(path, m)
    with pytest.raises(sb.StoryboardError, match="inline request too large"):
        sb.plan(path, tmp_path / "runs")
    assert not (tmp_path / "runs").exists()


def test_zero_budget_plan_not_execution(project, tmp_path):
    m, path = project()
    m["budget"]["limit_usd"] = "0"
    save(path, m)
    run = sb.plan(path, tmp_path / "runs")
    with pytest.raises(sb.StoryboardError, match="positive approved budget"):
        sb.generate(run, tmp_path / "budget", mock=True)
    assert not list(run.glob("attempts/*"))


def test_three_sample_two_with_five_dollars(project, tmp_path):
    m, path = project(selected=(0, 1, 2))
    m["budget"] = {"limit_usd": "5", "max_attempts": 3}
    save(path, m)
    run = sb.plan(path, tmp_path / "runs")
    with pytest.raises(sb.StoryboardError, match="conservative reserve"):
        sb.generate(run, tmp_path / "budget", mock=True)
    assert len(list(run.glob("attempts/*/final.png"))) == 2
    assert sb.RESERVE * 2 == sb.Decimal("4.063232")


def test_role_and_reference_count(project, tmp_path):
    m, _ = project()
    m["references"][0]["role"] = "unsupported"
    with pytest.raises(sb.StoryboardError, match="references.role"):
        sb.validate(m)
    m["references"][0]["role"] = "character"
    for i in range(4):
        r = copy.deepcopy(m["references"][0])
        r["id"] = f"character-{i}"
        m["references"].append(r)
        m["shots"][0]["reference_ids"].append(r["id"])
    with pytest.raises(sb.StoryboardError, match="maximum 14 references"):
        sb.validate(m)


def test_start_end_illustrations_and_contrasting_timing(project, tmp_path):
    paper, path = project(selected=(0, 1))
    for i, moment in enumerate(("start", "end")):
        paper["shots"][i]["illustration"] = moment
        paper["shots"][i]["direction"]["transformation"] = "folded boat opens into sail"
        paper["shots"][i]["timing"] = {"status": "explicit", "start_seconds": i * 4, "end_seconds": (i + 1) * 4}
    save(path, paper)
    _, pp, blobs = sb.load_run(sb.plan(path, tmp_path / "runs"))
    for i, moment in enumerate(("start", "end")):
        payload = json.loads(sb.request(pp, pp["prompts"][i], blobs)["contents"][0].parts[0].text.split("\n", 1)[1])
        assert payload["shot"]["illustration"] == moment
        assert payload["shot"]["timing"]["end_seconds"] == (i + 1) * 4
    neon, path = project("neon")
    _, np, _ = sb.load_run(sb.plan(path, tmp_path / "runs"))
    assert neon["shots"][0]["timing"] == {"status": "unknown"}
    assert pp["namespace"] != np["namespace"]


def test_package_links_and_discovery():
    root = Path(__file__).resolve().parents[1]
    skill = (root / "SKILL.md").read_text()
    assert skill.startswith("---\nname: gemini-storyboard\ndescription: ")
    assert len(skill.split("description: ", 1)[1].splitlines()[0]) <= 1024
    for doc in root.rglob("*.md"):
        if ".pytest_cache" in doc.parts:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if "://" not in target:
                assert (doc.parent / target.split("#", 1)[0]).exists(), (doc, target)


def test_dry_cards_are_not_images(planned):
    run, _, _ = planned
    data = (run / "plan.html").read_text()
    assert "NOT generated images" in data and "<img" not in data
    assert "&lt;script&gt;" in data and "<script>" not in data
    m, p, blobs = sb.load_run(run)
    req = sb.request(p, p["prompts"][0], blobs)
    payload = json.loads(req["contents"][0].parts[0].text.split("\n", 1)[1])
    assert "path" not in payload["references"][0]


def test_safety_and_modality_usage():
    response = types.GenerateContentResponse(candidates=[types.Candidate(
        finish_reason="SAFETY", safety_ratings=[types.SafetyRating(category="HARM_CATEGORY_DANGEROUS_CONTENT", probability="HIGH", blocked=True)])],
        usage_metadata=types.GenerateContentResponseUsageMetadata(prompt_token_count=20, candidates_token_count=30, thoughts_token_count=4, total_token_count=54,
            prompt_tokens_details=[types.ModalityTokenCount(modality="IMAGE", token_count=15)],
            candidates_tokens_details=[types.ModalityTokenCount(modality="IMAGE", token_count=25)]))
    result, image = sb.extract(response)
    assert result["status"] == "refusal" and image is None
    assert result["safety_ratings"][0]["blocked"] is True
    assert result["usage"]["candidates_tokens_details"][0]["token_count"] == 25
    assert result["usage"]["prompt_tokens_details"][0]["token_count"] == 15
    assert result["usage"]["thoughts_token_count"] == 4
