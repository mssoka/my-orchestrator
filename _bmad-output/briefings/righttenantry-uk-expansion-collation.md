# Briefing: righttenantry-uk-expansion-collation

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (the `uk-expansion-domain-research` worktree —
  you will switch it to a fresh branch below)
- **GitHub issue:** #534 — reference with `Refs #534`, do NOT close
- **Skills policy:** workflow = **bmad-quick-dev** (one-shot route; clarify
  pre-answered below, internal checkpoints pre-approved). Any review pass
  uses **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**
  (max 10 mega-minion panes, badge out every one).

## Mission

Collate the two sibling #534 reports into ONE self-contained interactive
HTML document and open the single PR. The two sources:

1. **Evidence report** (your own work):
   `_bmad-output/planning-artifacts/research/domain-uk-rental-portal-applicant-intake-gtm-research-2026-07-24.md`
   (+ raw thread evidence in `research/uk-threads/`)
2. **Decision analysis** (sibling minion):
   `_bmad-output/planning-artifacts/research/problem-solving-uk-expansion-534-2026-07-23.md`
   (on branch `origin/uk-expansion-problem-solving`, commit `edb9521`)

## Step 1 — branch surgery (exact commands)

```bash
git fetch origin develop uk-expansion-problem-solving
git switch -c uk-expansion-gtm-docs origin/develop
git checkout origin/uk-expansion-domain-research -- \
  _bmad-output/planning-artifacts/research/domain-uk-rental-portal-applicant-intake-gtm-research-2026-07-24.md \
  _bmad-output/planning-artifacts/research/uk-threads/
git checkout origin/uk-expansion-problem-solving -- \
  _bmad-output/planning-artifacts/research/problem-solving-uk-expansion-534-2026-07-23.md
git commit -m "Bring sibling #534 reports onto collation branch (Refs #534)"
```

## Step 2 — the collision (the point of this exercise)

Before generating HTML, produce the **assumption verdict table**: take the
analysis's 15-item numbered assumption ledger and test EVERY assumption
against the evidence report (+ `uk-threads/` raw evidence where needed).
Verdict per assumption: CONFIRMED / REFUTED / UNRESOLVED, each with an
evidence anchor (heading in the evidence report). Rules:

- **Never silently patch the analysis.** Where evidence contradicts it,
  show both and state the contradiction — the HTML reader must see it.
- Plug the confirmed facts into the analysis's conditional decision rule
  and state the resolution (which branch fires). That resolved rule is the
  document's headline recommendation.
- Flag any assumption whose verdict changes the leading option's ranking —
  prominently, in your final message.

## Step 3 — the HTML document

Path: `_bmad-output/planning-artifacts/research/uk-expansion-534-gtm-collated-2026-07-24.html`

A proven generator + verifier from job 535 exists at `/tmp/heist535/`
(`build_html.py`, `verify_html.py` — inspect first, adapt, copy your
versions into `/tmp/uk534/`; do NOT depend on `/tmp` files at runtime and
do not commit them). The output standard it encodes, which you must match:

- **Single self-contained .html** — all CSS/JS inlined, zero external
  assets (no CDNs/fonts/`@font-face`), works offline from disk.
- **Light-first paint** (dark toggle kept, saved-preference respected),
  quality **system font stacks only**, ~72ch measure, tuned hierarchy.
- **Colour system:** green = recommendation/verdict, red = hard
  requirements/compliance blockers, amber = open questions/contestable,
  blue = economics/pricing facts; per-section accents; key-stats band.
- **Interactivity:** sidebar TOC with scroll-spy, collapsible sections,
  client-side search with highlighting, anchor deep-links, back-to-top,
  sticky header, print stylesheet.
- **Structure:** ① resolved-recommendation callout + key stats ②
  assumption verdict table (linking into evidence) ③ decision analysis
  sections ④ five evidence-thread sections ⑤ union References section with
  in-text `[n]` jump markers.
- **Content fidelity:** every finding, citation, table, and the full
  assumption ledger from both sources must appear. Reorganize for
  navigation; drop nothing; no editorializing beyond the verdict table and
  the resolved decision rule.

## Step 4 — verify, then PR

- Re-run your adapted verifier: both sources fully incorporated (headings,
  fragments, table rows, URLs), zero external assets, anchors resolve, JS
  syntax-clean. Evidence in final message.
- Commit everything on `uk-expansion-gtm-docs`, `git push -u origin
  uk-expansion-gtm-docs`, then `gh pr create --base develop` with a
  **"Decisions & rationale"** section + `Refs #534`. **Never merge.**
- Standing orders per the playbook (env read-only, no secrets,
  notification on finish). Self-report:
  `/Users/moses/code/bin/ledger set righttenantry-uk-expansion-collation <status> "<note>"`
  (`working` at start, `in-review` when PR opens).
- Record the PR: `/Users/moses/code/bin/ledger pr righttenantry-uk-expansion-collation <url>`
- Final message: summary, files changed, PR URL, verifier evidence, and
  the assumption-verdict headline counts (X confirmed / Y refuted / Z
  unresolved) + any ranking change.
