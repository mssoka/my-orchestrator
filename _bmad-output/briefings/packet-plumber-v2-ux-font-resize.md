# Briefing — packet-plumber-v2-ux-font-resize (user report: font illegible + window un-resizable)

- **Job id:** `packet-plumber-v2-ux-font-resize`
- **Repo:** packet-plumber · **Base:** `v2` (Silas resolves head at dispatch) · **Slug:** `v2-ux-font-resize`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-edge-case-hunter` (layout math + golden surfaces).
- **Perkins:** `pr_review: 1` (rendering + readability canon surface + golden fold).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-ux-font-resize <url>` yourself.
- **Reference:** the prototype (`/Users/moses/code/packet-plumber-prototype-ref`)
  resized fine and its text read fine — diff what it did (window flags, font) vs v2.
- **Sibling note:** 5.2 node-health is in flight and touches `app/render/view.odin`
  (health rings). Expect a same-file base-merge; keep your diff surgical
  (draw_text paths + window init + scale handling) to minimize hunk overlap.
- **CI:** green. Full local suite must pass.

## Mission — fix two user-reported UX defects (USER REPORT 2026-08-15, ruling-grade)

**User's words:** "the font is hard to read" · "i cant seem to be able to resize the
window. prototype could"

### Part 1 — the font (readability canon, a11y 7.3 adjacency)

v2 renders the **raylib DEFAULT font** (see view.odin `draw_health_ring`'s comment:
"the font is the raylib default, software-rendered in the harness so T2 goldens
carry it"). On the light canvas at current sizes it's illegible.

1. **Replace with a readable bitmap font** — a clean, high-legibility font bundled
   as an asset (choose one with an unambiguous license; prefer something with
   strong x-height and open counters; document the choice + license in the PR).
   Load via `rl.LoadFontEx` (or the raylib font path the codebase prefers).
2. **Size + contrast audit:** HUD/legend/stat text minimums raised (nothing below
   ~14px effective at 1280×720; the footer SLA rows and the strain legend are the
   known offenders — small + thin). Verify contrast against the light-canvas
   palette (the readability canon: state must be readable — that includes TEXT).
3. **Golden impact — decide deliberately and document:** T2 goldens carry glyph
   rendering, so a font swap shifts every golden with text. That is an INTENDED
   visual change: fold the affected goldens deliberately (the 5.3-ux pause-ux
   pattern — list every updated golden in the PR body). Sim-level T1 goldens must
   NOT shift (font is presentation-only — if any T1 hash moves, STOP: that's a
   determinism break, not a golden fold).
4. The harness must still render deterministically with the new font (bundled
   asset, no system font loading — ODN-1 no file reads at sim level; font loading
   is app-layer init, fine).

### Part 2 — window resize (restore what the prototype had)

1. Enable `FLAG_WINDOW_RESIZABLE` at window init (diff the prototype's init for
   the exact pattern).
2. **Presentation-only invariant (load-bearing):** resize must NEVER touch the sim,
   serialization, or replay — no LOG_VERSION change, T1/T2 goldens captured at the
   canonical 1280×720 must not shift due to resize CODE (only the font fold from
   Part 1 may shift T2s). The harness runs fixed-size regardless.
3. **Layout handling:** the view already has a scale factor (`v.scale` — the camera
   pan/zoom path). On resize: either scale the render target to fit (letterbox if
   aspect drifts — no distortion) or adapt layout; HUD must remain readable + not
   overlap at sensible sizes. Clamp a minimum window size so HUD can't collapse.
   WIN_W/WIN_H constants threaded through HUD math need an audit — centralize the
   derived-dimensions handling rather than scattering GetScreenWidth calls.
4. Pause overlay edge-chip (5.3-ux) + QoS panel + weather report must survive
   resize without overlap at default AND at the minimum clamp.

**Acceptance:**

1. Both fixes in ONE PR; before/after screenshots embedded in the PR body (font
   close-ups at HUD sizes; resize at 1280×720 default, ~1600×900, min clamp, and a
   non-16:9 drag).
2. T1 goldens unshifted; T2 golden fold (if any) deliberate + listed; full local
   suite green.
3. PR body: font choice + license, size/contrast decisions, resize approach
   (letterbox vs adapt), the min-clamp value, golden inventory.

**Scope guard:** font + window ONLY. No new HUD surfaces, no visibility/gauge work
(queued separately), no 5.2 health-ring changes, no input-parity work.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-ux-font-resize
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
