# Briefing: righttenantry-guide-landlord-reference-letter

GitHub issue: solarity-services/RightTenantry **#530** (priority:high — "biggest prize", ~9,000/mo keyword cluster)

- **Repo:** /Users/moses/code/RightTenantry
- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/guide-landlord-reference-letter
- **Branch:** `guide-landlord-reference-letter` → PR targets **`develop`**
- **Base:** `develop`

## Standing orders

Read `/Users/moses/code/docs/orchestration-playbook.md` section **"Sub-agent standing orders"** and follow it exactly. Use the **bmad-quick-dev** skill; step-01 clarify = HALT and wait for relayed answers; internal approval checkpoints are pre-approved. When blocked or finished: `herdr notification show "righttenantry-guide-landlord-reference-letter" --body "<one-line status>"`. Never merge the PR.

## Task (from issue #530)

New SSR guide in the `content_pages` registry: `/guides/landlord-reference-letter`.

**Why (keyword evidence, Keyword Planner IE, 2026-07-18):** "landlord reference letter" 590/mo (x13 close variants); template/sample variants 140/mo x12; "reference for a landlord" / "landlord recommendation" 170/mo x2 → ~9,000/mo combined, MEDIUM competition. Same template-download playbook as /guides/tenancy-agreement-template (biggest validated cluster).

**Angle (brand rules — all mandatory):**
- Dual intent served honestly: tenants asking for a reference, landlords writing one.
- The RT bridge is real, not bolted on: what a genuine reference looks like vs a coached one — maps to the product's reference verification (one of the six analysis checks) and the "the references checked out" pain point.
- Do NOT portray landlords as naive: Irish landlords do ask for references; the credible gap is verification (paperwork can look fine and still not add up).
- "Analyse" not "score"; € symbol; no exclamation marks; no em dashes; (c) 2026 RightTenantry.
- PostHog + gtag + Pixel + `utm_medium=landlord-reference-letter` per the Tier-1 pattern.

**Interlinks:** to /guides/tenant-vetting-checklist and the product signup CTA (footer CTA keeps `utm_source=content&utm_medium=footer` guard from #416).

**Acceptance:** page live in registry, sitemap, guides nav; FAQ schema if the Tier-1 pages have it (they do — see below); meta title/description targeting "landlord reference letter" + template variants.

## Repo map (content system — verified by orchestrator)

To add a new guide page you must touch all of:

1. **NEW** `server/src/content/landlord_reference_letter_view.gleam` — model it closely on `server/src/content/tenancy_agreement_template_view.gleam` (the Tier-1 template playbook): `view_faq()` / `faqs()` / `faq_item()` structure, signup CTA `href: "/signup?utm_source=content&utm_medium=landlord-reference-letter"`, and JSON-LD via `layout.faq_page_json(faqs())`.
2. `server/src/content/content_pages.gleam` — add a `ContentPage(...)` entry (section: Guides). This one registry auto-surfaces the page in sitemap.xml, the /resources hub, and footer nav.
3. `server/src/content/content_handler.gleam` — add `handle_landlord_reference_letter` (model on `handle_tenancy_agreement_template`, ~line 852).
4. `server/src/router.gleam` — add `http.Get, ["guides", "landlord-reference-letter"]` alongside the other guide routes (~line 814, before the SPA catch-all).
5. `server/src/middleware.gleam` — add `["guides", "landlord-reference-letter"] -> True` to `is_public_path` (~line 289).
6. Tests: `server/test/content/content_test.gleam` has a registry/sitemap drift test (`sitemap_lists_every_registry_page_test`) that must pass; add page-level tests per quick-dev.

## Env / bootstrap

- `.env` is symlinked from the main checkout — treat as read-only (see standing orders).
- `_bmad` project config was copied into the worktree.

## Verify

`make test-server` from the repo root (unit tests, no Docker needed). `make test` also runs shared+client.

## Model policy

Unset — pi default model resolution. Applies to any sub-agents you spawn (close them when done).
