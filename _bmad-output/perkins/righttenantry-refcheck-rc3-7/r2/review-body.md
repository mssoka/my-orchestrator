## 🤖 Perkins automated review — round 2 of 3 (FIX-AUDIT)

**Job:** righttenantry-refcheck-rc3-7 · **Reviewed sha:** `5576ccb` · **Reviewers:** 7/7 completed
**Verification:** 8/8 reviewer findings survived code re-verification — 0 discarded as false-positive; 1 downgraded (blind `warning` → `note`, see N3-new rationale). All 13 r1 findings independently re-audited.
**Model:** `zai-coding-cn/glm-5.2` (kimi quota down this cycle — sanctioned fallback). One lens 429'd and was revived with a single `continue` (validated mitigation).

### Fix-audit — r1 findings (B1 + W1–W4 + N1–N8): 12 FIXED, 1 STILL OPEN

| r1 | Status | Evidence (at `5576ccb`) |
|---|---|---|
| **B1** blocker | ✅ FIXED | `create_one_slot` returns `Some(id)`/`None`; `create_eligible_slots` collects `created_ids`; `stamp_creation_fraud` returns `Nil` on `[]` and scopes the WRITE to `to_stamp = list.filter(all_refs, in created_ids)`. A skipped stamp leaves the honest state (no fabrication). Regression pinned by **2** integration tests (`re_trigger_does_not_wipe_submitted_fraud_signals_test` + `re_trigger_new_row_does_not_wipe_submitted_sibling_test`). |
| **W1** DRY | ✅ FIXED | `reference_checks/fraud_inputs.gleam` owns the 8 shared helpers; both `trigger.gleam` + `form_handler.gleam` import it; dup `opt_to_str` removed. Behavior-preserving. |
| **W2** carry_line_type test | ✅ FIXED | 4 unit tests (empty/valid/missing-key/unparseable → Unknown). |
| **W3** trigger wiring | ✅ FIXED | `trigger_stamps_creation_fraud_signals_test` asserts the `fraud_signals` column after `run_create_checks` (AC2 pinned end-to-end). |
| **W4** advisory gate | ✅ FIXED → PASS | W2+W3+N5+N6 closed; gate now **PASS** (P0 100%, P1 ≥90%, overall ≥80%). |
| **N1** extra form_session key | ✅ FIXED | `device_fingerprint_match_strength` removed; weakness is a comment only. Zero grep hits. |
| **N2** SQL-stamp unrecorded | ✅ FIXED | Spec OWNS #3 + Decisions record `stamp_referee_contact_invalid.sql` (jsonb_set) as the chosen mechanism. |
| **N3** stale comments | ⚠️ **STILL OPEN** | The inline `apply_delivery_failure` comments + the test comment were fixed, but the **module doc line 13** still says `Idempotent (claim_webhook_event, NFR-RC5)`. See Notes #1. |
| **N4** orphan claim .sql | ✅ FIXED | `claim_webhook_event.sql` deleted; generated fn + type removed. (Downstream: the `processed_reference_webhook_event` *table* is now orphaned — see Notes #2, a new finding r1 didn't enumerate.) |
| **N5** submit form_session | ✅ FIXED | Exit-routes submit test extended to the full `form_session` block. |
| **N6** line_type round-trip | ✅ FIXED | 3 lookup tests (all variants + round-trip + unmapped→Unknown). |
| **N7** effective_contact `Some("")` | ✅ FIXED | `effective_contact(Some(""), snapshot)` → `opt_nonempty("")` → `None` → `snapshot`. Matches its doc + the established SQL convention. |
| **N8** stamp directive | ✅ FIXED | `stamp_creation_fraud_signals.sql` directive is now `fraud_signals: JSONB`. |

r1's 2 false-positives respected (not re-flagged): `opt_to_str` (pre-existing/moved), `submitted_ip_text`/`submitted_user_agent` (`TEXT NOT NULL DEFAULT ''`).

### Blockers (0)
None. The B1 stamp-overwrite blocker is correctly fixed and regression-tested; AD-10 honesty holds (a skipped/failed stamp leaves the honest state, never a fabricated signal).

### Warnings (0)
None surviving verification. (Blind emitted one `warning` on `effective_contact`/NULLIF — downgraded to note: the divergence has no live trigger, see Notes #3.)

### Notes (5)

**#1 — N3 still open: webhooks.gleam module doc still names the deleted `claim_webhook_event` as the idempotency mechanism** `[edge+acceptance+architecture+codebase — 4-source agreement]`
`server/src/reference_checks/webhooks.gleam:12-13`
> `//// NOTHING — no spoofed bounce can move a row. Idempotent (claim_webhook_event,`
> `//// NFR-RC5) and sticky (the guarded mark_awaiting_correction leaves terminal /`

r2 fixed the inline `apply_delivery_failure` comments and the integration-test comment, but the module doc still attributes idempotency to `claim_webhook_event` — which N4 deleted. *Fix:* rewrite the clause to name the find/mark live-status scoping (`WHERE status IN ('queued','contact_initiated')`), matching the corrected inline + test comments.

**#2 — `processed_reference_webhook_event` table + a stale comment left behind after W1** `[codebase + Perkins]`
`supabase/migrations/20260812060000_create_processed_reference_webhook_event.sql:8` + `webhooks.gleam:38`
W1 removed the only writer (`claim_webhook_event`'s `INSERT ... ON CONFLICT`); nothing reads the table either. `webhooks.gleam:38` still documents it as the live idempotency table. Dead infrastructure (AGENTS.md "No Technical Debt"). (`source_resend`/`source_twilio` constants are **not** orphaned — still used at 122/211.) *Fix:* if rc3-6 is unmerged, drop the migration; otherwise a follow-up DROP TABLE (destructive → separate two-deploy, not this PR). Clear the line-38 comment either way.

**#3 — New rc3-7 SQL diverges from the established `NULLIF(corrected,'')` convention (latent)** `[blind → downgraded warning→note; Perkins-verified]`
`sql/get_application_reference_contacts.sql` + `sql/count_cross_application_contact_reuse.sql` (vs the established pattern at `sql.gleam:297-298`)
The new SQL uses plain `COALESCE(corrected_email, contact_email, '')`; the established dedup query uses `COALESCE(NULLIF(corrected_email,''), contact_email)`. IF `corrected_*` were ever stored as `''`, creation would return `''` (losing the snapshot) while submission `effective_contact(Some(""))` falls back to snapshot — a divergence. **No live trigger:** `corrected_*` is nullable TEXT, NULL-by-convention, and nothing writes it today (RC4.3 owns the correction write and doesn't exist yet). Comment-accuracy + consistency hardening. *Fix:* wrap `NULLIF` in both new COALESCEs; do it when RC4.3 lands the correction write at the latest.

**#4 — New N5 test helper string-interpolates the token into SQL** `[security + Perkins]`
`server/test/integration/reference_exit_routes_integration_test.gleam:684`
`form_session_text` builds `"... WHERE form_token = '" <> token <> "'"`. Test-only, token is test-controlled, and it follows this file's pre-existing idiom (no real injection, not a regression rc3-7 introduced). Flagged because the new helper models string-interpolated SQL rather than `pog.parameter` binding. *Fix (low priority):* bind with `pog.parameter(pog.text(token))` if the file's helpers are migrated wholesale.

**#5 — sprint-status `last_updated` regressed while rc3-7 advanced** `[blind + Perkins]`
`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`
`last_updated` moved `2026-08-12 → 2026-08-11` in the same edit that advanced rc3-7 `backlog → review`. Tracking-file metadata only, not product code. *Fix:* set it to the actual edit date.

### Reviewer agreement
4 independent lenses (edge + acceptance + architecture + codebase) converged on N3 (module doc) — the highest-confidence signal, independently confirmed by Perkins. The B1 blocker fix is verified correct and regression-tested. Advisory test gate PASS. No blocker or warning survives verification.

### Verdict
**READY TO MERGE.** All r1 findings fixed except N3 (a stale module-doc comment). The load-bearing B1 stamp-overwrite blocker is correctly scoped to newly-created rows and regression-pinned; AD-10 honesty, the §4.2 boundary, the `referee_contact_invalid` supersession, and innocent-reuse all hold; the test suite is green at this sha. The 5 notes are comment-accuracy / orphan-cleanup / latent-hardening items — none merge-blocking.

_Address the notes and push — I re-review automatically on the new sha. After round 3, the human takes over._
