# LENS: acceptance (source tag: `acceptance`) — Perkins r1 refcheck rc4-1

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Audit the diff against the spec. Identify:
- Violations of specific acceptance criteria (Story RC4.1 AC in the epics file, line ~607)
- Deviations from spec intent (architecture §8.1/§8.2/§9.5/§4.2/AD-11/AD-2, amendments A4/A5)
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

Walk the Story RC4.1 AC line by line against the diff:

1. **`reference_calls[]` per §8.1** — every field: `reference_call_id`, `ref_slot`, `owner_label`, `status`, `outcome`, `attempt_count`, `next_attempt_at`, the attempt log, the stored `result`, `display_disclaimer`, `hooks`. Check the §8.1 JSONC example in the architecture against the wire encoder.
2. **§4.2 stripping** — `form_token`, `objection_detail.payload_ref`, raw IPs/UAs inside `fraud_signals.form_session` absent from the serialized payload (escaped wire form too).
3. **`display_disclaimer` per §9.5** — written-channel results carry the §8.1 calibration copy verbatim; minimal terminals carry none. VERBATIM — byte-compare the shipped const against the §8.1 canon string.
4. **Hooks per §8.2** — `can_record_manual` any non-terminal, `can_substitute_referee` terminal objected/unreachable, `can_retry` failed.
5. **Application-level fields** — `attestation_on_file` AND `reference_contact_choice` (A4: nullable 'attested'/'declined'/NULL — the payload must distinguish declined-Off from pre-v1) "plus the referee trios, so the panel can render the Off state and the pre-trigger state without extra fetches". **Check whether `reference_contact_choice` and the referee trios (contact_name/contact_email/contact_phone of the referees) actually reach the payload.** The AC names them explicitly. Also check the SQL SELECT list — does it select the trio columns?
6. **AR21** — shared package types + JSON codecs, snake_case unbroken DB → JSON → Gleam, round-trip tests present.
7. **rc3-7 advisory notes sweep** (job briefing carry-forward): module doc, metadata, test-helper idiom, orphaned table — verify each was actually swept in this PR (grep the advisory edits in the diff: webhooks.gleam module doc, webhooks_test.gleam, reference_exit_routes_integration_test.gleam parameterized token helper). The NULLIF-convention note is NOT this PR's (RC4.3 owns it) — do not flag it.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
