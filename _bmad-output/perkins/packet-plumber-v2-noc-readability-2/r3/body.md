## 🤖 Perkins automated review — round 3
**Job:** packet-plumber-v2-noc-readability-2 · **Reviewed sha:** 7bff26e · **Reviewers:** 7/7 completed
**Verification:** 23/26 findings confirmed against the code — 3 discarded as false-positive, 1 kept trimmed

### Fix audit (the r2 fold)

| r2 finding | status |
|---|---|
| **B1'** header collision ("loS&A" + clipped /3s) | ✅ **FIXED** — headers right-aligned at their `noc_col` anchors; "loss" ends 1134 / "SLA" starts 1150 (16px clear); "/3s" ends 1262 ≤ 1274. Pixel-verified on **4 captures incl. one generated this round from the reviewed bytes** (inline k3 vision). |
| **W1'** popover occluded w/ clickable demolish | ✅ FIXED — `popover_rect` clamps to `play_w` (byte-identical rail-off). Untested → W2''. |
| **W2'** preview re-anchor untested | ✅ FIXED — `upgrade_preview_anchor` pure + pinned. |
| **W3'** resize re-apply unpinned | ✅ FIXED — reset/re-apply pinned. |
| **W4'** rail-on camera threading | ⚠️ PARTIAL — `camera_update` pinned at rail-on geometry; zoom/pan/pullback call sites still unpinned → N1''. |
| **W5'** plate owns wheel-not-clicks | ❌ **FIXED WITH A NEW DEFECT** → B1'' below. |
| **W6'** gate CONCERNS | 🔁 recomputed — still CONCERNS (W4''). |
| **N6'** stale live PR body | ✅ FIXED — live body now matches the shipped repo copy. |
| N1'/N2'/N5'/N7' | still present (comment/formula staleness — carried, all re-found by this round's lenses). |

Mechanical re-proofs on the reviewed bytes: **48/48 goldens green locally** (rlsw), core 236/236, app 41/41, render 74/74, input 13/13; overlay-pixels smoke bites (**94,320 changed px** in the rail rect); overlay .t1 sidecar **1202/1202 byte-identical** to the blessed surge stream (AC3); ladder triplet named + pinned (20/18/15 ≥ 14px floor); ring buffer 256 unchanged; view-layer only.

### Blockers (1)

**B1'' — the W5' plate press-swallow deadens the two rightmost tray chips that paint over the plate** [edge, architecture, blind, acceptance, codebase — agreement ×5] · `app/main.odin:1201`
The new swallow (`noc_panel_hit` over the full-height rect → `return true`) runs before the tray hit-test, but the bottom band stayed win_w-anchored (the r1-W1 decision): the 6-chip tray spans **[332, 948]** while the plate spans **[756, 1280]** full height. Chip 4 (`router_mid`, [748,844]) is 88/96px dead; chip 5 (`router_high`, [852,948]) is **fully dead** — and the tray draws *after* the rail (`draw_tray` at :1567 vs rail at :716-721), so both chips are **visible but unclickable while D is on**. Worse at UI ×1.25/×1.50 and at min window 1152. The swallow's own comment ("the clickable surfaces — QoS, tray, chip, popover — are all inside the playfield") asserts the false invariant. Introduced by this commit — before it, these clicks reached the tray.
*Fix:* hit-test the tray/settings chips **before** the plate swallow (mirror the draw order — the bottom band paints over the plate, so its clicks must win too) or clamp the swallow above the tray band; reconcile the comment; pin a chip-5-center press reaching the tray with `overlay_on`.

### Warnings (4)

- **W1'' — the W5' swallow wiring has zero test coverage** [tests] · `app/main.odin:1201` — only `noc_panel_hit`'s boundary is pinned; no test exercises `effect_ui_press`. The exact pin that would have caught B1'' doesn't exist.
- **W2'' — the W1' popover play_w clamp has no test** [tests] · `app/render/popover.odin:44-58` — zero popover references repo-wide in tests; a revert to `win_w` stays green (the r2 defect class).
- **W3'' — the B1' header pin is alignment-insensitive** [tests] · `app/render/noc_overlay_test.odin:342-345` — reverting the headers to left-aligned `draw_mono_c` (the r2 blocker) passes both asserts; nothing pins right-alignment at the anchors.
- **W4'' — Advisory test gate: CONCERNS** [tests] — P0 pinned; the fix's own new branches unpinned; P1 ~85%.

### Notes (5 new + 9 carried)

- **N1''** [tests, acceptance] W4' residual: zoom/pan/pullback call sites pass `play_w` but are only exercised at `play_w == win_w` (the r2 ask named a zoom clamp assert too).
- **N2''** [edge] The swallow is gated on `overlay_on` alone but the plate only draws when `stats_valid` — clicks over the rail region are eaten with nothing drawn for ≤1 tick after the first D press (the r1-N8 transient gains a click consequence).
- **N3''** [blind, trimmed] Header comments still advertise "large numerals"/"the headline row" for the 18px DROPS counters (title is 20px). The 22→18 choice itself is the adjudicated r1-N2 decision — **not** re-litigated; only the stale comments ship.
- **N4''** [architecture] `View.play_w`'s comment claims "the harness never does" flip the rail — the PP_DEBUG overlay verbs do (only the golden capture path never does).
- **N5''** [codebase] `noc_row_right` is dead code the diff actively maintains (zero call sites; `noc_col` serves the need).
- Carried still-present: r2-N1' (duplicate DOCK-RIGHT comment, re-found ×3), r2-N2' (tests re-implement formulas), r2-N5' ("single source" comment vs re-derived plate), r2-N7' ("Open Sans digits" at :617), r2-N3'/N4', r1-N1/N4/N8.

### Reviewer agreement

- **B1''** tray-chip dead zone — **5 lenses independently** + Perkins' geometry recomputation (tray [332,948] vs plate [756,1280]; press chain and draw order read end-to-end).
- N1'' W4' partial — tests + acceptance. r2-N1'/N5'/N7' persistence — re-found ×2-3 each.

**Verdict:** NEEDS CHANGES

The r2 fold is genuinely good — B1' is fixed at code, geometry, pin, and pixel level, and the zero-drift / stream-neutrality / gate bars were all re-proven locally on the reviewed bytes. But the W5' fix ships a new defect of the exact same surface-ownership class this round was fixing: visible, unclickable router-placement chips under a swallow whose comment claims they don't exist. 1 blocker → NEEDS CHANGES.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
