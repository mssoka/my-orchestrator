# Perkins briefing — round 2: righttenantry-refcheck-611-panel-persist (FIX-AUDIT)

- **PR:** https://github.com/solarity-services/RightTenantry/pull/616 (targets `develop`)
- **Reviewed sha:** `0b021b000c43fba67228df1fb19d1cb8f7f02392` (short `0b021b0`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-611-panel-persist-r2` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** GitHub issue #611 (dump it: `gh issue view 611 --json title,body,comments`) + the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-611-panel-persist.md`. Issue: **611**.
- **Model:** `zai-coding-cn/glm-5.3` (FIRST glm-5.3 round — reasoning flip; launch EVERY lens with `pi --model zai-coding-cn/glm-5.3`) (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** GitHub CI is account-billing-blocked — YOUR local verification at the sha is the ground truth.

## What the PR does (review scope)

**Issue #611 fix (persistence-correctness — the bug silently saved STALE data):** the edit-trio inputs swallowed keystrokes because they were keyed by ref SLOT (which shifts when the list reorders) — now keyed by `reference_call_id` (stable). Fixes the stale-save path.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the keying is STABLE + no stale save survives.** The edit-trio state (typed values + dirty flags) must be keyed by `reference_call_id` (stable across list reorders/refetches), NOT by slot index — a residual slot-keyed path (or a key that changes identity across a refetch) = a blocker (it IS the bug class). The stale-save reproduction from the issue must be pinned by a test that bites (typed value survives a reorder/refetch → save persists the NEW value, not the stale one).
- **Per-row isolation:** two rows' edit state never cross-contaminates (typing in row A cannot bleed into row B — the previous slot-keying collision).
- **Scope guard:** #611's fix ONLY — no unrelated changes. Sibling #612 merged (em-dash) — carry-forward; its copy is settled.
- **BASE = `develop`** (RC4.1-4.4 + #607 + #610 + #612 merged — carry-forward only; do NOT re-open settled findings).
- **RT em-dash ban + AR-RC13** guards stay intact (verify nothing in this diff weakens them).
- **a11y/testids** on the edit-trio inputs unchanged (verify no regression).

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-611-panel-persist/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-611-panel-persist/r2`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-611-panel-persist-perkins-r2 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).

## Round-2 mandate: verify the r1-rework claims at 0b021b0 (fix-audit)

Commit: "test(refcheck): #611 r1 — pin the SAVE half (B1), substitute+refetch survival (W1), all field branches (W2)". Verify EACH r1 finding — the commit message is a claim, not proof.

### (a) B1 (the r1 blocker) — the SAVE chain is now pinned
- The extended pin drives Save (simulate.click on the save control or UserSavedRefcheckEdit) and asserts saving == True with the dict entry retaining the TYPED values — a future re-key of the save path turns it red. A pin that still stops at render = B1 stays open.
### (b) W1 — the sibling substitute test exists (Objected + can_substitute_referee, empty prefill, dict write under reference_call_id) and/or the refetch/reorder survival assert.
### (c) W2 — name + phone branches typed in a test (a mistyped field literal hits the _ -> edit swallow with a failing test).
### (d) N1-N4 — addressed or carried with a real reason (N2 bug-hunt scenario re-run or the live-repro-supersedes statement; N3 accepted; N4 documented deferral).
### (e) DO NOT re-litigate: r1 VERIFIED-CORRECT (stable keying, isolation by UUID, lint gates) — do not re-open.
