You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-4-r2/AGENTS.md and treat it as the project conventions.

--- DIFF ---
This is chunk 1 of 2 (file-group split) of the PR diff. Review exactly these bytes:

diff --git a/_bmad-output/implementation-artifacts/spec-rc4-4-attempt-log-export-notification-completeness.md b/_bmad-output/implementation-artifacts/spec-rc4-4-attempt-log-export-notification-completeness.md
new file mode 100644
index 00000000..3d4fa6a5
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-rc4-4-attempt-log-export-notification-completeness.md
@@ -0,0 +1,364 @@
+---
+baseline_commit: 3dc3524
+story_key: rc4-4-attempt-log-export-notification-completeness
+---
+
+# Story RC4.4: Attempt Log, Export & Notification Completeness
+
+**Status:** in-progress (briefing pre-approved — epic ACs are canonical)
+**Epic:** RC4 (Landlord Reference Panel & Workflow). Depends on RC4.3 (merged, #606).
+**Model:** `deepseek/deepseek-v4-flash` (briefing policy — execution role).
+**Perkins:** ON.
+**GitHub issue:** (none)
+
+## Story
+
+> As a landlord,
+> I want the full attempt history and trustworthy notifications,
+> So that I have evidence for my records and never miss a state change.
+
+RC4.3 shipped the row actions and a plain clipboard copy of the send log. RC4.4
+completes the reference panel's evidence surface: the §7.6 attempt-log timeline
+rendered in the Audit Trail's visual language covering EVERY event class
+(send, form-opened, correction, takeover, substitution, terminal), an export
+that carries (reference, timeline, outcome, signals) with the verbatim OQ-5
+toast, and notification completeness per UX §7.9 — including the deferred
+RC2.1 codec that makes any emitted `reference_*` notification decodable
+client-side (today the notification dropdown fails to decode them).
+
+**The load-bearing rules:** (1) the attempt log is SERVER-BUILT — AR-RC13
+standing lesson (RC4.2 r1 / RC4.3 r1): the payload is the single source of
+truth; the client renders labels, never re-derives the event set or ordering
+(the current client-side mini-timeline groups sends and sorts by raw `at`,
+which mis-orders same-day PG-text (` ` separator) vs RFC3339 (`T`) stamps —
+the server builder normalizes and owns the order); (2) every terminal writer
+stamps the terminal instant (`terminalized_at`), the substitute path stamps
+the new row (`substituted_at`) — expand-only columns, previous revision never
+reads them; (3) notification copy is UX §7.9 verbatim (modulo the standing
+em-dash ban: §7.9's late-completion line was rephrased to a period in rc3-4
+and stays that way); (4) the OQ-5 export toast is verbatim INCLUDING its
+em-dash (spec copy — the client copy test's em-dash scan excludes spec-verbatim
+strings by construction; the toast moves out of the scanned list).
+
+## Scope
+
+### OWNS
+1. **Deferred RC2.1 codec (MUST land here):** `shared/src/shared/notification.gleam`
+   — FIVE `reference_*` NotificationType variants + codec arms
+   (`reference_completed`, `reference_unreachable`, `reference_objected`,
+   `reference_declined` from the RC2.1 migration, PLUS `reference_awaiting_correction`
+   which joined in RC3.6 and is already emitted — the briefing counts the RC2.1
+   four; completeness demands the fifth or awaiting_correction rows stay
+   undecodable) + `client/src/components/notification_dropdown.gleam` — the
+   exhaustive `view_type_icon` match gains the five arms (Gleam forces totality).
+2. **Attempt-log timeline (server-built):** new `attempt_log: List(AttemptLogEntry)`
+   wire key on `ReferenceCallDetail` — `{kind, at, channel, outcome, detail}`:
+   kinds `invitation_sent` | `co_nudge` | `reminder_sent` | `form_opened` |
+   `corrected` | `taken_over` | `substituted` | `terminal`. Built by a pure
+   `build_attempt_log` fn in `application_detail_handler.gleam`: attempts
+   JSONB grouped by `at` (one sweep step stamps one `at` for its channels) →
+   cadence kinds by batch position; column events appended; timestamps
+   normalized (PG ` ` → `T`) and the whole list sorted by `at` — the server
+   owns order (AR-RC13). `attempts` key stays (RC4.1 contract, back-compat).
+3. **Expand-only migration:** `substituted_at TIMESTAMPTZ` +
+   `terminalized_at TIMESTAMPTZ` on `reference_call`. Stamped by:
+   `terminalize_reference_call.sql` (refused/objected),
+   `complete_reference_call.sql` (form_completed), `sweep_terminal.sql`
+   (unreachable/partial), `exhaust_reference_call.sql` (unreachable),
+   `sweep_mark_failed.sql` (failed) — each gains `terminalized_at = now()`;
+   the substitute path stamps `substituted_at = now()` on the NEW row via a
+   new tiny `mark_substituted_reference_call.sql` (guarded
+   `WHERE id = $1 AND substituted_at IS NULL`) inside `do_substitute`'s
+   transaction. Detail read (`list_reference_calls_for_detail.sql`) gains
+   `corrected_at`, `substituted_at`, `terminalized_at`, `objected_at`,
+   `updated_at` (COALESCE ''; the builder falls back
+   `terminalized_at → submitted_at → objected_at → updated_at` for legacy
+   terminal rows).
+4. **Notification copy fix (§7.9 verbatim):** `notify_reference_unreachable`
+   (the T+96h warm-handoff in-app body) currently reads "X couldn't be reached
+   for Y's reference. You may want to call them yourself." — NOT the §7.9
+   Unreachable line. Fix to the verbatim line ("Couldn't reach X (Y's referee).
+   You can take over from the application page.") — identical to
+   `notify_reference_correction_exhausted` (both are `reference_unreachable`;
+   §7.9 defines one Unreachable copy). The warm-handoff EMAIL keeps its richer
+   template (separate surface). Other bodies verified already verbatim:
+   received (title+body compose), declined, objected, late-completion
+   (de-dashed per rc3-4).
+5. **Preference-matrix test:** extract `email_allowed_for(pref)` (pure gate:
+   Realtime → True, Daily → False, Off → False) used by `maybe_send_email` +
+   `maybe_send_rich_email`; unit-test the 3×matrix. Integration: per
+   preference (realtime/daily/off seeded on the landlord row), fire a
+   reference event and assert the in-app notification row lands with the
+   right type (all three) — the email half is proven by the gate unit test
+   (tests run with "" resend key, so the HTTP branch is unreachable; the gate
+   IS the preference decision).
+6. **No-duplicate-terminals test:** extend the sweep's full-cadence walk test
+   to assert the notification TYPE is `reference_unreachable` (not just
+   count==1) and T+144 adds none — the T+96h warm handoff is the only
+   unreachable-path notification (§8.3).
+7. **Client timeline + export:** `reference_panel.gleam` renders
+   `view_attempt_log` (replacing the mini-timeline internals) from the
+   payload `attempt_log` in the Audit Trail's visual language
+   (`role="list"`, `role="listitem"`, `<time datetime>`) for every started row
+   (attempt_log non-empty: ContactInitiated, AwaitingCorrection, Unreachable,
+   Refused, Objected, terminal rows incl. taken-over). The export affordance
+   (testid `refcheck-export-<slot>`, currently takeover-surface-only) moves
+   into the timeline block so ANY started row can export. `client.gleam`'s
+   `build_attempt_log_text` → `reference_panel.export_attempt_log_text`:
+   plain text of (reference, timeline, outcome, signals) — signals from the
+   parsed result fraud_signals (worth-knowing lines) or "None recorded";
+   outcome = a per-status label. `copy.gleam`: OQ-5 verbatim toast
+   ("Attempt log copied — paste it into your records or a message."), new
+   timeline labels (corrected/taken-over/substituted/terminal per status),
+   export section labels. `client/test/copy_test.gleam`: `refcheck_toast_exported`
+   moves OUT of the em-dash-scanned `refcheck_action_strings` (now spec-verbatim
+   OQ-5, excluded by construction — comment it).
+
+### Does NOT own (deferred / sibling stories)
+- **WoZ record-manual UI** — RC5.1.
+- **File-download export** — decided clipboard-only in v1 (OQ-5).
+- **Notification click-through to the application page** — the dropdown's
+  entity navigation is a separate surface; reference notifications carry
+  entity_type `reference_call` (navigating needs an application-id in the
+  payload — out of scope for this story's ACs).
+
+## Acceptance Criteria (BDD — from epic RC4.4 + UX §7.6/§7.9 + OQ-5 + §8.3)
+
+**AC1 — Attempt-log timeline**
+> **Given** a started row, when the attempt log expands, then the timeline per
+> UX §7.6 renders in the Audit Trail's visual language (`role="list"`,
+> `<time datetime>`), covering every send, form-opened, correction, takeover,
+> substitution, and terminal event — the event set and order come from the
+> payload `attempt_log`, never re-derived client-side (AR-RC13).
+
+**AC2 — Export**
+> **Given** a started row, when "Export attempt log" is chosen, then a
+> plain-text version (reference, timeline, outcome, signals) copies to the
+> clipboard with the verbatim OQ-5 toast ("Attempt log copied — paste it into
+> your records or a message.") — no file download in v1.
+
+**AC3 — Notification completeness**
+> **Given** the notification surface, when each reference event fires, then
+> every reference event has its UX §7.9 copy verbatim — including the
+> late-completion-after-handoff variant (reuses `reference_completed`) — and
+> a preference-matrix test proves realtime/daily/off behaviour per landlord
+> `notification_preference` (in-app always; email only for Realtime).
+
+**AC4 — No duplicate terminals**
+> **Given** the sweep cadence, when a row walks T+0 → T+144, then a
+> no-duplicate-terminals test proves the T+96h warm handoff is the only
+> unreachable-path notification (§8.3) — exactly one `reference_unreachable`
+> in-app row across the walk, none at T+144.
+
+**AC5 — Codec**
+> **Given** any emitted `reference_*` notification (all five values), when the
+> client decodes the notifications list, then it decodes (shared codec arms)
+> and the dropdown renders it (exhaustive icon match).
+
+## Verify
+- `make test-server` green (unit + integration: builder, terminal stamps,
+  substituted stamp, warm-handoff body, preference matrix, no-duplicate type).
+- `make test-client` green (timeline render from attempt_log, export text,
+  verbatim toast, dropdown totality).
+- `make test-shared` green (5 notification types round-trip; attempt_log
+  entry codec; detail decoder back-compat with absent `attempt_log`).
+- `make format && make build` green (pre-PR discipline); `gleam format --check` clean.
+- Squirrel regen after the SQL changes (`gleam run -m squirrel` after
+  `make test-db-up`; revert churn in `ai/sql.gleam`/`application/sql.gleam`
+  that isn't mine per the field notes).
+- Copy verbatim from the cited UX sections — grep-check key strings.
+
+## Files
+- **EDIT:** `shared/src/shared/notification.gleam` (5 variants + arms) ·
+  `shared/src/shared/reference_call.gleam` (AttemptLogEntry + `attempt_log`
+  key, back-compat decoder) · `server/src/application/application_detail_handler.gleam`
+  (build_attempt_log + map) · `server/src/application/sql/list_reference_calls_for_detail.sql`
+  (+5 COALESCE columns) · `server/src/notification/notification_dispatch.gleam`
+  (warm-handoff body verbatim + email_allowed_for gate) ·
+  `server/src/reference_checks/actions_handler.gleam` (substituted stamp) ·
+  `server/src/reference_checks/sql/terminalize_reference_call.sql` +
+  `complete_reference_call.sql` + `sweep_terminal.sql` +
+  `exhaust_reference_call.sql` + `sweep_mark_failed.sql` (terminalized_at)
+  · `client/src/components/reference_panel.gleam` (view_attempt_log + export
+  builder) · `client/src/components/notification_dropdown.gleam` (5 icon
+  arms) · `client/src/client.gleam` (export text call) ·
+  `client/src/copy.gleam` (OQ-5 toast + timeline/export labels) ·
+  `client/test/copy_test.gleam` (toast out of em-dash scan)
+- **NEW:** `supabase/migrations/20260813120000_reference_call_timeline_columns.sql`
+  (substituted_at + terminalized_at, expand-only) ·
+  `server/src/reference_checks/sql/mark_substituted_reference_call.sql` ·
+  `shared/test/...`/`server/test/...`/`client/test/...` additions per Verify.
+
+## Dev Notes
+
+### Source tree map (verified on disk at baseline)
+- `shared/src/shared/notification.gleam` — 7 variants, `encode_type` +
+  `type_decoder` (unknown → `decode.failure` — this is why the dropdown is
+  broken today: any `reference_*` row fails the whole list decode).
+- `server/src/notification/notification_dispatch.gleam` — `notify_reference_*`
+  fns; `maybe_send_email`/`maybe_send_rich_email` read
+  `sql.get_landlord_email_prefs` and gate on `landlord.Realtime`.
+- `server/src/reference_checks/sweep.gleam` — `dispatch_warm_handoff` calls
+  `notify_reference_unreachable` (in-app) AFTER the guarded advance (exactly-
+  once); T+144 `step_terminal` is silent (existing tests pin count==0).
+- `server/src/application/application_detail_handler.gleam:1194` —
+  `encode_reference_call` maps the detail row; `parse_attempt_log` already
+  parses the attempts JSONB. The builder slots in here (pure, unit-testable).
+- `client/src/components/reference_panel.gleam` — `view_attempt_summary`
+  (1267) groups attempts client-side (group_by_at) + sorts raw `at`
+  (`string.compare` — space-vs-T mis-order on same-day timestamps); the
+  takeover surface's export button (1247) moves into the timeline block.
+- `client/src/client.gleam:6863` — `build_attempt_log_text` (the v1 text:
+  "Reference: X / State: status / raw attempt lines").
+- `client/test/copy_test.gleam:341` — `refcheck_action_strings` includes
+  `refcheck_toast_exported` (currently "Attempt log copied") — it becomes
+  spec-verbatim OQ-5 and leaves the scanned list.
+- Terminal writers all bump `updated_at = now()` today; none records the
+  terminal INSTANT as first-class data (`submitted_at` covers form_completed,
+  `objected_at` covers objected; refused/unreachable/partial/failed have no
+  column) — `terminalized_at` is the honest stamp.
+- Substitution inserts via the shared `insert_reference_call_if_absent`
+  (idempotent) — the new-row marker is a separate guarded UPDATE inside
+  `do_substitute`'s transaction, so the shared insert stays untouched.
+
+### Decisions & rationale (for the PR)
+- **FIVE codec variants, not four:** the briefing counts the RC2.1 migration's
+  four `reference_*` values, but `reference_awaiting_correction` joined in
+  RC3.6's migration and is already emitted by `notify_reference_awaiting_correction`
+  (webhooks). Leaving it out keeps the dropdown decode-broken for exactly the
+  class this story exists to fix — completeness demands the fifth.
+- **Server-built `attempt_log` (AR-RC13):** the event set, kinds, and ordering
+  are state, not presentation — the server derives them from the row and the
+  client renders labels. This also fixes the latent same-day ordering bug in
+  the client's raw-`at` sort (PG `2026-08-01 21:12:00+00` sorts before
+  `2026-08-01T10:04:00Z` lexically even when later).
+- **`terminalized_at`/`substituted_at` columns (expand-only):** the terminal
+  instant is first-class evidence (§7.6 "Closed — no reply" needs a time);
+  `updated_at` is polluted by later writes (takeover on unreachable). The
+  previous Cloud Run revision never reads the new columns — expand-only per
+  the migration discipline.
+- **Warm-handoff in-app body → §7.9 verbatim:** §7.9 defines ONE Unreachable
+  copy; both unreachable-path notifications (T+96 warm handoff, correction
+  exhaustion) carry it verbatim. The warm-handoff EMAIL template is a
+  separate surface and keeps its richer attempt-log render.
+- **OQ-5 toast verbatim with its em-dash:** spec copy is excluded from the
+  client em-dash scan by construction (the scan list comment already says so);
+  the toast moves out of `refcheck_action_strings` with a comment. Other
+  implementer-authored strings stay dash-free.
+- **`attempts` key kept:** RC4.1 wire contract + the warm-handoff email build
+  from the row server-side; the client timeline switches to `attempt_log`.
+- **Late-completion body stays de-dashed** ("after all. It's on…") — rc3-4's
+  documented rephrase of §7.9's em-dash line; not re-litigated here.
+
+### Testing standards
+- Builder unit tests (pure): batch kinds by cadence position, column events,
+  normalization + ordering (same-day PG vs RFC3339), terminal fallback chain.
+- Terminal stamp tests: each terminal writer leaves `terminalized_at` set
+  (complete/terminalize/sweep_terminal/exhaust/mark_failed); substitute leaves
+  `substituted_at` on the NEW row only (old row untouched, idempotent double-
+  submit no-op).
+- Preference matrix: unit 3× (Realtime/Daily/Off → gate) + integration per
+  preference (seed landlord preference, fire reference event, assert in-app
+  row type).
+- No-duplicate: full-cadence walk → exactly one `reference_unreachable` in-app
+  row; T+144 terminal adds none (extend the existing full-cadence test with
+  a type assertion).
+- Client: serialized render assertions (`role="list"`, `<time datetime>`,
+  pinned `data-testid`s) per the 2026-08-03 field note; export text contains
+  reference/timeline/outcome/signals; dropdown renders all five types.
+- Negative control per the 2026-08-09 field note: the timeline test fails if
+  fed an old payload without `attempt_log` (back-compat default []).
+
+### References
+- [Source: `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` — Story RC4.4 (line ~692), OQ-5]
+- [Source: `_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md` — §7.6, §7.9, §8.3]
+- [Source: RC2.1 spec — the four deferred codec values; RC3.6 spec — awaiting_correction join; RC4.3 spec — the takeover-surface export affordance this story upgrades]
+
+## Dev Agent Record
+
+### Implementation notes (2026-08-13)
+
+- **Codec (the deferred RC2.1 land):** FIVE `reference_*` NotificationType
+  variants landed in `shared/notification.gleam` (the briefing counts the
+  RC2.1 four; `reference_awaiting_correction` joined in RC3.6 and IS emitted
+  — leaving it out keeps the dropdown decode-broken for exactly the class
+  this story fixes). Dropdown's exhaustive icon match gained the five arms.
+- **Attempt log:** new `attempt_log` payload key on `ReferenceCallDetail`
+  (server-built, AR-RC13). The builder lives in `application_detail_handler`
+  as pure fns (unit-tested): sends grouped by `at` → cadence kinds by batch
+  position with a post-correction cycle restart; lifecycle column events
+  (form_opened/corrected/taken_over/substituted/terminal); ALL timestamps
+  normalised space→T before the server-side sort (fixes the latent same-day
+  mis-order of the old client-side raw-`at` sort). `attempts` key kept
+  (RC4.1 contract + back-compat decoder default []).
+- **Expand-only migration:** `substituted_at` + `terminalized_at` on
+  `reference_call`; the five guarded terminal writers stamp `terminalized_at
+  = now()`; the substitute path stamps `substituted_at` on the NEW row via
+  `mark_substituted_reference_call.sql` (guarded, same transaction). The
+  detail read gains corrected_at/substituted_at/terminalized_at/objected_at/
+  updated_at; the terminal instant falls back
+  terminalized_at → submitted_at → objected_at → updated_at for legacy rows.
+- **Notifications:** `notify_reference_unreachable` in-app body is now the
+  §7.9 Unreachable line verbatim (was "You may want to call them yourself").
+  The five §7.9 bodies were extracted as pure builders + pinned verbatim
+  (late-completion keeps rc3-4's de-dashed rephrase). The preference gate
+  is a pure `email_allowed_for` (Realtime→True, Daily/Off→False) used by
+  both email paths, unit-tested 3×; integration tests prove the in-app row
+  lands per preference (realtime/daily/off).
+- **No-duplicate terminals:** the full-cadence walk test now pins the
+  notification TYPE (`reference_unreachable`, exactly one) and that T+144
+  adds none; the warm-handoff body is pinned verbatim in the sweep test.
+- **Client:** `view_attempt_log` renders the server-built timeline in the
+  Audit Trail's visual language (`role="list"`, `<time datetime>`) for every
+  started row (queued/skipped excluded); the export affordance moved into
+  the timeline block (any started row can export, RC4.3's takeover-surface
+  testid preserved). `export_attempt_log_text` builds the §7.6 plain text
+  (reference, timeline, outcome, signals) from the same payload event set;
+  the OQ-5 toast is verbatim ("Attempt log copied — paste it into your
+  records or a message.") and moved out of the em-dash-scanned list with a
+  comment (spec copy, excluded by construction).
+
+### Agent Model Used
+
+deepseek/deepseek-v4-flash
+
+### Perkins r1 rework (review 4928115400, sha 1a3839c — 2 blockers + 8 warnings)
+
+- **B1 (post-correction cadence restart re-fired forever):** the fold's
+  accumulator carried `#(cycle_index + 1, …)` — after the first post-
+  correction batch reset to 0, EVERY later batch still satisfied
+  `batch_index > 0` and restarted again; post-correction co_nudge + both
+  reminders all rendered as "Invitation sent" with empty ordinals. The
+  accumulator now carries a latched `restarted` flag: only the FIRST batch
+  strictly after `corrected_at` resets to 0, later batches continue the
+  fresh cycle. The restart test now feeds ≥2 post-correction batches and
+  pins co_nudge + reminder 1 + reminder 2 ordinals.
+- **B2 (test gate):** the one-batch restart test let the B1 defect through
+  (P1 <80%). The OQ-5 export toast is now pinned twice: the const verbatim
+  (copy_test) AND the firing arm end to end (client_test fires
+  `AppCompletedRefcheckExport(Ok)` and asserts the toast message). All five
+  terminal writers' `terminalized_at` stamps now have integration
+  assertions (complete, terminalize refused, terminalize objected, exhaust,
+  sweep_terminal, sweep_mark_failed).
+- W1: timeline grouping is kind-aware — a lifecycle line sharing its `at`
+  with a send batch is never swallowed (legacy unreachable taken over:
+  terminal at = updated_at = taken_over_at, one now()). Restructured to
+  group-then-map (`SendBatch`/`Single`), with a boundary test.
+- W2: the legacy terminal fallback skips `updated_at` when the row was
+  taken over (the takeover bumps it post-terminal; the terminal entry is
+  omitted rather than faked at the takeover instant).
+- W3: `failed` + v2 `completed` got explicit timeline-terminal AND export-
+  outcome labels ("Check couldn't run" / "Reference received") — no more
+  timeline "Closed" vs export "In progress" contradiction.
+- W4: a taken-over QUEUED row keeps the export affordance (the log block is
+  gated on the takeover event, not the queued status — §7.7 contract).
+- W5: the nine new implementer-authored consts joined the em-dash scan list
+  + the fn-built timeline/export labels are scanned by status (spec-verbatim
+  "Closed — no reply" arm excluded by the helper).
+- W6: the builder passes the attempt's OWN detail through for co_nudge
+  (the sweep's skip reason), and the client's nudge line only joins
+  " — detail" when the reason is non-empty — no dangling join.
+- W7/W8: OQ-5 toast pinned at const + firing arm; terminalized_at
+  integration pins for all five writers.
+- Notes: removed the unused `gleam/result` import; sprint-status YAML
+  updated (rc4-1/2/3 done); label-table consistency test added.
diff --git a/_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml b/_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml
index a27460fb..d8e140dc 100644
--- a/_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml
+++ b/_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml
@@ -82,10 +82,10 @@ development_status:
 
   # Epic RC4: Landlord Reference Panel & Workflow
   epic-rc4: in-progress
-  rc4-1-detail-payload-extension-backend-contract: review
-  rc4-2-reference-panel-status-summary: backlog
-  rc4-3-row-actions-start-skip-take-over-correct-substitute: backlog
-  rc4-4-attempt-log-export-notification-completeness: backlog
+  rc4-1-detail-payload-extension-backend-contract: done
+  rc4-2-reference-panel-status-summary: done
+  rc4-3-row-actions-start-skip-take-over-correct-substitute: done
+  rc4-4-attempt-log-export-notification-completeness: in-progress
   epic-rc4-retrospective: optional
 
   # Epic RC5: Manual Channel & Launch Hardening
diff --git a/client/src/client.gleam b/client/src/client.gleam
index 40598ef9..2f05d951 100644
--- a/client/src/client.gleam
+++ b/client/src/client.gleam
@@ -6857,27 +6857,12 @@ fn save_refcheck_edit(
   }
 }
 
-/// The plain-text attempt-log export (the takeover surface's affordance).
-/// RC4.4 owns the full timeline + the verbatim OQ-5 toast; this is the
-/// honest v1 text: the reference, each attempt line, and the current state.
+/// The plain-text attempt-log export (the §7.6 timeline block's affordance).
+/// RC4.4: the full record — reference, timeline, outcome, signals — built
+/// from the server-shipped `attempt_log` by the panel (the same event set
+/// the screen renders), with the verbatim OQ-5 toast on success.
 fn build_attempt_log_text(call: reference_call.ReferenceCallDetail) -> String {
-  let name = reference_panel.effective_name_value(call)
-  let status = reference_call.encode_status(call.status)
-  let lines =
-    call.attempts
-    |> list.map(fn(attempt) {
-      attempt.at
-      <> " - "
-      <> attempt.channel
-      <> " - "
-      <> attempt.outcome
-      <> case attempt.detail {
-        "" -> ""
-        detail -> " (" <> detail <> ")"
-      }
-    })
-    |> string.join("\n")
-  "Reference: " <> name <> "\n" <> "State: " <> status <> "\n" <> lines
+  reference_panel.export_attempt_log_text(call)
 }
 
 fn copy_refcheck_export_effect(call_id: String, text: String) -> Effect(Msg) {
diff --git a/client/src/components/notification_dropdown.gleam b/client/src/components/notification_dropdown.gleam
index 321bec2c..af3b0478 100644
--- a/client/src/components/notification_dropdown.gleam
+++ b/client/src/components/notification_dropdown.gleam
@@ -12,7 +12,9 @@ import model.{type Model}
 import msg.{type Msg}
 import shared/notification.{
   type Notification, AiComplete, BatchComplete, NewApplication, PaymentConfirmed,
-  VacancyClosed, VacancyClosing, VacancyExtended,
+  ReferenceAwaitingCorrection, ReferenceCompleted, ReferenceDeclined,
+  ReferenceObjected, ReferenceUnreachable, VacancyClosed, VacancyClosing,
+  VacancyExtended,
 }
 import shared/remote_data.{Failure, Loading, NotAsked, Success}
 
@@ -211,6 +213,18 @@ fn view_type_icon(
       )
     VacancyClosing | VacancyClosed | VacancyExtended ->
       view_mini_icon("M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z")
+    // Reference-check events (RC2.1 types — codec landed in RC4.4). A
+    // chat-bubble icon for the reference family: these all tell the landlord
+    // something about a referee's check, distinct from vacancy/application
+    // events.
+    ReferenceCompleted
+    | ReferenceUnreachable
+    | ReferenceObjected
+    | ReferenceDeclined
+    | ReferenceAwaitingCorrection ->
+      view_mini_icon(
+        "M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.76 9.76 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z",
+      )
   }
 }
 
diff --git a/client/src/components/reference_panel.gleam b/client/src/components/reference_panel.gleam
index cd9b3502..638c25e9 100644
--- a/client/src/components/reference_panel.gleam
+++ b/client/src/components/reference_panel.gleam
@@ -40,10 +40,11 @@ import model.{
 import msg.{type Msg}
 import shared/application.{type Application}
 import shared/reference_call.{
-  type ReferenceCallAttempt, type ReferenceCallDetail, type ReferenceCallStatus,
-  AwaitingCorrection, Calling, CharacterRef, Completed, ContactInitiated,
-  EmployerRef, Failed, FormCompleted, LandlordRef, ManualRecorded, Objected,
-  Partial, Queued, Refused, Scheduled, Skipped, Unreachable,
+  type AttemptLogEntry, type ReferenceCallAttempt, type ReferenceCallDetail,
+  type ReferenceCallStatus, AwaitingCorrection, Calling, CharacterRef, Completed,
+  ContactInitiated, EmployerRef, Failed, FormCompleted, LandlordRef,
+  ManualRecorded, Objected, Partial, Queued, Refused, Scheduled, Skipped,
+  Unreachable,
 }
 
 // -- Public API ---------------------------------------------------------------
@@ -601,7 +602,7 @@ fn row_detail(
 ) -> Element(Msg) {
   let first_name = app.first_name
   let slot = reference_call.encode_ref_slot(call.ref_slot)
-  case call.status {
+  let body = case call.status {
     Queued ->
       html.div([class("space-y-3")], [
         html.p([class("text-sm text-slate leading-relaxed")], [
@@ -674,25 +675,41 @@ fn row_detail(
         html.text(copy.refcheck_state_failed(first_name)),
       ])
     ContactInitiated ->
-      html.div([class("space-y-3")], [
-        view_attempt_summary(call),
-        case
-          pending_confirm(
-            call.reference_call_id,
-            RefcheckConfirmTakeOver,
-            confirm,
-          )
-        {
-          True -> view_take_over_confirm(call, app, slot, inflight)
-          False -> element.none()
-        },
-      ])
+      case
+        pending_confirm(
+          call.reference_call_id,
+          RefcheckConfirmTakeOver,
+          confirm,
+        )
+      {
+        True -> view_take_over_confirm(call, app, slot, inflight)
+        False -> element.none()
+      }
     FormCompleted | ManualRecorded | Partial | Completed ->
       view_completed(call, app)
     // v2-reserved pre-result voice states: nothing to show until a result
     // exists (the pill carries the state).
     Scheduled | Calling -> element.none()
   }
+  // RC4.4: the §7.6 attempt log renders for every STARTED row (the AC's
+  // Given) — the timeline block appears under whatever state body the row
+  // shows, whenever the payload carries events. Queued/Skipped rows never
+  // started (nothing was sent), so they never render the log even if a
+  // fixture carries stray attempts — EXCEPT a taken-over queued row: the
+  // landlord's takeover IS an event (the server ships it in the log), and
+  // §7.7's export-beside-the-chips contract needs the affordance there
+  // (W4 — RC4.3 regression guard).
+  let attempt_log = case call.status, list.is_empty(call.attempt_log) {
+    Skipped, _ -> element.none()
+    Queued, _ ->
+      case taken_over(call) {
+        True -> view_attempt_log(call, slot)
+        False -> element.none()
+      }
+    _, True -> element.none()
+    _, False -> view_attempt_log(call, slot)
+  }
+  html.div([class("space-y-3")], [body, attempt_log])
 }
 
 /// Whether the pending inline confirm targets this call + kind.
@@ -1211,9 +1228,10 @@ fn view_applicant_chips(app: Application) -> Element(Msg) {
 
 // -- RC4.3 taken-over surface (A7 / §7.7) ------------------------------------
 
-/// The post-takeover block: the referee's effective-contact chips + the
-/// attempt-log export affordance, per §7.7 ("the referee's contact chips
-/// render inline, and the attempt-log export sits beside them").
+/// The post-takeover block: the referee's effective-contact chips. The
+/// attempt-log export affordance moved into the §7.6 timeline block (RC4.4)
+/// so ANY started row can export — this surface keeps the chips + label
+/// only, and the timeline renders directly below it in the expanded row.
 fn view_taken_over_surface(
   call: ReferenceCallDetail,
   slot: String,
@@ -1242,6 +1260,35 @@ fn view_taken_over_surface(
           )
         _ -> element.none()
       },
+    ]),
+  ])
+}
+
+// -- The §7.6 attempt log (server-built timeline, RC4.4) ----------------------
+
+/// The §7.6 attempt log: renders the SERVER-BUILT `attempt_log` timeline in
+/// the Audit Trail's visual language (`role="list"`, `<time datetime>`) —
+/// AR-RC13: the payload owns the event set and ordering; this renders
+/// labels only, never re-derives what happened. Rendered for any row whose
+/// `attempt_log` is non-empty (a started row — the AC's Given), with the
+/// export affordance in the block header (§7.6 "Export attempt log").
+fn view_attempt_log(call: ReferenceCallDetail, slot: String) -> Element(Msg) {
+  let lines = attempt_log_lines(call)
+  // The cadence hint: an in-flight row still has steps to come (the old
+  // mini-timeline pinned batch-count < 4 — the server-built log counts the
+  // same way: the cadence runs at most 4 batches).
+  let has_next_reminder = case call.status {
+    ContactInitiated -> list.length(send_batches(call.attempt_log)) < 4
+    _ -> False
+  }
+  html.div([class("space-y-2")], [
+    html.div([class("flex items-center justify-between gap-2")], [
+      html.p(
+        [class("text-[10px] font-bold uppercase tracking-widest text-slate")],
+        [
+          html.text(copy.refcheck_attempt_log_title),
+        ],
+      ),
       html.button(
         [
           attribute("data-testid", "refcheck-export-" <> slot),
@@ -1254,37 +1301,6 @@ fn view_taken_over_surface(
         [html.text(copy.refcheck_export_log)],
       ),
     ]),
-  ])
-}
-
-// -- Mini timeline (in-flight rows) -------------------------------------------
-
-/// What has happened so far (§7.4): the attempt batches (invite, co-nudge,
-/// reminders) rendered as a mini timeline, plus "what happens next" while a
-/// reminder is still pending. The attempts log is the payload's record of
-/// sends; batch positions are the cadence steps (batch 1 = invitation,
-/// batch 2 = the applicant co-nudge, batches 3+ = reminders).
-fn view_attempt_summary(call: ReferenceCallDetail) -> Element(Msg) {
-  let batches = group_by_at(call.attempts)
-  let batch_lines =
-    batches
-    |> list.index_map(fn(batch, i) { batch_line(i, batch) })
-  let lines =
-    case call.form_opened_at {
-      None -> batch_lines
-      Some(ts) -> [
-        TimelineLine(copy.refcheck_timeline_form_opened, ts),
-        ..batch_lines
-      ]
-    }
-    // Chronological by timestamp — the form can open AFTER a reminder (the
-    // link stays live), so the pinned-after-invite placement was wrong
-    // (rc4-2 Perkins r1 W4). All `at` values are UTC ISO strings (RFC3339
-    // from the sweep, PG `::text` for form_opened_at) — lexical sort is
-    // chronological.
-    |> list.sort(fn(a, b) { string.compare(a.at, b.at) })
-  let has_next_reminder = list.length(batches) < 4
-  html.div([class("space-y-2")], [
     keyed.ul(
       [attribute("role", "list"), class("space-y-1.5")],
       list.map(lines, fn(line) {
@@ -1306,9 +1322,8 @@ fn view_attempt_summary(call: ReferenceCallDetail) -> Element(Msg) {
               ]),
               html.time(
                 [
-                  // PG `::text` renders "2026-08-01 21:12:00+00" (space
-                  // separator — not valid HTML datetime); normalize to the
-                  // RFC3339 "T" separator (rc4-2 Perkins r1 N2).
+                  // Server timestamps are RFC3339 ("T" separator); the
+                  // normalize is a back-compat no-op for older payloads.
                   attribute("datetime", normalize_datetime(line.at)),
                   class("text-xs text-slate flex-shrink-0"),
                 ],
@@ -1340,14 +1355,110 @@ fn normalize_datetime(at: String) -> String {
   string.replace(at, " ", "T")
 }
 
-/// Label one attempt batch. Batch 1 is the invitation; batch 2 is the
-/// applicant co-nudge (single email — delivered, skipped on gate, or failed);
-/// batches 3+ are reminders. Channel names join into the "email + SMS" style.
-fn batch_line(
-  index: Int,
-  batch: #(String, List(ReferenceCallAttempt)),
+/// Map the server-built attempt-log entries to display lines. Send entries
+/// (invitation/co_nudge/reminder) group by `at` for the "email + SMS"
+/// channel join (one sweep step stamps one `at` for all its channels);
+/// lifecycle entries (form_opened/corrected/taken_over/substituted/terminal)
+/// render singly. The server owns the ORDER — no client sort (AR-RC13; the
+/// old client-side raw-`at` sort mis-ordered same-day PG-vs-RFC3339 stamps).
+fn attempt_log_lines(call: ReferenceCallDetail) -> List(TimelineLine) {
+  call.attempt_log
+  // Group FIRST, map AFTER: consecutive same-`at` SEND entries merge into
+  // one batch line; lifecycle/terminal entries pass through singly. The old
+  // post-map collapse was kind-blind — a terminal line sharing its `at`
+  // with a taken-over line (legacy unreachable taken over: terminal falls
+  // back to updated_at == taken_over_at, one now()) got dropped from the
+  // timeline AND the export (W1).
+  |> group_timeline_entries
+  |> list.map(fn(item) {
+    case item {
+      SendBatch(entries) -> send_batch_line(entries)
+      Single(entry) -> lifecycle_line(call, entry)
+    }
+  })
+}
+
+/// One timeline unit: a merged send batch (all entries share `at` + kind)
+/// or a single lifecycle/terminal entry.
+type TimelineItem {
+  SendBatch(List(AttemptLogEntry))
+  Single(AttemptLogEntry)
+}
+
+fn is_send_kind(kind: String) -> Bool {
+  kind == "invitation_sent" || kind == "co_nudge" || kind == "reminder_sent"
+}
+
+/// Group consecutive same-`at` send entries into a SendBatch (the per-
+/// channel wire shape); anything else becomes a Single. Lifecycle entries
+/// NEVER merge with sends even on an `at` collision (W1).
+fn group_timeline_entries(entries: List(AttemptLogEntry)) -> List(TimelineItem) {
+  entries
+  |> list.fold([], fn(acc: List(TimelineItem), entry: AttemptLogEntry) {
+    // A send entry either starts a batch or joins the batch at its head
+    // (same kind + same at); lifecycle entries are always Single. The first
+    // send entry must START a SendBatch — never land as a Single (the
+    // batch would never form).
+    case acc {
+      [SendBatch(batch), ..rest] ->
+        case
+          is_send_kind(entry.kind),
+          is_send_kind(first_kind(batch)),
+          first_at(batch) == entry.at
+        {
+          True, True, True -> [SendBatch(list.append(batch, [entry])), ..rest]
+          _, _, _ ->
+            case is_send_kind(entry.kind) {
+              True -> [SendBatch([entry]), ..acc]
+              False -> [Single(entry), ..acc]
+            }
+        }
+      _ ->
+        case is_send_kind(entry.kind) {
+          True -> [SendBatch([entry]), ..acc]
+          False -> [Single(entry), ..acc]
+        }
+    }
+  })
+  |> list.reverse
+}
+
+fn first_kind(entries: List(AttemptLogEntry)) -> String {
+  case entries {
+    [first, ..] -> first.kind
+    [] -> ""
+  }
+}
+
+fn first_at(entries: List(AttemptLogEntry)) -> String {
+  case entries {
+    [first, ..] -> first.at
+    [] -> ""
+  }
+}
+
+/// One lifecycle/terminal line — label per kind, timestamps pass through.
+fn lifecycle_line(
+  call: ReferenceCallDetail,
+  entry: AttemptLogEntry,
 ) -> TimelineLine {
-  let #(at, entries) = batch
+  let label = case entry.kind {
+    "form_opened" -> copy.refcheck_timeline_form_opened
+    "corrected" -> copy.refcheck_timeline_corrected
+    "taken_over" -> copy.refcheck_timeline_taken_over
+    "substituted" -> copy.refcheck_timeline_substituted
+    "terminal" ->
+      copy.refcheck_timeline_terminal(reference_call.encode_status(call.status))
+    // Unknown future kinds degrade to the raw kind, never a fabricated
+    // label (honest-forward-compat: the payload is the source of truth).
+    other -> other
+  }
+  TimelineLine(label, entry.at)
+}
+
+/// Build the channel-joined line for one send batch: "Invitation sent —
+/// email + SMS". All entries in the batch share `at` + kind.
+fn send_batch_line(entries: List(AttemptLogEntry)) -> TimelineLine {
   let channels =
     entries
     |> list.map(fn(e) {
@@ -1358,21 +1469,67 @@ fn batch_line(
     })
     |> dedupe_keep_order
     |> string.join(" + ")
-  let label = case index {
-    0 -> copy.refcheck_timeline_invitation
-    1 -> nudge_label(entries)
-    n -> copy.refcheck_timeline_reminder(n - 1)
+  let label = case first_kind(entries) {
+    "invitation_sent" -> copy.refcheck_timeline_invitation
+    "co_nudge" -> nudge_label(entries)
+    "reminder_sent" -> reminder_label(first_or_empty(entries))
+    other -> other
+  }
+  TimelineLine(label <> " — " <> channels, first_at(entries))
+}
+
+fn first_or_empty(entries: List(AttemptLogEntry)) -> AttemptLogEntry {
+  case entries {
+    [first, ..] -> first
+    [] ->
+      reference_call.AttemptLogEntry(
+        kind: "",
+        at: "",
+        channel: "",
+        outcome: "",
+        detail: "",
+      )
+  }
+}
+
+/// "Reminder N sent" — the server ships the cadence ordinal ("1", "2") in
+/// the entry `detail`; a malformed/absent ordinal falls back to 1 (the
+/// server always stamps it; the fallback keeps rendering total).
+fn reminder_label(entry: AttemptLogEntry) -> String {
+  case int.parse(entry.detail) {
+    Ok(n) -> copy.refcheck_timeline_reminder(n)
+    Error(_) -> copy.refcheck_timeline_reminder(1)
   }
-  TimelineLine(label <> " — " <> channels, at)
 }
 
-fn nudge_label(entries: List(ReferenceCallAttempt)) -> String {
+/// Collapse consecutive same-`at` send lines into one (the per-entry wire
+/// shape emits one line per channel; the display shows one joined batch
+/// line per `at`). Lifecycle lines pass through untouched.
+/// Send-batch `at` values (the cadence hint counts batches, not channels).
+fn send_batches(entries: List(AttemptLogEntry)) -> List(String) {
+  entries
+  |> list.filter(fn(e) {
+    e.kind == "invitation_sent"
+    || e.kind == "co_nudge"
+    || e.kind == "reminder_sent"
+  })
+  |> list.map(fn(e) { e.at })
+  |> dedupe_keep_order
+}
+
+fn nudge_label(entries: List(AttemptLogEntry)) -> String {
   case list.all(entries, fn(e) { e.outcome == "delivered" }) {
     True -> copy.refcheck_timeline_nudge
     False ->
       case list.find(entries, fn(e) { e.outcome == "skipped" }) {
         Ok(skipped) ->
-          copy.refcheck_timeline_nudge_skipped <> " — " <> skipped.detail
+          // W6: join the skip reason ONLY when the server shipped one — a
+          // bare "Applicant nudge skipped" is honest, a dangling " — " is
+          // not.
+          case skipped.detail {
+            "" -> copy.refcheck_timeline_nudge_skipped
+            detail -> copy.refcheck_timeline_nudge_skipped <> " — " <> detail
+          }
         Error(_) -> copy.refcheck_timeline_nudge_failed
       }
   }
@@ -1391,7 +1548,9 @@ fn dedupe_keep_order(items: List(String)) -> List(String) {
 
 /// Group the append-only attempts log into cadence batches by shared `at`
 /// (one sweep step stamps one timestamp for all its channel entries),
-/// preserving chronological order.
+/// preserving chronological order. Still used by the pill-label batch
+/// counting (in_flight_label / last_batch_at) — the TIMELINE itself renders
+/// the server-built `attempt_log` and never groups client-side (AR-RC13).
 fn group_by_at(
   attempts: List(ReferenceCallAttempt),
 ) -> List(#(String, List(ReferenceCallAttempt))) {
@@ -1413,6 +1572,59 @@ fn group_by_at(
   })
 }
 
+/// The §7.6 plain-text export: reference, timeline, outcome, signals — the
+/// AC's exact content list, clipboard-only in v1 (OQ-5). Same event set as
+/// the rendered timeline (the payload `attempt_log`), so the record and the
+/// screen never disagree.
+pub fn export_attempt_log_text(call: ReferenceCallDetail) -> String {
+  let reference = effective_name_value(call)
+  let status = reference_call.encode_status(call.status)
+  let timeline =
+    attempt_log_lines(call)
+    |> list.map(fn(line) {
+      "- "
+      <> line.label
+      <> " ("
+      <> format.format_timestamp_short(timestamp: line.at)
+      <> ")"
+    })
+    |> string.join("\n")
+  let signals = export_signals(call)
+  copy.refcheck_export_reference
+  <> ": "
+  <> reference
+  <> "\n"
+  <> copy.refcheck_export_outcome_label
+  <> ": "
+  <> copy.refcheck_export_outcome(status)
+  <> "\n"
+  <> copy.refcheck_export_signals_label
+  <> ": "
+  <> signals
+  <> "\n"
+  <> copy.refcheck_export_timeline_label
+  <> ":\n"
+  <> timeline
+}
+
+/// The "signals" section of the export: the worth-knowing fraud-signal lines
+/// from the stored result, or "None recorded" when the row has no result /
+/// no signals (honest — never a fabricated signal, AD-10).
+fn export_signals(call: ReferenceCallDetail) -> String {
+  case call.result {
+    None -> copy.refcheck_export_signals_none
+    Some(text) ->
+      case json.parse(text, parsed_result_decoder()) {
+        Error(_) -> copy.refcheck_export_signals_none
+        Ok(parsed) ->
+          case worth_knowing_signals(parsed.fraud_signals) {
+            [] -> copy.refcheck_export_signals_none
+            lines -> string.join(lines, "; ")
+          }
+      }
+  }
+}
+
 // -- Completed / partial reference summary ------------------------------------
 
 fn view_completed(call: ReferenceCallDetail, app: Application) -> Element(Msg) {
diff --git a/client/src/copy.gleam b/client/src/copy.gleam
index aea992eb..72561654 100644
--- a/client/src/copy.gleam
+++ b/client/src/copy.gleam
@@ -889,6 +889,9 @@ pub const refcheck_edit_need_channel: String = "Add an email or phone number to
 /// surface; RC4.4 owns the full timeline + verbatim OQ-5 toast).
 pub const refcheck_export_log: String = "Export attempt log"
 
+/// The attempt-log block title (§7.6 — the expandable timeline's heading).
+pub const refcheck_attempt_log_title: String = "Attempt log"
+
 /// Success toasts (one sentence, brand voice).
 pub const refcheck_toast_started: String = "Reference started - the invite goes out now."
 
@@ -902,7 +905,7 @@ pub const refcheck_toast_corrected: String = "Details saved - the invitation is
 
 pub const refcheck_toast_substituted: String = "Referee substituted - the new invitation is on its way."
 
-pub const refcheck_toast_exported: String = "Attempt log copied"
+pub const refcheck_toast_exported: String = "Attempt log copied — paste it into your records or a message."
 
 /// The export clipboard failure (r1 N7 — a const, never an inline string).
 pub const refcheck_toast_export_failed: String = "Couldn't copy the attempt log. Try long-pressing to copy manually"
@@ -950,10 +953,71 @@ pub const refcheck_timeline_nudge_failed: String = "Applicant nudge: couldn't se
 
 pub const refcheck_timeline_form_opened: String = "Form opened"
 
+/// RC4.4 lifecycle-event labels (the server-built attempt log's non-send
+/// kinds — implementer-authored, brand voice, dash-free).
+pub const refcheck_timeline_corrected: String = "Contact details corrected"
+
+pub const refcheck_timeline_taken_over: String = "You took this over"
+
+pub const refcheck_timeline_substituted: String = "Referee substituted"
+
 pub fn refcheck_timeline_reminder(n: Int) -> String {
   "Reminder " <> int.to_string(n) <> " sent"
 }
 
+/// The terminal event's timeline label per status (§7.6's example line is
+/// "Closed — no reply" for the exhausted cadence; the others are the honest
+/// one-phrase renderings of the same terminal the state copy describes).
+pub fn refcheck_timeline_terminal(status: String) -> String {
+  case status {
+    "unreachable" -> "Closed — no reply"
+    "refused" -> "Declined to give a reference"
+    "objected" -> "Asked not to be contacted"
+    "form_completed" -> "Reference received"
+    "manual_recorded" -> "Recorded manually"
+    "partial" -> "Form left unfinished"
+    // W3: failed + v2-completed get EXPLICIT terminal labels — the old
+    // catch-all rendered "Closed" in the timeline while the export said
+    // "In progress" (contradictory for a terminal row).
+    "failed" -> "Check couldn't run"
+    "completed" -> "Reference received"
+    _ -> "Closed"
+  }
+}
+
+/// The export's "Outcome:" line — one phrase per status (the plain-text
+/// record's outcome, §7.6).
+pub fn refcheck_export_outcome(status: String) -> String {
+  case status {
+    "queued" -> "Waiting to start"
+    "skipped" -> "Skipped by the landlord"
+    "contact_initiated" -> "Invitation sent, awaiting the form"
+    "awaiting_correction" -> "Contact details need correcting"
+    "unreachable" -> "Couldn't be reached"
+    "refused" -> "Declined to give a reference"
+    "objected" -> "Asked not to be contacted"
+    "form_completed" -> "Reference received"
+    "manual_recorded" -> "Recorded manually"
+    "partial" -> "Form left unfinished"
+    // W3: terminal rows never export "In progress" — failed + v2-completed
+    // get explicit terminal outcomes matching the timeline labels.
+    "failed" -> "Check couldn't run"
+    "completed" -> "Reference received"
+    _ -> "In progress"
+  }
+}
+
+/// The export's section labels (§7.6 plain-text layout).
+pub const refcheck_export_reference: String = "Reference"
+
+pub const refcheck_export_outcome_label: String = "Outcome"
+
+pub const refcheck_export_signals_label: String = "Signals"
+
+pub const refcheck_export_signals_none: String = "None recorded"
+
+pub const refcheck_export_timeline_label: String = "Timeline"
+
 /// The channel words joined in a timeline line ("email + SMS").
 pub const refcheck_channel_email: String = "email"
 
diff --git a/client/test/client_test.gleam b/client/test/client_test.gleam
index 46d133c1..3edf90fa 100644
--- a/client/test/client_test.gleam
+++ b/client/test/client_test.gleam
@@ -4608,6 +4608,42 @@ pub fn notification_dropdown_renders_items_test() {
   html |> string.contains("notification-item-n1") |> should.be_true
 }
 
+/// RC4.4 (deferred RC2.1 codec): the five reference_* notification types
+/// render in the dropdown (the exhaustive icon match) — a regression here
+/// means an emitted reference notification fails the whole list decode.
+pub fn notification_dropdown_renders_reference_types_test() {
+  let types = [
+    notification.ReferenceCompleted,
+    notification.ReferenceUnreachable,
+    notification.ReferenceObjected,
+    notification.ReferenceDeclined,
+    notification.ReferenceAwaitingCorrection,
+  ]
+  list.each(types, fn(t) {
+    let notif =
+      notification.Notification(
+        id: "n-ref",
+        user_id: "u1",
+        notification_type: t,
+        title: "Reference event",
+        body: "Something about a referee",
+        is_read: False,
+        entity_type: option.Some("reference_call"),
+        entity_id: option.Some("rc-1"),
+        created_at: "2026-04-06 10:30:00.123456+00",
+      )
+    let m =
+      model.Model(
+        ..model.initial(),
+        show_notification_dropdown: True,
+        notifications: remote_data.Success([notif]),
+      )
+    let html =
+      notification_dropdown.view_notification_dropdown(m) |> element.to_string
+    html |> string.contains("Reference event") |> should.be_true
+  })
+}
+
 pub fn notification_unread_badge_shows_count_test() {
   let m =
     model.Model(
@@ -6160,6 +6196,7 @@ fn refcheck_call(
     corrected_phone: option.None,
     correction_cycles: 0,
     attempts: [],
+    attempt_log: [],
     result: option.None,
     display_disclaimer: option.None,
     hooks: reference_call.ReferenceCallHooks(
@@ -6660,3 +6697,26 @@ pub fn refcheck_export_handler_marks_clipboard_test() {
   let #(updated, _eff) = client.update(m, msg.UserClickedRefcheckExport("rc-1"))
   updated.clipboard_copied |> should.equal(option.Some("refcheck_export"))
 }
+
+/// W7: the export SUCCESS arm fires the verbatim OQ-5 toast — the firing
+/// path is pinned end to end (click → clipboard → toast), not just the const.
+pub fn refcheck_export_success_toasts_verbatim_oq5_test() {
+  let m =
+    refcheck_detail_model([
+      reference_call.ReferenceCallDetail(
+        ..refcheck_call("rc-1", reference_call.Queued),
+        contact_name: option.Some("Larry"),
+        contact_email: option.Some("larry@example.com"),
+      ),
+    ])
+  let #(updated, _eff) =
+    client.update(m, msg.AppCompletedRefcheckExport("rc-1", Ok(Nil)))
+  case updated.toasts {
+    [toast, ..] ->
+      toast.message
+      |> should.equal(
+        "Attempt log copied — paste it into your records or a message.",
+      )
+    [] -> panic as "export success must toast"
+  }
+}
diff --git a/client/test/components/reference_panel_test.gleam b/client/test/components/reference_panel_test.gleam
index 74a009fe..5e850f0c 100644
--- a/client/test/components/reference_panel_test.gleam
+++ b/client/test/components/reference_panel_test.gleam
@@ -9,6 +9,7 @@
 import components/reference_panel
 import copy
 import gleam/dict.{type Dict}
+import gleam/int
 import gleam/list
 import gleam/option.{type Option, None, Some}
 import gleam/set
@@ -52,6 +53,11 @@ fn row(
     corrected_phone: None,
     correction_cycles: 0,
     attempts: attempts,
+    // RC4.4: the timeline renders the SERVER-BUILT attempt_log. The fixture
+    // mirrors the server's send labeling (batch 0 = invitation, 1 = co-nudge,
+    // 2+ = reminders, ordinal in detail) so the timeline tests exercise the
+    // same payload shape production ships.
+    attempt_log: attempt_log_from(attempts),
     result: result,
     display_disclaimer: None,
     // Hooks mirror the server's terminal rule (can_record_manual =
@@ -66,6 +72,60 @@ fn row(
   )
 }
 
+/// The test-side mirror of the server's send-batch labeling: group attempts
+/// by shared `at`, label batch 0 `invitation_sent`, batch 1 `co_nudge`,
+/// batches 2+ `reminder_sent` (cadence ordinal in `detail`). One entry per
+/// attempt entry (channel passthrough), server order preserved.
+fn attempt_log_from(
+  attempts: List(ReferenceCallAttempt),
+) -> List(reference_call.AttemptLogEntry) {
+  attempts
+  |> group_attempts_by_at
+  |> list.index_map(fn(batch, i) {
+    let #(at, entries) = batch
+    let kind = case i {
+      0 -> "invitation_sent"
+      1 -> "co_nudge"
+      _ -> "reminder_sent"
+    }
+    let detail = case i {
+      n if n >= 2 -> int.to_string(n - 1)
+      _ -> ""
+    }
+    list.map(entries, fn(e) {
+      reference_call.AttemptLogEntry(
+        kind: kind,
+        at: at,
+        channel: e.channel,
+        outcome: e.outcome,
+        detail: detail,
+      )
+    })
+  })
+  |> list.flatten
+}
+
+fn group_attempts_by_at(
+  attempts: List(ReferenceCallAttempt),
+) -> List(#(String, List(ReferenceCallAttempt))) {
+  attempts
+  |> list.fold([], fn(groups, entry) {
+    case groups {
+      [] -> [#(entry.at, [entry])]
+      [#(at, entries), ..rest] if at == entry.at -> [
+        #(at, [entry, ..entries]),
+        ..rest
+      ]
+      _ -> [#(entry.at, [entry]), ..groups]
+    }
+  })
+  |> list.reverse
+  |> list.map(fn(group) {
+    let #(at, entries) = group
+    #(at, list.reverse(entries))
+  })
+}
+
 fn base_hooks() -> reference_call.ReferenceCallHooks {
   reference_call.ReferenceCallHooks(
     can_record_manual: False,
@@ -865,6 +925,9 @@ pub fn relationship_other_renders_verbatim_text_test() {
 
 /// Timeline stays chronological when the form opens after a reminder — the
 /// link stays live, so Form-opened can post-date Reminder 1 (Perkins r1 W4).
+/// RC4.4: the ORDER is the server's (the payload `attempt_log` is already
+/// sorted); the fixture feeds the entries in the server's order and the
+/// render must NOT re-sort them.
 pub fn timeline_orders_form_opened_after_reminder_test() {
   let attempts = [
     invite_attempt(),
@@ -881,6 +944,53 @@ pub fn timeline_orders_form_opened_after_reminder_test() {
     reference_call.ReferenceCallDetail(
       ..row("rc-1", ContactInitiated, None, attempts),
       form_opened_at: Some("2026-08-03T18:00:00Z"),
+      // The server's ordered log: invite, co-nudge, reminder, form-opened
+      // LAST (the form opened after the reminder). The render must keep
+      // this order untouched.
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "sms",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "co_nudge",
+          at: "2026-08-02T10:00:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "reminder_sent",
+          at: "2026-08-03T10:00:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "1",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "reminder_sent",
+          at: "2026-08-03T10:00:00Z",
+          channel: "sms",
+          outcome: "delivered",
+          detail: "1",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "form_opened",
+          at: "2026-08-03T18:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+      ],
     )
   let html =
     render(calls: [call], off: False, attestation_on_file: False, expanded: [
@@ -1358,6 +1468,24 @@ pub fn taken_over_row_shows_label_chips_and_export_test() {
     reference_call.ReferenceCallDetail(
       ..contact_row("rc-1", ContactInitiated),
       taken_over_at: Some("2026-08-03T08:00:00Z"),
+      // RC4.4: the export affordance lives in the §7.6 timeline block — the
+      // server ships a taken-over row with its takeover event in the log.
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "taken_over",
+          at: "2026-08-03T08:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+      ],
     )
   let html =
     render_with_actions(
@@ -1651,3 +1779,340 @@ pub fn enabled_confirm_omits_disabled_attribute_test() {
   |> string.contains("refcheck-confirm-start-yes-landlord_ref\" disabled")
   |> should.be_false
 }
+
+// -- RC4.4: the §7.6 attempt-log timeline + export ----------------------------
+
+/// The attempt log renders in the Audit Trail's visual language
+/// (role="list" + <time datetime>) and covers every §7.6 event class —
+/// send, form-opened, correction, takeover, substitution, terminal — from
+/// the SERVER-BUILT payload, never re-derived client-side (AR-RC13).
+pub fn attempt_log_renders_full_timeline_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..row("rc-1", Unreachable, None, []),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "sms",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "form_opened",
+          at: "2026-08-01T21:12:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "corrected",
+          at: "2026-08-02T09:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "taken_over",
+          at: "2026-08-03T08:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "substituted",
+          at: "2026-08-04T09:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "terminal",
+          at: "2026-08-05T10:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+      ],
+    )
+  let html =
+    render(calls: [call], off: False, attestation_on_file: False, expanded: [
+      "rc-1",
+    ])
+  // Audit-trail visual language: role="list" + <time datetime>.
+  html |> string.contains("role=\"list\"") |> should.be_true
+  html
+  |> string.contains("datetime=\"2026-08-01T10:04:00Z\"")
+  |> should.be_true
+  // Every §7.6 event class has its line.
+  html |> string.contains("Invitation sent") |> should.be_true
+  html |> string.contains("email + SMS") |> should.be_true
+  html |> string.contains("Form opened") |> should.be_true
+  html |> string.contains("Contact details corrected") |> should.be_true
+  html |> string.contains("You took this over") |> should.be_true
+  html |> string.contains("Referee substituted") |> should.be_true
+  // The terminal label follows §7.6's "Closed — no reply" for unreachable.
+  html |> string.contains("Closed") |> should.be_true
+  // The export affordance lives in the timeline block header.
+  html |> string.contains("refcheck-export-landlord_ref") |> should.be_true
+}
+
+/// A queued (not-started) row renders no attempt log — nothing happened yet.
+pub fn queued_row_renders_no_attempt_log_test() {
+  let html =
+    render(
+      calls: [row("rc-1", Queued, None, [])],
+      off: False,
+      attestation_on_file: False,
+      expanded: ["rc-1"],
+    )
+  html |> string.contains("refcheck-export-landlord_ref") |> should.be_false
+  html |> string.contains("Attempt log") |> should.be_false
+}
+
+/// The plain-text export carries the AC's content list — reference,
+/// timeline, outcome, signals — built from the same payload attempt_log the
+/// screen renders (the record and the screen never disagree).
+pub fn export_attempt_log_text_includes_reference_timeline_outcome_signals_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..row("rc-1", FormCompleted, Some(completed_result()), []),
+      contact_name: Some("Colm Byrne"),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "form_opened",
+          at: "2026-08-01T21:12:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "terminal",
+          at: "2026-08-02T09:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+      ],
+    )
+  let text = reference_panel.export_attempt_log_text(call)
+  text |> string.contains("Reference: Colm Byrne") |> should.be_true
+  text |> string.contains("Outcome:") |> should.be_true
+  text |> string.contains("Signals:") |> should.be_true
+  text |> string.contains("Timeline:") |> should.be_true
+  text |> string.contains("Invitation sent") |> should.be_true
+  text |> string.contains("Form opened") |> should.be_true
+  text |> string.contains("Reference received") |> should.be_true
+  // The completed result carries a fast-completion signal (95s) — the
+  // export's signals section lists it.
+  text |> string.contains("Completed unusually fast") |> should.be_true
+}
+
+/// In-flight rows with no result yet export "None recorded" for signals —
+/// honest, never a fabricated signal (AD-10).
+pub fn export_attempt_log_text_signals_none_when_no_result_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..row("rc-1", ContactInitiated, None, []),
+      contact_name: Some("Colm Byrne"),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+      ],
+    )
+  let text = reference_panel.export_attempt_log_text(call)
+  text |> string.contains("Signals: None recorded") |> should.be_true
+}
+
+// -- RC4.4 r1 rework: W1/W2/W3/W4/W6 pins -------------------------------
+
+/// W1: a lifecycle line sharing its `at` with a send batch is NEVER
+/// swallowed — the kind-aware grouping only merges SEND entries. (Legacy
+/// unreachable taken over: terminal at = updated_at = taken_over_at, one
+/// now() — both lines must render.)
+pub fn attempt_log_lifecycle_line_survives_same_at_send_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..row("rc-1", Unreachable, None, []),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "sms",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "taken_over",
+          at: "2026-08-05T10:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+        // Same instant as the takeover (legacy fallback) — must NOT vanish.
+        reference_call.AttemptLogEntry(
+          kind: "terminal",
+          at: "2026-08-05T10:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+      ],
+    )
+  let html =
+    render(calls: [call], off: False, attestation_on_file: False, expanded: [
+      "rc-1",
+    ])
+  html |> string.contains("You took this over") |> should.be_true
+  html |> string.contains("Closed") |> should.be_true
+}
+
+/// W4: a taken-over QUEUED row still gets the export affordance (§7.7's
+/// export-beside-the-chips contract) — the log block is gated on the
+/// takeover event, not the queued status.
+pub fn queued_taken_over_row_keeps_export_affordance_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..contact_row("rc-1", Queued),
+      taken_over_at: Some("2026-08-03T08:00:00Z"),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "taken_over",
+          at: "2026-08-03T08:00:00Z",
+          channel: "",
+          outcome: "",
+          detail: "",
+        ),
+      ],
+    )
+  let html =
+    render(calls: [call], off: False, attestation_on_file: False, expanded: [
+      "rc-1",
+    ])
+  html |> string.contains("refcheck-export-landlord_ref") |> should.be_true
+  html |> string.contains("You took this over") |> should.be_true
+}
+
+/// W6: a skipped co-nudge renders its skip reason (the server ships it in
+/// the attempt detail) and never a dangling \" — \" join.
+pub fn skipped_co_nudge_renders_skip_reason_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..row("rc-1", ContactInitiated, None, []),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "co_nudge",
+          at: "2026-08-02T10:00:00Z",
+          channel: "email",
+          outcome: "skipped",
+          detail: "co-nudge skipped: form already opened",
+        ),
+      ],
+    )
+  let html =
+    render(calls: [call], off: False, attestation_on_file: False, expanded: [
+      "rc-1",
+    ])
+  html
+  |> string.contains(
+    "Applicant nudge skipped — co-nudge skipped: form already opened",
+  )
+  |> should.be_true
+  // No dangling join: the label ends with the reason, not \" — \" + blank.
+  html |> string.contains("nudge skipped — —") |> should.be_false
+}
+
+/// W6: a skipped co-nudge WITHOUT a shipped reason renders the plain label
+/// — never a trailing \" — \".
+pub fn skipped_co_nudge_without_reason_no_dangling_join_test() {
+  let call =
+    reference_call.ReferenceCallDetail(
+      ..row("rc-1", ContactInitiated, None, []),
+      attempt_log: [
+        reference_call.AttemptLogEntry(
+          kind: "invitation_sent",
+          at: "2026-08-01T10:04:00Z",
+          channel: "email",
+          outcome: "delivered",
+          detail: "",
+        ),
+        reference_call.AttemptLogEntry(
+          kind: "co_nudge",
+          at: "2026-08-02T10:00:00Z",
+          channel: "email",
+          outcome: "skipped",
+          detail: "",
+        ),
+      ],
+    )
+  let html =
+    render(calls: [call], off: False, attestation_on_file: False, expanded: [
+      "rc-1",
+    ])
+  html |> string.contains("Applicant nudge skipped") |> should.be_true
+  html |> string.contains("nudge skipped — </p>") |> should.be_false
+}
+
+/// W3: the timeline terminal + export outcome label tables are consistent
+/// per status — a terminal row NEVER exports \"In progress\".
+pub fn terminal_labels_consistent_between_timeline_and_export_test() {
+  let statuses = [
+    "unreachable",
+    "refused",
+    "objected",
+    "form_completed",
+    "manual_recorded",
+    "partial",
+    "failed",
+    "completed",
+  ]
+  list.each(statuses, fn(status) {
+    let terminal = copy.refcheck_timeline_terminal(status)
+    let outcome = copy.refcheck_export_outcome(status)
+    terminal |> should.not_equal("")
+    // Same terminal phrase family — the export never says \"In progress\"
+    // for a terminal row.
+    outcome |> should.not_equal("In progress")
+  })
+  copy.refcheck_timeline_terminal("failed")
+  |> should.equal("Check couldn't run")
+  copy.refcheck_export_outcome("failed")
+  |> should.equal("Check couldn't run")
+  copy.refcheck_timeline_terminal("completed")
+  |> should.equal("Reference received")
+  copy.refcheck_export_outcome("completed")
+  |> should.equal("Reference received")
+}
diff --git a/client/test/copy_test.gleam b/client/test/copy_test.gleam
index 33970108..232fd229 100644
--- a/client/test/copy_test.gleam
+++ b/client/test/copy_test.gleam
@@ -343,11 +343,64 @@ fn refcheck_action_strings() -> List(String) {
     copy.refcheck_toast_taken_over,
     copy.refcheck_toast_corrected,
     copy.refcheck_toast_substituted,
-    copy.refcheck_toast_exported,
+    // NOTE: `refcheck_toast_exported` is deliberately ABSENT — RC4.4 made it
+    // the verbatim OQ-5 toast (§7.6: "Attempt log copied — paste it into
+    // your records or a message."), which carries a spec em-dash. Spec-
+    // verbatim copy is excluded from this scan by construction, exactly like
+    // the §7.4/§7.5/§7.8 state lines above.
     copy.refcheck_toast_export_failed,
+    // RC4.4 timeline-block + export labels (implementer-authored — must
+    // stay dash-free like the rest of this list; W5 closes the gap where
+    // the nine new consts were added to NO scan list).
+    copy.refcheck_attempt_log_title,
+    copy.refcheck_timeline_corrected,
+    copy.refcheck_timeline_taken_over,
+    copy.refcheck_timeline_substituted,
+    copy.refcheck_export_reference,
+    copy.refcheck_export_outcome_label,
+    copy.refcheck_export_signals_label,
+    copy.refcheck_export_signals_none,
+    copy.refcheck_export_timeline_label,
   ]
 }
 
+/// The fn-built timeline/export labels — scanned by status EXCEPT the
+/// spec-verbatim arm (§7.6's "Closed — no reply" line carries a spec
+/// em-dash; everything else is implementer-authored and must stay dash-free;
+/// W5).
+fn refcheck_fn_built_labels() -> List(String) {
+  let terminal_statuses = [
+    "unreachable",
+    "refused",
+    "objected",
+    "form_completed",
+    "manual_recorded",
+    "partial",
+    "failed",
+    "completed",
+  ]
+  let export_statuses = [
+    "queued",
+    "skipped",
+    "contact_initiated",
+    "awaiting_correction",
+    "unreachable",
+    "refused",
+    "objected",
+    "form_completed",
+    "manual_recorded",
+    "partial",
+    "failed",
+    "completed",
+  ]
+  list.append(
+    list.map(terminal_statuses, copy.refcheck_timeline_terminal),
+    list.map(export_statuses, copy.refcheck_export_outcome),
+  )
+  // The spec-verbatim §7.6 terminal line is the ONLY exempt arm.
+  |> list.filter(fn(s) { s != "Closed — no reply" })
+}
+
 /// Global em-dash ban (2026-08-05 user ruling): no em-dash may appear in
 /// any landlord-facing copy string. Pins the ban durably so a single
 /// reintroduced dash fails CI instead of shipping. Covers the toast/page
@@ -368,6 +421,26 @@ pub fn no_em_dash_test() {
       False -> Nil
     }
   })
+  list.each(refcheck_fn_built_labels(), fn(s) {
+    // W5: fn-built timeline/export labels scanned too (spec-verbatim
+    // "Closed — no reply" filtered out by the helper).
+    case string.contains(s, "\u{2014}") {
+      True -> panic as "em-dash in refcheck fn-built label"
+      False -> Nil
+    }
+  })
+}
+
+/// The export toast is the VERBATIM OQ-5 string (§7.6) — pinned here
+/// because it is excluded from the em-dash scan (spec copy) and nothing
+/// else locks the firing arm's exact copy (W7).
+pub fn export_toast_is_verbatim_oq5_test() {
+  copy.refcheck_toast_exported
+  |> should.equal(
+    "Attempt log copied — paste it into your records or a message.",
+  )
+  copy.refcheck_export_log
+  |> should.equal("Export attempt log")
 }
 
 /// Forbidden-word check that ignores "_<word>" substrings — those only


--- SPEC / CONTEXT ---
Read these spec files (all of them; in order of priority):
1. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/spec/original-job-briefing.md — the original job briefing (mission + requirements)
2. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/spec/epics-reference-checking-v1-2026-07-30.md — epic; story RC4.4 starts around line 692
3. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/spec/ux-reference-checking-v1-2026-07-29.md — UX spec; §7.6 attempt log, §7.9 notification copy, OQ-5 toast
4. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/spec/architecture-reference-checking-v1-2026-07-29.md — architecture (AR-RC13 one-stable-contract)
5. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/spec/perkins-briefing-r2.md — the ROUND-2 briefing; read 'CRITICAL lens-guards' and 'Round-2 mandate' sections first
6. /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/spec/prior-findings-r1.json — round-1 consolidated findings (2 blockers, 8 warnings, 13 notes); the rework in this diff claims to fix them

The repository you may read for verification is at /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-4-r2 (READ-ONLY — do not modify anything).

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

--- ROUND-2 RE-REVIEW (this diff is a fix round) ---
You are reviewing round 2 of this PR. The diff below contains the ORIGINAL work PLUS a rework commit that claims to fix round-1 review findings (commit: 'fix(refcheck): RC4.4 r1 — post-correction cadence restart latches once; lifecycle-line survival, legacy terminal fallback, label/scan/pin gaps'). Round-1 findings are in the prior-findings file listed in the spec list above — read it.

Your output must contain ONLY:
1. NEW findings — defects introduced by the rework, or things r1 never raised that this diff still gets wrong.
2. RESIDUAL findings — where the commit claims a fix but the diff/codebase shows the fix is absent, wrong, or incomplete, so the underlying r1 defect persists or a NEW defect arises. Reference the r1 finding's title in your `detail` (e.g. 'residual of r1 B1: …').

Do NOT re-emit r1 findings that the diff genuinely fixes. Do NOT re-emit unchanged r1 findings the commit does not claim to fix (the orchestrator audits carries separately) — unless the fix attempt itself introduced a new problem. Do NOT re-litigate the r1 VERIFIED-CLEAN list: AR-RC13 server-built timeline, codec completeness 5/5, expand-only migration, §7.9 verbatim bodies, preference matrix, no-duplicate-terminals pin, back-compat decode.

Verify the commit's claims against the codebase by opening the cited files in the worktree — e.g. the cadence-restart latch (application_detail_handler.gleam build_send_entries) must reset ONLY the first post-correction batch and its test must pin ≥2 post-correction batches; the OQ-5 export toast arms must be pinned to verbatim copy; 3 of 5 terminal writers' terminalized_at stamps must have integration assertions.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Write ONLY the JSON array (no prose, no markdown fencing, no preamble, no trailing text) to this exact file using your Write tool: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/architecture.c1.json
- Overwrite the file if it already exists.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not continue reviewing, do not modify anything else, do not emit further output beyond a one-line confirmation of what you wrote.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.