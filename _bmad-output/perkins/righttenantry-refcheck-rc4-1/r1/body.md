## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc4-1
**Reviewed sha:** `a7e8cee5`
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 14/15 findings confirmed — 1 rejected as unreachable; 0 unverifiable-speculative
**Spec:** Story RC4.1 (epics §line 607) + architecture §8.1/§8.2/§9.5/§4.2/AD-11/AD-2 + A4/A5/AR21 + job briefing
**Suites at the reviewed sha:** shared 106 ✅ · server unit 1476 ✅ (498 skipped) · integration 498 ✅ (incl. all 8 new `reference_detail_payload` tests) · format ✅ · build-server ✅ · client gleam build ✅

### Blockers (0)

### Warnings (2)

1. **§4.2 belt-and-braces guard checks escaped wire forms for `referee_ip`/`referee_user_agent` only — `form_token`/`payload_ref` escaped forms are unchecked** — `server/src/application/application_detail_handler.gleam:1148-1160` [`blind`, `architecture`, `security`]
   The guard's own doc claims "both forms are checked" (self-review #1), but the escaped-marker list covers only the two IP/UA keys. A corrupt/spoofed stored result containing `form_token` or `payload_ref` keys at any path would ship backslash-escaped on the wire and pass the guard clean; the negative-control test feeds those two markers only in the unescaped top-level form the encoder can never emit. The load-bearing strip (SQL never selects those columns, `#-` deletion, integration pin) is unaffected and holds — this is defense-in-depth completeness.
   *Fix:* add `\"form_token\"` / `\"payload_ref\"` escaped markers and extend the guard test with the escaped result-string forms.

2. **Unknown outcome value serialises as terminal `"unreachable"` while hooks can still say `can_record_manual: true`** — `server/src/application/application_detail_handler.gleam:1179-1184`, `shared/reference_call.gleam:215` [`blind`, `architecture`]
   `outcome_from_string`'s fallback is `OutcomeUnreachable` (pinned by `unknown_outcome_never_falls_back_to_success_test`), so in an enum expand-then-contract window an old server would render `outcome: "unreachable"` on a recordable row — the exact hooks-vs-wire divergence self-review #3 claims to prevent (status falls back inertly to `failed`; outcome does not). Impossible with today's 16-value enum; real in the expand window.
   *Fix:* map unrecognised outcome strings to `None` in `encode_reference_call` instead of round-tripping the fallback.

### Notes (8)

1. **`verify_payload_has_no_internal_fields` is test-only; the doc comment overstates a runtime re-verification** — `application_detail_handler.gleam:1148` [`blind`, `security`]
2. **SQL ELSE branch passes string-typed intermediates verbatim — the "cannot leak" comment is false for double-encoded corrupt rows** — `sql/list_reference_calls_for_detail.sql:33-49` [`edge`, `security`]; no current writer produces that shape, corrupt-row-only.
3. **`next_attempt_at` ships as `timestamptz::text` (space-separated, session-TZ-dependent) while `attempts[].at` and fixtures use ISO-T** — two datetime formats in one §8.1 entry [`blind`]; consistent with the house `::text` convention and client `format_timestamp_short` handles both — document or normalise for RC4.2.
4. **Shared `attempt_decoder` is strict (4 keys) while sweep/result parsers are tolerant — one key-less entry silently empties the whole attempts array** — `shared/reference_call.gleam:408-414` [`codebase`]; all current writers emit 4 keys.
5. **ApplicationDetail envelope codec round-trips only the new-field defaults** (`reference_calls: []`, `attestation_on_file: False`) — `shared/test/shared_test.gleam:824-825` [`tests`]
6. **Attempt-log writer/reader shape agreement is unpinned** — the wire test asserts only the `"attempts"` key [`tests`]
7. **No cross-tenant negative test for the new read paths** — all tests use the owning landlord; gated by the pre-existing landlord-scoped outer query, so no leak reachable [`tests`]
8. **Advisory test gate: PASS** [`tests`]

### Reviewer Agreement

Warnings 1–2 were each independently reported by two lenses; the guard-marker finding (W1) by three. `acceptance` returned `[]` and its AC-by-AC trace was confirmed by the lead.

### Verdict

**READY TO MERGE**

The load-bearing §4.2 strip holds end-to-end: the read never selects `form_token`/`objection_detail`/`fraud_signals` columns, deletes the raw IP/UA paths under `jsonb_typeof` guards, and the integration suite seeds a row carrying every internal marker and asserts absence in both unescaped AND escaped wire forms plus raw values, with live negative controls and corrupt-row resilience. One-stable-contract, AR21 codecs (snake_case + round-trips), hook edge states (incl. unknown→failed wire agreement), byte-verbatim §9.5 canon disclaimer, and correct `decode.optional_field` wiring all verified. The 2 warnings are expand-window/corrupt-row-only edges with trivial fixes, safe to fold into the RC4 series; the 8 notes are P3 test/robustness gaps.

Address findings and push — the implementing minion owns fixes; a fresh round will follow if the head moves.
