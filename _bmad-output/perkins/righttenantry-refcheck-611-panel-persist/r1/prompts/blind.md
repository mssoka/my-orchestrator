You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
diff --git a/client/src/components/reference_panel.gleam b/client/src/components/reference_panel.gleam
index 252389a9..cec2adfe 100644
--- a/client/src/components/reference_panel.gleam
+++ b/client/src/components/reference_panel.gleam
@@ -1108,21 +1108,21 @@ fn view_edit_trio(
   html.div([class("space-y-2")], [
     html.div([class("grid grid-cols-1 sm:grid-cols-3 gap-2")], [
       text_input(
-        slot,
+        call.reference_call_id,
         "name",
         copy.refcheck_field_name,
         name,
         "refcheck-edit-name-" <> slot,
       ),
       text_input(
-        slot,
+        call.reference_call_id,
         "email",
         copy.refcheck_field_email,
         email,
         "refcheck-edit-email-" <> slot,
       ),
       text_input(
-        slot,
+        call.reference_call_id,
         "phone",
         copy.refcheck_field_phone,
         phone,
diff --git a/client/test/client_test.gleam b/client/test/client_test.gleam
index 1998c2ec..17bb47d8 100644
--- a/client/test/client_test.gleam
+++ b/client/test/client_test.gleam
@@ -29,6 +29,9 @@ import gleeunit
 import gleeunit/should
 import helpers/format
 import helpers/leaderboard as leaderboard_helpers
+import lustre/dev/query
+import lustre/dev/simulate
+import lustre/effect
 import lustre/element
 import model
 import msg
@@ -6722,3 +6725,78 @@ pub fn refcheck_export_success_toasts_dash_free_oq5_test() {
     [] -> panic as "export success must toast"
   }
 }
+
+/// #611 keystroke-swallow pin: typing into the refcheck edit-trio must land
+/// in the `refcheck_edit` dict under the ROW's `reference_call_id` and render
+/// back into the field. The bug was a key mismatch — the trio inputs sent
+/// `UserEditedRefcheckTrio` keyed by the ref SLOT ("landlord_ref") while the
+/// view/update/save all key by `reference_call_id` ("rc-1"), so keystrokes
+/// wrote to a dict entry the view never read: the field snapped back to the
+/// prefill on every render and Save persisted the ORIGINAL contact with a
+/// success toast (the #611 repro). This drives the REAL runtime path —
+/// `simulate.input` → `cache.handle` (decode2) → `client.update` → view —
+/// and asserts both the dict write and the re-rendered value.
+pub fn refcheck_trio_keystroke_lands_in_field_test() {
+  let detail =
+    application_detail.ApplicationDetail(..test_detail(), reference_calls: [
+      reference_call.ReferenceCallDetail(
+        ..refcheck_call("rc-1", reference_call.AwaitingCorrection),
+        contact_name: option.Some("Maeve O'Brien"),
+        contact_email: option.Some("maeve@example.ie"),
+        contact_phone: option.Some("+353 87 123 4567"),
+      ),
+    ])
+  let m =
+    model.Model(
+      ..model.initial(),
+      route: routes.ApplicationDetail(
+        vacancy_id: "uuid-vac-1",
+        id: "uuid-app-1",
+      ),
+      application_detail: remote_data.Success(detail),
+      refcheck_expanded: set.from_list(["rc-1"]),
+      refcheck_edit: dict.from_list([
+        #(
+          "rc-1",
+          model.RefcheckEdit(
+            call_id: "rc-1",
+            kind: model.RefcheckEditCorrect,
+            name: "Maeve O'Brien",
+            email: "maeve@example.ie",
+            phone: "+353 87 123 4567",
+            saving: False,
+            error: None,
+          ),
+        ),
+      ]),
+    )
+  let sim =
+    simulate.start(
+      simulate.application(
+        init: fn(_) { #(m, effect.none()) },
+        update: client.update,
+        view: application_detail_page.view,
+      ),
+      Nil,
+    )
+  let sim =
+    simulate.input(
+      sim,
+      on: query.element(matching: query.attribute(
+        "data-testid",
+        "refcheck-edit-email-landlord_ref",
+      )),
+      value: "maeve.fixed@example.ie",
+    )
+  // The typed value lands in the dict under the ROW's id (the #611 key).
+  let edited = simulate.model(sim).refcheck_edit |> dict.get("rc-1")
+  case edited {
+    Ok(edit) -> edit.email |> should.equal("maeve.fixed@example.ie")
+    Error(_) -> panic as "edit state must exist for rc-1"
+  }
+  // And the re-rendered input carries the typed value (no snap-back).
+  simulate.view(sim)
+  |> element.to_string
+  |> string.contains("value=\"maeve.fixed@example.ie\"")
+  |> should.be_true
+}


--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<<=40 words>",
  "recommended_fix": "<<=40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

--- BLIND-ISOLATION RULE ---
Your lens is blind. Do NOT open the repository, do NOT read any file other than the diff above, do NOT run git or any command that inspects the codebase. Reading anything beyond this diff invalidates your lens and your findings will be discarded.

--- FILE-OUTPUT CONTRACT (headless mode — this overrides everything else about how you respond) ---
Write your JSON array — and NOTHING else — to the file:
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-611-panel-persist/r1/blind.json
Use the absolute path exactly as written above; do not derive or change it. Use your file-writing tool to write the file content, then STOP — no summary message, no prose, no follow-up questions. Your only deliverable is that file. If you have zero findings, write the two characters `[]` to the file.