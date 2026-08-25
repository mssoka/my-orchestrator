## 🤖 Perkins automated review — round 3 of 3

**Job:** righttenantry-demo-polish-2 · **Round:** 3 of 3 (loop-until-APPROVED)
**Reviewed sha:** `fa692d3829d6550261c039e3f6f17e1f850fddf5`
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests — kimi-coding/k3, thinking max, no failures, no retries)
**Verification:** 15/20 reviewer findings survived code re-verification — 3 discarded as false-positive, 2 severity-recalibrated and folded; 9 consolidated findings below. Local ground truth: shared 119 / client 650 / server 1530 passed, 0 failures; two revert-style bite checks executed (details below).

### Fix audit (vs round 2)

- **B2 (r2 blocker) — FIXED and BITES.** `server/test/demo/pdf_prebake_test.gleam` (new, 290 lines) pins all 8 payloads' `personal_statement` = `Some(<fixture text>)`; all 8 pin statements verified **verbatim** against `client/src/demo/demo_fixtures.gleam`; W1's flags/positives folded into the same pin. Revert-style: dropping the `simple_row` statement threading → `every_payload_carries_the_client_fixture_statement_test` **FAILS**; blanking `a-aoife` flags to `[]` → `every_payload_flags_and_positives_match_canonical_test` **FAILS**. Worktree restored clean after both.
- **W1 — FIXED payload-side / narrowed.** Screen side (`demo_store.analysis_for`) has zero coverage; label sets mechanically verified in exact sync at this sha (60/60, zero divergence). Residual → **W-A** below.
- **W2 — FIXED.** Liam prose now "One document on file — payslips. The landlord reference is a contact entry rather than an uploaded letter…" — verified in source and in the re-baked PDF (pdftotext); "only other attachment" gone.
- **W3 — FIXED.** Conor's evidence source label now "Reason for moving" — verified in source and rendered PDF.
- **Carried, spot-verified holding:** B1 statements (0 missing-statement claims across all 8 PDFs) · toast literal `fixed top-20 right-4 z-[2147483001]` vs banner `2147483000` · 13–15pp reports · substance pins (>1200 / >80) · Compare Top 3 real gate **plus a new render-proof pin** (`compare-top-3-btn` through the real view path) · no-network lint clean · gauntlet classes present · committed PDFs **content-fresh** (full prebake regen → 0 lines of pdftotext diff).

### BLOCKERS (0)

None.

### WARNINGS (1)

- **W-A** — Screen↔PDF parity pin is payload-side only, and its docstrings overclaim · `pdf_prebake_test.gleam:269-271` + header `:5-14` · [blind, edge, acceptance, architecture, tests]. The docstring says "reverting either copy to `[]` must fail a test" and the header claims "fail when EITHER side drifts" — but reverting the `demo_store.analysis_for` copy, or editing client fixture statements, fails **no** test (`client/test/demo` has zero flags/positives assertions). The B1 failure mode (one side edited, other stale, suites green) is now caught on the payload side only. `category_scores` is a further unpinned hand-synced field (render-verified in sync; Marta's null-vs-omitted renders identically). **Fix:** correct both docstrings to claim only what bites; add a client-side pin that `demo_store.analysis_for` flags/positives are non-empty and label-match the canonical lists (or hoist canonicals to `shared/`).

### NOTES (8)

1. **N1** — `competition_ranks` ported verbatim into `demo_store` (vs `application_list_handler.gleam:231`); tie/None-tail branches unexercised · [blind, architecture, codebase, tests] · *narrowed since r2*: the new ranks pin asserts `Some(1..8)`, and demo data has no ties, so output drift fails a test and tie-branch drift has no demo impact. Optional: hoist to `shared/`.
2. **N2** — toast test named "banner survival" never asserts the banner renders or its z-index (toast side only) · [blind]. The #615 guarantee itself is verified intact.
3. **N3** — Liam's insight is 1208 chars against the >1200 floor — 8 chars of headroom; the next W2-style rephrase breaks an unrelated pin. Suggest floor ~1100 or per-applicant minima.
4. **N4** — depth pin iterates a hardcoded 8-id list instead of `pdf_prebake.payloads()` · mitigated: the parity test's `length == 8` assertion trips first, so a 9th applicant can't ship silently.
5. **N5** — snapshot fixes (phone, tenure, income_sources) still unpinned (carry since r1; verified correct at this sha).
6. **N6** — committed PDFs still lack an automated freshness pin (carry since r1); freshness manually verified this round via full regen + content diff = 0.
7. **N7** — Aoife's real-format mobile `087 123 4567` still baked into the public demo PDF (carry since r2; security lens returned empty this round — orchestrator re-verified directly).
8. **N8** — demo evidence labels bypass `evidence_humanize`'s controlled table — by design (display-form labels); cosmetic-drift risk only.

### Reviewer agreement

- **W-A** independently reported by 5 of 7 lenses (blind, edge, acceptance, architecture, tests) — highest-confidence finding in the report.
- **N1** reported by 4 of 7 lenses (blind, architecture, codebase, tests).

### Verdict

**READY TO MERGE** — 0 blockers. The r2 blocker fix landed exactly in the contracted shape and bites revert-style; W1–W3 are fixed and verified in the re-baked artifacts; every carried gauntlet class holds. The one surviving warning is the narrowed one-sided parity pin with overstated docstrings — fix-forward material, not merge-blocking.

_Address findings and push — I re-review automatically on the new sha._
