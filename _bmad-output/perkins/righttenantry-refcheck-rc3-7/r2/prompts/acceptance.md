# Lens: ACCEPTANCE AUDITOR (source: `acceptance`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/prompts/_preamble.md` in full and internalize the lens-guards + the fix-audit scope. Then read the implementation spec `/Users/moses/code/_bmad-output/implementation-artifacts/spec-rc3-7-fraud-signals-module.md` (AC1–AC8 + the AD-10 table + the amended OWNS/Decisions) and the job briefing.

Audit the diff against the spec + ACs at `5576ccb`. Identify violations of specific acceptance criteria, deviations from spec intent, missing implementation, contradictions, or scope drift.

## Fix-audit priority — N1, N2 (the r1 acceptance notes)

- **N1 (device_fingerprint_match_strength extra key).** r1: a 5th `form_session` key violated AC1 "exactly these keys". **Verify FIXED:** read `fraud.gleam::form_session_block` — the `device_fingerprint_match_strength` key must be GONE; the weakness is conveyed by a code comment only (the spec's clarify #4 "keep the AD-10 name, no sibling data key"). Confirm `form_session_block` emits EXACTLY: completion_seconds, ip_matches_applicant, device_fingerprint_match, focus_seconds_reported, referee_ip, referee_user_agent (the §4.2 internal-only pair).
- **N2 (SQL-stamp mechanism unrecorded).** r1: the spec named a `with_referee_contact_invalid` Gleam fn not delivered (a SQL stamp substitutes). **Verify FIXED:** the spec OWNS section + the clarify now record the SQL `stamp_referee_contact_invalid.sql` (jsonb_set) as the CHOSEN mechanism (a documented decision, not a divergence). The spec's "Decisions & rationale" should carry it.

Each correctly addressed → FIXED (do NOT re-file).

## Full AC re-audit at the fixed sha

Verify each AC against the actual code (read the files; r1 already audited these but a fix could regress one):
- **AC1** — `fraud.gleam` produces EXACTLY the AD-10 table: 3 pure-DB reuse signals, `line_type`/`voip_or_burner`, `form_session.{completion_seconds, ip_matches_applicant, device_fingerprint_match, focus_seconds_reported, referee_ip, referee_user_agent}`, `geo_vs_claimed_property:"unknown"`, `coached_answer_score:null`, `voice_matches_other_reference` ABSENT, `referee_contact_invalid` ABSENT. **N1's fix means form_session now has exactly its keys** — re-confirm no extra/missing key slipped in.
- **AC2** — Phase 1 creation writes pure-DB signals + line-type + placeholders to the COLUMN (`form_session: null`); `result` stays null. The B1 fix scopes the stamp to newly-created rows — confirm this does NOT break AC2 (new rows still get stamped; only re-triggers skip). Read `trigger.gleam::stamp_creation_fraud`.
- **AC3** — Phase 2 submission computes form_session, re-runs DB signals, carries line-type; full signals in `result.fraud_signals` AND the column; raw IP/UA inside form_session.
- **AC4** — Innocent reuse (same-name letting agent) does not flag; never a verdict.
- **AC5** — `stamp_referee_contact_invalid` (the SQL jsonb_set) stamps honestly; slug is `referee_contact_invalid`; `referee_number_wrong` GONE (grep the whole worktree).
- **AC6** — No signal auto-rejects or alters a score.
- **AC7** — W1: dead `claim_webhook_event` defense layer REMOVED; comments name the real idempotency mechanism; NOT made early-return. The N3 fix corrected the comments — confirm they now attribute idempotency to find/mark live-status scoping.
- **AC8** — `make test-server` green; no em-dashes in USER-FACING copy (comments/spec SQL are not user-facing — do not flag em-dashes there).

For each finding, quote the exact AC phrase in `detail`. Verify claims against the worktree.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/acceptance.json`, using `source: "acceptance"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
