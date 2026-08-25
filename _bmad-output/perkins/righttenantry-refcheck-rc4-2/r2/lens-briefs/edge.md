# LENS: edge (source tag: `edge`) — Perkins r2 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples relevant to this diff:

- **Pre-v1 / NULL `reference_contact_choice`** — card hidden; `attestation_on_file` False with no rows.
- **`off` + rows both present** (declined choice but rows exist) — which renders, rows or Off block?
- **Empty attempts list** — `group_by_at([])`, `list.last([])`, batch indexing, `has_next_reminder` on an empty log.
- **Malformed stored result JSON** — `json.parse` failure in `view_completed` → what renders?
- **Result JSON with missing `ai_summary` / `verification` / `fraud_signals` keys** — decoder defaults.
- **Unparseable attempt entries** — attempts JSON parse failure.
- **Unknown slot string** in `slot_field_keys` → `[]` → answered 0 of 0? Division by zero in any count?
- **`render_period` / `render_amount` / `render_as_stated_*`** with partial objects (missing `to`, missing `from`, empty strings, `ongoing` variants).
- **`euros()`** with non-numeric amount string, negative, zero.
- **Batch label index** — batch 1 = invitation, batch 2 = co-nudge, batches 3+ = reminders; what if the co-nudge is skipped (gate) — is there still a batch 2 entry? What if only 2 batches exist — is `has_next_reminder` correct? What if reminder 2 sent but form also opened — ordering of the "Form opened" timeline line.
- **The "Form opened" timeline insertion — r1 W4 fix.** It must now insert chronologically by timestamp (compare against batch at-values), not at a fixed slot. Walk: form opened before first batch? between batches? after the last batch? equal timestamps? Does the fix handle all orders?
- **First-view auto-expand** — `refcheck_auto_expanded` set grows forever? Stale detail responses (id-mismatch guard); navigation away and back.
- **`field_is_answered`** — null values, empty strings, arrays, unexpected shapes; the r1 note about empty-period objects (count vs render mismatch) — fixed?
- **Row with `form_completed` status but `result: None`** — renders nothing on expand?
- **`status_timestamp`** — `submitted_at` None for terminal rows (old rows without the additive key).
- **Unicode/format edge** — `format_timestamp_short` on Postgres `::text` timestamps ("2026-08-01 21:12:00+00") vs ISO — the r1 note about the `<time datetime>` attribute carrying invalid HTML datetime — fixed (normalized) or still present?
- **relationship_other (r1 W3)** — the referee's verbatim "Other" relationship text now renders with the parent row; walk: `relationship == "other"` with/without `relationship_other` text; `relationship != "other"` but text present.
- **Explainer persistence (r1 W6)** — if localStorage hydration landed, walk: localStorage unreadable (throws), stale key, hydration vs route-reset ordering.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
