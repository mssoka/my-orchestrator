# Briefing: orchestrator-nefario-conflict-sensor

- **Repo:** my-orchestrator (`/Users/moses/code`, remote: the orchestrator meta repo)
- **Worktree:** this pane's cwd (`nefario-conflict-sensor` worktree, branch `nefario-conflict-sensor`, base `origin/main`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** `deepseek-v4-flash` (kimi walled until 08-08T21:57Z).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true` — this is the watcher's core logic; correctness matters.

## Mission

Add a **merge-conflict sensor** to `nefario-watch.ts` so the watcher detects when a tracked in-review PR becomes unmergeable (`mergeable: CONFLICTING` / `mergeStateStatus: DIRTY`) and alerts Silas — who relays to Gru → the minion rebases.

**Context (2026-08-04 incident):** PR #577 went CONFLICTING after a sibling PR (#574 sweep) merged to develop. nefario-watch's existing PR-state sensor (merge detection, CI, review, Perkins) never checked `mergeable` status — so the conflict sat undetected until the user tried to merge and hit it manually. The user asked "what happened to nefarios conflict sensors?" — the answer: they didn't exist. Now they will.

## Requirements

1. **The check:** in the existing PR-state polling loop (every 5 min, `gh pr list --state open` for tracked jobs), add `--json mergeable,mergeStateStatus` to the query (or per-PR `gh pr view <n> --json mergeable,mergeStateStatus`). When `mergeable` is `CONFLICTING` (or `mergeStateStatus` is `DIRTY`/`BLOCKED` for a merge-conflict reason), fire an alert.

2. **The alert:** inject a nefario-watch message into Silas's session:
   ```
   [nefario-watch · <ts>] CONFLICT on in-review job <job-id>:
   PR #<n> is CONFLICTING — develop moved since base. Relay to minion for rebase.
   ```
   Dedup: alert once per conflict-state transition (CONFLICTING → not-CONFLICTING → CONFLICTING again = two alerts). Same-state re-poll = no re-alert (same dedup pattern as the existing sensors).

3. **Silas's relay:** on the conflict alert, Silas relays to the minion's pane: "PR #<n> CONFLICTING — rebase onto <base>, force-push." Same as any sensor-driven relay.

4. **Do NOT break existing sensors:** the merge/CI/review/Perkins sensors stay exactly as they are. The conflict check is an ADDITION to the PR-state polling, not a replacement. Verify all five existing sensors still fire correctly after the change.

## Acceptance

- `nefario-watch.ts` gains the conflict check in the PR-state sensor; existing sensors unregressed.
- A simulated conflict (or a real one if timing allows) triggers the alert; dedup works (same-state re-poll = no re-alert).
- TypeScript parse-tested: `node --experimental-strip-types .pi/extensions/nefario-watch.ts` loads without errors (the raw-backtick gotcha — every inline `code` span in template literals must be escaped as \\`).
- Commit on `nefario-conflict-sensor`, push, `gh pr create --base main` titled "feat: nefario-watch conflict sensor (detect unmergeable in-review PRs)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

This is the orchestrator meta repo — no `_bmad` bootstrap needed (the repo IS the orchestrator). No `.env`, no staging/prod. TypeScript + pi extensions only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set orchestrator-nefario-conflict-sensor working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set orchestrator-nefario-conflict-sensor in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr orchestrator-nefario-conflict-sensor <url>`
- On blocked/finished: `herdr notification show "orchestrator-nefario-conflict-sensor" --body "<one-line>"`
- Final message: summary, files changed, PR URL, sensor logic explanation, open questions.

## Dispatch parameters

- repo: my-orchestrator
- repo_root: /Users/moses/code
- slug: orchestrator-nefario-conflict-sensor
- base: main
- pr_review: true
