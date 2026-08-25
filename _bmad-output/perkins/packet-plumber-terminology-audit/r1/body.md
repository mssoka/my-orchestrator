## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-terminology-audit · **Reviewed sha:** b9d5006 · **Reviewers:** 7/7 completed
**Verification:** 259/274 findings confirmed against the code — 15 discarded as false-positive

**The one hard blocker — serialized contracts untouched: HOLDS.** LOG_VERSION stays 4 (comment-only); tag constant keeps value 5 (name-only); all 29 `.log.bin` differ in EXACTLY the 8 catalog_hash bytes at offset 17 (`bdc90b1363c93d8b` → `8f94df8eb817dddb`), sizes identical. **Splice proof REPRODUCED independently**: in a scratch copy with one hook line (`cat.hash` forced to the old value; sim bytes untouched), all 29 demos reproduce the OLD goldens exactly — every tick of ~22k — and the old logs replay green. **T2: zero PNGs in the diff**; the harness capture path never calls the app HUD, so the renamed legend string moves no golden pixel. Gates at this sha: `odin test core` 183/183 · `lint.sh` 6/6 · `harness run` 29/29 (T1+T2+replay) · drift-check 204/204 rejected. Token-normalized hunk comparison proves every code/test change is rename-only — zero behavior deltas.

### Blockers (0)

### Warnings (2)

**1. The node-health inspect card still renders "STRAINED" — a rendered coinage string the audit's inventory missed** *(acceptance, architecture, blind, codebase, edge, security, tests — 7-lens agreement, 22 filings)* — `app/render/node_health.odin:25`: `if lvl == .Amber { return "STRAINED", p.state_congested, "!" }`. The PR renamed the type and the palette field on this very line but left the player-facing label; the audit's "Rendered HUD strings carrying coinage" table lists 6 strings and this 7th was never inventoried — so it is neither folded nor listed-as-kept, and the legend now says "node congestion" while the hover card screams "STRAINED". The card is app-hover only (the harness never renders it), so the decision has zero T2 impact either way. **Fix:** decide + list — rename to "CONGESTED" as a deliberate listed fold, or record the keep in the PR body.

**2. The audit record §4 contradicts itself and this PR's canon entry on Phase-2 / 5.2 status** *(acceptance, architecture, blind, codebase, security)* — `_bmad-output/implementation-artifacts/terminology-audit-v1.md:112-118`: the heading says "Phase 2 scope (NOT started — verdict cleared, 5.2 gate remains)" and Gate 2 says "5.2's merge (still OPEN)… NOT merged to v2 as of 2026-08-15", while the same section's Gate-1 bullet says "**Phase 2 shipped 2026-08-15** (PR #55)" and the decision-log canon entry records 5.2 "merged 2026-08-15, PR #54". The shipped evidence trail reads two contradictory states. **Fix:** amend §4's heading + Gate-2 bullet to the shipped state.

### Notes (11)

1. **Live demo comments still name `Cmd_Set_Emphasis`** *(6 lenses)* — `demos/qos_manual.dem:4`, `demos/qos_auto.dem:7`. Comment-only; the sweep didn't visit these files.
2. **`data/demand.json` `_comment` still cites `scripted_plan_pressure`** *(6 lenses)* — `data/demand.json:2`. Fixing it re-folds catalog_hash (every golden re-blesses) — bundle the fix with the next catalog-touching PR or accept as documented residue.
3. **"pressure-plan director" became "congestion-plan director"** *(architecture, security, tests)* — `core/flow.odin:51`, `harness/demo.odin:28`. The canon maps Pressure_Plan → **Demand**_Plan; the mechanical substitution conflated the two renames. Say "demand-plan director".
4. **Drop-"ladder" coinage survives in live comments** *(6 lenses)* — `core/catalog.odin:184`, `core/crisis.odin:26,71,126,235,391`, `core/flow.odin:62`, the `Drop_Reason.Queue_Overflow` comment, `demos/qos_contention.dem`/`sla.dem`/`surge.dem` + test-file comments. (The unrelated auto-reserve / routing-cost / port ladders are correctly untouched.)
5. **Ordinary-English "pressure" over-renamed to "congestion"** *(5 lenses)* — "time congestion" (gdd.md:73,107,367), "modernization congestion" (epics.md:75,154; gdd.md:478; stories-v2:873), "congestion-riser stings" (gdd.md:555), "sustained congestion" (gdd.md:291), "fair congestion" (gdd.md:430). The verdict renamed the coinage; these were idioms.
6. **stories-v2 half-sweeps** *(4 lenses)* — :365 "Strain metrics…" kept on the line whose "pipe pressure" was renamed; :295 "the full ladder BE → Standard → Express [E9]" kept.
7. **ASCII diagram borders misaligned by un-padded renames** *(acceptance, architecture, blind)* — GDD core-loop box row now 79 vs the 73/75 grid (gdd.md:84-89); arch §5 component diagram similar.
8. **Mechanical-rename grammar warts** *(6 lenses)* — `types.odin:173` "Amber = congested/congested"; "never congestion" as a verb (warnings.odin, node_health.odin); "must actually congestion a node" (node_health_test); spec-4-1 code map "(congestion, congestion, …)"; M5 table "congestion 20 s".
9. **Swept canon docs keep scattered old coinage** *(6 lenses)* — arch ODN-12 intent list + §10.3 demo sketch still say `Set_Emphasis` (:731,:1403); epics.md:48 "priority-emphasis dial"; spec-4-1:26 "Strain measure" heading; spec-traffic-model:149-150 `scripted_plan_pressure`/`Pressure_Plan`; gdd.md:108 "a straining bundle"; arch §6.3 "lane scheduling inside a link"/"the same 3 lanes" (two-tier: docs say class queue).
10. **"emphasis" vocabulary residue in live code** *(7 lenses)* — `validate_set_emphasis`/`apply_set_emphasis` proc names (the audit's ruled scope was "one union variant + comments", so never ruled renamed — but now durably mismatched with `Cmd_Set_Weights`); qos_test/app "emphasis" comments; balance.json's "3.2 emphasis-dial" gloss; the `press` local in warnings.odin. Optional consistency sweep.
11. **Advisory test gate: PASS** *(tests)* — 183/183 green; Perkins' hunk comparison proves every test-delta line is rename-only (zero assertion changes). The c1 tests lens filed CONCERNS citing the sweep residues; re-gated after mechanical proof — the residues ride as notes 1–10.

### Reviewer agreement
- **"STRAINED" card label survived** — all 7 lenses
- **"emphasis" proc-name/comment residue** — all 7 lenses
- **demo-comment + demand.json `_comment` residues** — 6 lenses each
- **Audit §4 self-contradiction** — 5 lenses

_**Round ops note:** the deepseek provider returned `402 Insufficient Balance` mid-round; the g13/g14 waves + two single-lens retries were swept and redispatched on `zai-coding-cn/glm-5.3` per the provider-incident doctrine (probed first). All 112 lens outputs recovered; no failed layers. The 15 discards: 10 historical-record exemptions (the 5.8 SET_EMPHASIS note), 3 documented back-compat (the `emphasis` demo DSL), 1 out-of-scope (pre-existing `bundle_class_queue`), 1 misread (the fold-table lane_* keys were deliberately not renamed per the two-tier ruling)._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
