# Perkins briefing — round 1: righttenantry-refcheck-613-615

- **PR:** https://github.com/solarity-services/RightTenantry/pull/618 (targets `develop`)
- **Reviewed sha:** `552aea52d8e3f8153f31594485141100b9169052` (short `552aea5`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-613-615-r1` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** GitHub issues **#613** + **#615** (dump both: `gh issue view 613 --json title,body,comments` and `gh issue view 615 --json title,body,comments`) + the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-613-615.md`. The issues ARE the spec.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live; a "glm-4.7" self-id is a hallucination, not a misroute). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED — PR #618's checks were green (migration, format/lint/unit, integration, terraform). Use CI if helpful; YOUR local verification at the sha remains ground truth.

## What the PR does (review scope)

Two UX fixes from the refcheck bug-hunt fallout, ONE PR:
- **#613 — stepper label ambiguity:** the `viewed` status now renders as **"Viewing held"** on every user-facing surface (stepper stop, backward-confirm modal, audit trail, shared pill, detail-page pill) via a single `label_for_slug_opt` source of truth, plus a native `title` hint on the viewed stop ("Mark when you've carried out the viewing. Reference checks start here."). The DB enum, API slugs, trigger logic, and `vacancy.viewed_at` (unrelated ad-view counter) are UNTOUCHED. Layout accommodation: leaderboard status track 5rem→6rem + whitespace-nowrap.
- **#615 — toasts hidden behind the consent banner:** the toast stack moved bottom-right → top-right below the header (`fixed top-20 right-4 z-[2147483001]`) — ONE z-step above the consent banner's `2147483000`. `consent.js` untouched; the banner stays visible + clickable. Evidence artifact in-repo: DOM geometry evals + screenshots (desktop / mobile / degenerate 320×480) + clickability proof.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING #613 scope: LABEL AND USER-FACING COPY ONLY.** The DB enum (`20260808120000_add_viewed_application_status.sql` must still read `viewed`), the refcheck trigger logic (marking `viewed` mints the queued reference calls), and `vacancy.viewed_at` (ad-view counter) must be UNTOUCHED. Internal/log/migration identifiers keep `viewed`. A stray USER-FACING "Viewed" status label surviving anywhere (grep the app surfaces) = a blocker.
- **#613 consistency:** ONE term everywhere — "Viewing held" on every user-facing render (stepper stop, backward-confirm modal, audit trail, shared pill, detail-page pill); no half-renamed surface. Copy tests pin the new wording.
- **🚨 LOAD-BEARING #615:** the consent banner must remain VISIBLE AND CLICKABLE at all times — never covered, never dismissed, never moved. `consent.js` untouched. Toast visibility DURING the consent window must be proven by the evidence artifact (DOM geometry + screenshots + clickability proof, desktop/mobile/degenerate).
- **Degenerate-corner trade-off:** at 320×480 with the customize panel expanded, the banner can be taller than the viewport — the minion chose "toast visible" over "never cover the banner" THERE ONLY. This is a documented + user-flagged decision. Verify the documentation is accurate and the banner is clickable on normal viewports; do NOT re-litigate the trade-off itself.
- **RT em-dash ban + AR-RC13** guards stay intact — the #612 precedent: all spec-verbatim strings must remain dash-free (em-dash exemptions were removed).
- **BASE = `develop`** — now includes #616 (611 stale-save fix, merged today) + #607/#610/#612. Carry-forward only; do NOT re-open settled findings.
- **Scope guard:** the two fixes only — no other copy sweep, no stepper-order changes, no consent-banner logic changes beyond layering, no #611 input-path work (that was PR #616, merged).

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-613-615/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-613-615-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
