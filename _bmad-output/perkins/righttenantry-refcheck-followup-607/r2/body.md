## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-refcheck-followup-607 · **Reviewed sha:** `5dcf5dce91202b1d6f967fc092c4ffaa74b8d65e` (short `5dcf5dc`)
**Verification:** 25/25 findings confirmed against the code — 0 discarded as false-positive

### Fix-audit (r1 → r2)

**B1 fixed** — the lockstep test now iterates the exported production `terminal_statuses` const in both directions; editing the const turns it red (sandbox-reasoned + suite green), and the arch-doc claim matches. **W1 fixed** — the doc claim is corrected to test-only with the false-positive rationale; the SQL-boundary strip stays the live defense. **W2 fixed** — `trigger.is_terminal` consumes shared `status_from_string` + `is_terminal_status`; no second unpinned server-side terminality list survives (grep-verified). **W3 fixed** — the token-based scanner fails all three historical shapes (single-line, multiline, non-final — sandbox-verified exit 1) and passes legal nested refactors. **W4 fixed** — one outcome mapping; `outcome_from_string` derives from the optional fn; the exhaustive `all_outcomes()` round-trip pin is green. **N1, N2, N3, N4, N5, N6 fixed** — nested-case false positive gone (sandbox exit 0), disclaimer whitelist-pinned in scope, escaped-quote and log-region handling verified, normalised grouping with a green merge pin (the `+00`→`Z` wire delta is display-safe — client formatting is position-based), copy.gleam scanned with owner-name exemptions, §8.2 now carries the unknown-outcome rule. **N7 carried** (documented exemption — allowed; still-present note below). **N8 re-measured:** CONCERNS (note below). All five #607 items' production behavior stands as r1-verified correct.

### Blockers (0)

### Warnings (3)

- **Lockstep direction 2 hardcodes the 14-string status universe** — `server/test/application/application_detail_handler_test.gleam:608` (blind, edge, architecture, codebase, tests). B1's fix is real, but direction 2 reintroduces the mirror-drift class one layer out: a 15th terminal status added to shared (v2 voice is the stated plan) yet missed in `terminal_statuses` fails nothing, so the timeline silently omits its terminal entry. The comment's "pinned by the shared every_status_round_trips_test" overstates — that test round-trips `all_statuses()` only. → Export the status-string universe from shared (single home) and iterate it in direction 2, or derive the const from shared truth.
- **W2 fix flips trigger slot-liveness for unknown status strings** — `server/src/reference_checks/trigger.gleam:1157` (blind, edge, architecture, tests). Unknown → `_ -> Failed` → terminal, so in an expand-then-contract window a future v2 status makes `find_live_row_for_slot` report the slot free while `idx_reference_call_live` still occupies it — the trigger then attempts a duplicate insert and the unique index rejects it (the old list-based code returned the live row and 409'd cleanly). Zero live impact today (enum-constrained); no test covers the branch. → Treat unrecognised strings as live in this context (known-set membership before shared truth) and pin the branch against the index exclusion set.
- **Token-based hooks lint still passes ungated constructions via a `!`-negated gate or a module-qualified constructor** — `scripts/lint_refcheck_hooks.py:46-51` (security, edge). Sandbox-verified: `case !call.hooks.can_take_over { True -> [RefcheckTakeOver] }` exits 0 (the `!` is untokenised, so the negated subject matches the gate — construction while the hook is OFF), and `[model.RefcheckTakeOver]` exits 0 (dotted tokens never match `HOOK_FOR`). The historical shapes are caught; these two semantic bypasses are not. → Strip/reject `!` on gate subjects; match on the final dot-segment; add a CI negative-control fixture.

### Notes (7)

- **N7 still present since round 1** (edge, acceptance, security, codebase, tests): substitute message-payload construction stays shape-exempt from the hooks lint — the exemption is now documented in the lint docstring with the panel tests as backstop (a real carry reason), but the construction site remains CI-invisible.
- **Hooks lint blind spots beyond the fixed shapes** (edge, architecture, tests, blind): sandbox-verified — `let a = RefcheckTakeOver` then `[a]` escapes, `fn helper() { RefcheckTakeOver }` escapes, bare paren-arg construction escapes; a legal multi-subject gated case (`case call.hooks.can_take_over, other {`) false-positives (exit 1); the docstring's "construction shape is irrelevant" overstates; the `:` reset token is dead.
- **Em-dash lint scope omits applicant-facing inline strings** in `application_handler.gleam`, `document_download_page`, `document_upload` (edge) — same class as the N2 gap this lint closes; zero live em-dashes today.
- **`outcome_from_string` wrapper is test-only** (codebase): its doc claims "code that must always produce a value" — repo-wide grep finds no production caller. Reword or delete.
- **Spec artifact drift** (blind): the implementation-artifacts spec still says the lint excludes copy.gleam wholesale; the shipped script scans it with owner exemptions. The tighter reading is the right one — update the artifact.
- **Comment inaccuracy** (blind): the inverted-mix test comment narrates 08:04/08:05 while the fixture uses 10:04/10:05.
- **Advisory test gate: CONCERNS** (tests): P0 100% — every #607 item behaviour has a green pin (shared 119, server 1512, client 571; both lints exit 0 and sandbox-fail on the historical shapes). P1 ≈85%: the three warnings above plus the N7 exemption keep P1 below PASS.

### Reviewer agreement

1. **Lockstep direction-2 hardcoded universe — 5/7 lenses.** 2. **Trigger unknown-status flip — 4 lenses.** 3. **N7 exemption still present — 5 lenses.** 4. **Hooks lint evasion shapes — 3 lenses.**

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
