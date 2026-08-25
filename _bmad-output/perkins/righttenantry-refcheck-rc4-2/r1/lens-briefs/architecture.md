# LENS: architecture (source tag: `architecture`) — Perkins r1 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Architectural fit review. Given the diff and the surrounding codebase:

- **AR-RC13 / one-stable-contract.** The panel must render from the server payload (`reference_calls[]`, `attestation_on_file`, `reference_contact_choice`, `display_disclaimer`, hooks) and NEVER re-derive state rules client-side. Verify: does `client/src/components/reference_panel.gleam` re-implement any server-computed rule (hook computation, terminality for action-gating, disclaimer generation)? Display mapping of status → §4.2 label is fine. Check `is_terminal` in the panel — is it re-deriving a server rule, or just choosing between the three §10.3 sub-lines? The sub-line itself (pre-trigger/in-flight/all-terminal) is a display choice — but check whether terminality should come from hooks.
- **Expand-only contract discipline.** `form_opened_at` + `submitted_at` additive on `ReferenceCallDetail`: type + encoder + back-compat decoder in shared, SQL COALESCE select, handler mapping. Verify: wire keys snake_case (AR21), old payloads still decode (absent-key default), RC4.1 strip assertions untouched, no destructive migration. Do NOT flag "column exists since rc2-1, no migration" — that's the design.
- **Module organization.** New `client/src/components/reference_panel.gleam` (1263 lines) — does it respect the codebase conventions (view module <400 lines target is a guideline, but flag egregious violations), copy in `copy.gleam` (no inline strings — verify), messages SubjectVerbObject naming, model fields documented?
- **Keyed lists.** `keyed.ul` with stable ids — verify dynamic lists use keys (Lustre requirement).
- **State duplication.** `refcheck_expanded` Set(String) + `refcheck_auto_expanded` Set(String) + `refcheck_explainer_open` Bool in the central model — consistent with existing patterns (documents_expanded, sweep_nudge)? Reset discipline on route change (mirror `documents_expanded`)?
- **Display-only scope.** No server mutations, no API calls from the panel — verify none crept in (RC4.3 owns actions).
- **Simpler alternatives.** Any over-engineering: e.g. the mini-timeline batch grouping — is `group_by_at` the right abstraction vs the payload's attempts list?
- **Future change cost.** Will RC4.3 (actions) and RC4.4 (attempt log export) fit cleanly onto this panel, or does the structure block them?

For each finding, quote the exact lines. Verify against the worktree.
