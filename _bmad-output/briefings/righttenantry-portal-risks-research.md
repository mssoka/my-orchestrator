# Briefing: righttenantry-portal-risks-research

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd, branch `portal-risks-research`
- **Base:** `develop` · **No PR** (standing-orders override — a collation job opens the single PR later)
- **Type:** market/competition research. Deliverable: cited markdown report on the branch.

## Mission

Run **bmad-market-research** as your operating workflow on two linked
questions for RightTenantry (Ireland, zero paid signups today):

1. **Platform risk:** RT's entire applicant-intake moat rides on DAFT.ie's
   enquiry-email flow. How exposed are we?
2. **The alternative:** would building a **landlord-listing feature**
   (competing with DAFT at the top of the funnel) be a better approach?

Follow the skill's activation exactly (`_bmad/scripts/resolve_customization.py`,
`_bmad/bmm/config.yaml`, honor its output conventions under
`planning_artifacts`).

**⛔ Search discipline (field notes from #535):** test web search FIRST;
halt `blocked` if unavailable. Steer queries to Irish sources
(`site:daft.ie`, `site:myhome.ie`, Irish business press). Primary sources
wherever possible; no fabricated citations; flag unverifiable claims.

**Decision lens:** does either finding change what improves **paid signups
in the next 6 months**? Speed-to-impact evidence beats long-term strategy.

## Threads

1. **DAFT dependency risk:** who owns DAFT.ie (Distilled group structure,
   stakeholders), its ToS/automation stance, its incentives (could it add
   native application forms/screening and cut RT out? has it moved toward
   landlords directly?), and precedents of platforms killing third-party
   flows (API deprecations, scraping/automation crackdowns — cite cases,
   any industry). Likelihood × impact scenarios for RT's intake breaking.
2. **DAFT's market position:** Irish rental-listings share vs myhome.ie
   and others, landlord/agent pricing, traffic and SEO moat, revenue
   estimates — how strong is the incumbent we'd either depend on or fight?
3. **Landlord-listing feature feasibility:** what competing as a portal
   actually takes — two-sided liquidity (chicken-and-egg), the SEO/domain-
   authority gap vs DAFT, CAC for landlord-listing acquisition, challenger
   precedents and their fates (Irish: myhome.ie, rentola-type aggregators;
   international: OpenRent vs Rightmove as the rare success — WHY it
   worked there, and whether those conditions exist in Ireland).
4. **Synergy analysis:** would listings + RT's screening (+ a possible
   renter passport, being researched by a sibling minion) compound — e.g.
   "screened-applicants-only listings" as differentiation DAFT can't copy
   cheaply?

You may fan out mega-minions (max 10 concurrent, badge out every pane).
Synthesize the single report yourself.

## Standing orders (overrides)

- Playbook "Minion standing orders" applies except: **skills policy** =
  bmad-market-research (mega-minion review pass: bmad-review-adversarial-general /
  bmad-review-edge-case-hunter); clarify pre-answered, internal checkpoints
  pre-approved — halt only for genuine blockers; **no PR** — commit on
  `portal-risks-research`, `git push -u origin portal-risks-research`,
  never merge.
- Env files symlinked from main checkout are read-only; never commit secrets.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-portal-risks-research <status> "<note>"`
  (`working` at start; `in-review` when pushed = ready for collation).
- On blocked/finished: `herdr notification show "righttenantry-portal-risks-research" --body "<one-line>"`

## Close-out

Final message: summary, report file path, per-thread headline findings,
anything flagged unverifiable.
