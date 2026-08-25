You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read the file /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-noc-player-toggle-r3/project-context.md — it holds the project's critical rules and conventions for AI agents. Use it when judging convention/pattern findings.

--- DIFF ---
The canonical diff under review is saved at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-noc-player-toggle/r3/diff.patch
Read it FIRST and review exactly those bytes. NEVER re-fetch or regenerate the diff (no `git diff`, no `gh pr diff`). Your cwd is a repository checkout at exactly the reviewed state (detached at the reviewed sha 29addf4) — use it for every verification read.

--- SPEC / CONTEXT ---
The spec is the original job briefing (there is no separate GitHub issue for this job):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-noc-player-toggle.md
Read it. It defines the task, scope, hard rules, and acceptance criteria this diff must satisfy.

--- RE-REVIEW CONTEXT (round 3 — rebase-delta fix-audit) ---
This is round 3 of this PR. Round 2 (sha 726cf7f) returned APPROVED — all round-1 findings (B1 stuck-on panel blocker, W1 boot-defaults pin, W2 row-count pin) were verified fixed, plus 6 notes. Since then the v2 BASE moved: PR #89 (camera zoom/pan) and PR #90 (dublin map) merged under #91 while it sat approved. The current head (29addf4) is a conflict-only REBASE onto the fresh v2, keeping both intents. The merge points that touch this PR's surface:
- Settings rows merged: the camera branch's AUTO PULLBACK took row 4; this PR's NOC PANEL (D) moved to row 5 — SETTINGS_ROW_COUNT is now 6 (the W2 nav pin test_settings_nav_reaches_noc_row navigates via the symbolic rnd.SETTINGS_ROW_NOC constant).
- The camera branch's effect_overlay PP_DEBUG toggle gate + effect_zoom Noc_Scroll PP_DEBUG gate are both obsolete under this PR's runtime gate: the toggle stays runtime-gated, the scroll body is ungated, and the camera's B2 wheel-policy test (app/pullback_test.odin) was UPDATED to the merged semantics (scroll-not-zooms over the panel in EVERY build + a scroll-step assertion).
- Wheel ownership merged: rnd.camera_wheel_policy (app/render/noc_overlay.odin) owns the wheel; the overlay draw no longer reads the wheel directly.
- CI gate 9 merged to the camera's richer leg (app+harness PP_DEBUG builds + the PP_DEBUG test leg) in BOTH .github/workflows/ci.yml and tools/ci-local.sh.
- Both e2e drives are env-gated (PP_NOC_E2E + PP_CAM_E2E) and live in any build.
Your audit targets, from your lens where relevant:
(a) The three r1-fold pins must still bite on THIS head: (B1) effect_settings_adjust's SETTINGS_ROW_NOC case clears overlay_on when noc_enabled flips off (pin: noc_disable_while_visible_dismisses_the_panel); (W1) noc_boot_defaults is the ONE proc main() and the suite both drive; (W2) the input leg reaches SETTINGS_ROW_NOC through the real nav chain and a SETTINGS_ROW_COUNT revert fails it.
(b) DELTA-INTRODUCED defects from the rebase merge are the norm — hunt them: the row-merge, the ungated scroll body, the wheel-policy test rewrite, the merged CI gate, the merged e2e arms.
(c) NOT re-litigatable (user-ruled, do not re-flag): the player-NOC ruling itself; the runtime-toggle design (default ON = available, zero pixels until D; removal = one-line default flip); the zero-golden-drift bar (captures never press D); view-layer-only with zero sim writes.
Treat every claim as unverified until you read the code.

--- YOUR LENS ---
