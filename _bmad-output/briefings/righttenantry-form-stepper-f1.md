# Briefing: righttenantry-form-stepper-f1

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-stepper-f1` worktree, branch `form-stepper-f1`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true` — automated review rounds will fire on your PR; address verdicts per the relay messages.

## Mission

Ship **follow-up B** of the ruled application-form completion plan: the **F1 progressive-disclosure stepper** on the existing 8 application-form sections, with **F4 field diet** and **F5 mobile upload copy** folded in. The spec of record:

`_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md` — read the Generated Solutions table (F1, F4, F5 rows), Solution Analysis, Recommended Solution (Wave 1 build pack), and Risk Mitigation in full; they are the requirements.

Context: W0+1a (instrumentation + copy pack) shipped in PR #556 (merged). 66 invited → 8 applied (~11%); target ≥20% by the 13/08 vacancy close; 80% mobile traffic.

## Requirements

1. **F1 stepper** — section-at-a-time flow over the existing 8 sections: named progress ("Step 3 of 8 — Work & Income"), sticky progress on mobile. Built on the existing `data-condition` engine. **Single POST at the end** — no per-section server round-trips. **Progressive enhancement:** the SSR no-JS fallback remains the current single long form (this is a hard risk-mitigation requirement — verify it).
2. **F4 field diet** — defer non-scoring optional fields (`listing_source` → post-submit or drop); collapse the optional address cluster. **All scoring inputs untouched** — do not remove, rename, or re-require any field the scorer reads.
3. **F5 upload copy** — camera-roll-friendly copy at the document slots; per-slot "what counts as this letter" helper text.

## Seams (left by the W0 minion, PR #556 — use, don't rebuild)

- Sections carry stable `data-section-id`s in DOM order; `apply_analytics.js` section funnel keys off them — **keep those ids intact** and stepper analytics (per-step funnel) come free.
- The prep block is `form_view.view_prep_block()` — it contains an `F3-SEAM` comment. **Leave that comment and the one-visit line untouched**; the C (save-resume) minion swaps it.

## Acceptance

- Stepper works end-to-end on mobile + desktop; no-JS fallback still submits the full form; `application_form_section_*` events still fire with unchanged section ids; scoring inputs unchanged (diff-verifiable); F4/F5 copy in place.
- `make test` and `make test-integration` (docker test DB) green; new behavior covered (step navigation, validation gating per step, fallback path).
- Commit on `form-stepper-f1`, push, `gh pr create --base develop` titled "feat: application-form stepper (F1) + field diet (F4) + upload copy (F5)" with **Decisions & rationale**. **Never merge.**
- Follow-up C (save-resume) is a SEPARATE minion — do not build it here; note any seams it should use (especially how your step navigation maps to "section change" for draft-saving).

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Do NOT run migrations against anything but a local/dev DB; do NOT touch prod.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-stepper-f1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-stepper-f1 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-form-stepper-f1 <url>`
- On blocked/finished: `herdr notification show "righttenantry-form-stepper-f1" --body "<one-line>"`
- Final message: summary, files changed, PR URL, fallback verification, scoring-input diff proof, seams noted for C, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-form-stepper-f1
- base: develop
- pr_review: true
