# Briefing: righttenantry-growth-route-analysis

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd, branch `growth-route-analysis`
- **Base:** `develop` · **No PR** (standing-orders override — a collation job opens the single PR later)
- **Type:** structured decision analysis. Deliverable: markdown analysis on the branch.

## Mission

Run **bmad-cis-problem-solving** as your operating workflow on the growth
decision below.

**The challenge (pre-answered — do NOT halt to clarify; internal skill
checkpoints pre-approved):**

RightTenantry has **zero paid signups** in Ireland, its only live market
(UK parked per #534). Three candidate growth levers are on the table:

- **Renter's passport** — a reusable verified renter profile
  (renter-side product; candidate CAC reducer + landlord-pull wedge)
- **Landlord listings** — compete with DAFT.ie at the top of the funnel
  (platform-risk hedge + listing-led landlord acquisition)
- **Status quo** — DAFT-dependent intake + current GTM, iterate on
  conversion of the existing funnel

**Decision: which lever(s) improve PAID SIGNUPS in the next 6 months —
and which are strictly later bets?** Constraints: founder-bandwidth
engineering, small Irish market, no implementation commitment yet (~6
month horizon unless evidence says "now").

**Two sibling minions are gathering the cited evidence in parallel**
(renter-passport precedents/mechanics/compliance; DAFT risk + portal
competition). Do NOT duplicate deep web research — reason from this
briefing, the repo's GTM context, and clearly-labelled general knowledge.
**State every assumption explicitly** (numbered ledger) so the collation
pass can test each against the evidence. Name unknowns instead of
resolving them by fiat.

## Required outputs

1. **Reframes (≥2)** — e.g. is the problem "no paid signups", "no
   landlord-side pull", "renter-side top-of-funnel", or "platform
   dependency"? Implications of each.
2. **Options beyond the menu (≥2)** — e.g. passport-as-free-tool SEO play,
   letting-agent partnerships, deepening the DAFT integration rather than
   hedging it, paid-channel conversion push on the existing funnel.
3. **Weighted evaluation matrix** — criteria anchored on the decision
   lens: paid-signup impact ≤6 months, CAC effect, time-to-first-effect,
   engineering cost (inverted), platform-risk delta, strategic option
   value. Scores WITH reasoning.
4. **Pre-mortem** on the leading option.
5. **Conditional decision rule** — "if evidence shows X about passport
   precedents / DAFT risk / portal feasibility, then Y" (the evidence
   lands in the sibling reports).
6. **Numbered assumption ledger** for the collation pass.

## Standing orders (overrides)

- Playbook "Minion standing orders" applies except: **skills policy** =
  bmad-cis-problem-solving (mega-minion review pass:
  bmad-review-adversarial-general / bmad-review-edge-case-hunter; max 10
  panes, badge out all); **no PR** — commit on `growth-route-analysis`,
  `git push -u origin growth-route-analysis`, never merge.
- Env files symlinked from main checkout are read-only; never commit secrets.
- Output path: `_bmad-output/planning-artifacts/research/problem-solving-growth-routes-2026-07-26.md`
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-growth-route-analysis <status> "<note>"`
  (`working` at start; `in-review` when pushed = ready for collation).
- On blocked/finished: `herdr notification show "righttenantry-growth-route-analysis" --body "<one-line>"`

## Close-out

Final message: summary, file path, reframes in one line each, leading
option + decision rule, assumption count.
