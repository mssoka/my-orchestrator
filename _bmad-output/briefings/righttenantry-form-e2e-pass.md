# Briefing: righttenantry-form-e2e-pass

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-e2e-pass` worktree, branch `form-e2e-pass`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev**; supporting = **bmad-qa-generate-e2e-tests** for any scenario gaps you add (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass if a PR opens: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start — esp. the form-stepper-f1 shard (local-DB E2E pattern, timing trap, dot_env trap); badge-out shard per standing orders.
- **Perkins:** off unless a PR opens (test additions only → tell Silas and he arms it).

## Mission

Run the **full end-to-end applicant journey** against the fully-upgraded form (develop now has: stepper F1 + field diet F4 + upload copy F5 + attestation RC1.2 + save-resume F3 + W0 instrumentation + W1a copy). Slices are all green; nobody has walked the WHOLE form like a real applicant since the waves landed together. The user wants it done — this is a verification pass first, a test-gap PR second.

## Environment (per the stepper shard's proven pattern)

- Local Docker test DB (`make test-db-up`; port discipline — siblings may hold 54321/54322, pick a free one), seeded vacancy, local server. **Never staging, never prod.**
- `dot_env.load_default()` overrides process env — repoint by replacing the `server/.env` symlink with an edited copy (gitignored).
- Timing trap: submissions <2s reject as spam — sleeps before scripted submits.
- Real browser (Chromium) for the journey — Perkins used one successfully on this repo; mobile viewport (375×812) is the primary pass (80% of traffic), desktop secondary.

## The journey (evidence for EVERY step — screenshots + DB state)

1. **Arrival → stepper:** open the seeded vacancy form; prep block renders (rc: the F3-SEAM line now promises save-and-continue); step through all 8 named steps; sticky progress on mobile viewport.
2. **Validation gating:** try to advance past the References step WITHOUT the attestation choice → blocked with the §5.3 message; choose "Yes" → advances.
3. **Document step:** upload slots accept a real file (small image = camera-roll case); the >5MB case fails LOUDLY (r1 blocker — the dead-end is dead); "what counts as this letter" helpers present.
4. **Submit:** full submission succeeds; confirmation page shows the §5.4 line (Yes path); DB: application row + `reference_contact_attestation` row + IP/UA columns written.
5. **Save-resume:** fresh start → fill 2 sections → step-change fires a draft save (verify `form_draft` row written, debounce working — the r2 Illegal-invocation fix) → request continue-link → restore via link (dev-mode email capture per repo precedent — check how w0 verified Resend in dev) → state restored → submit from restored draft.
6. **No-JS fallback:** JS disabled → single long form → attestation radio posts → full submit succeeds.
7. **Analytics:** section funnel events fire with the stable `data-section-id`s; resume-token appears NOWHERE in any captured payload (r3/r4 regression).

## Acceptance

- Every journey step evidenced (screenshots/DB dumps/event logs in `_bmad-output/implementation-artifacts/e2e-form-pass-<date>/` committed in the worktree).
- The existing 57-scenario suite + all `make test` / `make test-integration` suites green on develop BEFORE and AFTER your pass.
- Gaps found → fixed or filed: a real defect = HALT and escalate to Gru immediately (numbered findings); a missing automated scenario = add it via **bmad-qa-generate-e2e-tests** and open a PR (`test: e2e full applicant journey`) — **never merge**.
- Final message: journey checklist with evidence paths, defects found (or "none — clean pass"), scenarios added, PR URL if any.

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-e2e-pass working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-e2e-pass in-review "PR <url>"` if a PR opens (+ `ledger pr`)
- On blocked/finished: `herdr notification show "righttenantry-form-e2e-pass" --body "<one-line>"`

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-form-e2e-pass
- base: develop
