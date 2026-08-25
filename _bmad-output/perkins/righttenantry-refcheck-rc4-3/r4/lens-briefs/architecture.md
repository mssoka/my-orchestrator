# LENS: architecture (source tag: `architecture`) — Perkins r4 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/prior-findings.md` (the r4 FIX AUDIT list — you own the architecture-class items: the r3 TOCTOU BLOCKER, r3 W4 sweep-terminal guards, r3 N8/N9-spec drift, r3 N20 trio_matches_row name basis, r3 N21 one-cycle SQL backstop).

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (conditional-UPDATE mutation ownership AD-14, capability-token public routes AD-3, audit-on-state-change AD-16, Squirrel SQL, expand-only migrations)?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

**Round 4 — VERIFY-DON'T-REOPEN: FIRST classify each prior architecture-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r3): `). Then hunt NEW issues.**

**Round-specific architecture checks:**

1. **A7 take-over modeling + THE r3 TOCTOU BLOCKER.** `taken_over_at` as a distinct column — sweep skips taken-over rows, status stickiness untouched, late completion still guarded-transitions to `form_completed`. **The round's #1 mandate:** the wrong-person awaiting transition must carry the `taken_over_at IS NULL` backstop in the EXECUTED path (see _shared.md). The PR ADDS `mark_awaiting_correction_wrong_person.sql` (guarded) — but if the handler still executes `update_reference_call_status` (unguarded on taken_over_at), the guarded SQL is DEAD CODE: an orphaned, unwired query module. Orphan code is itself an architecture finding; the unwired backstop is a blocker. Check which query `apply_wrong_person` in form_handler.gleam actually calls. Also: is the stand-down modeled at the find/guard layer (one place) or duplicated at every call site — with the wrong-person leg now inconsistent with the webhook leg?
2. **AD-7 one-cycle + A1 immutability.** Correct stores `corrected_email`/`corrected_phone`/`corrected_name` — original `contact_*` snapshot never overwritten; `correction_cycles = 1`. The r3 N21: `correction_cycles = 0` backstop in mark_awaiting_correction's WHERE (verify present). The one-cycle rule must hold across BOTH failure routes (webhook mark_awaiting_correction AND wrong-person leg).
3. **AD-16 audit.** New audit events: take-over, correction, substitution (old + new ids), exhaustion → unreachable. Canonical tiered audit pattern; event types in `audit/event_type.gleam`. Idempotent substitute no-op must NOT double-write on double-submit.
4. **AD-14 mutation ownership.** Guarded-update + sticky-terminals discipline on every action; the exhaust path (webhooks + wrong-person) must respect that objection beats everything; the app↔vacancy precheck still the single canonical gate.
5. **§8.2/AR-RC13 — server-computed hooks.** Server computes `can_take_over` / `can_substitute_referee`; client renders. No client-side re-derivation.
6. **Substitute idempotency.** Substitute reuses the shared idempotent insert (predicate in ONE place; concurrent double-submits resolve). Fraud stamping only on REAL inserts. The r3 N20: `trio_matches_row` vs `trio_matches` must use the SAME effective-name basis (COALESCE(NULLIF(corrected_name,''), contact_name)).
7. **Module boundaries.** `actions_handler.gleam` reuses `reference_checks/sql.gleam`; new SQL files where they belong; `notification_dispatch.gleam` change in keeping; exhaustion notification interpolates the CORRECTED name post-correction.
8. **The new `mark_awaiting_correction_wrong_person.sql` + its generated code in sql.gleam** — if unwired, that's an orphan module shipped in the PR (generated from a SQL file nobody calls). Flag as orphan unless the handler calls it.
9. **Scope drift.** Anything in the diff not asked for by Story RC4.3?

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
