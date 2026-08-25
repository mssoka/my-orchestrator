## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc3-7 · **Reviewed sha:** `2bf2577` · **Reviewers:** 7/7 completed · **Diff:** 2184 lines, 16 files
**Verification:** 18/20 reviewer findings confirmed against the code — **2 discarded as false-positive** (both diff-only blindness: `opt_to_str` is pre-existing in `trigger.gleam:1067`; `submitted_ip_text`/`submitted_user_agent` are `TEXT NOT NULL DEFAULT ''`). Head sha unchanged at review time.

Build + unit tests re-run by Perkins at `2bf2577`: ✅ `gleam build` clean, ✅ `1458 passed, 0 failures` (488 integration skipped — need DB). Both production lints (`let assert`, bare `httpc.send`) clean. The line-type lookup correctly uses `httpc.timeout` (rc3-1 carry), so the flagged synchronous-trigger tradeoff is timeout-bounded and no-ops to `Unknown`.

The AD-10 honesty invariant **holds**: every signal is produced with the right semantics, the honest placeholders are exact (`geo`=`"unknown"`, `coached`=`null`, `voice` absent, `referee_contact_invalid` absent), `referee_number_wrong` is fully superseded (only in explanatory comments), and the §4.2 boundary holds in scope (rc3-7 touches no landlord API; the referee submit returns only a thank-you page). Innocent-reuse is handled correctly (`contact_name` is `NOT NULL`, so the same-name exclusion has no NULL gotcha).

### 🔴 Blockers (1)

**B1 — Re-triggering reference checks wholesale-overwrites submitted `fraud_signals` (the submitted `form_session` is wiped).** [`edge`, root cause also flagged by `architecture`]
`create_eligible_slots` (`trigger.gleam:209`) calls `stamp_creation_fraud` **unconditionally after the tx — even when `inserted==0`** (ON CONFLICT no-op). `get_application_reference_contacts.sql` selects `WHERE application_id=$1` with **no status filter** (returns submitted/terminal rows too), and `stamp_creation_fraud_signals.sql` does a **wholesale** `UPDATE … SET fraud_signals = $2::jsonb WHERE id=$1` (no status guard). `creation_fraud_signals` emits `form_session: null`.

A landlord clicking **"Start reference checks"** (`handle_start` → `run_create_checks` → `create_eligible_slots`) — or the viewed trigger re-firing — on an application that already has **submitted** reference rows wholesale-overwrites those rows' `fraud_signals` with the creation-time object, **silently destroying the submitted `form_session`** signals (`completion_seconds`, `ip_matches_applicant`, `device_fingerprint_match`, `focus_seconds_reported`, `referee_ip`, `referee_user_agent`) and re-running paid Twilio lookups. `run_action_with_prechecks` gates `handle_start` only on ownership + vacancy-active (no row-state guard), and the inserts are idempotent by design (ON CONFLICT) — so re-calling is a **supported, expected** operation. The docstring's claim that the trigger "is idempotent (fires ~once per application)" is false: `handle_start` re-fires it on demand. The same root cause will clobber RC4.3's `referee_contact_invalid` stamp once wired. Submission is terminal, so the wiped signals are not recomputed.

*Fix (small):* make the stamp idempotent — skip the stamp pass when `inserted==0` (no new rows → nothing creation-time to add), or filter the stamp to rows whose `fraud_signals IS NULL` / non-terminal. Prefer the `inserted==0` skip — matches the "fires once" intent.

### 🟡 Warnings (4)

**W1 — Duplicated helpers across `form_handler.gleam` and `trigger.gleam`.** [`blind`+`architecture`, 3-source incl. Perkins]
`cross_application_reuse`, `opt_nonempty`, `parse_count` (and `opt_to_str`) are byte-identical across both modules (only the `uuid.Uuid` alias differs). Violates AGENTS.md "extract helpers when logic repeats 2+ places"; the two copies will drift. *Fix:* move them into a shared module (e.g. `reference_checks/contacts.gleam`, or fold the pure ones into `fraud.gleam`) and import from both.

**W2 — `fraud.carry_line_type` has no test (all 3 branches uncovered).** [`tests`]
The submission line_type carry (D3) — `""`→Unknown, valid→mapped, parse-error/missing-key→Unknown — is exercised only in production (`form_handler.gleam:1345`). Degrades honestly (AD-10), so not a fabrication risk, but a regression goes uncaught. *Fix:* unit-test the three branches.

**W3 — Phase 1 trigger wiring (`stamp_creation_fraud`) is never asserted post-trigger.** [`tests`]
The trigger integration suite calls `run_create_checks` repeatedly but asserts only `Created(count:)`/audit counts — never the `fraud_signals` column. The SQL contract + pure builder are pinned, but the orchestrator glue is unverified. AC2 "at row creation" is not pinned end-to-end. *Fix:* one integration test asserting `fraud_signals` keys are present after `run_create_checks`. (This would also have caught **B1**.)

**W4 — Advisory test gate: CONCERNS.** [`tests`]
P0 (AD-10 honesty) ~100% unit-covered; AC4 innocent-reuse + AC7 idempotency pinned. P1 persistence ~80% (creation wiring unverified; submission `focus_seconds` end-to-end but richer `form_session` fields unit-only); overall ~80%. Not FAIL (no P0 gap, no P1 <80%). Closing W2 + W3 lifts P1 and clears the gate.

### 🔵 Notes (8)

**N1 — `device_fingerprint_match_strength` is emitted but absent from the AD-10 table.** [`blind`+`acceptance`]
`form_session_block` emits a 5th `form_session` key (`…_strength:"weak"`) the spec's "exactly these keys" contract doesn't list (AC1). Harmless, but scope drift. *Fix:* drop it (convey "weak" via RC4 rendering) or amend the AD-10 table.

**N2 — Spec-named `fraud.with_referee_contact_invalid` Gleam fn + unit test not delivered (SQL stamp substitutes).** [`blind`+`acceptance`+`tests`]
Spec OWNS #1 / AC5 / Phase 3 name `fraud.with_referee_contact_invalid(json)` + a unit test; only the SQL `jsonb_set` stamp + integration tests ship. No behavioral gap (outcome + tests equivalent), but it diverges from the spec's named API and the "fraud.gleam owns signals" separation. *Fix:* add the Gleam helper + unit test, or record the SQL-stamp decision in the spec.

**N3 — W1 comment-correction incomplete (two stale comments still name the removed claim).** [`codebase`+Perkins]
`webhooks.gleam:12-13` module doc ("Idempotent (claim_webhook_event, NFR-RC5)") and `webhooks_integration_test.gleam:133` ("idempotent (claim 0 rows)") still attribute idempotency to the claim this diff removed. AC7/D6 required correcting the comments; the inline `apply_delivery_failure` comments were fixed, these two were missed. The idempotency test still passes (asserts outcome). *Fix:* update both to name the find/mark live-status scoping.

**N4 — Orphaned `sql.claim_webhook_event` + `claim_webhook_event.sql` (zero callers).** [`codebase`+Perkins]
After W1 removed the call site, nothing calls `claim_webhook_event` (grep confirms only the def + signature comment). Squirrel keeps regenerating it. *Fix:* delete the `.sql` + rerun Squirrel (separate regen change — not a merge blocker).

**N5 — Phase 2 submit only partially integration-covered.** [`tests`]
`focus_seconds_reported_flows_into_the_result_test` proves the full submit→result→`fraud_signals` wiring, but the richer `form_session` fields are unit-only. *Fix:* extend the assertion to `completion_seconds`/`ip_matches_applicant`/`device_fingerprint_match`.

**N6 — `lookup.line_type_from_string` + round-trip + unknown-fallback untested.** [`tests`]
The honesty-critical `_ -> Unknown` fallback isn't directly pinned. *Fix:* a round-trip test over all variants + an unmapped-string→Unknown case.

**N7 — `effective_contact` comment claims `corrected=""` falls back to snapshot, but code returns `None`.** [`blind`]
`Some("")` → `opt_nonempty("")` → `None`, not the snapshot (which only fires on `None`). Likely low impact (corrected is probably stored NULL when absent, not `""`), but the comment misrepresents the code and diverges from the SQL `NULLIF(corrected,'')` convention. *Fix:* implement the documented fallback or correct the comment.

**N8 — `stamp_creation_fraud_signals` doc says "non-optional String" but the generated type is `Json` (SQL directive says `TEXT`).** [`blind`]
Cosmetic; the generated code is correct (`Json` → `json.to_string` → `::jsonb`). *Fix:* correct the doc to `Json` and align the SQL directive to `JSONB`.

### Reviewer agreement
Highest-confidence (multi-source): **duplicated helpers** [blind+architecture]; **`device_fingerprint_match_strength` extra key** [blind+acceptance]; **`with_referee_contact_invalid` Gleam fn missing** [blind+acceptance+tests]. The **W1 stale-comment** (N3) and **orphan `claim_webhook_event`** (N4) were independently verified by Perkins and the codebase lens.

### Verdict
**NEEDS CHANGES** — one blocker (B1: silent data loss of submitted fraud signals on a supported re-trigger; small guard fix). The honesty invariant and the §4.2 boundary hold; the build + unit suite are green. The warnings are DRY + test-coverage hardening; the notes are scope/spec/comment cleanups.

_Address B1 and push — I re-review automatically on the new sha. After round 3, the human takes over._
