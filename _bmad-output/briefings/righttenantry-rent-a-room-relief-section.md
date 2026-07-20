# Briefing: righttenantry-rent-a-room-relief-section

GitHub issue: solarity-services/RightTenantry **#532** (priority:low — ~2,170/mo, weakest product bridge)

- **Repo:** /Users/moses/code/RightTenantry
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/rent-a-room-relief-section
- **Branch:** `rent-a-room-relief-section` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Sub-agent standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. When blocked or finished: `herdr notification show "righttenantry-rent-a-room-relief-section" --body "<one-line status>"`. Never merge the PR.

## Task (from issue #532)

Add a rent-a-room relief section (+ FAQ entries) to the **existing** `/guides/rental-income-tax` guide. **Not a new page** — no new registry entry, same path.

**Why (keyword evidence, Keyword Planner IE, 2026-07-18):** "rent a room scheme ireland" 1,000/mo x2 variants; "rent a room relief ireland" 170/mo → ~2,170/mo combined, LOW competition. The tax guide is the natural home; a standalone page would split authority.

**Scope / honesty notes:**
- Rent-a-room relief: tax-free threshold (**verify the current figure against Revenue.ie** — historically €14,000/yr), owner-occupier condition, how it interacts with rental income reporting.
- Be honest that a room in your own home is usually a **licence, not an RTB tenancy** — different rules. Do NOT over-bridge to RightTenantry here (weak product fit per the free-tool rule); the section earns traffic and trust, the tax guide's existing CTAs do the rest.
- YMYL claim discipline: sourced, dated.

**Acceptance:** section live with FAQ schema entries; tracking unchanged; no new registry entry.

## Repo map (verified by orchestrator)

All edits are in **one file**: `server/src/content/rental_income_tax_view.gleam` (1086 lines).

- The guide already has the FAQ machinery: `view_faq()` (~line 877), `faqs() -> List(#(String, String))` (~line 893), and JSON-LD via `layout.faq_page_json(faqs())` (~line 1060, combined with a `webapp_schema()`). Adding FAQ entries to `faqs()` automatically adds them to the FAQ schema.
- Existing signup CTA at ~line 976 (`utm_medium=rental-income-tax`) — leave unchanged.
- Match the existing section/copy style of the page. Add the new section where it fits the page's narrative flow (reliefs/deductions area).
- Tests: `server/test/content/content_test.gleam` — add/update tests covering the new section per quick-dev.

## Brand rules (mandatory)

"Analyse" not "score"; € symbol; no exclamation marks; no em dashes; (c) 2026 RightTenantry.

## Env / bootstrap

- `.env` is symlinked from the main checkout — treat as read-only.
- `_bmad` project config was copied into the worktree.

## Verify

`make test-server` from the repo root (unit tests, no Docker needed).

## Model policy

Unset — pi default model resolution. Applies to any sub-agents you spawn (close them when done).
