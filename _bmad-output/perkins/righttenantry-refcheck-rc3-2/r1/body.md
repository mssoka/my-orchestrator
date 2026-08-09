## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc3-2 · **Reviewed sha:** `f5e827d` · **Reviewers:** 7/7 completed
**Verification:** 15/15 findings confirmed against the code — 0 discarded as false-positive

### Blockers (0)

### Warnings (4)

1. **Spec asserts `middleware.redact_token_route` covers `/reference/*` — no such arm exists** (`server/src/middleware.gleam:330`, spec line 158). [security + codebase]
   The spec's capability-token hygiene constraint claims the redaction registry covers `/reference/*` server-side. It doesn't: the registry has arms for `dsar`, `erase`, `apply/.../resume`, `apply/.../draft-erasure` only. No leak today (the routes land in rc3-3/rc3-4), but those stories will trust this claim and may skip adding the arm, leaking referee capability tokens into Sentry event paths and access logs. Fix: correct the spec sentence and add `["reference", ..] -> Ok("/reference/<redacted>")` in the story that wires the router entries.

2. **Warm-handoff email deviates from the pinned copy beyond the three documented deviations** (`server/src/reference_checks/messages.gleam:414`, `:431-433`). [acceptance + blind]
   The spec pins: "Their contact details and the same log are on the application page." + CTA, and attempt lines as `• {at}: {channel}, {outcome} {detail}`. The implementation adds an extra sentence ("If they complete the form anyway, it still shows up there.") and renders detail parenthesised (`(detail)`). Neither is in the three documented deviations nor in the dev record's delta list — the story's own contract is verbatim-minus-documented-deviations, enforced by pruning an extra co-nudge line for exactly this reason. Tests pin the implementation, not the spec. Fix: revert to the pinned strings, or add both to the spec's deviations register and pin them with tests.

3. **AC3 email sender identity + template tags unobservable to the suite; `send_reminder` never exercised with `ReminderTwo`** (`server/src/reference_checks/send.gleam:30,34,194-203`). [tests]
   Every send test uses `no_key_deps()`, so the non-empty-key branch (which references `referee_sender`, `standard_sender`, and the `reference_*` tags) is never reached. A typo in either sender, a swapped referee/applicant sender, or a wrong tag would pass the suite green — and the spec's Verify clause demanded payload-wiring assertions. Fix: expose a pure sender/tag selection (or build via the public `email_client.build_send_body` seam) and pin the senders, the four tags, and ReminderTwo through `send_reminder`.

4. **Advisory test gate: CONCERNS** [tests]
   P0 100% (Art 14 block, stop-link in every SMS, no reply-STOP, no-op-without-keys, outcome mapping, em-dash ban all pinned). P1 ~88%, overall ~93% — the AC3 email seam (warning 3) is the single P1 gap.

### Notes (9)

1. Warm-handoff count line says "tried to reach them" where the spec pinned "messaged them" — disclosed in the dev record, spec's pinned copy not amended (`messages.gleam:406`).
2. Greeting-split capitalisation in reminder-1 and co-nudge deviates from pinned copy but is documented only for reminder-2 (`build_reminder_email_html` / `build_co_nudge_email_html`).
3. Unresolved `??` placeholder shipped in the `send.gleam` doc comment and spec T4.2 ("corrected ?? snapshot") — the module doc rc3-5's implementer reads.
4. `first_name`'s `[]` branch is unreachable (`string.split` always yields ≥1 element); if it ever fired it would return the untrimmed name (`messages.gleam:first_name`).
5. `first_name` is exported with no production caller — public API committed ahead of rc3-5, the intended consumer.
6. Empty attempt log renders "We've tried to reach them 0 times over the last 4 days" — spec-pinned shape, awkward at 0; copy-deck question, not an implementation bug.
7. `item_style` hardcodes the brand font stack instead of composing the `brand_font` const (`messages.gleam:445-447`).
8. Email markup primitives + brand tokens now duplicated in two modules — deliberate per spec decision 7 (extraction deferred until a third email family), flagged for the rebrand.
9. Warm-handoff attempt-line empty-detail branch unpinned — both fixtures carry non-empty detail (`messages.gleam:431-433`).

### Reviewer agreement
Two findings were reported independently by two lenses (highest-confidence signals): the missing `/reference` redaction arm (security + codebase) and the warm-handoff copy-contract drift (acceptance + blind). Both verified confirmed.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
