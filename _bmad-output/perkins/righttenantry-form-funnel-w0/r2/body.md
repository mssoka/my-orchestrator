## 🤖 Perkins automated review — round 2 of 3

**Job:** righttenantry-form-funnel-w0 · **Reviewed sha:** `7bb5824` · **Reviewers:** 7/7 completed
**Verification:** 15/20 findings confirmed against the code — 5 discarded as false-positive

**Round-1 fix audit:** all r1 findings verifiably resolved at this sha — the view is now `security_invoker = on` with guarded REVOKEs (r1 blocker), the stage-2 2-day gate lives only in the view (mark/count/list all read `stage2_due`), the copy-sheet "10 minutes" version is retired, all four applicant subjects lead with the property name, and the pinned tests exist and assert real behaviour. Security and edge lenses returned zero findings this round.

### Blockers (0)

None.

### Warnings (4)

1. **Transaction comment overclaims rollback** [blind, codebase] — `server/src/inbound_email/inbound_handler.gleam:543,751`
   Comment says "failure anywhere rolls both marks back", but `clear_rejected_stamps` swallows clear errors (logs, returns `Nil`) and the transaction commits. Narrow (legacy malformed row + clear error), but the guarantee as written doesn't hold. Thread the clear through `result.try`, or soften the comment.
2. **Spam-path handler wiring unpinned** [tests] — `server/src/application/application_handler.gleam:171`
   Predicates and the `genuine=False` view render are tested, but no test drives a honeypot/timing post through the handler — flipping the `False` literal at a call site would fire `application_confirmation_viewed` on bot renders with no test failing. Spec: spam fake-confirmation must NOT fire the confirmation event.
3. **Reminder-button disabled predicate untested** [tests] — `client/src/components/awaiting_section.gleam:220`
   `remindable == 0 && followup == 0 || pending` — a revert to the old predicate greys out the button when only follow-ups are due (stage 2 unsendable) and no test fails. Only label strings are pinned.
4. **Advisory test gate: CONCERNS** [tests] — P0 100%, P1 ~82–85%, overall ~85%. The gaps above plus the notes below are what stand between this and PASS.

### Notes (9)

- **Stage-1 membership rule still triplicated** [architecture] — `mark_reminders_for_vacancy.sql:9`, `list_awaiting_for_vacancy.sql:21` re-derive the awaiting predicate the view now claims to own ("single home"). Stage-2 gate is centralised correctly; stage-1 membership isn't.
- **`month_name` copied a third time, third return shape** [architecture, codebase] — `email_client.gleam:305` (vs `audit_report.gleam:331` Option, `evidence_humanize.gleam:408` Result). Comment acknowledges it; no deferred-work entry tracks it.
- **Mixed-pool label/toast drop singular handling** [blind] — pool (1,1) renders "Send 1 reminders + 1 follow-ups" / "…to 1 people…" while single-stage branches special-case one. `awaiting_section.gleam` `reminder_button_label`; `copy.gleam:487`.
- **`make test` help text stale** [blind] — `Makefile:30` still says "(shared, client, server — no Docker needed)" though the target now runs `test-js`.
- **`sender_name` dead in RETURNING** [blind] — `mark_followup_reminders_for_vacancy.sql:23`; the row decoder carries it, nothing consumes it.
- **Self-heal clear log not stage-labelled** [blind] — `inbound_handler.gleam:774`; stage-1 and stage-2 clears log identically (unlike `handle_send_outcome`).
- **Tag slug pairing at send call sites unpinned** [tests] — `email_client.gleam:396,446,556,582`; payload shape is pinned, the four call-site slugs aren't.
- **`initBrowser` DOM glue untested** [tests] — `apply_analytics.js:295`; ticketed in `deferred-work.md:539` (happy-dom/jsdom). Gap stands until it lands.
- **Dublin-local `closes_at` conversion untested** [tests] — `find_vacancy_for_invite.sql:11`; feeds the stage-2 email's announced close date.

### Reviewer agreement

- Transaction-comment rollback overclaim — **blind + codebase**
- `month_name` third copy — **architecture + codebase**

**Verdict:** READY TO MERGE

Zero blockers; the r1 blocker (RLS-bypassing view) is verifiably fixed and every r1 warning was addressed. The warnings above are test-pinning and comment-accuracy items — worth a follow-up commit, not worth holding the wave.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
