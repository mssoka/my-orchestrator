# Briefing: finlit-gdd-amendments-design-session

- **Repo:** kids-finlit-game (`/Users/moses/code/kids-finlit-game`, remote: solarity-services/finlit)
- **Worktree:** this pane's cwd (`gdd-amendments` worktree, branch `gdd-amendments`, base `origin/main`)
- **Skills policy:** workflow = **bmad-quick-dev** (docs amendment; orchestration overrides per standing orders). Self-review: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes.
- **Model policy:** `deepseek-v4-flash` (kimi walled until 08-08T21:57Z).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start.
- **Perkins:** off (docs deliverable, lavish review gates the PR).

## Mission

Amend the GDD with three design decisions from the 2026-08-04/05 design session. These are **human-ruled renegotiations** of previously-locked GDD content (the user explicitly ruled each in conversation with Gru). Cite the ruling date and source in each amendment.

Target file: `_bmad-output/planning-artifacts/gdd-finlit-street-v1-2026-08-01.md` (the locked GDD). Also check `project-context.md` and the architecture doc for any target-audience or tutor references that need aligning.

### Amendment 1: The Owl Tutor (amends OQ3)

**Amends:** the brief's OQ3 ruling ("LLM tutor = child-initiated '?' help button") → **proactive character-driven tutor**.

- **Character:** ONE owl (universal wisdom symbol, cross-age appeal, non-human). Normal proportions (Disney Research: children don't prefer exaggerated baby-features by age). Expressive face — the bond is to personality, not gimmickry.
- **Personality:** warm, slightly dry-humored, genuinely excited when the player succeeds, never condescending. A mentor who CELEBRATES, not a teacher who lectures.
- **Home:** a treehouse/nest that is a building ON THE PLAYER'S STREET. When the owl has a tip, the treehouse lights up / the owl leans out. Part of the player's world.
- **Proactive, not reactive:** pops up at the GDD's ⑤ TEACH BEAT moments (first wage, first buy, first rate hike, first loan, asset-class unlock). Not every tick — only when there's a lesson.
- **Age-bracketed dialogue (one character, adaptive depth):**
  - 8-10: simple, celebratory (*"You earned your first wage!"*)
  - 11-12: cause-and-effect (*"Your rental pays you every tick because you own it."*)
  - 13-15: full terms (*"Your yield is 8%. Here's why diversifying matters."*)
  - 16+/adult: sophisticated (*"Your leveraged return is 12% but your rate-hike exposure doubled."*)
- **Powered by:** LLM for dynamic explanations (server relay per architecture) + scripted beats for milestone moments (guaranteed quality).
- **Research basis:** Disney Research (Carter et al. 2016) — no age-related character-design preferences in children aged 4-10; one well-designed character works across the full range. Clarence Tan (Boddle) — characters are the #1 engagement driver; the question is "how would this mechanic feel if it came from a character instead of a UI element?"

### Amendment 2: Expandable Street Plots (amends the street/economy design)

**Amends:** the spike's `MAX_PLOTS := 4` was arbitrary, not a design decision. The street grows.

- **Progression-gated unlocks:** start with 3-4 plots; unlock more through:
  - Wealth milestones (first $500 earned, first upgrade)
  - Era advances (cash → banking era)
  - Trust levels (Mrs. K, Marcus relationships)
  - Season rank achievements
- **The growth IS the reward:** new plots slide in with animation (juice); the owl celebrates (*"Look at that — your street is growing!"*). The street physically extends.
- **Per-tier economy tuning:** balanced at each stage (4 early → 8 mid → 12+ late). The economy doesn't need to handle infinite inflation at once.
- **Cognitive-load guardrail:** the kid manages a VISIBLE SET at any moment. New plots ARRIVE as celebration moments, not as overwhelming empty space.
- **AdVenture Capitalist doctrine:** "the next goal is always visible on the unlock ladder" — the plot unlocks ARE the ladder.

### Amendment 3: Adult Audience — Path A (amends target-audience scope)

**Amends:** the target-audience framing from "kids 8+" to "kids 8+ with uncapped depth for adults."

- **Nintendo model:** design for the kid (anchor: Noa, 9 — every pixel must react); let the financial depth attract the adult organically. The experience-first fantasy (*"start with nothing, build your street"*) triggers the urge at any age.
- **Do NOT pitch "for everyone 8-80."** Pitch the EXPERIENCE. The capsule art triggers the urge in whoever sees it. The adult who feels it is already in.
- **Age-bracket extension:** the existing system (8-10/11-12/13-15) extends naturally to 16+/adult — one more config row, deeper dialogue, same game.
- **COPPA note:** under-13 cohort keeps the consent flow; 13+ path is frictionless (COPPA doesn't apply). The compliance burden doesn't increase.
- **Steam discovery:** median Steam user is ~28. A "kids only" game has a smaller discovery surface. An experience-first game with uncapped depth reaches the full audience without compromising the kid's experience.

## Review loop (lavish — BEFORE the PR opens)

DOCS deliverable: when amended + self-reviewed, render via the **lavish** skill and post the review URL. Do NOT open the PR until the user's verdict.

## Acceptance

- GDD amended with all three decisions, each citing the ruling date (2026-08-04/05 design session) + research basis where applicable.
- `project-context.md` target-audience line aligned if needed.
- No contradictions with locked GDD content (these are explicit renegotiations, not silent edits).
- Lavish URL delivered.
- After user approval: commit, push, `gh pr create --base main` titled "docs: GDD amendments — owl tutor, expandable plots, adult audience (Path A)". **Never merge.**

## Env/bootstrap

Standard bootstrap (`_bmad` copied, gds module config in-repo).

## Self-report

- `bin/ledger set finlit-gdd-amendments working` at start
- `bin/ledger note finlit-gdd-amendments "lavish review posted: <url>"` when review goes up
- `bin/ledger set finlit-gdd-amendments in-review "PR <url>"` when PR opens (after approval)
- `herdr notification show "finlit-gdd-amendments" --body "<one-line>"` on finish

## Dispatch parameters

- repo: kids-finlit-game
- repo_root: /Users/moses/code/kids-finlit-game
- slug: finlit-gdd-amendments
- base: main
