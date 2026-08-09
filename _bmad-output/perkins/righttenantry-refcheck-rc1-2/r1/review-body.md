## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-rc1-2 · **Reviewed sha:** a8e8666 · **Reviewers:** 7/7 completed
**Verification:** 13/16 findings confirmed against the code — 3 discarded as false-positive

### Blockers (0)

None.

### Warnings (2)

1. **Error re-selection compares the untrimmed posted value; validator and writer trim** — `server/src/application/form_sections/references.gleam:237` _(blind + edge + acceptance)_
   `validate_choice` trims (`reference_attestation.gleam:50`), `get_form_value` trims (`application_handler.gleam:2253`), but the error re-render passes raw `common.get_val(...)` as `selected`. A crafted `" attested "` validates and persists, yet re-renders with neither radio checked if another field errors — contradicting the module's own "validator and writer must agree" invariant. Crafted-POST only; the browser `required` attribute makes it self-correcting on resubmit. **Fix:** pass `common.get_val(values, reference_attestation.field_name) |> string.trim` as `selected`.

2. **Yes-path §5.4 confirmation line: the `finalise_application` flag wiring has no test** — `server/src/application/application_handler.gleam:2150` _(tests)_
   `view_confirmation_page` is unit-tested both flag ways, but the derivation hop is not: the attested/declined integration tests assert status and DB rows, never the response body. Flipping `== attested_value` to `== declined_value` passes the entire suite. **Fix:** assert `simulate.read_body(resp)` contains `ref-attestation-confirmation` in the attested test and its absence in the declined one.

### Notes (9)

- **a11y — error span combines `role="alert"` with `aria-live="polite"`** — `reference_attestation.gleam:141` _(blind)_. The house rule is documented in `form_pages.gleam:377-379` ("setting aria-live="polite" alongside creates inconsistent announcements… keep role="alert" alone"). Drop the explicit `aria-live`.
- **copy — "Your landlord will ring them" helper survives in the landlord group** — `references.gleam:28` _(blind)_. Same contradiction the §5.2 intro replacement removed; knowingly deferred per spec Ask-First and flagged as open question #2 in the PR body. Resolve in a follow-up.
- **docs — spec task for the sprint-status flip unchecked while the diff performs the flip** — spec md:80 _(blind)_. Task text says the tick happens at badge-out; self-resolving bookkeeping drift.
- **docs — `review_loop_iteration: 0` contradicts the review-round-1 change log entry** — spec md:7 _(blind)_.
- **docs — spec Code Map omits `form_view_test.gleam`, which the diff modifies** — spec md:65 _(blind)_.
- **dry — attested-derivation `get_form_value(...) == attested_value` duplicated verbatim at two handler sites** — `application_handler.gleam:1539` _(architecture)_. A `pub fn is_attested(values)` on `reference_attestation` keeps one owner and is the natural companion to `validate_choice` for the stepper rebase.
- **tests — error-state `aria-describedby` join (help + error id) unpinned** — `reference_attestation.gleam:110` _(tests)_. Dropping the join passes all tests.
- **tests — vacuous `string.contains("required")` assertion** — `reference_attestation_test.gleam:95` _(tests)_. Satisfied by `aria-required="true"` even if the radio `required` attribute is removed; assert the bare-attribute form instead.
- **Advisory test gate: PASS** _(tests)_. P0 100% (choice-required, tamper rejection, attested/declined persistence, unsubmittable-trap — unit + integration + updated E2E fixtures); P1 ~93% with the confirmation-wiring hop above the only partial; overall ~97%.

### Reviewer agreement

The trim/re-selection inconsistency (Warning 1) was found independently by three lenses (blind, edge, acceptance) — highest-confidence finding in this round, one-line fix.

**Verdict:** READY TO MERGE

Zero blockers. The contract holds: §5.2/§5.3/§5.4 copy verbatim and pinned by render tests, required radio pair with no default, radiogroup aria wiring, error-summary anchor loop, RC1.1 write path exercised by integration tests, all five bug-hunt scenarios updated for the now-mandatory field, CI green at the reviewed sha. The two warnings (one-line trim consistency fix; two response-body assertions) are worth taking but neither gates the merge — the unsubmittable-develop trap does.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
