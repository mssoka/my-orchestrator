"""All images/manifests are synthetic and ephemeral. No credentials or network."""
import importlib.util
import io
import json
from pathlib import Path
import socket
import sys

import httpx
from PIL import Image
import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "storyboard.py"
spec = importlib.util.spec_from_file_location("storyboard", SCRIPT)
sb = importlib.util.module_from_spec(spec)
sys.modules["storyboard"] = sb
spec.loader.exec_module(sb)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError("NETWORK FORBIDDEN")
    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket.socket, "connect_ex", denied)
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)
    monkeypatch.setattr(httpx.Client, "send", denied)
    monkeypatch.setattr(httpx.AsyncClient, "send", denied)
    # Default client factory must not run, even if environment has credentials.
    monkeypatch.setattr(sb, "create_client", denied)


def png(color):
    buf = io.BytesIO()
    Image.new("RGB", (24, 16), color).save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def project(tmp_path):
    def make(variant="paper", run_id="sample-1", stage="sample", selected=(0,)):
        folder = tmp_path / variant
        folder.mkdir(exist_ok=True)
        paper = variant == "paper"
        for i in range(3):
            (folder / f"ref-{i}.png").write_bytes(png((30 + i, 150, 70) if paper else (210, 15 + i, 160)))
        m = {
            "schema_version": 1,
            "video": {"id": variant, "title": "Paper harbor <script>" if paper else "Neon desert", "story": {"premise": "folded boats reunite" if paper else "robot searches for a prism", "arc": ["arrival", "discovery"], "world": "miniature tidal library" if paper else "crystalline salt dunes"}},
            "run_id": run_id, "revision": "direction-v1",
            "approval": {"approved": True, "reviewer": "Synthetic human fixture", "reviewed_at": "2026-09-10T12:00:00Z"},
            "style": {"medium": "cut paper" if paper else "chrome raytrace", "palette": ["ochre", "teal"] if paper else ["magenta", "black"], "lighting": "diffuse dawn" if paper else "hard emissive rim", "camera": {"lens": "orthographic" if paper else "anamorphic"}, "shape_language": "folded wedges" if paper else "polished radial shells", "materials": "fiber paper" if paper else "reflective metal", "composition": "layered silhouettes" if paper else "vanishing-point symmetry", "mood": "tender" if paper else "severe", "continuity": "same creases" if paper else "same etched markings", "exclusions": "photoreal faces" if paper else "organic foliage"},
            "references": [{"id": f"ref-{i}", "role": "character" if i == 0 else "environment", "path": f"ref-{i}.png", "mime_type": "image/png", "provenance": f"synthetic {variant} RGB fixture {i}", "external_use_allowed": True} for i in range(3)],
            "shots": [{"id": f"shot-{i}", "status": "not_started", "selected": i in selected, "direction": {"story_beat": "arrival" if paper else "revelation", "subjects": "folded sailor" if paper else "chrome automaton", "action": f"{variant} action {i}", "location": "harbor" if paper else "desert", "framing": "wide asymmetric" if paper else "close axial", "lighting": "soft side light" if paper else "electric backlight", "emotion": "gentle" if paper else "urgent"}, "section": "verse" if paper else "unknown", "timing": {"status": "unknown"}, "reference_ids": [f"ref-{i}"], "start_frame": f"ref-{i}", "end_frame": f"ref-{i}"} for i in range(3)],
            "config": {"model": sb.MODEL, "aspect_ratio": "16:9" if paper else "3:4", "image_size": "1K" if paper else "2K", "max_output_tokens": 4096, "timeout_ms": 120000},
            "budget": {"limit_usd": "20", "max_attempts": 6},
            "sampling": {"stage": stage, "review_path": None}}
        path = folder / (run_id + ".json")
        path.write_text(json.dumps(m))
        return m, path
    return make


@pytest.fixture
def planned(project, tmp_path):
    m, path = project()
    return sb.plan(path, tmp_path / "runs"), m, tmp_path / "budget"


def save(path, m):
    path.write_text(json.dumps(m))


@pytest.fixture
def fake_sdk(monkeypatch):
    """Intercept official SDK boundary, NEVER HTTP. LIVE labels exist only in tmp tests."""
    from google import genai
    # Replace the entire environment mapping without reading a real key.
    monkeypatch.setattr(sb.os, "environ", {"GOOGLE_AI_API_KEY": "synthetic-sdk-boundary-key"})
    calls = []
    outcomes = []
    class Client:
        def __init__(self, **kwargs):
            calls.append(("client", kwargs))
            self.models = self
        def generate_content(self, **kwargs):
            calls.append(("request", kwargs))
            result = outcomes.pop(0) if outcomes else sb.mock_response()
            if isinstance(result, BaseException):
                raise result
            return result
        def close(self):
            calls.append(("close", {}))
    monkeypatch.setattr(genai, "Client", Client)
    # Restore only the real construction function from a separately loaded module;
    # its SDK Client boundary above is fake and transport traps remain active.
    fresh_spec = importlib.util.spec_from_file_location("storyboard_factory", SCRIPT)
    fresh = importlib.util.module_from_spec(fresh_spec)
    fresh_spec.loader.exec_module(fresh)
    monkeypatch.setattr(sb, "create_client", fresh.create_client)
    return calls, outcomes


def live(run, budget, **kwargs):
    return sb.generate(run, budget, live=True, approved_by="authorized-test-executor", approval_id="SYNTHETIC-TEST-NOT-APPROVAL", accept_cost=True, **kwargs)
