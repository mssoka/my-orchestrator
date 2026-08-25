# SHARED CONTEXT — Perkins r1 lenses (righttenantry-refcheck-rc4-2)

You are one lens in a parallel code-review wave. Read-only access to the repository. Verify every claim against the actual codebase — no claim is taken at face value.

## Round & scope

- Round 1 of 3. PR #605 → `develop`. Reviewed sha `9d66ce9240a8159d06f7250acfafa9b25cbe3110` (short `9d66ce9`).
- **Scope:** Epic RC4 Story 2 — the landlord Reference Panel (Status & Summary). The CLIENT renders the RC4.1 `reference_calls[]` contract: all 12 lifecycle states (UX §4.2/§7.4 copy verbatim), the completed-summary pull-quote + key-facts table, "Worth knowing" signals, the §9.5 disclaimer, §13 pill colours (never red), the §7.8 explainer, full a11y contract. Plus an expand-only contract addition (`form_opened_at`, `submitted_at`) with back-compat decoders.
- 14 files, ~+2892/−5. Full PR diff at `diff_file` (chunked into c1/c2 for size). Review EXACTLY those bytes; the worktree is at the same sha for verification.
- base = `develop` (RC1–RC4.1 merged — do NOT re-open their findings; carry-forward only).

## Inputs (absolute paths)

- `diff_file` chunk 1 (spec + all client files): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/diff.c1.patch`
- `diff_file` chunk 2 (server + shared): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/diff.c2.patch`
- `worktree`: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r1` (detached at `9d66ce9`; verification reads happen HERE)
- Round briefing (lens-guards + standing orders): `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc4-2-r1.md`
- Job briefing: `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-2.md`
- Story RC4.2 AC (epics file, Story RC4.2 at line ~629): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r1/_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`
- UX spec (authoritative copy — §4.2 lifecycle labels ~line 64, §7.1–7.8 panel ~324–532, §9.3/§9.5 legal flags ~590–610, §10.3 copy deck ~643, §12 a11y ~677, §13 design-system ~691): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r1/_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`
- Architecture (RC4.1 contract — §8.1 payload ~974, §8.2 hooks ~996, §9.5 disclaimer ~1075): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r1/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`

## ⚠️ Lens-guards — the load-bearing checks of THIS round (verify, don't assume)

1. **🚨 UX COPY VERBATIM — the load-bearing invariant.** All 12 lifecycle states render the UX spec's §4.2/§7.4 copy VERBATIM. **RT CI ban: NO em-dashes in user-facing copy** — flag any deviation (a missing state, reworded copy, or an em-dash in shipped strings = a real defect). NOTE: the UX spec's own copy contains em-dashes in some §7.4 strings (e.g. "Invitation, 2 reminders, and an applicant nudge over 6 days — no reply"); where the spec itself ships an em-dash, verbatim wins — but an em-dash ADDED by the implementer where the spec has none, or in implementer-authored strings not in the spec (e.g. the unmoderated-flag sentence, timeline labels, "More actions for" label), is a defect. Check `client/src/copy.gleam` lines ~514-870 against §4.2/§7.4/§7.5/§7.8/§10.3 byte by byte.
2. **🚨 PILL COLOURS — NEVER RED (§13).** Teal (received), slate (waiting/queued/declined/objected/skipped), navy (reminder/opened/invitation), amber (needs-attention: partial/awaiting-correction/unreachable/failed). A red pill anywhere = a blocker (test-pinned; a neutralization must go red).
3. **NEVER GUESS.** The key-facts table renders "Not answered" where the payload has no answer — NEVER a guessed value. A fabricated value, or a derived value presented as a fact (the wireframe's "As stated" Period) = a real defect. The Period deliberately shows the confirmed dates (from/to) instead of "As stated" (not client-side derivable — documented) — do NOT flag that; DO flag any invented date or fabricated value.
4. **"WORTH KNOWING" ONLY WHEN PRESENT.** Signals render only when the payload carries them (≤ threshold checks against the stripped `fraud_signals` block); notable quotes only when `ai_summary.notable_quotes` exists (v1 deterministic summaries never emit them — RC5.1 will). Do NOT flag "quotes missing" — that's the design. DO flag a signal block rendered without payload signals.
5. **OVERFLOW BUTTON DELIBERATELY NOT WIRED (guard!).** The ⋯ overflow button renders with its testid but is deliberately not click-wired — RC4.3 owns the actions (no dead-menu placeholder items). Do NOT flag "dead button" — a click-wired menu with placeholder items WOULD be a defect.
6. **EXPAND-ONLY CONTRACT (back-compat).** `form_opened_at` + `submitted_at` are additive on `ReferenceCallDetail`; the decoders are back-compat (old payloads still decode — absent-key default None) and the RC4.1 §4.2 strip assertions (escaped-marker guard, jsonb_typeof guards, internal-field absence) are untouched. A breaking change (old payloads fail to decode, strip assertions weakened, wire keys renamed) = a blocker.
7. **HOOKS/DISCLAIMER INTEGRITY (from RC4.1 — the panel must not re-derive).** The panel renders the server-computed hooks + `display_disclaimer`; it must NOT re-derive state rules client-side (one-stable-contract AR-RC13). A client-side re-derivation of hook/status rules = a blocker. (Display mapping of the server's status enum to §4.2 labels is fine; re-implementing hook logic is not.)
8. **a11y CONTRACT + AC TESTIDS.** Card `role="region"` + `aria-label="Reference checks"`; rows are buttons with `aria-expanded`/`aria-controls`; status never colour-only; testids `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}` all present on the right elements. A missing testid on a stated AC element, or a keyboard/focus trap = a real defect.
9. **§9.5 DISCLAIMER VERBATIM + confidence line** on written-channel results (server-rendered `display_disclaimer` rendered as-is; "Confidence: {level} · AI-generated summary — verify before relying on it."); minimal terminals carry none.
10. **"answered {m} of {n}"** — the partial line counts from the payload's verification block, never guessed; `n` is the slot's field set.
11. **Off state** — `reference_contact_choice == "declined"` renders the §7.4 Off block with referee contact chips and NO re-ask affordance; pre-v1 (choice NULL, no rows, no attestation) hides the card.

## OUTPUT CONTRACT (mandatory)

Write ONLY a single valid JSON array to your assigned output file (path given in your lens brief). No prose, no markdown fencing, no preamble. `[]` is valid and expected when you find nothing real. Do not invent findings to fill a quota.

Each element must match this schema exactly:
```json
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. If you cannot quote the lines, you have not verified it — drop the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```

ACCURACY MANDATE: every finding will be independently re-verified against the worktree before reaching the report. Findings whose `evidence` cannot be located, or whose claims contradict the actual code, are DISCARDED silently. Open the file. Read the lines. Quote them verbatim. Hedging ("might", "could") = you have not verified it → drop it. Accuracy > volume. Prefer fewer, well-grounded findings over many speculative ones.
