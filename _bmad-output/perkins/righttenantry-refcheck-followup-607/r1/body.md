## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-followup-607 · **Reviewed sha:** 9552847 · **Reviewers:** 7/7 completed
**Verification:** 27/28 findings confirmed against the code — 1 discarded as false-positive

All five #607 items are implemented and the production behavior is correct: the panel consumes `hooks` everywhere (no client-side terminality list survives), the escaped markers genuinely fire (verified byte-level), the unknown-outcome rule is named and pinned on both encode sides, the mixed-format sort fixture pins, and both lints run in CI and fail on the historical shapes (sandbox-verified the RC4.3-r1 menu and an injected em-dash). The blocker below is the one place where a claimed guard layer doesn't bite.

### Blockers (1)

**[B1] Lockstep pin never reads the production `terminal_statuses` const — the claimed guard cannot bite on const drift** — `server/test/application/application_detail_handler_test.gleam:593` vs `server/src/application/application_detail_handler.gleam:1286`
The PR's own spec and the AR-RC13 amendment claim *"A lockstep unit test pins the timeline's DB-string `terminal_statuses` list to the shared fn."* The test instead hardcodes its own copy of the list; the production const (driving the timeline's terminal entries at line 1454) is private and unreferenced by any test. Editing the const fails nothing — the exact mirror-drift pattern AR-RC13 names as the bug class, shipped inside the guard meant to prevent it. The truth-table and distinguishing pins do bite; this one does not.
→ Export the const (or a `pub` accessor) from `application_detail_handler` and iterate the real list in the lockstep test in both directions, then make the arch-doc claim match what the test actually pins.

### Warnings (4)

- **W1 (security):** `verify_payload_has_no_internal_fields` has zero production call sites — item 1's marker hardening is test-only. Pre-existing wiring gap, but the PR extends this fn and its "can't leak internals" doc claim. The SQL-boundary §4.2 strip is the live defense (integration-proven), so no live leak. Wire the re-verify into the serialization path or correct the claim.
- **W2 (edge, tests):** `trigger.gleam:1153` keeps a second unpinned server-side terminality list (`is_terminal` for slot-liveness). The amendment's "terminality has ONE home" is false while it exists. Consume `shared status_from_string` + `is_terminal_status` there, or pin the list against the shared fn.
- **W3 (edge, tests, architecture):** `lint_refcheck_hooks.py` is shape-fragile: multiline list construction and non-final list position (`[RefcheckTakeOver, RefcheckSkip]`) both pass the lint (sandbox-verified exit 0); the exact RC4.3-r1 shape is caught. Match governed identifiers at word boundaries regardless of position/line; consider a CI negative-control fixture.
- **W4 (blind, architecture, codebase, tests):** `outcome_from_string` is orphaned in production (zero non-test callers; its doc claims non-wire callers that don't exist) and `outcome_from_string_optional` duplicates the 15-arm mapping while being pinned for only 2 known values. A future outcome enum addition missed in the optional fn silently encodes as null — the drift class this PR targets. Derive one fn from the other so one mapping exists, and add an exhaustive `all_outcomes()` round-trip pin.

### Notes (8)

- N1: `lint_refcheck_hooks` false-positives on a legitimate non-hook `case` nested inside a hooks gate (sandbox-verified) — a legal AR-RC13 refactor would fail CI.
- N2: `written_response_disclaimer` (em-dash) ships to landlords but sits outside the lint scope with an undocumented exemption — the string is spec-verbatim, so exempt-by-construction is right; document it or whitelist-pin it.
- N3: `lint_em_dash.py` has two false-negative paths — escaped-quote state toggle and whole-line log-call exemption (no live impact today).
- N4: Same-instant mixed-format attempts group into two cadence batches (grouping on raw `at`); the new fixture pins ordering only.
- N5: copy.gleam em-dash enforcement rests on hand-maintained test lists while the lint exempts the module wholesale.
- N6: The amendment register claims §8.2 was amended in place with the unknown-outcome rule; §8.2 has no such content (the rule lives in the shared module doc).
- N7: Substitute message-payload construction is shape-exempt from the hooks lint — its gate is code-review-only (panel tests remain as backstop).
- N8: Advisory test gate: CONCERNS (P0 100%, P1 ≈85% — the three item-5 guard holes above).

### Reviewer agreement

1. **B1 (6/7 lenses)** — blind, edge, acceptance, architecture, codebase, tests all independently hit the non-biting lockstep pin.
2. W4 (4 lenses) · 3. W3 (3 lenses) · 4. W2 (2 lenses) · 5. N3 (2 lenses) · 6. N1 (2 lenses)

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
