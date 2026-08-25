# orchestrator-playbook-diet

## Task

Slim the playbook from ~1,280 lines to a lean operating core (~600),
relocating — never deleting — accumulated incident narrative and
superseded history. The user: "the playbook is getting really big."
Generalizes what U2 (PR #8) did for Model policy across the whole file.

## Rules (hard)

1. ZERO doctrine changes. This is relocation + tightening only. Every
   rule, ruling, threshold, and procedure must remain findable —
   acceptance test: for a list of doctrine keywords Gru supplies at
   review, each still greps to a hit (core or annex).
2. Core keeps: Roles, Gru/Silas sections, Model policy (incl. the LEFOU
   vision block), Intake, Dispatch, Minion standing orders, Tracking,
   Perkins essentials, Close-out, Concurrency, Skills availability.
   Target reading flow for a mid-operation session.
3. Relocate to `docs/playbook-annex.md`: incident narratives,
   case-by-case supersede histories, multi-paragraph war stories, and
   any block whose value is historical rather than operational. Core
   gets a one-line pointer + a one-line statement of the CURRENT rule.
4. The changelog appendix pattern U2 established stays the model —
   dated one-liners for how doctrine evolved.
5. DO NOT touch AGENTS.md (Gru-owned; handled separately).
6. Sequence: dispatch AFTER PR #8 merges (base on post-merge main).
   Worktree mandatory (orchestrator-root exception).

## Acceptance

- Line count: core ≤ ~650 (report before/after).
- Every keyword in Gru's review list greps to a live hit.
- No semantic diff in doctrine: a reviewer reading core + pointers can
  execute every procedure the old file supported.
- Lavish artifact (the slimmed playbook + what moved where) reviewed by
  the user BEFORE the PR opens.
- PR docs-only.

## Skills policy

bmad-quick-dev; lavish for the review artifact.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: orchestrator root
- repo_root: /Users/moses/code
- slug: orchestrator-playbook-diet
- base: main (post-#8-merge)
- model: deepseek-v4-flash
- release trigger: PR #8 MERGE (dispatch when merged; rebase onto the
  fresh head first)
- pr_review: 0 (docs; lavish loop is the review)
