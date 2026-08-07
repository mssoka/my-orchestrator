# Briefing: orchestrator-perkins-ops-codify

- **Repo:** orchestrator root (`/Users/moses/code`, remote: `mssoka/my-orchestrator`)
- **Worktree:** work directly in the orchestrator root (no worktree — this IS the repo; PR targets main)
- **Workflow:** bmad-quick-dev (targeted playbook edits). Perkins: OFF (docs — playbook codification). Self-review before PR: bmad-review-edge-case-hunter (playbook edits drive minion behavior — verify no contradictions with existing playbook sections).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF (docs deliverable).

## Mission

Codify three Perkins-ops patterns into `docs/orchestration-playbook.md` that are currently learned-but-undocumented (surfaced by dream-2026-08-07 UA3, reinforced by this window's evidence). These are Silas close-out / Perkins-round behaviors that, if unwritten, get rediscovered the hard way each session.

## The three patterns to codify

### 1. Formal skip-row policy (when NOT to fire a Perkins round)
A Perkins round should NOT fire when:
- The PR is a **pure no-op / docs-only / comment-only** diff with zero production bytes (e.g. RT CSP #585 — Perkins r1 still ran usefully to confirm byte-identical, but the policy should state when a round is skippable vs. always-on).
- The job is explicitly marked Perkins-OFF in the briefing (docs/lavish deliverables).
Pin the decision rule: **Perkins fires on every code PR by default; docs/no-op PRs may skip BUT only if the briefing or Gru explicitly waives — default is armed.** Cross-reference the existing Perkins sections.

### 2. Proactive-r2-vs-sensor-r1 framing
When a minion folds in advisory notes (N1/N2/...) pre-merge (the "fold-in" pattern, e.g. CSP #585 N1, RT-agent #169 N3), Silas should **proactively dispatch Perkins r2 on the updated sha** rather than waiting for the sensor tick to re-fire r1. Rationale: the sensor re-ticks on the new sha anyway, but a proactive r2 (with `prior_findings=r1/consolidated.json`, fix-audit mode) gives a cleaner verdict on just the delta. Document the proactive-r2 dispatch as the standard fold-in follow-up, with the prior-findings chaining.

### 3. Silas startup catch-up gap
When Silas launches on a fresh session, there's a **catch-up window** where he's re-orienting (reading playbook, ledger, agent list) before nefario-watch's first poll fires. During this window, in-flight minions can transition (done/idle) without a relay (this is how the cost-analysis completion slipped — see the no-PR-done-mid-turn gotcha). Document: on fresh-session startup, Silas should **proactively board-check all non-done jobs + idle panes** before settling into the watch loop, not just wait for the first sensor tick.

## How to write them

- Add these as clearly-delineated subsections or gotcha entries in the **Perkins / close-out** region of the playbook (don't bury them).
- **Cite the evidence** (the session examples: #585 fold-in, #169 N3, the cost-analysis slip) so future readers see the provenance.
- Cross-reference existing related playbook sections (don't duplicate — link/extend).
- Keep the playbook's existing voice/structure.

## Constraints

- This is the orchestrator's own playbook — precision matters (it drives Silas + minion behavior every session).
- Don't contradict existing Perkins/close-out sections — extend them.
- The gotchas live in AGENTS.md (separate concern — UA1 handles those); THIS task is playbook-only.

## Acceptance

- The three patterns codified in `docs/orchestration-playbook.md` with evidence citations.
- No contradictions with existing playbook sections.
- After user approval (lavish optional — it's a targeted edit, not a big doc; a clear PR body may suffice, but lavish if the diff is substantial): commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set orchestrator-perkins-ops-codify working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set orchestrator-perkins-ops-codify in-review "PR <url>"` when PR opens
- `herdr notification show "perkins-ops-codify" --body "<one-line>"` on finish
- Final message: summary, the three patterns + where they landed in the playbook, PR URL.

## Dispatch parameters

- repo: orchestrator (root)
- repo_root: /Users/moses/code
- slug: orchestrator-perkins-ops-codify
- base: main
