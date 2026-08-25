# orchestrator-role-skills

## Task

Kill paste-block drift: the per-role standing-orders blocks are
hand-maintained in TWO places — the playbook core
(docs/orchestration-playbook.md) AND the extension template literals
(.pi/extensions/gru.ts `STANDING_ORDERS` line ~37, .pi/extensions/silas.ts
line ~35, plus the startup-checklist strings). They WILL drift. Make the
playbook core the single source of truth by GENERATING the consumed blocks
from it. This is the P2 follow-up the playbook-diet job recommended
(user-ruled 2026-08-22: "fix 1 as well"); diet shipped as f7987bb
(core 712 + annex 597).

## Rules (hard)

1. ZERO doctrine change. Generated text is derived from the current
   playbook core sections — where the extension block is a CONDENSED
   version of a section, the generator carries that condensation
   mapping (deterministic, commented). No hand edits to generated
   artifacts, ever.
2. Mechanism is the minion's call within these constraints: a generator
   (e.g. bin/gen-role-blocks) reads marked source ranges in the playbook
   and emits an artifact the extensions import (generated .ts module
   preferred over paste-include). Mark the source ranges structurally
   (HTML comment markers like paste-block:gru in the playbook) rather
   than regex-fragile line numbers — but do NOT restructure doctrine
   content to do it.
3. Extension load safety: any text embedded in template literals must
   have backticks escaped — the 2026-08-01 ParseError class killed a
   whole extension at load. REQUIRED: a load test (at minimum node
   syntax-check of both extensions with generated content inlined;
   better: sacrificial pi boot per extension).
4. Drift check: regenerate + git diff --exit-code as a one-command
   check (script or make target); name it in the PR body. Gru runs it
   at review.
5. Survey ALL paste-block consumers before scoping: gru.ts, silas.ts,
   the Perkins standing-orders paste-block (playbook ~line 536
   references one), and any minion handover template blocks. Cover what
   is mechanical; explicitly flag (not fix) anything that needs
   judgment.
6. DO NOT touch AGENTS.md (Gru-owned; the vision/KYLE amendment is a
   separate pending loop). Do not touch nefario-watch.ts behavior.

## Acceptance

- Generator + generated artifacts + drift-check land in ONE PR, docs
  and tooling only.
- PR body shows before/after diff of the emitted STANDING_ORDERS text
  vs the current hand-maintained text; any wording delta is pure
  derivation — zero new doctrine.
- Load test shown green (backtick-escape proven — include the worst-case
  fixture).
- Drift check green: regenerate → no diff.
- Lavish artifact (mechanism diagram + before/after blocks + the
  consumer survey) reviewed by the user BEFORE the PR opens.
- No runtime behavior change in Gru/Silas sessions beyond identical-text
  delivery.

## Skills policy

bmad-quick-dev; lavish for the review artifact. NOTE: bmad-build render
is broken upstream (6.11.0 config token bug — waived on the
night-watchman #6 job, 2026-08-21); this briefing is self-contained,
proceed without it if it fails the same way, and note the waiver in
the PR body.

## Model policy

deepseek-v4-flash, --thinking max. Mega-minions (if any): same.

## Dispatch parameters

- repo: orchestrator root
- repo_root: /Users/moses/code
- slug: orchestrator-role-skills
- base: main (post-f7987bb)
- model: deepseek-v4-flash
- worktree: MANDATORY (orchestrator-root exception — always a worktree)
- pr_review: 0 (ops-tooling/codegen; the drift check + load test are
  the merge ground truth per the 2026-08-16 ruling)
- parallel-safe with orchestrator-night-watchman-hardening (no file
  overlap: extensions+playbook vs bin/night-watchman+plist)
