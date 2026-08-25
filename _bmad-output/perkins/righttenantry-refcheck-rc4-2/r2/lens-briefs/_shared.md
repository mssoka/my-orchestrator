# SHARED CONTEXT — Perkins r2 lenses (righttenantry-refcheck-rc4-2)

You are one lens in a parallel code-review wave. Read-only access to the repository. Verify every claim against the actual codebase — no claim is taken at face value.

## Round & scope

- **Round 2 of 3.** PR #605 → `develop`. Reviewed sha `e0f9fa7fee2c93dc349cc3fb408e66400401bf87` (short `e0f9fa7`).
- **Scope:** Epic RC4 Story 2 — the landlord Reference Panel (Status & Summary). The CLIENT renders the RC4.1 `reference_calls[]` contract: all 12 lifecycle states (UX §4.2/§7.4 copy verbatim), the completed-summary pull-quote + key-facts table, "Worth knowing" signals, the §9.5 disclaimer, §13 pill colours (never red), the §7.8 explainer, full a11y contract. Plus an expand-only contract addition (`form_opened_at`, `submitted_at`) with back-compat decoders.
- 17 files, 3932 diff lines. Full PR diff at `diff_file` (chunked into c1/c2/c3 for size). Review EXACTLY those bytes; the worktree is at the same sha for verification.
- base = `develop` (RC1–RC4.1 merged — do NOT re-open their findings; carry-forward only).

## Inputs (absolute paths)

- `diff_file` chunk 1 (spec artifact + all client/src): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/diff.c1.patch`
- `diff_file` chunk 2 (client tests): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/diff.c2.patch`
- `diff_file` chunk 3 (server + shared): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/diff.c3.patch`
- `worktree`: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r2` (detached at `e0f9fa7`; verification reads happen HERE)
- Round briefing (lens-guards + standing orders): `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc4-2-r2.md`
- Job briefing: `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-2.md`
- Story RC4.2 AC (epics file, Story RC4.2 at line ~629): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r2/_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`
- UX spec (authoritative copy — §4.2 lifecycle labels ~line 64, §7.1–7.8 panel ~324–532, §10.3 copy deck ~643, §12 a11y ~677, §13 design-system ~691): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r2/_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`
- Architecture (RC4.1 contract — §8.1 payload ~974, §8.2 hooks ~996, §9.3 unmoderated flag ~1050, §9.5 disclaimer ~1075): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r2/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`
- **r1 prior findings (fix audit — verify, don't re-open):** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/consolidated.json`

## 🚨 ROUND-2 MANDATE — fix audit FIRST, then fresh findings

This is round 2. The r1 review (NEEDS CHANGES @ 9d66ce9) found **1 blocker + 8 warnings + 13 notes**, all allegedly addressed in the r1 rework (head e0f9fa7). Your job:

1. **Fix audit (lead with it):** for each r1 finding below, re-read the cited code in THIS worktree and classify `fixed` or `still-present`. A missing or wrong fix is itself a finding (report it with severity = the r1 severity). Do NOT re-open a finding that has genuinely landed — a fixed finding is not a new finding.
2. **Fresh findings:** anything new the r1 rework introduced (new bugs, new copy deviations, weakened tests, scope drift in the rework commits).
3. Only findings that survive your own verification get reported.

### The r1 fix map (verify EACH)

| # | r1 finding (severity) | Claimed fix (from rework commit 167a43b) |
|---|---|---|
| B1 | Panel re-derives terminality client-side (`is_terminal`), set omitted Completed | Hook-driven terminality: `list.all(calls, fn(c) { not c.hooks.can_record_manual })`; no client `is_terminal` re-implementation |
| W1 | Em-dashes in implementer-authored strings (unmoderated flag + nudge-failed timeline label) | Both rewritten without em-dashes; `no_em_dash_test` extended to scan refcheck consts |
| W2 | Key-facts word map keys on phantom `their_landlord`; wire value `landlord` renders raw | `"landlord"` mapped in `refcheck_choice_word` + total-match word-map test |
| W3 | `relationship_other` (referee's verbatim Other text) never rendered | Rendered with the parent "Other" row |
| W4 | 'Form opened' timeline line pinned after invitation batch | Chronological insertion by timestamp |
| W5 | Objected-state copy hardcodes 'him' | Gender-neutral 'them' |
| W6 | Explainer dismissed-state spec drift (no localStorage persistence) | Either localStorage `rt_refcheck_explainer_dismissed` implemented per PR spec, or spec amended + documented decision |
| W7 | Character slot 'answered {m} of {n}' counts `free_text_signals` (7 vs honest 6) | `free_text_signals` excluded from character slot count [6-of-6] |
| W8 | Auto-expand update logic + total-match word-map test absent | Handler tests for auto-expand/toggle/route-reset + total-match word-map test |
| notes | datetime normalization (form-opened `<time datetime>`), dead const `refcheck_off_contacts_label`, month_abbr dedup, never-red full-token test, object-branch/signal tests, integration wire pins, v2-degradation/malformed/aria tests | All cheap notes allegedly landed too — spot-check each |

## ⚠️ Lens-guards — the load-bearing checks of THIS round (verify, don't assume)

1. **🚨 UX COPY VERBATIM — the load-bearing invariant.** All 12 lifecycle states render the UX spec's §4.2/§7.4 copy VERBATIM. **RT CI ban: NO em-dashes in user-facing copy** — flag any deviation (a missing state, reworded copy, or an em-dash in shipped strings = a real defect). NOTE: the UX spec's own copy contains em-dashes in some §7.4 strings (e.g. "Invitation, 2 reminders, and an applicant nudge over 6 days — no reply"); where the spec itself ships an em-dash, verbatim wins — but an em-dash ADDED by the implementer where the spec has none, or in implementer-authored strings not in the spec (e.g. timeline labels, "More actions for" label), is a defect. Check `client/src/copy.gleam` against §4.2/§7.4/§7.5/§7.8/§10.3 byte by byte.
2. **🚨 PILL COLOURS — NEVER RED (§13).** Teal (received), slate (waiting/queued/declined/objected/skipped), navy (reminder/opened/invitation), amber (needs-attention: partial/awaiting-correction/unreachable/failed). A red pill anywhere = a blocker (test-pinned; a neutralization must go red).
3. **NEVER GUESS.** The key-facts table renders "Not answered" where the payload has no answer — NEVER a guessed value. A fabricated value, or a derived value presented as a fact (the wireframe's "As stated" Period) = a real defect. The Period deliberately shows the confirmed dates (from/to) instead of "As stated" (not client-side derivable — documented) — do NOT flag that; DO flag any invented date or fabricated value.
4. **"WORTH KNOWING" ONLY WHEN PRESENT.** Signals render only when the payload carries them; notable quotes only when `ai_summary.notable_quotes` exists (v1 deterministic summaries never emit them — RC5.1 will). Do NOT flag "quotes missing" — that's the design. DO flag a signal block rendered without payload signals.
5. **OVERFLOW BUTTON DELIBERATELY NOT WIRED (guard!).** The ⋯ overflow button renders with its testid but is deliberately not click-wired — RC4.3 owns the actions (no dead-menu placeholder items). Do NOT flag "dead button" — a click-wired menu with placeholder items WOULD be a defect.
6. **EXPAND-ONLY CONTRACT (back-compat).** `form_opened_at` + `submitted_at` are additive on `ReferenceCallDetail`; the decoders are back-compat (old payloads still decode — absent-key default None) and the RC4.1 §4.2 strip assertions (escaped-marker guard, jsonb_typeof guards, internal-field absence) are untouched. A breaking change (old payloads fail to decode, strip assertions weakened, wire keys renamed) = a blocker.
7. **HOOKS/DISCLAIMER INTEGRITY (from RC4.1 — the panel must not re-derive).** The panel renders the server-computed hooks + `display_disclaimer`; it must NOT re-derive state rules client-side (one-stable-contract AR-RC13). A client-side re-derivation of hook/status rules = a blocker. (Display mapping of the server's status enum to §4.2 labels is fine; re-implementing hook logic is not.)
8. **a11y CONTRACT + AC TESTIDS.** Card `role="region"` + `aria-label="Reference checks"`; rows are buttons with `aria-expanded`/`aria-controls`; status never colour-only; testids `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}` all present on the right elements. A missing testid on a stated AC element, or a keyboard/focus trap = a real defect.
9. **§9.5 DISCLAIMER VERBATIM + confidence line** on written-channel results (server-rendered `display_disclaimer` rendered as-is; "Confidence: {level} · AI-generated summary — verify before relying on it."); minimal terminals carry none.
10. **"answered {m} of {n}"** — the partial line counts from the payload's verification block, never guessed; `n` is the slot's field set (character slot = 6, honest count).
11. **Off state** — `reference_contact_choice == "declined"` renders the §7.4 Off block with referee contact chips and NO re-ask affordance; pre-v1 (choice NULL, no rows, no attestation) hides the card.

## OUTPUT CONTRACT (mandatory)

Write ONLY a single valid JSON array to your assigned output file (path given in your lens brief). No prose, no markdown fencing, no preamble. `[]` is valid and expected when you find nothing real. Do not invent findings to fill a quota.
