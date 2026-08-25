# fix(demo): polish r2 — toast parity proof, reports at real-audit depth, Compare Top 3 real-gate fix

Three fixes from the demo-polish-2 briefing (the field-test items polish-1's
"real-twin" verdicts missed — all three were the same class of miss:
verifying a component/code path instead of the RUNTIME state that feeds it).

## Fix 1 — Toast position: verified parity + pins (production deploy lag is the real gap)

**Investigation result: the demo toast already matches the real app's CURRENT
code.** The demo and the real SPA render through the one shared
`components/toast.gleam` (`fixed top-20 right-4 z-[2147483001]`, moved there
by #615 so the stack never sits behind the bottom-anchored consent banner).
Runtime verification against the live deployments:

| Deployment | Toast classes in the served bundle | Notes |
|---|---|---|
| Production (`righttenantry.ie`) | `fixed bottom-4 right-4 z-50` | **stale pre-#615 build** — main hasn't merged from staging since Aug 10 (36 commits behind) |
| Staging (Cloud Run) | `fixed top-20 right-4 z-[2147483001]` | current code |
| Local demo (develop, this branch) | `fixed top-20 right-4 z-[2147483001]` | measured in-browser: top 80px, right 16px, fixed, z-index 2147483001 |

The user's "real app toasts appear elsewhere" = production's stale build.
Matching it (bottom-right z-50) would regress the #615 guarantee the briefing
explicitly keeps (toasts hidden behind the consent banner on narrow
viewports — the exact bug #615 fixed). **The user-visible mismatch resolves
when production receives the pending staging→main deploy** — no demo code
change can or should chase a stale deployment.

Pins (both directions): new `demo_toast_renders_shared_position_and_banner_survival_test`
renders the full demo view path with a toast and asserts the container
(position + z-index above the consent banner + not the old bottom-right
stack); the existing `toast_container_position_clears_consent_banner_test`
keeps the shared-component pin.

## Fix 2 — Reports at real-audit depth (13–15 pages, was 9–10)

The demo PDFs were thin because `pdf_prebake` fed the REAL Typst pipeline
thin `extras` data — the template already renders Analyst's Brief, Category
Notes, Recommendations, Scoring priority; the payloads simply didn't carry
them. New `server/src/demo/pdf_report_data.gleam` gives every one of the 8
applicants the same sections at the same depth as the 18–19 page staging
exemplars:

- **Analyst's Brief** (`detailed_insight`, ~1,200–1,600 chars each) — the
  long-form read in the exemplar voice.
- **Category Notes** — all six canonical categories per applicant, each with
  rationale + confidence bucket + evidence items (`structured` key:value
  excerpts render with the bolded key, mirroring the real pipeline's shape).
- **Recommended Next Steps** — 3–5 prioritized actions each (the exec-summary
  "N more actions listed" now renders; strong applicants like Aoife carry
  realistic lighter items, as the 83-score exemplar does).
- **Concerns & Strengths** — enriched flags/positives (Aoife: 0 → 3 concerns
  + 6 strengths; weak applicants 5 concerns). A flawless report reads as
  fake as a scanty one.
- **Verification Methodology** — every report now carries the
  credit-check-out-of-scope + RTB + employer-phone "What we didn't do" list
  and the Scoring priority block (`category_weights`).
- **Application on File** — fixed phone + time-in-role fields (were
  "Not provided" while the client fixtures carry them), Declan's DM Plumbing
  self-employed income now listed (was missing), and Aoife's co-applicant
  income no longer double-counted as an additional income source.

Screen↔PDF consistency: the on-screen app-detail analyses (`demo_store`)
now carry the same flags/positives arrays as the PDFs.

Pins: `server/test/demo/pdf_report_data_test.gleam` asserts every applicant's
extras carry every section with substance (brief > 1,200 chars, all 6 notes
with rationale/confidence/evidence, ≥3 valid-priority recommendations,
non-empty weights, credit-check note present, documents count matches).

## Fix 3 — Compare Top 3: the real gate was never satisfied (polish-1's pin was vacuous)

The shared leaderboard renders the button only when
`analysed_applications >= 3` **AND** `top_three_ids(entries) >= 3` — and
`top_three_ids` reads `score_based_rank` for ranks {1,2,3}. The demo store
set `score_based_rank` to the applicant's overall **score** (86, 78, 74…),
so no entry ever ranked ≤ 3 and the button never rendered. Polish-1's pin
asserted `overall_score != None` — a field the gate never reads.

Fix: `demo_store.leaderboard` now assigns real competition ranks — a port of
the server's `competition_ranks` (ties share a rank, next distinct score
jumps by tie count) over the same ordering as the real SQL
(`overall_score DESC NULLS LAST, created_at ASC, id ASC`). This also fixes
the leaderboard rank labels (the demo was showing scores as ranks) and the
top-row highlight (`rank == 1`).

Pins: `demo_compare_top3_ranks_feed_the_real_gate_test` asserts ranks 1..8
for v-maples and that `top_three_ids` returns 3; the render proof
`demo_vacancy_detail_renders_compare_top3_button_test` renders the demo
vacancy detail through `client.view` and asserts the button is on the page.
In-browser verified: button renders → click → `/vacancies/v-maples/compare`
opens with Aoife/Conor/Marta (86/78/74, the true top 3).

## Decisions & rationale

- **No toast position change** — the demo is already at parity with the real
  app's current code; production staleness is the mismatch. Regressing to
  bottom-right would break the #615 banner guarantee (a defended invariant).
  The deploy lag is flagged here and in the ledger so it reaches the human.
- **Demo data enriched, template untouched** — same real Typst pipeline, so
  layout cannot drift between demo and real reports; the fix lives entirely
  in the per-applicant payloads.
- **`gleam_json` 3.x `Json` is opaque** — the pin test decodes extras via
  `decode.field` chains rather than pattern-matching constructors.
- **The demo store's competition-rank port mirrors the server exactly**
  (`application_list_handler.competition_ranks`), so the demo's rank labels,
  movement semantics and Compare-top-3 gate behave identically to the real
  app.

## Files changed

- `server/src/demo/pdf_report_data.gleam` (new) — per-applicant rich extras
- `server/src/demo/pdf_prebake.gleam` — wire new extras; phones/tenure;
  income-source fixes; payload flags/positives enrichment
- `client/src/demo/demo_store.gleam` — competition ranks for the leaderboard;
  on-screen analyses flags/positives synced to the PDFs
- `client/test/demo/demo_flow_test.gleam` — 3 new pins (toast parity,
  compare-top-3 gate + render)
- `server/test/demo/pdf_report_data_test.gleam` (new) — report-section pins
- `server/priv/static/demo/report-*.pdf` — 8 re-baked PDFs (13–15 pages each)

## Verification

- `make format && make test && make build` green: shared 119, client 650,
  server 1528 (549 integration skipped)
- `scripts/lint_demo_network.py` clean (demo no-network structural guard)
- In-browser (local `make dev`): toast geometry measured at runtime
  (top 80 / right 16 / z 2147483001, consent banner unobstructed); Compare
  Top 3 button renders and opens the comparison with the top-3; report
  download serves the new 15-page PDF; app-detail flags match the PDFs

