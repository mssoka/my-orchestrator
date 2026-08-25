You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT edit any repository file — your only write is the JSON output file named below.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-righttenantry-demo-bulk-invite-guard-r1/AGENTS.md IN FULL before judging anything. Those are the project conventions (Gleam/Lustre monorepo: client/ SPA, server/ Wisp API, shared/ types; copy.gleam owns all landlord-facing strings; no JS FFI; explicit error handling).

--- DIFF (the canonical bytes under review — review exactly these) ---
diff --git a/client/src/copy.gleam b/client/src/copy.gleam
index f38774ab..4e5f8737 100644
--- a/client/src/copy.gleam
+++ b/client/src/copy.gleam
@@ -395,6 +395,8 @@ pub const demo_settings_notice_cta: String = "Create your vacancy →"
 
 pub const demo_payments_toast: String = "Payments aren't part of the demo. Create your own vacancy to unlock AI analysis."
 
+pub const demo_bulk_invite_toast: String = "Demo mode - invites are not sent."
+
 pub const demo_reset_failed: String = "Couldn't reset the demo. Give it another go in a moment."
 
 pub const demo_settings_profile_toast: String = "Settings aren't part of the demo. Sign up to manage your real profile."
diff --git a/client/src/demo/demo_api.gleam b/client/src/demo/demo_api.gleam
index 143e50b0..72d9c024 100644
--- a/client/src/demo/demo_api.gleam
+++ b/client/src/demo/demo_api.gleam
@@ -29,7 +29,6 @@ import lustre/effect.{type Effect}
 import model.{type ScoringStatusResponse, ScoringStatusResponse}
 import rsvp
 import shared/application_detail.{type ApplicationDetail}
-import shared/bulk_invite.{type BulkInviteResult}
 import shared/leaderboard.{type LeaderboardResponse}
 import shared/notification.{type Notification}
 import shared/vacancy.{
@@ -127,17 +126,6 @@ pub fn remind_applicant(
   #(next, deliver(on_response, result))
 }
 
-pub fn send_bulk_invite(
-  store: DemoStore,
-  vacancy_id: String,
-  _emails: String,
-  _csrf_token: String,
-  on_response: fn(Result(BulkInviteResult, ApiError)) -> msg,
-) -> #(DemoStore, Effect(msg)) {
-  let #(next, result) = demo_store.send_bulk_invite(store, vacancy_id)
-  #(next, deliver(on_response, result))
-}
-
 // -- Vacancy mutations --------------------------------------------------------
 
 pub fn create_vacancy(
diff --git a/client/src/demo/demo_store.gleam b/client/src/demo/demo_store.gleam
index 42115d24..955d51fd 100644
--- a/client/src/demo/demo_store.gleam
+++ b/client/src/demo/demo_store.gleam
@@ -39,7 +39,6 @@ import shared/application.{
 import shared/application_detail.{
   type ApplicationDetail, type AuditEntry, ApplicationDetail, AuditEntry,
 }
-import shared/bulk_invite.{type BulkInviteResult, BulkInviteResult}
 import shared/co_applicant.{type CoApplicant, CoApplicant}
 import shared/document.{
   type Document, type DocumentCategory, AdditionalDocs, CharacterRef, Document,
@@ -1584,21 +1583,6 @@ pub fn send_reminder(
   #(next, #(reminded_sent, followups_sent))
 }
 
-pub fn send_bulk_invite(
-  store: DemoStore,
-  _vacancy_id: String,
-) -> #(DemoStore, BulkInviteResult) {
-  #(
-    store,
-    BulkInviteResult(
-      sent: 2,
-      invalid: 1,
-      invalid_emails: ["bad@example.ie"],
-      trimmed: 0,
-    ),
-  )
-}
-
 pub fn refcheck_action(
   store: DemoStore,
   vacancy_id: String,
diff --git a/client/src/demo/demo_update.gleam b/client/src/demo/demo_update.gleam
index 31905ce1..e0212bf5 100644
--- a/client/src/demo/demo_update.gleam
+++ b/client/src/demo/demo_update.gleam
@@ -28,16 +28,15 @@ import gleam/string
 import helpers/notification_nav
 import lustre/effect.{type Effect}
 import model.{
-  type Model, LoadingArchive, LoadingBulkInvite, LoadingClose, LoadingPublish,
-  LoadingReminder, LoadingStatusUpdate, Model, RefcheckConfirmStart,
-  RefcheckConfirmTakeOver, RefcheckEditCorrect, RefcheckEditSubstitute,
-  RefcheckReEnable, RefcheckSkip,
+  type Model, LoadingArchive, LoadingClose, LoadingPublish, LoadingReminder,
+  LoadingStatusUpdate, Model, RefcheckConfirmStart, RefcheckConfirmTakeOver,
+  RefcheckEditCorrect, RefcheckEditSubstitute, RefcheckReEnable, RefcheckSkip,
 }
 import modem
 import msg.{
   type Msg, ApiReturnedApplicantReminder, ApiReturnedApplicationDetail,
   ApiReturnedArchiveVacancy, ApiReturnedArchivedVacancies, ApiReturnedAwaiting,
-  ApiReturnedBulkInvite, ApiReturnedCloseVacancy, ApiReturnedComparisonDetails,
+  ApiReturnedCloseVacancy, ApiReturnedComparisonDetails,
   ApiReturnedDashboardData, ApiReturnedLeaderboard, ApiReturnedLeaderboardPage,
   ApiReturnedMarkAllRead, ApiReturnedMarkRead, ApiReturnedNotifications,
   ApiReturnedRefcheckAction, ApiReturnedReminder, ApiReturnedRestoreVacancy,
@@ -425,28 +424,14 @@ pub fn handle(
         eff,
       )
     }
-    UserSubmittedBulkInvite(vacancy_id) ->
+    // Bulk invite is not part of the demo (user ruling 2026-08-24): no real
+    // send is ever attempted and no send-shaped simulation (sent/invalid
+    // counters, validation errors) can render — the demo notice replaces
+    // both. No demo_api/demo_store send path exists (defense in depth).
+    UserSubmittedBulkInvite(_) ->
       case model.bulk_invite_emails {
         "" -> #(model, effect.none())
-        _ -> {
-          let store = store_of(model)
-          let #(next, eff) =
-            demo_api.send_bulk_invite(
-              store,
-              vacancy_id,
-              model.bulk_invite_emails,
-              "",
-              ApiReturnedBulkInvite,
-            )
-          #(
-            Model(
-              ..model,
-              demo_store: Some(next),
-              loading_action: Some(LoadingBulkInvite),
-            ),
-            eff,
-          )
-        }
+        _ -> demo_not_in_demo_toast(model, copy.demo_bulk_invite_toast)
       }
 
     // -- Comparison ---------------------------------------------------------------
diff --git a/client/test/demo/demo_flow_test.gleam b/client/test/demo/demo_flow_test.gleam
index 8366268c..34c167a5 100644
--- a/client/test/demo/demo_flow_test.gleam
+++ b/client/test/demo/demo_flow_test.gleam
@@ -13,6 +13,7 @@
 //// resolves it. The browser E2E (bug-hunt) covers the effect execution.
 
 import client
+import copy
 import demo/demo_store
 import gleam/list
 import gleam/option.{type Option, None, Some}
@@ -1041,6 +1042,36 @@ pub fn demo_vacancy_detail_renders_compare_top3_button_test() {
   html |> string.contains("compare-top-3-btn") |> should.be_true
 }
 
+/// Ruling 2026-08-24: demo bulk invite must never attempt a send nor show
+/// send-shaped results — the demo notice toast replaces both. No send state
+/// (LoadingBulkInvite), no store mutation, no response dispatch, and the
+/// typed emails stay in the textarea (nothing was consumed). Reverting the
+/// arm to the old fake-send (demo_api.send_bulk_invite) fails the loading +
+/// toast assertions; the demo send path itself is removed at the source
+/// (demo_api/demo_store ship no send_bulk_invite), so the real mailer
+/// (vacancy_api.send_bulk_invite) is unreachable from demo at any level.
+pub fn demo_bulk_invite_shows_demo_notice_test() {
+  let m =
+    model.Model(
+      ..demo_model(),
+      bulk_invite_emails: "aoife@example.ie\nconor@example.ie",
+    )
+  let #(after, _) = client.update(m, msg.UserSubmittedBulkInvite("v-maples"))
+  // No send attempt: no in-flight marker, emails untouched.
+  after.loading_action |> should.equal(None)
+  after.bulk_invite_emails
+  |> should.equal("aoife@example.ie\nconor@example.ie")
+  // The demo notice replaced any send result — the send-shaped "2 sent. 1
+  // email didn't look right" copy can never render in demo mode.
+  case after.toasts {
+    [toast, ..] -> {
+      toast.message |> should.equal(copy.demo_bulk_invite_toast)
+      toast.level |> should.equal(model.ToastInfo)
+    }
+    [] -> should.fail()
+  }
+}
+
 /// Fix 1 (demo-path pin): a demo-mode toast renders through the SAME
 /// shared `components/toast.gleam` container as the real app — fixed
 /// top-right below the in-flow header, z-index one step above the consent
diff --git a/scripts/lint_demo_network.py b/scripts/lint_demo_network.py
index 9b5e031b..02729da6 100644
--- a/scripts/lint_demo_network.py
+++ b/scripts/lint_demo_network.py
@@ -118,6 +118,9 @@
 NEVER_PRODUCED = {
     "ApiReturnedConsentCheck": "UserClickedPayCheckout",
     "ApiReturnedExtensionConsentCheck": "UserClickedExtendVacancy",
+    # Demo bulk invite (2026-08-24 ruling): its only trigger is intercepted
+    # AND produces no response — the demo never renders a send-shaped result.
+    "ApiReturnedBulkInvite": "UserSubmittedBulkInvite",
 }
 
 # Helper fns whose api calls carry NO `case *.demo_mode` guard of their own.

--- SPEC / CONTEXT (the job briefing — your spec) ---
# righttenantry-demo-bulk-invite-guard

## Task

Demo-mode bulk invite must not attempt sends. User report + ruling
(2026-08-24): in RT demo mode, bulk invite → "send email" produced
"2 sent. 1 email didn't look right. Check and try that again." — an
attempted-send flow with a validation error. User ruling, verbatim:
"it should just say this is demo, not sent." Demo mode = NO real
sends and NO send-shaped errors; an explicit demo notice instead.

## Repro (as reported)

Demo mode → bulk invite → click send email → "2 sent. 1 email didn't
look right. Check and try that again." (2 appeared sent, 1 failed
validation.)

## Expected (user-ruled)

Demo mode → bulk invite → send email → a clear demo notice, e.g.
"Demo mode — invites are not sent." NO send attempt, NO validation
errors, NO fake partial-success counters. Non-demo behavior
unchanged (real sends + validation stay exactly as-is).

## Rules (hard)

1. The guard lives at the SEND path (service/action level), not just
   the button label — a demo-mode caller hitting the endpoint/service
   directly must get the same demo notice (defense in depth).
2. Find how demo mode is flagged in this codebase (env/config/seed
   marker) and use THE canonical check — don't invent a second demo
   detector. Note the mechanism in the PR body.
3. The validation-error path for real mode is untouched (real users
   still get "1 email didn't look right" with per-recipient detail —
   if the current message lacks WHICH email failed, that's a separate
   improvement; flag it, don't fix it here).
4. Tests: demo-mode bulk-invite send → demo notice, zero send
   attempts (assert the mailer is never called); real-mode path
   unchanged (existing tests green).

## Acceptance

- Demo: notice shown, no sends, no validation errors.
- Real mode: unchanged behavior + existing suite green.
- PR body shows the demo-mode detection mechanism + both paths.
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-demo-bulk-invite-guard
- base: develop (RT convention; main if no develop)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- note: dublin-rents-q2-2026 (p349) is in flight on the same repo —
  different surface (email/invite vs data posts); parallel-safe, Silas
  coordinates merge order

The PR under review: https://github.com/solarity-services/RightTenantry/pull/636 — its body is fetchable via `gh pr view 636 --json title,body` (repo solarity-services/RightTenantry). Spec rule 3 requires the real-mode validation-error gap to be FLAGGED in the PR (not fixed) — the PR body is part of the compliance surface.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Write ONE valid JSON array to this EXACT path: /Users/moses/code/_bmad-output/perkins/righttenantry-demo-bulk-invite-guard/r1/acceptance.json
Write ONLY the JSON array to that file (no prose, no markdown fencing, no preamble). Then stop.

Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
