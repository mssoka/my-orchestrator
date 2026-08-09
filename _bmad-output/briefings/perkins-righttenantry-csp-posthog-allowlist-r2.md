# Perkins briefing — round 2: righttenantry-csp-posthog-allowlist

- **PR:** https://github.com/solarity-services/RightTenantry/pull/585 (targets `develop`)
- **Reviewed sha:** `67cc7e47e9b65d4b0fdee906791337a8dfd3cb63` (head `csp-posthog-allowlist`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-csp-posthog-allowlist-r2` — pinned at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the original job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-csp-posthog-allowlist.md` **AS AMENDED by the user's Q3 no-op ruling + the N1 fold-in** (below). No GitHub issue for this job.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r1/consolidated.json` (r1 APPROVED, 0B/0W/2N on sha `b37c2d7`).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (round 2 scope)

r1 (sha `b37c2d7`) APPROVED the no-op doc comment. The user then asked for **N1 folded in pre-merge**: an invariant test locking `eu.posthog.com` absent. This push (sha `67cc7e47`) adds exactly that — a dedicated test in `server/test/csp_test.gleam`:

```
policy_never_allowlists_posthog_cloud_host_test
  → asserts "eu.posthog.com" is absent from csp.policy() on both the nonce and empty-nonce branches
```

The minion verified via **negative control**: injecting `eu.posthog.com` into `connect-src` flipped this test red (1220p/1f); reverting restored 1221p/0f. `make test-server` = 1221 passed.

### r2 review focus (fix-audit-first, then new)

1. **Fix-audit r1's notes:** r1 N1 = "no test asserts eu.posthog.com stays absent" → now ADDRESSED by this push (confirm the test actually closes it). r1 N2 = "advisory test gate PASS" → re-confirm still PASS.
2. **Review the new invariant test:** is it correct and does it actually BITE? (the negative-control evidence the minion provided is the proof — verify the test would fail if eu.posthog.com were added, i.e. it's not a tautology). Is it placed where policy-content invariants belong? Does it cover both header variants (the minion argues `csp.policy()` is the shared string for report-only + enforcing — verify that claim)?
3. **No-op still holds:** confirm the test push did NOT touch any CSP directive value or the nonce logic in `server/src/csp.gleam` (the only csp.gleam change should still be the r1 doc comment).

## ⚠️ CRITICAL lens-guard (still in force — read before any lens)

The user **ruled Q3 = no-op**: `eu.posthog.com` is **intentionally absent** from every CSP directive (events are same-origin proxied via `/_ph` + `/_ph_assets`; `ui_host` is links-only; toolbar unused in prod). Therefore:

- **Do NOT flag "eu.posthog.com is missing / should be allowlisted" as a defect.** Its absence is the user-ruled design.
- **Do NOT flag the new test as wrong for asserting absence.** `policy_never_allowlists_posthog_cloud_host_test` asserting `eu.posthog.com` is absent is CORRECT — that invariant is the whole point of this push (the user asked for it). A lens that "discovers" PostHog should be allowlisted, or that the absence-test is incorrect, is re-litigating a closed question = a FALSE POSITIVE.
- Legitimate findings here would be: the test doesn't actually bite (tautology / wrong assertion target), the test is misplaced/malformed, the no-op was accidentally broken (a directive value changed), or the test's coverage claim (both header variants) is false.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 585 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd, `spec_files` = this briefing (carries the user ruling + N1 fold-in as the spec; no GitHub issue — skip the `gh issue view` dump), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r2`, and `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-csp-posthog-allowlist/r1/consolidated.json`. The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings remain → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; if it failed, fall back to `gh pr comment 585 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 585 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 2 of 3
  **Job:** righttenantry-csp-posthog-allowlist · **Reviewed sha:** 67cc7e4 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  **Prior-round fix audit:** r1 N1 (absence-test) <addressed/open> · r1 N2 (advisory gate) <pass/fail>

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _No-op doc-comment PR + N1 absence-invariant test (user-ruled Q3); eu.posthog.com is intentionally absent._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `67cc7e4`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-csp-posthog-allowlist-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow).
