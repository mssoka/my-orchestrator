## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc1-1 · **Reviewed sha:** e8682fd · **Reviewers:** 7/7 completed
**Verification:** 16/16 findings confirmed against the code — 0 discarded as false-positive (2 demoted on adjudication, noted below)

### Blockers (0)

None. All Story RC1.1 acceptance criteria are implemented as specced: the enum migration follows the `20260420000003` precedent exactly; the three capture columns carry the specified bounds/CHECK; the submission transaction writes bounded IP/UA, sets `reference_contact_choice` on every success, and gains the fourth `insert_acknowledgement_records` write with the current `policy_version` only when attested; declined writes no row and submits normally; missing/tampered choice fails validation with zero rows persisted; the AD-2 §3.2 vocabulary constraint is clean (new code uses attestation/acknowledgement wording throughout — "consent" appears only in pre-existing unrelated GDPR code and the `consent_type` type name itself). Test coverage: attested/declined/missing/tampered paths at unit + integration level, overlong-header truncation, codec round-trips incl. absent-key default, DSAR key assertions. Advisory test gate: **PASS** (P0 100%, P1 ~95%, overall >90%).

### Warnings (2)

1. **Deploy-sequencing: mandatory choice validation ships before the RC1.2 UI that emits it** [blind, edge, codebase] — `server/src/application/application_handler.gleam:510`. `validate_form` now hard-requires `reference_contact_choice`, but no form posts it yet (verified: no emission in `form_sections/`, `form_fields.gleam`, `form_pages.gleam`, or `client/src` — RC1.2, currently backlog). This is exactly the story's AC (explicit choice required, no silent skip) and the PR body already carries the correct gate: deploys are manual — **do not promote `develop` toward staging/production between this PR and RC1.2's**, or every live submission fails validation with an error no applicant can answer. Not a code defect; a release-order constraint to honor. (edge filed this as a blocker; demoted to warning because the behavior is spec-mandated and the gate is documented in the PR body.)

2. **`client_ip` first-XFF-hop trust note codifies a spoofable assumption** [security] — `server/src/request_helpers.gleam:17-33` + the trust note in `supabase/migrations/20260731220100_add_application_capture_columns.sql`. "Cloudflare appends the originating IP first" holds only when the client sends no XFF; Cloudflare preserves client-supplied leading XFF entries and appends the true connecting IP **last** (the reliable source is `CF-Connecting-IP`). The first XFF hop — what `client_ip` captures — is therefore client-controlled even behind Cloudflare, so this capture is forgeable evidence feeding RC3.7's fraud comparators. AD-10 already labels the signal honestly weak and display-only, so this is not a launch gate — but the comments should stop asserting trustworthiness (or the helper should read `CF-Connecting-IP`, a shared-helper change best paired with the deferred slicing fix).

### Notes (8)

1. **Grapheme slice vs codepoint CHECK bounds** [blind, edge, security, tests] — `server/src/request_helpers.gleam:30,41`. Gleam `string.slice` counts grapheme clusters; Postgres `length()` counts codepoints — a multi-codepoint header can exceed the 64/512 CHECK post-slice and 500 the submission transaction. Already logged in this diff's `deferred-work.md` with the fix (codepoint-bounded slicing across all three callers) correctly scoped outside this PR; the new truncation test exercises ASCII only, so the deferred fix should add a multi-codepoint header case. (blind filed as warning; demoted to note given the documented deferral.)
2. **DSAR export is beyond the story's Files/areas — justified, and on record** [blind, acceptance] — `server/src/dsar/sql/find_application_by_id.sql:54`. Art. 15 requires the subject's own new personal-data columns in the export; AD-11 restricts only the landlord payload, and the PR body states the rationale ("found in review"). The spec doc's Code Map/Tasks were not updated to include `dsar/*`, so the frozen spec's "Ask First" gate was honored in substance but not on paper.
3. **Tracking drift** [blind] — spec frontmatter says `status: 'done'` with its Tests task unchecked, while the sprint tracker says `review`. The tests plainly exist in the diff; the artifacts, not the code, are stale.
4. **Design Notes vs implementation** [blind] — the spec promises an `apply_form_fixture_values` `choice` parameter; the implementation hard-codes the pair and per-test maps over it (`server/test/integration/gdpr_integration_test.gleam:2170`). Behavior matches; the documented mechanism does not.
5. **Redundant override** [codebase] — `client/test/client_test.gleam:2239` re-states `reference_contact_choice: None` in a functional update that already inherits it from `..test_application()`. Harmless.
6. **Insert-layer guard untestable** [tests] — the loud-abort `HandlerLogicError("invalid_reference_contact_choice")` sits in private `insert_application_row` (`application_handler.gleam:1668`), unreachable from the test surface; verified by inspection only. Acceptable as defense-in-depth.
7. **Unpinned label** [tests] — `"reference_contact_choice" -> "Contacting your referees"` (`error_summary.gleam:172`) appears in neither `error_summary_test.gleam`'s label pins nor its drift-guard key list; deleting it would silently degrade the banner.
8. **Advisory test gate: PASS** [tests] — P0 100% (attested/declined/missing-choice each at unit + integration; IP/UA bounds pinned at 64/512), P1 ~95%, overall >90%; only the P3 residuals above.

### Reviewer agreement

- Deploy-sequencing warning — flagged independently by **blind + edge + codebase**.
- Grapheme/codepoint note — flagged independently by **blind + edge + security + tests**.

**Verdict:** READY TO MERGE — 0 blockers; the story contract is fully implemented and well tested. Honor the deploy gate in the PR body (ship RC1.2 before any promotion past `develop`) and correct the XFF trust note at the next opportunity.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
