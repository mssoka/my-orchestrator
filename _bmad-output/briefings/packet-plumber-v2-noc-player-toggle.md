# packet-plumber-v2-noc-player-toggle

## Task

Make the NOC dashboard available to PLAYERS in the normal build. User
ruling (2026-08-23): "the noc might be useful for players as well — we
can remove it if it's [too much]" — the D-key panel ships in the
standard build behind a runtime toggle, default available, trivially
removable later (a default flip, not a code excision).

## Scope

1. **Compile gate → runtime toggle**: the v2-noc surface currently
   compiles only under PP_DEBUG (release builds carry zero pixels).
   Change: compile it into the NORMAL build; gate the D-key toggle at
   RUNTIME (a settings flag, default ON = available). run-dev.sh keeps
   working (it can simply become the same build).
2. **Zero release-pixels rule relaxed ONLY for user-pressed D**: the
   dashboard renders ONLY while toggled on by the player — default
   state OFF (invisible). No new pixels in any normal frame.
3. **Harness immunity preserved**: the capture path never presses D —
   goldens byte-identical (48/48 proof); a settings-persistence choice
   (remember toggle state across runs?) defaults to NO (fresh runs
   start clean) — document.
4. **Help/discoverability**: one line somewhere discoverable (settings
   panel or a hint chip) that D exists — players can't find what they
   can't see. Keep it minimal.
5. Removal path: the toggle default + the settings flag make future
   removal a one-line change — note in the PR body.

## Rules (hard)

1. View-layer only; zero sim writes; T1/T2/replay hash-equal.
2. Zero golden drift (captures never toggle D).
3. The dev flag (PP_DEBUG) may still exist for run-dev.sh — but the
   normal build now carries the surface too; reconcile the two paths
   (one code path, two entry points) — no forked rendering.
4. Follow the existing settings-panel conventions for the toggle.

## Acceptance

- Normal `odin run app`: D toggles the NOC panel (captures in PR body);
  default frame unchanged (no pixels without a keypress).
- run-dev.sh unchanged in behavior.
- T1/T2/replay hash-equal; 48/48 + full suites green.
- PR body documents the removal path (one-line default flip).
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-noc-player-toggle
- base: v2 (fresh head)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe: view/settings layer; Silas coordinates merge order
