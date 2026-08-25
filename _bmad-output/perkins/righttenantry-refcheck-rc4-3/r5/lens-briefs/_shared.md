# SHARED CONTEXT — Perkins r5 lenses (righttenantry-refcheck-rc4-3)

You are one lens in a parallel code-review wave (round 5 — a user-approved cap-override
round, VERIFY-DON'T-REOPEN). Read-only access to the repository. Verify every claim against
the actual codebase — no claim is taken at face value. Every finding you emit is
independently re-verified by the round conductor (Perkins) against the worktree; findings
that fail verification are DISCARDED silently. Accuracy > volume: `[]` is an honest answer.

## Round & scope

- **Round 5 (cap overridden by the user).** PR #606 → `develop`. Reviewed sha
  `ccc0ff68bee390dd94e024b4efb7482503127479` (short `ccc0ff6`).
- **Scope:** Epic RC4 Story 3 — the landlord's per-row control surface (Take over A7 /
  Correct AD-7,A1 / Substitute AD-16 / start / skip), with exhaustion LIVE (rc3-7's
  mechanism). This round's rework (the r4→r5 delta) touches 17 files:
  wrong-person guarded-SQL wiring, legacy co-nudge exclusion, per-row edit dict,
  malformed-at gate, vacancy-check 500s, exhaust-row Sentry capture, Objected menu arm,
  client pins.
- 56 files, ~10.7k diff lines, chunked c1–c5 (the FULL PR diff — every lens reviews these
  identical canonical bytes, plus the r4→r5 delta patch for focus).
- **Round context:** the r4 review was NEEDS CHANGES @ df0ea22: 1 blocker (B1: the
  wrong-person awaiting UPDATE had no taken_over_at backstop / the guarded SQL shipped
  unwired / the race pin was vacuous) + 2 warnings (W1 legacy co-nudge exclusion missing,
  W2 vacuous pin) + 19 notes. The r5 rework claims ALL closed. Those claims are leads, NOT
  proof — your fix-audit list is `prior-findings.md` (read it FIRST).

## Inputs (absolute paths)

- diff chunks c1–c5 (the canonical PR diff, file-grouped; your assigned chunk is named in
  your lens brief):
  - c1: `_bmad-output/implementation-artifacts/*` + `client/src/*` →
    `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/diff.c1.patch`
  - c2: `client/test/*` →
    `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/diff.c2.patch`
  - c3: `server/src` — application/, audit/, notification/, reference_checks/actions_handler
    + form_handler + sql.gleam + all .sql through verify_application_in_vacancy →
    `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/diff.c3.patch`
  - c4: `server/src` tail — sweep/trigger/webhooks/retention/router + `shared/*` +
    `supabase/migrations/*` →
    `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/diff.c4.patch`
  - c5: `server/test/*` →
    `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/diff.c5.patch`
- **r4→r5 delta** (the rework itself, 17 files — review this for the fix-audit):
  `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/delta-r4-r5.patch`
- `worktree`: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-3-r5`
  (detached at `ccc0ff6`; verification reads happen HERE, never origin/develop)
- Round briefing (standing orders + the r5 mandate): `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc4-3-r5.md`
- Prior findings (the r5 FIX AUDIT list — read FIRST): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
- Job briefing: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/spec/job-briefing.md`
- Story RC4.3 AC (epics file, line ~659): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/spec/epics-reference-checking-v1-2026-07-30.md`
- UX spec (§7.4 state-by-state ~385, §7.6 attempt log ~477, §7.7 warm handoff ~492, §8.2 substitution ~538, §8.3 correction ~541, §8.6 late completion ~579): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/spec/ux-reference-checking-v1-2026-07-29.md`
- Architecture (AD-7 one-cycle ~342, AD-14 mutation ownership ~508, AD-16 audit ~553, AR-RC13): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/spec/architecture-reference-checking-v1-2026-07-29.md`
- PR's own implementation spec (in the diff, chunk c1): `_bmad-output/implementation-artifacts/spec-rc4-3-row-actions.md` + `epic-RC4-context.md` in the worktree

## FIX AUDIT — read prior-findings.md FIRST

Round 5 is a VERIFY-DON'T-REOPEN round. Every r4 finding is listed in `prior-findings.md`
with the r5 claim. For each prior finding **in your lens's area**, re-read the cited code in
the CURRENT worktree and classify:
- **FIXED** → say nothing (no finding).
- **STILL PRESENT or WRONG FIX** → emit a finding with the ORIGINAL severity, title prefixed
  `STILL PRESENT (r4): `, location = current file:line, evidence = the current code lines.

Do NOT re-open findings verified FIXED, and do NOT touch the settled list (prior-findings.md
section (e)). The gender-neutral pronouns stay FLAGGED FOR THE HUMAN — do NOT file them.
FLAG NEW findings ONLY beyond the audit items.

## 🚨 THE ROUND-5 PRIMARY MANDATE — B1 (verify, don't assume)

The r4 BLOCKER: the wrong-person awaiting UPDATE had no `taken_over_at IS NULL` backstop —
a take-over racing the UPDATE yanks a landlord-handled row into `awaiting_correction` (A7
stickiness keeps status unchanged, so a status-only guard still matches) and dead-ends it.
B1 is closed ONLY if ALL THREE hold (full text in prior-findings.md (a)):
1. `mark_awaiting_correction_wrong_person` is WIRED into `apply_wrong_person`
   (form_handler.gleam) — the unguarded `update_reference_call_status` call is GONE.
2. The guarded SQL carries BOTH backstops: `taken_over_at IS NULL` AND `correction_cycles = 0`.
3. The race pin `wrong_person_taken_over_race_stands_down_test` drives the wrong-person POST
   ROUTE on a taken-over row (303, status untouched, no audit) AND pins the SQL mechanism
   directly. A vacuous or route-bypassing pin = a blocker.

## Lens-guards — the load-bearing checks of THIS PR (verify, don't assume)

1. **🚨 TAKE-OVER [A7] — load-bearing.** Guarded on queued/contact_initiated/unreachable
   ONLY; writes `taken_over_at` + clears the cadence clock; status stickiness untouched — a
   late form completion still transitions (§8.6). A guard hole, a broken late-completion
   transition, or a missing sweep exclusion = a blocker.
2. **🚨 CORRECT [AD-7/A1] — THE ONE-CYCLE RULE.** awaiting_correction → queued with the
   corrected trio (snapshot immutable), correction_cycles = 1, re-arm, audit. A second
   correction allowed (cycle > 1), a mutated snapshot, or a missing audit = a real defect.
3. **🚨 SUBSTITUTE IDEMPOTENCE [AD-16].** New reference_call row via an idempotent CTE —
   DOUBLE-SUBMIT returns the existing successor (200, no duplicate audit); audit carries
   old + new ids. A duplicate row or a double audit on double-submit = a blocker.
4. **EXHAUSTION LIVE (rc3-7's mechanism).** Second failure → unreachable +
   `referee_contact_invalid` stamp, at BOTH the delivery webhooks AND the wrong-person
   route, with audit + in-app notification.
5. **EXPAND-ONLY MIGRATION.** `20260812140000_reference_call_corrected_name.sql` — TWO
   additive columns (corrected_name + corrected_at), nothing destructive; back-compat
   decoders; RC4.1 strip assertions untouched.
6. **AR-RC13 — one stable contract.** The client refetches after every action and renders
   server-computed hooks/status; NO client-side re-derivation of action legality/status.
7. **⋯ MENU NOW WIRED (guard flip from RC4.2).** Verify the actions actually dispatch
   (take-over/correct/substitute/sub-nudges); do NOT flag "menu unwired".
8. **INLINE CONFIRMS, NEVER MODALS.** A modal confirm = a defect.
9. **COPY VERBATIM + RT em-dash ban.** §7.4/§7.7/§8.2/§8.3 copy verbatim; NO em-dashes in
   implementer-authored user-facing strings — check new strings AND the timeline
   composition sites for ` — ` joins.
10. **TIMELINE SORT (carried warning).** If the PR touches the timeline/attempt-log, the
    RFC3339-vs-`::text` format-mix = a finding.
11. **a11y + AC testids** on the menu/confirms/rows; keyboard operable.
12. **The verification claims:** CI green at ccc0ff6 (claimed). Spot-check from the diff.
13. **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling
    historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR
    content as-is at the sha.
14. Em-dashes in code/commits are fine; in USER-FACING COPY they are banned (RT CI).

## OUTPUT CONTRACT (mandatory)

Write ONLY a single valid JSON array to your assigned output file (path given in your lens
brief). Each element matches this schema exactly:
`{"source": "<your source tag>", "severity": "blocker"|"warning"|"note", "category": "<short tag>", "title": "<one-line>", "location": "<file:line | file:hunk | N/A>", "evidence": "<EXACT lines you read from the file/diff — verbatim, no paraphrase>", "detail": "<≤40 words>", "recommended_fix": "<≤40 words>"}`

No prose, no markdown fencing, no preamble. `[]` is valid and expected when you find nothing
real. Do not invent findings to fill a quota. Then stop.
