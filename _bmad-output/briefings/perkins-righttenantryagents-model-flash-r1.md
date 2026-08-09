# Perkins briefing — round 1: righttenantryagents-model-flash

- **PR:** https://github.com/solarity-services/RightTenantryAgents/pull/169 (targets `develop`)
- **Reviewed sha:** `fb98f8fe4617bf303941b87e4d2460901d32ddb7` (head `model-flash`)
- **repo_root:** `/Users/moses/code/RightTenantryAgents`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-model-flash-r1` — pinned at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the original job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantryagents-model-flash.md` (carries the user's rulings: switch ALL 12 agents to gemini-3.6-flash; both config.py + variables.tf). No GitHub issue for this job.
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

Consolidates all 12 RT inference agents onto **`gemini-3.6-flash`**. The implementing minion found the briefing's forensics were STALE (PR #164 had already moved `config.py`'s fallback + the default-tier Terraform vars to 3.6-flash), so the real delta in this PR is the **5 Pro-tier agents** (`risk_scorer`, `verification_compliance_judge`, `final_compliance_reviewer`, `consistency_checker`, `personal_statement_analyzer`) flipped from `gemini-3.1-pro-preview` → `gemini-3.6-flash`, across 4 surfaces:
- `deployment/terraform/variables.tf` — 5 prod defaults
- `tenant_scorer/.env.example` — 5 matching dev entries + section comment
- `deployment/README.md` — model-variable table (swept; would've shipped stale)
- `tenant_scorer/config.py` — 1 comment ref

Acceptance per the minion: pytest 2026 unit + 34 integration pass (15 xfail "Requires model access", unchanged); retry/fail-fast/gate/repair logic (#156) untouched; remaining `gemini-3.1-pro-preview` refs are non-config and deliberately retained.

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

This is a **user-approved cost-optimization model switch**, verified as an UPGRADE (not a downgrade) via Artificial Analysis (3.6 Flash beats 3.1 Pro Preview on intelligence 50v46, cost 33% cheaper, speed 1.8×). Therefore:

- **Do NOT flag the Pro→Flash change as a "downgrade" or "wrong model" defect.** Switching the 5 Pro agents (incl. the compliance judges + risk_scorer) to Flash is the user's explicit ruling. It is intentional + correct.
- **Do NOT flag the remaining `gemini-3.1-pro-preview` references as "stale strings that must be changed."** They are NON-CONFIG (e.g. test fixtures, docs referencing the prior tier) and deliberately retained — documented in the PR's "Decisions & rationale." Only the 4 config surfaces above were meant to change.
- **Do NOT flag "judge quality not verified at runtime" as a blocker.** The minion ran the judge sanity-check (Pro baseline clean; Flash side inconclusive inline only due to a dev-env `BRAVE_API_KEY` gap — a prod-only artifact). A full staging eval (with Brave) is the user's separate deploy-time quality gate — it is NOT something this diff can or should provide. The diff's job is the model switch; runtime eval is downstream.

### Legitimate findings here would be
- A model-selection point the minion MISSED (some agent still resolves to `gemini-3.5-flash` or `gemini-3.1-pro-preview` in an actual config path — grep `get_agent_model` resolution).
- The 4 surfaces are INCONSISTENT (e.g. variables.tf says 3.6-flash but .env.example still says 3.1-pro-preview for the same agent).
- An accidental change to the retry/fail-fast/gate/repair logic (#156) — the diff should be model strings + comments ONLY.
- A wrong model ID (it must be exactly `gemini-3.6-flash`).
- A broken config syntax (Terraform/Gleam/Python parse error).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 169 --repo solarity-services/RightTenantryAgents` → `/Users/moses/code/_bmad-output/perkins/righttenantryagents-model-flash/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd, `spec_files` = this briefing + the original job briefing (no GitHub issue — skip the `gh issue view` dump), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantryagents-model-flash/r1`, `prior_findings` = none (round 1). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings remain → `--comment` + flag Gru ("incomplete review").
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; if it failed, fall back to `gh pr comment 169 --repo solarity-services/RightTenantryAgents --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 169 --repo solarity-services/RightTenantryAgents --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** righttenantryagents-model-flash · **Reviewed sha:** fb98f8f · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _User-approved model consolidation: all 12 agents -> gemini-3.6-flash (UPGRADE per Artificial Analysis); retry/fail-fast (#156) untouched._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `fb98f8f`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantryagents-model-flash-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow).
