# Briefing: righttenantry-renters-passport-research

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd, branch `renters-passport-research`
- **Base:** `develop` · **No PR** (standing-orders override — a collation job opens the single PR later)
- **Type:** evidence research. Deliverable: cited markdown report on the branch.

## Mission

Run **bmad-domain-research** as your operating workflow on the **renter's
passport** growth option for RightTenantry (Option I from the #534 UK
research): a reusable, verified renter profile/application a renter builds
once and shares with any landlord.

Follow the skill's activation exactly (`_bmad/scripts/resolve_customization.py`,
`_bmad/bmm/config.yaml`, honor `planning_artifacts` output location and
`research.template.md` naming).

**⛔ Search discipline (field notes from #535):** test web search with a
trivial query FIRST — if unavailable, halt `blocked` (ledger +
notification), never write an uncited report from memory. The search tool
may default to region=cn — explicitly steer queries (e.g. `site:daft.ie`,
UK/EU sources for passport precedents). Primary sources wherever possible;
no fabricated citations; flag what you cannot verify.

**Decision lens (shapes every thread):** RightTenantry has **zero paid
signups today**, Ireland-only (UK parked per #534). Moses wants to know:
does a renter's passport improve **paid signups in the next 6 months**, or
is it a later bet? Evidence bearing on *speed to paid-signup impact* is the
most valuable kind.

## Threads

1. **Product landscape & precedents:** existing renter-passport / reusable
   verified-profile products (UK: Canopy RentPassport, Movem, Goodlord,
   RentProfile; EU analogues; any Irish attempts). Features, pricing,
   traction, pivots and shutdowns — what killed the dead ones, what scaled
   the live ones.
2. **Mechanics for RT:** concretely how a passport would work inside
   RightTenantry — what gets verified once (identity, references incl. the
   #535 AI-call concept, affordability), who owns the data, how a renter
   shares it with landlords inside AND outside the platform, expiry/refresh.
3. **CAC impact:** the renter-side acquisition loop (passport completion →
   sharing → SEO/virality → more renters), landlord pull (pre-verified
   applicant supply as the landlord wedge), and any published
   CAC/conversion benchmarks for comparable reusable-profile or two-sided
   plays. Label estimates honestly.
4. **Landlord acquisition:** evidence landlords value pre-verified
   applicants enough to engage/pay; precedents of renter-side products
   pulling landlord-side supply.
5. **Compliance (Ireland-first, EU):** GDPR lawful basis/consent/retention
   for reusable referencing data, data-portability angle, DPC guidance,
   RTB considerations, anti-discrimination constraints on what a passport
   may display, ePrivacy on any outreach the model implies.

You may fan out mega-minions (one per thread works; max 10 concurrent,
badge out every pane). Synthesize the single report yourself.

## Standing orders (overrides)

- Playbook "Minion standing orders" applies except: **skills policy** =
  bmad-domain-research (mega-minion review pass: bmad-review-adversarial-general /
  bmad-review-edge-case-hunter); clarify pre-answered above, internal
  checkpoints pre-approved — halt only for genuine blockers; **no PR** —
  commit on `renters-passport-research`, `git push -u origin
  renters-passport-research`, never merge.
- Env files symlinked from main checkout are read-only; never commit secrets.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-renters-passport-research <status> "<note>"`
  (`working` at start; `in-review` when pushed = ready for collation).
- On blocked/finished: `herdr notification show "righttenantry-renters-passport-research" --body "<one-line>"`

## Close-out

Final message: summary, report file path, per-thread headline findings,
anything flagged unverifiable.
