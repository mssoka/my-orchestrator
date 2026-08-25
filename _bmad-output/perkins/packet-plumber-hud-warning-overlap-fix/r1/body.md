## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-hud-warning-overlap-fix · **Reviewed sha:** `b3b8ded` · **Reviewers:** 7/7 completed
**Verification:** 9/9 lens claims re-verified against the worktree at `b3b8ded` — 2 merged duplicates, 0 discarded as false-positive

**Empirical gate (all green at the reviewed sha):** diff is surgical — one block in `app/main.odin` (+9/−6), zero `core/` files, LOG_VERSION stays 3, no new commands · `odin test core` 136/136 · `tools/harness.sh run` 18/18 demos (T1 state hashes + T2 pixels byte-exact — zero golden shift; no T2 capture shows the rejection, `capture_frame` never calls `draw_hud`) · the collision is actually gone: `12, 76` now appears only at the strain legend (`app/main.odin:765`); the rejection draw anchors at `cur.x+12, cur.y-14` — byte-identical anchor/offset/size to the established cost readout (`app/main.odin:842`) · game-over block and the `12, 156` QoS toast untouched · PR body's collision-sweep table verified accurate against every fixed `draw_text` anchor in `draw_hud` · the option-C cursor anchor is implemented exactly as the user verified — this review does not re-litigate the approach.

### Blockers (0)

None.

### Warnings (3)

1. **[edge] `drag_to==0` sentinel collides with live node id 0 — rejection (and commit) suppressed for drags onto the residential node (pre-existing, carry-forward)** — `next_node_id` starts at 0 and `seed_fixture` spawns residential FIRST, so the residential node IS id 0; snapping to it sets `app.drag_to = 0` (the "none" sentinel), and the gate at `app/main.odin:836` skips the whole block. An invalid host→residential terminal→terminal drag — AC1's own example — draws NO rejection, and a VALID draw ending at residential can never commit (the commit gate at line 406 shares the sentinel). Pre-existing in v2; the diff's hunk keeps the gate unchanged. Recommend a follow-up (ids from 1, or a snap-ok bool) outside this surgical fix.
2. **[blind, edge] Cursor-anchored rejection clips at window edges — no clamp** — `draw_text` clamps nothing: near the top edge the anchor (`cur.y-14`) goes negative; near the right edge the 33–46-char reject labels (~260–370px at 16px) run past `WIN_W=1280` where the 7-char "cost N" fits. Inherent to the user-verified cursor-anchor pattern (the cost readout shares it), but the rejection's length makes it clip earlier. Cosmetic and transient. Recommend a follow-up refinement (clamp y ≥ 0; flip left of the cursor near the right edge) that keeps the verified anchor.
3. **[tests] Advisory test gate: CONCERNS** — P0 100%, P1 100%; the diff's single behavior (rejection label at cursor) is P2 with 0% automated coverage: core tests are pure-sim, `capture_frame` never renders the HUD (`drag` state = `{}`), no demo drives an invalid drag. AC3's documented-sweep branch was taken and the PR body's sweep table checks out; a HUD-aware capture + invalid-drag demo golden would need new harness plumbing beyond the surgical scope.

### Notes (4)

1. **[blind, architecture] Comment overclaims "never collides"** — anchor is `cur+(12,-14)`, so a mouse at screen (0,90) draws the rejection exactly at (12,76), the legend's anchor. The FIXED-position collision is gone; the transient cursor-overlap is inherent to the verified approach and identical for the cost label. Only the comment's absolute wording overclaims — soften it.
2. **[blind] Hoisted `to_screen` computes `cur` on paths that draw nothing** — in Full assist with a live ok preview, neither branch draws yet `cur` is computed. One multiply-add per drag frame; the PR body documents the deliberate hoist (one shared anchor definition — cannot drift). Harmless, no fix needed.
3. **[blind] "Glow_Only shows no numbers at all" vs the rejection label drawing in every assist mode** — the rejection branch has no assist-mode guard, so an invalid drag in Glow_Only still draws the rejection text. Behavior UNCHANGED from v2 (the old rejection had no guard either) and the phrasing targets the cost/route NUMBER readout (the rejection is text, not a number). Comment precision only.
4. **[tests] Rejection-at-cursor draw has no automated coverage — AC3's documented-sweep branch accepted** — no layer renders the HUD drag state; AC3 explicitly sanctions "a regression test if practical, a documented sweep otherwise", and the sweep is documented + verified accurate. Recorded as spec-sanctioned residual risk.

### Reviewer agreement

No multi-lens disagreement on verdict-relevant claims. The two merged pairs (comment overclaim, edge clipping) were reported independently by two lenses each; all other findings are single-lens and code-verified.

**Verdict:** READY TO MERGE — the user-reported collision is genuinely fixed (rejection at the cursor, legend exclusive at (12, 76)), the implementation matches the established cost-readout pattern exactly, the diff is surgical, and every local gate is green with zero golden shift. W1–W3 are follow-ups, not defects in this fix.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
