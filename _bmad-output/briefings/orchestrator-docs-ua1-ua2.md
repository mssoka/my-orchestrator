# Briefing: orchestrator-docs-ua1-ua2

- **Repo:** orchestrator root (`/Users/moses/code`, remote: `mssoka/my-orchestrator`)
- **Worktree:** work directly in the orchestrator root (no worktree; PR targets main)
- **Workflow:** bmad-quick-dev (targeted doc edits). Perkins: OFF (docs). Self-review before PR: bmad-review-edge-case-hunter (AGENTS.md is read every Gru/Silas turn — high blast radius; verify ZERO content loss in the reorg + no broken cross-refs).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (docs deliverable).

## Mission

Two doc-maintenance tasks from dream-2026-08-07 (UA1 + UA2, user-approved):

### UA1 — AGENTS.md gotchas themed structural split
The "## Gru gotchas (field notes, learned the hard way)" section in `/Users/moses/code/AGENTS.md` is a flat bulleted list that's grown to ~25 entries. It's read on **every** Gru/Silas turn, so length = real context cost. Reorganize it into **themed subsections** for scannability:

- **Dispatch / handover** (herdr agent send/pane run, wait-idle, identity-tab splits, cwd-Gru guard)
- **Provider incidents** (the 4 classes: transient/mid-turn/connection/quota-403/glm-5.2; PI_MODEL override; continue vs redirect)
- **Perkins / review sensors** (self-close norm, sensor echo races, serialize-hold, moot-on-merge, skip-row)
- **Ledger** (table view lossy, events count, same-status note, pr-field timing)
- **Pane forensics** (session jsonl ground truth, idle-hides-dead, idle-hides-live-dead-turn, extension armedness)
- **Extensions** (raw-backtick kills load, etc.)

**Hard constraints for UA1:**
- **ZERO content loss** — every gotcha, every date citation, every addendum must survive the reorg. This is a pure structural move (group + add subheaders), not editing/removing content.
- Preserve the intro line ("Gru gotchas (field notes, learned the hard way)").
- Keep each gotcha's full text (the parenthetical date/evidence citations are load-bearing provenance — keep them).
- If a gotcha spans two themes, put it in its primary theme and add a one-line cross-ref where useful.

### UA2 — playbook worktree-bootstrap node_modules symlink
In `docs/orchestration-playbook.md`, the **Worktree bootstrap** step (Dispatch step 4, ~line 387) notes worktrees only get git-tracked files. For **JS repos** (e.g. RightTenantry), a fresh worktree ships no `node_modules` → `make build` fails on tailwind. Add the standard fix: **symlink `node_modules` from the main checkout into the worktree** at bootstrap (same-deps base branch → safe; if a minion changes deps it runs its own install). Add it as a clear sub-step / note in the worktree-bootstrap section, scoped to JS repos.

## Constraints
- AGENTS.md reorg = pure structural; **no content loss**, no rewording of individual gotchas.
- Playbook edit = additive (the symlink step); don't contradict the existing bootstrap logic.
- Don't touch Perkins-ops patterns (UA3 — a separate minion owns those).

## Acceptance
- UA1: AGENTS.md gotchas reorganized into themed subsections, **diff = moves + subheaders only** (verify no gotcha text changed/lost).
- UA2: playbook worktree-bootstrap has the node_modules symlink step for JS repos.
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set orchestrator-docs-ua1-ua2 working` at start
- `/Users/moses/code/bin/ledger set orchestrator-docs-ua1-ua2 in-review "PR <url>"` when PR opens
- `herdr notification show "docs-ua1-ua2" --body "<one-line>"` on finish
- Final message: the themed subsections created (UA1), confirmation zero content loss, the playbook symlink step (UA2), PR URL.

## Dispatch parameters
- repo: orchestrator (root)
- repo_root: /Users/moses/code
- slug: orchestrator-docs-ua1-ua2
- base: main
