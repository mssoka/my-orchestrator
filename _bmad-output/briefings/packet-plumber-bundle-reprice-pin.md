# Briefing — packet-plumber-bundle-reprice-pin (W1 follow-up pin)

- **Job id:** `packet-plumber-bundle-reprice-pin`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `bundle-reprice-pin`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (canon-surface verification code — the U3 scope guard reserves
  `pr_review=0` for CI/ops-tooling).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (Job A — routing-bandwidth-cost — is merged, #37). Rebase onto origin/v2 if
  it moves mid-work; clean-rebase hygiene.

## Mission — the W1 dedicated pin

Perkins r1 on #37 (review 4932327768, APPROVED) carried ONE advisory warning: **W1 — the
mixed-tier BUNDLE re-pricing branch has no dedicated pin.** Perkins fuzz-verified it correct
across 400 random graphs (0 mismatches), but a dedicated regression pin is the gap.

**Read first:** the Perkins r1 artifacts for the exact branch + evidence:
`_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/` (body.md + consolidated.json
+ lens JSONs — find the W1 wording and which branch it names). Also re-read
`core/routing.odin` (the merged Dijkstra cost model) and `core/bundles.odin` (2.1 fat-edge
pooling) to locate the branch: bundle re-pricing = the cost lookup when a bundle's members
carry DIFFERENT tiers (representative-pipe cost vs member cost) and when a member's tier
changes the pricing.

**Acceptance:**

1. A dedicated `@(test)` pin in `core/` covering the mixed-tier bundle re-pricing branch —
   named for W1, asserting the locked behavior (representative-pipe pricing, insertion-order
   stability, integer-only).
2. **The pin must actually bite:** prove it by temporarily breaking the re-pricing logic
   (toggle test) and showing the pin fails — then restore. State this proof in the PR body.
3. Harness green; **existing goldens MUST NOT shift** (test-only change — any shift = STOP
   and flag).
4. If the pin instead reveals a REAL bug (behavior differs from the fuzz-verified claim):
   STOP, do not patch production code silently — flag it in the PR body + report it.

**Verify:** `odin test` green (core/demos/lint), harness green, goldens unchanged, bite-proof
in the PR body.

**Scope guard:** the W1 pin ONLY — no production-code changes, no other pins, no demo
changes (a demo capture is optional and only if goldens stay new-file-only).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: bundle-reprice-pin
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
