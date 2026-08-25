## 🤖 Perkins automated review — round 2 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-7.1-visual-juice · **Reviewed sha:** `cb3bf2d` · **Reviewers:** 7/7 completed
**Verification:** 29/33 findings confirmed against the code — 2 discarded as false-positive, 1 kept as [unverified], 1 folded into the carry-forward set

> **Head moved mid-review:** reviewed `cb3bf2d`, head now `5c482df` ("7.1 rebase onto #63 (5.10): re-bless for the catalog drift + the slice-boundary fold") — a fresh round will follow. The blocker below was filed against `cb3bf2d`; the new head appears to be the rebase it asks for — r3 verifies it.

### Fix audit (r1 → r2) — the round's mandate

- **B1 (sprite bbox y flip) — FIXED, mechanically proven.** `content_bbox` emits top-down y: the committed sidecar equals a PIL top-down alpha bbox of all 9 PNGs **exactly**; the as-drawn src windows hold 76–93% alpha fill (the correct regime; r1's broken crop held 24–38%); the juice goldens now carry the wall band, puck greys and LEDs while the r1 golden (negative control @ `dbed6a3`) had **zero** wall pixels; and the new palcheck play-marking canary sits 22/22 rows inside the fixed window vs **0/22** in the r1 window — the gate demonstrably bites a B1-class crop.
- **B2 (cold-boot camera fit) — FIXED.** `view_compute` (main.odin:269, static balance dims) now runs before the first `start_run`; `start_run`'s `camera_set_fit` reads valid world dims and snaps (578–581); `camera_update` derives from the snapped state; resize re-fits.
- **W1 (×2.2 band formula ×4) — folded, with one gap** (W-A below: the assist route-glow, a 5th consumer, kept the pre-band formula).
- **W2 (committed verification) — FIXED.** The palcheck gate is real and wired as gate 5 in both CI homes; it pins per-sprite roofs/host/marking + banner-rect agreement + a live zoomed lane read. Follow-ups: W-B (header overclaims), W-K (puck canaries aggregate).
- **W3 (nav-zoom exit) — FIXED** (`on_cancel` homes the camera even with nothing selected). Seams: N-G (ordering), W-C (last_sel bypass).
- **W4 — FIXED** (5×5 = 25 slots). **W5 — FIXED** (`sla_row_rect` single-source, 5.5 fill + hairline; N-E 2px overlap). **W6 — FIXED** (popover click precedes banner/SLA).
- **Notes:** N6/N7/N9 folded (partial-unload + value-range checks + the harness's capture refusal + the app's fallback log — all verified in code). **N1 still present** (N-A). N2/N3/N4/N5/N8 unchanged (carry-forward, not claimed).
- **The 76-golden re-bless — sound within the branch** (76/76 changed, juice manifests byte-identical, zero non-juice `.t1`/`.log.bin`; T1/replay green, ci-local 10/10 Perkins-run) — **but invalidated going forward by B1 below.**

### Blockers (1)

**B1 — Post-#63 lane collision: this PR cannot merge green.** #63 (narrow `capacity_units` 5→10 — `core/flow.odin` + `data/pipe_tiers.json` + its own 88-file re-bless) merged to `v2` (`ebd02cb`, 21:29) **after** this branch's push (21:17); the branch does not contain it (merge-base `1d7f442`). Consequences, mechanically proven on a scratch merge resolved in this PR's favor:
- **15 golden PNGs are touched by both PRs → 15 binary merge conflicts** (`ecmp_cost` ×2, `forecast_preview` ×4, `forecast_shift` ×2, `health_lose` ×3, `pause` ×2, `surge` ×2) — the merge button blocks regardless.
- **Gate 4 fails 6 demos on the merged tree**: `health_lose`, `juice`, `forecast_preview`, `surge`, `pause`, `forecast_shift` (T2 pixel drift 218–12,311 px/frame — every re-bless here was made against the pre-#63 catalog; e.g. puck sizing reads tier capacities). T1 hashes + replay stay green (pure render-input drift); palcheck stays green. Logs: `merged-tree-gate4.log` in the round dir.

**Fix:** relay the merge/rebase onto `ebd02cb`, re-bless the 6 drifted demos' T2s **on the merged tree** (the re-bless itself resolves the 15 conflicts correctly), document the #63 cause chain in the PR body, push. r3 verifies the merged tree.

### Warnings (11)

- **W-A** `[architecture, codebase]` assist.odin:425/442 — the route-glow halo still sizes from the pre-band wire formula (no ×2.2), narrower than the tier band it overlays; the candidate halo pops on commit. Route both branches through `band_width` (+6·scale halo). *The missed 5th consumer of the W1 fold.*
- **W-B** `[blind]` palcheck.odin:7-15 — the header promises scans of "house bodies AND roofs"; the gate scans roofs only (the §1a comment explains the wall band is occluded — correct reasoning, stale header), and `HOUSE_BODIES`/`HOST_BODY` are declared-but-unused. Align the header (or gate the shaded wall tones).
- **W-C** `[edge]` main.odin:1160–1178/687–689 — `camera_focus_pair`/`effect_cancel` move the camera without updating `last_sel_*`: after a banner-focus detour, re-clicking the *same* selected node never re-homes (no selection diff; ESC/pad-B remains the only exit).
- **W-D** `[architecture]` palcheck.odin:77-93 — `normalize` re-implements same-package `goldens.odin` flip + `swizzle_rb` (both `package main`).
- **W-E** `[blind, unverified]` umbrella: no automated coverage for the new interaction surfaces (specifics: W-F..W-I).
- **W-F/W-G/W-H/W-I** `[tests]` zero committed coverage for: the focus-zoom camera model (palcheck pins only the zoomed lane read), the `on_cancel` exit, the boot-order fix, and the class-focus ghosting (every T2 capture draws `focus_class=-1`).
- **W-K** `[tests]` palcheck's puck canaries aggregate across tiers — a puck_3-only crop evades the gate (per-sprite checks exist only for houses/host).
- **W-L** `[tests]` Advisory test gate: **CONCERNS** (P0 shipped-pixel surface pinned by goldens+palcheck; P1 app-layer interactions ~0% committed — the known charter class, warnings ≠ blockers).

### Notes (13)

- **N-A** `[blind]` view.odin:601-604 — draw_packets header **still** says queued packets "pile at the departure node in lane order" (r1-N1 still present since round 1; the doorstep fan replaced it).
- **N-B** `[blind]` view.odin:216-237 — the comment block still describes the fiber/pooled inner-core draw the diff deleted (per the approved band design — the stale comment is the finding, not the removal).
- **N-C** `[blind]` gen_sprites.py:40,42 — `CREAM`/`DC_VENT` never used.
- **N-D** `[blind]` main.odin:406-410 — banner focus-zoom with empty selection: clicking empty map doesn't exit (ESC/pad-B does). UX nicety.
- **N-E** `[blind]` main.odin:1247-1255 — adjacent SLA hit rects overlap 2px (16px spacing vs 18px rect); the lower row is unreachable in that band.
- **N-F** `[blind]` look-book:161 (added text) — trailer says "a PR opens targeting `main`"; this PR targets `v2`.
- **N-G** `[edge, architecture, codebase]` exec.odin:48-62 — `on_cancel` fires before the placement branch: mouse-ESC mid-draw homes the camera while the draw survives; placement-cancel homes it while the selection persists.
- **N-H** `[edge]` palcheck.odin:196-206 — catalog lookup bools discarded; a rename would build a wrong scene silently.
- **N-I** `[acceptance]` PR body: says the juice golden shows "the health meter" (the demo deliberately runs health off), and the Verification section still says "9/9 gates" (the suite is 10).
- **N-J** `[acceptance, codebase]` ci-local.sh:4-6,28-30 — four "9 gates" strings stale after palcheck (run count itself derives from the array — correct).
- **N-K** `[security]` palcheck.odin:161-165 — the banner-rect `y_base` keys on a whole-file substring `"health on"` of the demo; a future comment containing the phrase flips the expectation (correct today).
- **N-L** `[architecture]` chrome geometry in two homes (banner rect render-owned, SLA rows app-owned) — locally consistent with the pre-existing app-owned gauges; idiom observation.
- **N-M** `[tests]` the doorstep fan's 25-slot no-wrap property is unpinned.

### Reviewer agreement
- **W-A** (architecture + codebase independently) — the strongest signal this round: the W1 fold's missed consumer.
- **N-G** (edge + architecture + codebase) — the on_cancel ordering seam, three lenses.
- **N-J** (acceptance + codebase) — the stale 9-gates text.
- **W-E/W-F..W-L** (blind + tests) — the app-layer coverage cluster.

**Verdict:** NEEDS CHANGES

Everything r1 asked for was delivered — B1/B2 are mechanically fixed, the folds landed, the re-bless chain is documented, ci-local is 10/10. The single blocker is collateral, not regression: #63 merged under you 12 minutes after your push. Rebase onto `ebd02cb`, re-bless the six drifted demos on the merged tree, and push — r3 should be short.

_Address findings and push — I re-review automatically on the new sha._
