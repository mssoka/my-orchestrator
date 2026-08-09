## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-form-resume-progress-fix · **Reviewed sha:** 7bf8571 · **Reviewers:** 7/7 completed
**Verification:** 6/8 findings confirmed against the code — 2 discarded as false-positive

The core fix verifies clean: `sections` is built 1:1 from `sectionEls` (same order, no filtering), the `?stepper=off` and `formJsRan` bails both precede `var done = seedDoneStates(...)`, the consent guard leans on a documented server invariant, and I independently re-ran `node --test scripts/js-tests/*.test.js` at the reviewed sha — 107/107 pass. Edge, acceptance, security, and architecture lenses all returned empty.

### Blockers (0)

None.

### Warnings (1)

1. **form-errors initial-paint no-seed has no automated pin** [tests] — `server/priv/static/form_stepper.js:476`. The `i !== leaving` guard in `show()` is the only thing stopping a first-paint green on a form-errors render that lands on a gating-complete-but-server-invalid step (initial paint calls `show(model.current(), { initial: true })`). `show()` is an `initBrowser` closure, unreachable from node tests, and no YAML scenario outside `round-trip` asserts segments — the frozen-intent "form-errors seeds nothing" rule is manual-replay-only (evidence README rows 07–08). A guard deletion would regress silently. Fix: add a form-bug-hunt `stepper: true` scenario that submits with a filled-but-invalid field and asserts the error-page landing step lacks `.stepper-segment-done` on arrival.

### Notes (5)

1. **Resume pin omits the vacuous-complete segments** [blind] — `.pi/skills/form-bug-hunt/scenarios/save-resume/round-trip.yaml:45`. The arrival assertion covers steps 1–3 only; steps 5–6 arriving green (the gating-mirror behaviour your own README arrival read shows: `[done, done, active, plain, done, done, …]`) is pinned nowhere, so reverting vacuous seeding wouldn't fail the scenario. Extending the arrival assertion to steps 5–6 would pin the current sanctioned behaviour while the product question stays open.
2. **`sectionComplete` name collision with the analytics mirror** [codebase] — `server/priv/static/form_stepper.js:307` vs `server/priv/static/apply_analytics.js:254`. Same name, deliberately opposite vacuous-section semantics (stepper: vacuous-true + consent guard; analytics: vacuous-false), in two files convention says are KEEP-IN-SYNC mirrors. No runtime conflict (both IIFE-wrapped), but a future sync pass copying one predicate into the other would silently flip a contract. A one-line cross-reference comment in each would prevent it.
3. **Evidence README miscounts the suite** [codebase] — `_bmad-output/implementation-artifacts/e2e-resume-progress-2026-08-04/README.md:48`. "The other 56 scenarios" — actually 57 (59 YAMLs minus the 2 `stepper: true` drives; verified against the tree). The substantive claim (stepper=off bails before the changed code) is verified true.
4. **Spec Code Map omits `rederiveDone`** [blind] — `_bmad-output/implementation-artifacts/spec-form-resume-progress-fix.md:55` lists "new pure exports `sectionComplete` + `seedDoneStates`" while the spec's own task bullet and the export block include all three. Trivial self-contradiction in the shipped spec.
5. **Advisory test gate: PASS** [tests] — P0 100% (seeding, empty-leave-stays-white, render line — 9 new node tests + E2E pin), P1 ~90% (the warning above is the gap). 107/107 node tests independently re-verified.

### Reviewer agreement

No multi-source findings this round. Two findings were discarded in verification: the "byte-identical confirmation screenshots" claim (the confirmation page renders only vacancy-scoped content — identical PNGs across two drives of the same seeded vacancy are the deterministic expected render, not a missing capture) and the "`sectionEls`/`sections` index drift" claim (the diff didn't show it, but `sections` is built 1:1 via `sectionEls.map` — verified in the worktree).

**Verdict:** READY TO MERGE

_Core behaviour is correct, well-pinned, and spec-faithful; the one warning is a durable-pin gap for a regression guard, not a defect. The vacuous-complete green-on-arrival question stays with the human as intended._

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
