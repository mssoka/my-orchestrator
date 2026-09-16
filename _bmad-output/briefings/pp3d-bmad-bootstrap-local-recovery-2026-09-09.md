# PP3D — local BMAD token qualification; then resume the user-approved guard fix

## Delegated routine setup correction

Gru approves the bounded LOCAL workflow-input correction below under the user's explicit “go with your recommendatipn” for the guard fix + two editor comparisons. No new user A/E. This is a NEW corrected bootstrap attempt after preserving the reported HALT, not permission to execute workflow sources directly or ignore the renderer error. Same pMY/session/worktree/job/Astra-xhigh, no new parent/fleet.

Main controlling scope remains `/Users/moses/code/_bmad-output/briefings/pp3d-guard-fix-user-resume-2026-09-09.md`. All original acceptance failures, guard requirements, native0/2 budget,60s/180s/90s/512MiB limits, no native retry/third run/instrumentation/waiver/remote, and Selva independence remain intact.

## Root cause verified by Gru

Read COMPLETE MILESTONE1-BLOCKED.md (SHA90c91fdeddf93abc95d323541d14065c063b2c1405921cd58007ed5b007c0644), installed skillSKILL.md/customize.toml, renderer/config loader and shared config. Read-only actual merged-config/token census establishes:

- Worktree `_bmad` is a SYMLINK to `/Users/moses/code/_bmad`; installed `~/.agents/skills/bmad-build` is also a shared symlink. **Neither is a local-edit target.** Do not edit the shared installer-managed config, canonical skill, renderer, override files or link topology.
- Installed workflow short tokens `{{.implementation_artifacts}}` AND `{{.planning_artifacts}}` each match BOTH modules.bmm and modules.gds. Each pair currently has IDENTICAL intended values (`{project-root}/_bmad-output/implementation-artifacts` and `/planning-artifacts`). This is namespace ambiguity, not a disputed output path.
- `communication_language`/`document_output_language` each resolve uniquely to core/English.
- Unchanged renderer explicitly supports FULL tokens `{{config.modules.bmm.implementation_artifacts}}` and `{{config.modules.bmm.planning_artifacts}}`; it intentionally rejects ambiguous shorthand. `_resolve_replacements()` handles these through explicit `_lookup()`. Config/customization merge cannot remove duplicate scalar keys via a legitimate sparse override; workflow customize.toml exposes no token-namespace option. Do not invent one or delete/hide GDS configuration.

## Exact allowed correction

1. Preserve old failed `editor-ab-guard-fix-20260909T092143459529Z` context/report/result (resultSHAd5e222a1ee55bcab59dbe0fc4c998efaeae28781d4469dc4afa222213890d05f), original failed command/output and all prior evidence.
2. Create a NEW job-owned, uninstalled workflow source snapshot under the SAME worktree's scratch recovery directory, with final directory basename EXACTLY `bmad-build` (e.g. `.../bootstrap-recovery-<utc>/workflow-sources/bmad-build`). Copy the actual current installed skill inputs byte-for-byte first, recording source hashes/provenance. Do not write through canonical skill/_bmad symlinks. Keep SKILL.md, customize.toml, workflow steps/order/review instructions and all other files unchanged except the two token substitutions below. Preserving basename keeps the existing bmad-build TOML customization lookup intact.
3. In copied Markdown source files ONLY, replace every exact `{{.implementation_artifacts}}` with `{{config.modules.bmm.implementation_artifacts}}`, and every exact `{{.planning_artifacts}}` with `{{config.modules.bmm.planning_artifacts}}`. bmm is the explicit namespace for this bmad-build snapshot; both module values match, so output destinations/meaning do not change. Do not alter language tokens, workflow behavior, checkpoints, review requirements or user/skill instruction text. Record precise diff/counts and original/new hashes. If actual values no longer match, report the new facts rather than arbitrarily choosing.
4. HOST-ONLY verify corrected snapshot has no remaining ambiguous config tokens; full namespaces resolve to the same intended absolute paths under the REAL PP3D worktree, not scratch/root. All source changes must be the two exact token substitutions; SKILL.md/customize.toml unchanged. Preserve strict ambiguity rejection in the renderer; missing/wrong namespace still fails. No render_skill.py/config_utils.py monkey-patch/global override/old rendered workflow reuse.
5. Invoke the copied unchanged SKILL.md's mandated bootstrap exactly ONCE for this corrected attempt, **same cwd and real project-root**, using the unchanged official worktree `_bmad/scripts/render_skill.py` and `--skill` pointing to the NEW local snapshot directory. The supported renderer may publish its normal NEW uniquely hashed immutable generation; no shared existing generation is overwritten. On success, read COMPLETE the absolute generated workflow path actually printed and follow it. The input snapshot is NOT an execution shortcut. On failure, preserve exact error and HALT/report as skill requires; no invisible fallback/retry loop.
6. Then continue SAME USER-approved guard task. This is not new discovery or a task-choice question: intent/scope/owner are pinned by the guard-fix user-resume brief. Routine in-scope planning goes through Gru as already delegated, not another user go. Guard repair/regression/mutation proof/retained review STILL owed; a successfully rendered workflow is not Milestone1 PASS or native readiness. Pending-control API research remains incomplete until actually proven—no assumed-empty queue/keyword workaround.

## Boundaries / handoff

This is a local token-resolution compatibility correction ONLY. Do not globally patch BMAD, reinstall anything, edit shared configuration/skill/cache history, drop modules, change worktree symlink, alter Godot/game code, or create a new tooling project/PR. Flag the broader shared-install ambiguity separately to Silas, OUT OF SCOPE for this job; it must not become a prerequisite for the local fix. No Selva or other agent changes.

Silas: relay this explicit correction to existing pMY and verify actual processing. Keep ledger/evidence for the bootstrap; user-facing milestone remains actual guard proof + editor result, not each namespace receipt. Reopen same row as appropriate, no duplicate job; old failed contexts remain closed. New authority should be included deliberately when the eventual new diagnostic binding freezes; do not amend bound briefs for progress.

## Skills / model / dispatch

- `bmad-build`: unchanged mandated renderer + locally qualified input snapshot as above; generated workflow only.
- `context7-docs`/supported installed docs for real API work. `bmad-customize` exposes no supported namespace field; do not pretend a workflow TOML override solves it.
- Parent/retained3Dhelpers Astra/xhigh; Silas Luna/max; no model change/new fleet.

repo: packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
job_id: packet-plumber-3d-planet-life-router-legibility
worktree: /Users/moses/.herdr/worktrees/packet-plumber-3d/planet-life-router-legibility
mode: same-owner local bootstrap input correction -> existing approved guard task
base: main (retained branch/dirty work)
model: openai-codex/gpt-6-astra
thinking: xhigh
pr_review: 1 (retained; no PR/Perkins now)
new_job: false
native_attempts_authorized_by_bootstrap_step: 0
native_scope_after_success: original user-go two editor comparisons only after complete guard proof/readiness
