## 🤖 Perkins automated review — round 1 of 3

- **Job:** righttenantry-demo-polish-1
- **Reviewed sha:** `34a2f3b5aa8f5367efb02955d2a71312eb1eeb5d`
- **Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests)
- **Verification:** 17/18 reviewer findings survived code re-verification — 1 discarded as false-positive (see Notes). Local ground truth re-run: client suite **626 passed, no failures**; demo no-network lint clean + **8/8 bite-tests pass**.

### Fix-audit (the 5+1)

1. **Toast placement** — verified-parity pin intact (shared `components/toast.gleam`, top-20 right-4); #615 consent-banner guarantee untouched. ✅
2. **Remind + Follow-up state mutation** — mutates the demo store rows (reminded → followed-up). ⚠️ W1 below: phantom `#(0,1)` for unknown email.
3. **Compare Top 3** — verified-parity, pins present. ✅
4. **Report detail** — enriched bake present (`report-a-grainne.pdf` + 7 others in `server/priv/static/demo/`). ⚠️ W3: zero automated coverage of the enrichment.
5. **Logo/wordmark → landing** — implemented in `shell.gleam:82-85` and pinned. ✅
6. **a-grace purge** — no live id references; `report-a-grainne.pdf` baked. ⚠️ W2: the literal "zero `grace` grep hits" AC fails — 4 comment/docstring mentions remain.

### BLOCKERS (0)

None.

### WARNINGS (3)

1. **`remind_applicant` reports `#(0,1)` "follow-up sent" for an email not in the pool** [blind, architecture, codebase, tests] — `client/src/demo/demo_store.gleam:1441-1467`. `sent_reminded` is `False` for both already-reminded rows *and* unknown emails; the latter yields a phantom follow-up toast with no mutation, and the documented `0,0` branch is unreachable. Latent from the UI (buttons only render for pool rows), but it contradicts the mirrored `remind_applicant_toast_copy` semantics. Fix: single `list.find` — `Ok(a)` → `#(1,0)`/`#(0,1)`; `Error` → `#(store, #(0,0))`.
2. **Fix-6 literal AC unmet: `grace` grep hits remain in demo code** [acceptance, codebase] — `pdf_prebake.gleam:618,724`, `demo_flow_test.gleam:877-878`. All 4 hits are comments/docstrings; functional purge is complete. Reword the comments (e.g. "Purged legacy id -> a-grainne.") so `grep -ri grace` over demo code returns zero, or explicitly relax the AC.
3. **Fix-4 enrichment has zero automated coverage** [tests] — `server/src/demo/pdf_prebake.gleam:585+`. Nothing in `server/test/` touches `pdf_prebake`; the only report test pins id→filename. The per-applicant verification summary / income sources / document lists baked into the 8 PDFs can silently regress, and fixture truth is now triplicated between `pdf_prebake` and client `demo_store` with no pin. Add a server unit test on the enriched payload + an asset-existence check.

### NOTES (6)

- `awaiting/2` doc comment promises a seed fallback; the code returns `[]` on a missing key [blind, architecture, codebase] — comment-only fix.
- Test helper `result_map_custom` re-implements `gleam/result.map` [blind, architecture] — delete and use the stdlib.
- After a demo reminder, vacancy-detail header counts stay stale until the next detail load [edge] — verified, but the **real flow shares the identical handler shape**, so this is parity, not a demo regression. Optional: refetch detail too, or pin the behaviour.
- The a-grace pin asserts presence of `a-grainne` but never *absence* of `a-grace` despite its doc comment [tests] — add negative assertions.
- `remind_applicant` pins only the `#(1,0)` stage; the follow-up flip and unknown-email paths are untested [tests].
- Advisory test gate: **PASS** [tests] — P0 (no-network lint + bite-tests) 100%, fixes 1/2/3/5/6 pinned; fix-4 gap is the one open item.

### Reviewer agreement

- W1 (phantom follow-up in `remind_applicant`) — flagged independently by 4 lenses; highest-confidence finding in this report.
- W2 (grace comment residue) — flagged by 2 lenses.
- The two comment/doc-accuracy notes (awaiting fallback, result_map_custom) each drew 2–3 lenses.

### Rejected as false-positive (1)

- "Wordmark test is vacuous — any `href="/"` in the page satisfies it" [blind]: in the demo view (shell + dashboard + banner) the **only** `href="/"` is the wordmark itself (`auth_layout`'s is not rendered on `routes.Demo`). The pin currently bites — if the wordmark regressed to `/dashboard`, the assertion would fail.

### Verdict

**READY TO MERGE** — 0 blockers. The no-network pillar and the r1–r5 gauntlet classes hold (lint + bite-tests re-run green this round). The 3 warnings are worth a quick follow-up pass but none gates the merge.

_Address findings and push — I re-review automatically on the new sha._
