# Briefing — packet-plumber-hud-warning-overlap-fix (drag-warning / strain-legend collision)

- **Job id:** `packet-plumber-hud-warning-overlap-fix`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `hud-warning-overlap-fix`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (app-surface gameplay code — the U3 scope guard reserves
  `pr_review=0` for CI/ops-tooling).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (current @ 948996d or newer — Job A/B/C + W1 pin + 4.1/4.2 merged).
  Rebase onto origin/v2 if it moves mid-work.
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will be
  red/not-started until the user fixes it. NOT a code failure. Run the FULL local suite
  green (`odin test`, `harness run`) before opening the PR; Perkins verifies locally.

## Mission — one precise HUD collision (user-reported 2026-08-14)

**The bug:** when the player drags an invalid link, the rejection warning overlaps the grey
strain-legend row that starts with "node strain". Root cause is exact — in `app/main.odin`
TWO texts draw at the same position `x=12, y=76`:

1. The 4.1 strain legend (added later, never checked for collisions):
   `draw_text(app, lead_s, 12, 76, 14, p.ink_soft)` — "node strain ~30s to critical / …"
2. The drag rejection warning (older):
   `draw_text(app, reject_label(app.drag.valid), 12, 76, 16, rl.Color{200, 60, 60, 255})`

The warning draws over the legend → red-on-grey overlap. (Screenshot evidence: the user's
2026-08-14 02:32 screenshot, if you need it.)

**The fix — anchor the warning at the drag cursor:** the cost readout already has the
pattern, a few lines below the bug:

```odin
cur := rnd.to_screen(&app.view, app.drag.wx, app.drag.wy)
draw_text(app, label, i32(cur.x)+12, i32(cur.y)-14, 16, p.ink)
```

Move the rejection draw to the same anchor (`cur.x+12, cur.y-14`, red, 16px). No new
collision is possible: the rejection shows ONLY when `app.drag.valid != .None`, and the
cost label ONLY when valid — they are mutually exclusive by construction.

**Acceptance:**

1. Dragging an invalid link (e.g. terminal→terminal, span-exceeds-tier, self-loop) shows
   the red rejection AT the cursor — never at (12, 76).
2. The strain legend row renders clean at (12, 76) with no occlusion, in every run-mode
   state.
3. Collision sweep (prove in the PR body): enumerate ALL fixed-position `draw_text` y
   anchors in `app/main.odin` run mode (36, 56, 76, 96/114/132/156 selected-pipe block,
   bottom-left SLA rows, bottom-right assist rows) and show none overlap — a regression
   test if practical, a documented sweep otherwise.
4. Game-over mode untouched; the QoS toast (12, 156) untouched.
5. `odin test` + `harness run` green; **goldens MUST NOT shift** (verify no T2 capture
   shows the rejection; any shift = STOP and flag).

**Verify:** local suite green, launchable increment in the PR body (drag an invalid link →
   warning at the cursor, legend clean).

**Scope guard:** the warning position ONLY — no other UI changes, no core changes, no
behavior changes.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: hud-warning-overlap-fix
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
