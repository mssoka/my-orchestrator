## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-refcheck-rc4-4 · **Reviewed sha:** 1a3839c · **Reviewers:** 7/7 completed
**Verification:** 42/44 findings confirmed against the code — 2 discarded as false-positive (chunk-boundary artifact + a covered-decode claim; details in the consolidated artifact)

### Blockers (2)

**1. Post-correction cadence restart re-fires for EVERY post-correction batch — co_nudge and reminders all mislabel as `invitation_sent`** · [blind, edge, security, codebase, tests]
`server/src/application/application_detail_handler.gleam:1356-1387` (`build_send_entries`)

The fold accumulator carries `#(cycle_index + 1, …)`. After the first post-correction batch restarts (`cycle_index = 0`), the accumulator becomes `(1, …)` — and every later batch still satisfies `Gt if batch_index > 0`, so the restart re-fires indefinitely. `correct_reference_call.sql:32` resets `attempt_count = 0`, so every corrected row runs a full re-cadence (invite + co-nudge + 2 reminders): the post-correction co-nudge and both reminders render as "Invitation sent" with empty detail — ordinals never emitted. The only restart test feeds ONE post-correction batch, so CI is green while AC1 fails for every corrected row.

**Fix:** carry a `restarted` flag (or the post-restart position) in the accumulator so only the FIRST batch strictly after `corrected_at` resets to 0; extend `attempt_log_restarts_cadence_after_correction_test` with ≥2 post-correction batches pinning `co_nudge` and reminder ordinals.

**2. Advisory test gate: FAIL** · [tests]

P0 100% (timeline render + order, export content, dropdown totality, 5-type codec round-trips, back-compat decode, builder happy paths, payload wiring, no-duplicate pin, preference matrix, §7.9 pins). P1 <80%: the restart defect above shipped through a one-batch restart test; the OQ-5 export toast (AC2 headline) has no pin at its firing arms or verbatim copy; 3 of 5 terminal writers' `terminalized_at` stamps have no integration assertion.

### Warnings (8)

- **Kind-blind same-`at` collapse drops lifecycle/terminal lines** — reachable: a legacy unreachable row taken over post-migration gets `terminal at = updated_at = taken_over_at` (one `now()`), so its terminal line vanishes from timeline AND export. Restrict the collapse to send kinds + add a boundary test. [blind, tests, security, edge, acceptance, architecture] · `reference_panel.gleam:1421-1435`
- **Legacy terminal fallback uses `updated_at`** — the exact column the migration comment documents as polluted by takeovers; the terminal event gets stamped at the takeover instant. Skip `updated_at` when `taken_over_at` is set. [architecture] · `application_detail_handler.gleam:1457-1463`
- **`failed` (and v2 `completed`) rows get contradictory labels** — timeline "Closed" vs export outcome "In progress" for a v1-reachable terminal (sweep_mark_failed renders + exports). Add explicit arms + table tests. [blind, codebase, edge, acceptance, architecture] · `copy.gleam:971-998`
- **Queued taken-over rows lose the export affordance** — takeover is offered on queued rows and the taken-over surface (chips + label) renders, but the export button now lives only in the attempt-log block, which Queued suppresses — §7.7's export-beside-the-chips contract breaks (RC4.3 regression). [architecture] · `reference_panel.gleam:699-705`
- **Em-dash enforcement gap** — "Closed — no reply" is new fn-built copy carrying an em-dash without the by-construction exclusion the OQ-5 toast got, and the nine new dash-free consts were added to no scan list, so the ban silently stops covering the new surface. [blind, tests, codebase, architecture] · `copy.gleam:979`, `copy_test.gleam:320-352`
- **Skipped co-nudge renders a dangling " — " and loses its skip reason** — the builder ships `detail` only for reminders, but `nudge_label` unconditionally joins " — " + detail. Carry the attempt's detail for co_nudge entries and/or guard the join. [edge] · `reference_panel.gleam:1455`
- **OQ-5 verbatim toast unpinned** — the toast fires with the exact copy (verified), but nothing pins the firing arms or the verbatim string, and the const left the em-dash scan. [tests] · `client.gleam:3514-3538`
- **3 of 5 terminal writers' `terminalized_at` stamp unpinned** — terminalize (refused/objected), exhaust, and sweep_mark_failed assert status only; a dropped stamp ships silently. [blind, tests]

### Notes (13)

Legacy-payload rollout window shows an empty timeline (documented back-compat default, transient) · cadence hint counts batches across correction cycles · per-status label tables exercised for only 2/9 statuses · `export_signals` parse-error/empty branches untested · reminder ordinal fallback untested · unknown-kind fallback untested · terminal fallback legs `submitted_at`/`updated_at` untested · client test fixture mirrors the server builder (divergence risk) · dropdown test comment overclaims decode coverage · group-by-at fold triplicated · builder lands inline in a 2151-line handler · unused `gleam/result` import in the actions integration test · sprint-status YAML still lists rc4-3 as backlog.

### Reviewer agreement

The two blockers rest on 5-lens and 6-lens agreement plus the lead's own fold trace; the failed-row labels (5), em-dash gap (4), and stamp coverage gap (2) are independently confirmed. Everything else verified clean: AR-RC13 server-built timeline holds (no client re-derivation of event state), codec completeness 5/5, expand-only migration, §7.9 bodies verbatim, preference matrix, no-duplicate-terminals pin, back-compat decode.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
