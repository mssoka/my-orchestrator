# LENS: tests (source tag: `tests`) — Perkins r2 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

**Round-2 priority — r1 fix-audit half (verify each landed as a TEST, don't re-open):**

1. **W8 — auto-expand handler tests.** r1 W8: first-view auto-expand + toggle/route-reset update logic had zero coverage; the fix claimed update-level tests in `client/test/client_test.gleam`. Verify tests exist for: first-view auto-expand (only when there's a summary to expand), toggle messages, route-change reset. Also the r1 note "auto-expand consumed by first detail landing even when nothing to expand" — is the insert now gated on `summary_ids` non-empty, AND is THAT tested?
2. **W8 — total-match word-map test.** The spec mandates every wire value resolves; r1 W8 says the total-match test was absent and W2 (unmapped "landlord") shipped because of it. Verify a test iterates ALL wire values (from `server/src/reference_checks/questions.gleam` / result.gleam) through `refcheck_choice_word` and asserts no raw fallthrough — and that it would catch "landlord" specifically.
3. **W1 — em-dash ban coverage.** r1 W1: `no_em_dash_test` iterated `for_each_copy` (toast/page codes only) so refcheck consts bypassed the pin. Fix claimed: the test now scans refcheck copy too. Verify the refcheck consts (incl. timeline labels, unmoderated flag) are inside the scanned set.
4. **B1 — hook-driven sub-line test.** Is there a test asserting the all-terminal sub-line derives from `hooks.can_record_manual` (e.g. a Completed row with can_record_manual=false → "All references closed")?
5. **Cheap notes (spot-check each landed):** never-red full-token test (asserts pill class is one of the four consts, or scans any red token); object-branch tests (ongoing/dont_remember/differs/stated/dont_know/different_amount_eur/as_stated fixtures); per-signal sentence tests (each of the 7 worth-knowing sentences); integration wire pins for `form_opened_at`/`submitted_at` (empty→null + populated ride-through on the wire); v2-degradation tests (Scheduled/Calling/Completed pills); malformed-result JSON test; aria-expanded='true' test.

**Then the fresh trace** (new behaviour the rework added — e.g. relationship_other rendering, chronological timeline merge, localStorage hydration if landed):

1. **The 12-state matrix** — every §4.2 state covered by a test asserting the verbatim label AND pill colour AND state copy?
2. **Off state / pre-v1 hidden card** — chips render, no re-ask, card hidden with no choice/rows/attestation.
3. **Completed summary** — headline, key-facts words, "Not answered", period/amount renderers, free-text + unmoderated flag, ≤3 notable quotes, worth-knowing block, confidence line, display_disclaimer.
4. **Expand/collapse** — aria-expanded flips both ways.
5. **Back-compat decoder** — old payload without form_opened_at/submitted_at decodes; round-trips with values; snake_case keys.
6. **Negative controls** — no red pill; no re-ask in Off; overflow absent on terminal rows; no worth-knowing without signals.

Blind-spot heuristics: happy-path-only coverage where error handling is implied; new state transitions without boundary tests.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80% · CONCERNS: P0 100%, P1 80–89%, overall ≥80% · FAIL: P0 <100%, or P1 <80%, or overall <80%.
