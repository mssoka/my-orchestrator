# Review preamble — read this FIRST (applies to all specialist lenses)

You are reviewing a code diff as ONE specialist lens in a parallel review team. You have read-only access to the repository worktree and MAY (and should) verify the diff's claims against the actual codebase using your tools before filing any finding.

**THIS IS ROUND 2 — A FIX-AUDIT ROUND.** The implementing minion (pTQ) pushed fixes for round 1's findings (1 blocker + 4 warnings + 8 notes; it claims 13/13 addressed). Your FIRST job is to verify each r1 finding is actually FIXED at this sha. Your SECOND job is a normal pass over the delta for any NEW issue the fix introduced. **Fix-audit-first.**

## Inputs

- **DIFF (review these exact bytes):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/diff.patch` (the FULL PR diff develop...HEAD, 2628 lines, 16 files). Every finding must be anchored in lines you can quote from this file.
- **WORKTREE (verification reads — your cwd):** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-7-r2`. Detached at exactly the reviewed sha `5576ccb`. Trust it, not `origin/develop`.
- **PRIOR FINDINGS (the r1 audit targets — read this FIRST):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/consolidated.json`.
- **SPEC / CONTEXT (read these to understand intent):**
  - The Perkins r2 briefing: `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-7-r2.md`
  - The job briefing: `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-7.md`
  - The implementation spec: `/Users/moses/code/_bmad-output/implementation-artifacts/spec-rc3-7-fraud-signals-module.md`
  - The GitHub issue dump: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/issue-548.json`
  - Project conventions (AGENTS.md): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-7-r2/AGENTS.md`

## The r1 findings to verify FIXED (fix-audit scope)

For each, re-read the cited code at `5576ccb`. Mark **FIXED** (with the new code location proving it) or **STILL OPEN** (with evidence). A correctly-fixed r1 finding is NOT a round-2 blocker — only re-flag if the fix is WRONG, INCOMPLETE, or introduced a NEW defect.

- **B1 (BLOCKER — stamp_creation_fraud wholesale-overwrite).** r1: re-triggering (handle_start re-fires) wiped submitted fraud_signals because the stamp ran unconditionally (even inserted==0), read ALL rows, wholesale SET. **Verify FIXED:** a guard skips stamping when `created_ids == []`, and the WRITE is scoped to only the newly-created row ids (not all the application's rows). Read `trigger.gleam::create_eligible_slots` + `stamp_creation_fraud` + `create_one_slot`. The fix must leave a submitted sibling's `form_session` intact on a re-trigger.
- **W1 (DRY — duplicated helpers).** r1: `cross_application_reuse` + `opt_nonempty` + `parse_count` (+ `opt_to_str`) duplicated across `form_handler.gleam` and `trigger.gleam`. **Verify FIXED:** a shared `reference_checks/fraud_inputs.gleam` module owns them; both call sites import it; the duplicate `opt_to_str` is gone from `trigger.gleam`; the extraction is behavior-preserving (same fn bodies).
- **W2 (carry_line_type untested).** r1: 3 branches (empty/valid/unparseable) uncovered. **Verify FIXED:** real, passing unit tests in `fraud_test.gleam` covering the branches.
- **W3 (Phase-1 trigger wiring unasserted).** r1: the trigger integration tests asserted only `Created(count:)`, never the `fraud_signals` column. **Verify FIXED:** an integration test that calls `trigger.run_create_checks` then asserts the fraud_signals keys landed (AC2).
- **W4 (advisory gate CONCERNS).** r1: P1 ~80% → CONCERNS. **Verify:** W2+W3 closed → re-evaluate the gate (should now be PASS).
- **N1 (device_fingerprint_match_strength extra key).** r1: a 5th form_session key violated AD-10 "exactly these keys". **Verify FIXED:** the key is dropped from `form_session_block`; the weakness is conveyed by comment only.
- **N2 (SQL-stamp mechanism unrecorded).** r1: the spec named a `with_referee_contact_invalid` Gleam fn that wasn't delivered (a SQL stamp substitutes). **Verify FIXED:** the spec records the SQL-stamp as the chosen mechanism (not a divergence).
- **N3 (stale comments).** r1: the webhooks module doc + a test comment still named the removed `claim_webhook_event` as the idempotency mechanism. **Verify FIXED:** both name the find/mark live-status scoping now.
- **N4 (orphaned claim_webhook_event.sql).** r1: zero callers but the `.sql` + generated fn remained. **Verify FIXED:** `claim_webhook_event.sql` deleted; the generated `claim_webhook_event` fn + `ClaimWebhookEventRow` type removed from `sql.gleam`.
- **N5 (submit only partially covered).** r1: focus_seconds end-to-end but richer form_session fields unit-only. **Verify FIXED:** the exit-routes submit test asserts the full form_session block (completion_seconds, ip_matches_applicant, device_fingerprint_match, referee_ip/ua).
- **N6 (line_type round-trip untested).** r1: `line_type_to_string`/`line_type_from_string` + the unknown-fallback untested. **Verify FIXED:** tests in `lookup_test.gleam` for all variants + round-trip + unmapped→Unknown.
- **N7 (effective_contact Some("") mis-documented).** r1: the comment claimed corrected="" falls back to snapshot, but code returned None. **Verify FIXED:** the `effective_contact` helper now falls back to snapshot for Some("") (matching the SQL NULLIF convention), OR the comment is corrected.
- **N8 (stamp directive TEXT vs JSONB).** r1: the `stamp_creation_fraud_signals` SQL directive said `TEXT` but the generated fn took `Json`. **Verify FIXED:** the `.sql` directive now says `JSONB` (consistent with the `arg_2: Json` signature).

## r1's 2 false-positives — DO NOT re-flag

- `opt_to_str` "missing" — it is pre-existing in `trigger.gleam` (r1) / now in `fraud_inputs.gleam`. Not a defect.
- `submitted_ip_text` / `submitted_user_agent` "NULL-crash" — both are `TEXT NOT NULL DEFAULT ''` (migration 20260731220100). `decode.string` is correct.

## ⚠️ CRITICAL LENS-GUARDS — read before evaluating ANY finding (prevents false positives)

These are documented, accepted design decisions or out-of-scope gates. Flagging any as a defect is a FALSE POSITIVE.

- **Do NOT re-litigate the r1 findings as NEW findings.** B1/W1-W4/N1-N8 are in fix-audit scope — you VERIFY each is fixed (FIXED with location, or STILL OPEN with evidence). A correctly-fixed r1 finding is NOT a round-2 finding. Only re-flag one if the fix is WRONG/INCOMPLETE or introduced a new defect.
- **AD-10 HONESTY is the load-bearing invariant.** Fraud signals are CLUES about provenance — NEVER fabricated detections, NEVER verdicts. They NEVER auto-reject and NEVER alter a score. The v2-reserved signals emit honest placeholders EXACTLY: `geo_vs_claimed_property` = `"unknown"`, `coached_answer_score` = `null`, `voice_matches_other_reference` is **ABSENT**, `referee_contact_invalid` is **ABSENT** until a correction cycle exhausts. A fabricated signal, a placeholder pretending to be real data, a signal that auto-rejects, or a signal that alters a score = a BLOCKER. Do NOT flag the honest placeholders themselves as "wrong". The B1 guard fix touches the stamping path — verify it doesn't break the honesty contract (a SKIPPED stamp must leave the honest state, not a fabricated one).
- **RAW IPs/UAs are stored INSIDE `form_session` BY DESIGN (§4.2 + spec D5).** `form_session.referee_ip` and `form_session.referee_user_agent` are intentionally server-side evidence, internal-only. RC4.1 (a FUTURE story) strips them at the landlord API boundary. rc3-7 touches NO landlord API — storing them inside `result.fraud_signals` and the `fraud_signals` column is the DOCUMENTED, ACCEPTED design. Do NOT flag it as a privacy leak. (You MAY verify rc3-7 added no landlord-facing response/notification exposing them.)
- **INNOCENT REUSE ≠ FRAUD.** A letting agent legitimately appearing across several applications under the SAME name is NOT fraud — the cross-application SQL excludes same-name (`rc.contact_name <> $2`). Do NOT flag the same-name exclusion as a bug. (You MAY check whether `contact_name` can be NULL and whether that breaks the `<>` comparison.)
- **`referee_contact_invalid` SUPERSEDES `referee_number_wrong` (§6.4).** The old slug must NOT still be present anywhere. Both present = a real defect.
- **External gate — Twilio Lookup needs keys (unprovisioned).** Until then `line_type` is `"unknown"` and the lookup no-ops to `Unknown` — the HONEST value, not a bug. Do NOT flag "line_type always unknown without keys."
- **The synchronous line-type lookup in the trigger path is a FLAGGED, ACCEPTED tradeoff** (~1s typical, no-ops on timeout). You MAY note a genuine concrete risk (a timeout path leaving a stale signal, the lookup running while holding a transaction) IF you verify one — but the tradeoff itself is accepted.
- **The `fraud_signals` JSONB column is PRE-EXISTING (rc2-1).** This PR adds NO migration. rc3-7 only WRITES it.

## OUTPUT — write ONE valid JSON array to your lens's path and STOP

Write your JSON array to the path named in your lens file (e.g. `.../r2/edge.json`). The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble.

Each element must match this schema exactly:
```json
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the diff or worktree file that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```

An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. For a clean fix-audit round, an empty array (all r1 findings verified FIXED, no new defect) is the HONEST and EXPECTED answer.

## ACCURACY MANDATE — the most important instruction

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore: open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code. The `evidence` field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly") is a signal you have not verified the issue — either verify and report crisply, or do not report. Fewer well-grounded findings beat many speculative ones.
