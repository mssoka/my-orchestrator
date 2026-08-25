## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-demo-polish-2 · **Reviewed sha:** `3f7e09f` · **Reviewers:** 7/7 completed
**Verification:** 18/21 reviewer findings confirmed against the code — 3 discarded as false-positive
**Local ground truth (CI billing-blocked):** client 650 ✓ · server 1528 ✓ (549 int. skipped) · shared 119 ✓ · no-network lint clean ✓ · PDFs 13–15pp with full section skeleton ✓ · competition-ranks port byte-identical to server ✓

**Fix audit (runtime bar):**
- **Fix 1 (toast)** — VERIFIED. Shared container `fixed top-20 right-4 z-[2147483001]` (`components/toast.gleam:34`), one step above the bottom-anchored consent banner (`consent.js:393`, z 2147483000). Demo-path pin renders `client.view` and asserts the classes **and** the absence of the pre-#615 bottom-right stack; the shared-component pin holds too. The "production is stale" analysis is accepted — chasing a 36-commits-behind prod build would regress #615.
- **Fix 2 (report depth)** — VERIFIED, with one blocker below. 8 re-baked PDFs at 13–15pp carrying the full exemplar skeleton (At a glance, Top concerns/strengths, Recommended next steps w/ "N more actions", Score Dashboard, Category Notes ×6, methodology, credit-check note, GDPR footer), enriched with genuine concerns; server pin asserts substance (brief >1,200 chars, 6 notes w/ rationale+confidence+evidence, ≥3 recs, weights, docs count).
- **Fix 3 (Compare Top 3)** — VERIFIED. The real gate (`leaderboard_view.gleam:140-141` + `top_three_ids` reading `score_based_rank` {1,2,3}) is now satisfied by real competition ranks; pin asserts ranks `Some(1)..Some(8)` + `top_three_ids == 3`; render proof puts `compare-top-3-btn` on the page through `client.view`; `demo_store.comparison` serves the top-3 with demo data. The port of `competition_ranks` is byte-identical to the server's.

**No-network pillar (the hard blocker class):** lint clean; diff adds no demo network surface.

### Blockers (1)

**1. Five of eight demo PDFs say the applicant "did not provide a personal statement" — while the demo app shows one, and three of those PDFs quote it** · `server/src/demo/pdf_prebake.gleam:250` (`simple_row` has no `personal_statement` param → `base_row` default `None`) · sources: codebase

`pdftotext` on report-a-{conor,marta,sara,tom,liam}.pdf: "The applicant did not provide a personal statement." Yet every one of those applicants' client fixtures carries a statement that renders on-screen in the demo app detail (e.g. Sara: "Junior developer at Kite Software, one year in, renting in Clontarf for two years."). Worse: Tom/Marta/Liam's own PDFs quote the statement verbatim as HIGH-confidence "Personal statement" evidence in Category Notes, and Sara's Recommended Next Steps says **"Request a personal statement"** for one she gave. Screen↔PDF parity is this round's core bar — this is exactly the fake-feeling inconsistency the round was funded to remove, visible in a sales demo. Fix: thread the five fixture statements through `simple_row` and re-bake.

### Warnings (2)

**2. Screen↔PDF flags/positives sync unpinned** — the PR's claimed deliverable is hand-maintained in two places; reverting the enrichment to `"[]"` fails no test. The personal-statement drift (blocker 1) is this failure mode already shipped. · sources: tests, architecture

**3. Liam's report contradicts its own document count** — "One document on file — payslips — with the landlord reference as the only other attachment", but `documents_for("a-liam")` is payslips alone and the same note's evidence says "1 of 5 categories". The landlord reference is a form entry, not an attachment. · sources: blind, codebase

### Notes (8)

4. Client `competition_ranks` port unpinned for ties/None-tail — server side has full tie/tail/offset tests and the port is byte-identical, but a future divergence of the copy would pass the client suite. (blind, architecture, tests)
5. Banner-survival pin is one-sided — toast z literal asserted; the consent banner's own `z-index:2147483000` + bottom anchor (`consent.js:393`) asserted nowhere. (edge, tests)
6. `docs_processed` pin is param-echo — the real wiring matches (verified), but nothing pins server `documents_for` against the client fixtures' document lists. (edge, tests)
7. `extras_for` fallback silently bakes a thin report for any unlisted id — a future 9th applicant would ship a 3-page stub with no red test. (edge)
8. `pub` widenings with no external callers: `pdf_prebake.payloads`, `demo_store.competition_ranks`. (blind, architecture, codebase)
9. Compare Top 3 click-through unpinned — render proof covers the button; no test dispatches `UserClickedCompareTop3` anywhere. (tests)
10. Snapshot-row fixes unpinned (phone, tenure, Declan's DM Plumbing income source, Aoife/Marta income-source removals) — reverting to `None` fails nothing. (tests)
11. Committed PDFs have no freshness pin against prebake output — regen is manual; the next payload edit can ship stale PDFs (a sha256 manifest from the bake would close it). (tests)

### Reviewer agreement
Blocker 1 (codebase, confirmed mechanically via pdftotext + fixtures) · Warnings 2–3 and Notes 4–8 each independently reported by 2–3 lenses.

**Verdict:** NEEDS CHANGES — fixes 1 and 3 land clean and pinned; fix 2's reports are deep but five of them contradict the demo app (and three contradict themselves) on the personal statement. Small fix, re-bake, push.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
