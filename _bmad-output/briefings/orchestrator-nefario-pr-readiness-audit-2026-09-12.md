# Read-only orchestration audit — Nefario sensors and check-pr-ready

## User request / outcome

User: **"look at the current orchestration and see how it can be improved.esp the nefario sensors. are there flaws in the check-pr-ready? do an audit and suggest improvements."**

Deliver an evidence-backed CURRENT-SYSTEM audit and prioritized, implementable recommendations. Answer directly whether check-pr-ready can produce false READY/NOT READY and whether Nefario can lose/duplicate/misroute work. Audit only; do not implement production fixes, open a PR, file issues, dispatch actual jobs/reviews or change live orchestration. Recommendations are requested; no extra permission interview needed to analyze these known surfaces.

## Dispatch / immutable scope

Orchestrator root repo `/Users/moses/code`, remote `https://github.com/mssoka/my-orchestrator`, CURRENT local HEAD **0bdfcf8caaf5a4f7d559a447b88f7b0bab1c1994** as of12:54Z2026-09-12. Source paths bin/, .pi/extensions/, docs/orchestration-playbook.md and docs/playbook-annex.md were clean at intake. The live root as a whole is DIRTY (skills, journals, state, untracked evidence); do not switch/pull/reset it. Root PR28 skills-untracking trap remains: no pull or skills cleanup. No bootstrap by copying/removing .agents/skills.

Silas: create a DETACHED audit worktree at that exact current local HEAD, outside `/Users/moses/code`; do NOT use origin/main instead. Capture a read-only manifest of relevant live source SHA/time and compare with the audit snapshot, to distinguish current disk source, historical baseline and actually-loaded runtime. Preserve discrepancies; no 'current' claim from a stale branch. Root jobs always isolated, never launch another pseudo-Gru in the root.

New row `orchestrator-nefario-pr-readiness-audit`, pr_review0 (no implementation/PR). Parent is an Astra/xhigh reasoning audit lead, not a formal Perkins PR round. Up to TWO non-3D Sol/xhigh specialist helpers for independent bounded source areas; no fabricated full-lens-review claim. Use dedicated audit tab(s), never identity tabs. Explicitly clear inherited PI_GRU/PI_SILAS/PI_MODEL/PI_PROVIDER on audit/helper launches and pin model/thinking/cwd. No observer extension may attach to the live COO role from the audit worktree.

Selva pYR and PP3D pYQ continue independently. This audit imposes NO source/native/GPU hold on them. Silas remains operations owner; audit agents must not intervene in observed jobs.

## Primary code / policy perimeter

- `bin/check-pr-ready` (194L): actual invocation/exit contract, docstring/CLI flags, ledger/GitHub/schema handling, repository/PR identity, review and CI semantics.
- `.pi/extensions/nefario-watch.ts` (1298L): pane30s tick, PR/CI/review/conflict/Perkins/dream/quota/GitHub-status/round-debris/stuck polling and all state/dedup/delivery paths.
- `bin/ledger` (320L), schema/current caller contracts; `.pi/extensions/silas.ts`, `.pi/extensions/gru.ts`; `bin/night-watchman`, `bin/quota-probe`, model-policy helpers/tests, relevant installed/runbook configurations and other actual callers of readiness/sensors.
- `docs/orchestration-playbook.md`, relevant `docs/playbook-annex.md`, root AGENTS gotchas as *hypotheses/history*, not proof. Inspect actual bin/test-* or other tests; don't equate narrative doctrine with executable coverage.
- Read-only coherent ledger snapshot and selected job_events/current sensor state/session evidence as needed to establish real reachability/incidents. Silas may supply a SQLite read-only-connection backup to the audit scratch; do not write the live DB or run a 'read' CLI before checking whether initialization mutates it. Record snapshot timestamp/WAL consistency. Don't expose credentials/unrelated user conversation or bulk personal data in the report.

Current user policy wins over stale docs: OpenAI hold LIFTED; Astra/Sol/Luna ALL xhigh; Silas owns operations; review freshness is exact head/target scoped; billing-blocked GitHub runners alone do not block locally proven reviews/merges; mssoka fallback-comment structural limitation and disclosed user-accepted verdicts exist; detection-only cleanup (no automatic close/delete); no false native/pixel verification or treating old unresolved grants as new authority. Distinguish policy questions from code defects and propose reconciliation rather than inventing a new policy.

## Audit questions — verify, don't assume

### A. check-pr-ready: high-priority decision-table audit

Run isolated fixtures against the actual pinned implementation and reproduce exact exit/output for each confirmed defect. Cover:
- job missing/wrong status/done, pr field absent/bare-number/full URL/malformed/wrong owner/remote SSH/HTTPS, pr_review0/1, --require-perkins, --allow-pending and documented GH/LEDGER_BIN overrides.
- OPEN/draft/conflicting/unknown/missing mergeability; sparse/schema-invalid fields, missing tool, command failures, hung calls, partial/truncated API results.
- Both GitHub CheckRun and StatusContext shapes, all terminal/pending/unknown outcomes, no checks versus required checks, required versus optional checks, neutral/skipped/action-required/stale, canceled/billing-blocked CI, local evidence bound to current head. 'No listed failure' is not automatically 'required gates passed'.
- Approval identity/authenticity, actual exact bot identity versus substring, pr_review1 enforcement, any-human approval, own-account/fallback-comment rules, APPROVED/CHANGES_REQUESTED/DISMISSED/COMMENTED/PENDING transitions, multiple reviewers, duplicate/missing authors/timestamps, stale approvals after head movement, explicit reviewed commit, reviewDecision/branch protection consistency, paginated review history.
- Two-call snapshot races: head/state/check/review changes between observations, repo/PR confusion, exact source/head binding and TOCTOU before recommendation. A readiness check cannot make a future user merge atomic; disclose residual boundary and recheck/expected-head proposals.
- Is this really an enforced merge/close-out gate, or just an optional CLI that prose tells an agent to call? Trace all actual callers and commands that can bypass it. Separate pre-merge readiness from post-merge housekeeping: an OPEN-only gate should not accidentally obstruct cleanup of an already merged PR.

Quick-read leads from Gru, UNCONFIRMED until fixture-tested/refuted: pending checks appear warn-only even without --allow-pending; helper appears to discard remote owner while parsing; reviews request has no head binding; documented GH override may be ignored; pr_review1 may not force trusted Perkins approval; reviewDecision is fetched but apparently unused. Do not stop at these or inflate one mechanism into many findings.

### B. Nefario: liveness, safety, delivery and restart semantics

Produce a complete sensor inventory: cadence/trigger, input/state scope, persistence, alert recipient, wake mode, dedup key, retry/expiry/recovery and blind spots. Trace:
- Cold-start baselining versus catching already-actionable reviews/merges/CI/stuck jobs; dropped events while COO offline; in-memory versus durable dedup after reload/restart; overlapping/slow ticks and first-sample errors; timezone/clock/counter handling; serial GitHub calls starving other sensors.
- CI/review/head association, API paging/errors/throttles/outages, missing/unknown statuses, wrong repo/URL patterns, shell/SQL interpolation, untrusted review content entering an agent, auth/enterprise assumptions. No live injection proof; fakes only.
- Mark-as-seen timing versus actual alert dispatch/queue/recipient availability/ack. Delivery is not merely a successful typing API call. Burst batching, useful milestones versus receipt spam, queued-not-lost relays, repeat-until-acted semantics and cooldown without permanent suppression.
- pr_review/parent/note/fullSHA/status data contract; sensor round dedup versus actual stale target/new target/held/moot/rebased/done round; cap-era policy remnants and fallback-comment recognition; approval alerts that tell user to merge without invoking equivalent freshness gate.
- blocked/done/clarifying/paneless/no-PR jobs, source work under native holds, completed no-PR artifacts, stopped-but-LIVE versus dead/wedged pi, W3 main-idle/lenses-working, interactive Lavish polls and explicit user-review holds. Sensor output must not authorize an automatic continue/retry/cleanup.
- PID/cwd/session pointer lifetime, stale registry versus real JSONL, mtime-only false signals, shared cwd/helper sessions, orphan cleanup's exact ownership, detached user shells and preserved source dependencies. Detection-only laws retained.
- Watchman outside-pi liveness and shared failure domains; absent/unloaded/broken watcher should be visible. Model/probe helper side effects, stale hold/config drift and limits of proving loaded code equals current on-disk file.

### C. Improvement design / regression protection

Prioritize small corrective changes before architecture rewrites. Compare shared pure readiness evaluator + thin CLI/sensor adapters, typed/structured reason codes and evidence freshness, durable event/outbox + acknowledgement/reconciliation, explicit job PR/round/hold schemas, periodic catch-up independent of edge events, bounded timeouts/backoff and per-sensor health. Recommend only what the observed problems justify; SQLite transactions may be better than a new service. Keep human merge authority and detection-only cleanup.

For every fix proposal name acceptance tests that would fail on the current defect, expected operational behavior, rollout/migration/backward compatibility and failure-mode risks. Include a small NOW/NEXT/LATER sequence and decisions needing the user (particularly local-CI/fallback verdict policy), with effort/dependency estimates not invented precision.

## Safe verification / evidence bar

- Production files/DB/sensors/panes/apps are READ-ONLY. No live extension reload, tick invocation, night-watchman/quota-probe execution, notifications to real agents, job mutations, review posting, merge, process signals or cleanup. No Godot/Blender/native scene operation.
- Put repro harnesses and fixtures ONLY in the isolated audit scratch. Inspect test entrypoints first. Fully fake subprocess/gh/git/sqlite/herdr/clock/timer/FS/network paths before executing the target; default-deny unexpected external actions. Avoid reading live credentials or importing an extension with hardcoded real effects. A fixture must not accidentally mutate the live ledger merely because a path is absolute.
- Prefer actual-source execution with injected/mocked boundaries, not a reimplemented approximation. If tests require in-memory extraction/instrumentation, preserve the transformation and explain limits; independent static source verification of tested code required. A passing original self-test is not proof a mutant/repro is impossible.
- Verify installed pi SDK/runtime semantics from local README/docs/examples where relevant. This is a pi-extension audit: read relevant .md files COMPLETELY (follow extension/lifecycle/message docs cross-references), not training assumptions. Paths: `/Users/moses/.local/share/fnm/node-versions/v22.22.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/{README.md,docs/,examples/}`. For GitHub/gh schema claims use installed help/captured responses and current authoritative docs as needed; load context7-docs when querying named SDK/CLI APIs. Web/documentation sources require URLs in report and Sources section. Don't run quota probes as audit tests.
- Findings classified CONFIRMED (source + deterministic repro or direct observation), DEDUCED (explicit chain), HYPOTHESIZED (missing evidence). Attempt to disprove each important candidate. Severity/impact distinct from confidence. Cite path:line at pinned SHA; include exact repro, expected/actual result, affected lifecycle, smallest fix and test. Distinguish hypothetical reachability from proven historical incident. Record rejected leads separately, not as blockers.
- Stop scope expansion beyond the orchestrator boundaries; flag cross-repo findings without editing. Avoid an unbounded forensic dump of all historical sessions. Ask only a concrete blocking question; don't make the user re-authorize this already commissioned audit one stage at a time.

## Deliverables / review handoff

Under `/Users/moses/code/_bmad-output/implementation-artifacts/orchestrator-nefario-pr-readiness-audit-20260912/` preserve BEFORE any worktree cleanup:
1. `AUDIT.md`: concise executive answer, prioritized findings, sensor/decision tables, coverage and uncertainty, evidence-backed NOW/NEXT/LATER proposals.
2. `findings.json`, `coverage.json`, source/runtime snapshot manifest; reproducible inert harness/fixtures and raw results with actual counts. Findings and report usable without the original session/worktree.
3. New rich Lavish report: clearly label current versus proposed flows, critical false-ready/missed-work examples, ranked remedies, user decisions. Use project visual language (docs/orchestration-explained.html/design assets if appropriate), relevant lavish playbooks; do not publish externally. Deliver final ready-to-read findings to Gru/Silas BEFORE entering the sole foreground poll, then start/verify the owning parent's foreground poll. No report PR needed. Never reopen an ended session or leave only a page server with no owner poll.

First relay when a high-impact defect is genuinely proved; final report must not wait indefinitely for browser feedback before Gru gets its substantive conclusions. Notify completion/readiness with actual shown:true and relay through Silas; checklist proof, not prose claim. While user is reviewing, row clarifying (or explicit review-await state) not abandoned/done-and-unwatched. No user-facing hash/receipt flood. After feedback, update audit only; production fixes require a new user decision. No PR/issue creation in this job.

## Skills / model policy

Use `gds-investigate` evidence grading/stronghold/refutation/source-trace methodology for this commissioned area audit; the briefing fixes scope and authorizes investigation through report, so do not start an unrelated interactive interview or implementation workflow. `lavish` owns the final report/feedback loop. Helpers use the same evidence discipline and return structured JSON with citations; they don't run another orchestrator/review fleet. This is not a seven-lens formal Perkins verdict and must not be represented as one.

- Lead: `openai-codex/gpt-6-astra` / xhigh, reasoning audit role.
- Up to TWO non-3D specialist helpers: `openai-codex/gpt-5.6-sol` / xhigh; suggested division Nefario state/delivery and watchman/ledger/runtime integration while parent owns check-pr-ready/repro/triage. Zero helpers is fine if direct evidence scope is manageable; no partial-lens claims.
- Explicit model/thinking/cwd/env pin and session verification per launch; no stale max/legacy fallback or identity flags. Silas handles dispatch-time liveness gate, not the audit harness.

## Dispatch parameters

- job_id: orchestrator-nefario-pr-readiness-audit
- repo: my-orchestrator
- repo_root: /Users/moses/code
- github_repo: mssoka/my-orchestrator
- base: current local HEAD0bdfcf8caaf5a4f7d559a447b88f7b0bab1c1994 (audit snapshot, not origin/main)
- slug: orchestrator-nefario-pr-readiness-audit
- worktree: NEW DETACHED outside live root at exact SHA
- model: openai-codex/gpt-6-astra
- thinking: xhigh
- pr_review: 0
- github_issue: none
- blocked_by: none
- outputs: local audit + inert repros + Lavish, no code/doc PR

Silas: dispatch and verify real source work. Preserve existing jobs/user terminals; no live mutations from audit tools. Report pane id and meaningful audit findings to Gru.
