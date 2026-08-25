## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc1-1-grapheme-fix
**Reviewed sha:** `c252019`
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 12/13 findings confirmed against the worktree — 1 rejected (blind's "cannot compile" blocker: `string.to_utf_codepoints`/`from_utf_codepoints` in gleam_stdlib 0.70.0 return `List`/`String`, not `Result`; the server compiled and 1484 unit tests passed at this exact sha).
**Suites at sha:** unit 1484 passed / 501 skipped, format clean, no `let assert` in src. New integration pins pass in isolation (`multi_codepoint_headers_within_check_bounds_test`, `apply_submission_multi_codepoint_headers_bounded_test`). Full integration re-run: 499 passed + 2 pre-existing parallel-execution flakes in `ai_integration_test` (seed-dependent truncate collisions; module untouched by this PR; 62/62 green in isolation) — not a regression.

### Blockers (0)

### Warnings (0)

### Notes (10)

1. **Stale PTA CHECK citation (3-lens agreement: acceptance + blind + codebase)** — `consent_integration_test.gleam:327-328` (new comment) and the spec file still cite `payment_terms_acceptance` as a live 64/512 CHECK site; `20260512182900_constraint_parity_with_staging.sql` dropped those CHECKs and this PR's own `request_helpers.gleam:15-17` doc says so. Doc-only; zero functional impact (test targets `cookie_consent_log`, which does carry the CHECK). *Fix: reword the comment to cite only `cookie_consent_log` + `application.submitted_*`.*
2. **`client_ip` invalid-UTF-8 crash before the decoder (security)** — `string.trim` runs before `slice_codepoint_bounded`, and Erlang `string:trim` raises `badarg` on invalid UTF-8 (empirically verified) — the doc's "truncation, not a crash" guarantee holds only for the UA path. Pre-existing (old code identical), not a regression.
3. **NUL byte survives slicing → Postgres still rejects (edge)** — NUL is valid UTF-8, so it passes `to_utf_codepoints`; Postgres rejects `0x00` in text (verified: `invalid byte sequence for encoding "UTF8": 0x00`). Same 500 class as the fix eliminates, via NUL instead of length. Pre-existing, raw-socket clients only, out of scope.
4. **"Never displayed or parsed" doc claim omits DSAR (edge)** — `dsar_handler.gleam:378-379` serializes `submitted_ip_text`/`submitted_user_agent` into the applicant's export; a mid-grapheme cut would surface as a dangling ZWJ/lone emoji member there. Cosmetic; JSON stays valid.
5. **XFF unit-test comment 140 vs 150 (blind)** — `request_helpers_test.gleam:67` describes the emoji portion (140 codepoints) while the assert counts 150 including the `", 10.0.0.1"` suffix. Comment nit.
6. **Header comment names only two callers (blind)** — `request_helpers.gleam:4-8` ("both store the values") omits `application_handler`; historically accurate as origin-story, incomplete as consumer map.
7. **GDPR test comment misstates 3584 (blind)** — `gdpr_integration_test.gleam:2783-2785` says grapheme slicing would retain "512 graphemes = 3584"; for the pinned 100-grapheme input it would retain 700 codepoints. Comment nit; pin itself correct.
8. **Payment caller lacks stored-value pin (tests, P3)** — no test asserts `payment_terms_acceptance.ip_text`/`user_agent`; PTA's CHECKs are dropped so there's no 500 risk — the pin would only catch a caller-side revert.
9. **XFF no-comma branch lacks multi-codepoint pin (tests, P3)** — the `split_once` Error path is only covered by ASCII tests that can't distinguish codepoint from grapheme slicing.
10. **Advisory test gate: PASS (tests)** — all 8 unit + 2 integration behaviours traced FULL; negative control verified real for all 4 new pins (revert to `string.slice` → 2 unit + 2 integration red, `/apply` 500).

### Load-bearing invariant check (Perkins verification)

- **Grapheme-boundary slicing:** fix is `to_utf_codepoints |> list.take(max) |> from_utf_codepoints` — codepoint-boundary only, never splits a multi-byte char; decoder pattern-match drops invalid bytes without crashing. ✅
- **Exact-boundary semantics:** 512 = 73×7+1 → 73 full family-emoji + lone 👨 (no dangling ZWJ at the cut); 64 = 9×7+1 → same shape; ASCII byte-identical (1 cp/grapheme); absent → `''`; short passthrough. All pinned by tests. ✅
- **All 3 callers + DB CHECKs:** consent (196-197), payment (157-158), application (206-207) all route through the helpers; no bypass. Live CHECKs: `cookie_consent_log` (64/512) + `application.submitted_*` (64/512) — exactly the bounds the fix targets. ✅
- **Negative control real:** unit tests assert codepoint lengths (512/64) that old grapheme slicing fails (700/140 retained); integration tests assert stored lengths + 200/204 that old behavior fails via CHECK violation. ✅
- **No regression:** suites green at sha; diff touches no rc4-3/rc4-4 files; no scope drift (helper + 3 callers + tests only). ✅

**Verdict:** READY TO MERGE

Notes 1–7 are doc-comment nits and 8–9 are optional P3 coverage pins — none block. Address findings and push (fold into this PR or a follow-up); a fresh round will re-verify. (Reviewed `c252019`; head is unchanged.)
