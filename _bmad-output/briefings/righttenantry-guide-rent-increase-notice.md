# Briefing: righttenantry-guide-rent-increase-notice

GitHub issue: solarity-services/RightTenantry **#531** (priority:high — "cheapest win", ~330/mo all LOW competition)

- **Repo:** /Users/moses/code/RightTenantry
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/guide-rent-increase-notice
- **Branch:** `guide-rent-increase-notice` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Sub-agent standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. When blocked or finished: `herdr notification show "righttenantry-guide-rent-increase-notice" --body "<one-line status>"`. Never merge the PR.

## Task (from issue #531)

New SSR guide: `/guides/rent-increase-notice` (working title "How to raise the rent legally: cap, notice and timing").

**Why (keyword evidence, Keyword Planner IE, 2026-07-18):** "rental increase ireland" 260/mo LOW; "rent increase notice ireland" 40/mo; "rent review ireland" 20/mo; "how much rent can i charge" 10/mo → ~330/mo, all LOW competition. The RPZ calculator computes the number but doesn't own the informational intent (when, how often, what notice); this guide captures it and interlinks.

**Scope:**
- Cap = lower of CPI or 2% per annum pro-rated — **derive from `content/rpz`, never hardcode** (same rule as the rent posts).
- Review only once per 12 months; written notice requirement; market reset on turnover / past 72 months.
- **Verify every rule against `server/src/content/rpz.gleam` + tests** (legal-reviewed source of truth) and RTB guidance. Per the rent-cap claim correction of 2026-06-22: never flatten the pro-rata rule into a single number.
- **Also in scope:** while interlinking, verify the /tools/rpz-calculator page copy (`server/src/content/rpz_calculator_view.gleam`) reflects the post-March-2026 nationwide cap (old RPZ-area framing is dead; "rent pressure zone" still gets 720/mo and searchers now get a different answer). Fix stale framing if found.

**Acceptance:** page live in registry, sitemap, guides nav; tracking + `utm_medium=rent-increase-notice` per Tier-1 pattern; interlinks to /tools/rpz-calculator and the /resources/dublin-rents-q1-2026 series.

## Brand rules (mandatory)

"Analyse" not "score"; € symbol; no exclamation marks; no em dashes; (c) 2026 RightTenantry; PostHog + gtag + Pixel per the Tier-1 pattern; YMYL claim discipline (sourced, dated).

## Repo map (content system — verified by orchestrator)

To add a new guide page you must touch all of:

1. **NEW** `server/src/content/rent_increase_notice_view.gleam` — model on `server/src/content/tenancy_agreement_template_view.gleam` (Tier-1 pattern): `view_faq()` / `faqs()` / `faq_item()`, signup CTA `href: "/signup?utm_source=content&utm_medium=rent-increase-notice"`, JSON-LD via `layout.faq_page_json(faqs())`.
2. `server/src/content/content_pages.gleam` — add a `ContentPage(...)` entry (section: Guides); auto-surfaces in sitemap.xml, /resources hub, footer nav.
3. `server/src/content/content_handler.gleam` — add `handle_rent_increase_notice` (model on `handle_tenancy_agreement_template`, ~line 852).
4. `server/src/router.gleam` — add `http.Get, ["guides", "rent-increase-notice"]` (~line 814, before SPA catch-all).
5. `server/src/middleware.gleam` — add `["guides", "rent-increase-notice"] -> True` to `is_public_path` (~line 289).
6. `server/src/content/rpz.gleam` — the cap derivation source (read-only for this job; derive, don't hardcode).
7. Tests: `server/test/content/content_test.gleam` has a registry/sitemap drift test that must pass; add page-level tests per quick-dev.

## Env / bootstrap

- `.env` is symlinked from the main checkout — treat as read-only.
- `_bmad` project config was copied into the worktree.

## Verify

`make test-server` from the repo root (unit tests, no Docker needed).

## Model policy

Unset — pi default model resolution. Applies to any sub-agents you spawn (close them when done).
