# Lens: ACCEPTANCE AUDITOR (source: `acceptance`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/prompts/_preamble.md` in full and internalize the lens-guards. Then read the implementation spec at `/Users/moses/code/_bmad-output/implementation-artifacts/spec-rc3-7-fraud-signals-module.md` (AC1–AC8 + the AD-10 table) and the job briefing.

Audit the diff against the spec + ACs. Identify:
- Violations of specific acceptance criteria (reference the exact AC in `detail`)
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

Verify each AC against the actual code (read the files, don't infer):
- **AC1** — Does `fraud.gleam` produce EXACTLY the AD-10 table: the 3 pure-DB reuse signals, `line_type`/`voip_or_burner`, `form_session.{completion_seconds, ip_matches_applicant, device_fingerprint_match, focus_seconds_reported}`, `geo_vs_claimed_property:"unknown"`, `coached_answer_score:null`, `voice_matches_other_reference` ABSENT, `referee_contact_invalid` ABSENT? Any extra/missing key?
- **AC2** — Phase 1: creation writes the pure-DB signals + line-type + placeholders to the COLUMN (`form_session: null`); `result` stays null; pre-existing rows keep null. Verify the trigger wiring + `stamp_creation_fraud_signals`.
- **AC3** — Phase 2: submission computes `form_session` (completion_seconds server wall-clock, ip_matches, device_fingerprint_match labelled weak, focus_seconds_reported), re-runs DB signals, carries line-type; full signals land in `result.fraud_signals` AND the column; raw IP/UA inside form_session.
- **AC4** — Innocent reuse (same-name letting agent) does not flag; never a verdict/never auto-rejects/never alters a score.
- **AC5** — `with_referee_contact_invalid` / `stamp_referee_contact_invalid` stamps honestly; slug is `referee_contact_invalid` (the OLD `referee_number_wrong` is superseded/gone); absent at creation + submission. **Verify the old slug is NOT present anywhere in the worktree** (grep).
- **AC6** — No signal auto-rejects or alters a score (signals are display/confidence only).
- **AC7** — W1: dead `claim_webhook_event` defense layer REMOVED; comments name the real idempotency mechanism (find/mark `WHERE status IN ('queued','contact_initiated')`); NOT made early-return. Verify `webhooks.gleam::apply_delivery_failure`.
- **AC8** — (build/test + em-dashes are verified by Perkins directly; flag only if you see an obvious AC8 violation in copy.)

For each finding, quote the exact AC phrase in `detail`. Verify claims against the worktree.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/acceptance.json`, using `source: "acceptance"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
