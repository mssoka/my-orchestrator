# righttenantry-dublin-rents-q2-2026 — dispatch briefing

**Source of truth: GitHub issue #529** (read it first — the issue body is the spec: what / why / data sources / acceptance).

**Status: GATE RELEASE** — this row was HELD on the Daft.ie Q2 2026 Rental Report (user decision 2026-07-22, re-confirmed 08-12 FULL HOLD option B: all-in-one-PR). The report **published ~2026-08-23** (verified: journal.ie 23 Aug 2026 coverage — avg 2-bed €2,204, +1.4% Mar→Jun vs Q1's 4.4%; Galway +13%/Cork +12%/Limerick +11%/Waterford +5.5% y/y, Dublin +6.5% y/y, availability 2,400 on 1 Aug). Gate satisfied → bump issue to priority:high (done) + dispatch.

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section 'Minion standing orders' first, then this briefing, then begin. Worktree = your cwd, branch `dublin-rents-q2-2026` from `origin/develop`. Self-report `bin/ledger set righttenantry-dublin-rents-q2-2026 working` at start, `in-review "<pr url>"` at PR open (with `bin/ledger pr righttenantry-dublin-rents-q2-2026 <url>`), and fire `herdr notification show "righttenantry-dublin-rents-q2-2026" --body "..."` at completion.

## Task (from issue #529)

Add `dublin_q2_2026` to the rent-data series registry (`server/src/content/rent_post.gleam`, alongside `dublin_q1_2026`). Sitemap + `/resources` hub surface automatically from the `posts` const.

**Data — VERIFY against the live reports before drafting figures (the registry's own standing rule):**
- Daft.ie Rental Report Q2 2026 (asking rents) — **published ~Aug 23 2026** (see above; pull the actual report figures from reports.daft.ie, don't rely on press numbers alone)
- RTB/ESRI Rent Index, latest available
- Three-figure discipline: asking vs new-registered vs existing-registered, never conflated
- Headline figure table gets its `VERIFY before prod` comment, same as Q1

**Also in scope (SAME PR):** the post derives cap/CPI from `content/rpz`'s `cpi` const (currently 360bps "May 2026" — STALE). CSO June 2026 CPI = **3.4%** (published 9 Jul 2026, verified in the 08-12 gate re-check) → bump all three const fields to 340bps/June in this PR. No duplicate cpi-freshness issue exists (checked).

**Marketing note (no code):** this post is the Q2 press-pitch hook — flag Herald when it ships (in the PR body + your completion message).

## Acceptance

- `/resources/dublin-rents-q2-2026` renders, 404s nothing, appears in sitemap.xml + `/resources` hub newest-first
- All € figures verified against the live reports named in the sources block
- No hardcoded cap percentage in copy (derives from `rpz`)

## Environment

Bootstrap performed by Silas: `_bmad` copied; `.env` + `.env.test` symlinked from the main checkout; `node_modules` symlinked. `make build` should work directly; run `npm ci` only if deps changed. Model: deepseek/deepseek-v4-flash (ops tier).

pr_review=0 (original intake decision — data verification is the issue's own VERIFY-before-prod gate; no Perkins round).
