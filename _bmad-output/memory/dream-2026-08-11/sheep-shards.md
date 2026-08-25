# Sheep shard — dream-2026-08-11 (field-note shards reader)

Source: per-job shards in `_bmad-output/field-notes/` newer than the
2026-08-09T13:54:22Z marker. Cross-referenced against the cloned
`store/minion-field-notes.md` + `store/AGENTS.md` Gru-gotchas. Be generous
per brief; Bob filters.

---

## minion-field-notes.md — Tooling traps

### C1 — grep ERE: backslash-pipe is literal, not alternation
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: NEW
- Lesson: `grep -cE "a\|b"` does NOT count lines matching `a` or `b` — in
  ERE the backslash makes the pipe literal, so it matches the 4-char
  string `a|b` and silently returns 0. Use bare `|` for alternation
  (`grep -cE "a|b"`). Verify-grep that returns an unexpected 0 is the
  tell.
- Evidence:
  - packet-plumber-gdd-mechanics-amend (2026-08-10): "`grep -cE \"a\\|b\"` is WRONG in ERE — backslash-pipe is literal; use bare `|`. It gave false 0s in my verify pass."
- Why it makes future sessions smarter: a verify-grep that false-0s ships
  an un-verified change with no error signal.

### C2 — macOS grep has no -P; multibyte/codepoint search needs perl -CSD
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: NEW
- Lesson: macOS BSD `grep` has no `-P` (perl-regex). Searching for a
  specific multibyte codepoint (em-dash U+2014, etc.) with a plain-byte
  pattern silently misses it (returns 0). Use
  `perl -CSD -ne 'print if /\x{2014}/'` (`-CSD` = STDIN/STDOUT/STDERR
  UTF-8 + UTF-8 layer) for codepoint-accurate greps on macOS.
- Evidence:
  - righttenantry-find-stuck-terminal (2026-08-11): "macOS `grep` has no `-P`... the plain-byte form silently misses multibyte chars (first check wrongly said '0 em-dashes', `-CSD` found the U+2014 I'd added)."
- Why it makes future sessions smarter: stops the false-"0 em-dashes"
  clean-bill that lets a banned character ship.

### C3 — backtick command-substitution bites inside ANY double-quoted `-c` string, not just gh heredocs
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: AMEND-2026-08-09 (the `gh pr create --body "$(cat <<'EOF'…)` entry)
- Lesson: The backtick command-substitution trap generalizes beyond
  `gh --body` heredocs — bash substitutes backticks inside ANY
  double-quoted arg. New vector: a `-- \`kind\` is...` SQL **comment**
  inside `psql -c "..."` got substituted (`kind: command not found` to
  stderr; the query still ran, masking it). Rule: no backticks anywhere
  inside a `-c "..."` string — comments included. (Also: `gh pr create
  --body-file <path>` errors `open ...: no such file` if you drop the
  extension by reflex — the file exists, you mis-named it.)
- Evidence:
  - righttenantry-find-stuck-terminal (2026-08-11): "the backtick command-substitution trap hits `psql -c \"...\"` SQL comments too, not just `gh --body` heredocs — a `-- \\`kind\\` is...` comment inside the double-quoted `-c` arg got bash-substituted."
  - righttenantry-find-stuck-terminal (2026-08-11): "`gh pr create --body-file <path>` errors `open ...: no such file or directory` if you drop the extension by reflex."
- Why it makes future sessions smarter: one rule (no backticks in any
  double-quoted `-c`/heredoc body) covers both the known gh case and the
  new psql-comment case.

### C4 — edit-tool atomic-per-call: grep line-break positions pre-batch + marker-grep verify post-batch
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: AMEND-2026-08-03 (multi-edit atomic-per-call entry; the 2026-08-09 addendum covers cross-file + sed-rename, NOT line-break grep + marker verify)
- Lesson: The atomic-per-call rejection bit the DREAM itself: one stale
  oldText (a misplaced line-break in a wrapped bullet) silently rejected
  a 7-edit store batch. Two preventive practices not yet in the entry:
  (a) **grep the exact line-break positions** of each oldText before
  issuing a batch (wrapped bullets/reflowed strings lie about where the
  newline sits); (b) **verify post-hoc with a marker grep**
  (`grep -c dream-<date>`) that every edit actually landed — a rejected
  edit is otherwise silent.
- Evidence:
  - dream-2026-08-09 (2026-08-09): "the edit tool's atomic-per-call rejection bit the DREAM itself — one stale oldText (misplaced line-break in a wrapped bullet) silently rejected a 7-edit store batch; grep line-break positions before issuing batch edits, and verify post-hoc with a marker grep (`grep -c dream-<date>`) that all edits actually landed."
- Why it makes future sessions smarter: closes the silent-reject gap the
  cross-file/sed addendum didn't cover (line-break drift + no post-verify).

### C5 — lavish multi-question Decide answers arrive as compact code ("1A,2B,3A"); empty freeform still arrives as a prompt tag
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: NEW
- Lesson: A lavish multi-question Decide poll can return the user's
  answers as a compact code string (`1A,2B,3A`), not prose — parse
  question-number + option-letter. Also: an empty freeform-text field
  still arrives as a `"Freeform message"` prompt tag with empty `text`;
  the verdict lives in the prior `message` prompt, not the empty one
  (user often ends the session immediately after —
  `session_ended: true, ended_by: user`).
- Evidence:
  - packet-plumber-sprint-replan-v2 (2026-08-11): "Lavish multi-question Decide answers can arrive as a compact code ('1A,2B,3A'), not prose. Parse question-number + option-letter. Also: an empty freeform-text field still arrives as a `\"Freeform message\"` prompt tag with empty `text` — the verdict was in the prior `message` prompt, not the empty one."
- Why it makes future sessions smarter: stops a minion reading a compact
  answer as garbage / reading an empty freeform tag as "no verdict" and
  re-prompting.

### C6 — lavish poll `dom_snapshot` is a first-class self-check (DOM-throw render bugs)
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: AMEND-2026-07-31 (the "READ the poll's dom_snapshot" lavish-craft entry)
- Lesson: Reinforces the 2026-07-31 lesson with a sharper failure class:
  a DOM-throw inside the rendered artifact (`insertBefore(ring,
  svg.firstChild.nextSibling)` where `nextSibling` wasn't a child of the
  path → `NotFoundError`) aborted `draw()` mid-loop, leaving only the
  first node rendered — invisible without the snapshot. Read the
  dom_snapshot EVERY poll: text content = node glyphs; missing symbols =
  a throw; it both catches and confirms-every-fix with no browser.
- Evidence:
  - packet-plumber-routing-explorer (2026-08-10): "the lavish poll's `dom_snapshot` is a first-class self-check — it caught a DOM-throw render bug (`insertBefore(ring, svg.firstChild.nextSibling)` ... → NotFoundError aborted `draw()` mid-loop, leaving only the first node) AND confirmed every fix without a browser."
- Why it makes future sessions smarter: a second independent confirmation
  that dom_snapshot is the no-browser self-check, now with the
  exception-throws-mid-render failure mode named.

### C7 — lavish-gated deliverable in an absent-user window: hold the gate, don't escalate as blocked
- Target: minion-field-notes.md (Recurring review findings — the lavish/state.json entry)
- Class-hint: AMEND-2026-08-03 (lavish session-end strand prompt; 2026-08-09 addendum named the state.json path)
- Lesson: A lavish-gated docs deliverable dispatched into an absent-user
  window = long idle polls (observed ~6.5h overnight; state.json frozen
  at open-time). Re-running the poll on each bash timeout is correct
  (queued feedback is never lost) — **hold the gate, do NOT escalate as
  blocked**. Verify the verdict via `~/.lavish-axi/state.json`
  `sessions.<id>.chat[].text` (the compact poll `prompts[]` repr is
  ambiguous; "good" + `ended_by:user` = unambiguous approval through the
  gate channel — no Gru provenance check needed).
- Evidence:
  - packet-plumber-routing-canon-amend (2026-08-10): "a lavish-gated docs deliverable dispatched into an absent-user window = long idle polls. The poll blocked ~6.5h overnight (user away, state.json frozen at open-time); re-running on each bash timeout is correct... just hold the gate, don't escalate as blocked, and verify the verdict via `~/.lavish-axi/state.json`."
- Why it makes future sessions smarter: stops a false "blocked" escalation
  on an overnight lavish gate and pins the approval signal.

### C8 — Squirrel emits its OWN per-module enum types (shadowing shared types) + shared-constructor enums can't be emitted at all
- Target: minion-field-notes.md (Tooling traps — the Squirrel triple-trap entry)
- Class-hint: AMEND-2026-07-31 (Squirrel triple-trap; 2026-08-08 addendum covered sql.gleam churn)
- Lesson: Two new Squirrel facets. (a) Squirrel generates its OWN
  `<Type>` inside each `<module>/sql.gleam`, mirroring the PG enum,
  SEPARATE from the `shared.*` type — status args to the sql functions
  must be `sql.Refused`/`sql.Objected`/etc. (the trigger module's
  `sql.Skipped` is the precedent), NOT the shared variants (type
  mismatch → "Expected sql.ReferenceCallStatus"). (b) When two PG enums
  SHARE constructor names (e.g. `reference_call_status` +
  `reference_call_outcome` both have `ManualRecorded`/...), Gleam forbids
  duplicate constructors in one module, so HEAD never had a Gleam
  outcome type — outcomes are passed as STRING +
  `NULLIF($n,'')::reference_call_outcome` cast. A bare
  `$n::reference_call_outcome` in a NEW query makes Squirrel emit the
  conflicting type → "Duplicate definition". Always use the
  NULLIF-string-cast convention for shared-constructor enum params.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "Squirrel generates its OWN `ReferenceCallStatus` type inside `reference_checks/sql.gleam` ... SEPARATE from `shared.reference_call.ReferenceCallStatus`. Status args to the sql functions must be `sql.Refused`/`sql.Objected`/etc. ... Don't pass the shared variants."
  - righttenantry-refcheck-rc3-5 (2026-08-10): "the `reference_call_*` status + outcome PG enums SHARE constructor names ... Gleam forbids duplicate constructors across types in one module, so HEAD never had a `ReferenceCallOutcome` Gleam type — outcomes are passed as STRING + `NULLIF($n,'')::reference_call_outcome` cast ... Always use the NULLIF-string-cast convention for outcome params."
- Why it makes future sessions smarter: two independent Squirrel type
  traps (2 sightings) — naming the per-module-shadow + the
  shared-constructor-emit failure saves a compile cycle each.

### C9 — `decode.null` does NOT exist in this Gleam version
- Target: minion-field-notes.md (Tooling traps — Gleam null-handling entry)
- Class-hint: AMEND-2026-07-31 (Gleam null-handling — `decode.subfield`/`decode.optional` fail-whole-decode)
- Lesson: `decode.null` does not exist in gleam/dynamic/decode (this
  Gleam version). To detect a JSON null in a Dynamic, use
  `decode.dict(...)` (succeeds on an object, fails on null) or the
  `decode.optional(string)` trick. Corollary from the same job: a
  `has_draft_key` completeness check must count object-valued answers
  (tenancy_period, rent_amount) as answered, not just strings.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "`decode.null` does NOT exist in gleam/dynamic/decode (this Gleam version). To detect a JSON null in a Dynamic, use `decode.dict(...)` ... or the `decode.optional(string)` trick."
- Why it makes future sessions smarter: a minion reaching for
  `decode.null` gets a compile error with no hint; the workaround is
  non-obvious.

### C10 — Postgres JSONB re-serialises with space-after-colon + may reorder keys → substring on `result::text` fails
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: NEW
- Lesson: Postgres JSONB re-serialises stored JSON with a **space after
  colons** (`"key": value`) and may reorder keys — so a substring
  assertion on `result::text` (e.g. `"schema_version":"refcall-v1"`)
  FAILS even when the value is correct. Use `result->>'field'`
  extraction (`test_db.query_text`) for JSONB field assertions; reserve
  raw-text substring matches for non-JSONB columns.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "Postgres JSONB re-serialises stored JSON with a **space after colons** (`\"key\": value`) and may reorder keys — substring assertions on `result::text` ... FAIL. Use `result->>'field'` extraction (`test_db.query_text`) for JSONB field assertions."
- Why it makes future sessions smarter: a flaky-looking JSONB assertion
  that "should match" is a storage-format artifact, not a data bug.

### C11 — `unitest.tag` needs a STRING LITERAL (static analysis, not runtime)
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: NEW
- Lesson: The integration-test skip via `unitest.tag` is STATIC
  ANALYSIS, not runtime: `use <- unitest.tag(tag)` (a const) does NOT
  skip under `gleam test` (runs + fails on no DB); only
  `use <- unitest.tag("integration")` (a literal) skips. A whole sweep
  suite can run+fail until the const is swapped for the literal.
- Evidence:
  - righttenantry-refcheck-rc3-5 (2026-08-10): "`unitest.tag` needs a STRING LITERAL: the integration-test skip is STATIC ANALYSIS, not runtime — `use <- unitest.tag(tag)` (a const) does NOT skip under `gleam test` (runs + fails on no DB); `use <- unitest.tag(\"integration\")` (literal) does. My 12 sweep tests ran+failed until I swapped the const for the literal."
- Why it makes future sessions smarter: the const-vs-literal distinction
  is invisible until CI/no-DB run; naming it saves a red sweep suite.

### C12 — Testing inline-Gleam-emitted JS under `node --test`: extract + unescape + eval the shipped literal
- Target: minion-field-notes.md (Tooling traps)
- Class-hint: NEW
- Lesson: To test the EXACT shipped bytes of inline JS emitted by a
  Gleam `<> "..."` string-literal block (e.g. a PostHog
  `sanitize_properties` scrub) under `node --test`: extract the literal
  block from the `.gleam` source (anchor on stable tokens like
  `sanitize_properties:function(p){` … `return scrub(p);`, span opening
  `<>` to the last literal's closing `"`), unescape Gleam escapes, eval
  it. Tests the real shipped bytes with no module refactor and zero leak
  risk on the defended invariant.
- Evidence:
  - righttenantry-apply-form-scrub-fix (2026-08-10): "Testing inline-Gleam-emitted JS under `node --test`: extract the `<> \"...\"` string-literal block from the .gleam source ... unescape Gleam escapes, eval it. Tests the EXACT shipped bytes with no module refactor and zero leak risk on the defended token-redaction invariant."
- Why it makes future sessions smarter: gives a repeatable harness for
  the inline-JS-in-Gleam pattern instead of a risky module refactor.

### C13 — `instanceof Node` blind under `node --test` → use `Object.prototype.toString.call`
- Target: minion-field-notes.md (Tooling traps — "Node tests blind to browser semantics" entry)
- Class-hint: AMEND-2026-08-03 (Node tests blind to browser-runtime semantics)
- Lesson: Reinforces with a concrete remedy. `instanceof Node` guards
  are BLIND under `node --test` (no `Node` global there — the exact
  Node-blind trap). For a DOM/host-object guard that must be
  runtime-tested in Node, use `Object.prototype.toString.call(o)`
  (plain-object check): skips ALL host objects, not just Nodes, and
  needs no browser shim. Prove the guard bites by neutering it in the
  shipped source and confirming the test goes red.
- Evidence:
  - righttenantry-apply-form-scrub-fix (2026-08-10): "`instanceof Node` guards are BLIND under `node --test` (no `Node` global there — the exact 'Node tests blind to browser semantics' trap). For a DOM/host-object guard that must be runtime-tested in Node, use `Object.prototype.toString.call(o)` ... Prove the guard bites by neutering it in the shipped source and confirming the test goes red."
- Why it makes future sessions smarter: a Node-testable host-object guard
  recipe that doesn't need a browser shim.

### C14 — Progressive-enhancement hidden field is INERT unless the populating JS runs on THAT page; `simulate.form_body` masks it
- Target: minion-field-notes.md (Tooling traps — "Node tests blind to browser semantics" entry)
- Class-hint: AMEND-2026-08-03 (Node tests blind; new flavor: server-side test helper masks client wiring)
- Lesson: A progressive-enhancement field rendered in the HTML is INERT
  unless the JS that populates it actually runs on that page. Concrete:
  `reference_form.js initBrowser` bailed on the review page (different
  testid) and `onSubmit` bound only `.ref-question` forms, so the review
  submit's `_focus_seconds` shipped dead (always 0). The integration
  test MASKED it via `simulate.form_body` (bypasses the browser). Any
  client-populated hidden field needs (a) the JS wiring on the SPECIFIC
  page that renders it, AND (b) a Node/browser-path test that drives the
  wiring seam — never rely on `simulate.form_body` alone. Also: a hidden
  field rendered on ONE form but NOT the form that POSTs the terminal
  action silently zeroes the downstream signal — render it on EVERY form
  that POSTs that action + assert end-to-end.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "a progressive-enhancement field rendered in the HTML is INERT unless the JS that populates it actually runs on that page. reference_form.js `initBrowser` bailed on the review page ... so the review submit's `_focus_seconds` shipped dead (always 0). The integration test MASKED it via `simulate.form_body`."
  - righttenantry-refcheck-rc3-4 (2026-08-10): "a hidden field rendered on ONE form ... but NOT the form that actually POSTs the terminal action ... silently zeroes a downstream signal. The integration test masked it by injecting the field manually."
- Why it makes future sessions smarter: a third Node-blind flavor (server
  test helper bypasses the browser seam) — the remedy is a
  page-specific wiring test, not relaxing gates.

### C15 — The double-scheme CTA trap (`https://https://domain/...`)
- Target: minion-field-notes.md (Recurring review findings)
- Class-hint: NEW
- Lesson: `origin_from_domain` returns scheme-full (`https://domain`),
  but `email_client.build_entity_url` prepends `https://` itself.
  Passing the scheme-full origin to ANY notification CTA builder yields
  `https://https://domain/...` — a dead link in every email. Pass the
  RAW `origin_domain` to `build_entity_url`; reserve `origin_from_domain`
  for message-body links (the invite base_url). The
  `notify_application_scored` precedent (ai_client.gleam) does it right;
  mirror it. (Shard calls it "the canonical double-scheme CTA trap" — a
  known RT pattern.)
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "the canonical double-scheme CTA trap — `origin_from_domain` returns scheme-full (`https://domain`), but `email_client.build_entity_url` prepends `https://` itself. Passing the scheme-full origin to ANY notification CTA builder yields `https://https://domain/...` — a dead link in every email."
- Why it makes future sessions smarter: one RT code navigation rule that
  prevents a class of dead-email-link blockers.

### C16 — Grep the SPECIFIC function name, not a generic token with many unrelated hits
- Target: minion-field-notes.md (Tooling traps / Conventions — ground-truth-first)
- Class-hint: AMEND-2026-07-31 (ground-truth-first)
- Lesson: When locating a code seam by grep, the generic token can have
  20+ unrelated hits across modules. Concrete: the PostHog
  `sanitize_properties` scrub is the ONLY inline-JS-in-Gleam scrub on
  `/apply`; grep `sanitize_properties` to find it — bare `scrub` has 20+
  hits (model-version scrub, Stripe/GoTrue PII scrub). Grep the specific
  identifier first; fall back to the generic only with a narrowing
  context flag.
- Evidence:
  - righttenantry-apply-form-scrub-fix (2026-08-10): "The PostHog `sanitize_properties` scrub is the ONLY inline-JS-in-Gleam scrub on `/apply`; grep `sanitize_properties` to find it — bare `scrub` has 20+ unrelated hits (model-version scrub, Stripe/GoTrue PII scrub, etc.)."
- Why it makes future sessions smarter: stops a minion editing the wrong
  `scrub` and shipping a no-op on the defended seam.

## Odin toolchain/API cluster (packet-plumber-v2) — NEW tooling traps

### C17 — Current Odin `core:testing` API form
- Target: minion-field-notes.md (Tooling traps — new "Odin" cluster)
- Class-hint: NEW
- Lesson: Current Odin `core:testing` = `testing.expect(t, ok, "msg")` /
  `testing.expectf(t, cond, fmt, args)` /
  `testing.expect_value(t, got, want)`. NOT `tfail`/`tfailf` (old /
  prototype), NOT method-call `t.expect(...)` (fails — use the qualified
  `testing.expect(t, ...)` form). `expect_value` takes NO message string
  (its 4th param is a `Source_Code_Location`).
- Evidence:
  - packet-plumber-v2-1.1-walking-skeleton (2026-08-1x): "Current Odin `core:testing` API = `testing.expect(t, ok, \"msg\")` ... NOT `tfail`/`tfailf` (old/prototype), NOT method-call `t.expect(...)` (fails — use the qualified `testing.expect(t, ...)` form)."
- Why it makes future sessions smarter: the prototype used the old API;
  every PP-v2 story minion would otherwise copy the stale form.

### C18 — Odin `delete` / `new(T)` memory semantics
- Target: minion-field-notes.md (Tooling traps — Odin cluster)
- Class-hint: NEW
- Lesson: `delete` on a `[dynamic]` is `delete(arr)` with NO `&` in
  current Odin; `new(T)` heap pointers can't be `delete`d at all —
  prefer stack locals (`x: T; defer run_destroy(&x)`) for test state and
  `defer delete(returned_dynamic)` for returned `[dynamic]`s (the test
  mem-tracker flags leaks as warnings).
- Evidence:
  - packet-plumber-v2-1.1-walking-skeleton (2026-08-1x): "`delete` on a `[dynamic]` field is `delete(arr)` with NO `&` in current Odin; `new(T)` heap pointers can't be `delete`d at all — prefer stack locals ... for test state and `defer delete(returned_dynamic)` for returned `[dynamic]`s (the test mem-tracker flags leaks as warnings)."
- Why it makes future sessions smarter: the `&`/no-`&` + heap-not-deletable
  rules are non-obvious and every PP-v2 test allocates dynamics.

### C19 — `package core` collides with Odin runtime `core`; the ODN-1 purity gate is import-grep + `nm`, not `-build-mode:obj`
- Target: minion-field-notes.md (Tooling traps — Odin cluster)
- Class-hint: NEW
- Lesson: `package core` COLLIDES with Odin's runtime `core` for
  `-build-mode:obj`/`-lib` output naming — those builds emit ONLY runtime
  objects, not the user package's code (vacuous but exit-0). The
  definitive ODN-1 purity gate is the import grep (`tools/lint.sh` gate
  1: zero forbidden imports) + `nm` of a binary that LINKS core
  (`odin build harness -out:bin/harness` → `_core::*` symbols present,
  ZERO raylib). Do NOT rename `package core` (architecture + prototype
  both pin it; `odin test core` + `import pp "../core"` work fine).
  Reconcile the §16.3 `-build-mode:obj` artifact gate in a later CI-gate
  story. Also: `odin build <pkg> -out:bin/x` fails with a clang linker
  error if `bin/` doesn't exist — `mkdir -p bin` first (bless goldens via
  `odin run harness -- save boot`, which compiles to a temp, no bin/
  needed).
- Evidence:
  - packet-plumber-v2-1.1-walking-skeleton (2026-08-1x): "`package core` COLLIDES with Odin's runtime `core` for `-build-mode:obj`/`-lib` output naming — those builds emit ONLY runtime objects... The definitive ODN-1 purity gate is the import grep ... + `nm` of a binary that LINKS core."
  - packet-plumber-v2-1.1-walking-skeleton (2026-08-1x): "`odin build <pkg> -out:bin/x` fails with a clang linker error if `bin/` doesn't exist — `mkdir -p bin` first."
- Why it makes future sessions smarter: a vacuous-but-exit-0 build gate
  is a silent false-pass; `nm` is the real purity proof.

### C20 — Odin nested procs are non-capturing
- Target: minion-field-notes.md (Tooling traps — Odin cluster)
- Class-hint: NEW
- Lesson: Odin nested procs are non-capturing — a `clone` proc defined
  inside `make_drift_mutations` couldn't see `src`. Lift helpers to
  module scope or pass params explicitly. (Unlike JS/Rust closures,
  Odin inner procs do NOT close over enclosing locals.)
- Evidence:
  - packet-plumber-v2-1.2-window-draw-pipe (2026-08-1x): "Odin nested procs are non-capturing — a `clone` proc defined inside `make_drift_mutations` couldn't see `src`; lift helpers to module scope or pass params explicitly."
- Why it makes future sessions smarter: the closure-reflex copies stale
  and compiles weirdly; one line saves the debug.

### C21 — Odin `make([]u8, len, allocator)` for a slice is finicky; prefer `[dynamic]` then `dyn[:]`
- Target: minion-field-notes.md (Tooling traps — Odin cluster)
- Class-hint: NEW
- Lesson: `make([]u8, len, allocator)` for a slice is finicky in this Odin
  build; prefer `make([dynamic]u8, len, allocator)` then pass `dyn[:]`
  (matches the core pattern that compiles cleanly).
- Evidence:
  - packet-plumber-v2-1.2-window-draw-pipe (2026-08-1x): "`make([]u8, len, allocator)` for a slice is finicky in this Odin build; prefer `make([dynamic]u8, len, allocator)` then pass `dyn[:]` (matches the core pattern that compiles cleanly)."
- Why it makes future sessions smarter: the slice-allocator overload
  bites silently; the `[dynamic]`-then-slice form is the known-good one.

### C22 — `free_all(context.temp_allocator)` per tick nukes fields read DURING the tick
- Target: minion-field-notes.md (Tooling traps — Odin cluster)
- Class-hint: NEW
- Lesson: A per-tick `free_all(context.temp_allocator)` nukes
  `demo.captures`/`draws` if they're temp-allocated. The 1.1 spine's
  per-tick free_all was safe because 1.1 demos had no dynamic fields;
  the moment a demo carries a field read DURING the tick loop, allocate
  it with `context.allocator` (persistent), not temp. Symptom:
  "captures=1" logged but no PNG written (the capture loop iterated
  freed memory).
- Evidence:
  - packet-plumber-v2-1.2-window-draw-pipe (2026-08-1x): "`free_all(context.temp_allocator)` per tick nukes demo.captures if they're temp-allocated ... allocate them with `context.allocator` (persistent), not temp. Symptom: 'captures=1' logged but no PNG written (the capture loop iterated freed memory)."
- Why it makes future sessions smarter: the determinism spine's
  per-tick free is load-bearing for every later PP-v2 story; the
  persistent-vs-temp allocator choice is the silent footgun.

### C23 — T2 pixel goldens need the rlsw SOFTWARE renderer (GPU raylib renders solid black headless)
- Target: minion-field-notes.md (Tooling traps — Odin/rlsw cluster; sibling to the Godot headless entry)
- Class-hint: NEW (2 sightings, same root cause — distinct engine from the Godot entry)
- Lesson: T2 pixel goldens need the rlsw software renderer via
  `tools/harness.sh` — `odin run harness` links the stock GPU
  `vendor:raylib` and renders a SOLID BLACK frame headless (no GPU
  context). Headless capture path: `rl.InitWindow` +
  `LoadImageFromScreen` (no GPU/display); port the prototype's
  `goldens.odin` (flip + BGRA→RGBA swizzle) verbatim; `CIRCLE16`-style
  constant arrays can't be indexed by a runtime index in Odin (assign to
  a local first). The SW raylib build (`tools/build_raylib_sw.sh`) takes
  ~40s + a github clone — kick it off in the BACKGROUND before coding.
- Evidence:
  - packet-plumber-v2-1.2-window-draw-pipe (2026-08-1x): "rlsw T2 capture path works headless via `rl.InitWindow` + `LoadImageFromScreen` ... port the prototype's `goldens.odin` (flip + BGRA→RGBA swizzle) verbatim ... The SW raylib build (`tools/build_raylib_sw.sh`) takes ~40s + a github clone; kick it off in the background before coding."
  - packet-plumber-v2-1.3-packet-flow (2026-08-1x): "T2 pixel goldens need the rlsw software renderer via `tools/harness.sh` — `odin run harness` links the stock GPU `vendor:raylib` and renders a SOLID BLACK frame headless (no GPU context)."
- Why it makes future sessions smarter: 2 independent sightings — the
  GPU-black-frame failure is the raylib analog of the Godot headless
  trap, and the 40s SW build should run in the background.

### C24 — The pinned `.odin-version` resolves to the SAME nightly already on the machine
- Target: minion-field-notes.md (Tooling traps — Odin cluster)
- Class-hint: NEW
- Lesson: The pinned `.odin-version` `dev-2026-08` downloads as the SAME
  `nightly+2026-08-06` / `902106f` that's already on the machine — so the
  local toolchain IS the pinned release. A T2 golden mismatch is a REAL
  diff, not a version drift; don't burn time re-pinning to explain a
  pixel diff.
- Evidence:
  - packet-plumber-v2-1.3-packet-flow (2026-08-1x): "the pinned `.odin-version` `dev-2026-08` downloads as the SAME `nightly+2026-08-06` / `902106f` that's already on the machine — so the local toolchain IS the pinned release; a T2 mismatch is a real diff, not a version drift."
- Why it makes future sessions smarter: stops a false "version drift"
  rabbit hole on a real pixel diff.

## ADK (RT-Agents) cluster — NEW tooling traps

### C25 — ADK `ctx.state` is a per-node SNAPSHOT, not live; read cross-node gate state via `ctx.session.state`
- Target: minion-field-notes.md (Tooling traps — new "ADK" cluster)
- Class-hint: NEW
- Lesson: ADK `ctx.state` is a per-node SNAPSHOT, not live. A child
  agent's `output_key` write (via `ctx.run_node`) lands on the live
  `ctx.session.state` but is absent from the node's `ctx.state` snapshot
  → `ctx.state.get(child_key)` returns `None` right after `run_node`. The
  RightTenantry convention (documented at `agent.py:263`/:396) is raw
  `ctx.session.state` for ALL cross-node gate state — the compliance
  review read violated it. When editing ADK Workflow gates: read child
  output via `ctx.session.state`, NEVER `ctx.state`.
- Evidence:
  - righttenantryagents-boundary-gate-state-fix (2026-08-1x): "ADK `ctx.state` is a per-node SNAPSHOT, not live. A child agent's `output_key` write ... lands on the live `ctx.session.state` but is absent from the node's `ctx.state` snapshot → `ctx.state.get(child_key)` returns `None` right after `run_node` ... When editing ADK Workflow gates: read child output via `ctx.session.state`, never `ctx.state`."
- Why it makes future sessions smarter: the snapshot/live split is the
  core ADK state footgun; `ctx.state` looks right and fails silently.

### C26 — InMemory recorder harness CAN'T reproduce the ctx.state snapshot bug; build a divergent fake ctx
- Target: minion-field-notes.md (Tooling traps — ADK cluster)
- Class-hint: NEW (test-harness corollary to C25)
- Lesson: `tests/unit/test_workflow_pipeline.py`'s `_Recorder` stubs
  SHARE the live dict, so `ctx.state` sees child writes and the C25 bug
  is invisible there. To regression-guard a state-view fix, build a
  divergent fake ctx (stale `State({}, {})` snapshot + live
  `session.state` dict) and assert the gate reads through
  `ctx.session.state` — see `tests/unit/test_gate_state_marshalling.py`.
  Reaching attempt-1 in a gate-loop regression needs BOTH `scrub_*`
  (return touched) AND `_run_compliance_repair` (return True) to succeed
  on attempt 0 (no other continue path); the boundary scrub reads
  `ctx.state` (stale), so the `_DivergentCtx` harness needed an optional
  `stale_seed` to carry a verifier output.
- Evidence:
  - righttenantryagents-boundary-gate-state-fix (2026-08-1x): "The InMemory recorder harness can't reproduce this. ... `_Recorder` stubs share the live dict, so `ctx.state` sees child writes and the bug is invisible there. To regression-guard a state-view fix, build a divergent fake ctx (stale `State({}, {})` snapshot + live `session.state` dict)."
  - righttenantryagents-boundary-gate-slot-clear (2026-08-1x): "To reach attempt-1 in the gate-loop regression test, BOTH `scrub_*` ... AND `_run_compliance_repair` ... must succeed on attempt 0 — there's no other continue path."
- Why it makes future sessions smarter: the stock test harness gives a
  false-green on the exact bug class; the divergent-ctx recipe is the
  only reproduction.

### C27 — ADK `output_key` write is conditional but `after_agent_callback` ALWAYS fires → stale-slot; per-attempt pop is hygiene
- Target: minion-field-notes.md (Tooling traps — ADK cluster)
- Class-hint: NEW
- Lesson: ADK skips the `output_key` write on empty chunks /
  schema-validation-fail / tool-call-only responses (documented at
  `agents/anonymizer.py:313`, `pii_reviewer.py:248`), while the judge's
  `after_agent_callback` (which writes the verdict stamp via
  `_stamp_review_verdict`) ALWAYS fires. So a clean attempt can leave the
  PRIOR dirty review in the slot while stamping clean — finalize reads
  non-None dirty → fail-close. The per-attempt `pop` is necessary
  hygiene, not paranoia. The bug fingerprint (telemetry asymmetry): a
  `boundary_gate.exhausted{review_parseable=False, violations=0}`
  co-occurring with `compliance.review_completed{passed:true}` — the
  judge's callback is a reliable independent witness (reads its own delta
  with the output_key) even when the pipeline node's `ctx.state` reads
  None.
- Evidence:
  - righttenantryagents-boundary-gate-slot-clear (2026-08-1x): "ADK skips the `output_key` write on empty chunks / schema-validation-fail / tool-call-only responses ... while the judge's `after_agent_callback` ... ALWAYS fires. So a clean attempt can leave the prior dirty review in the slot while stamping clean ... The per-attempt `pop` is necessary hygiene, not paranoia."
  - righttenantryagents-boundary-gate-state-fix (2026-08-1x): "The judge's own `after_agent_callback` IS a reliable independent witness ... `compliance.review_completed{passed:true}` co-occurring with `boundary_gate.exhausted{review_parseable=False, violations=0}` is the exact bug fingerprint."
- Why it makes future sessions smarter: the conditional-write /
  always-fire asymmetry is the root of a class of stale-state
  fail-closes; the telemetry fingerprint pinpoints it in prod logs.

---

## minion-field-notes.md — Conventions that saved time

### C28 — A planning doc's recent DATE doesn't mean it's on the current stack — check which arch file it cites + grep its code samples
- Target: minion-field-notes.md (Conventions — ground-truth-first)
- Class-hint: AMEND-2026-08-07 (verify-briefing-premises; 2026-08-09 addendum listed claim types) — new claim type: stale-stack planning doc
- Lesson: v1 sprint-plan/stories were dated AFTER the Odin pivot
  (2026-08-08) but drafted in Godot/GDScript (`RefCounted`, `AC-FinLT`,
  `scripts/core/`) and cited `architecture-v1.md` (the superseded
  GL5.2/Godot arch), NOT `odin-architecture-v1.md` — and sat on the
  reversed BFS+RR/LB routing. A "recent date" on a planning doc does NOT
  mean it's on the current stack. Before trusting a planning/arch doc's
  engine/routing: check WHICH architecture file it cites + grep its code
  samples for the current language/API.
- Evidence:
  - packet-plumber-sprint-replan-v2 (2026-08-11): "v1 sprint-plan/stories were dated *after* the Odin pivot (2026-08-08) but drafted in Godot/GDScript (`RefCounted`, `AC-FinLT`, `scripts/core/`) and cited `architecture-v1.md` (the GL5.2 Godot arch), NOT `odin-architecture-v1.md` ... A 'recent date' on a planning doc does NOT mean it's on the current stack."
- Why it makes future sessions smarter: a new claim-type for the
  verify-premises convention — date != currency after a pivot.

### C29 — A briefing can name the WRONG identifier/state-key — verify against the code, don't follow key names blindly
- Target: minion-field-notes.md (Conventions — ground-truth-first)
- Class-hint: AMEND-2026-08-07 (verify-briefing-premises) — new claim type: wrong identifier
- Lesson: The briefing named the WRONG state key for the final gate
  (`STATE_FINAL_OUTPUT` — that's the audited v4 payload the scrubber
  mutates). The final gate's review slot is `STATE_FINAL_COMPLIANCE_REVIEW`
  (what `finalize_final_gate` reads). Popping `STATE_FINAL_OUTPUT` would
  have emptied the reviewer's `{final_output}` placeholder. Verify
  identifier/key names against the code before acting; a briefing's key
  names are a hint, not a contract.
- Evidence:
  - righttenantryagents-boundary-gate-slot-clear (2026-08-1x): "The briefing named the WRONG state key for the final gate (`STATE_FINAL_OUTPUT` — that's the audited v4 payload the scrubber mutates). The final gate's review slot is `STATE_FINAL_COMPLIANCE_REVIEW` ... Verify against the code, don't blindly follow the briefing's key names."
- Why it makes future sessions smarter: acting on a wrong key name can
  mutate the wrong slot; grep the symbol in the code first.

### C30 — Verify a briefing's MECHANISM claims against disk (prefix-match registries, not per-arm)
- Target: minion-field-notes.md (Conventions — ground-truth-first)
- Class-hint: AMEND-2026-08-07 (verify-briefing-premises) — new claim type: wrong mechanism model
- Lesson: The briefing's "register EACH route in ALL three registries"
  rested on a per-arm mental model; the registries are actually
  PREFIX-MATCHED `"reference", ..` (one arm covers any depth). The router
  is the only per-arm registry. Verify the briefing's mechanism claims
  against disk before acting — the work was router arms + coverage tests,
  NOT registry edits (which would have been dead code). Same root lesson
  as the verify-premises convention, now with a concrete routing
  instance.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "the briefing's 'register EACH route in ALL three registries' rests on a per-arm mental model; the registries are **prefix-matched** `\"reference\", ..` (one arm covers any depth). The router is the only per-arm registry. Verify the briefing's mechanism claims against disk before acting."
- Why it makes future sessions smarter: a per-arm assumption would have
  produced dead-code registry edits; disk shows the prefix-match truth.

### C31 — Disambiguate same-letter namespaces + superseded-vs-live docs before editing
- Target: minion-field-notes.md (Conventions — ground-truth-first / canon)
- Class-hint: AMEND-2026-08-07 (verify-premises) — new claim types: namespace collision + superseded doc
- Lesson: Two namespace/doc traps. (a) Disambiguate the two "E"
  namespaces before editing — the briefing's "E1/E29" were the ARCH
  edge-case behaviors (E1–E32 table at §11.7 + §6.2), NOT the GDD epics
  (E1–E11 in epics.md). (b) `architecture-v1.md` is the SUPERSEDED
  GL5.2/Godot arch (ADRs); the live canon with the ODN-* decisions + E1–E32
  edge cases is `odin-architecture-v1.md` — only the latter was amended;
  the former stays historical (flagged in the PR). When a project has
  same-letter namespaces OR superseded-vs-live doc pairs, name which is
  which in the PR and edit only the live one.
- Evidence:
  - packet-plumber-routing-canon-amend (2026-08-10): "disambiguate the two 'E' namespaces before editing — the briefing's 'E1/E29' were the **arch edge-case behaviors** ... NOT the GDD epics ... And `architecture-v1.md` is the SUPERSEDED GL5.2/Godot arch (ADRs); the live canon ... is `odin-architecture-v1.md` — only the latter was amended."
- Why it makes future sessions smarter: editing the superseded doc or the
  wrong namespace ships a no-op amendment.

### C32 — Canon-amendment blast radius exceeds named sections; ASCII box edits MUST be width-preserving
- Target: minion-field-notes.md (Conventions — canon-doc amendment craft, 2026-08-09 entry)
- Class-hint: AMEND-2026-08-09 (canon-doc amendment craft)
- Lesson: Reinforces the 2026-08-09 blast-radius lesson with new craft
  detail. Here the briefing named GDD §M3/§M5 + arch §6.2/§6.3/ODN-9/10/E1/E29,
  but the radius ALSO caught: epics.md (E1.4/E1.5/E2.3/test-contracts),
  §4 ASCII diagrams (**box edit MUST be width-preserving**:
  `span, LB)`→`span,bndl)` kept 13 chars — a width-shift breaks the
  diagram alignment), §5.1 ODN-9/10 summary rows, §8.1 catalog + §8.2
  data model + §15.1 coverage, and decision-log.md
  (history-preserving supersession APPEND, not a rewrite — matches the
  project's amendment pattern).
- Evidence:
  - packet-plumber-routing-canon-amend (2026-08-10): "canon-amendment blast radius always exceeds the briefing's named sections — grep-bound it ... §4 ASCII diagrams (box edit MUST be width-preserving: `span, LB)`→`span,bndl)` kept 13 chars) ... decision-log.md (history-preserving supersession APPEND, not a rewrite — matches the project's amendment pattern)."
- Why it makes future sessions smarter: width-preserving ASCII edits +
  history-preserving append are two new craft rules for the amendment
  convention.

### C33 — Pre-emptive no-overlap doc placement under an open sibling PR
- Target: minion-field-notes.md (Conventions — canon-doc amendment craft)
- Class-hint: AMEND-2026-08-09 (canon-doc amendment craft) — new sub-technique
- Lesson: When amending a doc an open sibling PR also touches, grep the
  sibling's diff hunks first and place inserts OUTSIDE them. Concrete:
  a single §M5 insert placed at the END of §M5 (after the V2 paragraph),
  deliberately clear of #18's archetype-table hunk → `gdd.md` auto-merged
  CLEAN; the only conflict was a dual tail-append on `decision-log.md`
  (both PRs appended at EOF), trivial to resolve (keep both).
- Evidence:
  - packet-plumber-gdd-mechanics-amend (2026-08-10): "Pre-emptive no-overlap placement pays off under an open sibling PR. I placed my single §M5 insert at the END of §M5 ... deliberately clear of #18's archetype-table hunk → `gdd.md` auto-merged CLEAN ... When amending a doc an open sibling PR also touches, grep the sibling's diff hunks first and place inserts outside them."
- Why it makes future sessions smarter: a cheap pre-flight that turns a
  conflict-rebase into a clean auto-merge.

### C34 — id-0 sentinel: 0 is a valid id, not a sentinel; the red→green is the negative-control proof
- Target: minion-field-notes.md (Conventions — prove-tests-bite, 2026-08-09 entry)
- Class-hint: AMEND-2026-08-09 (prove a test/guard actually BITES) — new negative-control example
- Lesson: PP node/pipe ids are 0-based (first spawned node = id 0, first
  pipe = id 0), so `edge==0` / `at_node==0` CANNOT be the on-edge/at-node
  sentinel — a packet forwarded onto pipe id 0 looked "at a node" and
  never moved. Use an explicit `on_edge: bool` flag (or a +1 id scheme).
  General: 0 is a valid id, not a sentinel. The flow tests went RED →
  GREEN on this fix — the red was the negative-control proof the tests
  bite (reinforces the prove-tests-bite convention).
- Evidence:
  - packet-plumber-v2-1.3-packet-flow (2026-08-1x): "id-0 sentinel trap (bit me, then the tests caught it): PP node/pipe ids are 0-based ... so `edge==0` / `at_node==0` CANNOT be the on-edge/at-node sentinel ... Use an explicit `on_edge: bool` flag ... The flow tests went red → green on this fix; the red was the negative-control proof the tests bite."
- Why it makes future sessions smarter: a second concrete negative-control
  story for the prove-tests-bite convention + the 0-is-valid-id rule.

### C35 — A mandate term is precise, not absolute — read the rule's exact scope before extending a ban
- Target: minion-field-notes.md (Conventions — ground-truth-first)
- Class-hint: NEW (generalizable from a PP instance)
- Lesson: "No BFS legacy" is precise, not absolute. The mandate bans the
  prototype's spawn-time BFS route cached per packet + the RR/weighted LB
  at parallel pipes. It does NOT ban a deterministic SPF computing the
  forwarding table internally — arch ODN-10 rule 1 explicitly permits
  `(junction,dst)→next hop` via deterministic BFS/SPF (insertion-order
  tie-breaks). State a ban's exact scope precisely in any plan, or a
  reviewer flags a phantom contradiction with the mandate. Generalizes:
  a named prohibition has a defined boundary — grep the rule's
  enumerated scope, don't over-apply it to permitted internal uses.
- Evidence:
  - packet-plumber-sprint-replan-v2 (2026-08-11): "'No BFS legacy' is precise, not absolute. The mandate bans the prototype's spawn-time BFS route cached per packet + the RR/weighted LB at parallel pipes. It does NOT ban a deterministic SPF computing the forwarding table internally ... State this precisely in any routing plan or a reviewer flags a phantom contradiction with the 'no BFS' mandate."
- Why it makes future sessions smarter: over-applying a ban wastes a
  rework cycle on a phantom contradiction.

### C36 — Derived data must NOT be hashed if replay must stay stable; confirm canon structurally (grep, not prose)
- Target: minion-field-notes.md (Conventions — ground-truth-first / determinism)
- Class-hint: NEW
- Lesson: The forwarding table is DERIVED from the topology → not hashed
  (hashing it would bind replay to the build algorithm). Confirm canon
  structurally via grep, not just prose: `core/routing.odin` +
  `core/flow.odin` have NO `route[]` field on Packet, NO
  `compute_route` BFS-on-packet, NO rng draw in routing/flow (ECMP hash
  is slice 2). For any determinism spine, derived/cached data that could
  vary by build algorithm stays OUT of the replay hash.
- Evidence:
  - packet-plumber-v2-1.3-packet-flow (2026-08-1x): "Per-hop forwarding confirmed structurally (grep, not just prose): `core/routing.odin` + `core/flow.odin` have NO `route[]` field on Packet ... The forwarding table is DERIVED from the topology → not hashed (hashing it would bind replay to the build algorithm)."
- Why it makes future sessions smarter: a determinism-design rule
  (derived ≠ hashed) + the grep-not-prose verification habit.

## PP-v2 determinism spine (load-bearing for every later story)

### C37 — The replay gate re-creates run-setup but NOT demand by default; thread every run-setup through BOTH live + replay
- Target: minion-field-notes.md (Tooling traps — PP determinism, or a PP-specific note)
- Class-hint: NEW
- Lesson: The replay gate re-creates run-setup (fixture) but NOT flow
  demand by default. The flow demand is run-setup (like the fixture),
  NOT in the action log — so ODN-11 replay diverged at tick 1 until the
  demo's `spawn` intents were threaded through `replay_hashes` (live
  lowers them via `lower_spawns`, replay re-creates them identically).
  Any future run-setup added to the sim (director plans, etc.) needs the
  same treatment in BOTH the live + replay paths. (The spine's `step` is
  a heartbeat — one owned-RNG draw/tick folded into a `tick_nonce`
  state field — tying the RNG into the step path so replay-equality is
  non-vacuous.)
- Evidence:
  - packet-plumber-v2-1.3-packet-flow (2026-08-1x): "The replay gate re-creates run-setup (fixture) but NOT flow demand by default ... so the ODN-11 replay diverged at tick 1 until I threaded the demo's `spawn` intents through `replay_hashes` ... Any future run-setup added to the sim ... needs the same treatment in BOTH the live + replay paths."
  - packet-plumber-v2-1.1-walking-skeleton (2026-08-1x): "The spine's `step` is a heartbeat (one owned-RNG draw/tick folded into a `tick_nonce` state field) — it ties the RNG into the step path so replay-equality is non-vacuous."
- Why it makes future sessions smarter: the determinism spine is
  load-bearing for every PP-v2 story; a new run-setup that bypasses
  replay_hashes silently breaks ODN-11.

---

## AGENTS.md gotchas

### C38 — Conflict-sensor rebase is the MINION's job, not Silas's
- Target: AGENTS.md gotchas (Dispatch & handover)
- Class-hint: NEW
- Lesson: A briefing may SAY "Silas rebases your branch at PR time"
  (narrative), but the playbook's conflict-sensor section relays
  "rebase onto <base>, force-push" to the MINION pane — the minion owns
  the rebase + conflict resolution. Don't wait for Silas; when #18 merged
  mid-job, the minion was already mid-rebase when his relay arrived.
  (`git rebase origin/<base>` → resolve → `git push --force-with-lease`.)
- Evidence:
  - packet-plumber-gdd-mechanics-amend (2026-08-10): "Conflict-sensor rebase is the MINION's job, not Silas's. A briefing may say 'Silas rebases your branch at PR time' (narrative), but the playbook's conflict-sensor section relays 'rebase onto <base>, force-push' to the MINION pane — the minion owns the rebase + conflict resolution. Don't wait for Silas."
- Why it makes future sessions smarter: a minion waiting on Silas for its
  own rebase stalls the PR; the minion owns it.

### C39 — A sheep can hit the provider quota wall MID-TURN; check the shard FILE exists, not just pane status, before closing it
- Target: AGENTS.md gotchas (new "Dreaming (Bob)" subsection, or Provider incidents) — Bob-specific ops
- Class-hint: NEW
- Lesson: A sheep can hit the provider quota wall MID-TURN (kimi 402 JSON
  error in-pane, status `done`, shard unwritten). A one-word nudge
  ("go"/continue) after the quota returns revives it mid-work with ~zero
  loss. Before closing a sheep: check the shard FILE exists (not just
  the pane status — a quota-walled sheep shows `done` with an empty
  shard).
- Evidence:
  - dream-2026-08-09 (2026-08-09): "a sheep can hit the provider quota wall MID-TURN (kimi 402 JSON error in-pane, status done, shard unwritten) — a one-word nudge ('go'/continue) after the quota returns revives it mid-work; check the shard FILE exists, not just the pane status, before closing a sheep."
- Why it makes future sessions smarter: a quota-walled sheep at `done`
  with no shard is invisible to status-only checks; the file check is the
  real completion signal.

### C40 — Diff the cloned store against LIVE at dream pass start (store==live check)
- Target: AGENTS.md gotchas (new "Dreaming (Bob)" subsection) — Bob ops safety
- Class-hint: NEW
- Lesson: Diff the cloned store against LIVE at pass start (store==live
  check) — cheap, and it makes the close-out store→live copy provably
  safe against concurrent Silas gotcha edits (if Silas wrote a new
  gotcha between clone and close-out, the diff-at-start + diff-at-end
  pair surfaces the divergence instead of clobbering it).
- Evidence:
  - dream-2026-08-09 (2026-08-09): "diff the cloned store against LIVE at pass start (store==live check) — cheap, and it makes the close-out store→live copy provably safe against concurrent Silas gotcha edits."
- Why it makes future sessions smarter: prevents a store→live copy from
  silently reverting a concurrent Silas gotcha edit.

### C41 — A lavish iteration loop is sequential; mega-minions don't speed it up — defer during a concurrent glm Perkins round
- Target: AGENTS.md gotchas (Provider incidents — glm) OR minion-field-notes (Conventions)
- Class-hint: NEW (ops) + REINFORCE (glm 429-avoidance)
- Lesson: A human-in-the-loop lavish iteration loop is sequential by
  nature (annotate→apply→react), so mega-minions DON'T speed it up. A
  glm-5.2 single-pane built a ~100KB faithful JS sim (BFS
  `compute_route`, `pick_pipe`/`rr_next`, `qos_allocate` WFQ, severance
  reroute) fine end-to-end as ONE file via the `write` tool (file write,
  not a pipe → no 85KB pipe-buffer truncation); `node --check` the
  extracted `<script>` before serving. Correctly deferred entirely during
  a concurrent Perkins glm-5.2 round per Silas's ruling (429-avoidance),
  then lifted; never needed. Reinforces the glm 429-avoidance rule: when
  glm-5.2 is running a Perkins round, don't spawn a concurrent glm lavish
  job.
- Evidence:
  - packet-plumber-routing-explorer (2026-08-10): "glm-5.2 single-pane built a ~100KB faithful JS sim ... fine end-to-end; a human-in-the-loop lavish iteration loop is sequential by nature (annotate→apply→react), so mega-minions DON'T speed it up — correctly deferred entirely during a concurrent Perkins glm-5.2 round per Silas's ruling (429-avoidance), then lifted; never needed."
- Why it makes future sessions smarter: stops spawning mega-minions on a
  loop that can't parallelize, and honors the glm 429-avoidance window.

### C42 — Lavish interactive SVG: parallel edges overlap unless fanned perpendicular; proximity-check oscillates → track explicit from/to
- Target: minion-field-notes.md (Tooling traps — lavish/game-animation; domain-specific, surface for completeness)
- Class-hint: NEW (domain-specific — game/SIM visualization)
- Lesson: Two lavish SVG-sim rendering traps. (a) Parallel pipes between
  the same node pair overlap into ONE visible line unless you fan them
  perpendicular — compute each pipe's arc offset from sibling count:
  `(idx-(n-1)/2)*spacing`. (b) A proximity-check
  (`Math.abs(p.x-n.x)<8`) for packet-travel direction OSCILLATES (flips
  the from/to every other tick → packet jitters in place, looks "no
  animation") — track explicit `fromNode`/`toNode` per edge instead
  (mirror the real `current_node` walk).
- Evidence:
  - packet-plumber-routing-explorer (2026-08-10): "lavish interactive SVG sims — parallel pipes between the same node pair overlap into ONE visible line unless you fan them perpendicular (compute each pipe's arc offset from sibling count: `(idx-(n-1)/2)*spacing`); and a proximity-check (`Math.abs(p.x-n.x)<8`) for packet-travel direction OSCILLATES (flips the from/to every other tick → packet jitters in place ...) — track explicit `fromNode`/`toNode` per edge instead."
- Why it makes future sessions smarter: two non-obvious SIM-rendering
  traps that present as "no animation" / "missing edge" with no error.
