# Perkins briefing — round 1: packet-plumber-v2-4.3-network-health

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/43 (targets `v2`)
- **Reviewed sha:** `8659070ed0a5ec176dc15eece6e807432c9a2a34` (short `8659070`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.3-network-health-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-4.3-network-health.md` + Story 4.3 in `stories-v2.md` (~line 402) + GDD win/lose sections + architecture `[E16]`/`[E17]`/`[E30]` + the 3.4 SLA + 4.1 telegraph + 4.2 crisis engine the meter consumes. GitHub issue: none.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** GitHub CI is account-billing-blocked — YOUR local verification at the sha is the ground truth.

## What the PR does (review scope)

**Story 4.3 — Network Health meter + win/lose/retry (CLOSES SLICE 4 — the fun-test loop):** the meter drains on sustained SLA breach (grace countdown on breach onset; SLA breach feeds drain; forecast surfaces the countdown; crisis feeds it); win/lose/retry — the terminal-event state machine (exactly ONE terminal event per run, step-freeze, T1 determinism over the loop incl. the terminal frame); retry = clean restart (run_destroy+run_init+fresh seed). The win is provably achievable (the minion flags one tuning risk: era-3 session demand scale vs build time — GDD [ASSUMPTION: prototype tuning], playtest's call).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the terminal-event barrier [E17] + determinism over the loop.** Exactly ONE terminal event per run (win/lose/goal/tick-cap/terminal — a second terminal event or a post-terminal mutation = a blocker); the step-freeze holds (step returns before tick mutates); determinism rides the T1 hash over the FULL loop INCLUDING the terminal frame (replay byte-identical — win AND lose golden paths).
- **🚨 The meter's drain semantics.** Sustained SLA breach drains with a grace countdown that STARTS on breach onset (not instantly); the drain consumes the right signals (3.4 SLA breach + 4.2 crisis + 4.1 forecast surfaces the countdown). A meter that drains instantly, never recovers, or ignores the grace = a real defect.
- **🚨 Retry = clean restart.** run_destroy + run_init + fresh crypto seed; no state carries across a retry (a leaked crisis/routing/flow state from the previous run = a blocker).
- **Locked (do NOT flag as defects):** the capacity-cost routing model (A), the readability assist (B), the forecast-shift helper (C), the crisis engine (4.2) — all merged + settled; the W1 pin; the win/lose design per the GDD (the era-3 tuning risk is a DOCUMENTED assumption — playtest's call, not a defect).
- **Golden discipline:** new goldens blessed with proof; existing goldens MUST NOT shift without cause documentation (any undocumented shift = a finding). The HUD fix (#42) touched app/main.odin render — if its golden impact is visible here, verify it traces (cross-PR context, not a defect in THIS diff).
- **Scope guard:** 4.3 content ONLY (meter + win/lose/retry) — NOT 4.4+ content, NOT new player commands (LOG_VERSION stays 3 unless flagged — a bump without a flag = flag it).
- **BASE = `v2`** (full throttle + 4.1/4.2 + pin + HUD fix merged — carry-forward only). **Em-dashes OK in PP.**

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.3-network-health/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.3-network-health/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-4.3-network-health-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
