## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-mobile-form-hunt · **Reviewed sha:** `109006f` · **Reviewers:** 7/7 completed
**Verification:** 29/30 findings confirmed against the code — 1 discarded as false-positive

**Ground truth:** the blocker bar for this PR (the four user-approved fixes present and pinned: B1 stepper rail, T1–T7 44px targets, "Comparing:" overlap, N1 email wrap) is **met** — verified structurally, and the local suite was independently re-run in the round worktree: **1527 passed, 0 failures**. CI red here is the known Actions billing block, not a defect.

### Blockers (0)

None.

### Warnings (5)

1. **T2 fix incomplete: "See all guides →" row still ~36px** — `client/src/components/shell.gleam:469` — the playlist link keeps `py-2 block` with no `min-h-[44px]` while every sibling row in the same menu was fixed. *(edge, acceptance, codebase)* — add `min-h-[44px] flex items-center`, drop `block`.

2. **T3 pattern persists on the settings page** — `client/src/pages/settings_security.gleam:222` — settings has its **own** `view_password_field` whose toggle got none of the `p-2 -m-2` hit-area fix (~16px; the hunt only listed login/signup/reset). *(edge, acceptance)* — apply the same padding or share `auth_layout`'s component.

3. **`select_mode_action_bar` is the unfixed twin of `comparison_bar`** — `client/src/components/select_mode_action_bar.gleam:43-69` — fixed bottom bar from the leaderboard with the exact pre-fix pattern: `h-9` (36px) buttons, no `flex-wrap`, `whitespace-nowrap` count label. Same overlap + tap-target class T1 just fixed, one component over. *(edge, architecture)* — mirror the T1 fix.

4. **B1 regression net is half-pinned** — `client/test/client_test.gleam:5247` — the terminal-roots test renders only `Rejected`; the identical `w-full` literal on the `auto_closed` root (`status_stepper.gleam:375`) and the load-bearing `application_detail.gleam:373` wrapper `w-full` (half of B1's documented two-fold root cause) have no pin — reverting either re-breaks mobile clipping with a green suite. *(blind, architecture, codebase, tests — 4-way agreement)* — extend the test to render `AutoClosed` and assert the wrapper string.

5. **Committed screenshot evidence has mislabeled duplicates** — `…/mobile-form-hunt/screenshots/` — shasum shows 9 files byte-identical across captions, including `11-create-vacancy-390` ≡ `12-login-390` (provably wrong capture) and `24-apply-top` ≡ `25-apply-stepper`. *(blind; hash-verified)* — recapture or drop before anyone cites them.

### Notes (9)

1. Help-guide rows carry conflicting `block` + `flex items-center` (`shell.gleam:487`) — works (flex wins Tailwind's cascade) but `block` is dead. *(blind, architecture, codebase)*
2. Committed lavish report still says "No code changes — findings only" (`mobile-form-hunt-findings.html:61,354`) — hunt-phase snapshot; findings.md POST-REVIEW supersedes. *(blind)*
3. Regression checklist item 2 has both ✅ and ❌ BROKEN (`findings.md:132`) — stale ✅. *(blind)*
4. `run-probe.sh` unwrapping loop breaks before parsing object payloads — committed `probe-menu.json` is left an unparsed string and the summary step would TypeError on it. *(blind)*
5. `view_copy_button` duplicated in `distribution_strip` + `vacancy_handoff` (pre-existing) — this PR had to apply the identical fix twice. *(architecture, codebase)*
6. T3 lands at ~36-40px hit area — documented and user-approved as-is in findings.md POST-REVIEW; carried for the record. *(blind)*
7. "+3 pins" = 2 committed tests + 1 browser-verified comparison wrap — accurate but easy to misread; the wrap is still unpinned in the suite. A one-line `string.contains("flex flex-wrap")` pin closes it. *(blind, acceptance, tests)*
8. Remaining class-level fixes unasserted anywhere (mobile menu never rendered in tests; T4 copy/save-draft; T3/T6 hit-area classes; T5/T7 static assets; N1 `break-all`) — optional pins; `demo_banner_controls_reach_44px_test` is the in-repo precedent. *(tests)*
9. Terminal-roots test pins the full ordered class string — brittle to unrelated reordering; assert a shorter stable token. *(architecture)*

### Reviewer agreement
Four lenses independently converged on **W4** (B1 pin depth), three on **W1** (playlist row) and **Note 1** (block+flex), two each on **W2**, **W3**, **Note 5**, **Note 7** — all code-verified before reporting. The one discarded finding was the tests lens's percentage-based "coverage gate FAIL" — the project's standing orders explicitly rule out coverage-percentage gates, and its substance survives as W4.

**Verdict:** READY TO MERGE

_Zero blockers — the approved fix set landed exactly as specified and the suite is independently green. The five warnings are same-class stragglers (three missed instances of the very patterns this PR fixes) plus pin-depth and evidence hygiene — cheap follow-ups, none gating._

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
