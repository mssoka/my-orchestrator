## 🤖 Perkins automated review — round 1
**Job:** righttenantry-demo-pdf-watermark · **Reviewed sha:** `798e9d0` · **Reviewers:** 7/7 completed

> ℹ️ Head moved mid-review: reviewed `798e9d0`, head now `e1df69a` ("fix(test): normalize xref offsets + startxref in PDF golden comparison") — a fresh round will follow on the new sha.
**Verification:** 16/18 findings confirmed against the code — 2 discarded as false-positive

Mechanical verification run by Perkins directly (I don't take claims on faith): `make test-server` green (1533/0/549, typst on PATH); **mutation runs bite exactly as claimed** — disabling the watermark layer fails precisely the 2 presence tests (1531/2), corrupting the golden fails precisely the identity test (1532/1); **re-baked all 8 demo PDFs** via `RT_DEMO_PRIV_DIR` into a throwaway — normalized byte-equal to every committed file; format-check clean; single `typst_compile` call site confirmed (the central seam is real); demo download intercept confirmed client-side. Visual claims were verified mechanically only (byte/pixel-diff) — aesthetic adjudication is deferred to the k3 re-check per the standing vision caveat.

### Blockers (2)
1. **[tests] Real-mode runtime wiring unasserted** — `server/src/ai/ai_report_handler.gleam:283`. The only test touching `handle_get_pdf` (`pdf_download_writes_audit_log_test`) asserts `status == 200` + audit row, never the PDF body; the golden test bypasses the handler. A one-token flip of `watermark: False` → `True` DEMO-stamps every real landlord report with a fully green suite. Spec hard rule 3's runtime enforcement point has no guard — and no existing test would fail on the flip (verified by reading every `handle_get_pdf` caller). *Fix: in the integration test, compare the handler's response body (via `normalize_metadata`) against a fresh `generate(watermark: False)` render — ~10 lines.*
2. **[tests] Advisory test gate: FAIL** — P0 100% (seam pins, mutation-verified), P1 ~25% (handler wiring NONE, served demo bytes NONE/PARTIAL), overall ~65%. Aggregate of blocker 1 + warning 1; fixing both flips the gate to PASS.

### Warnings (2)
1. **[blind] Cover page renders TWO stacked watermark layers (≈44% combined alpha vs 25% on interiors)** — `audit_report.typ:211,258`. Proven mechanically: cover-only renders with each layer removed differ in bytes **and** in rendered pixels — both the page `background:` and the explicit `#demo-watermark` visibly render on the cover. The cover block has no fill (transparent), so the comment's rationale ("the navy block paints over the background") is factually wrong. Not a spec violation (watermark present, diagonal, readable-through on every page) — but unintended, inconsistent cover-vs-interior, and the comment documents a false mechanism. *Fix: delete the explicit trailing `#demo-watermark` (background already delivers it), correct the comment, re-bake, and flag cover-vs-interior consistency for the k3 visual re-check.*
2. **[tests] Served demo bytes unpinned** — no test reads `priv/static/demo/report-*.pdf` (grep: comment hit only); tests re-render via `generate`. A stale or regressed re-bake ships unwatermarked demo PDFs with a green suite. Correct today (Perkins re-bake proved byte-equality at this sha), unguarded tomorrow. *Fix: pin 1–2 committed demo PDFs against a fresh `generate(watermark: True)` render.*

### Notes (7)
1. **[blind·architecture·acceptance·tests — 4-lens agreement] Per-page presence (rule 3 "every page") rests on template construction, not assertion** — both presence tests compare whole-document bytes; a page-level drop passes silently (mechanically confirmed: deleting the cover's explicit place keeps both green). Consider a per-page draw-op/page-count assertion.
2. **[architecture·codebase] Test helpers duplicated** — `skip_if_no_typst`/`typst_available`/`priv_dir`/`normalize_metadata` external copied across both test files; `server/test/test_helpers.gleam` already exists as the shared home. Extract (panic message as argument).
3. **[blind] `normalize_metadata/1` is a test-only export on the production FFI module** — zero production callers. Fold into the shared test-support move.
4. **[blind] Golden pin is deterministic per typst version** — a CI typst bump fails it (documented re-bless policy; acceptable, or pin/extend the normalizer if it bites).
5. **[acceptance] "Two distinct PDF paths" AC delivered as two payloads through the demo's single (only) PDF path** — documented deviation, intent satisfied; optional test rename to match reality.
6. **[blind] `--input watermark=true` appended after the positional output path** — works today (clap accepts interspersed); reorder for hygiene.
7. **[blind·codebase] No-op `let _ = application_id`** in `payload_for`'s error branch — delete the line.

### Reviewer agreement
Four lenses independently flagged the per-page-coverage gap (note 1) — the highest-confidence signal in this round. The two rejected findings: `RT_DEMO_PRIV_DIR` "docs/code mismatch" (the env-var reading exists at the base commit — the diff corrects a stale comment) and "DM Sans not bundled" (`dm-sans-700.ttf` is in `typst-fonts/`; the re-bake byte-match proves resolution).

**Verdict:** NEEDS CHANGES

The seam itself is well-built — one central flag, byte-identical real mode (pinned), mutation-verified tests, honest survey. The two gaps are both about *guards at the ends of the pipe* (the runtime handler flag, the served demo bytes) plus the unintended cover double-stamp. All fixes are small.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
