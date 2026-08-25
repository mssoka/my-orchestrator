# v2 look polish — raising the Odin build to the UE slice-1 / Mini Motorways bar

The v2-look-polish pass (ODIN FOCUS): the user played the UE slice-1 build and set the bar — the Odin build should read at the Mini Motorways look level out of the box. This PR is the answer: a **presentation-only** polish pass (the sim never saw a byte) delivered as 6 reviewable commits + pins, with the before/after goldens, the UE/MM comparison analysis, and the measured perf.

## The gallery (before/after, same scene, same seed)

Full interactive gallery (lavish artifact): `_bmad-output/pr-bodies/v2-look-polish/gallery.html` — open it to annotate. Key frames inline:

| | BEFORE (HEAD) | AFTER (this PR) |
|---|---|---|
| juice 30s (calm) | `frames/before-juice-30000ms.png` | `frames/after-juice-30000ms.png` |
| juice 65s (surge) | `frames/before-juice-65000ms.png` | `frames/after-juice-65000ms.png` |
| terminals close-up | `frames/crop-terminals-before.png` | `frames/crop-terminals-after.png` |
| side-by-side | | `frames/side-by-side-juice-30000ms.png` |

UE slice-1 reference (the bar, read-only): `frames/ue-slice1-2-drawn-pipe.png`, `frames/ue-slice1-3-packet.png`.

## What changed (7 commits + pins)

1. **Soft shadows** — node contact shadows 33%→16% alpha ink, oversized + closer (the UE "soft blob" recipe). Juice 30000ms: 3694/921600 px differ, shadow footprints only.
2. **Ribbon casing** — a darker opaque under-stroke with round caps under every pipe band (the UE "tube"/casing read); tier color darkened 22% toward ink, OPAQUE on purpose (the rlsw line-alpha divergence trap). 5548 px differ — 5391 exactly the three predicted casing blends.
3. **Canvas warm-paper lift** — #E8DDC2 → #EDE2C8 (the UE step; the reference reads ~#F2EEE3); settings chip stops hardcoding the hex; look-book amendment 8.
4. **Packet glint** — warm-cream highlight on circular dots (the MM-car read). Diff = glint color only.
5. **Unit pins** — casing blend exact values + shipped canvas token; fixed a pre-existing 12B palette-load leak (json parse tree never destroyed).
6. **Gate r1 (user feedback)** — stream (triangle) glints + the MM-ward sprite touch-up: thin canon-ink outline plates under every terminal + flattened wall bands (no more pseudo-3D extrusion read).
7. **LEFOU system-tone pass** — the comparison's ranked findings: pipe tiers muted to the gray-blue family, water/park desaturated, grid 18%→9% (tokens only; tier read survives on width + warmth + the lane stripes).

## Kyle diff-analysis vs the reference (what differs, what I changed because of it)

Per the 08-21 user doctrine, the vision mega-minion **Kyle** (`zai-coding-cn/glm-4.6v` — the doctrine's model, downgraded from 5v-turbo which the subscription lacks: 429/1311; the earlier 5v-turbo attempt is documented in the ledger) was summoned to compare current-game frames against the reference and recommend changes. Three comparison sheets (early-game vs UE slice1-2, mid-game vs UE slice1-3, dense vs mid) — Kyle's run + the accuracy-verified `vision-read` (qwen) fallback run.

| Finding (Kyle + the qwen fallback) | Verdict | Action taken |
|---|---|---|
| Ribbon hue load (qwen, all 3 runs): "six saturated ribbon hues braid into noise at the hub" | Implemented (compromise) | Pipe tiers muted into the gray-blue family (copper → warm gray, steel → neutral, fiber → muted slate) — the tier read survives on width + warmth + the QoS lane stripes; white ribbons deferred (tier color is load-bearing canon) |
| Ribbon width −30%, paper-thin (Kyle) | Held for the user gate | Conflicts with the 7.1 gate-approved band language (×2.2 tier band + inset lane stripes); a trim is a one-line constant if the gate rules for it |
| Grid: "second-loudest element, reads as graph paper" (qwen) | Implemented | Grid blend 18% → 9% |
| Water/park blobs "loudest thing on screen" (qwen) | Implemented | Water #A4C7D8 → #B3CDE0, park #A0C294 → #AAC69E |
| Shadows 16% → 8% (Kyle) | Kept at 16% | The UE look-parity checklist's own recipe is 14% — 16% matches it |
| Canvas → #F0E6D2 (Kyle) | Held for the user gate | A ~1% warmth nudge; marginal vs the re-bless churn |
| "White ink outlines" on buildings (Kyle) | Skipped | MM buildings carry DARK outlines (we shipped ink); white would vanish on the cream |
| Node halo rings, packet size/glow variation (both lenses, diverging) | Skipped / on-target | Pucks are two-tone canon; the 1.3 outline + 08-21 glint are the packet read; qwen said "no glow" |
| Node spacing changes in dense areas (Kyle) | Skipped — OUT OF SCOPE | Node positions are SIM STATE; the presentation-only constraint forbids touching them |
| Map geography (peninsulas, lobe radii) (qwen) | Skipped | The 7.4 gate approved the map style |
| Density-based packet hiding + auto camera zoom (qwen) | Named follow-ups | Would misrepresent sim data / new camera behavior |

The **real Mini Motorways frame comparison is PENDING** — the user's MM reference drop at `/Users/moses/code/_local-refs/mm/` (IP guardrail: never committed; referenced by local path only) contained only the README at the time of writing. The UE slice-1 self-assessment above is the committed surface; the MM step will be appended when the frames land.

## Honesty notes (the re-bless discipline)

- **T1 byte-identity:** every re-blessed `.log.bin` + `.t1` is byte-identical to HEAD (`cmp -l` verified across all 45 demos after every commit) — the view never perturbs the sim.
- **T2 re-bless:** deliberate, per commit, cause-documented (diff bundles under `goldens/_reports/`; the pixel counts in the commit table above).
- **palcheck:** 38/38 green; the map-land pin re-pinned to the new canvas hex; the sprite pins were already the roof-panel tones (still emitted — no pin churn); the a11y mode tables untouched byte-for-byte.
- **Perf (measured before/after, median of 3 runs, full demo runs):** juice 0.84→0.84s (final state), juice 0.86→0.85s / estate_surge 0.59→0.60s / qos_contention 0.21→0.21s (intermediate state) — no measurable regression (the added draws are a handful of primitives per bundle/node; zero per-frame allocations).

## Decisions & rationale

| # | Decision | Rests on | Rejected alternative |
|---|---|---|---|
| D1 | Keep the tier-colored pipe bands (casing added, colors unchanged) | Pipe tier = load-bearing gameplay info (canon) | White roads from the UE fixture (would lose the tier read) |
| D2 | Canvas lift is partial (#EDE2C8, not #F5F0E4) | Our canvas also carries the landmass + grid + HUD contrast | Full UE value (would flatten the map tokens) |
| D3 | Casing is an OPAQUE solid, never translucent | rlsw line primitives ignore alpha — translucency would diverge between the GPU app and the goldens | Alpha-blended rim |
| D4 | Shadows only under nodes (not under pipes) | The UE recipe; pipe shadows would need translucent line draws | Pipe drop shadows |
| D5 | Sprite touch-up keeps all canon details (play-marking, LEDs, roof tones) | The 7.1 gate approved them; palcheck pins them | Full MM strip-down to single-fill shapes (breaks the pins + the approved family) |
| D6 | Full-repolish scope (08-21 user amendment): not bound to preserve prior look-layer choices — subsystems redo where the comparison says so | The Gru relay (user-approved) | Scope-limited polish |
| D7 | Pipe tiers muted (not white) — the LEFOU "neutral ribbon" direction lands as a muted gray-blue family; the tier read stays (width + warmth + lane stripes) | Tier color is load-bearing gameplay info; the briefing's "gray-blue system tones" | White ribbons (the UE fixture's literal look — loses the tier read) |
| D8 | LEFOU's density/zoom/map-geography recommendations deferred or named follow-ups | The 7.4 map gate, the sim-truth rule (never hide packets), camera scope | Implementing them in the presentation-only pass |

## Scope amendments carried (08-21, from Gru)

1. **Vision mega-minions (Kyle) on `zai-coding-cn/glm-4.6v`** — user-ruled doctrine (renamed from the original LEFOU/5v-turbo naming: 5v-turbo is not subscription-available — 429/1311; the doctrine's model is 4.6v). The comparison ran on both Kyle and the `vision-read` (qwen) fallback; the findings + triage are in the analysis section.
2. **MM-comparison workflow approved** — side-by-side vs the real Mini Motorways reference; the user drop is pending at `_local-refs/mm/` (outside repos; IP guardrail respected — the committed surface is our frames + the checklist).
3. **Full-repolish scope approved** — hard constraints unchanged: presentation-only, compiles at every push, gates green, 60fps.

## Verification

- `tools/ci-local.sh --mac` — **10/10 gates green** (lint, unit tests, app build, harness T1/T2, palcheck, drift-check, preview-check, PP_DEBUG builds, stats-check, input parity).
- `odin build app -out:app.bin` — compiles + links (the user's playing build stays runnable at every push).
- T1 byte-identity (`cmp -l` on every `.log.bin`/`.t1` vs HEAD) — proven after every commit.

