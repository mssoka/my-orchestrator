#!/usr/bin/env python3
"""Offline guard mutations in disposable copies; never edit the working helper."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/storyboard.py"
MUTATIONS = [
    ("key-mapping", 'api_key=require_key(), vertexai=False', 'vertexai=False', "test_opaque_key_mapping"),
    ("preflight-key", 'require_key()  # Pre-flight', 'pass  # Pre-flight', "test_no_sdk_credential_fallback"),
    ("required-style", 'object_fields(m["style"],', 'dict(m["style"]) if True else object_fields(m["style"],', "test_required_omissions"),
    ("eligibility", 'require(s["status"] == "not_started",', 'require(True,', "test_invalid_manifest"),
    ("cloud-permission", 'require(r["external_use_allowed"] is True,', 'require(True,', "test_invalid_manifest"),
    ("thought-filter", 'if getattr(part, "thought", False):', 'if False:', "test_final_not_thought"),
    ("budget-money", 'require(RESERVE * (len(rows) + 1) <= Decimal(m["budget"]["limit_usd"]),', 'require(True,', "test_shared_budget"),
    ("attempt-limit", 'require(len(rows) < m["budget"]["max_attempts"],', 'require(True,', "test_shared_budget"),
    ("sdk-retries", 'types.HttpRetryOptions(attempts=1)', 'types.HttpRetryOptions(attempts=2)', "test_contrasting_conditioning"),
    ("resume-skip", 'attempted = {r["shot_id"] for r in own}', 'attempted = set()', "test_final_not_thought"),
    ("expansion-gate", 'if m["sampling"]["stage"] != "expansion":', 'if True:', "test_expansion_rejects_dry_mock_missing"),
    ("snapshot-hash", 'require(p == build_plan(m, blobs),', 'require(True,', "test_immutable_input"),
    ("html-escape", 'esc = html.escape', 'esc = lambda value, **kwargs: value', "test_final_not_thought"),
]


def suite(root, targeted=None):
    args = [sys.executable, "-m", "pytest", str(root / "tests"), "-q", "--tb=short"]
    if targeted:
        args += ["-k", targeted]
    return subprocess.run(args, cwd=root, capture_output=True, text=True)


def main():
    original = SCRIPT.read_bytes()
    pristine = suite(ROOT)
    print(pristine.stdout, end="")
    if pristine.returncode != 0:
        print(pristine.stderr)
        return 1
    for name, old, new, target in MUTATIONS:
        source = original.decode()
        assert source.count(old) == 1, (name, "mutation anchor must be unique")
        with tempfile.TemporaryDirectory(prefix="gemini-storyboard-mutation-") as td:
            copy = Path(td) / "skill"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
            (copy / "scripts/storyboard.py").write_text(source.replace(old, new, 1))
            result = suite(copy, target)
            # Collection/import errors do NOT count as killed behavioral mutants.
            if result.returncode != 1 or " failed" not in result.stdout or "ERROR collecting" in result.stdout:
                print(f"SURVIVED/INVALID {name}\n{result.stdout}\n{result.stderr}")
                return 1
            print(f"KILLED {name}: {target}")
    assert SCRIPT.read_bytes() == original, "working helper changed"
    final = suite(ROOT)
    print(final.stdout, end="")
    print(f"{len(MUTATIONS)}/{len(MUTATIONS)} guard mutations killed; working helper unchanged")
    return final.returncode


if __name__ == "__main__":
    sys.exit(main())
