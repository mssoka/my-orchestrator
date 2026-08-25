# LENS: acceptance (source tag: `acceptance`) — Perkins r5 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/_shared.md`
FIRST (shared context, inputs, lens-guards, output contract), then
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
(the r5 FIX AUDIT list — you own the acceptance-class items: B1 TOCTOU, N1 per-row edit,
N2 Escape, N3 spec drift, N5 duplicate §8.3 copy, N12 Cancel literal, N13 Objected menu arm,
N15 client dispatch pins, N17 confirm scoping, N18 substitute prefill).

Audit the diff against the spec. Identify:
- Violations of specific acceptance criteria (Story RC4.3 AC in the epics file, line ~659)
- Deviations from spec intent (UX §7.4/§7.6/§7.7/§8.2/§8.3/§8.6, architecture
  A7/AD-7/A1/AD-14/AD-16/AR-RC13)
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

**Round 5 — VERIFY-DON'T-REOPEN: FIRST classify each prior acceptance-class finding against
the current worktree (fixed = silent; still present/wrong fix = finding with original
severity, title prefixed `STILL PRESENT (r4): `). Then walk the AC line by line for NEW
deviations.**

Walk the Story RC4.3 AC line by line against the diff:

1. **AC1 — Pre-trigger row actions.** `⋯` overflow on a queued row: "Start this check now"
   (asks once inline, §7.4 copy, RC2.3 API with per-row `?slot=`) + "Skip this reference"
   (excludes, re-enable-able). Both dispatch.
2. **AC2 — In-flight row take-over.** queued/contact_initiated/unreachable → inline §7.7
   confirm (never a modal) → `taken_over_at`, sweep stops, chips + export render inline,
   "You're handling this one"; form link stays live — a late completion still transitions
   (§8.6). **B1: the wrong-person route's awaiting transition must carry the executed
   `taken_over_at IS NULL` backstop (see _shared.md — the round's #1 mandate) AND the race
   pin must drive the real POST route + the SQL mechanism.**
3. **AC3 — awaiting_correction correct.** Inline edit-trio per §8.3 behind a button
   (Name/Email/Phone + "Save & resend" + applicant contact chips); audit-logged;
   `corrected_*` snapshot immutable (contact_* never overwritten); correction_cycles = 1;
   re-queue + re-arm + fresh form_token; session state (form_opened_at, draft_answers)
   cleared. **THE ONE-CYCLE RULE:** a second correction impossible — awaiting guard IS the
   rule; the wrong-person SQL also carries `correction_cycles = 0` (verify present).
4. **AC3b — Exhaustion LIVE.** Second failure → unreachable + referee_contact_invalid at
   BOTH the delivery webhooks AND the wrong-person route, with audit + in-app notification.
   Stale-bounce gates (same-day typed, fallback pre-correction-only, co-nudge exclusion)
   stand down non-genuine failures without swallowing genuine ones.
5. **AC4 — Terminal objected/unreachable substitute.** `can_substitute_referee` hook; NEW
   reference_call row (prior retained as history); audit carries old + new ids (AD-16);
   idempotent double-submit (200, no duplicate audit); identical-trio → 400 with EMPTY
   prefill; history-row re-submit with DIFFERENT details → 409. **The r5 N7 change:
   trio_matches_row now uses the EFFECTIVE basis (corrected ?? snapshot) — verify the
   400-no-op compare, the 409 guard, and the Objected menu arm all stay coherent.**
6. **AC5 — Every action endpoint** ownership-checked + pre-state guarded (AD-14); manual
   actions hidden entirely in the Off (declined) state; app↔vacancy precheck holds
   (N10: a DB error on the vacancy check must NOT run the action).
7. **COPY VERBATIM — the load-bearing invariant.** §7.4/§7.7/§8.3 copy verbatim; **RT CI
   ban: NO em-dashes in implementer-authored user-facing strings** — check
   `client/src/copy.gleam` new strings byte by byte AND the timeline/attempt-log
   composition sites for ` — ` joins. Where the UX spec itself ships an em-dash, verbatim
   wins; an em-dash ADDED by the implementer is a defect. (The pronoun deviation stays
   FLAGGED FOR THE HUMAN — do NOT file it.)
8. **AR-RC13 — one stable contract.** Client refetches after every action and renders the
   server-computed hooks/status; NO client-side re-derivation of action legality/status.
9. **a11y + AC testids** on the menu/confirms/rows; keyboard operable (the N2 Escape flow).

For each finding, reference the violated AC or spec phrase in `detail` (quote the exact
phrase from the spec when possible). Verify against the worktree — read the actual
handler/SQL/client code. Quote exact lines in `evidence`.
