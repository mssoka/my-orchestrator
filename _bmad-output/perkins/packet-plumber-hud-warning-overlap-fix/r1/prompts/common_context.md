# Shared context for all lenses (packet-plumber-hud-warning-overlap-fix, round 1)

## The PR (scope)

PR #42 on `solarity-services/Packet-Plumber`, targets `v2`, reviewed at sha `b3b8ded`. TINY diff (+9/−6, app/main.odin, ONE block): the drag-rejection warning no longer draws at the fixed `12, 76` (colliding with the 4.1 strain legend) — it anchors at the drag cursor, following the cost readout's established pattern (option C, user-verified 2026-08-14).

The bug (user-reported): when the player drags an invalid link, the rejection warning overlapped the grey strain-legend row starting with "node strain". Root cause: TWO texts drew at the same position x=12, y=76:
1. The 4.1 strain legend: `draw_text(app, lead_s, 12, 76, 14, p.ink_soft)` — "node strain ~30s to critical / …"
2. The drag rejection warning (older): `draw_text(app, reject_label(app.drag.valid), 12, 76, 16, rl.Color{200, 60, 60, 255})`

The fix: the rejection draw moves to the cursor anchor (`cur.x+12, cur.y-14`, red, 16px) — the SAME anchor the cost readout already uses a few lines below. `cur := rnd.to_screen(&app.view, app.drag.wx, app.drag.wy)` was hoisted once at the top of the drag block so both branches share one anchor definition.

## Acceptance criteria (from the job briefing)

1. Dragging an invalid link (e.g. terminal→terminal, span-exceeds-tier, self-loop) shows the red rejection AT the cursor — never at (12, 76).
2. The strain legend row renders clean at (12, 76) with no occlusion, in every run-mode state.
3. Collision sweep (prove in the PR body): enumerate ALL fixed-position `draw_text` y anchors in `app/main.odin` run mode and show none overlap — a regression test if practical, a documented sweep otherwise.
4. Game-over mode untouched; the QoS toast (12, 156) untouched.
5. `odin test` + `harness run` green; **goldens MUST NOT shift** (verify no T2 capture shows the rejection; any shift = STOP and flag).

## ⚠️ CRITICAL lens-guards (this is a surgical-fix review)

- **Verify the collision is actually gone:** the strain-legend draw (`"node strain ~30s to critical / …"` at `12, 76, 14, p.ink_soft`) and the drag-warning draw must no longer share a position. The warning renders at the cursor (the reject_label text at the drag point). A residual overlap or a warning that renders off-screen/at a nonsense position = a finding.
- **Verify the pattern matches the established cost readout** (the anchor style the briefing names) — consistent placement, readable, not clipped at screen edges.
- **Verify the diff is surgical:** ONE block in app/main.odin, no unrelated changes, no core/ touches, LOG_VERSION 3 (core/serialize.odin), no new commands. Anything beyond the drag-rejection draw = a finding.
- **BASE = `v2`** (Job A/B/C + 4.1/4.2 + pin merged — carry-forward only). NOTE: in-flight 4.3 (win/lose toast) will touch app/main.odin separately — not in this PR; do not flag missing win/lose UI.
- **Em-dashes OK in PP.** Golden discipline: this diff cannot shift goldens (render-path only — verify none shifted).
- **User-verified approach:** the option-C cursor-anchor was explicitly confirmed by the user — review whether it's IMPLEMENTED correctly, do not re-litigate the choice of approach.

## Legitimate findings here would be

- A residual collision: the rejection still drawing at (12, 76) or sharing a position with another fixed HUD element.
- The rejection rendering off-screen or at a nonsense position (e.g. wrong anchor math, wrong world→screen transform, text clipped at screen edges in a way the cost readout is not).
- A pattern mismatch with the cost readout (different anchor/offset/size than the established `cur.x+12, cur.y-14, 16`).
- Scope drift: changes beyond the drag-rejection draw (core/ touched, LOG_VERSION bumped, new commands, other UI changed, game-over or QoS-toast modified).
- A golden shift or a broken local suite at the sha.

## Context the lenses may rely on

- **Perkins local verification at the sha (ground truth — CI is account-billing-blocked):** `odin test core` → 136/136 tests pass; `tools/harness.sh run` → 18/18 demos PASS (T1 state hashes + T2 pixel goldens byte-exact, zero shift).
- The repo is a worktree detached at exactly `b3b8ded`: `/Users/moses/.herdr/worktrees/packet-plumber/perkins-hud-warning-overlap-fix-r1` — verify any claim against THIS checkout, not origin.
- The PR body (visible on GitHub PR #42) contains the collision sweep table and rationale — treat its claims as leads, verify independently.
