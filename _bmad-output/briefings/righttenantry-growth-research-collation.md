# Briefing: righttenantry-growth-research-collation

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (the `growth-route-analysis` worktree — you
  will switch it to a fresh branch below)
- **Skills policy:** workflow = **bmad-quick-dev** (one-shot; clarify
  pre-answered, internal checkpoints pre-approved). Review pass (if any):
  **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**,
  max 10 panes, badge out all.

## Mission

Collate the three sibling growth-research reports into ONE self-contained
interactive HTML document and open the single PR. Sources:

1. **Decision analysis** (your own work, this worktree):
   `_bmad-output/planning-artifacts/research/problem-solving-growth-routes-2026-07-26.md`
2. **Passport evidence** (branch `origin/renters-passport-research`, `80b604f`):
   `_bmad-output/planning-artifacts/research/domain-renters-passport-research-2026-07-26.md`
   + `research/passport-threads/`
3. **Portal-risk evidence** (branch `origin/portal-risks-research`, `478c530`):
   `_bmad-output/planning-artifacts/research/market-righttenantry-portal-risks-research-2026-07-26.md`

## Step 1 — branch surgery (exact commands)

```bash
git fetch origin develop renters-passport-research portal-risks-research
git switch -c growth-research-docs origin/develop
git checkout origin/growth-route-analysis -- \
  _bmad-output/planning-artifacts/research/problem-solving-growth-routes-2026-07-26.md
git checkout origin/renters-passport-research -- \
  _bmad-output/planning-artifacts/research/domain-renters-passport-research-2026-07-26.md \
  _bmad-output/planning-artifacts/research/passport-threads/
git checkout origin/portal-risks-research -- \
  _bmad-output/planning-artifacts/research/market-righttenantry-portal-risks-research-2026-07-26.md
git commit -m "Bring sibling growth-research reports onto collation branch"
```

## Step 2 — the collision (the point of this exercise)

1. **First action:** resolve U1/U2 (the analysis flagged them as resolvable
   today — resolve them and record what they were + the answers).
2. Test EVERY entry of the analysis's 30-item assumption ledger against the
   two evidence reports (+ `passport-threads/` raw evidence). Verdict per
   assumption: CONFIRMED / REFUTED / UNRESOLVED + evidence anchor.
3. Resolve the analysis's 5-branch conditional decision rule with the
   evidence: state which branch(es) fire and the resulting now/later/parked
   dispositions. Honor its arbitration meta-rule and inconclusive defaults.
4. Rules: **never silently patch the analysis** — show contradictions
   explicitly; flag any verdict that changes an option's ranking
   prominently (in the HTML and in your final message).

## Step 3 — the HTML document

Path: `_bmad-output/planning-artifacts/research/growth-routes-collated-2026-07-26.html`

A proven generator + verifier exists at `/tmp/uk534/` (`build_html.py`,
`verify_html.py` — inspect, adapt, copy your versions into `/tmp/growth/`;
no runtime /tmp dependency, do not commit them). Required standard:

- **Single self-contained .html** — all CSS/JS inlined, zero external
  assets (no CDNs/fonts/`@font-face`), works offline from disk.
- **Light-first paint** (dark toggle kept, saved preference respected),
  quality system font stacks only, ~72ch measure.
- **Colour system:** green = recommendation/verdict, red = hard
  requirements/compliance blockers, amber = open questions/contestable,
  blue = economics/pricing; per-section accents; key-stats band.
- **Interactivity:** sidebar TOC with scroll-spy, collapsible sections,
  client-side search with highlighting, anchor deep-links, back-to-top,
  sticky header, print stylesheet.
- **Structure:** ① resolved recommendation callout (now ≤6mo / later /
  parked split) + key stats ② U1/U2 resolutions ③ assumption verdict
  table (30 rows, linked into evidence) ④ decision analysis sections
  ⑤ passport evidence sections ⑥ portal-risk evidence sections ⑦ union
  References with in-text `[n]` jump markers.
- **Content fidelity:** every finding, citation, table, and the full
  assumption ledger from all three sources must appear. Reorganize for
  navigation; drop nothing; no editorializing beyond verdicts + the
  resolved decision rule.

## Step 4 — verify, then PR

- Re-run your adapted verifier: all sources incorporated (headings,
  fragments, table rows, URLs), zero external assets, anchors resolve, JS
  clean. Evidence in final message.
- Commit on `growth-research-docs`, `git push -u origin
  growth-research-docs`, then `gh pr create --base develop` — body carries
  **"Decisions & rationale"** + "Related: #534 (Route I), #535" (closes
  nothing). **Never merge.**
- Self-report:
  `/Users/moses/code/bin/ledger set righttenantry-growth-research-collation <status> "<note>"`
  (`working` at start, `in-review` when PR opens) and record the PR:
  `/Users/moses/code/bin/ledger pr righttenantry-growth-research-collation <url>`
- On blocked/finished:
  `herdr notification show "righttenantry-growth-research-collation" --body "<one-line>"`
- Final message: summary, files changed, PR URL, verifier evidence,
  verdict counts (X conf / Y ref / Z unr), any ranking changes.
