# orchestrator-vision-tooling

## Task

Re-point the vision tooling to the KYLE doctrine (user ruling
2026-08-21, now canon in AGENTS.md @ d5e1fe5): vision mega-minion on
`zai-coding-cn/glm-4.6v` (standing; one-line flip to glm-5v-turbo when
ZAI trial access lands — 1311 subscription-gated as of 08-21). The
08-18 local-lmstudio doctrine (qwen3.8-27b@4bit) is RETIRED. Doctrine
is ALREADY written — this job ships the tools that implement it. Do
not re-litigate the doctrine.

## Scope

1. **bin/vision-read** (repo): re-point the default model to
   `zai-coding-cn/glm-4.6v`. Mechanism stays (headless pi + @file
   attachment) — this becomes KYLE's quick-read mode. Keep --model
   override + VISION_MODEL env swap; re-point help text to the KYLE
   doctrine (two modes: quick-read = this tool; visual-verification =
   full mega-minion spawned in the summoning cwd with read/grep/bash —
   see the AGENTS.md block). Local lmstudio path: keep ONLY as an
   explicit `--fast`-style last-resort flag, clearly labeled fallback,
   never default. One-line flip target documented (glm-5v-turbo).
2. **vision-read skill** (SKILL.md — find it under
   ~/.pi/agent/skills/vision-read/; NOTE it may live outside the repo:
   canonical skills home is /Users/moses/code/.agents/skills, symlinked
   into ~/.pi/agent/skills — check both, edit the REAL file, keep the
   symlink intact): rewrite for the two KYLE modes + codebase-access
   recipe (spawn cwd = summoning repo/worktree; prompt carries
   summon-reason + pointers; image attached via @file). Include the
   probe-first rule (env-cleared pi probe; if 4.6v DOWN, stop and
   escalate — never proceed on a blind model).
3. **models.json**: ensure the glm-4.6v registration declares
   `input: ["text","image"]` (pi gates image attachment on declared
   input types — a missing declaration bounces with "Current model
   does not support images"). Only add/fix the entry if missing.
4. **End-to-end proof (the acceptance core):** run a REAL image through
   bin/vision-read on glm-4.6v and verify THROUGH pi per provenance
   doctrine: the session jsonl's modelId must be glm-4.6v (never trust
   the reply's self-named id). Use a real screenshot from the repo's
   test fixtures/goldens if any exist; else generate any PNG and prove
   the pipeline. Capture the proof (command + modelId line) in the PR
   body.

## Rules (hard)

1. No behavioral change beyond the model re-point + docs; the tool's
   output contract (reply text on stdout) unchanged.
2. Out-of-repo file (skill SKILL.md if it lives only in ~/.pi): edit
   via absolute path from the worktree; note the exact path in the PR
   body. If a repo copy exists under .agents/skills, that one is
   canonical.
3. NO doctrine edits to AGENTS.md or the playbook (canon landed at
   d5e1fe5; pointers only).
4. Parallel-safe: touches bin/vision-read + skill file only — no
   overlap with night-watchman-hardening (bin/night-watchman, plist),
   role-skills (extensions, playbook), or the PP jobs.

## Acceptance

- bin/vision-read defaults to glm-4.6v; --model/VISION_MODEL still
  override; help text matches KYLE canon.
- Skill rewritten: two modes, codebase-access recipe, probe-first rule.
- E2E proof in PR body: real image → reply + session-jsonl modelId
  glm-4.6v.
- grep check: no remaining default references to qwen3.8/lmstudio in
  bin/vision-read's default path (fallback flag excepted) or the
  skill's instructions.

## Skills policy

bmad-quick-dev. (bmad-build render may still be broken upstream —
6.11.0 config token bug, waived on night-watchman #6; self-contained
briefing, proceed without it if it fails, note the waiver.)

## Model policy

deepseek-v4-flash, --thinking max. Kyle test calls: glm-4.6v.

## Dispatch parameters

- repo: orchestrator root
- repo_root: /Users/moses/code
- slug: orchestrator-vision-tooling
- base: main @ d5e1fe5
- model: deepseek-v4-flash
- worktree: MANDATORY (orchestrator-root exception)
- pr_review: 0 (ops-tooling; the E2E modelId proof is the merge
  ground truth per the 2026-08-16 ruling)
