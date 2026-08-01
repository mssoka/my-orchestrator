# Briefing: righttenantry-form-funnel-w0

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-funnel-w0` worktree, branch `form-funnel-w0`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Ship **Wave 0 (instrumentation) + Wave 1a (copy pack)** of the ruled application-form completion plan. The spec is the merged report:

`_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md` — read the W0 instrumentation pack + W1a copy pack sections in full; they are the requirements.

Context: 66 invited → 8 applied (~11%) on the live 70 Meadowgate vacancy; target ≥20% by 13/08. Bimodal exits (~25% <30s shock; p75 8.7-min wall exits); 80% mobile; ~21 mandatory fields + 2 third-party letters.

## W0 — Instrumentation pack

PostHog is already live (EU project; `$pageview`/`$pageleave` only today). Add, per the report:

1. **Confirmation event** — fires on successful submission (NOT on validation-error re-render; the current page-reload pattern makes >1 pageview ambiguous — your event must disambiguate submit vs error vs reload).
2. **Section step/abandon events** — per form section: entered/completed (+ abandoned where derivable), with stable section ids.
3. **Stable anon id** — per the report's design (survives reloads, respects the existing consent posture — client events must honor the same consent gate as the current `$pageview` capture).
4. **Resend open/click tracking** — on the invite/reminder sends, per the report.

Verify: events emit correctly client-side (unit tests on payload shapes + the submit/error disambiguation); document in the PR exactly what Moses should see in PostHog to confirm.

## W1a — Copy pack (real copy, honest-expectation doctrine)

1. **Invite email** — honest "what you'll need" checklist (incl. the two third-party letters UP FRONT — no mid-form surprise) per the report's copy guidance.
2. **Form-header preparation block** — same doctrine at the top of the form.
3. **Two-stage doc-gathering reminder series** — per the report.
4. **KILL the lies**: remove/replace "only takes a few minutes" / "Takes about 10 minutes" and any sibling promises, wherever they appear (invite flow, form header, daft auto-reply if in-repo).

Copy lives in the app/templates — real edits, real copy, brand voice per `_bmad-output/planning-artifacts/brand-identity-and-design-system.md`.

## Acceptance

- All W0 events firing + tested; copy pack live in the app/templates; the "few minutes" lie is gone everywhere in the repo (`rg -i "few minutes|10 minutes"` clean or justified); tests pass; the report's W0/W1a checklists are ticked with evidence.
- Commit on `form-funnel-w0`, push, `gh pr create --base develop` titled "feat: form funnel instrumentation + honest-expectation copy pack (wave 0+1a)" with **Decisions & rationale**. **Never merge.**
- Follow-ups B (stepper) and C (save-resume) are SEPARATE minions — do not build them here; note any seams they should use.

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Do NOT run migrations against anything but a local/dev DB; do NOT touch prod.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-funnel-w0 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-funnel-w0 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-form-funnel-w0 <url>`
- On blocked/finished: `herdr notification show "righttenantry-form-funnel-w0" --body "<one-line>"`
- Final message: summary, files changed, PR URL, event list shipped, copy changes, PostHog verification notes, open questions.
