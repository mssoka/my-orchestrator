# righttenantry-apply-form-scrub-fix (2026-08-10)

- The PostHog `sanitize_properties` scrub is the ONLY inline-JS-in-Gleam scrub
  on `/apply`; grep `sanitize_properties` to find it — bare `scrub` has 20+
  unrelated hits (model-version scrub, Stripe/GoTrue PII scrub, etc.). The SPA
  shell's PostHog init (Makefile + Dockerfile `RT_ANALYTICS` perl) has NO scrub.
- Testing inline-Gleam-emitted JS under `node --test`: extract the `<> "..."`
  string-literal block from the .gleam source (anchor on stable tokens like
  `sanitize_properties:function(p){` … `return scrub(p);`, span from the opening
  `<>` to the last literal's closing `"`), unescape Gleam escapes, eval it.
  Tests the EXACT shipped bytes with no module refactor and zero leak risk on
  the defended token-redaction invariant (redaction stays always-on inline).
- `instanceof Node` guards are BLIND under `node --test` (no `Node` global
  there — the exact "Node tests blind to browser semantics" trap). For a
  DOM/host-object guard that must be runtime-tested in Node, use
  `Object.prototype.toString.call(o)` (plain-object check): skips ALL host
  objects, not just Nodes, and needs no browser shim. Prove the guard bites by
  neutering it in the shipped source and confirming the test goes red.
