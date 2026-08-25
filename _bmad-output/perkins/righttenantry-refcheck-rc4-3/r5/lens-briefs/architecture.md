# LENS: architecture (source tag: `architecture`) — Perkins r5 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/_shared.md`
FIRST (shared context, inputs, lens-guards, output contract), then
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
(the r5 FIX AUDIT list — you own the architecture-class items: B1 TOCTOU wiring, W1
legacy co-nudge exclusion, N7 trio_matches_row basis, N9 fallback-leg trade-off).

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (conditional-UPDATE mutation ownership
  AD-14, capability-token public routes AD-3, audit-on-state-change AD-16, Squirrel SQL,
  expand-only migrations)?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

**Round 5 — VERIFY-DON'T-REOPEN: FIRST classify each prior architecture-class finding
against the current worktree (fixed = silent; still present/wrong fix = finding with
original severity, title prefixed `STILL PRESENT (r4): `). Then hunt NEW issues.**

**Round-specific architecture checks:**

1. **A7 take-over modeling + B1 TOCTOU.** `taken_over_at` as a distinct column; sweep skips
   taken-over rows; status stickiness untouched; late completion still transitions. **The
   round's #1 mandate:** the wrong-person awaiting transition must carry the
   `taken_over_at IS NULL` backstop in the EXECUTED path (see _shared.md). Check which
   query `apply_wrong_person` actually calls — the guarded
   `mark_awaiting_correction_wrong_person` (wired) vs the unguarded
   `update_reference_call_status`. Is the stand-down modeled at the find/guard layer (one
   place) or duplicated at every call site — and are the wrong-person leg and the webhook
   leg now consistent?
2. **AD-7 one-cycle + A1 immutability.** Correct stores `corrected_*` — original `contact_*`
   snapshot never overwritten; `correction_cycles = 1`. The one-cycle rule holds across
   BOTH failure routes (webhook mark_awaiting_correction's `correction_cycles = 0` AND the
   wrong-person leg's — verify both in the worktree SQL).
3. **AD-16 audit.** New audit events: take-over, correction, substitution (old + new ids),
   exhaustion → unreachable. Canonical tiered audit pattern; event types in
   `audit/event_type.gleam`. Idempotent substitute no-op must NOT double-write on
   double-submit.
4. **AD-14 mutation ownership.** Guarded-update + sticky-terminals discipline on every
   action; the exhaust path (webhooks + wrong-person) respects that objection beats
   everything; the app↔vacancy precheck the single canonical gate (N10's Error arm).
5. **§8.2/AR-RC13 — server-computed hooks.** Server computes `can_take_over` /
   `can_substitute_referee`; client renders. No client-side re-derivation.
6. **Substitute idempotency.** The shared idempotent insert (predicate in ONE place;
   concurrent double-submits resolve). N7: `trio_matches_row` now uses the EFFECTIVE basis
   (corrected ?? snapshot) — consistent with the panel prefill (what the landlord sees) and
   with the insert that created the successor? Walk the no-op compare end to end.
7. **Module boundaries.** `actions_handler.gleam` reuses `reference_checks/sql.gleam`; new
   SQL files where they belong; the r5 changes to webhooks/form_handler/sql.gleam stay in
   their modules; `notification_dispatch.gleam` change in keeping.
8. **The batch-shape co-nudge exclusion (W1).** The predicate now lives in FOUR copies
   (matched_send_at, send_is_post_correction, send_is_malformed, EXISTS) inside one SQL
   file — duplication within a single query is acceptable; drift risk between them? Are all
   four copies byte-identical in their exclusion?
9. **N9 fallback-leg trade-off (carried).** Verify the justification is REAL and documented
   in the SQL header comment; do not demand rework of a documented trade-off.
10. **Scope drift.** Anything in the r4→r5 delta not asked for by the round-5 mandate?

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
