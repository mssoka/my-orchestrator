## 🤖 Perkins automated review — round 2 of 3
**Job:** righttenantry-refcheck-rc4-4 · **Reviewed sha:** 8e48605 · **Reviewers:** 7/7 completed
**Verification:** 15/21 findings confirmed against the code — 6 discarded as false-positive

### Fix audit (r1 → r2)

**Blockers — both fixed, verified:**

- **B1 cadence restart latch** — the fold now carries `#(cycle_index, restarted, entries)`; only the first batch strictly after `corrected_at` resets to 0, later batches continue the fresh cycle (co_nudge, reminder 1, reminder 2). The restart test now feeds 3 post-correction batches and pins co_nudge + both reminder ordinals — neutralizing the latch turns it red. Unit suites green (server 1508).
- **B2 test gate** — OQ-5 toast pinned at the const (verbatim) and at the firing arm end to end (`AppCompletedRefcheckExport(Ok)` asserts the exact toast); `terminalized_at` integration assertions added for terminalize refused + objected, exhaust, and sweep_mark_failed — all five terminal writers now pinned.

**W1–W8 — all fixed, verified in the worktree** (kind-aware group-then-map with a boundary test; `updated_at` fallback skipped when taken over; explicit failed/completed labels in both tables; queued taken-over export restored; nine consts + fn-built labels in the em-dash scan with the spec-verbatim arm excluded; co_nudge detail passthrough + conditional join; toast + stamp pins as above). **Notes:** N11 (sprint YAML) and N13 (unused import) fixed; N3 and N7 partially fixed (see Notes); N1, N2, N4–N6, N8–N10, N12 carried as note-severity.

### Blockers (0)

### Warnings (3)

1. **[acceptance] Corrected (re-queued) rows hide the attempt-log timeline and export — the correction event is suppressed while queued** — `reference_panel.gleam:702-710` + `correct_reference_call.sql`. AC1 requires the timeline to cover the correction event for a started row; correction re-queues to `queued`, and the Queued arm renders no log unless the row was taken over. The moment the landlord corrects, the correction event and prior sends vanish from the panel until T0 re-claims (or the row terminals — indefinitely if the corrected contact keeps failing). Also the queued body claims "not started" for a row that started. Gate the suppression on log content rather than status.

2. **[edge] Taken-over ContactInitiated rows still show "Next reminder in ~2 days if there's no reply"** — `reference_panel.gleam:1280-1283` + `take_over_reference_call.sql`. Takeover NULLs `next_attempt_at` and the sweep excludes taken-over rows — no reminder will ever fire — yet the hint promises one on every warm handoff. Suppress the hint when `taken_over(call)`.

3. **[codebase] Failed/skipped send channels render as "sent", and the reminder ordinal overwrites the failure detail** — `reference_panel.gleam:1461-1480` + `application_detail_handler.gleam:1384-1387`. W6 fixed the co-nudge case only; invitation/reminder labels are unconditional ("Reminder N sent — email + SMS") even when a channel's outcome is failed or skipped ("no email contact on file"), and the ordinal replaces the attempt's failure detail for reminders. An exported evidence record claims "sent" for sends that never went out. Make the label outcome-aware and keep failure detail on the line.

### Notes (7)

1. **[architecture, codebase, tests] Residual of r1 B2: the export Error arm (`refcheck_toast_export_failed`) still has no firing pin** — Ok arm + const are pinned; add one Error-arm test.
2. **[blind, architecture] `group_timeline_entries` merges on at + send-kind but never compares entry kind to batch kind**, though the comment claims "same kind + same at" — unreachable from server data today; fix the comment or the condition.
3. **[blind, tests] Residual of r1 N3: the label-consistency test asserts weak proxies** — failed/completed are pinned exactly; the other six statuses assert only non-empty / not-"In progress". Extend the table to exact strings.
4. **[blind] The " — " composition joins in timeline/export strings sit outside the W5 scan** — add the join-built lines to the scan or document the joins as structural separators.
5. **[blind] Migration comment documents an unconditional `updated_at` fallback** the W2 code deliberately skips when taken over — amend the comment before merge.
6. **[architecture] AttemptLogEntry kind vocabulary is a raw-string wire contract duplicated across server and client** — consider shared consts in `shared/reference_call.gleam`.
7. **[tests] Advisory test gate: PASS** — P0 100%, P1 ≥90% (multi-batch restart, OQ-5, 5/5 stamps, W1–W8 pins all green).

### Reviewer agreement

- Export Error-arm firing pin missing — 3 sources (architecture, codebase, tests)
- `group_timeline_entries` kind-equality comment/code mismatch — 2 sources (blind, architecture)
- Label-table weak proxies (partial r1 N3) — 2 sources (blind, tests)

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
