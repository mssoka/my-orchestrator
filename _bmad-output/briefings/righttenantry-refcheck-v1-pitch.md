# Briefing: righttenantry-refcheck-v1-pitch

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-v1-pitch-copy` worktree, branch `refcheck-v1-pitch-copy`, base `origin/develop`)
- **GitHub issue:** #548 (read it + comments, incl. the 2026-07-29 gate amendment — the pitch serves the amended gate)
- **Skills policy:** workflow = **bmad-cis-storytelling** (follow its step files; orchestration overrides per standing orders — step-01 clarify: ask numbered questions then HALT for Gru relay; internal approval checkpoints pre-approved). Review pass (optional): **bmad-review-adversarial-general**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).

## Mission

Produce the **cohort pitch copy-deck for the reference-checking feature** — the sales asset the amended gate calls for ("pitch-test 'we check references for you' with something demoable" + the Wizard-of-Oz delivery note):

`_bmad-output/planning-artifacts/refcheck-pitch-copy-deck-2026-07-29.md`

Copy-deck convention per the repo's existing `*-copy-deck-*.md` files. No code changes. Planning artifact + PR only.

## Required reading

1. `gh issue view 548 --repo solarity-services/RightTenantry --comments`
2. `_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md` — the pain story (manual reference-chasing: 1–2h + 2–10 days per applicant; hybrid completion ~55–88%; costs ~$0.60–0.85/reference; EUR 299 framing)
3. `_bmad-output/planning-artifacts/research/problem-solving-growth-routes-2026-07-26.md` — the Conversion Offensive, concierge cohort, G1/G2 evidence standards (the pitch must serve these, not dodge them)
4. Voice/brand canon: `brand-identity-and-design-system.md`, `site-storytelling-design-strategy-2026-06-10.md`, and one existing copy-deck for format (e.g. `landlord-reference-letter-copy-deck-2026-07-20.md`)
5. `prd.md` executive summary — product framing (EUR 299/vacancy vs EUR 2,990 agent; March 2026 reforms stakes)

## Deliverable contents (all four, real copy)

1. **Cohort pitch variants** for "we check references for you": cold/warm email (short + long), verbal script (60s + 3min), one follow-up. Honest about what v1 is: structured referee verification, founder-supervised — never claim AI voice calls exist.
2. **One-page narrative** (problem → the manual-chase pain → the promise → how it works today → EUR 299 framing) usable as a leave-behind section in cohort materials.
3. **Cohort conversation script addendum — the gate-2 instrument:** open, non-leading questions that surface whether manual reference-chasing is a top pain / willingness-to-pay driver (e.g. ordering against other pains; "tell me about the last time" behavioural prompts; what would make it a must-pay). This is the veto mechanism on v2 — design it to detect the truth, not to confirm the feature.
4. **Internal Wizard-of-Oz ops note:** what the founder does when a landlord says yes (form-first collection, founder-placed follow-up where needed, what the landlord sees), what is measured (conversion on the pitch, completion, pain ranking), and the line the founder never crosses (no fabricated automation claims).

## Constraints

- No fabricated stats — anchor every number to the research (cite doc + section inline).
- Ireland-first audience; plain landlord language, no proptech jargon; brand-voice consistent.
- The pitch sells the outcome (verified references without the chase), not the technology.

## Acceptance

- Copy-deck at the exact path above with all four sections; stats anchored; brand-consistent; open questions numbered.
- Commit on `refcheck-v1-pitch-copy`, `git push -u origin refcheck-v1-pitch-copy`, `gh pr create --base develop` titled "docs: reference-checking cohort pitch copy-deck (#548)" with a **Decisions & rationale** section. **Never merge.**

## Env/bootstrap

Gru applied standard bootstrap (`_bmad` copied, `.env` symlinked). Env is read-only; commit nothing from it. Docs task — do NOT run the app or tests.

## Verify

Artifact exists at the path; markdown renders; internal doc links resolve; no code files touched (`git diff --stat` shows only the new artifact).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-pitch working` at start (`clarifying` if you halt with questions)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-pitch in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-v1-pitch <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-v1-pitch" --body "<one-line>"`
- Final message: summary, files changed, PR URL, open questions.
