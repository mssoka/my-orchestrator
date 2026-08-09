# Briefing: righttenantry-refcheck-rc1-2

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-rc1-2` worktree, branch `refcheck-rc1-2`, base `origin/develop`)
- **GitHub issue:** #548 (refcheck v1 feature line)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true` — automated review rounds will fire on your PR; address verdicts per the relay messages.

## Mission

Ship **Story RC1.2: Attestation UI — the References Section Choice** (Epic RC1, refcheck v1). Two documents are your spec, both in the repo:

1. `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` — **Story RC1.2** (acceptance criteria, files/areas, verify). This is your contract; every Given/When/Then must pass.
2. `_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md` — **§5.2, §5.3, §5.4** hold the verbatim copy (section framing, the attestation card anatomy + anti-coercion footer, the confirmation-page line). Copy goes in **verbatim** — do not paraphrase.

Context: RC1.1 (PR #557, merged) built the write path — "Yes" persists a `reference_contact_attestation` row via `insert_acknowledgement_records`. Your UI posts into that plumbing; the schema work is done. **Urgency:** RC1.1 made `reference_contact_choice` mandatory at submission with no UI yet — develop's form is UNSUBMITTABLE until you ship. You are the fix; develop deploys (incl. the copy-pack deploy) are gated on your merge.

## Requirements (distilled — the epics doc ACs govern)

1. References section gains the §5.2 framing copy above the first referee field group, and the attestation card at the end of the section per §5.3: heading, body, privacy link, **required radio pair, no default**, `role="radiogroup"` + `aria-required`, `aria-describedby` help text, `data-testid`s `ref-attestation` / `ref-attestation-yes` / `ref-attestation-no`.
2. Validation: no selection → scroll to the card with the §5.3 message, wired at **final submit** per the story ACs. Sequencing note: you ship BEFORE the stepper (`form-stepper-f1`, PR #561, in review) — build against the current single-long-form develop. The stepper minion will rebase onto your merged work and lift your validation into its References-step gating — so keep the validation wiring simple and self-contained (one function it can call); do NOT build step-aware gating yourself.
3. Confirmation page: "Yes" submissions carry the §5.4 line verbatim; "No" shows nothing.
4. No-JS: the choice posts with the plain SSR submission and persists via the RC1.1 path.
5. Wording is attestation/acknowledgement — **never "consent"** (AD-2).

## Acceptance

- All RC1.2 Given/When/Thens pass; server form tests (choice required, posted value plumbed); SSR render check of the card in both states; `make test` green (`make test-integration` if you touched plumbing).
- Update `_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`: `rc1-2` → `done` (and flip `rc1-1`/`rc2-1` from `review` to `done` while you're there — both merged this morning; the file is stale).
- Commit on `refcheck-rc1-2`, push, `gh pr create --base develop` titled "feat: refcheck rc1-2 — attestation UI (references section choice) (#548)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Do NOT run migrations against anything but a local/dev DB; do NOT touch prod.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc1-2 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc1-2 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-rc1-2 <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-rc1-2" --body "<one-line>"`
- Final message: summary, files changed, PR URL, AC checklist with evidence, notes for the stepper rebase (which function owns the attestation validation), open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-refcheck-rc1-2
- base: develop
- github_issue: 548
- pr_review: true
