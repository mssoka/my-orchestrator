## 🤖 Perkins automated review — round 1
**Job:** righttenantry-agents-prod-scale-to-zero · **Reviewed sha:** 1ab67ba · **Reviewers:** 7/7 completed
**Verification:** 13/16 findings confirmed against the code — 2 discarded as false-positive, 1 kept as [unverified]

**Scope & focus audit (clean):** the diff is exactly the scoped change — 1 file, 2 value lines + comment in `vars/production.tfvars`; `cpu = 2` / `memory = 4Gi` / `max_instances = 20` untouched; SAs remain empty (by design); `variables.tf` defaults and staging untouched. Acceptance #2 re-verified on this tree: `fmt -check` exit 0, `init -backend=false` ok, `validate` → Success. Acceptance #3 claim verified TRUE: `deploy-to-prod.yml` paths exclude `deployment/**`, triggers are `workflow_dispatch` + push to `main` only, and no workflow runs terraform — **merge ≠ prod change; `make tf-apply-prod` lands it.**

### Blockers (2)

**1. `test_min_instances` pins `min_instances == 1` — unit suite is red at this sha** [edge, codebase, tests]
`tests/unit/test_concurrency.py:38-43` — the diff flips the exact invariant this test encodes, without updating it. Re-ran the suite myself: `1 failed, 2050 passed` (`assert 0 == 1`). CI won't catch it on this PR (pr-checks targets `main`/`staging` and its paths exclude `deployment/**`), so it detonates on the next unrelated PR. Fix: assert `0`, rewrite the test's warm-instance comment to the scale-to-zero rationale + tripwire — and mind the regex hazard in Warning 2 while in there.

**2. Advisory test gate: FAIL** [tests]
P0 (`min_instances` pin): broken, 0%. P1 (`cpu_idle`): 0% coverage. Overall 0/2. Below every threshold — fixed entirely by Blocker 1 + Warning 1.

### Warnings (4)

**1. `cpu_idle = true` is the only unpinned prod sizing value** [tests]
`test_max_instances` / `test_resources` pin cpu/memory/max; no test references `cpu_idle` (grep-verified). Drift — including the planned tripwire flip-back — would go unnoticed. Add `test_cpu_idle` asserting `true` alongside the existing pins.

**2. Regex false-pass hazard: the new comment is matched *before* the assignment** [tests]
`_extract_literal_int` uses `re.search` (first match in file order); the line-12 comment `scale-to-zero (min_instances = 0)` precedes the assignment. Mechanically verified: with the assignment flipped back to `1`, the helper still extracts `0` from the comment — a tripwire revert could ship with the test falsely green. Fix the helper (skip `#` lines or anchor to line starts).

**3. Cold-start path: measured 27.7s boot vs the ~42s claimed runway, no `startup_cpu_boost`, no alerting** [edge]
27.7s one-time session-create cold start is on record (`tests/load_test/baselines/2026-04-18-phase2-vertex-sessions/README.md`), leaving ~14s margin; the 2026-05-04 scar (variables.tf) is exactly this budget being burned under the old retry config. The trade-off is user-accepted (2026-09-04) and both hardening options are outside this PR's scope guard — but track `startup_cpu_boost` / a `session_create` alert as follow-up before the first paying customer.

**4. Terraform-only PRs run zero CI** [tests]
Both workflows' path filters omit `deployment/terraform/**`; fmt/validate are manual-only (Makefile: "config changes require a manual `terraform apply`"). Follow-up PR: add `deployment/terraform/**` to pr-checks paths + a `fmt -check`/`validate` step.

### Notes (5)

**1. [unverified] `~42s runway` arithmetic is ambiguous** [blind] — 3 *total* attempts see only 2+8=10s of backoff; 42s requires all three gaps (initial + 3 retries). Consistent only under the retries reading; the policy lives in the external Gleam backend, unverifiable here. Wording mirrors staging's merged comment and the job spec. Confirm the real policy and phrase to remove ambiguity.

**2. The 2026-05-04 citation is the burn record, not absorption evidence** [architecture] — variables.tf documents the retry budget being *exhausted* at min=0 (old config). The absorption evidence is staging's live scale-to-zero record (#152, merged) plus 27.7s < 42s. Wording precision only — staging's comment shares the structure.

**3. Tripwire is comment-only** [blind] — verified: no monitoring/alerting resources exist in the terraform. Spec-compliant as written, but "first paying customer" as a revert trigger relies on human memory; a tracked ticket or alert would make it real.

**4. Merge is inert — confirmed** [edge, codebase] — verified directly in `deploy-to-prod.yml`: this reaches prod only via manual `make tf-apply-prod`. The PR body's ⚠️ section is accurate; no action needed.

**5. Pre-existing: `fmt -check -recursive` fails on `staging.tfvars` alignment** [codebase] — byte-identical on develop; the spec'd acceptance command (non-recursive) passes. Out of scope here ("No staging changes"); separate cleanup PR candidate.

### Reviewer agreement
- **`test_min_instances` broken** — edge + codebase + tests independently ran pytest; Perkins re-ran: `1 failed / 2050 passed`. Highest-confidence signal in this review.
- **Merge is inert / manual apply required** — edge + codebase, and verified by Perkins directly.

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha.
The loop runs until an APPROVED verdict._
