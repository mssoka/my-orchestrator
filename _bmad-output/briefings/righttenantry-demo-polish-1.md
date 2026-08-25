# Briefing: demo-mode polish round 1 — real-app parity gaps (user field-tested)

**Job id:** righttenantry-demo-polish-1
**Repo:** RightTenantry

## Context

Demo mode (#629) merged and the user manually tested it in dev. Five parity
gaps found — the demo must behave like the REAL app so demo users trust it.
The interactive verify minion (righttenantry-demo-dev-verify, p2B8) remains
available for re-verification after the fixes.

## Fixes (all five required)

1. **Toast placement wrong.** The demo toast appears at the TOP of the page;
   the real app's toasts appear where the real app puts them (verify exact
   position/behavior in the real app and match it — likely bottom stack).
2. **Remind + Follow-up buttons don't change demo state.** In the real app
   they mutate the row state (→ reminded/followed-up visual state). In the
   demo only a toast fires and nothing changes. Make them mutate the DEMO
   state the same way (mock data — state change lives in demo universe).
3. **Vacancy detail: "Compare Top 3" button missing in demo.** The real
   vacancy detail has it; add it to the demo and wire it to demo-universe
   comparison data.
4. **Downloaded report too scanty.** Must contain the same level of detail
   as the real app's report (sections, figures, breakdowns). A thin report
   undersells the product to demo users. Match the real report's structure
   with demo data.
5. **Logo/wordmark click should return to the landing page** (in the demo at
   least) — currently it doesn't navigate.
6. **Purge the `a-grace` residue** (user forensic finding). The string
   `a-grace` survives in 9 spots: `demo_store.gleam` (analysis/docs/
   decisions/report-name branches), `demo_fixtures.gleam` (`app_grace_json`),
   `pdf_prebake.gleam` (`row_grace()` + output filename), and the committed
   PDF `server/priv/static/demo/report-a-grace.pdf`. Visible exposure: the
   address-bar URL `/vacancies/v-maples/applications/a-grace` + the wire
   URL for the report. PURGE: ~9 mechanical renames to a `grainne`-based
   id (e.g. `a-grainne`), delete the old PDF, re-bake via
   `gleam run -m demo/pdf_prebake -- server/priv` (committed PDFs,
   whitelisted in .gitignore). Zero test pins (user grepped the suites).

## Acceptance

- Each of the 6 verified side-by-side against the real app's behavior
  (fix 6: zero `grace` grep hits in demo code, PDF re-baked, URL shows the
  new id).
- No regression on the r1–r5 blocker classes (exit leak, deep-link boot,
  session stash/restore, no-network lint) — the polish must not reopen the
  gauntlet. Full client suite green.
- Demo exit still leaves NO demo state bleeding into real sessions.

## Skills policy

- Workflow: **bmad-quick-dev**.

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash).

## Review

- `pr_review: true` — demo-mode surface carries the same review weight as
  #629 (it sold itself through 5 rounds).

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: demo-polish-1
- base: develop
- pr_review: 1
