---
title: 'Selected orchestration safety fixes (R01–R04, N04/N05/N07/N08, N10)'
type: 'bugfix'
created: '2026-09-12'
status: 'done'
route: 'dispatch'
baseline_commit: 'd194d9f7'
review_loop_iteration: 0
context:
  - '{project-root}/docs/orchestration-playbook.md'
  - '{project-root}/AGENTS.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The 2026-09-12 readiness/Nefario audit (0bdfcf8c, byte-identical at current origin/main for both target files) proved nine selected defects: `bin/check-pr-ready` returns false READY on failing/pending/unknown CI, stale-head approvals, substring lookalike Perkins actors, and broken repo-identity parsing (R01–R04); `nefario-watch.ts` converts Herdr tool failure into false pane deaths (N04), reads a GitHub-status field absent from its endpoint (N05), passes debris paths through shell expansion (N07), and can recommend sweeping an active round's worktree (N08); N10 (Luna/xhigh disk pins) is already fixed upstream at `5b30440f` and needs verification + safe-deployment closure, not another patch.

**Approach:** One cohesive PR, coherent commits by packet (A readiness / B sensor safety / C N10 closure). A: split `bin/check-pr-ready` into a stdlib pure evaluator (`bin/pr_ready_core.py`) plus a bounded collector/CLI that binds PR identity, CI evidence, review verdicts and head SHA; head re-read before READY. B: four narrow sensor patches (typed Herdr inventory, summary.json schema+multi-incident classification, fs.statSync path checks, fail-closed ownership + live-owner exemption on every debris branch) plus the two narrow R02/R04 sensor surfaces (APPROVED = observation not merge verdict; bare-number PR identity explicit-or-skip). C: verify upstream N10 fix with evidence, add no duplicate commits, carry rollout/handoff note.

## Boundaries & Constraints

**Always:**
- Model policy for this lane: every parent/helper/reviewer/lens surface `zai-coding-cn/glm-5.3` @ `max`; no Astra fallback; no model flips.
- Preserve audit artifacts and the user-ended review untouched; read-only use of the audit dir.
- Inert/local verification only: no live sensor ticks, watcher reloads, probes, process signals, live ledger mutations, native/editor/Godot/Blender runs, real GitHub mutations. Tests use fakes + local scratch temp dirs; default-deny external calls.
- Exit compatibility: 0 = READY (qualified-ready stays 0 with explicit qualification banner), 1 = NOT READY (blockers), 2 = UNKNOWN/tool error — documented in `--help`.
- Current behaviors that are correct stay: same-reviewer CR→APPROVED clears veto; per-reviewer latest-stance; pr_review=0 ordinary-review route; NEUTRAL/SKIPPED checks pass; all-reported-failing-check policy (not required-only); detection-only cleanup (never auto-close/remove/kill); exact-cwd debris matching; successful-empty Herdr inventory detection; bounded calls + useful dedup.
- Fresh worktree from origin/main only; live root at `0bdfcf8c` never touched.
- PR body separates: fix implemented/tested in worktree / merged / active in live orchestration; nine-ID closure matrix (newly fixed / already-upstream-with-proof `5b30440f` / deployment-pending); safe Silas rollout note (aside copy of `.agents/skills` before any root integration per PR #28 trap; retain local `0bdfcf8c` root-config fix; controlled activation at ops-safe checkpoint — NOT implemented by this job).

**Never:**
- Unselected findings (R05, R06, N01, N02, N03, N06, N09, N11, N12): no outbox/ACK/schema overhaul, no scheduling/liveness/probe rewrite, no new model policy, no local-CI/fallback waiver format, no GitHub merge enforcement, no unrelated cleanup, no silent policy broadening (no optional/billing exceptions).
- No substring actor matching, no promotion of the audit's refuted synthetic-dismissal shape, no shell eval of paths/CLI overrides, no ambient-repo bare-number lookups.
- No edits to production assets/skills/journals/AGENTS.md beyond the narrow surfaces named; no live root pull/reset/rebase/clean; no revival of the ended Lavish review.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| StatusContext FAILURE/ERROR | rollup item state=FAILURE | NOT_READY `CI_FAILED` | — |
| CheckRun pending, no flag | status=IN_PROGRESS | NOT_READY `CI_PENDING` | — |
| CheckRun pending, --allow-pending | same flag given | exit 0 READY-qualified banner naming pending checks; never says CI green | — |
| ACTION_REQUIRED / STARTUP_FAILURE / STALE / unknown conclusion | completed non-success | NOT_READY `CI_FAILED`/`CI_UNKNOWN` | — |
| Missing/unknown rollup evidence | field absent or empty without established no-gates | UNKNOWN, actual gap reported | exit 2 |
| No gates positively established | protection query OK, no required checks, empty rollup | pass (not a failure) | — |
| Approval at older head | review.commit.oid != headRefOid | NOT_READY `REVIEW_STALE` | — |
| Head moves between calls | re-read differs | UNKNOWN/`STALE`, never READY | exit 2 |
| pr_review=1 or --require-perkins, human approves | login != `perkins-review[bot]` exact | NOT_READY `REVIEWER_MISMATCH` | — |
| Substring impostor | login `not-perkins-bot` | NOT_READY `REVIEWER_MISMATCH` | — |
| Missing review author | login null | not counted as approval | reason reported |
| Sparse PR JSON | mergeable/isDraft/state missing | UNKNOWN `EVIDENCE_MISSING` | exit 2 |
| URL vs remote/ledger identity conflict | owner/repo disagree | NOT_READY/UNKNOWN `IDENTITY_MISMATCH` | exit 2 |
| Bare number + resolvable slug | repo_root remote or full-slug repo col | explicit `--repo owner/repo` | unresolvable → exit 2 |
| https/git@/ssh remote forms | origin URL | correct owner/repo | invalid → None |
| GH/LEDGER_BIN env + --ledger | documented overrides | honored, flag > env > default | missing binary → exit 2 reason |
| gh timeout / non-JSON / bad schema | tool failure | `TOOL_ERROR` with reason code | exit 2, no traceback |
| N04: herdr nonzero/garbage | tool failure | skip state diff; one rate-limited health event; no gone/recovery synthesis | — |
| N04: successful empty inventory | zero agents | real disappearance semantics preserved | — |
| N05: documented status payload | summary.json, indicator=major | incident advisory fires (any of multiple incidents listed) | invalid schema → skip, NOT recovery |
| N05: partial recovery | one of two incidents resolves | new key → updated advisory; full recovery → evidence-based clear (no git-green claim) | — |
| N07: `$(…)`, backticks, quotes, spaces, newlines in paths | malicious/odd paths | literal fs.stat bytes; zero bash invocations for existence; no execution | unexpected root → invalid, never cleanup instruction |
| N08: done old row + live new row same cwd | shared worktree | no sweep candidate (live-owner exemption on done branch too) | — |
| N08: live-row/registered query fails | tool error | no candidates, health warning (fail closed) | — |
| N08: real unowned debris | done, dir exists, no live owner | detection-only candidate still surfaces | — |

</frozen-after-approval>

## Code Map

- `bin/check-pr-ready` — A target. Python CLI ~200 lines: `run/gh_json/git_owner_repo/main`. Defect sites: rollup loop reads only conclusion/status (never StatusContext.state), pending only warns, ACTION_REQUIRED passes; no headRefOid/review commit/reviewDecision; `"perkins" in login` substring + `"?"` fallback; `git_owner_repo` double-rsplit collapses to repo segment → None; literal `gh` ignores documented `GH` env; `run()` unbounded; sparse JSON passes.
- `bin/pr_ready_core.py` — NEW pure evaluator (stdlib only, no subprocess/env): identity resolution (remote/URL/slug parse + conflict detection), rollup classification, review stance + head binding + actor policy, PR-state validation, verdict→(status, reason codes, human lines). Reusable + unit-testable.
- `.pi/extensions/nefario-watch.ts` — B target + two A surfaces. `liveStatuses()` (~216-229) + `tick()` diff loop (N04); GitHub-status block in `prTick` (~982-1020, N05: status.json + `incidents[0]`); `roundDebrisCheck` existence script (~452-463 N07; 413-436 livePaths only on orphan branch, liveQ/registered failures fail open, N08); `REVIEW_ACTIONS.APPROVED` (~168-171, R02 wording); `prInfo`/`reviewUrls`/`inReviewJobs` (bare-number `gh pr view` without `--repo`, R04 sensor side). Extension runs in-process; `node:fs` built-in imports are documented-available (pi docs/extensions.md "Available Imports").
- `bin/perkins-token` — read-only contract source: Perkins posts as the `perkins-review` GitHub App → canonical review author login `perkins-review[bot]` (exact-match only).
- `.pi/extensions/silas.ts:72`, `bin/night-watchman:104-120`, `bin/test-model-policy:34-45`, `docs/orchestration-playbook.md:276,893-898` — N10 surfaces, all xhigh at origin/main via `5b30440f` (verified ancestor). No code change unless a gap is proven.
- `test/nefario-watch-conflict.test.ts` — existing harness pattern: imports REAL extension via `node --experimental-strip-types`, FakePi boundary; must stay green (conflict/merge/CI/review/Perkins dedup unregressed). Fake `curl` returns `{status, incidents:[]}` — keep compatible with N05 parser.
- `test/test_bmad_renderer_short_config.py` — Python test convention (standalone unittest, run via `uv run --python 3.11 test/...` or python3).
- Audit dir (READ-ONLY): `/Users/moses/code/_bmad-output/implementation-artifacts/orchestrator-nefario-pr-readiness-audit-20260912/` — `AUDIT.md` (finding details + regression acceptance per ID), `fixtures/readiness.json` (85-case matrix with exact gh JSON shapes: CheckRun `{__typename,name,status,conclusion}`, StatusContext `{__typename,context,state}`, review `{id,state,author.login,submittedAt,commit.oid}`, view adds `headRefOid`), `harness/readiness.py`+`nefario.cjs` (fake-boundary patterns to adapt), `FOLLOW-UP.md` (packet A/B/C boundaries).
- Node strip-types constraint (field notes): no TS ctor parameter properties / non-erasable enums in extension edits; keep erasable syntax only; parse-test after edits.

## Tasks & Acceptance

**Execution:**
- [x] `bin/pr_ready_core.py` — NEW pure evaluator module with the R01–R04 semantics above — single source of decision truth, testable without subprocesses.
- [x] `bin/check-pr-ready` — rewrite as bounded collector (timeouts, GH/LEDGER_BIN/--ledger precedence, schema validation, head re-read before READY) calling the evaluator; update `--help`/docstring for exits + qualified output — packet A.
- [x] `.pi/extensions/nefario-watch.ts` — N04 typed inventory union + rate-limited health event; N05 summary.json endpoint + schema validation + multi-incident/partial-recovery keys + evidence-based clear; N07 fs.statSync existence (no shell) + meaningful-root validation; N08 fail-closed ownership queries + live-owner exemption on every debris branch; R02 APPROVED wording (observation + verify-before-merge, never "merge when ready" on disagreeing evidence); R04 bare-number explicit-slug-or-skip in PR sensing — packet B.
- [x] `test/test_check_pr_ready.py` — NEW regression suite: port the audit's 85-case fixture matrix as explicit updated expectations against the REAL CLI (fake ledger/gh/git boundary like audit `harness/readiness.py`), positive controls kept; RED on old code proven for selected classes.
- [x] `test/nefario-sensor-safety.test.ts` — NEW sensor suite (real extension, FakePi + real fs on temp dirs): N04/N05/N07/N08 + APPROVED wording + bare-number identity; existing `nefario-watch-conflict.test.ts` must stay green unmodified.
- [x] `bin/test-model-policy` — run + verify all N10 pins xhigh; strengthen ONLY if a real gap is found (no no-op commits) — packet C.
- [x] Mutation legs (documented results in PR body): ignore StatusContext state; drop head match; exact-actor→substring; inventory-error→empty-map; restore shell interpolation; omit one active-owner branch; xhigh→max — each must flip the relevant suite RED.

**Acceptance Criteria:**
- Given the audit fixture matrix, when run against the new CLI, then every selected-defect case returns NOT_READY/UNKNOWN per the I/O matrix and every preserved-correct control (baseline, same-reviewer CR→APPROVED, mixed-reviewers veto, pr-MERGED, NEUTRAL/SKIPPED, no-gates-established) stays correct.
- Given old code checked out, when the new suites run, then at least the selected-defect classes fail (RED) — proving the suites bite; new code GREEN.
- Given a path containing `$(printf INERT)`/backticks/newlines, when the debris sensor samples it, then zero bash processes are spawned for existence and the bytes stay literal.
- Given a Herdr nonzero exit, when the pane tick runs, then no job transitions to gone and one rate-limited health event fires; successful-empty inventory still yields real disappearance.
- Given `5b30440f` evidence + fresh-main verification, when the PR opens, then N10 is credited already-upstream with commit + test proof and marked deployment-pending for the live root (rollout note included; no live activation from this job).
- Given the full suite, when run twice consecutively, then results are identical (no flaky state).


## Implementation Notes

Planning decisions (mine, per commission): qualified-ready (--allow-pending) keeps exit 0 with an explicit qualification banner; required-gates establishment queries branch protection via gh api and treats inability as conservative UNKNOWN with the actual gap reported; review approval counts only when bound to the exact current headRefOid; pr_review parsing treats non-integer as UNKNOWN (exit 2) not crash. Step-02 gates: no open questions (commission pre-answers them); spec exceeds 1600 tokens — user pre-ruled one cohesive PR ("Keep all goals" equivalent); CHECKPOINT 1 pre-approved per orchestration standing orders (explicit commission, no proposal gate).

## Spec Change Log

## Review Triage Log

Review 2026-09-12, layers: blind (15 findings, glm-5.3/max), edge-case (14), verification-gap (3 verified + 2 other). Every finding verified against the code (contested claims re-executed) before verdict.

| # | Finding (layer) | Verdict | Evidence & route |
|---|---|---|---|
| 1 | `--allow-pending` + pending REQUIRED gate → NOT_READY + qualified=True contradiction (blind+edge, executed) | high → patch | Reproduced via evaluator: NOT_READY/EVIDENCE_MISSING despite the frozen matrix's exit-0-qualified row. FIXED: required-gate pending under the flag = tolerated QUALIFIED (warn, exit 0); test `test_allow_pending_required_gate_qualified`. |
| 2 | `--help` never shows exit codes (blind) | medium → patch | argparse had no epilog; description pointed at itself. FIXED: EXIT_EPILOG + RawDescriptionHelpFormatter. |
| 3 | Orphan-pane branch turns N07-skipped paths into cleanup instructions (blind+edge) | high → patch | `exists.get(cwd) ?? false` read skipped/relative cwds as REMOVED. FIXED: `meaningfulPath` guard in the orphan loop; tests orph-a/orph-b. |
| 4 | N05 partial-malformed incident entries → false CLEARED (blind+edge) | high → patch | Filter dropped bad entries → `incidents.length===0` + good indicator = clear. FIXED: filter-count mismatch = invalid sample, skip tick. |
| 5 | Conflict-test curl fake schema-invalid under new parser, green by accident (blind) | low → reject | Observable behavior (baseline silence) preserved via the invalid-skip path; clear-path covered by sensor suite n05e; spec pins the file unmodified — editing it is scope creep. |
| 6 | sensorHealthNote rate-limits per kind, hiding subjects 2..N (blind+verif-other) | medium → patch | FIXED: bare-pr-identity aggregates ALL affected job ids into the one rate-limited note. |
| 7 | DEBRIS recipe interpolates raw paths into a copy-paste shell line (blind) | medium → patch | FIXED: shell-quote helper (single-quote escaping) on repoRoot/wt in the relayed recipe. |
| 8 | In-review fallback query discards `repo` for all rows (blind) | low → reject | Degradation is the SAFE direction (skip + health note, never ambient lookup); rare schema-drift-only; the fix (column probing) is more than a direct correction. |
| 9 | Pre-READY re-read laxer than first read: no-rollup/null-mergeable/pending-flip pass (blind+edge+verif-other) | high → patch | FIXED: same evidence standard on the re-read (rollup present+non-null, mergeable not null/UNKNOWN, pending appearance without flag → UNKNOWN). |
| 10 | EVIDENCE_MISSING spans both exit classes (blind) | low → patch | FIXED: contract docstring states the dual role explicitly; consumers key on verdict/exit. |
| 11 | Bare number + non-github remote → silent github.com coercion (blind, executed) | high → patch | Reproduced: ghe.corp remote + matching ledger slug resolved with zero problems. FIXED: non-github remote host on a bare number → IDENTITY_MISMATCH refusal; test. |
| 12 | test-model-policy absent-file skip is vacuous pass + skips the tracked-surface GLM grep (blind+edge+verif, live-demo) | high → patch | Verif layer demonstrated FALLBACK_MODEL=glm-5.3-flash passing. FIXED: `! grep legacy-GLM bin/vision-read` unconditional; SKIP labels distinct from PASS. |
| 13 | Dead `if False else` cruft in test (blind) | low → patch | FIXED: removed. |
| 14 | Playbook:413 stale gate description (blind) | medium → patch | FIXED: line updated to the new contract (exit semantics, exact actor, head binding). |
| 15 | Coverage gaps: orphan branch, debris-pane-inventory failure, non-github bare number (blind) | medium → patch | FIXED: orph-a/orph-b + v1/v1b + bare-number-non-github tests added. establish_required_checks-ToolError covered by the required=None UNKNOWN path (test_no_checks_gates_unreadable_unknown). |
| 16 | Reviews non-object entry → AttributeError traceback (edge) | high → patch | Reproduced AttributeError in sorted(). FIXED: all-dict schema guard + defensive sort key; test. |
| 17 | mergeable unrecognized type passes → READY (edge, executed) | medium → patch | Reproduced READY with mergeable=7. FIXED: unrecognized value → EVIDENCE_MISSING unknown; test. |
| 18 | statusCheckRollup JSON-null treated as no checks (edge, executed) | medium → patch | Reproduced READY with null rollup. FIXED: absent-or-null → unknown; test. |
| 19 | Invalid UTF-8 tool output → uncaught UnicodeDecodeError (edge) | low → patch | except-list gap verified by inspection. FIXED: ToolError conversion. |
| 20 | Malformed-but-parseable herdr inventory (agents non-array) → ok:true empty map → false gone (edge) | high → patch | N04 re-entry class. FIXED: Array.isArray guard → ok:false. |
| 21 | Agents-failure during roundDebrisCheck → DEBRIS alert without pane knowledge (edge) | low → patch | Row evidence (dir+registered+done) stands; FIXED: alert annotates "pane inventory UNAVAILABLE this tick". |
| 22 | Clock-step-backward suppresses health notes (edge) | low → patch | FIXED: negative elapsed re-arms the limiter. |
| 23 | statSync unbounded on stalled/automounted fs (edge) | low → defer | Real trade-off: N07 required removing the shell path; a bounded stat needs async infra (fs.promises + race) beyond a direct correction — pre-existing in-process sync-fs exposure class. deferred-work.md. |
| 24 | Missing test: prTick inventory failure kills ALL PR-tick alerting (verif, pre-verified) | high → patch | Mutation shipped green. FIXED: v1/v1b test (co-present MERGED alert + health note under herdrAgents failure). |
| 25 | Missing test: bare-number reviews-api path transposition invisible (verif, pre-verified) | medium → patch | FIXED: r04d execLog assertion on repos/acme/demo/pulls/7/reviews. |

Post-patch verification (all on the patched tree): python 80/80 OK, sensor 16/16 ALL PASS, conflict 8/8 unmodified-green, bin/test-model-policy ALL PASS (16 PASS/SKIP lines), py_compile clean. RED-on-old + 7/7 mutation legs re-verified earlier (pre-patch); patched behaviors carry their own new red-capable tests.

## Design Notes

Evaluator returns `(verdict, reasons[], lines[])`; verdict ∈ {READY, NOT_READY, UNKNOWN}; reason codes: CI_FAILED, CI_PENDING, CI_UNKNOWN, REVIEW_STALE, REVIEW_REQUIRED, REVIEWER_MISMATCH, EVIDENCE_MISSING, IDENTITY_MISMATCH, TOOL_ERROR, STATE_INVALID, DRAFT, CONFLICTED, plus OK-qualified. Collector maps NOT_READY→1, UNKNOWN→2, READY→0. gh view fields: `state,mergeable,isDraft,reviewDecision,headRefOid,baseRefName,statusCheckRollup,reviews`. Example classification: `{"__typename":"StatusContext","context":"ci","state":"FAILURE"}` → FAIL(CI_FAILED); `{"__typename":"CheckRun","name":"x","status":"COMPLETED","conclusion":"ACTION_REQUIRED"}` → FAIL; `conclusion:"NEUTRAL"` → SKIP (passes). N05 dedup key: `ind:<indicator>|inc:<sorted id:status>`; clear only when key was incident-ish AND new sample valid AND no unresolved incidents AND indicator ∈ {none,good}? — no: indicator minor/major with zero unresolved incidents still advisory-worthy; clear requires indicator good/none AND zero incidents.

## Verification

**Commands:**
- `python3 test/test_check_pr_ready.py` -- all cases pass on new code; on stashed-old code the selected-defect classes fail (RED proof documented in PR body).
- `node --experimental-strip-types test/nefario-sensor-safety.test.ts` -- ALL PASS.
- `node --experimental-strip-types test/nefario-watch-conflict.test.ts` -- ALL PASS (unmodified file, unregressed).
- `bin/test-model-policy` -- PASS (xhigh pins).
- `bash -n bin/check-pr-ready`-equivalent: `python3 -m py_compile bin/check-pr-ready bin/pr_ready_core.py` -- clean.
- Parse gate for extension edits: `node --experimental-strip-types --check`-style load via the conflict test import (strip-types rejects non-erasable syntax at import).

**Manual checks (if no CLI):**
- PR body carries the nine-ID closure matrix + live-vs-reviewed SHA status + Silas rollout note; audit dir untouched (mtime/hash check of AUDIT.md).
