# LENS: tests (source tag: `tests`) — Perkins r1 refcheck rc4-1

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Test coverage analysis via traceability. For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity: blocker = P0 gap (critical path, happy + core error) OR P1 <80%; warning = P1 gap at 80–89% OR P2 gap; note = P3 gap.

Behaviour changes in this diff to trace:
1. **§4.2 strip at the SQL boundary** — `list_reference_calls_for_detail.sql` `#-` + `jsonb_typeof` guards. Is there an integration test seeding a row with ALL internal markers (form_token, objection_detail.payload_ref, raw IP/UA) and asserting absence on the wire — INCLUDING the escaped wire form (`\"referee_ip\"` as backslash-quote sequence, which is how inner keys of a JSON-string field actually serialize)? Is the negative control real (a test that would go RED if the strip were disabled — e.g. asserting a marker the payload DOES carry, proving the search path is live)? Is the corrupt-row test present (scalar result → 200 + rows render)?
2. **Hooks §8.2** — full matrix across every status incl. skipped, unknown-enum-value agreement test (hooks == wire render).
3. **display_disclaimer §9.5** — written-with-verification → canon copy verbatim; minimal terminal (verification null) → None; no result → None; malformed → None.
4. **Encoder whitelist** — `encode_reference_call` serializes only §8.1 public keys; pre-terminal nullables → null (not '').
5. **Application-level** — `attestation_on_file` true/false integration tests; empty `reference_calls: []` for untriggered apps; existing detail contract preserved.
6. **Codec round-trips (AR21)** — shared tests: detail entry round-trip (all fields), terminal round-trip, attempt round-trip, hooks round-trip, snake_case wire-key check. Also: does the APPLICATION_DETAIL codec test exercise a NON-EMPTY reference_calls + attestation_on_file:true round-trip, or only the empty/false defaults? (Check `shared/test/shared_test.gleam` — if only defaults, that's a PARTIAL for the ApplicationDetail-level codec.)
7. **The attempt-log writer/reader shape agreement** — is there a test proving the sweep's written attempt entries decode through `attempt_decoder`? (If the writer is out of diff scope, note the trace gap.)
8. **`verify_payload_has_no_internal_fields`** — unit tests for the guard itself (both escaped + unescaped markers → False).

Also:
- New endpoint surface without matching coverage? (The handler change is additive to an existing endpoint — integration coverage exists?)
- Auth/authz negative tests for the new read paths?
- Test level mix (unit/integration): the strip is integration-tested (DB); hooks/disclaimer unit-tested — appropriate?

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL", category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80%; CONCERNS: P0 100%, P1 80–89%, overall ≥80%; FAIL: P0 <100% or P1 <80% or overall <80%.

Run the actual test suites if feasible (worktree: `make test-shared`; `make test-server` — integration tests need Docker, skip if unavailable) to verify the suite is green. Report what you actually observe.
