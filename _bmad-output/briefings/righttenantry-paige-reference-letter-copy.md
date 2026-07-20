# Briefing: righttenantry-paige-reference-letter-copy

Supporting task for job `righttenantry-guide-landlord-reference-letter` (GitHub issue solarity-services/RightTenantry **#530**). You are the **copywriter**; a separate dev agent builds the page from your deck.

- **Worktree (your cwd):** /Users/moses/.herdr/worktrees/RightTenantry/guide-landlord-reference-letter
- **Branch:** `guide-landlord-reference-letter` (do NOT commit, do NOT push, do NOT open a PR — artifact only)
- **Deliverable:** `_bmad-output/planning-artifacts/landlord-reference-letter-copy-deck-2026-07-20.md` (write it in this worktree)

## Persona / skill

Invoke the **bmad-agent-tech-writer** skill (Paige). BMad skills are installed globally (`~/.pi/agent/skills/`) and `_bmad` project config is present in this worktree, so activation works as documented. Stay in the Paige persona for the task; the deliverable is a copy deck, not chat.

## What you are writing

A **copy-complete deck** for a new SSR guide page `/guides/landlord-reference-letter`, so complete that the dev agent does not have to invent a single sentence. Model the format on the existing deck `_bmad-output/planning-artifacts/tenancy-agreement-template-copy-deck-2026-06-13.md` (and skim `guide-rental-income-tax-copy-deck-2026-06-13.md`).

## Mandatory reading before writing (all in this worktree)

1. `_bmad-output/implementation-artifacts/spec-brand-voice-copy.md` — the brand voice spec. Follow it exactly.
2. `server/src/content/tenancy_agreement_template_view.gleam` — the Tier-1 page pattern your copy must slot into: meta title/description, hero, body sections, `faqs()` Q&A pairs, signup CTA. Note how much copy each slot carries.
3. `server/src/content/tenant_vetting_checklist_view.gleam` — the interlink target; match its tone.

## The assignment (from issue #530)

**Keyword evidence (Keyword Planner IE, 2026-07-18):** "landlord reference letter" 590/mo (x13 close variants: letter of recommendation, referral letter, etc.); template/sample variants 140/mo x12; "reference for a landlord" / "landlord recommendation" 170/mo x2 → ~9,000/mo combined cluster, MEDIUM competition on the head term. Same template playbook as /guides/tenancy-agreement-template.

**Angle (all mandatory):**
- Dual intent served honestly: tenants asking for a reference, landlords writing one.
- The RightTenantry bridge is real, not bolted on: what a genuine reference looks like vs a coached one — this maps to the product's reference verification (one of the six analysis checks) and the "the references checked out" pain point.
- Do NOT portray landlords as naive: Irish landlords do ask for references; the credible gap is verification (paperwork can look fine and still not add up).
- "Analyse" not "score"; € symbol; no exclamation marks; no em dashes; (c) 2026 RightTenantry.
- YMYL claim discipline: sourced, dated, no invented legal claims. Flag anything load-bearing for legal review in a dedicated deck section.

**Decisions already made by the user (do not re-litigate):**
- Template delivery: **inline copy-paste sample letter rendered on the page itself** — no hosted PDF/DOCX, no gated download card. The deck must contain the complete, copy-paste-ready sample landlord reference letter.
- OG image: handled by the dev agent separately — out of your scope.

**Interlinks:** to /guides/tenant-vetting-checklist and the product signup CTA (signup URL will be `/signup?utm_source=content&utm_medium=landlord-reference-letter`).

## Deck contents required

- Meta title + meta description (targeting "landlord reference letter" + template/sample variants)
- H1 + hero copy
- Section-by-section body copy (dual-intent structure: for tenants requesting, for landlords writing)
- The complete sample landlord reference letter (inline, copy-paste-ready)
- "Genuine vs coached reference" section copy (the verification angle — the honest RT bridge)
- FAQ Q&A pairs (these become the page's FAQ schema), covering the lookup/template intents above
- Signup CTA copy + the tenant-vetting-checklist interlink copy
- A "claims flagged for legal review" section listing any load-bearing claims with sources/dates

## When done

Run: `herdr notification show "righttenantry-paige-reference-letter-copy" --body "<one-line status>"`
End your final message with: deck path, section list, and any claims you flagged for legal review.
