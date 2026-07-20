# Briefing: righttenantry-rtb-registration-faq

GitHub issue: solarity-services/RightTenantry **#533** (priority:medium — cheap FAQ expansion, 880/mo lookup intent)

- **Repo:** /Users/moses/code/RightTenantry
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/rtb-registration-faq
- **Branch:** `rtb-registration-faq` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Sub-agent standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. When blocked or finished: `herdr notification show "righttenantry-rtb-registration-faq" --body "<one-line status>"`. Never merge the PR.

## Task (from issue #533)

Add an FAQ section to the **existing** `/guides/rtb-registration` guide covering how to find an RTB registered number and how to check whether a tenancy/property is registered. **No new page** — no new registry entry.

**Why (keyword evidence, Keyword Planner IE, 2026-07-18):** "rtb registration" 1,600/mo (head term, already targeted, LOW competition); "rtb registered number" 880/mo; "rtb registered properties" 140/mo. The 880/mo registered-number variant is a distinct intent (lookup, not how-to) the current guide doesn't answer.

**Scope:**
- FAQ entries: where to find your registered number, how a tenant/landlord checks a registration, what happens if unregistered (brief, link to RTB).
- Verify against RTB.ie; YMYL claim discipline (sourced, dated).
- This guide is SEO-only (FirstTime-RTB ads paused 2026-06-15) — purely organic play.

**Acceptance:** FAQ section live with FAQ schema; no new page; tracking unchanged.

## Repo map (verified by orchestrator)

All edits are in **one file**: `server/src/content/rtb_registration_view.gleam` (268 lines).

- The guide already has the FAQ machinery: `view_faq()` (~line 135), `faqs() -> List(#(String, String))` (~line 148), and JSON-LD via `layout.faq_page_json(faqs())` (~line 245, combined with a `howto_schema()`). Adding entries to `faqs()` automatically adds them to the FAQ schema — no separate schema wiring needed.
- Existing signup CTA at ~line 174 (`utm_medium=rtb-registration`) — leave unchanged.
- If the new FAQ entries warrant it, ensure `view_faq()` renders them (check how it maps `faqs()` — it likely renders all entries already).
- Tests: `server/test/content/content_test.gleam` — add/update tests covering the new FAQ entries per quick-dev.

## Brand rules (mandatory)

"Analyse" not "score"; € symbol; no exclamation marks; no em dashes; (c) 2026 RightTenantry.

## Env / bootstrap

- `.env` is symlinked from the main checkout — treat as read-only.
- `_bmad` project config was copied into the worktree.

## Verify

`make test-server` from the repo root (unit tests, no Docker needed).

## Model policy

Unset — pi default model resolution. Applies to any sub-agents you spawn (close them when done).
