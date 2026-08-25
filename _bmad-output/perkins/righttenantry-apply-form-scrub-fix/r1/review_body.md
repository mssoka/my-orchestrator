## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-apply-form-scrub-fix
**Reviewed sha:** `7870f90`
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests). No failed lenses.
**Verification:** 5/11 reviewer findings survived code re-verification. 6 discarded (4 false-positives where the reviewer lacked source access or misread the snippet; 2 speculative with no grounded scenario; 1 out-of-scope pre-existing comment).

### Lens-guard checks (the load-bearing invariants — verified directly against the worktree)

- **Token/URL redaction did NOT regress.** Traced the guard against every value class: `Object.prototype.toString.call(o)` recurses only into `[object Object]` and `[object Array]`; every host object is returned untouched. Redaction targets all live in plain-object string properties (`attr__data-resume-token` keys, `/resume/<tok>` and `/draft-erasure/<tok>` URL strings), so they are still walked. Runtime test asserts keys + URLs incl. nested arrays — green.
- **No second ticking copy.** `grep -rn sanitize_properties server/src server/priv/static` returns exactly ONE hit (`form_view.gleam:278`). The Makefile/Dockerfile `RT_ANALYTICS` perl (SPA-shell PostHog init) has no scrub. `posthog_js_snippet.gleam`, `tracking_snippets.gleam`, `draft_view.gleam`, `form_pages.gleam` carry no redaction logic.
- **Regression test is real, not tautological.** Extracts the exact shipped bytes (anchors resolve verbatim), the fake DOM element reproduces the failure mode (throw-on-set `outerText` + `[object HTMLDivElement]` toStringTag + enumerable DOM keys), the negative control genuinely bites (an unguarded scrub throws and fires the setter — proving the green tests mean something), and the test is wired into CI (`make test` -> `test-js` -> globs `scripts/js-tests/*.test.js`; `test.yml:131` runs `make test`).
- **Build/tests green.** `node --test scripts/js-tests/apply_event_scrub.test.js` = 5/5 pass. `gleam test --module form_view_test` = 37/37 pass (incl. new structural pin). Server compiles (warnings are pre-existing, unrelated files).

### Blockers (0)

None.

### Warnings (0)

None.

### Notes (5) — all optional, non-blocking

1. **[edge] Cyclic plain-object/array properties would overflow the scrub stack** (`form_view.gleam:306`). The recursion has no visited-set. Pre-existing (pre-fix code identical), not realistic for JSON PostHog event properties, and the worst case is one event capture throwing inside PostHog's own try/catch (not a form collapse). Optional `WeakSet` guard if cycles ever become plausible; safe to defer.

2. **[architecture] Test's hand-rolled unescape only maps `\n \t \r`** (`apply_event_scrub.test.js:75-81`). Verified correct for the shipped snippet (only backslash-doubled escapes present; `\/` and `\s` are reproduced exactly). Pure forward-looking fragility: a future `\u`/`\x` escape added to the snippet would be silently mangled. The load+eval would still fail loudly on a functional break. Low priority.

3. **[architecture] Root-cause narrative triplicated** (`form_view.gleam:281-299`, js-test header `1-22`, `form_view_test.gleam:737-746`). Three near-verbatim copies will drift over time. Each is locally justified, so this is a minor DRY note only. Optional: trim the two test-site copies to a one-line pointer.

4. **[tests] Negative control is hand-written pre-fix code, not derived from shipped-minus-guard** (`apply_event_scrub.test.js:232-248`). A future refactor of the shipped scrub shape could leave the control non-representative. Low impact: the control's job (proving the fake element bites) does not depend on the redaction regex. Optional: derive it by stripping the two guard lines from the loaded shipped bytes.

5. **[tests] Advisory test gate: PASS.** P0 100%. The regression test extracts shipped bytes, exercises the failure mode, the negative control bites, and redaction is asserted for keys + URLs incl. nested arrays.

### Considered but not counted (informational)

- The security lens flagged `draft_handler.gleam:435` as a stale comment (it claims the resume page "carries the token in data-resume-token"). Premise is actually TRUE: the resume page now carries the token in `window.__rtResumeToken` (`form_pages.gleam:459`), not a DOM attribute. But that line is **not in this diff** (pre-existing comment in an untouched file) and has no bearing on the fix, so it is out of scope here. Worth a separate one-line cleanup PR.

### Verdict: READY TO MERGE

The fix is correct and complete, the diagnosis-pinned guard is the right shape, the load-bearing redaction invariant is verified intact, there is exactly one scrub copy in the codebase, and the regression test genuinely bites and runs in CI. The 5 remaining notes are all optional polish. Recommend merge once Silas confirms.

---

Address findings and push, or reply to dismiss individual notes. Round 2 will re-verify any carried-forward items.
