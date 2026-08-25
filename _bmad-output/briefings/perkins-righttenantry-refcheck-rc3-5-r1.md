# Perkins briefing — round 1: righttenantry-refcheck-rc3-5

- **PR:** https://github.com/solarity-services/RightTenantry/pull/600 (targets `develop`)
- **Reviewed sha:** `cc1b0413360bb45e9e59924bba2ad64e169b35b5` (short `cc1b041`; commit "RC3.5: reference-check cadence sweep + Cloud Run Job (#548)")
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-5.md` + the story spec at `_bmad-output/implementation-artifacts/spec-rc3-5-the-sweep-cadence-engine-cloud-run-job.md` + the architecture (AD-4/AD-6/AD-14/AD-15, A2, A7, §4.6, §8.3, §9). No GitHub issue (tracked under #548).
- **prior_findings:** the rc3-4 rounds' consolidated.json files (`_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/`..`r3/`) — CONTEXT (rc3-5 extends the rc3-4 terminal states; the rc3-4 invariants carry forward). This round's findings are about the sweep delta.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**RC3.5: The Sweep — Cadence Engine + Cloud Run Job.** The 15-minute sweep that owns every reference-check send + transition:
- **Infra:** a `reference-checks` Cloud Run Job (`docker-entrypoint.sh` entry, `deployment/terraform/reference-checks-job.tf`, a 15-min Cloud Scheduler entry in `scheduler.tf` — house pattern, same env-gating as retention/digest) + a shared-secret `POST /api/v1/internal/reference-checks` manual-fire route.
- **The tick:** for rows with `next_attempt_at <= now()` AND `taken_over_at IS NULL`: compute the due step from the attempt log — **T0 invite / T+24h applicant co-nudge / T+48h reminder 1 / T+96h reminder 2 + landlord warm-handoff (with attempt log) / T+144h terminal `unreachable`** — send via the rc3-2 helpers, and apply transition + atomic attempt-append + next-step as ONE guarded update (AD-4, AD-14).
- **Co-nudge gate:** fires only when the form was never opened AND no draft exists (A2); taken-over rows skipped entirely.
- **T+96h:** reminder 2 + the `reference_unreachable` warm-handoff notification (attempt log rendered); T+144h terminal transition is **silent** (no duplicate terminal notification, §8.3).
- **Terminals:** abandoned form w/ saved answers → `partial` (result structured from `draft_answers`, unanswered null, confidence capped medium); zero answers → `unreachable`; failed correction cycle → `unreachable` + `reference_unreachable` notification (§4.6).
- **Failure:** a row that can't process → `failed` (`outcome` NULL + `terminal_reason`), Sentry captures, **no landlord notification** (§4.6).
- **Liveness (AD-15):** per-tick completion log; any job failure → Sentry.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

Production server code + infra on the referee path. The diagnosis/design is PINNED — review the implementation.

- **EXACTLY-ONCE + IDEMPOTENT IS THE LOAD-BEARING INVARIANT:** re-runs after downtime MUST NOT double-send. The **no-duplicate-T0 across a retry is a REQUIRED test** — verify it's real (a retry of a T0 tick must not re-send the invite; the guarded update must make the re-run a no-op). The same for every cadence step (a re-run after a crash mid-tick must not double-send reminder 1/2 or the warm-handoff).
- **THE GUARDED ATOMIC UPDATE (AD-4/AD-14):** the transition + atomic attempt-append + next-step must be ONE guarded `UPDATE ... WHERE` (like the rc3-4 objection pattern) — a row processed by two concurrent ticks must not double-advance or double-send. Verify the race test is real.
- **TERMINAL-STATE RESPECT (rc3-4 carry-forward):** `objected` (sticky AD-6 — blocked, NEVER re-sent), `refused` / `awaiting_correction` / `form_completed` must not be re-processed; taken-over rows (`taken_over_at IS NULL` check) skipped entirely. Verify a sweep tick against each terminal is a no-op.
- **The cadence math:** T0 / T+24 / T+48 / T+96 / T+144 computed from the attempt log (next_attempt_at), not wall-clock drift — verify the fake-clock tests per cadence step are real + the due-step computation is correct (a wrong offset = a reminder at the wrong time).
- **The co-nudge gate:** fires ONLY when the form was never opened AND no draft exists — verify the A2 checks (form_opened_at / draft_answers) are correct + the gate doesn't fire for a form that was opened/drafted.
- **The terminals:** `partial` (from draft_answers, unanswered null, confidence capped medium) vs `unreachable` (zero answers) vs failed-correction — verify the result structuring + the §8.3 no-duplicate-terminal (T+144 silent; the warm-handoff already fired at T+96).
- **The failure path:** a row that can't process → `failed` with NO landlord notification + Sentry capture.
- **Infra (Terraform):** the job + scheduler follow the house pattern (retention/digest precedent), env-gating matches, the manual-fire route is shared-secret protected (not public).
- **No-op without Twilio keys** (rc3-2's posture): the sweep still runs + transitions; SMS just doesn't send — verify the no-op path is real + doesn't stall the transition.
- **No em-dashes** in user-facing copy (the warm-handoff attempt-log render).
- **CONTEXT NOTE (not a finding):** this PR was affected by a known bmad-tooling quirk (its work was briefly misdirected to the main checkout; Silas synced it into the worktree + the PR carries the full work, verified). Review the PR's content as-is.
- **Do NOT re-open the rc3-4 findings** (verified fixed in its rounds) — carry-forward markers only.

### Legitimate findings here would be
- **A double-send path** (a retry or a concurrent tick re-sends T0/reminder/warm-handoff) — a blocker (the exactly-once invariant).
- **A terminal row re-processed** (objected/taken-over/etc. not skipped) — a blocker.
- **A non-atomic transition** (send + update not one guarded unit — a crash between them double-sends or loses the transition) — a blocker.
- **The cadence math wrong** (a due step fires at the wrong time).
- **The co-nudge gate wrong** (fires for an opened/drafted form, or misses a never-opened one).
- **The failure path notifying the landlord** (violates §4.6) or not capturing to Sentry.
- **A Terraform/env-gating mistake** (the job public, the scheduler wrong cadence, the manual-fire route unprotected).
- **A Gleam compile/test failure** (the minion's fake-clock tests per cadence step + the race + no-duplicate-T0 + terminal-respect tests).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 600 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + the story spec + the architecture (AD-4/AD-6/AD-14/AD-15, A2, A7, §4.6, §8.3, §9), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1`, `prior_findings` = none for this PR (the rc3-4 rounds are CONTEXT). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 600 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 600 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc3-5 / **Reviewed sha:** cc1b041 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-5-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: zai-coding-cn/glm-5.2** — kimi quota down; glm-5.2 is the sanctioned fallback.
