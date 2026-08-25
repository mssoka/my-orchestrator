## 🤖 Perkins automated review — round 2 of 3

**Job:** righttenantry-demo-polish-2 · **PR:** #632 · **Reviewed sha:** `1efcf2708c0a9dc43cc13fec5372e135f03bbca3` (fix commit for the r1 blocker)

**Reviewers:** 7/7 completed · **Verification:** 31/36 reviewer findings survived code re-verification — 5 discarded as false-positive, 1 gate-marker folded into its root cause · **Local ground truth:** client 650 ✓ · server 1528 ✓ (549 integration skipped) · shared 119 ✓ · demo no-network lint clean

**Model note (transparency):** all lens spawns on the mandated `kimi-coding/k3` 403'd — the billing-cycle usage cap re-tripped mid-round. Each lens was re-dispatched once (per retry policy) on the global default reasoning model `glm-5.3 --thinking max`. All 7 lenses completed; the verification pass is unchanged.

### Fix audit (r1 findings at this sha)

| r1 | Verdict |
|----|---------|
| **B1** statements missing from 5 PDFs | ✅ **FIXED and bites** — `simple_row` threads the five fixture statements (`pdf_prebake.gleam:280,323`); pdftotext on all five PDFs: zero "did not provide a personal statement", each renders its statement verbatim in *In the applicant's own words*; Sara's next steps no longer request one; Tom/Marta/Liam Category Notes quotes consistent. All 8 PDFs re-baked (13–15pp). |
| W1 flags/positives unpinned | ❌ still present |
| W2 Liam prose vs doc count | ❌ still present |
| N1–N8 | ❌ all still present (carried below, not re-counted) |

Carried pins spot-verified: toast literal `top-20 right-4 z-[2147483001]` vs banner `2147483000` ✓ · report substance pin (brief >1,200 / rationale >80 / evidence) ✓ · Compare Top 3 real gate `leaderboard_view.gleam:140-141` ✓ · gauntlet classes (deep-link boot, session stash) ✓

### BLOCKERS (1)

1. **The r1 blocker fix shipped with zero regression pins — re-dropping the statements fails no test** (advisory gate: **FAIL**, P0 <100%) — `server/src/demo/pdf_prebake.gleam:280,323`. Fix commit `1efcf27` touched 8 PDFs + 2 payload files and **no test file**; grep for `personal_statement`/`statement:` across `client/test/demo/` + `server/test/demo/` returns nothing. Reverting the threading re-bakes PDFs that claim a missing statement while every suite stays green. r1's W1 warned this hand-sync class had already shipped B1 once — the pin is the cheap, named-regression defense this time. *Fix: one test iterating the 8 payloads asserting `Some(<fixture statement text>)`; ideally fold W1's flags/positives into the same parity pin.*

### WARNINGS (3)

2. **W1 (carried):** screen↔PDF flags/positives sync unpinned — payload strings duplicated verbatim between `demo_store.gleam:215-216` and `pdf_prebake.gleam:337-338` with no parity test. *[acceptance, tests, architecture]*
3. **W2 (carried):** Liam prose still says "with the landlord reference as the only other attachment" (`pdf_report_data.gleam:1352`; insight `:1279` repeats it) while the same report counts 1 document — the reference is a form entry. *[acceptance, codebase]*
4. **W3 (new):** Conor's evidence item attributes the quote *"Looking for a place with my partner"* to source **"Personal statement"** (`pdf_report_data.gleam:464-468`) — that's his `reason_for_moving`; the actual statement is the nurse text. Same self-contradiction class as W2, smaller scope. *[acceptance]*

### NOTES (9)

5. **N1 (carried):** client `competition_ranks` port exercised only on distinct scores — no tie/None-tail test; remains a verbatim duplicate of the server algorithm. *[5-lens agreement: blind, acceptance, architecture, codebase, tests]*
6. **N2 (carried):** toast pin asserts the toast side only; `consent.js:393` banner z/anchor unasserted — test name says "banner survival" but never reads the banner. *[blind, acceptance, tests]*
7. **N3 (carried):** `docs_processed` pin is param-echo (feeds and asserts the same `documents_for` length). *[blind, acceptance, tests]*
8. **N4 (carried):** `fallback_parts()` thin-report arm still unreachable by any test (`pdf_report_data.gleam:139,163`). *[acceptance, tests]*
9. **N5 (carried):** `pub` widenings with no external callers (`pdf_prebake.payloads`, `demo_store.competition_ranks`). *[acceptance, tests]*
10. **N6 (carried):** Compare Top 3 click-through unpinned — `UserClickedCompareTop3` never dispatched. *[acceptance, tests]*
11. **N7 (carried):** phone/tenure/income-source snapshot fixes unpinned. *[acceptance, tests]*
12. **N8 (carried):** committed PDFs have no freshness manifest vs prebake output — stale-bake risk is B1's exact mechanism. *[acceptance, tests]*
13. **N9 (new):** Aoife's real-format mobile `087 123 4567` (pre-existing fixture value) is now baked into the public PDF — every other demo phone uses the fictional 555 triple. *[security]*

### Reviewer agreement

N1 is the only 5-lens finding. W1 (3 lenses) and W2/N2/N3 (3 lenses each) are the strongest remaining. Rejected as false-positives after re-verification: 5 (including "Aoife/Marta income sources dropped" — client and server are both declan-only and in sync; and "`checks_performed` always empty" — the Typst template intentionally never renders it).

### Verdict

**NEEDS CHANGES** — 1 blocker. The fix landed and the shipped bytes are right (all mechanical checks green), but the one named regression this job exists to fix has no test defense, and two one-line content blemishes (W2, W3) remain in the baked reports. All three are small, mechanical fixes plus a re-bake.

_Address findings and push — I re-review automatically on the new sha._
