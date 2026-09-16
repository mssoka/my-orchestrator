# IMPLEMENT NOW — selected orchestration safety fixes (GLM5.3/max)

## Authority and model override

User after audit disposition: **"so it's fix. what are we waiting for?"** This is the separate explicit implementation commission. No more proposal/permission gate for the nine selected fixes. Implement, prove, review and open a code PR; do not return another plan as the deliverable.

User's subsequent model direction: **"what model are you planning to use for the orchestration work? I'll suggest glm5.3 at max thinking. we really need astra for 3D youtube and PP work."**

For THIS orchestration-fix lane, parent, any non-3D implementation helpers, built-in review workers and subsequent independent Perkins round/lenses all use **`zai-coding-cn/glm-5.3` at `max`**. This explicit scope override supersedes generic GPT/legacy-retirement defaults. NO Astra fallback; if GLM is unavailable, tell Silas/Gru, do not spend reserved Astra capacity. User did NOT request flipping identity panes or active Selva/PP3D: leave Gru/Silas and those jobs alone. Actual modelId AND thinking-level provenance must be verified.

## One cohesive implementation job, no three-stage proposal bureaucracy

Job `orchestrator-selected-safety-fixes`, new branch/worktree from freshly resolved **origin/main**, repo `/Users/moses/code`, GitHub `mssoka/my-orchestrator`. Root is LIVE/DIRTY and currently on vision-read-skill-cleanup at0bdfcf8caaf5a4f7d559a447b88f7b0bab1c1994; NEVER switch/pull/reset/rebase/clean that checkout. This is code work in an isolated NEW worktree, not mutation/reuse of the sealed detached audit. No need to revive its ended Lavish session or its Astra parent.

Freshness matters: cached origin/main at intake isd194d9f7 (mergePR31). Gru has VERIFIED cached upstream already fixes **N10**: `.pi/extensions/silas.ts` setThinkingLevel(xhigh), watchman SILAS_THINKING=xhigh, matching tests/docs. Live root still has max because its branch diverges. Re-resolve upstream, compare EVERY selected finding with it, and credit existing fixes by exact commit/test evidence rather than recreating them. Distinguish SOURCE FIXED UPSTREAM from LIVE ACTIVATED. N10's real remaining concern may be safe deployment, not another patch. Do not let that block implementing the other selected defects.

One code PR with coherent commits by A(readiness),B(sensor safety),C(policy/test reconciliation if needed) is preferred; these share Nefario/test surfaces, so do not spawn three conflicting feature branches. Existing code review/Perkins applies, pr_review1. User merges. No separate proposal/docs-review gate: **lavish not needed, PR directly** (this is code; incidental focused docs and rollout notes ride it). Do not reopen the ended audit report.

## Exact selected scope

Authoritative audit artifacts:
`/Users/moses/code/_bmad-output/implementation-artifacts/orchestrator-nefario-pr-readiness-audit-20260912/`
Read `AUDIT.md`, `findings.json`, `coverage.json`, `FOLLOW-UP.md`, `feedback.json`, harness README and relevant raw fixtures. Audit source snapshot0bdfcf8c; 148 passing CHARACTERIZATION cases prove current behavior, including bugs, not functional correctness.

**Only nine selected IDs:**
- A: **R01,R02,R03,R04** — readiness correctness/identity/bounds.
- B: **N04,N05,N07,N08** — narrow sensor safety.
- C: **N10** — already-ruled Luna/xhigh consistency, accounting for upstream fixes.

**Excluded:** R05,R06,N01,N02,N03,N06,N09,N11,N12. No durable outbox/ACK/schema overhaul, broad scheduling/liveness/probe rewrite, new model policy, local-CI/fallback waiver format, GitHub merge enforcement or unrelated cleanup. Shared small pure helpers needed for these fixes are allowed; do not smuggle unselected projects into them. Native PP3D/Selva grants remain entirely unaffected.

## Acceptance — implement substantive behavior, not grep-only promises

### A — bin/check-pr-ready (plus the narrow R02 recommendation surface)

1. **R01:** Normalize actual CheckRun and StatusContext schemas, distinguish pass/pending/fail/unknown, and reject unsuccessful/unknown/incomplete required evidence. Legacy FAILURE/ERROR and ACTION_REQUIRED cannot return READY; pending without --allow-pending must be non-ready. With the explicit flag, output must disclose qualification and never say CI is green. Strict PR field/schema validation: sparse/missing mergeability/draft/check evidence is not affirmative proof. Positively established no-configured-gates is not the same as absent required-check evidence.
   - Preserve current all-reported-failing-check policy; do NOT silently choose required-only policy or new optional/billing exceptions (R05 was not selected). Existing sanctioned local/fallback manual paths remain disclosed outside this CLI's unfinished exception support. Use conservative UNKNOWN where collection cannot establish requirements; report the actual gap rather than fabricate a pass.
2. **R02:** Bind canonical PR, current head, checks and reviewer verdict to exact evidence SHA. Request review commit and head; honor applicable aggregate review/protection state and independent vetoes. Re-read/check head/state before returning readiness so modeled A→B movement is STALE/UNKNOWN, never READY. Keep source/base/target provenance explicit where needed. Preserve correct same-reviewer CR→APPROVED behavior, do not promote the audit's refuted synthetic dismissal shape into a requirement.
   - Nefario's APPROVED event must be a review observation, not an unqualified 'merge when ready' recommendation when CI/conflicts/head freshness disagree. Make the narrow wording/provenance correction in scope for R02. Full shared-evaluator enforcement wiring is R06 and NOT selected. No autonomous merge, no claim a CLI can make a later human merge atomic.
3. **R03:** pr_review1 implies the designated Perkins reviewer, not any human. --require-perkins must enforce canonical exact trusted actor/app identity, never a substring. Resolve existing actual canonical actor representations from preserved trustworthy source/API contracts; normalize only documented forms. Missing actor cannot count as approval. Do not infer identity from display names/review-body text or create an exception issuer policy. pr_review0's documented ordinary-review route can remain, but still requires valid actor/current-head evidence.
4. **R04:** One consistent validated host/owner/repo/PR identity across CLI and touched sensor calls. Fix common HTTPS/git@/ssh remote parsing; bare-number handling must use explicit canonical repo and cannot inherit ambient COO repo. Reject ledger/full-URL identity conflict instead of trusting the URL silently. Honor GH and LEDGER_BIN/--ledger precedence as documented. Bound subprocess calls; handle tool errors/timeouts/invalid JSON/schema with useful nonzero/UNKNOWN and reason codes, not uncaught traceback or false success. No shell eval of paths/CLI overrides.

Prefer a small stdlib pure evaluation/normalization module plus collector/CLI wrapper if it simplifies real tests; no dependency/service/framework rewrite. Keep exit compatibility explicit (0 only policy-ready, nonzero not-ready/unknown); document any distinct error exit and new qualified output. Do not solve unselected accepted-evidence policies by broadening or silently waiving them.

### B — .pi/extensions/nefario-watch.ts

5. **N04:** Herdr failure/invalid inventory is UNKNOWN, not a successful empty Map. Do not overwrite last-known pane states or synthesize death/recovery transitions on tool failure. Rate-limited sensor-health/error reporting allowed; preserve successful-empty detection and existing meaningful rearm behavior.
6. **N05:** Use the correct GitHub Status endpoint/schema; validate input and classify actual indicator/incidents/components. Handle multiple active incidents and partial/full recovery without blindly claiming Git is green. Unknown/invalid response is not a recovery. Preserve bounded calls and useful dedup; no broad delivery architecture rewrite.
7. **N07:** Eliminate shell interpretation from debris path checks: fs stat or fixed helper argv, not JSON.stringify-as-bash-quoting. Dollar/backtick/newline/quote/space filenames remain literal; neither command nor parameter expansion may execute. Validate meaningful path roots/ownership without destroying legitimate existing worktree layouts or following a cleanup path through shared preservation assets.
8. **N08:** Apply active-owner exemption to EVERY done-row/orphan branch, not only the latter. Failed/unknown ownership query means no cleanup candidate, not an empty owner set. Exact cwd/generation/ownership evidence remains; recommendations stay detection-only and require fresh operator verification. Real unowned debris must still surface. Never auto-close/remove/kill.

### C — N10 and actual activation

9. Verify freshly fetched main already carries Luna/xhigh in extension/watchman/tests/docs; add or strengthen meaningful tests only where missing, not duplicate no-op commits. Do not alter current healthy Luna/xhigh COO or 3D Astra parents. Ensure no modified launch path regresses to max. No new generalized model-policy project.

The final PR must explicitly separate **fix implemented/tested in worktree**, **merged**, and **active in live orchestration**. The live root diverges from main and carries modified tracked skills/untracked evidence. PR28 skills-untracking can delete canonical skills; an aside copy plus verified preservation is mandatory before any eventual root integration. The local0bdfcf8c root-config fix is user-approved/unmerged and must be retained too. Include a concrete safe rollout/handoff note for Silas (backup source/evidence/skills, reconcile local commit and dirty tree without discarding, verify hashes, then controlled activation/reload at an ops-safe checkpoint). Do NOT implement that live sync/reload from this job and do not invent an unsafe pull/reset workaround. Do not mark N10 LIVE fixed merely because upstream is correct. If deployment needs a further destructive/conflicting decision, disclose it while the code PR still advances.

## Testing, scope safety and review

- Reuse the audit's actual-source inert harnesses; preserve the original audited evidence untouched. Copy appropriate tests into the repo in a maintainable regression suite and point them at the actual changed production code, not only preserved old source. Version updated expectations explicitly: keep positive controls, and prove old code RED→new code GREEN for selected fixes. Mutation legs for critical protections: ignore StatusContext state; remove head match; change actor exact match to substring; map inventory error to empty; restore shell interpolation; omit one active-owner branch; flip xhigh back to max. Each must be caught by relevant semantic tests.
- Establish fresh upstream baseline before changes. Report actual case counts/coverage and gaps; 148 characterization cases are not 148 correctness tests. Upstream-resolved findings need existing commit + relevant test proof, not a recreated defect.
- Unit/inert integration tests and normal host build tooling are authorized. No actual watcher/extension tick, real failed-GitHub/noisy notification/agent manipulation, live ledger mutations, probe/relaunch, process signals, native Godot/Blender or source deployment as tests. Default-deny external calls in mocks, local scratch tempHOME, structured fixture boundaries; no real credential output. Read test scripts before running: watchman full self-test has live effects, so do NOT invoke it blindly.
- Read installed pi README/relevant docs/examples COMPLETELY and follow .md cross-references for extension API/lifecycle usage. Use context7-docs/current authoritative GitHub/gh contracts where needed; don't derive API shape from memory. No paid external service needed.
- No production assets/skills/journals/AGENTS broad edits. Root _bmad/canonical skills must be resolved safely in the fresh worktree for bmad-build; do not repair bootstrap by editing/removing shared files. Canonical renderer script is `/Users/moses/code/_bmad/scripts/render_skill.py`; project config values must refer to this worktree's outputs. Follow the installed skill exactly; if bootstrap genuinely fails, report the exact failure rather than silently bypassing it.
- Complete bmad-build implementation/verification/review, then open focused PR **--base main**. Explicitly set ledger PR URL through Silas/standard exact-row self-report contract, pr_review1 column verified. Code review ALL required lenses per installed skill, model override GLM5.3/max on every reviewer surface; don't handwrite substitutes or claim missing lenses. Formal Perkins loop is operated by Silas, independent of the implementation's built-in review.
- On mssoka the existing perkins-token installation/own-author limitation may require the established full fallback-comment verdict. Disclose it; don't fake formal approval or patch accepted-evidence policy to make this PR pass its own gate. User merge authority and prior permitted review process stay. Do not claim the updated gate is green on an unsupported exception path.
- Hold pushes while any independent round is in flight; fold reviewed blockers locally and push after verdict per normal loop. No live sensor behavior changes until controlled post-merge activation.

## Deliverables / completion

- Working scoped code + regression tests in ONE reviewable PR; coherent A/B/C commits where useful.
- Nine-ID closure matrix: newly fixed, already-upstream with proof, and deployment-pending status, explicitly differentiated. No silently dropped IDs and no broad 'all18 fixed' claim.
- Exact RED→GREEN/mutation results, limitations, compatibility/rollout note and current live-versus-reviewed SHA status. Small focused docs only; **lavish not needed, PR directly**. Audit review remains ended.
- Meaningful first milestone to Silas when real defects close; no paperwork-only completion. Same new job ID throughout. Field-note shard for this job only; do not mutate the audit report/verdict.

## Skills / dispatch parameters

Workflow: **bmad-build** end to end; installed full code-review method for review, relevant pi docs/context7-docs for API work. All orchestration-fix parent/helpers/reviewers **zai-coding-cn/glm-5.3 / max**, user override. No Astra use on this lane. Silas coordinates actual dispatch/review; no new concurrency hold on PP3D/Selva.

- job_id: orchestrator-selected-safety-fixes
- repo: my-orchestrator
- repo_root: /Users/moses/code
- github_repo: mssoka/my-orchestrator
- base: main — fresh origin/main resolved at dispatch, not dirty live root HEAD
- slug: orchestrator-selected-safety-fixes
- branch: fix/orchestrator-selected-safety
- worktree: NEW isolated branch worktree; never root or sealed audit tree
- model: zai-coding-cn/glm-5.3
- thinking: max
- review_model: zai-coding-cn/glm-5.3
- review_thinking: max
- pr_review: 1
- github_issue: none required; user directly commissioned fixes
- blocked_by: none

Silas: dispatch NOW after normal model availability check for THIS approved GLM route (never Astra fallback); verify actual model/thinking/hand-over/progress. Keep audit rowDONE and its ended review intact. This is the implementation commission, not another proposal job. Record future independent reviewer model override durably so no default Astra round/lens gets spawned for it.
