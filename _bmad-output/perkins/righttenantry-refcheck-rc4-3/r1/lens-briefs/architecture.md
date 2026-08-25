# LENS: architecture (source tag: `architecture`) — Perkins r1 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract).

Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (conditional-UPDATE mutation ownership AD-14, capability-token public routes AD-3, audit-on-state-change AD-16, Squirrel SQL, expand-only migrations)?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

**Round-specific architecture checks (per the architecture doc + amendments):**

1. **A7 take-over modeling.** `taken_over_at` as a distinct column (NOT a status) — sweep skips taken-over rows (`WHERE ... taken_over_at IS NULL`), status stickiness untouched, late completion still guarded-transitions to `form_completed`. Verify the sweep SQL's exclusion, and that take-over doesn't fork the lifecycle enum (no new status like `taken_over` — the design is a timestamp + label).
2. **AD-7 one-cycle + A1 immutability.** Correct stores `corrected_email`/`corrected_phone` — original `contact_*` snapshot never overwritten; `correction_cycles` = 1 (a fresh field, one correction); re-queues and re-arms the cadence (T0 restart). The awaiting-guard IS the one-cycle rule.
3. **AD-16 audit.** New audit events for: take-over, correction, substitution (old + new ids), exhaustion → `unreachable`. Are they written with the canonical tiered audit pattern (Tier 1 fail-closed / Tier 2 fail-open)? Event types in `audit/event_type.gleam` — new ones added or reused? The `audit_log` row shape is append-only (no column changes to audit_log itself).
4. **AD-14 mutation ownership.** The new actions are two more writers on the row — do they follow the guarded-update + sticky-terminals discipline? Does the exhaust path (webhooks + wrong-person) respect that objection beats everything (an `objected` row must NOT flip to `unreachable` on a late failure)?
5. **§8.2 state rules the API computes (AR-RC13).** The server computes `can_substitute_referee` + hooks; the client renders them. No client-side re-derivation of action legality/status. Verify the new hooks flow through the detail payload.
6. **The substitute CTE idempotency.** An idempotent CTE creating the successor row — is this pattern consistent with the codebase (any prior idempotent CTE precedent)? Does it keep the attempt log on the prior row and start fresh on the successor? Does the successor inherit the slot/cadence correctly?
7. **Module boundaries.** `actions_handler.gleam` as a new module — does it reuse `reference_checks/sql.gleam` and the established service pattern (like `ai/`, `application/`)? Are the 8 new SQL files where they belong (reference_checks/sql/)? Is `notification_dispatch.gleam` change in keeping with the notification module's shape?
8. **Scope drift.** Anything in the diff not asked for by Story RC4.3 (e.g. unrelated refactors, changes to RC4.2 panel behavior, extra endpoints)?

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
