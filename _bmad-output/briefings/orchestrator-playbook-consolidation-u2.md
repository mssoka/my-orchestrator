# orchestrator-playbook-consolidation (U2 — user-approved 2026-08-19)

## Task

Consolidate the playbook's Model policy and Perkins sections — the
recorded U2 scope — ending the self-contradiction Bob's dream surfaced:
Model policy ~line 247 is glm-first (commit 39c9574) while ~lines
285-296 still mandate kimi-coding/k3 for Perkins/Gru/Bob. Both can't be
true; make the playbook single-voiced again.

## Canonical doctrine to write (the ruling chain, do NOT invent policy)

1. **Reasoning tier (Gru / Perkins rounds / Bob):** kimi-coding/k3
   primary → zai-coding-cn/glm-5.3 fallback → HOLD when both probe
   down. **deepseek-v4-pro is BANNED (cost, 7e889ec).**
   deepseek-v4-flash is ops/coding ONLY.
2. **Probe at EVERY reasoning dispatch** (k3 "back" is never durable;
   freed windows re-cap; cap-message reset times lie; single probe-DOWN
   row = re-probe once before acting).
3. **Model flips apply to NEW dispatches only** — in-flight panes
   finish on their launched model.
4. **1302 concentration:** with k3 cycle-capped, glm bursts
   episodically — one continue per errored pane, hold NEW glm fan-outs
   until the wave settles, escalate only if continues stop clearing.
5. **402 class:** deepseek 402 = account wall, user top-up fixes it,
   waiting does not; per-pane recovery = /model <ops fallback> +
   continue, once.
6. **Pane valve is ADVISORY; business priority resolves contention:
   RT first over PP** (0d70ff5).
7. Perkins specifics: provenance pin (--model on every round-MAIN
   launch + verify session modelId), lens --cwd pin, empty-lens doctrine
   (3rd straight empty → sweep + regenerate; g-wave compensation
   verdict counts as valid), vision caveat verbatim on non-k3 rounds,
   fix-audit hold on UNSTABLE (red, not pending) targets.

## Structure changes

- Model policy + Perkins sections rewritten as the single source above.
- **Supersede history → changelog appendix** at the end of the playbook
  (dated one-liners: 08-12 k3 retired → 08-14 glm-5.3 → 08-16 k3 back →
  08-19 v4-pro ban + chain → 08-19 evening flash ops return). The body
  states CURRENT truth; the appendix carries how we got here.
- Cross-check every other playbook section that names a model or
  provider for staleness (grep kimi, glm, deepseek, v4-pro, flash).

## Standing rules that bind this job

- **Sensor-doctrine sync:** grep `.pi/extensions/*.ts` for the retired
  doctrine being amended — the cap-3 echo class lived in
  nefario-watch.ts after the playbook retired it. Amend or confirm
  clean; state findings in the PR.
- DOCS deliverable → **lavish review BEFORE the PR opens** (build the
  artifact; Gru relays the URL to the user; merge only after user
  ack).
- AGENTS.md gotchas are Gru-owned: if consolidation surfaces a gotcha
  that now contradicts the playbook, NOTE it in the PR — Gru amends
  AGENTS.md separately after merge.

## Acceptance

- No contradiction remains: one grep for each retired phrase
  (e.g. "MUST pass kimi", glm-first at 247) returns the single new
  policy statement.
- Changelog appendix present and dated.
- Lavish artifact reviewed by the user before PR.
- PR is docs-only (playbook + nothing else, except sensor-config
  changes if the sync rule demands them).

## Skills policy

bmad-quick-dev; lavish for the review artifact.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: orchestrator root
- repo_root: /Users/moses/code
- slug: playbook-consolidation-u2
- base: main
- model: deepseek-v4-flash
- worktree: MANDATORY (orchestrator-root exception)
- pr_review: 0 (docs; lavish loop is the review)
