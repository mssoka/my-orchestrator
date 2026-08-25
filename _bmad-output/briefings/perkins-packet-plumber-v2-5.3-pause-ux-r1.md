# Perkins briefing — round 1: packet-plumber-v2-5.3-pause-ux

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/49 (targets `v2`)
- **Reviewed sha:** `57eeda708c61f0abedbdc364cbc41de9e6cb8d98` (short `57eeda7`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.3-pause-ux-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** GitHub issue **#48** (dump it: `gh issue view 48 --json title,body,comments`) + the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.3-pause-ux.md`. The user report IS the spec.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing FIXED (checks green); local verification at the sha remains ground truth.

## What the PR does (review scope)

**USER-REPORT fix (ruling-grade): the pause overlay defeated pause-and-plan.**
- Deleted the full-screen dim veil (the `DrawRectangle` alpha-130 viewport fill) — the paused world now renders at FULL brightness, byte-identical to the running world minus stepping (prototype baseline — the prototype pauses with NO overlay at all).
- Removed the centered 48px "PAUSED" + hint text.
- Added a small edge chip ("PAUSED" / "P/Space to resume", 120×38, tray-chip styled: bg + 1px border + ink_soft text) in the top HUD band at `win_w/2 + 240` — the only top-edge position free in every state (top-left carries the QoS readout when a pipe is selected; top-right hosts the forecast panel during a crisis pause). Collision-verified via a scratch replica rendered with the rlsw shadow (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`) + `LoadImageFromScreen` + PIL pixel-scan (vision models misjudge absolute coordinates).
- Pause-and-plan untouched: draw/place/demolish/QoS fast-paths, the paused bundle-view refresh, glow/preview/demolish surface — all unchanged. **No core/harness/data changes** — determinism holds by construction.
- Canon amended in the SAME PR: GDD §UI&Navigation + art-direction §8.1 "Pause-to-plan" lines now specify the ruling (full-brightness world, edge chip indicator, prototype-aligned); story 5.3 card status records it.
- Verification: 158 core tests, 25/25 demos goldens byte-identical (no re-bless), lint green, build clean.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — presentation-only scope.** The diff must touch `app/main.odin` presentation paths ONLY (and the canon docs + tests): NO core (`core/`), NO harness (`harness/`), NO data/goldens changes. A core/harness/data change hiding in this diff = a blocker (it would endanger the 5.3 determinism spine that r1 just pinned — pause is driver-level, the T1 pin freezes the sim, the log pins the edits).
- **Pause-and-plan intact:** the edit fast-path (draw/place/demolish/QoS while paused) and the paused bundle-view refresh must be unchanged — verify by diff, not by claim.
- **Golden-safety:** all 25 demos' goldens byte-identical — the app overlay is app-layer-only and never appears in harness T2 captures; any golden shift = a blocker (rendering change is NOT a golden change; the briefing allows NO sim-level shift).
- **The edge chip** must be small + unobtrusive (like other HUD chips), NOT overlap the map's interactive area more than existing HUD elements, and NOT re-cover the play area (the user's complaint was exactly "text right in the middle of the page").
- **Canon agreement:** the amended GDD/art-direction lines must match the CODE (full-brightness world, edge chip indicator) — canon and code agree, per the ruling.
- **Base = `v2`** — includes 5.3 pause (7b56485) + 5.5/5.6 + the 5.7 telemetry line (4749470, merged... if merged before this review). Carry-forward only; do NOT re-open settled findings.
- **Scope guard:** the pause overlay presentation + its canon line ONLY — no toggle-key changes, no stepping/accumulator logic, no fast-path changes, no QoS, nothing 5.7-telemetry touches.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-ux/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.3-pause-ux-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
