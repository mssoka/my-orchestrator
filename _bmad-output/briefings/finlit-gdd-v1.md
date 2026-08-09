# Briefing: finlit-gdd-v1

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: solarity-services/finlit)
- **Worktree:** this pane's cwd (`finlit-gdd-v1` worktree, branch `finlit-gdd-v1`, base `origin/main`)
- **Skills policy:** workflow = **gds-gdd** (create intent — follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before lavish: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter** (docs lens: consistency, coverage, contradictions), max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** off (docs deliverable).

## Mission

Produce the **Game Design Document for FinLit Street** (working title — the game names itself later; do NOT pick a final title). The design intent is LOCKED; your job is to grow it into a complete GDD, not to re-litigate it.

**Primary sources (read in full, in this order):**

1. `_bmad-output/planning-artifacts/briefs/brief-FinLit-2026-07-31/brief.md` — the final game brief (concept, pillars, players, market).
2. `_bmad-output/planning-artifacts/briefs/brief-FinLit-2026-07-31/addendum.md` — the locked MoSCoW board, persona detail, market evidence, rejected alternatives, decision audit trail. **The Must board and locked decisions govern — do not reopen them.**
3. `_bmad-output/implementation-artifacts/spec-quick-prototype-finlit-street.md` — the prototype slice spec (what's already built in `game/` — the GDD must be consistent with the slice's proven decisions: ownership formula, minute-one, two-door doctrine).
4. `_bmad-output/brainstorming/brainstorm-kids-financial-literacy-game-2026-07-27/` — intent, memlog, research ×2, synthesis (background evidence; the brief supersedes on any conflict).

## Requirements

1. Follow `gds-gdd`'s full structure: pillars → core loop → mechanics (earn/save/buy/grow/show; two doors to capital; trust-meter web; four asset classes; supply chains; anonymous order-book market) → progression (eras, seasons, New Life prestige, L1–L4 reset model) → content scope for v1 → UX/flow overview → art direction (placeholder-now, direction-later) → audio → economy/tuning model (the 60s tick, pricing curves, disaster/rate-hike cards) → COPPA/compliance constraints as design requirements (age signal, no social surface, provably-fair seeded decks, AI-tutor guardrails).
2. **Economy model gets real numbers** — starter wages, asset price/income curves per level, tick math, disaster frequency/severity bands. The prototype's `game/data/` files and the tutor-economy-fix PR (#5, two-door doctrine rebalance) are the current tuning baseline — read them; the GDD's numbers must be consistent with or explicitly amend them.
3. Age-bracket adaptation (8–10 / 11–12 / 13–15) as a design system, not an afterthought.
4. Every design element traceable: locked decision (cite brief/addendum) vs new design proposal (mark clearly as NEW — the user reviews these hardest).
5. Deliverable: `_bmad-output/planning-artifacts/gdd-finlit-street-v1-<date>.md` in the worktree.

## Review loop (lavish — BEFORE the PR opens)

This is a DOCS deliverable: when the GDD is drafted and self-reviewed, render it via the **lavish** skill (`lavish-axi`) and post the review URL in your final message — the user annotates in the browser. Do NOT open the PR until the user's verdict comes back through Gru/Silas. Clarify questions go through lavish too when practical.

## Acceptance

- GDD complete per `gds-gdd`'s structure; locked-vs-NEW traceability throughout; economy numbers internally consistent; lavish review URL delivered; zero unresolved self-review findings (or each explicitly deferred with reason).
- After user approval: commit on `finlit-gdd-v1`, push, `gh pr create --base main` titled "docs: FinLit Street GDD v1" with a summary of NEW proposals vs locked decisions. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied — the gds module config is already in this repo's `_bmad/gds`). Godot project lives in `game/`; you do NOT need to run it, but `game/data/` + `game/scripts/` are ground truth for the tuning baseline.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set finlit-gdd-v1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note finlit-gdd-v1 "lavish review posted: <url>"` when the review goes up (status stays working — the PR waits on the user)
- `/Users/moses/code/bin/ledger set finlit-gdd-v1 in-review "PR <url>"` when the PR opens (after approval), and `/Users/moses/code/bin/ledger pr finlit-gdd-v1 <url>`
- On blocked/finished: `herdr notification show "finlit-gdd-v1" --body "<one-line>"`
- Final message: summary, GDD path, lavish URL, NEW-proposals list, open questions.

## Dispatch parameters

- repo: kids-finlit-game
- repo_root: /Users/moses/code/kids-finlit-game
- slug: finlit-gdd-v1
- base: main
