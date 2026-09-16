# PP3D — root-fix the ambiguous implementation_artifacts (bmad-build halt class)

## Intake

The `implementation_artifacts` ambiguity halted ≥4 jobs across 3 days (pMY 09-09, gemini-storyboard core 09-10, test-parse-hotfix 09-11, +the original discovery). The sanctioned workaround = job-local qualified-token binding + reverse byte-equality + ONE corrected renderer bootstrap. This job = the ROOT fix, per user ruling 2026-09-11.

## Task

Qualify the two ambiguous `implementation_artifacts` tokens in the CANONICAL bmad-build skill files at the ROOT config (`/Users/moses/code/.agents/skills/bmad-build/` — bmm paths), using the SAME qualified-token form as the sanctioned job-local binding (reference the binding spec: `_bmad-output/briefings/gemini-storyboard-internal-unblock-2026-09-10.md`).

## Verification (mandatory)

Scratch render from a FRESH TEMP project-root against the ROOT `_bmad` (the config this fix changes): the render must resolve without the halt. Record hashes (skill files before/after + render output). A previous verified instance of this exact verification exists: the test-parse-hotfix job's binding proof (see its spec artifacts).

## Bounds

- Touch ONLY the root `.agents/skills/bmad-build/` skill files (the two tokens) — canonical skill, no other files.
- NO worktree/repo commits (the dir is untracked post-#28; the change IS the live canonical state).
- NO blanket edits to other skills; the aside-copy baseline of the whole `.agents/skills` tree is already refreshed at `_bmad-output/implementation-artifacts/agents-skills-aside-20260911/` (1238 files, hash-verified) — restore source if anything regresses.
- glm-5.3 @ max. No OpenAI. No editor/GUI.
- On ANY ambiguity beyond the two named tokens: stop, report, halt-class documented.

## Reporting

Self-report working at start; at the end: files changed + hashes + the scratch-render proof + self-report in-review. Silas administers any follow-up verification entries.
