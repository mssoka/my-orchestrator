#!/usr/bin/env python3
"""Regression contract for the local BMad 6.12.0 renderer compatibility patch.

Run from the orchestrator root:
    uv run --python 3.11 test/test_bmad_renderer_short_config.py

The tracked bmad-build skill is intentionally left installer-owned. These tests
exercise it through the installed renderer, including mixed BMM+GDS config.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SOURCE = ROOT / "_bmad" / "scripts"
SKILL_SOURCE = ROOT / ".agents" / "skills" / "bmad-build"
PATCHED_RENDERER_SHA256 = "6b8752a0a0552c4d24221912c2ef5cf0a37539e060b19425e7433574d589738d"


def config(*, include_gds: bool = True, conflict: bool = False, missing: bool = False) -> str:
    bmm_implementation = "{project-root}/_bmad-output/implementation-artifacts"
    gds_implementation = (
        "{project-root}/_bmad-output/gds-implementation-artifacts"
        if conflict
        else bmm_implementation
    )
    lines = [
        "[core]",
        'communication_language = "English"',
        'document_output_language = "English"',
        "",
        "[modules.bmm]",
        'planning_artifacts = "{project-root}/_bmad-output/planning-artifacts"',
    ]
    if not missing:
        lines.append(f'implementation_artifacts = "{bmm_implementation}"')
    if include_gds:
        lines.extend(
            [
                "",
                "[modules.gds]",
                'planning_artifacts = "{project-root}/_bmad-output/planning-artifacts"',
            ]
        )
        if not missing:
            lines.append(f'implementation_artifacts = "{gds_implementation}"')
    return "\n".join(lines) + "\n"


class RendererFixture:
    def __init__(self, config_text: str, skill: Path = SKILL_SOURCE):
        self.temp = tempfile.TemporaryDirectory(prefix="bmad-render-regression-")
        outer = Path(self.temp.name)
        self.project = outer / "project"
        self.installed = outer / "installed-bmad"
        self.skill = skill
        (self.project / "nested" / "cwd").mkdir(parents=True)
        (self.installed / "scripts").mkdir(parents=True)
        for name in ("config_utils.py", "render_skill.py"):
            shutil.copy2(SCRIPT_SOURCE / name, self.installed / "scripts" / name)
        (self.installed / "config.toml").write_text(config_text, encoding="utf-8")
        (self.project / "_bmad").symlink_to(self.installed, target_is_directory=True)

    def close(self) -> None:
        self.temp.cleanup()

    def run(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(self.installed / "scripts" / "render_skill.py"),
                "--project-root",
                str(self.project),
                "--skill",
                str(self.skill),
            ],
            cwd=self.project / "nested" / "cwd",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )


class BmadRendererShortConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        required_paths = (
            SCRIPT_SOURCE / "render_skill.py",
            SCRIPT_SOURCE / "config_utils.py",
            SKILL_SOURCE,
        )
        for required in required_paths:
            self.assertTrue(required.exists(), f"required installed BMad path missing: {required}")
        renderer_hash = hashlib.sha256(
            (SCRIPT_SOURCE / "render_skill.py").read_bytes()
        ).hexdigest()
        self.assertEqual(renderer_hash, PATCHED_RENDERER_SHA256)

    def render(self, config_text: str) -> tuple[RendererFixture, subprocess.CompletedProcess[str]]:
        fixture = RendererFixture(config_text)
        self.addCleanup(fixture.close)
        return fixture, fixture.run()

    def assert_entry(self, result: subprocess.CompletedProcess[str]) -> Path:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1, result.stdout)
        prefix = "read and follow "
        self.assertTrue(lines[0].startswith(prefix), result.stdout)
        entry = Path(lines[0][len(prefix) :])
        self.assertTrue(entry.is_absolute(), entry)
        self.assertTrue(entry.is_file(), entry)
        return entry

    def test_equivalent_mixed_module_bindings_render_and_record_every_source(self) -> None:
        fixture, result = self.render(config())
        entry = self.assert_entry(result)
        generation = entry.parent
        manifest = json.loads((generation / "manifest.json").read_text(encoding="utf-8"))
        resolved_project = fixture.project.resolve()
        implementation = str(resolved_project / "_bmad-output" / "implementation-artifacts")
        planning = str(resolved_project / "_bmad-output" / "planning-artifacts")

        self.assertEqual(manifest["project_root"], str(resolved_project))
        self.assertTrue(str(entry).startswith(str(resolved_project / "_bmad" / "render" / "bmad-build")))
        resolved = manifest["inputs"]["resolved_values"]
        self.assertEqual(resolved["config.modules.bmm.implementation_artifacts"], implementation)
        self.assertEqual(resolved["config.modules.gds.implementation_artifacts"], implementation)
        self.assertEqual(resolved["config.modules.bmm.planning_artifacts"], planning)
        self.assertEqual(resolved["config.modules.gds.planning_artifacts"], planning)

        markdown = "\n".join(
            path.read_text(encoding="utf-8") for path in generation.rglob("*.md")
        )
        self.assertNotRegex(markdown, r"\{\{(?:\.|config\.)")
        self.assertNotIn("[[bmad-snapshot:", markdown)
        self.assertIn(implementation, markdown)
        self.assertIn(planning, markdown)

        required_instructions = {
            "workflow.md": "## READY FOR DEVELOPMENT STANDARD",
            "step-02-plan.md": "### CHECKPOINT 1",
            "step-03-implement.md": "### Tasks & Acceptance Verification",
            "step-04-review.md": "### Review",
            "step-05-present.md": "The verification and review result",
        }
        for name, needle in required_instructions.items():
            self.assertIn(needle, (generation / name).read_text(encoding="utf-8"), name)

    def test_conflicting_duplicate_short_binding_still_halts_with_paths(self) -> None:
        _, result = self.render(config(conflict=True))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("HALT: ambiguous config value `implementation_artifacts`", result.stdout)
        self.assertIn("modules.bmm.implementation_artifacts", result.stdout)
        self.assertIn("modules.gds.implementation_artifacts", result.stdout)
        self.assertNotIn("read and follow", result.stdout)

    def test_missing_short_binding_still_halts(self) -> None:
        _, result = self.render(config(missing=True))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("HALT: missing config value `implementation_artifacts`", result.stdout)
        self.assertNotIn("read and follow", result.stdout)

    def test_single_module_config_remains_compatible(self) -> None:
        fixture, result = self.render(config(include_gds=False))
        entry = self.assert_entry(result)
        manifest = json.loads((entry.parent / "manifest.json").read_text(encoding="utf-8"))
        resolved = manifest["inputs"]["resolved_values"]
        self.assertEqual(
            resolved["config.modules.bmm.implementation_artifacts"],
            str(fixture.project.resolve() / "_bmad-output" / "implementation-artifacts"),
        )
        self.assertNotIn("config.modules.gds.implementation_artifacts", resolved)


if __name__ == "__main__":
    unittest.main(verbosity=2)
