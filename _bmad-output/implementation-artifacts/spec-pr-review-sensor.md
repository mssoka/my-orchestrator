---
title: 'nefario-watch PR review sensor'
type: 'feature'
created: '2026-07-21'
status: 'done'
baseline_commit: '042fcd5d10c26a9149a4a44a3fca249d7299d007'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** nefario-watch detects PR merges and CI failures but is blind
to review activity — Gru learns of review feedback on in-review PRs only
when someone happens to look at GitHub.

**Approach:** Extend the existing 5-min `prTick` in
`.pi/extensions/nefario-watch.ts` to fetch each in-review PR's reviews,
dedupe by review id with a silent first-sighting baseline, classify NEW
submitted reviews, and inject a self-contained detection-only message
stating Gru's expected action per review state.

## Boundaries & Constraints

**Always:**
- Reuse `prTick`'s gh/injection patterns; parse owner/repo/number from the
  ledger `pr` URL, never from cwd.
- Silent baseline on first sighting of a job: record existing non-PENDING
  review ids, alert on none.
- Skip `PENDING` reviews WITHOUT recording their ids (a pending review
  keeps its node id when submitted — recording it would swallow the alert).
- Expected action per state: `CHANGES_REQUESTED` = Gru relays to minion
  pane as work needed (address comments, push, re-request review, ledger
  back to in-review); `COMMENTED` = Gru relays straight to minion as FYI,
  no user round-trip; `APPROVED` = Gru notifies user only ("PR approved —
  merge when ready").
- Every alert carries: job id, pane id, PR URL, review state, review URL,
  author, body, plus an explicit "detection only — nefario-watch never
  writes the ledger or sends pane input; Gru owns relays and ledger
  transitions" instruction.
- Existing pane/PR-merge/CI sensor behavior unchanged.

**Ask First:** alerting on standalone conversation comments (v1 ignores);
any author/bot filtering (locked: bots = humans); persisting baselines to
disk (v1 in-memory, matching existing sensor state).

**Never:** ledger writes, pane input, `gh` mutations; GitLab support
(non-GitHub PR URLs skipped silently by the review sensor only); touching
`gru.ts` or Gru's live session; merging the PR; alerting on
DISMISSED/unknown states (record as seen, no alert).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| First sighting | job in-review, existing reviews | Record non-PENDING ids; zero alerts | N/A |
| New review, actionable state | baselined job; CHANGES_REQUESTED / COMMENTED / APPROVED | One followUp message with the per-state expected action above | review-URL resolution fails → fall back to PR URL |
| PENDING review | state PENDING | Ignored, id NOT recorded; later submission alerts as new | N/A |
| DISMISSED/unknown | new review | Id recorded; no alert | N/A |
| Re-observation | same id again (incl. new head sha) | Never re-alerts | N/A |
| gh pr view fails | offline/rate-limit/deleted PR | Skip job this tick, no state change | existing `prInfo` null path |
| Non-GitHub pr URL | GitLab etc. | Review sensor skips job; merge/CI sensors unaffected | regex no-match → skip |
| Long body | > ~1500 chars | Truncate + "…(full text at review URL)" | N/A |

</frozen-after-approval>

## Code Map

- `.pi/extensions/nefario-watch.ts` — extend `prInfo`'s gh call with
  `reviews`; add `seenReviews: Map<job_id, Set<review_id>>` beside
  `prStates`/`ciAlerted`; classify in `prTick`'s non-terminal branch;
  update header doc comment.
- `bin/ledger` — read-only reference for job fields. No changes.
- `docs/orchestration-playbook.md` — Tracking section (fourth sensor) +
  GitLab-deferred note.

## Tasks & Acceptance

**Execution:**
- [x] `.pi/extensions/nefario-watch.ts` — implement the sensor per Intent
  + I/O matrix; resolve review URLs lazily via
  `gh api repos/{owner}/{repo}/pulls/{n}/reviews` matched on `node_id`,
  only when alerting on a NEW actionable review
- [x] `docs/orchestration-playbook.md` — Tracking: add review sensor as
  fourth sensor with convention "Request changes = work, Comment = FYI
  straight to minion, Approve = notify human"; standalone comments ignored
  in v1; short Gitlab-deferred note (unresolved diff threads = work,
  approvals = approve; built when the first GitLab-hosted job lands)
- [x] Ephemeral stubbed-`pi` harness (not committed) driving `prTick`
  through the I/O matrix rows — exercises edge cases with zero repo test
  infra

**Acceptance Criteria:**
- Given an in-review job with a GitHub PR URL, when the tick first
  observes its reviews, then no review alert is injected.
- Given a baselined job, when a new CHANGES_REQUESTED review appears, then
  Gru receives one followUp message with job id, pane id, PR URL, review
  URL, author, body, and the relay-as-work-needed action.
- Given a baselined job, when a new COMMENTED / APPROVED review appears,
  then the message frames COMMENTED as FYI straight to the minion and
  APPROVED as notify-user-only.
- Given a PENDING review, when later submitted, then it alerts as new.
- Given any alerted review, when later ticks run (even after a head-sha
  change), then it never re-alerts.
- Given a non-GitHub PR URL or gh failure, when the tick runs, then the
  job is skipped silently and MERGED/CI handling is unchanged.
- Given any injected message, when read cold, then it states nefario-watch
  only detects and Gru owns ledger writes and pane relays.

## Spec Change Log

## Design Notes

`gh pr view --json reviews` has no URL field → resolve `html_url` via one
`gh api .../reviews` call per PR only when alerting (match on `node_id`);
fall back to the PR URL on failure. Baselines in-memory like `prStates` —
restart re-baselines silently, per locked spec. Bodies truncate at ~1500
chars (bot reviews run 7k+; the URL has the full text). No test infra for
`.pi/` → stubbed-pi harness + read-only gh smoke against
`solarity-services/RightTenantryAgents#164` (real COMMENTED review).

## Verification

**Commands:**
- `npx tsc --noEmit --strict --skipLibCheck --module esnext --target es2022 .pi/extensions/nefario-watch.ts` (temp tsconfig mapping the global pi-coding-agent types) — clean
- `npx tsx /tmp/nefario-review-smoke.ts` — stubbed `pi.exec`/`sendMessage`; all I/O-matrix assertions pass
- `gh pr view https://github.com/solarity-services/RightTenantryAgents/pull/164 --json state,headRefOid,statusCheckRollup,reviews` — expected: parses, one COMMENTED review (read-only)

## Suggested Review Order

**Review sensor core**

- Entry point: baseline → dedupe → classify → alert flow inside the non-terminal tick branch
  [`nefario-watch.ts:371`](../../.pi/extensions/nefario-watch.ts#L371)
- Per-state expected actions injected verbatim so a cold Gru session knows what to do
  [`nefario-watch.ts:73`](../../.pi/extensions/nefario-watch.ts#L73)
- GitHub-only URL gate; GitLab MR shapes never match, sensor skips silently
  [`nefario-watch.ts:69`](../../.pi/extensions/nefario-watch.ts#L69)
- Dedupe state: silent first-sighting baseline; PENDING ids never recorded
  [`nefario-watch.ts:222`](../../.pi/extensions/nefario-watch.ts#L222)
- Reviews ride the existing per-PR gh call — no extra fetch cost per tick
  [`nefario-watch.ts:267`](../../.pi/extensions/nefario-watch.ts#L267)
- Lazy review-URL resolution (only when alerting), PR-URL fallback on failure
  [`nefario-watch.ts:315`](../../.pi/extensions/nefario-watch.ts#L315)
- Header doc: alert policy for the new fourth sensor
  [`nefario-watch.ts:40`](../../.pi/extensions/nefario-watch.ts#L40)

**Docs**

- Tracking section: fourth sensor convention + failure modes
  [`orchestration-playbook.md:185`](../../docs/orchestration-playbook.md#L185)
- GitLab-deferred note with the planned mapping
  [`orchestration-playbook.md:204`](../../docs/orchestration-playbook.md#L204)
