# Perkins review — orchestrator-selected-safety-fixes r1

## Mission
You are the independent Perkins round main for `orchestrator-selected-safety-fixes`, PR #33 in `mssoka/my-orchestrator`. Review only the exact PR head `7b823c9dd02580d2bd77f2c5d241aa308ee6b9f4` in your detached worktree. Never fix, edit, push, merge, or touch the implementing minion's worktree. The human remains the merger.

## Mandatory model override
The user explicitly overrides the normal model policy for this PR: the round main and every review lens use `zai-coding-cn/glm-5.3` at `max`. Verify the round session `modelId` and `thinkingLevel` from its session JSONL. Every lens must launch with the full model path and `--thinking max`; never launch bare `pi`, never use Astra, and never flip models. If GLM fails, stop and report the provider error; do not fall back to Astra or another model.

## Exact review inputs
- PR: `https://github.com/mssoka/my-orchestrator/pull/33`
- Reviewed head: `7b823c9dd02580d2bd77f2c5d241aa308ee6b9f4`
- Base: `main`
- Detached worktree: `/Users/moses/.herdr/worktrees/code/perkins-orchestrator-selected-safety-fixes-r1`
- Original implementation briefing/spec: `/Users/moses/code/_bmad-output/briefings/orchestrator-selected-safety-fixes-2026-09-12.md`
- Canonical full diff: `/Users/moses/code/_bmad-output/perkins/orchestrator-selected-safety-fixes/r1/diff.patch` (do not regenerate or re-fetch)
- Chunk 1: `/Users/moses/code/_bmad-output/perkins/orchestrator-selected-safety-fixes/r1/diff-chunk-1.patch` (2,107 lines; `.pi`, `_bmad-output`, and `bin` files)
- Chunk 2: `/Users/moses/code/_bmad-output/perkins/orchestrator-selected-safety-fixes/r1/diff-chunk-2.patch` (1,478 lines; `docs` and `test` files)
- Round output directory: `/Users/moses/code/_bmad-output/perkins/orchestrator-selected-safety-fixes/r1/`
- No GitHub issue; use the original briefing as the spec/context.

The full diff is over the code-review headless chunk threshold. Run two sequential complete lens waves, one per canonical chunk, then merge findings before the mandatory verification/consolidation pass. Do not substitute a hand-written subset: use every lens defined in the installed `code-review` skill (`blind`, `edge`, `acceptance`, `security`, `architecture`, `codebase`, `tests`).

## Required mechanics
Read `/Users/moses/code/.agents/skills/code-review/SKILL.md` completely and follow its Headless / Automated Mode verbatim. The skill owns the exact lens prompts, JSON contract, blind isolation, chunking, pane grid, `--cwd` rooting, one retry for missing/invalid JSON, mandatory code re-verification, deduplication, triage, and `consolidated.json`. The acceptance lens is active because the original briefing is the spec. The user has selected no interactive fix flow: this is review only.

For each chunk, use:
- `diff_file`: the exact chunk file above
- `worktree`: this detached worktree
- `spec_files`: `/Users/moses/code/_bmad-output/briefings/orchestrator-selected-safety-fixes-2026-09-12.md`
- `out_dir`: a chunk-specific directory under the round output, such as `chunk-1` and `chunk-2`
- no `prior_findings` for r1

Use dedicated lens tabs in workspace `w85`, explicitly rooted with `--cwd` at the detached worktree, no more than six lens panes per tab, and build each grid at creation (never a split ladder). Close every lens pane after its wave. Keep all source reads in the detached worktree at the reviewed SHA. Do not use GitHub diff retrieval in place of the saved canonical bytes.

After both waves, perform the skill's full verification/consolidation against the detached worktree and write the round-level `/Users/moses/code/_bmad-output/perkins/orchestrator-selected-safety-fixes/r1/consolidated.json` and report/body artifacts. Re-fetch the PR head before posting; if it moved, disclose old versus new SHA and do not pretend the review is current.

## Posting and closeout
Post the resulting verdict to PR #33 as the `perkins-review` app using `/Users/moses/code/bin/perkins-token --owner mssoka` and the exact fallback-comment rules in the playbook annex. Never let an empty token fall through to ambient `mssoka` approval. If the app token is unavailable, use the required fallback comment and disclose it; do not fake a formal approval.

The round's verdict is informational for Silas' loop: 0 blockers requests an approval; 1–3 requests changes; 4+ requests changes with MAJOR REWORK; failed lens plus zero findings is a comment/degraded guard, never approval. Do not fix findings. Self-report the round row `orchestrator-selected-safety-fixes-perkins-r1` as working at start and finish with verdict, review URL or fallback-comment URL, and counts. Silas owns the ledger closeout and merge gate.

## Safety boundaries
No live sensor/extension tick, live ledger mutation beyond this round's self-report, real process manipulation, native Godot/Blender work, deployment, root checkout mutation, or changes to PP3D, Selva, the audit, or the implementing worktree. The detached review worktree is disposable only after Silas verifies and sweeps the round's own panes/worktree; do not remove it yourself.

## Dispatch parameters
- job_id: `orchestrator-selected-safety-fixes-perkins-r1`
- parent: `orchestrator-selected-safety-fixes`
- repo: `my-orchestrator`
- repo_root: `/Users/moses/code`
- base: `main`
- model: `zai-coding-cn/glm-5.3`
- thinking: `max`
- review_model: `zai-coding-cn/glm-5.3`
- review_thinking: `max`
- pr_review: `0` (this is the review round row; parent carries `pr_review=1`)
