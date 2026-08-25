# LENS: tests (source tag: `tests`) — Perkins r1 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Behaviours to trace (from the panel implementation `client/src/components/reference_panel.gleam` + copy + tests):

1. **The 12-state matrix** — is EVERY §4.2 state covered by a test that asserts the verbatim label AND the pill colour class AND the state-specific copy? (queued, invitation sent, reminder sent, form opened, received, partial, awaiting correction, unreachable, refused, objected, skipped, failed, plus ManualRecorded-as-received, plus the v2-reserved Scheduled/Calling/Completed degradation.)
2. **Off state** — chips render, NO re-ask, card visible with zero rows.
3. **Pre-v1 hidden card** — no choice, no rows, no attestation.
4. **Pre-trigger A5 sub-line** and in-flight / all-terminal sub-lines.
5. **Completed summary** — headline pull-quote, key-facts words mapping (ALL wire values → words: yes/no/not_sure/unsure/prefer_not_to_say/always_on_time/... — is the full word map tested or just a sample?), "Not answered" for unanswered, period/amount/as-stated renderers (from/to/ongoing/dont_remember/differs/stated/dont_know), free-text + unmoderated flag, ≤3 notable quotes, worth-knowing signals (each signal sentence? fast-completion threshold 120s?), confidence line, display_disclaimer.
6. **Expand/collapse toggle** — aria-expanded flips, detail region appears/disappears.
7. **First-view auto-expand** — the `client.gleam` handler logic (first_view, summary_ids, refcheck_auto_expanded) — is it tested? (This is logic in client.gleam's update_inner — check whether any existing client update test covers it.)
8. **Route-change reset** of refcheck_expanded/explainer.
9. **Back-compat decoder** — old payload without form_opened_at/submitted_at decodes; round-trips with values; wire snake_case.
10. **Server serializer** — form_opened_at/submitted_at ride through encode_reference_call; nulls when empty.
11. **Negative controls** — no red pill anywhere; no re-ask in Off; overflow ABSENT on terminal rows; "Not answered" not "guessed"; no worth-knowing block without signals.
12. **Test-level mix** — client component tests via serialized render (per field notes: sorted attributes, `&#39;`); shared round-trips; server unit. Any missing integration coverage for the new server columns?

Blind-spot heuristics: happy-path-only coverage where error handling is implied (e.g. malformed result JSON in view_completed — tested?), new state transitions without boundary tests (e.g. form_opened_at + reminder both present).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80% · CONCERNS: P0 100%, P1 80–89%, overall ≥80% · FAIL: P0 <100%, or P1 <80%, or overall <80%.
