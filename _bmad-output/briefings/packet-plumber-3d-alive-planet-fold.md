# Briefing — packet-plumber-3d-alive-planet-fold

## Context

alive-planet PR #14 was APPROVED by Perkins r6 (0 blockers, 18:43Z, 6-round
loop closed). 12 non-blocking warnings rode the verdict. This follow-up folds
the two headline items. MORE ITEMS MAY ARRIVE MID-FLIGHT as user-relayed
amendments (the user is heading into testing) — this PR is the folding
surface; fold relayed amendments into the SAME PR, never spin new jobs.

## Scope (exactly this, nothing more)

1. **🧊 Igloo regression — GAMEPLAY, priority.** The r6 snow-filter delta
   silently erased L1's igloos (2 → 0). Find the r6 change (snow-filter /
   biome placement predicate) that dropped them and restore the two igloos on
   L1 (ARPANET level).
   - Acceptance: seeded-deterministic L1 world gen shows igloo count == 2.
   - Guard: a test pinning the count (EXPECTED_CHECKS discipline if riding a
     harness; per-file expected run-count pins + final-line guard).
   - MUTATION LEG (Perkins will re-run it): reverting/deleting the fix makes
     the new guard RED. A guard that cannot be made to fail is a blocker.
2. **🖼️ Orphan texture purge — hygiene.** 11 orphan textures are still
   committed despite a false 6th-round "purged" claim (r6 review found them).
   Delete them + their `.import` side-files per the repo's side-file policy.
   - Acceptance: zero references remain (grep code + .tscn/.tres), project
     imports clean (godot --headless import or editor MCP verify), the count
     of removed files is stated in the PR body.

## Scope guard

- The OTHER 10 r6 warnings are NOT in scope unless explicitly relayed by
  Gru/Silas as amendments. Do not eat them.
- Do not modify PR #14 itself. This is a separate stacked PR.

## Amendment protocol

- Amendments arrive as relayed user rulings (via Gru → this pane). Fold each
  into this PR in arrival order; reply with the fold receipt (what changed,
  which commit). Never kill-and-redispatch.

## Mechanics

- Base: `main`. If PR #14 is still unmerged, branch from #14's head branch
  (stacked PR — it unlocks when the parent merges).
- Build/verify surface: godot 4.7.1 (`/opt/homebrew/bin/godot`) + the godot
  MCP (editor-driving) per repo doctrine; captures for visual proof.
- Vision: the minion tier is multimodal — captures may be verified inline.

## Acceptance summary

- L1 igloos == 2, guard test present, mutation leg proven (fix-reverted ⇒ RED).
- 11 orphan textures (+ side-files per policy) gone, imports clean.
- PR open to `main`, body carries: igloo before/after captures, purge file
  list, and a running FOLD LOG section for amendments.
- pr_review=1 (gameplay/canon surface — world-gen content + asset manifest).

## Skills policy

- Workflow skill: bmad-quick-dev.

## Model policy

- Unset (Silas pins at dispatch; ops default).

## Dispatch parameters

- repo: Packet-Plumber-3D
- repo_root: /Users/moses/code/Packet-Plumber-3D
- slug: packet-plumber-3d-alive-planet-fold
- base: main (stack on #14 head if unmerged)
- pr_review: 1
