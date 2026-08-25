You are reviewing a code diff. This is the 'tests' lens of a parallel code-review.

--- PROJECT CONVENTIONS ---
RightTenant: Gleam/Lustre monorepo. The /apply/:code public application form is SSR (server-side rendered Erlang via Wisp), NOT part of the SPA. PostHog analytics is inlined into the SSR page via an inline <script> emitted by server/src/application/form_view.gleam (function view_posthog_snippet). The authenticated landlord SPA (index.html) has a SEPARATE PostHog init injected by Makefile/Dockerfile perl (RT_ANALYTICS) that has NO sanitize_properties scrub. There must be exactly ONE copy of the sanitize_properties/scrub logic in the codebase (in form_view.gleam). No JavaScript FFI is allowed in this codebase (server-side Erlang FFI is fine). No `let assert` in production. No em-dashes in user-facing copy. The fix is internal snippet JS, not user-facing copy.

LOAD-BEARING INVARIANTS for THIS review (the diagnosis is PINNED — do NOT re-derive or re-litigate the bug; review the FIX + its tests):
1. The resume-token/URL redaction invariant must NOT regress: any property key matching /resume-token/i (PostHog autocapture encodes the DOM attribute data-resume-token as the key attr__data-resume-token) must be redacted to "<redacted>"; any string value matching /(\/(?:resume|draft-erasure)\/)[^\s&#/?]+/ must have its token segment redacted. This must work for plain objects, arrays nested inside them, and string values. This is the thing that must never regress.
2. There must be NO second ticking copy of the sanitize_properties/scrub without the host-object guard anywhere in server/src or server/priv/static or the Makefile/Dockerfile perl.
3. The guard must recurse ONLY into plain objects ([object Object]) and arrays ([object Array]); every host object (DOM nodes, Window, Document, NodeList, etc.) returned untouched. This is the chosen/approved guard variant — do NOT flag "why not instanceof Node". VERIFY the chosen guard is correct + complete and that it keeps redaction working.
4. The regression test (scripts/js-tests/apply_event_scrub.test.js) must be REAL, not tautological: it extracts the exact shipped bytes from form_view.gleam, evals them, and the fake DOM element must genuinely exercise the failure mode + the negative control must genuinely flip.

--- SPEC / CONTEXT (the job briefing) ---
Mission: Fix a self-destruct bug in the /apply form's PostHog sanitize_properties scrubber. web-vitals.js fires CLS/LCP/INP events whose properties carry live DOM element refs; the scrub recursed into them (typeof==='object'), walked the live DOM keys, and the o[k]=... assignments fired DOM setters — setting outerText on an attached node replaces it with a text node, deleting the page structure + CSS classes, so the form collapsed to unstyled HTML the instant an applicant typed (and threw NoModificationAllowedError on detached nodes).

Required fix: guard scrub so it recurses ONLY into plain objects + arrays (Object.prototype.toString.call(o) check). Two variants were pre-approved; the plain-object variant was selected + directed. Token redaction must remain fully working.

Scope: fix ALL instances of the sanitize_properties/scrub pattern across server/src and server/priv/static. Don't leave a second ticking copy.

Required regression test: extract the shipped scrub logic (it is an inline Gleam string literal) and exercise it in isolation. Assert: (1) scrub returns without throwing given a DOM-like element; (2) the element is not mutated; (3) redaction STILL works on plain object nests (attr__data-resume-token key -> <redacted>, /resume/<token> URL -> /resume/<redacted>, incl. nested in arrays). posthog-js no-ops capture under HeadlessChrome UAs, so exercise scrub directly (do not rely on real capture).

Acceptance: scrub guards against host objects; the form no longer collapses; the console error is gone; regression test added + green; same pattern fixed in every copy; never merge.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics: new/modified API endpoints without matching coverage; auth/authz paths missing negative tests; happy-path-only coverage where error handling is implied; new DB operations without integration coverage; new state transitions without boundary tests.

Test level mix (unit/integration/E2E): flag mismatches as findings.

For this review specifically: VERIFY the regression test is REAL and non-tautological. It must (a) extract the EXACT shipped bytes from form_view.gleam (read the test + the source to confirm the anchors resolve to the shipped scrub); (b) use a fake DOM element that genuinely reproduces the failure mode (throw-on-set outerText, enumerable DOM-ish keys, a host-object toStringTag); (c) include a negative control that genuinely goes red if the guard is removed; (d) assert redaction still works (keys + URLs, nested in arrays). If any of these is weak or missing, file it.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate
Gate thresholds: PASS P0 100%/P1>=90%/overall>=80%; CONCERNS P0 100%/P1 80-89%/overall>=80%; FAIL P0<100% or P1<80% or overall<80%.

--- DIFF ---
diff --git a/scripts/js-tests/apply_event_scrub.test.js b/scripts/js-tests/apply_event_scrub.test.js
new file mode 100644
index 00000000..c9797e3d
--- /dev/null
+++ b/scripts/js-tests/apply_event_scrub.test.js
@@ -0,0 +1,261 @@
+// Regression test for the 2026-08-10 /apply form-collapse bug.
+//
+// Root cause: the inline PostHog `sanitize_properties` scrub recursed into ANY
+// `typeof === 'object'` value. web-vitals CLS/LCP/INP events attach the live
+// DOM element that shifted / painted / was interacted with as an event
+// property, so scrub walked the live DOM node and the `o[k] = ...` assignments
+// fired DOM setters — setting `outerText` on an attached node REPLACES it with a
+// text node, deleting the page structure + CSS classes, so the form collapsed to
+// unstyled HTML the instant an applicant typed (and threw NoModificationAllowed
+// Error on detached nodes — the console signature). The fix: scrub now recurses
+// ONLY into plain objects + arrays (every host object is returned untouched).
+//
+// This test exercises the EXACT bytes that ship to /apply/:code — it reads the
+// sanitize_properties block out of server/src/application/form_view.gleam,
+// reconstructs the function, and evals it. No drift between test and production:
+// change the shipped scrub and this test tracks it (and fails loudly if the
+// extraction anchors move, forcing an update — never a silent pass). The
+// behaviour is also structurally pinned in form_view_test.gleam.
+//
+// Note: posthog-js no-ops capture under HeadlessChrome UAs (_is_bot()), so we
+// exercise the scrub function directly — never real PostHog capture.
+
+const { test } = require("node:test");
+const assert = require("node:assert/strict");
+const fs = require("node:fs");
+const path = require("node:path");
+
+// ---------------------------------------------------------------------------
+// Load the SHIPPED sanitize_properties from form_view.gleam.
+// ---------------------------------------------------------------------------
+
+const GLEAM = path.join(
+  __dirname,
+  "..",
+  "..",
+  "server",
+  "src",
+  "application",
+  "form_view.gleam",
+);
+
+function loadShippedSanitize() {
+  const src = fs.readFileSync(GLEAM, "utf8");
+
+  // The scrub is rendered inline as a run of `<> "..."` Gleam string-literal
+  // concatenations. Anchor on the stable start/end tokens of the block, then
+  // span from the `<>` that opens the first literal to the closing `"` of the
+  // last so every literal in between is captured whole.
+  const START = "sanitize_properties:function(p){";
+  const END = "return scrub(p);";
+  const startIdx = src.indexOf(START);
+  const endIdx = src.indexOf(END, startIdx);
+  if (startIdx === -1 || endIdx === -1) {
+    throw new Error(
+      "apply_event_scrub.test: could not locate the sanitize_properties " +
+        "block in form_view.gleam — has the snippet been restructured? " +
+        "Update the extraction anchors.",
+    );
+  }
+  const openIdx = src.lastIndexOf("<>", startIdx);
+  const closeQuote = src.indexOf('"', endIdx);
+  const region = src.slice(openIdx, closeQuote + 1);
+
+  // Pull each `<> "..."` literal's content out of the region.
+  const literals = [...region.matchAll(/<>\s*"((?:[^"\\]|\\.)*)"/g)].map(
+    (m) => m[1],
+  );
+  if (literals.length === 0) {
+    throw new Error(
+      "apply_event_scrub.test: no string literals found in the " +
+        "sanitize_properties region of form_view.gleam.",
+    );
+  }
+
+  // Unescape Gleam string escapes (standard C-like): \n \t \r pass through;
+  // \\ -> \, \" -> ", \/ -> /, etc.
+  const unescape = (s) =>
+    s.replace(/\\(.)/g, (_, c) =>
+      c === "n" ? "\n" : c === "t" ? "\t" : c === "r" ? "\r" : c,
+    );
+
+  let js = literals.map(unescape).join("");
+  // js === "sanitize_properties:function(p){...return scrub(p);},"
+  // Turn the object-method shorthand into a standalone callable expression:
+  //   "sanitize_properties:function(p){...}" -> "(function(p){...})"
+  js = js.replace(/,$/, "").replace(/^sanitize_properties:/, "");
+  // Indirect eval: returns the function, with access to the real `Object`.
+  return (0, eval)("(" + js + ")");
+}
+
+// ---------------------------------------------------------------------------
+// A faithful fake of the DOM element web-vitals attaches to its events.
+// ---------------------------------------------------------------------------
+
+// It is a HOST object (Object.prototype.toString -> '[object HTMLDivElement]',
+// NOT '[object Object]') with a setter on outerText that throws like a detached
+// node would, and enumerable DOM-ish own keys so an UNGUARDED recursion walks
+// straight into the throwing setter. On a real ATTACHED node the same setter
+// would silently replace the node with a text node (the form-collapse mechanism)
+// — the throw here just makes that mutation observable from a test.
+function makeFakeDomElement() {
+  let outerTextSets = 0;
+  const el = {
+    nodeName: "DIV",
+    nodeType: 1,
+    tagName: "DIV",
+    id: "",
+    className: "form-card",
+    classList: { add() {}, remove() {} },
+    children: [],
+    childNodes: [],
+    style: {},
+    textContent: "real text",
+    get outerText() {
+      return "real text";
+    },
+    set outerText(_v) {
+      outerTextSets += 1;
+      throw new TypeError(
+        "NoModificationAllowedError: Failed to set 'outerText': " +
+          "this element has no parent.",
+      );
+    },
+    get innerText() {
+      return "real text";
+    },
+    set innerText(_v) {
+      outerTextSets += 1;
+      throw new TypeError("NoModificationAllowedError: Failed to set 'innerText'");
+    },
+    getAttribute() {
+      return null;
+    },
+  };
+  Object.defineProperty(el, Symbol.toStringTag, {
+    value: "HTMLDivElement",
+    configurable: true,
+  });
+  Object.defineProperty(el, "_outerTextSets", {
+    get: () => outerTextSets,
+    enumerable: false,
+    configurable: true,
+  });
+  return el;
+}
+
+// ---------------------------------------------------------------------------
+// Tests.
+// ---------------------------------------------------------------------------
+
+test("shipped sanitize_properties is loadable from form_view.gleam", () => {
+  // Guards the extraction itself: if this throws, the anchors moved and every
+  // other test below is moot.
+  const sanitize_properties = loadShippedSanitize();
+  assert.equal(typeof sanitize_properties, "function");
+});
+
+test("scrub does not throw when an event carries a DOM element (the bug)", () => {
+  const sanitize_properties = loadShippedSanitize();
+  const el = makeFakeDomElement();
+  // Mirror web-vitals' shape: the element rides `target` (and CLS attribution
+  // nests it under `attribution.target`).
+  const props = {
+    $current_url: "https://righttenantry.ie/apply/ABC123",
+    target: el,
+    attribution: { target: el, value: 0.12 },
+  };
+
+  let out;
+  assert.doesNotThrow(() => {
+    out = sanitize_properties(props);
+  }, "scrub must return without throwing for a DOM-element-bearing event");
+
+  // The element must be untouched — no DOM setter fired.
+  assert.equal(
+    el._outerTextSets,
+    0,
+    "scrub must not fire outerText/innerText setters on the element",
+  );
+  assert.equal(el.className, "form-card");
+  assert.equal(el.textContent, "real text");
+  // The element reference is returned as-is (scrub returns host objects whole).
+  assert.strictEqual(out.target, el);
+  assert.strictEqual(out.attribution.target, el);
+});
+
+test("scrub still redacts resume-token keys and resume/draft-erasure URLs", () => {
+  const sanitize_properties = loadShippedSanitize();
+  const out = sanitize_properties({
+    // PostHog autocapture encodes the data-resume-token DOM attribute as the
+    // key `attr__data-resume-token` (hyphenated) — the key regex's target.
+    "attr__data-resume-token": "the-secret-capability-token",
+    $current_url: "https://righttenantry.ie/resume/ABCDEF123",
+    nested: {
+      continue_url: "https://righttenantry.ie/draft-erasure/XYZ999/step/2",
+      selector: 'div[attr__data-resume-token="zzz"]',
+      plain: "kept as-is",
+    },
+  });
+
+  // Key redaction: any key matching /resume-token/i -> value replaced.
+  assert.equal(out["attr__data-resume-token"], "<redacted>");
+  // URL redaction: the token segment after /resume/ or /draft-erasure/ is
+  // redacted; the rest of the URL (path + query) is preserved.
+  assert.equal(out.$current_url, "https://righttenantry.ie/resume/<redacted>");
+  assert.equal(
+    out.nested.continue_url,
+    "https://righttenantry.ie/draft-erasure/<redacted>/step/2",
+  );
+  // A CSS-ish selector string is NOT a URL path — left alone.
+  assert.equal(
+    out.nested.selector,
+    'div[attr__data-resume-token="zzz"]',
+  );
+  assert.equal(out.nested.plain, "kept as-is");
+});
+
+test("scrub redacts token keys nested inside arrays too (recursion preserved)", () => {
+  const sanitize_properties = loadShippedSanitize();
+  // Arrays must still be recursed into (the guard allows [object Array]).
+  const out = sanitize_properties({
+    elements: [
+      { "attr__data-resume-token": "tok-a", href: "https://x.ie/resume/AAA" },
+      { href: "https://x.ie/draft-erasure/BBB" },
+    ],
+  });
+  assert.equal(out.elements[0]["attr__data-resume-token"], "<redacted>");
+  assert.equal(out.elements[0].href, "https://x.ie/resume/<redacted>");
+  assert.equal(out.elements[1].href, "https://x.ie/draft-erasure/<redacted>");
+});
+
+test("NEGATIVE CONTROL — a scrub WITHOUT the host-object guard fires the setter (proves the suite bites)", () => {
+  // Reproduces the pre-fix bug verbatim. A green test above is only meaningful
+  // if removing the guard turns this red: the unguarded scrub recurses into any
+  // object, so a DOM-element-bearing event walks into the throwing setter.
+  // eslint-disable-next-line no-new-func
+  const buggyScrub = new Function(
+    "p",
+    "var re=/(\\/(?:resume|draft-erasure)\\/)[^\\s&#/?]+/g;" +
+      "var scrub=function(o){if(!o||typeof o!=='object')return o;" +
+      "for(var k in o){var v=o[k];" +
+      "if(/resume-token/i.test(k)){o[k]='<redacted>';}" +
+      "else if(typeof v==='string'){o[k]=v.replace(re,'$1<redacted>');}" +
+      "else if(v&&typeof v==='object'){scrub(v);}}" +
+      "return o;};" +
+      "return scrub(p);",
+  );
+
+  const el = makeFakeDomElement();
+  assert.throws(
+    () => buggyScrub({ target: el }),
+    /outerText|NoModification/i,
+    "the unguarded scrub must throw when it walks a DOM element",
+  );
+  assert.ok(
+    el._outerTextSets > 0,
+    "the unguarded scrub must have fired the outerText setter — " +
+      "if not, this fake element does not reproduce the bug and the " +
+      "green tests above prove nothing",
+  );
+});
diff --git a/server/src/application/form_view.gleam b/server/src/application/form_view.gleam
index b3e256c7..b72824c3 100644
--- a/server/src/application/form_view.gleam
+++ b/server/src/application/form_view.gleam
@@ -277,7 +277,29 @@ pub fn view_posthog_snippet(
         // belt-and-braces now the token rides a JS global instead of the DOM.
         <> "sanitize_properties:function(p){"
         <> "var re=/(\\/(?:resume|draft-erasure)\\/)[^\\s&#/?]+/g;"
-        <> "var scrub=function(o){if(!o||typeof o!=='object')return o;"
+        <> "var scrub=function(o){"
+        // Host-object guard (2026-08-10 form-collapse regression). web-vitals
+        // CLS / LCP / INP events attach the live DOM element that shifted /
+        // painted / was interacted with as an event property. Without this
+        // guard scrub recursed into it (typeof==='object'), walked the live
+        // DOM keys, and the o[k]=... assignments fired DOM setters: setting
+        // outerText on an attached node REPLACES it with a text node, deleting
+        // the page structure and the classes the CSS targets, so the form
+        // collapsed to unstyled HTML the instant an applicant typed (and threw
+        // NoModificationAllowedError on detached nodes). Recurse ONLY into
+        // plain objects + arrays; every host object (DOM nodes, Window,
+        // Document, NodeList, ...) is returned untouched. Preferred over
+        // `instanceof Node`: skips ALL host objects (not just Nodes) AND stays
+        // testable under `node --test`, where the `Node` global is absent (so
+        // an `instanceof Node` guard is untestable there). Token redaction is
+        // unaffected: every redaction target (resume-token keys, resume /
+        // draft-erasure URL strings) lives in plain-object string properties,
+        // never inside a DOM node. Runtime behaviour pinned in
+        // scripts/js-tests/apply_event_scrub.test.js (extracts + evals these
+        // exact bytes).
+        <> "if(!o||typeof o!=='object')return o;"
+        <> "var ts=Object.prototype.toString.call(o);"
+        <> "if(ts!=='[object Object]'&&ts!=='[object Array]')return o;"
         <> "for(var k in o){var v=o[k];"
         <> "if(/resume-token/i.test(k)){o[k]='<redacted>';}"
         <> "else if(typeof v==='string'){o[k]=v.replace(re,'$1<redacted>');}"
diff --git a/server/test/application/form_view_test.gleam b/server/test/application/form_view_test.gleam
index 5e5e3618..071a73dc 100644
--- a/server/test/application/form_view_test.gleam
+++ b/server/test/application/form_view_test.gleam
@@ -734,3 +734,28 @@ pub fn apply_form_posthog_scrubs_draft_tokens_test() {
   |> should.be_true
   html |> string.contains("resume|draft-erasure") |> should.be_true
 }
+
+// 2026-08-10 form-collapse regression. web-vitals CLS/LCP/INP events attach
+// the live DOM element that shifted / painted / was interacted with as an
+// event property; without a host-object guard the scrub recursed into it,
+// walked the live DOM keys, and the o[k]=... assignments fired DOM setters
+// (setting outerText on an attached node replaces it with a text node, so
+// the form collapsed to unstyled HTML the instant an applicant typed). The
+// scrub must recurse ONLY into plain objects + arrays. This pins the guard
+// at the shipped-snippet level (exact bytes); the runtime behaviour is
+// pinned in scripts/js-tests/apply_event_scrub.test.js, which extracts and
+// evals these same bytes and proves the guard bites.
+pub fn apply_form_posthog_scrub_guards_against_dom_nodes_test() {
+  let vacancy = test_helpers.test_vacancy_row()
+  let html = form_view.view_application_page(vacancy, "phc_test_key")
+  // The plain-object-only recursion guard: host objects (DOM nodes, Window,
+  // Document, NodeList, ...) are returned untouched.
+  html
+  |> string.contains("Object.prototype.toString.call(o)")
+  |> should.be_true
+  html
+  |> string.contains(
+    "if(ts!=='[object Object]'&&ts!=='[object Array]')return o;",
+  )
+  |> should.be_true
+}

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
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT (HEADLESS MODE — overrides the prose output above):
You are running headless. There is no human reading your stdout. Instead of printing the JSON array, you MUST write it — and ONLY it — to this exact path:
/Users/moses/code/_bmad-output/perkins/righttenantry-apply-form-scrub-fix/r1/tests.json
Write valid JSON (a single array, possibly empty). Then STOP. Do not do anything else. Do not attempt to commit, edit source, or run tests beyond what you need to verify your findings. Reading the worktree to verify claims is REQUIRED and allowed (you are at the reviewed checkout). Writing anywhere other than the named path is a violation.
