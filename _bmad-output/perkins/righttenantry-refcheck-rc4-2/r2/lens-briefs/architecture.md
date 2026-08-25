# LENS: architecture (source tag: `architecture`) — Perkins r2 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Architectural fit review. Given the diff and the surrounding codebase:

- **AR-RC13 / one-stable-contract — r1 B1 fix audit (verify first, don't re-open).** The panel must render from the server payload (`reference_calls[]`, `attestation_on_file`, `reference_contact_choice`, `display_disclaimer`, hooks) and NEVER re-derive state rules client-side. r1 B1: the panel re-implemented terminality (`is_terminal`) and diverged from the server's terminal set (omitted Completed). The claimed fix: the all-terminal sub-line now derives from the payload hooks (`list.all(calls, fn(c) { not c.hooks.can_record_manual })`). VERIFY: (a) no client-side `is_terminal`/terminal-set re-implementation remains anywhere in the panel; (b) the sub-line uses the hooks; (c) the old `is_terminal` function is gone (not dead code). A residual re-derivation of hook/status rules = a blocker. Display mapping of status → §4.2 label is fine.
- **Expand-only contract discipline.** `form_opened_at` + `submitted_at` additive on `ReferenceCallDetail`: type + encoder + back-compat decoder in shared, SQL COALESCE select, handler mapping. Verify: wire keys snake_case (AR21), old payloads still decode (absent-key default), RC4.1 strip assertions untouched, no destructive migration. Do NOT flag "column exists since rc2-1, no migration" — that's the design.
- **Module organization.** `client/src/components/reference_panel.gleam` — the r1 note flagged 1263 lines (3× the <400 target). Did the rework split it (per the note's recommendation) or leave it? Note-level only either way — but flag if it GREW.
- **State management.** `refcheck_expanded` Set + `refcheck_auto_expanded` Set + explainer state in the central model — consistent with existing patterns (`documents_expanded`, `sweep_nudge`)? Reset discipline on route change? If the W6 localStorage persistence landed: hydration point, write-back point, and reset ordering must not fight each other.
- **Keyed lists.** `keyed.ul` with stable ids — verify dynamic lists use keys (the r1 note flagged the mini-timeline as unkeyed — check whether the rework keyed it).
- **Display-only scope.** No server mutations, no API calls from the panel — verify none crept in (RC4.3 owns actions).
- **Future change cost.** Will RC4.3 (actions) and RC4.4 (attempt log export) fit cleanly onto this panel, or does the structure block them?

For each finding, quote the exact lines. Verify against the worktree.
