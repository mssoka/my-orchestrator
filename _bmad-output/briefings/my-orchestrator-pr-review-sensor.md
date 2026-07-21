# Briefing: my-orchestrator-pr-review-sensor

First: read `/Users/moses/code/docs/orchestration-playbook.md` section
**"Minion standing orders"** — they apply in full (work only in your
worktree, env read-only, ledger self-report, mega-minion rules,
notification on halt/finish) except where this briefing overrides.

## Task

Add a **GitHub PR review sensor** to the orchestrator's watcher extension,
`.pi/extensions/nefario-watch.ts` (in your worktree:
`/Users/moses/.herdr/worktrees/code/pr-review-sensor/.pi/extensions/nefario-watch.ts`).
Read the whole file first — match its existing single-file, dependency-free
style and its state/baseline patterns. pi extension API docs if needed:
`/Users/moses/.local/share/fnm/node-versions/v22.22.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md`.

### Locked spec (user decisions, 2026-07-21 — not negotiable)

On the existing 5-min PR-watcher tick, for every ledger job in `in-review`
with a `pr` URL recorded:

1. Fetch the PR's reviews via `gh` (e.g. `gh pr view <n> --repo <owner/repo>
   --json reviews` — parse owner/repo/number from the ledger `pr` URL, never
   from cwd). Skip reviews with state `PENDING`.
2. Dedupe by review id per job. Silent baseline on first poll/startup —
   never alert on reviews that already existed.
3. Classify each NEW submitted review and inject a structured message to
   Gru (the extension's existing injection mechanism):
   - `CHANGES_REQUESTED` → Gru relays to the minion pane as **work needed**:
     review URL, author, body, PR URL, and the instruction to address each
     comment, push, then re-request review and set the ledger back to
     `in-review`.
   - `COMMENTED` → Gru relays **straight to the minion** as FYI/judgment
     (no user round-trip): same payload, framed as "address or reply, your
     call".
   - `APPROVED` → Gru notifies the **user only**: "PR approved — merge when
     ready". No minion action.
   - Standalone PR conversation comments: **ignored entirely** (v1).
   - **No author/bot filtering** — bot reviews (CodeRabbit etc.) are treated
     exactly like the human's.
4. **Detection-only.** nefario-watch never writes the ledger and never
   sends input to panes — it injects the message; Gru owns relays and all
   ledger transitions. Make that explicit in the injected text so the
   receiving Gru session knows the expected action per state.
5. CI sensor and MERGED/CLOSED handling stay as-is; don't regress them.

### Docs (same PR)

Update `docs/orchestration-playbook.md`:
- Tracking section: add the review sensor as a fourth sensor with the
  convention **Request changes = work, Comment = FYI straight to minion,
  Approve = notify human**; note standalone comments are ignored in v1.
- Add a short "GitLab" note: GitLab support deliberately deferred — GitLab
  has no native review states; planned mapping is unresolved diff threads =
  work, approvals = approve, to be built when the first GitLab-hosted job
  lands.

## Acceptance criteria

- Sensor implemented per spec above; existing three sensors' behavior
  unchanged.
- Injection messages are self-contained (Gru reads them cold: job id, pane,
  PR, review state, URL, author, expected action).
- Playbook updated as above.
- PR opened against `main` of `mssoka/my-orchestrator` with a
  **"Decisions & rationale"** section, including: Gru's live session keeps
  running the old extension until the PR merges AND the pi session reloads
  extensions — that reload is a post-merge human step.
- Dogfood note in the PR: PR `solarity-services/RightTenantryAgents#164`
  has a COMMENTED swarm review posted by a sibling minion — after reload,
  that PR (if still in-review) is the natural first live case.

## Repo map

Orchestrator root repo (`mssoka/my-orchestrator`, default branch `main`):
- `.pi/extensions/nefario-watch.ts` — the file you're extending (~343 lines).
- `.pi/extensions/gru.ts` — standing-orders enforcement (do not touch).
- `bin/ledger` — ledger CLI (read it to see job fields: `pr`, `status`,
  `pane_id`).
- `docs/orchestration-playbook.md` — docs to update.

## Env / bootstrap

- Worktree: `/Users/moses/.herdr/worktrees/code/pr-review-sensor`, branch
  `pr-review-sensor` from `origin/main`.
- `_bmad` copied from the main checkout; root `.env` **symlinked** — treat
  as read-only (you likely won't need it).

## Verify

- Type-check/lint with whatever the repo provides (check `package.json` /
  `tsconfig.json`; if none cover `.pi/`, at minimum `npx tsc --noEmit` on the
  file or a syntax check via the repo's existing toolchain — say in the PR
  what you ran).
- If feasible, a read-only smoke of the review-fetch logic against PR
  `solarity-services/RightTenantryAgents#164` (real `gh` call, no injection).
- Do NOT reload or touch Gru's live session/extensions.

## Model policy

Unset — pi default resolution (launch plain `pi`; same for any mega-minions).

## Skills policy

- **Your workflow skill: `bmad-quick-dev`** — follow its step files; step-01
  clarify per standing orders (numbered questions, then HALT; Gru relays).
  Internal approval checkpoints are pre-approved — proceed.
- **Mega-minions** (if you self-review before opening the PR):
  `bmad-review-adversarial-general` and `bmad-review-edge-case-hunter`.
  Close every mega-minion pane before finishing.
