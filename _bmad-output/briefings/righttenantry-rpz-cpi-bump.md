# Briefing: righttenantry-rpz-cpi-bump (GitHub issue #526)

**Standing orders:** read `/Users/moses/code/docs/orchestration-playbook.md`
section "Minion standing orders" first — they apply in full (ledger
self-report on every transition, env files read-only, badge-out panes,
never merge the PR).

## Task

From GitHub issue solarity-services/RightTenantry#526 (verbatim):

> /tools/rpz-calculator is still showing CPI for **May 2026**, and a newer
> CSO monthly release should be available by now. The page promises its
> figures are checked against official sources, so it needs a bump.
>
> One edit:
>
> 1. Latest annual CPI rate: https://www.cso.ie/en/statistics/prices/consumerpriceindex/
> 2. Quick glance at the RTB rules page for changes: https://www.rtb.ie/renting/setting-and-reviewing-private-rents-from-1-march-2026/
> 3. Update the single `cpi` constant in `server/src/content/rpz.gleam` — rate in basis points (3.7% = 370), reference month, and checked-on date.
> 4. `make format && make test && make build`, then PR as usual.
>
> If CPI has dropped below 2%, no code change is needed beyond the constant — the cap logic and the page copy switch to the CPI-binding branch automatically.
>
> Opened automatically by `.github/workflows/cpi-freshness.yml`.

Orchestration addenda:

- Use web_fetch on the CSO page to get the latest annual CPI rate and its
  reference month. If the CSO page is ambiguous, cross-check with the CSO
  CPI release PDF / a news summary, and cite what you used in the PR.
- If the latest published month is still May 2026 (no newer release), the
  correct outcome may be **only refreshing the checked-on date** — or
  closing as no-op. If so, say that in your final message instead of
  forcing a diff.
- Note: issue #529 (Dublin Rents Q2 post) also touches this constant but
  is NOT being dispatched yet — do not worry about it; your PR stands alone.

## Acceptance

- `cpi` const in `server/src/content/rpz.gleam` reflects the latest CSO
  annual CPI (basis points), correct reference month, today's checked-on
  date — or a clear no-op explanation.
- `make format && make test && make build` all green.
- PR targets `develop`, carries a "Decisions & rationale" section (which
  CSO release you used, RTB page checked + outcome).

## Repo map

- Repo: `/Users/moses/code/RightTenantry` (worktree: this pane's cwd)
- Gleam backend under `server/src`; content/constants in
  `server/src/content/` (`rpz.gleam` is your only expected edit).
- Build/test via `Makefile` at repo root (`make format`, `make test`,
  `make build`).
- Base branch: `develop`; your branch: `rpz-cpi-bump`.

## Env / bootstrap

- `_bmad` copied from the main checkout at dispatch.
- `.env` symlinked from the main checkout (gitignored; treat read-only).
- `.env.example` / `.env.test` are tracked — already in the worktree.

## Verify

`make format && make test && make build` — all must pass before the PR.

## Model policy

Unset — pi default model resolution. Same for any mega-minions (you are
unlikely to need any for this job).

## Skills policy

- Your workflow skill: **bmad-quick-dev**. Follow its step files; per
  standing orders, internal approval checkpoints are pre-approved, but the
  step-01 clarify halt still applies if you have genuine blocking
  questions (you probably won't — the issue is a locked recipe).
- Mega-minions (only if you spawn one): review →
  `bmad-review-adversarial-general` / `bmad-review-edge-case-hunter`.
