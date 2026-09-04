# look(congestion-read): the link congestion telegraph — PURE PULSE, sizes unchanged (A1 as amended)

**AMENDED + REFINED 2026-08-28 (user rulings, relayed by Silas on Gru authority —
supersede the 2026-08-27 A1 width emphasis):** keep link sizes EXACTLY as v2 has
them — no width bump, no min-width floor, no width oscillation — and the pulse is
**GLOW ONLY** (option A of glow/stroke/both): the halo margin's brightness
oscillates while the stroke keeps the steady classic recolor; geometry never moves.
The USER EYEBALL is the final visibility gate — peak-vs-trough corridor captures
are committed in this PR (`_bmad-output/pr-bodies/v2-congestion-read-a1/frames/`).
The r1 width emphasis, its width gates, and its width-strip evidence are superseded
and out of the evidence set.

Spec source: viscomm regression audit (`R1` row; the audit's F4 recorded that no
pulse envelope ever existed on the halo — the pulse is new telegraph behavior under
this ruling). Skill note (the standing waiver): bmad-build's renderer is waived in
this repo (no `_bmad/scripts/render_skill.py`; the 2026-08-21/23 sanctioned path);
step-04 ran as the two-hunter review swarm before the r1 push.

## The change (view.odin, both draw_bundles branches)

- The width line is the **untouched v2 law**: `w := band + 5.0 * v.scale` in both
  branches. `CONGESTION_HALO_FLOOR_WORLD` / `congested_halo_width` are deleted.
- GLOW-ONLY split render (both branches): a pulsing glow pass at the full halo
  extent (`band + 5*scale`, constant v2 width) whose state-color SHARE oscillates
  `CONGESTION_PULSE_TROUGH_SHARE 0.43` (byte-exact v2 blend) →
  `CONGESTION_PULSE_PEAK_SHARE 0.75`, then the STEADY stroke core pass at exactly
  `band` in the classic recolor over it. The stroke's color never oscillates; no
  geometry ever moves.
- The envelope rides the house **`pulse_read`** seam (PULSE16, 16-tick cycle =
  1.25 Hz, phase seeded by bundle id so sibling links don't pulse in lockstep;
  reduced-motion pins the PEAK — the a11y convention).
- `congested_halo_blend(raw, state, share)` — ONE blend derivation for both
  branches; `draw_bundles` gains the `tick` param (the honest oscillator).
- LOOK §3 canon comment: "congested PULSE emphasis, sizes unchanged".

## Gates (mutation leg = delete-the-pulse)

- **Delete-the-pulse (RED -> GREEN)**: freezing the share at the trough fails
  palcheck §8 (a) inline-amber, (b) red, (d) routed, (g) reduced-motion — the
  glow margin measures 0 px at the predicted peak AND the core scan over-runs
  (the whole width collapses to the trough color) — plus the
  `congestion_pulse_law_is_the_ruled_envelope` math pin. Restored: all green.
  The §8 predictions anchor to the RULED CONSTANTS at pinned phase ticks —
  never through the proc under test (the self-confirmation trap).
- **Glow-only split pins**: §8 (a)/(b)/(d) assert the peak-color run == the glow
  margin (5×scale) AND a steady-core run == band exactly — a pulse that leaks
  onto the stroke core, or any width move, fails the same legs.
- **Trough pin (f)**: at the trough tick the whole width renders the
  classic-blend color and the PEAK color is absent (the oscillation moved).
- **Reduced-motion pin (g)**: the envelope freezes at the peak at ANY tick.
- **Calm covenant (c)/(e)**: calm stroke == capped band exactly, zero halo pixels
  at the midpoint AND the end-cap columns, inline + routed. Calm demos'
  goldens: zero byte shift.
- **Vacuity premise**: peak/trough predictions differ by 74 (> 20) on the r
  channel — a flattened envelope fails loud instead of passing vacuously.
- **Suites**: `odin test app/render` 115 green, `odin test app` 51 green, palcheck
  102 PASS, lint all gates green.
- **Sim bytes (ODN-1-safe)**: every `goldens/*.t1` + `*.log.bin` cmp-identical
  across the whole arc (03dd6f8 -> df14785 -> HEAD). Render-only.
- **Re-bless (supersedes the A1 re-bless)**: same 18 congestion-bearing demos,
  33 PNGs — every shifted pixel is the halo's intensity moving along the
  raw->state blend at the capture tick's pulse phase. estate_surge correctly
  unmoved (its fat bundle reads near-trough + no thin-stroke collapse).

## Motion evidence — intensity-over-time series (the ruled deliverable)

Warn demo 44.0–46.5 s (the audit's strip window), 50 frames @ 50 ms,
T1-hash-verified timelines; state-color SHARE projected on the steel->state
blend segment inside the congested corridor:

MAX-share = the glow envelope's top (undamped); MEAN damps toward the steady
core exactly as the split dictates:

| rung | zoom | BEFORE (A1: flat, mean span) | AFTER glow envelope (max) | AFTER mean |
|---|---|---|---|---|
| CORE (fit) | 1.0 | 0.427–0.430 (span 0.003) | **0.440–0.750** (span 0.310) | 0.433–0.589 |
| DISTRIBUTION | 1.4 | 0.427–0.430 (span 0.003) | **0.440–0.750** (span 0.310) | 0.434–0.621 |
| ACCESS (rest) | 2.0 | 0.427–0.430 (span 0.003) | **0.440–0.750** (span 0.310) | 0.434–0.607 |

The AFTER series shows **3 clean cycles in 2.5 s = 1.25 Hz** (peaks 800 ms
apart) — the PULSE16 law measured at pixels. Juice's corridor is crisis-
outline-overdrawn at its capture window (the audit's own strips used warn for
the same reason); its coverage rides on the §8 legs + the re-blessed goldens.
Superseded r1 width strips/CSVs remain on disk in the artifact dir but are OUT
of this evidence set. Strips + CSVs + measurer:
`_bmad-output/implementation-artifacts/packet-plumber-v2-congestion-read-a1/`
(orchestrator home; `measure_halo_pulse.py`).

**For the eyeball gate** — committed in this PR:
`_bmad-output/pr-bodies/v2-congestion-read-a1/frames/glow_peak-vs-trough_warn_z{1.0,1.4,2.0}.png`
(top = PEAK, bottom = TROUGH; 3x nearest-neighbor crops of the congested
corridor). Mechanical cross-check: high-share (>0.65) pixels appear ONLY in the
peak crops — 8,379 / 16,992 / 40,374 px by rung; zero in the trough crops.

## Harness (view-only, T1-safe — carried from r1)

`motion-strip` honors the demo's pinned `zoom` directive + a `zoom=<f32>`
evidence override (duplicate tokens rejected; malformed = usage error) through
ONE `apply_capture_zoom` helper shared with run's directive path; the applied
altitude is echoed in the summary line. Corpus re-run neutral.

## Decisions & rationale

- **Pulse mechanics**: intensity = the halo's state-color SHARE (color math
  only). NOT alpha oscillation — rlsw renders line-primitive alpha as OPAQUE
  (the 2026-08-23 field note), so an alpha pulse would be renderer-invisible.
- **0.43 -> 0.75**: the trough is the untouched v2 blend (byte-exact); the peak
  is a one-constant tunable (`CONGESTION_PULSE_PEAK_SHARE`) pinned by the math
  test's visible-swing bound. No ruling band was given for amplitude; this is
  the implementation choice inside "visibly pulsate", flagged here.
- **Reduced motion pins the peak** (not the trough): the 7.3 convention — "the
  most legible static reading, deterministic + golden-stable."
- **Ruling lineage**: 2026-08-27 A1 (width emphasis) superseded 2026-08-28
  (pure pulse) — the LOOK-SPEC.md itself is untracked in the main checkout, so
  the amendment line lives in the tracked LOOK §3 canon comment (view.odin) +
  deferred-work.md carries the mirror-into-the-doc debt.
- **Out of scope (flag-only)**: R2 lane stripes, R3 Dublin blocks, A2/A3/A4 —
  untouched; the audit's LEAVE recommendations stand.

## CI note

GH-Actions billing block may show 5s runs / zero logs / "payments failed" —
that signature is note-only, reruns are useless; the local gates above are
the merge ground truth.
