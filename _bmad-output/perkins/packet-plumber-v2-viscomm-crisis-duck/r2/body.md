# Perkins round 2 — fix-audit verdict: APPROVED ✅

**PR:** #102 · **sha:** `0c86e83ec568dd4900352512c165fe9dedf4f943` (head stable — re-fetched at post time) · **model:** glm-5.3 (all lenses + round, pinned & session-verified) · **verdict: 0 blockers, 6 warnings, 11 notes → APPROVED.**

**CI caveat (once):** remote CI on this sha is billing-blocked (6-second failed runs, runner never started — known class). Per the standing ruling, local harness runs at the sha are the ground truth; all executed green below.

**Chunking:** big-diff policy — c1-docs (2041 lines: `_bmad-output/**` + `_pr_body_*` mirrors) + c2-code (1229 lines: `app/render/**` + goldens + harness). One full 7-lens wave per chunk, sequential. Chore fold 8c482ec re-verified verbatim vs the main checkout: **8/8 byte-identical**. Lens time weighted to the render code per the briefing.

**Local verification (ground truth, all at the reviewed sha):** `odin test app` **48/48** · `app/render` **100/100** · `core` **261/261** · `tools/lint.sh` **all gates green** · `tools/harness.sh palcheck` **all green** (incl. the new §7f Dublin legs) · `tools/harness.sh run` **49/49 demos green, zero golden drift** · `drift-check` **353/353 mutations rejected**. Worktree left `git status --porcelain` EMPTY after every mutation leg.

## B1 mutation verification (the round's headline — verified independently)

The r1 blocker claimed the Dublin street-block recede was mutation-vacuous. The §7f fix gates it. Verified RED-then-GREEN in the detached worktree:

| mutation | method | result |
|---|---|---|
| whole block recede bypass | `col := fam` + `edge := fam` (fill + edge, dublin.odin:363/371) | **RED** — §7f "non-involved block recedes" FAILs (receded 114 / raw 41) |
| edge line alone | `edge := fam` (fill recede intact) | **RED** — same leg FAILs |
| factor bypass (r1 standing leg) | `desat_f := f32(0)` at view.odin:531 | **RED** — 6 §7 failures (band, chip, rider, at-node ×2, mid-ramp, reduced-motion) |
| restore | `git checkout` ×3 | **GREEN**, porcelain clean |

Layering note (sound): §7f feeds `desat: 1.0` explicitly to `draw_nodes` — it owns the dublin.odin surface; the other six legs own the view.odin:531 seam. A gate that cannot be made to fail would be a blocker — this one bites on both deletion forms.

## Fix audit — r1 findings vs the current worktree (re-read, not trusted)

| r1 finding | r2 classification |
|---|---|
| **B1** Dublin recede mutation-vacuous (blocker) | **FIXED** — §7f leg; mutation-verified above (3/3 RED, restore green) |
| **W1** missing 6th golden table row | **FIXED** — `a11y_scale@65s` row present (mirror line 68) |
| **W2** catalog leak in chain test | **FIXED** — `defer pp.catalogs_destroy(&cat)` (palette_polish_test:412); leak WARN gone from suite output |
| **W3** `scan_col` x-axis unguarded | **FIXED** — both-axis guard, mirrors scan_box |
| **W4** advisory gate CONCERNS (Dublin gap) | **CLOSED on its blocker** — the Dublin gap is gated; the thin single-scene pins remain (see W3–W5 below; the gate stays CONCERNS, disclosed) |
| **N1** render-test count 99→100 | **FIXED** (100/100 re-verified live) |
| **N2** frontage-edge alpha trap | **FIXED** — RGB mix + measured comment |
| **N6** reduced_motion not in save/defer set | **FIXED** — `sv_rm` joins the save set |
| **N7** banner doc orphaned | **FIXED** — doc adjacent to `draw_crisis_banner` again |
| **N8** basis-switch pin single-row | **FIXED** — genuinely two-row now (A+B rows, capture-before-mutate) |
| **N13** purity wording (settings flag) | **PARTIAL — still present**: the spec's change log claims "the derivation comment names reduced_motion as a settings flag," but no such wording exists in crisis.odin (contract block unchanged at :80). Comment-only; see N11 |
| fan-stub forward-wiring unnote'd | still present (accepted class; N10) |
| ring/wash/glint golden-only pins | still present (W5 sharpens it) |
| primitive-fallback divergence | still present (N4 adds the play-triangle surface) |
| spine template / dead links / absolute path (pre-existing, verbatim) | still present (N7–N9; owners: egress-qos / gauge jobs' backlogs) |

## New findings — verified against the worktree (27 lens findings → 25 survive, 2 rejected; dedupe merges 9 → 16 unique + 1 Perkins fix-audit finding)

### WARNINGS (6)

**W1 — Tie-mirror CVD table computed without the shipped mode tables** `[codebase]` · `_pr_body_viscomm_tie.md:55-63`
The W1 advisory deliverable's refreshed table (deutan 142.2/214.2, protan 191.8/248.5, tritan 129.6/86.2) claims "the same simulation harness/palcheck.odin runs" — but Perkins reproduced those exact numbers only by simulating the **base palette** without `palette_apply_mode`; the oracle applies the mode tables first and measures **102.8/202.1, 120.8/236.5, 184.8/105.0**. Both sets pass the 48 threshold (no gate impact), but the mirror documents the wrong method under an oracle-provenance claim — the exact defect class W1 was folded to fix. *Fix: recompute from the effective palette or re-caption the table as base-bytes simulation.*

**W2 — deutan and protan goldens are byte-identical: `modes.deutan == modes.protan` in palette.json** `[blind]` · `data/palette.json` + `goldens/a11y_{deutan,protan}/*`
Verified: identical git blobs at BOTH capture ticks, **and already identical on the v2 base** (d46aa141 both 65s) — the re-bless faithfully carried a pre-existing identity; `modes.deutan` and `modes.protan` are literally equal tables (17 entries). The corpus is self-consistent (each demo compares its own mode's render), so nothing fails — but two nominally distinct CVD modes render identical frames. **Pre-existing on v2, NOT introduced here; routed to the a11y/palette owner (cross-job flag, not this PR's rework).**

**W3 — Halo raw-blend fix is golden-pinned only** `[tests]` · view.odin:848 · the r1-fix's only guard is the juice@65s composition (1,934 px of raw-based halo on one congested bundle). Scene-timeline drift (the class deferred-work.md already documents for surge/estate_surge) would silently orphan the pin. A §7-style halo leg (or unit pin on the blend base) would close it.

**W4 — Lane-stripe recede loops golden-pinned only** `[tests]` · view.odin:885-891 · 18,455 px of receded lane composites in juice@65s, zero §7 lane pixels, no unit pin. Same single-scene drift exposure as W3.

**W5 — Router tier ring/wash/glint recedes golden-pinned only** `[tests]` · view.odin:1685/1757/2044 · 58 px of receded basic-tier ring carries the bird's-eye tier-read canon pin. Thin; same class as W3/W4 (r1 N10 sharpened by measurement).

**W6 — Advisory test gate: CONCERNS** `[tests]` · P0 100% multi-layer (unit purity + §7 draw-path + goldens + mutation legs re-verified this round); P1 accent surfaces (lanes/halo/ring/glint) ride single-scene golden compositions → ≈85%. Closing W3–W5 lifts it to PASS.

### NOTES (11)

- **N1 — Dublin block fill recede applies BOTH RGB mix and alpha twin** `[acceptance ×2, architecture ×2 — 4-source agreement]` · dublin.odin:363-364. rlsw renders the fill opaque (goldens pin RGB-only); the GPU app blends fam.a 204→71 on top of the mix, receding played-renderer blocks deeper than every other surface. Comment-documented as "rides the RGB MIX" but the alpha scale remains — belt-and-braces or divergence; a one-line comment update (or deferred-work entry) settles it.
- **N2 — Spec verification record says "7 palcheck FAILs under the factor bypass"; measured 6** `[acceptance ×2]` · spec:97. Direction true, counts stale (body says "five," spec says 7, actual 6 — the involved-at-node leg passes under bypass by design). Refresh on the next spec edit.
- **N3 — CRISIS_FADE16 byte-duplicates EASE16 with the independence rationale only in the PR body** `[architecture]` · crisis.odin:117. Values identical today by design; a future dedupe-refactor would silently re-couple gauge/crisis timing. Add the "do not dedupe" comment at the table.
- **N4 — Content_Host play-triangle stays raw in the primitive fallback** `[blind]` · view.odin:1213. Hardcoded {250,246,238} while body/roof/wash/chip recede around it — dormant path (sprite atlas always loads), sub-case of the r1 fallback-divergence note.
- **N5 — Chip outline full-alpha while its glyph fades to 35%** `[blind]` · view_type_chip. Coherent with the documented split (glyph = identity, chip paper/ink = chrome) but the never-recede list names only "chip glyphs" — one clarifying line in the contract block would close it.
- **N6 — Chore-fold artifacts undisclosed in the PR body** `[acceptance ×2]` · 8c482ec carries ~10 stranded files. Spec-mandated (Gru hygiene ruling 2026-08-25, carried in the briefing); re-verified verbatim 8/8. A one-line body mention on the next mirror refresh.
- **N7 — ARCHITECTURE-SPINE.md ships as a raw unfilled template** `[architecture, blind, codebase — 3-source agreement]` · pre-existing, verbatim-preserved; belongs to the egress-qos job's backlog.
- **N8 — Gauge-spec review links point into a swept .herdr worktree (17 dead links)** `[codebase]` · pre-existing verbatim; mirror-hygiene pass.
- **N9 — deferred-work.md mixes one absolute source_spec path into a relative file** `[architecture, codebase]` · pre-existing gauge entry; normalize on next edit.
- **N10 — Dormant-path recede sites have zero reachable coverage** `[tests]` · fan-stubs behind off-by-default flags + primitive fallback. Accepted forward-wiring (r1 carry); pin if the flags ever default on.
- **N11 — N13's claimed wording fix did not land in code** `[perkins fix-audit]` · the spec change log asserts a "settings flag" clarification in the derivation comment; crisis.odin:80 still reads "NO app-fed View state" without it. Comment-only; land it with N1/N3's comment pass.

### Rejected (2, disclosed per the accuracy mandate)

`blind-c1#1` (gauge refill leg "vacuous" — premise wrong: the zombie-fix re-anchors t0=20 at the refill; reads traverse phases 0–16 of a live tween) · `blind-c1#2` ("no code hunks" — cross-chunk artifact; c1 is docs-only by design, the code fixes verified in the worktree).

**Dedupe:** 25 surviving → 16 unique (merged: Dublin double-recede ×4 → N1; spine template ×3 → N7; chore-fold ×2 → N6; 7-vs-6 ×2 → N2; deferred-path ×2 → N9; gate ×2 → W6). The c2 `[]` empties (edge/security/codebase) are deliberate reasoned results, not dead-pane artifacts — lens transcripts verified.

## Verdict

**APPROVED — 0 blockers.** The r1 blocker (B1) is fixed and independently mutation-proven (3/3 RED, restore green, porcelain clean); every r1 warning closed; the corpus is green with zero golden drift; the desat mechanism is byte-identical when inert. The 6 warnings are coverage-thinness (W3–W6) and pre-existing/routed a11y-table + mirror-accuracy items (W1–W2) — none block the LOOK-canon surface this PR ships. The 11 notes are comment/doc polish and pre-existing verbatim-fold content owned by sibling jobs.

*— Perkins (glm-5.3, thinking max), round 2 fix-audit, 2-wave 7-lens swarm, 27→17 findings after verification.*
