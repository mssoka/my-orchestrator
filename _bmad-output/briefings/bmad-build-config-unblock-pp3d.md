# Ops unblock — bmad-build mixed-module config

## Task / authorization
Resolve the tooling prerequisite blocking `packet-plumber-3d-planet-life-router-legibility`, without changing its gameplay scope or bypassing bmad-build. Silas owns this as an independent small tooling/config lane; no new user-scope question is needed. Keep PP3D's existing pane/worktree intact. This is not a reason to switch model, skip review, hand-read unrendered workflow instructions, or kill/re-dispatch.

## Reported failure
The parent's once-only command was:
`uv run --no-cache "$PWD/_bmad/scripts/render_skill.py" --project-root "$PWD" --skill /Users/moses/.agents/skills/bmad-build`

CORRECTION verified by Silas: PWD was `/Users/moses/.herdr/worktrees/packet-plumber-3d/planet-life-router-legibility`. Project rooting was CORRECT. The earlier displayed `/Users/moses/code` expansion came from Silas' relay shell, not the minion execution. The prior project-root leakage diagnosis is withdrawn; do not repair/relaunch/reconfigure a correctly rooted minion.

Exit 1: ambiguous config value implementation_artifacts at modules.bmm.implementation_artifacts and modules.gds.implementation_artifacts. The skill correctly requires a HALT on failure and forbids directly executing workflow source.

## Read-only evidence gathered by Gru
- Canonical bmad-build SKILL.md requires ONE invocation of `{project-root}/_bmad/scripts/render_skill.py --project-root {project-root} --skill {skill-root}`, no cwd change; on success follow the one absolute workflow.md printed to stdout; on failure HALT.
- `_bmad/scripts/render_skill.py` `_resolve_short_config` lines ~140–150 rejects more than one key match irrespective of resolved values; `_resolve_replacements` supports fully qualified `{{config.<path>}}` tokens too.
- Root `_bmad/config.toml` and PP3D's main installed config both contain modules.bmm.implementation_artifacts and modules.gds.implementation_artifacts with the same `{project-root}/_bmad-output/implementation-artifacts` string. Other short-name collisions may follow; inspect all used bindings rather than whack-a-mole blindly.
- PP3D worktree `_bmad` is a symlink to `/Users/moses/code/_bmad`. It supplies the canonical renderer; the ACTUAL minion invocation correctly kept --project-root at the PP3D worktree. Preserve this arrangement. Rooting is a regression guard, not a current defect.

## Acceptance
1. Diagnose and fix the ambiguous config binding with a supported durable mechanism. There is NO evidenced project-root leakage to fix. Read renderer/config/customization docs and tests before selecting the fix. Prefer an explicit documented binding/qualified-key solution if available; do not delete either installed module, silently select the first match, or fabricate a workflow file. If a narrowly scoped renderer repair is needed, regression-test its semantics, preserve conflicts as hard failures, and record provenance/ownership.
2. Renderer/script location may resolve via the sanctioned worktree symlink to canonical tools; `--project-root` and all project artifact paths must remain the ACTUAL PP3D worktree. Verify rendered workflow metadata and replacement paths, not merely exit code.
3. Mixed BMM+GDS configuration successfully renders bmad-build; genuine conflicting values still HALT with diagnostics; missing config remains failure; no stale rendered snapshot accepted; required plan/implementation/review/verification instructions remain intact. Test non-game/single-module compatibility as appropriate.
4. Respect the skill's once-only failure contract: no repeated retry loop in the blocked parent and no workflow-source fallback. After prerequisites are corrected, provide a fresh compliant skill invocation / newly rendered workflow through the documented success path, with exact command, printed absolute path and successful receipt. Parent resumes only on that verified path, same task/pane/model.
5. Locate ownership of installed/ignored tooling before changes. Tracked orchestrator-root edits use an isolated worktree and scoped PR (pr_review=0 ops-tooling, no merge); installed canonical package changes need durable supported overrides/patch provenance, not an unexplained edit to ignored files. Avoid recursive reliance on the broken renderer for its own bootstrap fix: use the repo's documented maintenance/customization route and manual regression verification, not bypasses in the GAME lane.
6. Tests/proof at actual head. Do not alter unrelated dirty root files/config or the two live creative/code lanes. If a working fix cannot be achieved without a new material policy decision, report the exact alternatives rather than guessing.
7. Relay compliant success to PP3D minion, verify it is working past the render gate, and report to Gru. Preserve failed command/error as evidence. Do not alter dispatch/rooting instructions based on the withdrawn diagnosis. Preserve literal shell expressions in future relay evidence so the relay shell cannot fabricate a different execution root.

## Skills policy
This is orchestration tooling/config maintenance, not the PP3D implementation. Read bmad-build entrypoint and relevant renderer/config documentation/tests for diagnosis. Use bmad-customize if using supported customization. PP3D resumes normal bmad-build with independent review and Perkins after prerequisites work; no raw-source fallback. Small targeted canon amendments: lavish not needed, PR directly where tracked.

## Model policy
Non-3D tooling agent/helper: openai-codex/gpt-5.6-sol xhigh (or Silas self-edit on its assigned Luna/max). PP3D minion and all 3D helpers stay Astra/xhigh. No legacy model fallback.

## Dispatch parameters
repo: orchestrator root / installed BMAD tooling (verify actual file ownership)
repo_root: /Users/moses/code
slug: bmad-build-config-unblock-pp3d
base: fresh origin/main for tracked root changes
pr_review: 0
worktree: required for tracked root edits; preserve PP3D existing worktree
blocked_job: packet-plumber-3d-planet-life-router-legibility
completion: verified compliant bmad-build render rooted to PP3D + resumed parent + durable fix receipt; no merge
