## 🤖 Perkins automated review — round 2

**Job:** righttenantry-demo-pdf-watermark · **Reviewed sha:** `e9537cd` · **Reviewers:** 7/7 completed
**Verification:** 17/18 findings confirmed against the code — 1 discarded as false-positive

### Fix audit (r1 findings)

| r1 | Finding | Status |
|----|---------|--------|
| B1 | Handler watermark flag unasserted at runtime | **FIXED — bite verified.** New integration pin `pdf_real_mode_route_serves_unwatermarked_report_test` asserts served body == `watermark: False` render AND != `watermark: True` render. Perkins mutation: flipping `ai_report_handler.gleam:295` to `True` fails the test on the PDF body; clean run passes. |
| B2 | Advisory test gate: FAIL | **FIXED.** Gate flips to PASS — both r1 wiring gaps now FULL. |
| W1 | Cover renders two stacked watermark layers | **FIXED — pixel verified.** Explicit cover `place` deleted; only `background: demo-watermark` remains (both page styles). Perkins pixel proof vs the r1-committed PDFs: interiors pixel-identical, cover stamp red-lift ratio old/new 1.90 (two 25% layers → one), one layer remains. |
| W2 | Committed demo PDFs unpinned | **FIXED — bite verified.** `committed_demo_pdfs_match_fresh_rebake_test` pins all 8 committed PDFs against fresh `watermark: True` renders. Perkins mutation: +1 byte on `report-a-aoife.pdf` fails exactly that test. |
| 7 notes | carry-forward | Each either fixed or carried below — see Notes. |

Local suite at `e9537cd`: **1534 passed / 0 failed / 550 skipped** (typst on PATH).

### Blockers (0)

None.

### Warnings (3)

1. **Typst test helpers now copied in THREE test files** — the B1 fix added a third copy of `skip_if_no_typst`/`typst_available`/`priv_dir`/`normalize_metadata` instead of extracting to `test/test_helpers.gleam` (r1 note predicted exactly this). A skip-policy change now touches three files. *[architecture, blind, acceptance, codebase, tests]* — `server/test/integration/ai_integration_test.gleam:1314-1318`
2. **Stale contradictory comment in `audit_report_test.gleam:343-348`** — still documents the removed cover "explicit place" layer, contradicting the template's "Do NOT re-add it" fix and documenting a false mechanism. *[blind, acceptance, architecture, codebase]*
3. **Unused `import gleam/bit_array`** in `ai_integration_test.gleam:16` (delta-introduced; compiler warning, zero references). *[blind]*

### Notes (8)

1. Per-page watermark presence remains construction-guaranteed, not asserted per-page (whole-document inequality only). *[blind, tests — carried since r1]*
2. `watermark --input` pair appended after both positionals (typst parser reliance). *[edge — carried since r1]*
3. The new B1 integration pin silently skips on missing typst in CI, unlike the unit pins that panic — guard asymmetry, mitigated by the unit pins failing loudly. *[edge — new]*
4. No-op `let _ = application_id` in `payload_for` error branch. *[codebase — carried since r1]*
5. Test-only `normalize_metadata/1` exported from the production FFI; its consumer-list comment rotted. *[architecture — carried since r1]*
6. Advisory test gate: PASS (informational). *[tests]*
7. Golden pin deterministic only per typst version — accepted, documented trade. *[carried since r1]*
8. `...two_distinct_paths_test` name slightly overstates (two payloads, one path) — optional rename. *[carried since r1]*

### Reviewer agreement

Five lenses (architecture, blind, acceptance, codebase, tests) independently confirmed the helper-duplication widening; four confirmed the stale test comment — both highest-confidence findings of the round. One blind claim rejected on verification (RT_DEMO_PRIV_DIR "not read" — the reader exists at base `pdf_prebake.gleam:740`).

**Verdict:** READY TO MERGE

Both r1 blockers are fixed with mutation-verified pins, both warnings fixed (W1 pixel-proven), no new blockers introduced by the delta. The three warnings are cleanup-grade (comment, dead import, deferred extraction) — address them in a follow-up or fold into the next touch of these files.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
