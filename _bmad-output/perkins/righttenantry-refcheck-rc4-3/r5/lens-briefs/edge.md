# LENS: edge (source tag: `edge`) — Perkins r5 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/_shared.md`
FIRST (shared context, inputs, lens-guards, output contract), then
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
(the r5 FIX AUDIT list — you own the edge-class items: B1 TOCTOU, W1 legacy co-nudge
exclusion, W2 pin-bite, N8 malformed-at, N9 fallback-leg trade-off, N10 vacancy-check
error, N11 exhaust-row error, N16 sweep_mark_failed pin).

You are a pure path tracer. Do not comment on whether the code is good or bad — list only
unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable
from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist.
Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent
operations and race conditions, unhandled error paths in new code, external service
unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new
code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack
an explicit guard in the diff; discard handled ones silently. No editorializing.

**Round 5 — VERIFY-DON'T-REOPEN: FIRST classify each prior edge-class finding against the
current worktree (fixed = silent; still present/wrong fix = finding with original severity,
title prefixed `STILL PRESENT (r4): `). Then walk the r5 rework's new code for NEW
unhandled paths.**

**Round-specific paths to walk (round 5):**

1. **B1 TOCTOU — the round's #1 mandate.** Walk the actual flow in the worktree:
   `handle_wrong_person_post` → `apply_wrong_person` — which query does the
   cycles=0 arm execute? If it still called `update_reference_call_status` (WHERE only
   id+status), the guarded SQL is dead code and the race is OPEN. Verify:
   - the wired call is `mark_awaiting_correction_wrong_person` (both backstops in the SQL);
   - the 0-row arm redirects (race lost → 303, no audit, no transition);
   - the read-time `taken_over_at != ""` arm still stands down;
   - `correction_cycles >= 1` read-time arm still routes to exhaust_wrong_person;
   - take-over racing BETWEEN read and UPDATE: 0 rows → redirect → structurally impossible
     to yank a landlord-handled row.
2. **W1 legacy co-nudge exclusion — the batch-shape predicate.** Walk:
   - a legacy untagged single-email co-nudge entry whose bounce arrives POST-correction
     (must stand down — no exhaust, no referee_contact_invalid);
   - a GENUINE referee email send: does the sweep always append an sms sibling (delivered OR
     skipped) at the same `at`, so the genuine case is never excluded? (read the sweep's
     `outcomes_to_json`/`send_invite` in the worktree);
   - an email entry whose sibling sms entry carries outcome 'failed'/'skipped' — still a
     sibling (the predicate checks channel only, not outcome) — not excluded, correct?
   - the `s->>'at' = e->>'at'` string-equality join: same writer, same format — any
     format-mix risk (RFC3339 vs space)?
   - both timestamp subqueries AND the EXISTS leg carry the exclusion (a missed leg = the
     legacy bounce still exhausts via that leg).
3. **N8 malformed-at gate.** Walk: a present-but-malformed `at` on the matched entry
   (regex fails → matched_send_at='' + send_is_malformed=true → stand down ✓); an at-less
   (NULL at) delivered entry — `NULL ~ regex` is NULL → `NOT NULL` is NULL → COALESCE false
   → matched_send_at='' → genuine_failure=true → EXHAUST. Is that reachable (does any
   writer produce an at-less entry)?; a well-formed pre-correction entry on a post-correction
   row (typed compare → stand down ✓); the fallback-path '' (no send-ref match at all,
   cycles=0) — still treated genuine (crash-mid-tick doctrine).
4. **N9 fallback-leg trade-off (carried).** Verify the justification is REAL: the SQL
   comment documents the pre-correction-only fallback; a genuine post-correction
   crash-mid-tick send (send_ref never appended) cycles until the sweep's sequence terminal
   — walk what the sweep terminal does (unreachable, NO stamp) and note whether the
   trade-off is documented, not whether you'd design it differently.
5. **Exhaustion live.** Second failure → unreachable + stamp at BOTH routes; first failure
   must NOT exhaust; the wrong-person exhaustion leg's 0-row/Error split; exhaustion racing
   a concurrent terminal (0-row → stand down); DB error on the exhaustion UPDATE
   (webhooks: Sentry capture, event acked; wrong-person: log + 500).
6. **Client per-row edit dict.** Two rows both mid-edit (one Correct + one Substitute);
   cancel on one row must not drop the other; action success on row A must not clear row B's
   edit or confirm; the dict on route change resets; `UserEditedRefcheckTrio` for a row
   whose edit dict entry is missing (prefill fallback).
7. **Escape-close.** tabindex="-1" + autofocus on the menu div — walk the click-then-Escape
   flow (focus lands on the div?); the keydown handler's decoder; menu toggle idempotence.

Verify each path against the actual worktree code (read the handler + SQL + client code),
not just the diff. Report only unhandled paths. Accuracy > volume.
