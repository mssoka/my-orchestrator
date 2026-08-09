You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
RightTenantry is a Gleam/Lustre monorepo (client SPA + Wisp API + shared types) for an AI-powered tenant-vetting product, in production. Key conventions:
- No JavaScript FFI in the client (approved packages only: gleam_time, plinth, rsvp, modem).
- No `let assert` in production code — use `case` with explicit error handling.
- Every outbound HTTP call in server/src must set an explicit timeout via httpc.configure() |> httpc.timeout(<ms>).
- No em-dashes in any user-facing copy (global ban, CI-guarded).
- Squirrel for type-safe SQL: queries live in server/src/<module>/sql/*.sql.
- All fallible operations return Result; messages are SubjectVerbObject; landlord-facing strings live in client/src/copy.gleam.
- The email reminder system lives in server/src/inbound_email/: a two-stage gate (stage 1 = initial doc-gathering nudge, never-reminded; stage 2 = follow-up, stage-1 series completed >= 2 days ago), per-email scoping in the inbound_email_sender_state view. Bulk remind handler: handle_remind_applicants (mark_reminders_for_vacancy + mark_followup_reminders_for_vacancy → stamp + return recipients → send via send_reminders_background → clear rejected stamps).

--- DIFF ---
diff --git a/_bmad-output/implementation-artifacts/spec-per-applicant-remind.md b/_bmad-output/implementation-artifacts/spec-per-applicant-remind.md
new file mode 100644
index 00000000..f7892708
--- /dev/null
+++ b/_bmad-output/implementation-artifacts/spec-per-applicant-remind.md
@@ -0,0 +1,104 @@
+---
+title: 'Per-applicant remind button in the Awaiting list'
+type: 'feature'
+created: '2026-08-08'
+status: 'in-progress'
+baseline_commit: 'baa3e9b748d75be8cd3544d1ab0d004a1e15071b'
+context:
+  - '{project-root}/_bmad-output/briefings/righttenantry-per-applicant-remind.md'
+---
+
+<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">
+
+## Intent
+
+**Problem:** The Awaiting section's only reminder control is the header "Send reminder to N" button, which nudges every eligible enquirer at once. The pool mixes stale invites (days old) with fresh ones (today), so a landlord can't selectively nudge one person without nagging someone just invited.
+
+**Approach:** Add a per-row "Remind" / "Follow up" button next to each enquirer, gated on that person's two-stage reminder state, coexisting with the unchanged bulk header button. A new single-applicant endpoint reuses the bulk handler's transactional stamp+send plumbing, scoped to one email — the existing two-stage gate enforces itself unchanged.
+
+## Boundaries & Constraints
+
+**Always:**
+- The single-applicant endpoint reuses the bulk handler's email-sending logic, template, validation (`valid_recipients`), background sender (`send_reminders_background`), self-heal (`handle_send_outcome`), and `clear_rejected_stamps` — no duplicated email plumbing.
+- Atomic stamp+send in one transaction (mark → validate → clear-rejected → commit), then background send; a send-time validation failure un-stamps inside the same transaction — identical discipline to the bulk handler.
+- Gate-respecting only: send the stage that is NEXT-DUE for that person. Stage 1 if any row is un-reminded; stage 2 only when the `inbound_email_sender_state` view says `stage2_due` for that email. No force-remind / bypass.
+- Owner check via `find_vacancy_for_invite` (excludes closed/archived; the owner mismatch returns 404) — server-side defence, same as bulk.
+- Bulk header button stays unchanged and coexists; per-row button is additive.
+- Run `bash run_squirrel.sh` after the SQL edits; pre-PR gate `make format && make test && make build`.
+- Brand-voice copy, no em-dashes, `data-testid` on every new control, no JS FFI, no `let assert` outside tests.
+
+**Ask First:**
+- A force-remind mode (bypass the gate, re-nudge an already-stage-1 enquirer) —Gru's lean is to defer it; implement gate-respecting and note force-remind as a follow-up option, not the default.
+
+**Never:**
+- No duplicate email-sending/template code; no new email template.
+- No change to the bulk endpoint, the bulk button's behaviour, the `inbound_email_sender_state` view, or the two-stage gate rules.
+- No per-row hard delete or status mutation beyond the reminder stamps.
+- No client-side re-implementation of the stage-2 gate (the server is the source of truth; the row's `followup_due` flag already carries the verdict).
+
+## I/O & Edge-Case Matrix
+
+| Scenario | Input / State | Expected Output / Behavior | Error Handling |
+|----------|--------------|---------------------------|----------------|
+| STAGE1_DUE | `!reminded` enquirer, POST remind-applicant | Stamps stage 1, sends, `{reminded:1, followup:0}`, 200 | Send failure → self-heal clears stamp |
+| STAGE2_DUE | reminded + `followup_due` + `!followed_up` | Stamps stage 2 (all rows of email), sends, `{reminded:0, followup:1}`, 200 | Send failure → self-heal clears stamp |
+| ALREADY_FULLY_REMINDED | `followed_up` (both stages sent) | Both per-sender marks match 0 rows, `{reminded:0, followup:0}`, 200 | N/A |
+| RE_ENQUIRED | old stage-1 ≥2d + fresh un-reminded row | Stage 1 fires (fresh row); stage 2 suppressed (`has_unreminded`) — matches bulk | N/A |
+| CLOSED_VACANCY | vacancy status=closed/archived | `find_vacancy_for_invite` returns [] → 404, nothing stamped | 404 |
+| CROSS_TENANT | landlord ≠ vacancy.user_id | 404, nothing stamped (defence-in-depth) | 404 |
+| APPLIED_SINCE_LOAD | enquirer applied after list loaded | Both marks exclude applied email (view + NOT IN application) → `{0,0}`, 200 | N/A |
+| BAD_BODY | missing/empty/malformed email | 400 BadRequest | 400 |
+
+</frozen-after-approval>
+
+## Code Map
+
+- `server/src/inbound_email/sql/mark_reminder_for_sender.sql` — NEW. Stage-1 stamp scoped to one email (`lower(sender_email)=lower($2)`), same WHERE as `mark_reminders_for_vacancy` plus the sender predicate; stamps all un-reminded rows of that email (re-enquiry).
+- `server/src/inbound_email/sql/mark_followup_for_sender.sql` — NEW. Stage-2 stamp scoped to one email, gated by `inbound_email_sender_state.stage2_due` for that sender; stamps all rows (DISTINCT-ON-latest displays the flag).
+- `server/src/inbound_email/sql.gleam` — regenerated by Squirrel; reuse existing `clear_reminder_for_sender` / `clear_followup_for_sender` (already per-sender).
+- `server/src/inbound_email/inbound_handler.gleam` — add `handle_remind_applicant` mirroring `handle_remind_applicants`: parse `{"email":_}` body, owner check, one transaction (mark_reminder_for_sender + mark_followup_for_sender + valid_recipients + clear_rejected_stamps), spawn `send_reminders_background` with the single recipient in the due stage's list, respond `{"data":{"reminded":0|1,"followup":0|1}}`.
+- `server/src/router.gleam` — route `POST ["api","v1","vacancies",id,"remind-applicant"]` → `inbound_handler.handle_remind_applicant` (kebab sibling of `remind-applicants`), beside line 518.
+- `client/src/api/vacancy_api.gleam` — add `remind_applicant(vacancy_id, email, csrf_token, on_response)` POSTing `{"email":email}`; reuse `remind_response_decoder` (`#(Int,Int)`).
+- `client/src/model.gleam` — add `reminding_applicant_email: Option(String)` beside the awaiting fields (init `None`); reuse `LoadingReminder` for the in-flight gate.
+- `client/src/msg.gleam` — add `UserClickedRemindApplicant(vacancy_id: String, email: String)` and `ApiReturnedApplicantReminder(Result(#(Int, Int), ApiError))`.
+- `client/src/client.gleam` — handler sets `loading_action: LoadingReminder` + `reminding_applicant_email`, calls `remind_applicant`; response handler mirrors the bulk (`ApiReturnedReminder`): refetch awaiting list, toast, clear `reminding_applicant_email`/`loading_action`. Disable all remind buttons while `LoadingReminder`.
+- `client/src/components/awaiting_section.gleam` — `view_row` gains a per-row button: "Remind" when `!reminded`; "Follow up" when `reminded && followup_due && !followed_up`; hidden when `followed_up`; pending row shows "Sending…". Testids `awaiting-row-remind-<email>` / `awaiting-row-followup-<email>`.
+- `client/src/copy.gleam` — add `remind_applicant_toast_copy(reminded, followup)` (singular brand-voice) + `CtxApplicantReminder` error context.
+
+## Tasks & Acceptance
+
+**Execution:**
+- [x] `server/src/inbound_email/sql/mark_reminder_for_sender.sql` + `mark_followup_for_sender.sql` — per-sender stage stamps, view-gated stage 2 — the gate reuse (same view, same rules, scoped to one email).
+- [x] `bash run_squirrel.sh` — regenerate `server/src/inbound_email/sql.gleam`; revert any whitespace churn in `ai/sql.gleam`.
+- [x] `server/src/inbound_email/inbound_handler.gleam` — `handle_remind_applicant` mirroring the bulk transaction/spawn/response; 400 on bad body.
+- [x] `server/src/router.gleam` — `POST .../remind-applicant` route.
+- [x] `client/src/api/vacancy_api.gleam` — `remind_applicant` + reused decoder.
+- [x] `client/src/model.gleam` + `msg.gleam` — `reminding_applicant_email`, two new messages.
+- [x] `client/src/client.gleam` — click + response handlers (refetch + toast + clear pending).
+- [x] `client/src/components/awaiting_section.gleam` — gated per-row button + pending state.
+- [x] `client/src/copy.gleam` — singular toast copy + error context (reused `CtxReminder` — no new context variant needed; same reminder-send domain).
+- [x] `server/test/integration/awaiting_integration_test.gleam` — single-applicant stamp+send (stage1), stage2-only-when-due, already-fully-reminded (both 0), cross-tenant 404, closed-vacancy 404, re-enquiry scoping.
+- [x] `client/test/components/awaiting_section_test.gleam` + `client/test/copy_test.gleam` — row button gating/pending + decoder reuse + singular copy matrix.
+
+**Acceptance Criteria:**
+- Given an un-reminded enquirer, when the landlord clicks the row "Remind", then stage 1 stamps+sends for that email only, the row flips to "Reminded ✓" on refetch, and no other row is stamped.
+- Given a `followup_due` enquirer, when the landlord clicks the row "Follow up", then stage 2 stamps+sends for that email, the row flips to "Followed up ✓".
+- Given a `followed_up` enquirer, then no per-row button renders; calling the endpoint anyway returns `{reminded:0, followup:0}` 200.
+- Given landlord B clicks remind-applicant on landlord A's vacancy, then 404 and nothing is stamped.
+- Given a closed vacancy, then `find_vacancy_for_invite` excludes it → 404, nothing stamped.
+- Given the bulk header button, it remains unchanged and works alongside the per-row buttons; while any remind is in flight, all remind buttons are disabled.
+
+## Design Notes
+
+**Why "call both per-sender marks in one transaction" is gate-correct.** The two-stage gate lives entirely in the `inbound_email_sender_state` view (`has_unreminded`, `stage2_due`). Scoping each mark to one email cannot send a stage the person isn't due: stage 1 matches only if the sender has an un-reminded row; stage 2 matches only if the view says `stage2_due` (series complete, ≥2 days, vacancy open). The re-enquiry edge (old stage-1 + fresh row) is handled identically to the bulk path — `has_unreminded` suppresses stage 2 until the fresh stage-1 ages. So the per-applicant path shares the EXACT gate, not a re-implementation — zero drift risk. This is the load-bearing reuse.
+
+**Response shape mirrors the bulk.** `{"data":{"reminded":0|1,"followup":0|1}}` reuses `remind_response_decoder`; exactly one stage fires at most, so at most one count is 1. Both-zero covers "already fully reminded" and the defensive "email not in pool / applied since load" cases — the client already gated the button, so a 200 (not an error) keeps the toast path simple.
+
+## Verification
+
+**Commands:**
+- `make test-db-up && bash run_squirrel.sh` — expected: SQL regenerates, `ai/sql.gleam` churn reverted.
+- `make test-server` + `make test-integration` — expected: green, including new single-applicant pins.
+- `make test-client` — expected: green, row-gating + decoder pins.
+- `make format && make build` — expected: clean.
+- `grep -rn '—' client/src server/src` (em-dash ban) — expected: no new hits in changed copy.
diff --git a/client/src/api/vacancy_api.gleam b/client/src/api/vacancy_api.gleam
index d92cc0a5..b71c966d 100644
--- a/client/src/api/vacancy_api.gleam
+++ b/client/src/api/vacancy_api.gleam
@@ -300,6 +300,28 @@ pub fn send_reminder(
   )
 }
 
+/// POST /api/v1/vacancies/:id/remind-applicant — remind ONE enquirer by
+/// email, sending only the stage that's next-due for that person (gate-
+/// respecting, same two-stage rules as the bulk endpoint). Returns the
+/// per-stage counts as #(reminded, followup) — exactly one is 1 at most,
+/// both 0 means the person is already fully reminded. Reuses the bulk's
+/// response decoder.
+pub fn remind_applicant(
+  vacancy_id: String,
+  email: String,
+  csrf_token: String,
+  on_response: fn(Result(#(Int, Int), ApiError)) -> msg,
+) -> Effect(msg) {
+  api_helpers.post_json(
+    "/api/v1/vacancies/" <> vacancy_id <> "/remind-applicant",
+    json.object([#("email", json.string(email))]),
+    csrf_token,
+    rsvp.expect_json(remind_response_decoder(), fn(result) {
+      on_response(api_error.map_rsvp(result))
+    }),
+  )
+}
+
 /// Decode the {"data": {"reminded": Int, "followup": Int}} response wrapper.
 /// `followup` is optional_field so a prior-revision server payload (no
 /// stage-2 key at all) still decodes instead of erroring the landlord's
diff --git a/client/src/client.gleam b/client/src/client.gleam
index dfa4a454..28b84d6d 100644
--- a/client/src/client.gleam
+++ b/client/src/client.gleam
@@ -56,10 +56,11 @@ import model.{
 import modem
 import msg.{
   type Msg, ApiReturnedAcceptPolicy, ApiReturnedAccountDeletion,
-  ApiReturnedApplicationDetail, ApiReturnedApplicationOpened,
-  ApiReturnedArchiveVacancy, ApiReturnedArchivedVacancies, ApiReturnedAwaiting,
-  ApiReturnedBillingHistory, ApiReturnedBulkInvite, ApiReturnedBulkReject,
-  ApiReturnedCheckoutUrl, ApiReturnedCloseVacancy, ApiReturnedComparisonDetails,
+  ApiReturnedApplicantReminder, ApiReturnedApplicationDetail,
+  ApiReturnedApplicationOpened, ApiReturnedArchiveVacancy,
+  ApiReturnedArchivedVacancies, ApiReturnedAwaiting, ApiReturnedBillingHistory,
+  ApiReturnedBulkInvite, ApiReturnedBulkReject, ApiReturnedCheckoutUrl,
+  ApiReturnedCloseVacancy, ApiReturnedComparisonDetails,
   ApiReturnedDashboardData, ApiReturnedDashboardRefresh, ApiReturnedForgot,
   ApiReturnedInvoices, ApiReturnedLeaderboard, ApiReturnedLeaderboardPage,
   ApiReturnedLeaderboardRefresh, ApiReturnedLogin, ApiReturnedLogout,
@@ -114,10 +115,10 @@ import msg.{
   UserClickedLoadMoreApplications, UserClickedLogout, UserClickedMarkAllRead,
   UserClickedMarkAllRejected, UserClickedMarkSelectedRejected,
   UserClickedNotification, UserClickedPlayLandingIntro,
-  UserClickedPublishVacancy, UserClickedResendConfirmation,
-  UserClickedRestoreVacancy, UserClickedSaveVacancyDraft,
-  UserClickedSaveVacancyDraftUpdate, UserClickedScrollTo,
-  UserClickedSendReminder, UserClickedSettingsSection,
+  UserClickedPublishVacancy, UserClickedRemindApplicant,
+  UserClickedResendConfirmation, UserClickedRestoreVacancy,
+  UserClickedSaveVacancyDraft, UserClickedSaveVacancyDraftUpdate,
+  UserClickedScrollTo, UserClickedSendReminder, UserClickedSettingsSection,
   UserClickedShowMoreAwaiting, UserClickedViewComparison, UserClosedDeleteModal,
   UserConfirmedAccountDeletion, UserConfirmedApproval,
   UserConfirmedArchiveVacancy, UserConfirmedBackwardTransition,
@@ -582,6 +583,7 @@ fn update_inner(model: Model, msg: Msg) -> #(Model, Effect(Msg)) {
             awaiting_expanded: False,
             awaiting_list: NotAsked,
             awaiting_visible_count: model.awaiting_page_size,
+            reminding_applicant_email: None,
             scoring_status: None,
             scoring_poll_count: 0,
             scoring_poll_vacancy_id: "",
@@ -2487,6 +2489,7 @@ fn update_inner(model: Model, msg: Msg) -> #(Model, Effect(Msg)) {
         awaiting_expanded: False,
         awaiting_list: NotAsked,
         awaiting_visible_count: model.awaiting_page_size,
+        reminding_applicant_email: None,
       ),
       effect.batch([
         vacancy_api.get_detail(id, ApiReturnedVacancyDetail),
@@ -2868,6 +2871,60 @@ fn update_inner(model: Model, msg: Msg) -> #(Model, Effect(Msg)) {
           )
       }
 
+    UserClickedRemindApplicant(vacancy_id, email) -> #(
+      Model(
+        ..model,
+        loading_action: Some(LoadingReminder),
+        reminding_applicant_email: Some(email),
+      ),
+      vacancy_api.remind_applicant(
+        vacancy_id,
+        email,
+        model.csrf_token,
+        ApiReturnedApplicantReminder,
+      ),
+    )
+    ApiReturnedApplicantReminder(result) ->
+      // Mirrors the bulk ApiReturnedReminder handler: on success, refetch the
+      // awaiting list so the row flips to its new stage badge and the header
+      // counts re-derive; clears the pending row marker either way.
+      case result {
+        Ok(#(reminded, followup)) -> {
+          let message = copy.remind_applicant_toast_copy(reminded, followup)
+          let #(awaiting_list, refetch) = case model.vacancy_detail {
+            Success(detail) -> #(
+              Loading,
+              vacancy_api.fetch_awaiting(detail.id, fn(result) {
+                ApiReturnedAwaiting(detail.id, result)
+              }),
+            )
+            _ -> #(model.awaiting_list, effect.none())
+          }
+          let #(m, toast_eff) =
+            add_toast(
+              Model(
+                ..model,
+                loading_action: None,
+                reminding_applicant_email: None,
+                awaiting_list:,
+              ),
+              message,
+              model.ToastSuccess,
+            )
+          #(m, effect.batch([toast_eff, refetch]))
+        }
+        Error(err) ->
+          add_toast(
+            Model(
+              ..model,
+              loading_action: None,
+              reminding_applicant_email: None,
+            ),
+            error_toast_copy(err, copy.CtxReminder),
+            model.ToastError,
+          )
+      }
+
     // -- Document URL refresh (signed URL expiry) --------------------------------
     msg.DocumentImageFailed(vacancy_id, application_id) ->
       // Re-fetch application detail to get fresh signed URLs (once per page load)
diff --git a/client/src/components/awaiting_section.gleam b/client/src/components/awaiting_section.gleam
index 895c9c5f..325ffc09 100644
--- a/client/src/components/awaiting_section.gleam
+++ b/client/src/components/awaiting_section.gleam
@@ -6,7 +6,8 @@
 
 import gleam/int
 import gleam/list
-import gleam/option.{type Option, Some}
+import gleam/option.{type Option, None, Some}
+import gleam/string
 import helpers/format
 import lustre/attribute.{attribute, class}
 import lustre/element.{type Element}
@@ -27,6 +28,7 @@ pub fn view_awaiting_section(
   awaiting_list awaiting_list: RemoteData(List(AwaitingApplicant)),
   visible_count visible_count: Int,
   loading_action loading_action: Option(LoadingAction),
+  reminding_applicant_email reminding_applicant_email: Option(String),
 ) -> Element(Msg) {
   // Prefer the freshly-loaded list's stage counts (so the button updates the
   // moment a send completes); fall back to the detail's counts so the header
@@ -59,7 +61,14 @@ pub fn view_awaiting_section(
         pending,
       ),
       case expanded {
-        True -> view_body(awaiting_list, visible_count)
+        True ->
+          view_body(
+            awaiting_list,
+            visible_count,
+            vacancy_id,
+            pending,
+            reminding_applicant_email,
+          )
         False -> element.none()
       },
     ],
@@ -120,6 +129,9 @@ fn view_header(
 fn view_body(
   awaiting_list: RemoteData(List(AwaitingApplicant)),
   visible_count: Int,
+  vacancy_id: String,
+  pending: Bool,
+  reminding_email: Option(String),
 ) -> Element(Msg) {
   html.div([class("mt-4")], [
     html.p([class("text-sm text-slate mb-3")], [
@@ -145,7 +157,9 @@ fn view_body(
               attribute("id", "awaiting-list"),
               class("divide-y divide-slate-100"),
             ],
-            list.map(visible, fn(a) { #(a.email, view_row(a)) }),
+            list.map(visible, fn(a) {
+              #(a.email, view_row(vacancy_id, a, pending, reminding_email))
+            }),
           ),
           view_show_more_button(remaining),
         ])
@@ -175,7 +189,16 @@ fn view_show_more_button(remaining: Int) -> Element(Msg) {
   }
 }
 
-fn view_row(a: AwaitingApplicant) -> Element(Msg) {
+fn view_row(
+  vacancy_id: String,
+  a: AwaitingApplicant,
+  pending: Bool,
+  reminding_email: Option(String),
+) -> Element(Msg) {
+  let row_pending = case reminding_email {
+    Some(e) -> string.lowercase(e) == string.lowercase(a.email)
+    None -> False
+  }
   html.div(
     [
       attribute("data-testid", "awaiting-row-" <> a.email),
@@ -188,17 +211,90 @@ fn view_row(a: AwaitingApplicant) -> Element(Msg) {
         ]),
         html.p([class("text-xs text-slate")], [html.text(secondary_line(a))]),
       ]),
-      case a.followed_up, a.reminded {
-        False, False ->
-          html.span([class("text-xs text-slate whitespace-nowrap")], [
-            html.text("awaiting"),
-          ])
-        _, _ ->
-          html.span(
-            [class("text-xs font-semibold text-teal whitespace-nowrap")],
-            [html.text(row_stage_label(a.followed_up, a.reminded))],
-          )
-      },
+      view_row_action(vacancy_id, a, pending, row_pending),
+    ],
+  )
+}
+
+/// The row's right-hand action: a per-applicant "Remind" / "Follow up"
+/// button when the next-due stage is sendable, otherwise the status badge
+/// (in the 2-day waiting window, or once fully followed up). Gated on the
+/// server-supplied flags alone — the client never re-derives the stage-2
+/// gate. Coexists with the header bulk button; while any remind is in
+/// flight (`pending`), every remind button is disabled to prevent a stamp
+/// race with the bulk path.
+fn view_row_action(
+  vacancy_id: String,
+  a: AwaitingApplicant,
+  pending: Bool,
+  row_pending: Bool,
+) -> Element(Msg) {
+  case a.followed_up, a.reminded, a.followup_due {
+    // Both stages sent — nothing more to send; show the badge.
+    True, _, _ -> status_span(row_stage_label(a.followed_up, a.reminded))
+    // Stage 2 due (series complete, 2-day gate passed) — offer the follow-up.
+    False, True, True ->
+      view_row_button(
+        vacancy_id,
+        a.email,
+        "Follow up",
+        "followup",
+        pending,
+        row_pending,
+      )
+    // Reminded but the 2-day window hasn't elapsed — show the badge.
+    False, True, False ->
+      status_span(row_stage_label(a.followed_up, a.reminded))
+    // Never reminded — offer stage 1.
+    False, False, _ ->
+      view_row_button(
+        vacancy_id,
+        a.email,
+        "Remind",
+        "remind",
+        pending,
+        row_pending,
+      )
+  }
+}
+
+fn status_span(label: String) -> Element(Msg) {
+  html.span([class("text-xs font-semibold text-teal whitespace-nowrap")], [
+    html.text(label),
+  ])
+}
+
+fn view_row_button(
+  vacancy_id: String,
+  email: String,
+  label: String,
+  testid_suffix: String,
+  pending: Bool,
+  row_pending: Bool,
+) -> Element(Msg) {
+  html.button(
+    [
+      attribute("data-testid", "awaiting-row-" <> testid_suffix <> "-" <> email),
+      attribute("type", "button"),
+      attribute.disabled(pending),
+      event.on_click(msg.UserClickedRemindApplicant(vacancy_id, email)),
+      class(
+        "shrink-0 px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap "
+        <> case row_pending {
+          True -> "bg-slate-100 text-slate cursor-not-allowed"
+          False ->
+            case pending {
+              True -> "bg-amber/50 text-white cursor-not-allowed"
+              False -> "bg-amber text-white hover:bg-amber/90 transition-colors"
+            }
+        },
+      ),
+    ],
+    [
+      html.text(case row_pending {
+        True -> "Sending…"
+        False -> label
+      }),
     ],
   )
 }
diff --git a/client/src/copy.gleam b/client/src/copy.gleam
index be8868f2..e0a432a5 100644
--- a/client/src/copy.gleam
+++ b/client/src/copy.gleam
@@ -492,3 +492,24 @@ pub fn reminder_toast_copy(reminded: Int, followup: Int) -> String {
       <> " more."
   }
 }
+
+/// Toast copy after a per-applicant remind. Exactly one stage can fire (the
+/// next-due one), so at most one of reminded/followup is 1; both 0 means the
+/// person was already fully reminded (a defensive/race case — the button is
+/// hidden once followed_up). The higher-count arms are unreachable for a
+/// single applicant but keep the match total. Brand voice: singular, calm.
+pub fn remind_applicant_toast_copy(reminded: Int, followup: Int) -> String {
+  case reminded, followup {
+    1, 0 -> "Reminder's on its way."
+    0, 1 -> "Follow-up's on its way."
+    0, 0 -> "They've already had both reminders."
+    n, 0 -> "Reminders on their way to " <> int.to_string(n) <> " people."
+    0, m -> "Follow-ups on their way to " <> int.to_string(m) <> " people."
+    n, m ->
+      "Reminders on their way to "
+      <> int.to_string(n)
+      <> " people, follow-ups to "
+      <> int.to_string(m)
+      <> " more."
+  }
+}
diff --git a/client/src/model.gleam b/client/src/model.gleam
index a26d5837..d9d0ee01 100644
--- a/client/src/model.gleam
+++ b/client/src/model.gleam
@@ -257,6 +257,10 @@ pub type Model {
     awaiting_expanded: Bool,
     awaiting_list: RemoteData(List(AwaitingApplicant)),
     awaiting_visible_count: Int,
+    // The enquirer whose per-row remind button is in flight (shows
+    // "Sending…" on that row + disables every remind button to prevent a
+    // stamp race with the bulk header button). Cleared on response.
+    reminding_applicant_email: Option(String),
     // Vacancy lifecycle
     confirm_action: Option(ConfirmAction),
     archived_vacancies: RemoteData(List(VacancyWithStats)),
@@ -546,6 +550,7 @@ pub fn initial() -> Model {
     awaiting_expanded: False,
     awaiting_list: NotAsked,
     awaiting_visible_count: awaiting_page_size,
+    reminding_applicant_email: None,
     confirm_action: None,
     archived_vacancies: NotAsked,
     loading_action: None,
diff --git a/client/src/msg.gleam b/client/src/msg.gleam
index bf445866..1bf153a6 100644
--- a/client/src/msg.gleam
+++ b/client/src/msg.gleam
@@ -160,6 +160,11 @@ pub type Msg {
   // #(reminded, followup) — stage-1 and stage-2 send counts. One click can
   // send both stages to disjoint pools (never-reminded vs due-a-follow-up).
   ApiReturnedReminder(Result(#(Int, Int), ApiError))
+  // Per-applicant remind: the row's enquirer email is the target. The
+  // response is the same #(reminded, followup) shape — exactly one is 1 at
+  // most (the next-due stage), both 0 means already fully reminded.
+  UserClickedRemindApplicant(vacancy_id: String, email: String)
+  ApiReturnedApplicantReminder(Result(#(Int, Int), ApiError))
   // Vacancy lifecycle — close, archive, restore
   UserClickedCloseVacancy(String)
   UserConfirmedCloseVacancy(String)
diff --git a/client/src/pages/vacancy_detail.gleam b/client/src/pages/vacancy_detail.gleam
index 079f2b81..d956a462 100644
--- a/client/src/pages/vacancy_detail.gleam
+++ b/client/src/pages/vacancy_detail.gleam
@@ -135,6 +135,7 @@ fn view_detail(v: VacancyDetail, model: Model) -> Element(Msg) {
           awaiting_list: model.awaiting_list,
           visible_count: model.awaiting_visible_count,
           loading_action: model.loading_action,
+          reminding_applicant_email: model.reminding_applicant_email,
         )
       _, _, _ -> element.none()
     },
diff --git a/client/test/components/awaiting_section_test.gleam b/client/test/components/awaiting_section_test.gleam
index 1db8ab97..dda3ddac 100644
--- a/client/test/components/awaiting_section_test.gleam
+++ b/client/test/components/awaiting_section_test.gleam
@@ -1,10 +1,18 @@
 //// Unit tests for the awaiting-section reminder button label matrix. The
 //// two-stage reminder series makes the button's copy load-bearing: the
 //// landlord must see which stages a click will send (stage-1 reminders,
-//// stage-2 follow-ups, or both) before they click it.
+//// stage-2 follow-ups, or both) before they click it. The per-row tests pin
+//// the new per-applicant button's gating matrix (which stage's button shows,
+//// when none shows, and the pending-row label).
 
 import components/awaiting_section
+import gleam/option
+import gleam/string
 import gleeunit/should
+import lustre/element
+import model
+import shared/remote_data.{Success}
+import shared/vacancy.{type AwaitingApplicant, AwaitingApplicant}
 
 pub fn label_pending_test() {
   awaiting_section.reminder_button_label(
@@ -74,3 +82,122 @@ pub fn row_stage_label_awaiting_test() {
   awaiting_section.row_stage_label(followed_up: False, reminded: False)
   |> should.equal("awaiting")
 }
+
+// -- Per-row button gating ----------------------------------------------------
+
+fn awaiting_section_html(
+  applicant: AwaitingApplicant,
+  loading_action: option.Option(model.LoadingAction),
+  reminding_email: option.Option(String),
+) -> String {
+  awaiting_section.view_awaiting_section(
+    vacancy_id: "v1",
+    awaiting_count: 1,
+    remindable_count: 1,
+    followup_count: 0,
+    expanded: True,
+    awaiting_list: Success([applicant]),
+    visible_count: 10,
+    loading_action:,
+    reminding_applicant_email: reminding_email,
+  )
+  |> element.to_string
+}
+
+/// A never-reminded enquirer gets the stage-1 "Remind" button (not follow-up).
+pub fn row_renders_remind_button_when_not_reminded_test() {
+  let html =
+    awaiting_section_html(
+      AwaitingApplicant(
+        email: "a@example.com",
+        name: option.None,
+        invited_at: "2026-01-01",
+        reminded: False,
+        followed_up: False,
+        followup_due: False,
+      ),
+      option.None,
+      option.None,
+    )
+  html
+  |> string.contains("data-testid=\"awaiting-row-remind-a@example.com\"")
+  |> should.be_true
+  html |> string.contains("Remind") |> should.be_true
+  // No follow-up button for a never-reminded enquirer.
+  html
+  |> string.contains("data-testid=\"awaiting-row-followup-a@example.com\"")
+  |> should.be_false
+}
+
+/// An enquirer whose stage-1 aged past the gate gets the stage-2 "Follow up"
+/// button (not the stage-1 remind button).
+pub fn row_renders_followup_button_when_due_test() {
+  let html =
+    awaiting_section_html(
+      AwaitingApplicant(
+        email: "b@example.com",
+        name: option.None,
+        invited_at: "2026-01-01",
+        reminded: True,
+        followed_up: False,
+        followup_due: True,
+      ),
+      option.None,
+      option.None,
+    )
+  html
+  |> string.contains("data-testid=\"awaiting-row-followup-b@example.com\"")
+  |> should.be_true
+  html |> string.contains("Follow up") |> should.be_true
+  html
+  |> string.contains("data-testid=\"awaiting-row-remind-b@example.com\"")
+  |> should.be_false
+}
+
+/// An enquirer at both stages (followed_up) shows no remind button at all —
+/// there's nothing left to send.
+pub fn row_hides_remind_button_when_followed_up_test() {
+  let html =
+    awaiting_section_html(
+      AwaitingApplicant(
+        email: "c@example.com",
+        name: option.None,
+        invited_at: "2026-01-01",
+        reminded: True,
+        followed_up: True,
+        followup_due: False,
+      ),
+      option.None,
+      option.None,
+    )
+  html
+  |> string.contains("data-testid=\"awaiting-row-remind-c@example.com\"")
+  |> should.be_false
+  html
+  |> string.contains("data-testid=\"awaiting-row-followup-c@example.com\"")
+  |> should.be_false
+  // The status badge is still there.
+  html |> string.contains("Followed up ✓") |> should.be_true
+}
+
+/// The pending row (its remind in flight) shows "Sending…" instead of the
+/// button label, so the landlord sees exactly which person is being nudged.
+pub fn row_shows_sending_label_for_pending_applicant_test() {
+  let html =
+    awaiting_section_html(
+      AwaitingApplicant(
+        email: "d@example.com",
+        name: option.None,
+        invited_at: "2026-01-01",
+        reminded: False,
+        followed_up: False,
+        followup_due: False,
+      ),
+      option.Some(model.LoadingReminder),
+      option.Some("d@example.com"),
+    )
+  html
+  |> string.contains("data-testid=\"awaiting-row-remind-d@example.com\"")
+  |> should.be_true
+  html |> string.contains("Sending…") |> should.be_true
+}
diff --git a/client/test/copy_test.gleam b/client/test/copy_test.gleam
index 14154d67..7ba8e9cf 100644
--- a/client/test/copy_test.gleam
+++ b/client/test/copy_test.gleam
@@ -519,3 +519,21 @@ pub fn reminder_toast_mixed_pool_test() {
   copy.reminder_toast_copy(2, 3)
   |> should.equal("Reminders on their way to 2 people, follow-ups to 3 more.")
 }
+
+// -- Per-applicant remind toast matrix ---------------------------------------
+// Singular brand voice: at most one stage fires for a single enquirer.
+
+pub fn remind_applicant_toast_stage1_test() {
+  copy.remind_applicant_toast_copy(1, 0)
+  |> should.equal("Reminder's on its way.")
+}
+
+pub fn remind_applicant_toast_followup_test() {
+  copy.remind_applicant_toast_copy(0, 1)
+  |> should.equal("Follow-up's on its way.")
+}
+
+pub fn remind_applicant_toast_already_fully_reminded_test() {
+  copy.remind_applicant_toast_copy(0, 0)
+  |> should.equal("They've already had both reminders.")
+}
diff --git a/server/src/inbound_email/inbound_handler.gleam b/server/src/inbound_email/inbound_handler.gleam
index 27be6fe9..f3ce5b8f 100644
--- a/server/src/inbound_email/inbound_handler.gleam
+++ b/server/src/inbound_email/inbound_handler.gleam
@@ -642,6 +642,200 @@ pub fn handle_remind_applicants(
   }
 }
 
+// -- Remind a Single Applicant -----------------------------------------------
+
+/// Handle POST /api/v1/vacancies/:id/remind-applicant
+/// Per-applicant analogue of handle_remind_applicants: remind ONE enquirer
+/// (by email), sending exactly the stage that's next-due for that person.
+/// The two-stage gate is enforced by scoping the SAME stamp+send plumbing to
+/// a single sender — stage 1 matches only if the sender has an un-reminded
+/// row, stage 2 only if inbound_email_sender_state says stage2_due — so the
+/// per-row button can never spam or skip the cadence. When both stages are
+/// already sent, neither mark matches any row and the response carries
+/// {reminded:0, followup:0} (the UI hides the button; the server is the
+/// source of truth). Same atomic stamp+send transaction, owner check, and
+/// no-remind-on-closed defence as the bulk handler.
+pub fn handle_remind_applicant(
+  req: Request,
+  config: ServerConfig,
+  landlord_id: String,
+  vacancy_id: String,
+) -> Response {
+  let db = config.db
+  let resend_api_key = config.resend_api_key
+  let origin_base = domain_helpers.build_origin_url(req, "")
+
+  use json_body <- wisp.require_json(req)
+  case decode.run(json_body, remind_applicant_body_decoder()) {
+    Error(_) ->
+      response_helpers.json_error(
+        error_code.ValidationError,
+        "Invalid request body",
+        400,
+      )
+    Ok(raw_email) -> {
+      let email = string.trim(raw_email)
+      case email {
+        "" ->
+          response_helpers.json_error(
+            error_code.ValidationError,
+            "No email provided",
+            400,
+          )
+        _ ->
+          case email_parser.is_valid_email(email) {
+            False ->
+              response_helpers.json_error(
+                error_code.ValidationError,
+                "Invalid email",
+                400,
+              )
+            True ->
+              case uuid.from_string(vacancy_id) {
+                Error(_) ->
+                  response_helpers.json_error(
+                    error_code.BadRequest,
+                    "Invalid vacancy ID",
+                    400,
+                  )
+                Ok(vacancy_uuid) ->
+                  // find_vacancy_for_invite excludes closed/archived — a
+                  // reminder never fires on a filled vacancy (server-side
+                  // defence; the UI also hides the button).
+                  case sql.find_vacancy_for_invite(db, vacancy_uuid) {
+                    Ok(pog.Returned(_, [vacancy])) ->
+                      case vacancy.user_id == landlord_id {
+                        False ->
+                          response_helpers.json_error(
+                            error_code.NotFound,
+                            "Vacancy not found",
+                            404,
+                          )
+                        True ->
+                          // Atomic one-shots, ONE transaction: stamp the
+                          // next-due stage for this sender (at most one of
+                          // the two marks can match — the gate forbids both
+                          // being due), validate, and un-stamp any address
+                          // that fails send-time validation, all before
+                          // commit. A failure rolls both marks back.
+                          case
+                            pog.transaction(db, fn(tx) {
+                              use stage1 <- result.try(
+                                sql.mark_reminder_for_sender(
+                                  tx,
+                                  vacancy_uuid,
+                                  email,
+                                ),
+                              )
+                              use stage2 <- result.try(
+                                sql.mark_followup_for_sender(
+                                  tx,
+                                  vacancy_uuid,
+                                  email,
+                                ),
+                              )
+                              let #(
+                                pog.Returned(_, stage1_rows),
+                                pog.Returned(_, stage2_rows),
+                              ) = #(stage1, stage2)
+                              let stage1_recipients =
+                                valid_recipients(
+                                  list.map(stage1_rows, fn(r) { r.sender_email }),
+                                )
+                              let stage2_recipients =
+                                valid_recipients(
+                                  list.map(stage2_rows, fn(r) { r.sender_email }),
+                                )
+                              clear_rejected_stamps(
+                                tx,
+                                vacancy_uuid,
+                                list.map(stage1_rows, fn(r) { r.sender_email }),
+                                stage1_recipients,
+                                sql.clear_reminder_for_sender,
+                              )
+                              clear_rejected_stamps(
+                                tx,
+                                vacancy_uuid,
+                                list.map(stage2_rows, fn(r) { r.sender_email }),
+                                stage2_recipients,
+                                sql.clear_followup_for_sender,
+                              )
+                              Ok(#(stage1_recipients, stage2_recipients))
+                            })
+                          {
+                            Ok(#(stage1_recipients, stage2_recipients)) -> {
+                              let application_url =
+                                origin_base <> "/apply/" <> vacancy.short_code
+                              // Fire-and-forget: the request returns
+                              // immediately; a per-send failure self-heals
+                              // (clears the stamp) so the enquirer stays
+                              // remindable on the next click.
+                              process.spawn(fn() {
+                                send_reminders_background(
+                                  db,
+                                  vacancy_uuid,
+                                  stage1_recipients,
+                                  stage2_recipients,
+                                  resend_api_key,
+                                  vacancy.property_name,
+                                  application_url,
+                                  vacancy.id,
+                                  vacancy.closes_at,
+                                )
+                              })
+                              let body =
+                                json.object([
+                                  #(
+                                    "data",
+                                    json.object([
+                                      #(
+                                        "reminded",
+                                        json.int(list.length(stage1_recipients)),
+                                      ),
+                                      #(
+                                        "followup",
+                                        json.int(list.length(stage2_recipients)),
+                                      ),
+                                    ]),
+                                  ),
+                                ])
+                                |> json.to_string
+                              wisp.json_response(body, 200)
+                            }
+                            _ ->
+                              response_helpers.json_error(
+                                error_code.InternalError,
+                                "Failed to send reminder",
+                                500,
+                              )
+                          }
+                      }
+                    Ok(pog.Returned(_, [])) ->
+                      response_helpers.json_error(
+                        error_code.NotFound,
+                        "Vacancy not found",
+                        404,
+                      )
+                    _ ->
+                      response_helpers.json_error(
+                        error_code.InternalError,
+                        "Failed to look up vacancy",
+                        500,
+                      )
+                  }
+              }
+          }
+      }
+    }
+  }
+}
+
+/// Decode {"email": "..."} for the single-applicant remind endpoint.
+fn remind_applicant_body_decoder() -> decode.Decoder(String) {
+  use email <- decode.field("email", decode.string)
+  decode.success(email)
+}
+
 /// Validate, case-fold and dedupe a marked row set into sendable recipients.
 /// Mirrors the validation comment at the call site: inbound-store validation
 /// keeps this a defence-in-depth filter, but legacy rows can still fail it.
diff --git a/server/src/inbound_email/sql.gleam b/server/src/inbound_email/sql.gleam
index 5633f119..d4fb465f 100644
--- a/server/src/inbound_email/sql.gleam
+++ b/server/src/inbound_email/sql.gleam
@@ -46,12 +46,13 @@ WHERE vacancy_id = $1
 /// - clear_reminder_for_sender(vacancy_id: UUID, sender_email: TEXT)
 /// - Revert a reminder stamp when the send failed, so the enquirer stays
 /// - remindable on the next attempt (self-healing). Case-folded match. Scoped
-/// - to stamps minted in the last hour: comfortably past the worst-case send-queue runtime (batches of 5
-/// - with 1.1s pauses at Resend's 5 req/s cap), while still scoping the clear
-/// - to the failed attempt's own stamps — nulling OLDER rows would re-arm
-/// - duplicate stage-1s for enquirers successfully reminded in earlier clicks
-/// - (and, after a stage-2, manufacture the reminder-less-but-followed-up
-/// - half-state). The handler logs when a clear matches zero rows.
+/// - to stamps minted in the last hour: comfortably past the worst-case
+/// - send-queue runtime (batches of 5 with 1.1s pauses at Resend's 5 req/s
+/// - cap), while still scoping the clear to the failed attempt's own stamps —
+/// - nulling OLDER rows would re-arm duplicate stage-1s for enquirers
+/// - successfully reminded in earlier clicks (and, after a stage-2,
+/// - manufacture the reminder-less-but-followed-up half-state). The handler
+/// - logs when a clear matches zero rows.
 ///
 /// > 🐿️ This function was generated automatically using v4.6.0 of
 /// > the [squirrel package](https://github.com/giacomocavalieri/squirrel).
@@ -66,12 +67,13 @@ pub fn clear_reminder_for_sender(
   "--- clear_reminder_for_sender(vacancy_id: UUID, sender_email: TEXT)
 --- Revert a reminder stamp when the send failed, so the enquirer stays
 --- remindable on the next attempt (self-healing). Case-folded match. Scoped
---- to stamps minted in the last hour: comfortably past the worst-case send-queue runtime (batches of 5
---- with 1.1s pauses at Resend's 5 req/s cap), while still scoping the clear
---- to the failed attempt's own stamps — nulling OLDER rows would re-arm
---- duplicate stage-1s for enquirers successfully reminded in earlier clicks
---- (and, after a stage-2, manufacture the reminder-less-but-followed-up
---- half-state). The handler logs when a clear matches zero rows.
+--- to stamps minted in the last hour: comfortably past the worst-case
+--- send-queue runtime (batches of 5 with 1.1s pauses at Resend's 5 req/s
+--- cap), while still scoping the clear to the failed attempt's own stamps —
+--- nulling OLDER rows would re-arm duplicate stage-1s for enquirers
+--- successfully reminded in earlier clicks (and, after a stage-2,
+--- manufacture the reminder-less-but-followed-up half-state). The handler
+--- logs when a clear matches zero rows.
 UPDATE inbound_email
 SET reminder_sent_at = NULL
 WHERE vacancy_id = $1
@@ -251,6 +253,78 @@ WHERE v.id = $1
   |> pog.execute(db)
 }
 
+/// A row you get from running the `mark_followup_for_sender` query
+/// defined in `./src/inbound_email/sql/mark_followup_for_sender.sql`.
+///
+/// > 🐿️ This type definition was generated automatically using v4.6.0 of the
+/// > [squirrel package](https://github.com/giacomocavalieri/squirrel).
+///
+pub type MarkFollowupForSenderRow {
+  MarkFollowupForSenderRow(
+    sender_email: Option(String),
+    sender_name: Option(String),
+  )
+}
+
+/// - mark_followup_for_sender(vacancy_id: UUID, sender_email: TEXT)
+/// - Atomically stamp second_reminder_sent_at for ONE enquirer and return the
+/// - stamped rows. The per-applicant analogue of mark_followup_reminders_for_
+/// - vacancy: eligibility is still the view's stage2_due column
+/// - (inbound_email_sender_state is the single home of the rule), now scoped
+/// - to one sender — so the per-row "Follow up" button fires stage 2 only for
+/// - the person whose series is complete and aged past the 2-day gate. All of
+/// - the sender's rows are stamped so the DISTINCT-ON-latest awaiting list
+/// - always displays the flag. Consuming the one-shot in the same statement
+/// - makes a double-click safe: the second call matches zero rows. Recipients
+/// - are deduped (case-folded) and validated in Gleam before send.
+///
+/// > 🐿️ This function was generated automatically using v4.6.0 of
+/// > the [squirrel package](https://github.com/giacomocavalieri/squirrel).
+///
+pub fn mark_followup_for_sender(
+  db: pog.Connection,
+  arg_1: Uuid,
+  arg_2: String,
+) -> Result(pog.Returned(MarkFollowupForSenderRow), pog.QueryError) {
+  let decoder = {
+    use sender_email <- decode.field(0, decode.optional(decode.string))
+    use sender_name <- decode.field(1, decode.optional(decode.string))
+    decode.success(MarkFollowupForSenderRow(sender_email:, sender_name:))
+  }
+
+  "--- mark_followup_for_sender(vacancy_id: UUID, sender_email: TEXT)
+--- Atomically stamp second_reminder_sent_at for ONE enquirer and return the
+--- stamped rows. The per-applicant analogue of mark_followup_reminders_for_
+--- vacancy: eligibility is still the view's stage2_due column
+--- (inbound_email_sender_state is the single home of the rule), now scoped
+--- to one sender — so the per-row \"Follow up\" button fires stage 2 only for
+--- the person whose series is complete and aged past the 2-day gate. All of
+--- the sender's rows are stamped so the DISTINCT-ON-latest awaiting list
+--- always displays the flag. Consuming the one-shot in the same statement
+--- makes a double-click safe: the second call matches zero rows. Recipients
+--- are deduped (case-folded) and validated in Gleam before send.
+UPDATE inbound_email
+SET second_reminder_sent_at = now()
+WHERE vacancy_id = $1
+  AND lower(sender_email) = lower($2)
+  AND second_reminder_sent_at IS NULL
+  AND sender_email IS NOT NULL
+  AND sender_email <> ''
+  AND lower(sender_email) IN (
+    SELECT sender_email_lc
+    FROM inbound_email_sender_state
+    WHERE vacancy_id = $1
+      AND stage2_due
+  )
+RETURNING sender_email, sender_name
+"
+  |> pog.query
+  |> pog.parameter(pog.text(uuid.to_string(arg_1)))
+  |> pog.parameter(pog.text(arg_2))
+  |> pog.returning(decoder)
+  |> pog.execute(db)
+}
+
 /// A row you get from running the `mark_followup_reminders_for_vacancy` query
 /// defined in `./src/inbound_email/sql/mark_followup_reminders_for_vacancy.sql`.
 ///
@@ -321,6 +395,75 @@ RETURNING sender_email, sender_name
   |> pog.execute(db)
 }
 
+/// A row you get from running the `mark_reminder_for_sender` query
+/// defined in `./src/inbound_email/sql/mark_reminder_for_sender.sql`.
+///
+/// > 🐿️ This type definition was generated automatically using v4.6.0 of the
+/// > [squirrel package](https://github.com/giacomocavalieri/squirrel).
+///
+pub type MarkReminderForSenderRow {
+  MarkReminderForSenderRow(
+    sender_email: Option(String),
+    sender_name: Option(String),
+  )
+}
+
+/// - mark_reminder_for_sender(vacancy_id: UUID, sender_email: TEXT)
+/// - Atomically stamp reminder_sent_at on every not-yet-reminded row of ONE
+/// - enquirer (case-folded) and return them. The per-applicant analogue of
+/// - mark_reminders_for_vacancy: scoping the same WHERE to a single sender
+/// - means the per-row "Remind" button sends exactly the stage that's
+/// - next-due for that person (stage 1 here — any un-reminded row), reusing
+/// - the bulk's gate unchanged. Stamps ALL of that sender's un-reminded rows
+/// - (a re-enquiry's fresh row) so the DISTINCT-ON-latest awaiting list
+/// - always displays the flag. Consuming the one-shot in the same statement
+/// - makes a double-click safe: the second call matches zero rows. Recipients
+/// - are deduped (case-folded) and validated in Gleam before send.
+///
+/// > 🐿️ This function was generated automatically using v4.6.0 of
+/// > the [squirrel package](https://github.com/giacomocavalieri/squirrel).
+///
+pub fn mark_reminder_for_sender(
+  db: pog.Connection,
+  arg_1: Uuid,
+  arg_2: String,
+) -> Result(pog.Returned(MarkReminderForSenderRow), pog.QueryError) {
+  let decoder = {
+    use sender_email <- decode.field(0, decode.optional(decode.string))
+    use sender_name <- decode.field(1, decode.optional(decode.string))
+    decode.success(MarkReminderForSenderRow(sender_email:, sender_name:))
+  }
+
+  "--- mark_reminder_for_sender(vacancy_id: UUID, sender_email: TEXT)
+--- Atomically stamp reminder_sent_at on every not-yet-reminded row of ONE
+--- enquirer (case-folded) and return them. The per-applicant analogue of
+--- mark_reminders_for_vacancy: scoping the same WHERE to a single sender
+--- means the per-row \"Remind\" button sends exactly the stage that's
+--- next-due for that person (stage 1 here — any un-reminded row), reusing
+--- the bulk's gate unchanged. Stamps ALL of that sender's un-reminded rows
+--- (a re-enquiry's fresh row) so the DISTINCT-ON-latest awaiting list
+--- always displays the flag. Consuming the one-shot in the same statement
+--- makes a double-click safe: the second call matches zero rows. Recipients
+--- are deduped (case-folded) and validated in Gleam before send.
+UPDATE inbound_email
+SET reminder_sent_at = now()
+WHERE vacancy_id = $1
+  AND lower(sender_email) = lower($2)
+  AND reminder_sent_at IS NULL
+  AND sender_email IS NOT NULL
+  AND sender_email <> ''
+  AND lower(sender_email) NOT IN (
+    SELECT lower(email) FROM application WHERE vacancy_id = $1
+  )
+RETURNING sender_email, sender_name
+"
+  |> pog.query
+  |> pog.parameter(pog.text(uuid.to_string(arg_1)))
+  |> pog.parameter(pog.text(arg_2))
+  |> pog.returning(decoder)
+  |> pog.execute(db)
+}
+
 /// A row you get from running the `mark_reminders_for_vacancy` query
 /// defined in `./src/inbound_email/sql/mark_reminders_for_vacancy.sql`.
 ///
diff --git a/server/src/inbound_email/sql/mark_followup_for_sender.sql b/server/src/inbound_email/sql/mark_followup_for_sender.sql
new file mode 100644
index 00000000..e9bcf7ba
--- /dev/null
+++ b/server/src/inbound_email/sql/mark_followup_for_sender.sql
@@ -0,0 +1,25 @@
+--- mark_followup_for_sender(vacancy_id: UUID, sender_email: TEXT)
+--- Atomically stamp second_reminder_sent_at for ONE enquirer and return the
+--- stamped rows. The per-applicant analogue of mark_followup_reminders_for_
+--- vacancy: eligibility is still the view's stage2_due column
+--- (inbound_email_sender_state is the single home of the rule), now scoped
+--- to one sender — so the per-row "Follow up" button fires stage 2 only for
+--- the person whose series is complete and aged past the 2-day gate. All of
+--- the sender's rows are stamped so the DISTINCT-ON-latest awaiting list
+--- always displays the flag. Consuming the one-shot in the same statement
+--- makes a double-click safe: the second call matches zero rows. Recipients
+--- are deduped (case-folded) and validated in Gleam before send.
+UPDATE inbound_email
+SET second_reminder_sent_at = now()
+WHERE vacancy_id = $1
+  AND lower(sender_email) = lower($2)
+  AND second_reminder_sent_at IS NULL
+  AND sender_email IS NOT NULL
+  AND sender_email <> ''
+  AND lower(sender_email) IN (
+    SELECT sender_email_lc
+    FROM inbound_email_sender_state
+    WHERE vacancy_id = $1
+      AND stage2_due
+  )
+RETURNING sender_email, sender_name
diff --git a/server/src/inbound_email/sql/mark_reminder_for_sender.sql b/server/src/inbound_email/sql/mark_reminder_for_sender.sql
new file mode 100644
index 00000000..489ac770
--- /dev/null
+++ b/server/src/inbound_email/sql/mark_reminder_for_sender.sql
@@ -0,0 +1,22 @@
+--- mark_reminder_for_sender(vacancy_id: UUID, sender_email: TEXT)
+--- Atomically stamp reminder_sent_at on every not-yet-reminded row of ONE
+--- enquirer (case-folded) and return them. The per-applicant analogue of
+--- mark_reminders_for_vacancy: scoping the same WHERE to a single sender
+--- means the per-row "Remind" button sends exactly the stage that's
+--- next-due for that person (stage 1 here — any un-reminded row), reusing
+--- the bulk's gate unchanged. Stamps ALL of that sender's un-reminded rows
+--- (a re-enquiry's fresh row) so the DISTINCT-ON-latest awaiting list
+--- always displays the flag. Consuming the one-shot in the same statement
+--- makes a double-click safe: the second call matches zero rows. Recipients
+--- are deduped (case-folded) and validated in Gleam before send.
+UPDATE inbound_email
+SET reminder_sent_at = now()
+WHERE vacancy_id = $1
+  AND lower(sender_email) = lower($2)
+  AND reminder_sent_at IS NULL
+  AND sender_email IS NOT NULL
+  AND sender_email <> ''
+  AND lower(sender_email) NOT IN (
+    SELECT lower(email) FROM application WHERE vacancy_id = $1
+  )
+RETURNING sender_email, sender_name
diff --git a/server/src/router.gleam b/server/src/router.gleam
index 91694a15..9416987e 100644
--- a/server/src/router.gleam
+++ b/server/src/router.gleam
@@ -524,6 +524,15 @@ pub fn handle_request(ctx: Context, req: Request) -> Response {
       )
       inbound_handler.handle_remind_applicants(req, ctx.config, landlord.id, id)
     }
+    http.Post, ["api", "v1", "vacancies", id, "remind-applicant"] -> {
+      use _req, landlord <- session_middleware.require_session(
+        req,
+        ctx.config.db,
+        ctx.config.sentry,
+        supabase_config(ctx.config),
+      )
+      inbound_handler.handle_remind_applicant(req, ctx.config, landlord.id, id)
+    }
 
     // AI analysis polling (authenticated)
     http.Get, ["api", "v1", "ai", "jobs", id] -> {
diff --git a/server/test/integration/awaiting_integration_test.gleam b/server/test/integration/awaiting_integration_test.gleam
index 0aa1b030..625f2524 100644
--- a/server/test/integration/awaiting_integration_test.gleam
+++ b/server/test/integration/awaiting_integration_test.gleam
@@ -8,6 +8,7 @@
 //// self-healing clear-on-failure) out of the assertions.
 
 import gleam/http
+import gleam/json
 import gleam/list
 import gleam/option
 import gleam/string
@@ -826,3 +827,231 @@ pub fn remind_clears_invalid_legacy_sender_in_transaction_test() {
          AND reminder_sent_at IS NULL")
   unstamped |> should.equal(1)
 }
+
+// -- Per-applicant remind (POST .../remind-applicant) -------------------------
+//
+// The per-row "Remind" / "Follow up" button's endpoint. It reuses the bulk
+// handler's transactional stamp+send plumbing, scoped to one email — so the
+// two-stage gate enforces itself unchanged (stage 1 only for an un-reminded
+// sender; stage 2 only when inbound_email_sender_state says stage2_due). The
+// SQL-level tests pin the per-sender scoping deterministically (no background
+// send); the handler-level tests assert only the synchronous response, never
+// persisted stamps — the background self-heal clear races the empty Resend
+// key (same discipline as the bulk handler tests above).
+
+fn remind_applicant_request(vacancy_id: String, email: String) {
+  simulate.request(
+    http.Post,
+    "/api/v1/vacancies/" <> vacancy_id <> "/remind-applicant",
+  )
+  |> simulate.json_body(json.object([#("email", json.string(email))]))
+}
+
+/// The per-sender stage-1 stamp touches ONLY the named email — the headline
+/// scoping invariant (a per-row click never stamps a sibling enquirer).
+pub fn mark_reminder_for_sender_stamps_only_the_named_email_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound(db, vacancy_id, "alice@example.com")
+  seed_inbound(db, vacancy_id, "bob@example.com")
+  let assert Ok(vacancy_uuid) = uuid.from_string(vacancy_id)
+
+  let assert Ok(pog.Returned(_, marked)) =
+    inbound_sql.mark_reminder_for_sender(db, vacancy_uuid, "alice@example.com")
+  list.length(marked) |> should.equal(1)
+
+  // Alice stamped, Bob untouched.
+  let assert Ok(alice_stamped) =
+    test_db.query_int(db, "SELECT count(*)::int FROM inbound_email
+       WHERE vacancy_id = '" <> vacancy_id <> "'::uuid
+         AND lower(sender_email) = 'alice@example.com'
+         AND reminder_sent_at IS NOT NULL")
+  alice_stamped |> should.equal(1)
+  let assert Ok(bob_stamped) =
+    test_db.query_int(db, "SELECT count(*)::int FROM inbound_email
+       WHERE vacancy_id = '" <> vacancy_id <> "'::uuid
+         AND lower(sender_email) = 'bob@example.com'
+         AND reminder_sent_at IS NOT NULL")
+  bob_stamped |> should.equal(0)
+}
+
+/// The per-sender stage-2 stamp honours the view's stage2_due gate: only the
+/// due enquirer is stamped, never one whose stage-1 is too fresh or who was
+/// never reminded.
+pub fn mark_followup_for_sender_respects_the_gate_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound_reminded_days_ago(db, vacancy_id, "due@example.com", 3)
+  seed_inbound_reminded_days_ago(db, vacancy_id, "too-soon@example.com", 1)
+  let assert Ok(vacancy_uuid) = uuid.from_string(vacancy_id)
+
+  // Stamping the DUE enquirer succeeds…
+  let assert Ok(pog.Returned(_, marked)) =
+    inbound_sql.mark_followup_for_sender(db, vacancy_uuid, "due@example.com")
+  list.length(marked) |> should.equal(1)
+
+  // …stamping the too-soon enquirer matches nothing (gate holds), even
+  // though their stage-1 row exists.
+  let assert Ok(pog.Returned(_, blocked)) =
+    inbound_sql.mark_followup_for_sender(
+      db,
+      vacancy_uuid,
+      "too-soon@example.com",
+    )
+  list.length(blocked) |> should.equal(0)
+}
+
+/// Handler: a never-reminded enquirer → stage 1 fires, stage 2 doesn't.
+pub fn single_applicant_remind_reports_stage1_count_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound(db, vacancy_id, "alice@example.com")
+
+  let resp =
+    inbound_handler.handle_remind_applicant(
+      remind_applicant_request(vacancy_id, "alice@example.com"),
+      test_server_config(db),
+      landlord_id,
+      vacancy_id,
+    )
+  resp.status |> should.equal(200)
+  let body = simulate.read_body(resp)
+  body |> string.contains("\"reminded\":1") |> should.be_true
+  body |> string.contains("\"followup\":0") |> should.be_true
+}
+
+/// Handler: an enquirer whose stage-1 aged past the gate → stage 2 fires.
+pub fn single_applicant_remind_reports_stage2_count_when_due_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound_reminded_days_ago(db, vacancy_id, "due@example.com", 4)
+
+  let resp =
+    inbound_handler.handle_remind_applicant(
+      remind_applicant_request(vacancy_id, "due@example.com"),
+      test_server_config(db),
+      landlord_id,
+      vacancy_id,
+    )
+  resp.status |> should.equal(200)
+  let body = simulate.read_body(resp)
+  body |> string.contains("\"reminded\":0") |> should.be_true
+  body |> string.contains("\"followup\":1") |> should.be_true
+}
+
+/// Handler: an enquirer already at both stages → nothing fires (both 0).
+pub fn single_applicant_remind_reports_zero_when_already_fully_reminded_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound_reminded_days_ago(db, vacancy_id, "done@example.com", 5)
+  let assert Ok(_) =
+    pog.query(
+      "UPDATE inbound_email SET second_reminder_sent_at = now() - interval '4 days'
+       WHERE lower(sender_email) = 'done@example.com'",
+    )
+    |> pog.execute(db)
+
+  let resp =
+    inbound_handler.handle_remind_applicant(
+      remind_applicant_request(vacancy_id, "done@example.com"),
+      test_server_config(db),
+      landlord_id,
+      vacancy_id,
+    )
+  resp.status |> should.equal(200)
+  let body = simulate.read_body(resp)
+  body |> string.contains("\"reminded\":0") |> should.be_true
+  body |> string.contains("\"followup\":0") |> should.be_true
+}
+
+/// Handler: another landlord can't remind this vacancy's enquirers — 404,
+/// nothing stamped.
+pub fn single_applicant_remind_cross_tenant_returns_404_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(owner_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, owner_id, True)
+  seed_inbound(db, vacancy_id, "alice@example.com")
+  let assert Ok(other_id) = test_db.seed_landlord(db, 3)
+
+  let resp =
+    inbound_handler.handle_remind_applicant(
+      remind_applicant_request(vacancy_id, "alice@example.com"),
+      test_server_config(db),
+      other_id,
+      vacancy_id,
+    )
+  resp.status |> should.equal(404)
+
+  let assert Ok(stamped) =
+    test_db.query_int(db, "SELECT count(*)::int FROM inbound_email
+       WHERE vacancy_id = '" <> vacancy_id <> "'::uuid
+         AND (reminder_sent_at IS NOT NULL OR second_reminder_sent_at IS NOT NULL)")
+  stamped |> should.equal(0)
+}
+
+/// Handler: a closed vacancy is invisible to find_vacancy_for_invite — 404,
+/// nothing stamped.
+pub fn single_applicant_remind_closed_vacancy_returns_404_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound(db, vacancy_id, "alice@example.com")
+  let assert Ok(_) =
+    pog.query(
+      "UPDATE vacancy SET status = 'closed' WHERE id = '"
+      <> vacancy_id
+      <> "'::uuid",
+    )
+    |> pog.execute(db)
+
+  let resp =
+    inbound_handler.handle_remind_applicant(
+      remind_applicant_request(vacancy_id, "alice@example.com"),
+      test_server_config(db),
+      landlord_id,
+      vacancy_id,
+    )
+  resp.status |> should.equal(404)
+
+  let assert Ok(stamped) =
+    test_db.query_int(db, "SELECT count(*)::int FROM inbound_email
+       WHERE vacancy_id = '" <> vacancy_id <> "'::uuid
+         AND reminder_sent_at IS NOT NULL")
+  stamped |> should.equal(0)
+}
+
+/// Handler: a re-enquiry (old stage-1 + fresh un-reminded row) sends stage 1
+/// and suppresses stage 2 — the fresh stamp restarts the series, matching the
+/// bulk path's pinned behaviour.
+pub fn single_applicant_remind_re_enquiry_sends_stage1_not_stage2_test() {
+  use <- unitest.tag("integration")
+  let db = setup()
+  let assert Ok(landlord_id) = test_db.seed_landlord(db, 3)
+  let assert Ok(vacancy_id) = test_db.seed_vacancy(db, landlord_id, True)
+  seed_inbound_reminded_days_ago(db, vacancy_id, "returning@example.com", 5)
+  seed_inbound(db, vacancy_id, "returning@example.com")
+
+  let resp =
+    inbound_handler.handle_remind_applicant(
+      remind_applicant_request(vacancy_id, "returning@example.com"),
+      test_server_config(db),
+      landlord_id,
+      vacancy_id,
+    )
+  resp.status |> should.equal(200)
+  let body = simulate.read_body(resp)
+  body |> string.contains("\"reminded\":1") |> should.be_true
+  body |> string.contains("\"followup\":0") |> should.be_true
+}

--- SPEC / CONTEXT ---
This PR adds a per-applicant "Remind"/"Follow up" button to the landlord Awaiting list, coexisting with the existing bulk "Send reminder to N" button.

CRITICAL LENS-GUARD (deliberate design choices — do NOT flag as defects):
- Do NOT flag "no force-remind / can't bypass the stage gate" as a defect. Gate-respecting-only is the user-confirmed design; force-remind is a deferred follow-up, not a gap. The two-stage gate MUST be respected.
- Do NOT flag "reuses the bulk plumbing instead of standalone" as a defect. Reusing the email template/sending/validation (valid_recipients, send_reminders_background) is the explicit requirement — no duplicate plumbing. Verify the reuse is correct, not that it exists.
- Do NOT flag the bulk button still existing, or the buttons coexisting, as redundancy. The per-applicant button is deliberately ADDITIVE.

Legitimate findings in this area WOULD be: the single-applicant path not faithfully mirroring the bulk's atomicity (stamp-then-send, un-stamp on send-time validation failure); a gate breach (per-applicant endpoint sending a reminder the two-stage gate should suppress — double-send, or stage-2 when only stage-1 is due; the re-enquiry edge of old stage-1 + fresh row is the key case); owner-check/closed-vacancy gaps; stamp races (concurrent per-applicant + bulk, or two per-applicant clicks — is the server-side guard real, not just client-side?); PII leakage (applicant emails logged/echoed beyond the legitimate recipient); em-dashes in user-facing copy; broken Gleam/JS parse; missing tests for pinned behavior.

WORKTREE (the reviewed checkout — verify all claims against these files): /Users/moses/.herdr/worktrees/RightTenantry/perkins-per-applicant-remind-r1

Full specs (read both with your read tool):
- Round briefing: /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-per-applicant-remind-r1.md
- Original job briefing (the spec with acceptance criteria): /Users/moses/code/_bmad-output/briefings/righttenantry-per-applicant-remind.md

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- FILE OUTPUT: write ONLY your JSON array to the absolute path in FILE-OUTPUT below, using your write tool. Then reply to your user with a single word: DONE. Do not write anywhere else.

FILE-OUTPUT: /Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1/acceptance.json

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
