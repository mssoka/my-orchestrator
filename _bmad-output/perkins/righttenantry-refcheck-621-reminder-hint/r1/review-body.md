## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-refcheck-621-reminder-hint · **Reviewed sha:** 3c29e3b · **Reviewers:** 7/7 completed
**Verification:** 7/9 findings confirmed against the code — 2 discarded as false-positive; one blind/tests duplicate pair merged, with corrected framing after verification.

### Blockers (0)

None. The one hard blocker for this fix — **hint/badge agreement** — HOLDS: the hint gate (`view_attempt_log`, `reference_panel.gleam:1284`) and the "You're handling this one" badge (`:298`/`:351`) both read the same `taken_over()` predicate, so they can never disagree.

### Warnings (0)

None.

### Notes (6)

- **N1 — Test docstring over-promises timeline visibility** `[blind, tests]` — `reference_panel_test.gleam:1571-1623`. The new test's docstring says "the invite + takeover events stay visible", but no timeline entry is asserted on the taken-over row. *(Verification correction: both reviewers' hazard framing — "gutting the whole attempt log would pass" — is false: the export button `refcheck-export-landlord_ref` renders inside `view_attempt_log` and is pinned by the existing `taken_over_row_shows_label_chips_and_export_test`, so block removal fails the suite. The residual nit is docstring-vs-assertions only.)* Fix: assert a timeline entry (e.g. `"Invitation sent"` present) or trim the docstring.
- **N2 — Hint-absence assertion hardcodes the escaped literal** `[blind]` — `reference_panel_test.gleam:1617-1619`. The test asserts on `"Next reminder in ~2 days if there&#39;s no reply"` while `copy.refcheck_what_happens_next` (`copy.gleam:663`) holds the source string. Copy drift would let the absence assertion pass vacuously. Matches the file-wide literal pattern (the positive test at `:460` does the same), so consistency-neutral but drift-fragile. Fix: derive the escaped expectation from the copy constant in both tests.
- **N3 — Post-takeover staleness window is pre-existing architecture** `[edge]` — `client.gleam:3590`, `:6649-6657`. The take-over success handler converges the model only via a one-shot refetch (no local `taken_over_at` update, no retry), so the hint persists until the refetch lands — and indefinitely if it fails. Verified accurate, but: (a) badge and hint still *agree* in the window (same predicate, same model field), so this fix's invariant holds; (b) the mechanism predates this diff and is shared by every row action; (c) changing it would breach the briefing's panel-only scope guard. Worth a follow-up issue, not this PR.
- **N4 — Taken-over fixture duplicated verbatim in two adjacent tests** `[architecture]` — `reference_panel_test.gleam:1521-1543` vs `:1584-1603`. Identical `ReferenceCallDetail` construction (verified by direct read — they differ only in one comment line, and the comments have already started to drift). AGENTS.md's DRY rule (extract at 2+ repeats) applies. Fix: extract a `taken_over_contact_row()` helper.
- **N5 — Bug-hunt scenario yaml absent at this sha** `[tests]` — `.pi/skills/bug-hunt/scenarios/reference_checks/` does not exist on develop; the yaml lives on branch `rt-refcheck-bughunt2` (commit `9f40472`). The issue/briefing treat runtime re-creation of the suite as precedent and confine this PR to application code, so this is a process observation: the PR body's scenario evidence isn't re-runnable from this sha. Fix: land the `reference_checks` scenario suite on develop so `/bug-hunt reference_checks` is reproducible.
- **N6 — Advisory test gate: PASS** `[tests]` — both arms of the changed `case` are pinned at unit level: the new test (taken-over → hint absent; red on pre-fix code) and the existing `invitation_sent_state_test` (non-taken-over `ContactInitiated` → hint present; `row()` sets `taken_over_at: None`). No API/DB/auth surfaces touched. P0 100%, P1 ≥90%, overall ≥80%.

### Reviewer agreement

One finding reached by two independent lenses (blind + tests): the new test's docstring over-promises timeline-event visibility (N1, with the corrected framing above).

**Scope check (per lens guards):** clean — exactly 2 files changed (`reference_panel.gleam`, `reference_panel_test.gleam`); no sweep/cadence/DB/toast changes. The sweep exclusion the fix rests on is verified present at the reviewed sha (`sweep_due_reference_calls.sql:59` — `AND rc.taken_over_at IS NULL`; pre-existing contract, not part of this change). The bug-hunt scenario yaml on `rt-refcheck-bughunt2` matches the regression test's semantics (pre-takeover hint present, post-takeover label present + hint absent).

**Discarded as false-positive:** (1) "positive hint path unasserted" — pinned by the existing `invitation_sent_state_test`; (2) "fix rests on unverified sweep SQL" — the `taken_over_at IS NULL` exclusion is in the repo at this sha.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
