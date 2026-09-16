# Sheep shard — field-notes (dream-2026-09-07)

Read: 9 shards, dated 2026-09-04 (levels), 2026-09-05 (alive-planet, cumulative,
era-planets, l1-topology-font, scene-refactor, model-single-source, tf-in-ci),
2026-09-06 (wif-durable).

## Candidate patterns

### `gh pr create --body "$(heredoc)"` quoting trap → `--body-file` FIRST (2 sightings: packet-plumber-3d-gdd-amend-alive-planet 2026-09-05, packet-plumber-3d-gdd-amend-cumulative 2026-09-05)
- Quote/evidence: alive-planet — "The `gh pr create --body "$(cat <<'EOF'…)"` trap is real even for carefully quoted heredocs (×3 now) — went straight to `--body-file /tmp/…` on the second attempt; should have been the FIRST attempt." cumulative — "`gh pr create --body "$(cat <<'EOF' ...)"` with apostrophe-rich markdown dies on quoting — write the body to a temp file and use `--body-file` instead."
- Proposed lesson (one line, diff-ready voice): Never build a gh PR body via `--body "$(heredoc)"` — write the body to a temp file and pass `--body-file` on the FIRST attempt; apostrophes/backticks defeat even careful quoting.

### Column-aligned markdown (ASCII boxes, tables): script-assert widths before edit, re-render region after (2 sightings: packet-plumber-3d-gdd-amend-alive-planet 2026-09-05, packet-plumber-3d-gdd-amend-levels 2026-09-04)
- Quote/evidence: alive-planet — "after editing box lines, re-measure ALL box lines with a python east-asian-width script — my first pad math used inner=65 (real: 64) and every replaced line came out 70; a one-line assert script caught and fixed it." levels — "box-art/ASCII blocks in markdown need exact column-count replacements — build replacement lines in python and assert interior width (64) BEFORE issuing the edit; and after table edits, re-render the region to catch rows orphaned by an inserted clarifier paragraph (my M5 table split silently on first attempt)."
- Proposed lesson: Editing column-aligned markdown: generate replacement lines in python, assert display width (east-asian-aware) BEFORE the edit, and re-render the region after — pad-math slips and table rows orphaned by inserted paragraphs fail silently.

### Canon-amendment hygiene: grep OLD phrasings + date-stamp the supersede at EVERY site (2 sightings: packet-plumber-3d-gdd-amend-alive-planet 2026-09-05, packet-plumber-3d-gdd-amend-cumulative 2026-09-05)
- Quote/evidence: alive-planet — "grep the OLD phrasings before editing ... caught two non-obvious stragglers (tutorial seed line, L1 remediation 'direct pipe') that the section-level plan missed." cumulative — "supersede chains must be DATE-STAMPED at every amended canon site (M2/M3/OQ9/E10.7), not just in the decision log, or readers meet the old claim first and trust it (D5's retirement clause had propagated to 4 sites)."
- Proposed lesson: A canon amendment greps the OLD phrasings repo-wide before editing and date-stamps the supersede note at every site the old claim lives — section-level plans miss stragglers, and an undated site reads as current canon.

### Scope-guard courtesy: adjacent-surface finds get flagged for a ruling, never silently fixed (3 sightings: packet-plumber-3d-gdd-amend-cumulative 2026-09-05, packet-plumber-3d-gdd-amend-era-planets 2026-09-05, packet-plumber-3d-gdd-amend-levels 2026-09-04)
- Quote/evidence: cumulative — "stale canon found ADJACENT to the named sections ... gets flagged in the decision log + PR body, never silently fixed; keeps the diff reviewable and the ruling trail honest." era-planets — "touch ONLY the files the briefing names (3 GDD files), put the adjacent-surface find (README stale comment) behind an in-page decision form — the user ruled it in, and the README edit rode this PR with zero l1-arpanet conflict risk." levels — "a user annotation can RESCUE a briefing's scope guard without breaking it — 'look at the odin version' was satisfied from THIS repo's own verbatim inheritance records ... check what the repo's canon already records before reading across the guard."
- Proposed lesson: Under a scope guard, adjacent-surface finds are flagged for a ruling (decision log / PR body / lavish decision form), never silently fixed — and a user request satisfied from the repo's own records does not break the guard.

### Lavish ruling gates: per-row radios + one Queue button + pros/cons explainer (2 sightings: packet-plumber-3d-gdd-amend-levels 2026-09-04, packet-plumber-3d-gdd-amend-era-planets 2026-09-05)
- Quote/evidence: levels — "per-row radios + one Queue button got clean machine-parseable rulings (D1–D5 all arrived as tagged prompts); pair every form with a pros/cons explainer block when the options aren't self-evident (the user asked 'explain this, pros and cons' on the two forms that lacked one)." era-planets — "put the adjacent-surface find ... behind an in-page decision form — the user ruled it in."
- Proposed lesson: Lavish decision forms: per-row radios + a single Queue button produce machine-parseable verdicts; attach a pros/cons explainer to every form whose options aren't self-evident — the user asks for it when it's missing.

### Godot MCP LSP is not ground truth: main-checkout-rooted + stale class cache; verify on disk, pkill to respawn (2 sightings: packet-plumber-3d-l1-topology-font 2026-09-05, packet-plumber-3d-scene-refactor 2026-09-05)
- Quote/evidence: l1-topology-font — "the godot MCP LSP serves the MAIN checkout root — worktree files analyze as outsiders (phantom 'hides a global script class' + 'not declared' for NEW global classes). Prove health via on-disk `.godot/global_script_class_cache.cfg` + `--check-only --script` per file." scene-refactor — "the godot MCP's LSP is a long-lived `godot --headless --editor --lsp --path .` process that holds the PRE-MOVE class cache after refactors (140 phantom diagnostics citing old paths; res:// resource-existence checks also lag new files). `pkill -f "godot.*--lsp"` → MCP respawns fresh → 0 real diagnostics."
- Proposed lesson: Godot MCP LSP diagnostics are not ground truth — it serves the main checkout root and holds stale class caches after refactors; verify via the on-disk `.godot/global_script_class_cache.cfg` + per-file `--check-only --script`, and `pkill -f "godot.*--lsp"` to force a fresh spawn.

### herdr wait syntax: `herdr agent wait <pane> --until idle` — `herdr wait agent-status` is dead on this build (2 sightings: righttenantry-agents-model-single-source 2026-09-05, righttenantry-agents-wif-durable 2026-09-06)
- Quote/evidence: model-single-source — "`herdr agent wait <pane> --until idle` is the working syntax (skill doc's `herdr wait agent-status --status` is a newer/other CLI); `--until done` fires only in background panes, `idle` when seen." wif-durable — "`herdr wait agent-status` doesn't exist in this CLI build — use `herdr agent wait <pane> --until idle --timeout N` (and `pane run` for prompts)."
- Proposed lesson: `herdr wait agent-status` is dead syntax on this CLI build — the working form is `herdr agent wait <pane> --until idle --timeout N` (and `--until done` only fires for background panes); docs/templates naming the old form are stale. (Already in AGENTS.md from dream-2026-08-19; two fresh sightings + a new fact: `--until done` background-only.)

### bmad-build can't render where repo-local `_bmad` lacks render_skill.py — read skill step files / review-prompts directly (2 sightings: righttenantry-agents-model-single-source 2026-09-05, righttenantry-agents-tf-in-ci 2026-09-05)
- Quote/evidence: model-single-source — "bmad-quick-dev is GONE from the canonical home (successor bmad-build can't render — no `_bmad/scripts/render_skill.py`); standing waiver path worked: self-contained briefing + waiver note in PR body + run bmad-build's review-prompts (`review-prompts/*.md`) directly as herdr mega-minions — step-04 discipline without the renderer." tf-in-ci — "bmad-build's render_skill.py doesn't exist in RTA's older `_bmad` install — the skill's step files carry everything; read them directly from the skill dir (template placeholders like `{workflow.review_layers}` stay unresolved; improvise the named layer from the playbook's lens list)."
- Proposed lesson: bmad-build can't render where `_bmad/scripts/render_skill.py` is absent (repo-local older installs) — read the skill's step files / review-prompts directly (improvise unresolved placeholders from the playbook's lens list) and record the waiver in the PR body.

### Mutation-test craft on macOS: never BSD sed, never `git checkout --` restore (1 sighting — watch-item candidate: righttenantry-agents-model-single-source 2026-09-05)
- Quote/evidence: "BSD (macOS) sed has no `0,/re/` address — a 'mutation test' silently mutates NOTHING; worse, `git checkout -- <file>` afterwards nuked my real unstaged edits. Mutation tests: python replace + cp backup + diff-verify restore, never sed+checkout."
- Proposed lesson: Mutation tests on macOS: never sed (BSD sed lacks `0,/re/` and silently no-ops) and never `git checkout --` to restore (it nukes unstaged edits) — python replace + cp backup + diff-verified restore.

### Godot editor-viewport captures: control the environment, gate on structural pixel diff not md5 (2 sightings: packet-plumber-3d-l1-topology-font 2026-09-05, packet-plumber-3d-scene-refactor 2026-09-05)
- Quote/evidence: l1-topology-font — "macOS occlusion throttling freezes windowed captures (the freshness gate caught identical frames); fullscreen puts the window on an active Space and `CONTENT_SCALE_MODE_CANVAS_ITEMS`+`EXPAND` keeps UI at true game proportions on the big canvas." scene-refactor — "editor-viewport PNG md5 is NOT a valid determinism gate: same-code re-renders gave 3 different md5s pre-refactor; the audit pinned the mechanism (editor viewport height drifts ±1 px with window/dock layout). Gate instead on structural pixel diff (12× downscale + blur, grayscale): noise floor max≈1; real composition change reads max 110+."
- Proposed lesson: Godot editor-viewport captures: fullscreen on an active Space (occlusion throttling freezes windowed frames) and never gate on PNG md5 (viewport drifts ±1px with dock layout) — gate on a structural pixel diff (downscale+blur+grayscale) with a calibrated noise floor.

### Godot @tool placeholder-instance trap: editor-hint paths construct via `.new()` (1 sighting — watch-item candidate: packet-plumber-3d-scene-refactor 2026-09-05)
- Quote/evidence: "`PackedScene.instantiate()` of a scene whose root script is NOT @tool yields a placeholder under the editor — script methods (setup()) are uncallable and staging silently aborts at child 1. Editor-hint paths must construct via .new(); runtime can instantiate. Caught ONLY by pixel forensics (suite is runtime-only)."
- Proposed lesson: Godot: under the editor, `PackedScene.instantiate()` of a non-@tool root script yields a placeholder (methods uncallable, staging silently aborts) — editor-hint paths construct via `.new()`; only pixel forensics catches it (runtime suites are blind).

### Godot 4.7 silent input failures: FontVariation fourcc keys + project.godot `;` comments (1 sighting — watch-item candidate: packet-plumber-3d-l1-topology-font 2026-09-05)
- Quote/evidence: "Godot 4.7 `FontVariation.variation_opentype` SILENTLY IGNORES string axis keys (`{"wght": 700}` renders regular) — only integer fourcc tags work (`{("w"<<"24")|...: 700}`); a bold-vs-regular advance-width pin is the cheap guard. Also: `#` comment lines poison project.godot sections (keys read back empty) — use `;`."
- Proposed lesson: Godot 4.7 fails silently on malformed input — FontVariation.variation_opentype needs integer fourcc keys (string keys render regular; pin with an advance-width guard) and project.godot comments must be `;` (`#` poisons the section, keys read back empty).

### GCP IAM roles: never trust memory — gcloud-verify existence AND full permission list; "viewer" ≠ read-only (1 sighting, 4 internal notes — watch-item candidate: righttenantry-agents-tf-in-ci 2026-09-05)
- Quote/evidence: "predefined-role memory CANNOT be trusted — bigquery.viewer and resourcemanager.projectIamViewer don't exist (real: bigquery.metadataViewer; no predefined project-IAM read role). gcloud-verify every roles/* string ... before it reaches tfvars"; "'viewer' != read-only — roles/aiplatform.viewer carries aiplatform.specialistPools.update (WRITE). ANY predefined role on a PR-reachable SA needs its full permission list gcloud-verified"; "legacy `roles/storage.viewer` = buckets.list ONLY (no buckets.get/objects.get ... don't trust memory)."
- Proposed lesson: GCP IAM: never write a roles/* string from memory — names don't exist (bigquery.viewer) and "viewer" roles carry writes (aiplatform.viewer); gcloud-verify every role's existence AND full permission list before tfvars, and pin zero-write claims with per-permission custom roles.

### Terraform invariant tests: strip WHOLE-LINE comments (anchored MULTILINE) before substring asserts (1 sighting — watch-item candidate: righttenantry-agents-wif-durable 2026-09-06)
- Quote/evidence: "invariant tests asserting on `_resource_block` output must strip WHOLE-LINE comments (`^\s*#` + MULTILINE) — comment prose inside a tf resource block can satisfy substring asserts (masked a real condition regression in my first draft); unanchored `#[^\n]*` corrupts HCL strings containing '#'."
- Proposed lesson: Terraform invariant tests: strip whole-line comments with an anchored MULTILINE regex before substring-asserting on a resource block — comment prose can satisfy the assert (masking regressions), and an unanchored strip corrupts HCL strings containing '#'.

### Pre-commit hooks fire after message-drafting — run the hook's linter on touched files BEFORE committing (1 sighting — watch-item candidate: righttenantry-agents-wif-durable 2026-09-06)
- Quote/evidence: "PR-branch lint (ruff F541) runs in pre-commit AFTER your message-drafting — run `uv run ruff check` on touched test files before committing; f-strings without placeholders (even with `{{}}` escapes) fail the hook and force an amend dance."
- Proposed lesson: Pre-commit hooks fire after the commit message is drafted — run the hook's linter (e.g. `uv run ruff check`) on touched files BEFORE committing to avoid the amend dance.

### Edit anchors: python `repr()` of the exact line beats re-reading the rendered view (1 sighting — watch-item candidate: packet-plumber-3d-gdd-amend-era-planets 2026-09-05)
- Quote/evidence: "two edit-batch rejections came from mis-transcribing the `]`` ` `—` inline-code close in the read output; python `repr()` of the exact line beat re-reading the rendered view every time."
- Proposed lesson: When an edit anchor keeps rejecting, take python `repr()` of the exact line — rendered views mis-transcribe inline-code/quote/dash sequences.

## One-off / job-scoped lessons (watch-item candidates)

- packet-plumber-3d-gdd-amend-era-planets (2026-09-05): PP3D lavish pages — the repo's little-planet palette tokens (GDD Art §) + SVG viewBox + short labels make a coherent zero-CDN dark review page that survived the DOM audit with zero layout warnings on first serve (PP3D-scoped lavish craft).
- righttenantry-agents-tf-in-ci (2026-09-05): RTA WIF trap — `roles/iam.serviceAccountTokenCreator` on a repo-wide principalSet lets ANY PR-ref token mint write-SA tokens WITHOUT workloadIdentityUser; ref-scope EVERY WIF-granted role on the write SA, not just the workloadIdentityUser binding.
- righttenantry-agents-tf-in-ci (2026-09-05): GCS backend has NO state locking below Terraform 1.10 (CI pins ~1.7) — GitHub concurrency groups per env are the real plan/apply mutex; never grant a planner objectCreator "for the lock" (at 1.10 a creator-without-delete strands the lock).

## Per-shard summary

- packet-plumber-3d-gdd-amend-alive-planet.md: ASCII-box width assertions + gh `--body-file` + grep-old-phrasings canon amendment.
- packet-plumber-3d-gdd-amend-cumulative.md: date-stamp supersede chains at every canon site; adjacent stale canon flagged, never silently fixed.
- packet-plumber-3d-gdd-amend-era-planets.md: python `repr()` for exact edit anchors; adjacent finds go behind an in-page decision form; PP3D lavish page craft.
- packet-plumber-3d-gdd-amend-levels.md: lavish decision forms + pros/cons explainers; width-assert + re-render on column-aligned markdown edits; repo-records can satisfy a user ask without breaking the scope guard.
- packet-plumber-3d-l1-topology-font.md: Godot 4.7 silent input failures (fourcc keys, `;` comments); macOS capture environment control; MCP LSP main-root phantom diagnostics.
- packet-plumber-3d-scene-refactor.md: @tool placeholder-instance trap; structural pixel diff beats md5; LSP stale-cache pkill-respawn with disk cache as ground truth.
- righttenantry-agents-model-single-source.md: BSD sed mutation trap (+ git-checkout restore hazard); render_skill.py-absent waiver path; herdr agent wait syntax.
- righttenantry-agents-tf-in-ci.md: GCP IAM role verification (memory untrustworthy; "viewer" ≠ read-only); WIF principalSet scoping trap; GCS pre-1.10 locking gap; render_skill.py-absent step-file reading.
- righttenantry-agents-wif-durable.md: herdr agent wait syntax (again); HCL whole-line comment stripping in invariant tests; run hook linters before committing.
