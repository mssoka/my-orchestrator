## 🤖 Perkins automated review — round 1

**Job:** righttenantry-demo-bulk-invite-guard · **Reviewed sha:** `599a6569` · **Reviewers:** 7/7 completed
**Verification:** 5/5 findings confirmed against the code — 0 discarded as false-positive (1 kept with its headline claim corrected: the send button is disabled when the textarea is empty, so the "silent swallow" user-facing concern was false; only the untested-arm kernel survives)

Round notes: kimi k3 hit its billing-cycle quota cap mid-wave (6 lenses died on 403; blind had finished) — the 6 re-ran once on probe-verified `zai-coding-cn/glm-5.3` per the model chain. Mechanical gates reproduced in the round worktree: `make test-client` **653 passed, no failures**; `lint_demo_network.py` **clean (exit 0)**. PR head unchanged at `599a6569`. Spec rule 3 verified as flagged-not-fixed in the PR body ("Flagged, not fixed" section) — per briefing, not held against the round.

### Blockers (0)

None.

### Warnings (0)

None.

### Notes (5)

1. **Real-mode in-flight `ApiReturnedBulkInvite` can render a send-shaped toast after entering demo** [edge] — `client/src/demo/demo_update.gleam:654` (`_ -> fallback(model, msg)`) → `client/src/client.gleam:2252`. A real-mode send whose response lands after `/demo` entry falls through the demo dispatcher to the real handler; `enter_demo` resets `loading_action` but can't cancel in-flight HTTP effects. Pre-existing systemic fall-through (same window for every real-mode response message, incl. the other two `NEVER_PRODUCED` entries); sub-second navigation race; the send itself happened in real mode, so the ruling's no-demo-send holds. The new lint comment's absolute claim ("the demo never renders a send-shaped result") is broader than what the lint proves (no demo-**originated** producer). Optional: intercept `ApiReturnedBulkInvite` in `demo_update.handle`, or scope the comment.

2. **`NEVER_PRODUCED` lint branch has no bite-test** [tests] — `scripts/lint_demo_network_bite_test.py:219-231`: bites 1–7 cover `DEMO_INTERCEPTED`/`FN_INTERCEPTED` drift, none injects drift into the `NEVER_PRODUCED` trigger check (`lint_demo_network.py:295-298`) this diff relies on. Optional bite-8 mirroring bite-7.

3. **Toast copy deviates from the sibling demo-toast pattern** [blind] — `client/src/copy.gleam` (+`demo_bulk_invite_toast`). Siblings read "X aren't part of the demo. <next action>"; the new copy uses a "Demo mode -" prefix, uncontracted "are not", no next action. Counterweight: it faithfully renders the user's verbatim ruling ("it should just say this is demo, not sent"), the hyphen-over-em-dash choice is correct per the #607/#612 toast em-dash ban, and the decision is documented in the PR. Voice polish only.

4. **Empty-emails demo arm untested** [blind, corrected] — `client/src/demo/demo_update.gleam:431-435`. The reviewer's user-facing claim was false (the send button is disabled when the textarea is empty — `has_emails && !is_loading` gate in `vacancy_handoff.gleam`). Surviving kernel: the `"" -> #(model, effect.none())` arm has no test; it's stray-dispatch defense mirroring the real handler's identical empty no-op. Optional one-line test.

5. **Advisory test gate: PASS** [tests] — P0 100% (demo no-send pinned by a unit test through the real `client.update` dispatch path + compile-time removal of the demo send fns + CI structural lint), P1 100% (notice copy, level, state untouched). Only gap is the P3 note 2 above.

### Reviewer agreement

No multi-source findings this round (all five notes are single-lens).

**Verdict:** READY TO MERGE

The demo bulk-invite guard satisfies every hard rule: the interception lives at the canonical send path (`demo_update.handle` — the same `model.demo_mode` dispatch that guards payments/settings), the demo send path is removed at the source (no second detector, and reintroducing a fake-send is a compile error), real mode is untouched, and the notice is pinned by a test through the real dispatcher. All findings are notes; none blocks.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
