# Perkins briefing — round 1: righttenantry-refcheck-612-emdash-prose

- **PR:** https://github.com/solarity-services/RightTenantry/pull/614 (targets `develop`)
- **Reviewed sha:** `42afaf093da15dc4ccde6e557a7284af86a981a5` (short `42afaf0`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-612-emdash-prose-r1` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** GitHub issue #612 (dump it: `gh issue view 612 --json title,body,comments`) + the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-612-emdash-prose.md`. Issue: **612**.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** GitHub CI is account-billing-blocked — YOUR local verification at the sha is the ground truth.

## What the PR does (review scope)

**Issue #612 fix:** the em-dash lint exemptions shipped em-dashes to landlords — the exemptions are removed and all 15 spec-verbatim strings re-composed dash-free (the RT em-dash ban now covers everything user-facing).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — NO em-dash survives in user-facing copy.** Grep the user-facing strings (copy.gleam + composition sites + timeline/export/notification strings) for U+2014 — ZERO may remain in implementer-authored OR spec-verbatim strings (the exemptions are GONE — verify the exemption mechanism was actually removed, not just the strings). An em-dash in any shipped string = a blocker.
- **Spec-verbatim integrity:** the 15 re-composed strings must still MATCH the spec copy semantically (dash-free but word-identical otherwise — the fix re-composes, it does not rewrite; a string that drifted from the spec = a finding).
- **The lint still bites:** `lint_em_dash.py` + the ban test still FAIL on an injected em-dash (the exemption removal must not have weakened the scanner; negative controls green).
- **Scope guard:** #612's copy fixes ONLY — no unrelated changes, no behavior changes outside the strings.
- **BASE = `develop`** (RC4.1-4.4 + #607 + #610 merged — carry-forward only; do NOT re-open the RC4/#607 settled findings). Sibling #611 (panel-persist) runs in PARALLEL — not in this PR.
- **RT em-dash ban applies** (this is the enforcement story).

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-612-emdash-prose/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-612-emdash-prose-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
