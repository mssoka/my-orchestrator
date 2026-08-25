# Perkins briefing — round 1: packet-plumber-v2-5.8-qos-panel

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/50 (targets `v2`)
- **Reviewed sha:** `ea1026d7fd67667bca6e576baada50f7ecba1d46` (short `ea1026d`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.8-qos-panel.md` + the story 5.8 card in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + canon `odin-architecture-v1.md` (QoS sections). No GitHub issue — the lavish-clarified rulings below ARE the spec.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Local verification at the sha remains ground truth. (The job briefing's "CI blocked" line predates the fix — ignore it.)

## What the PR does (review scope)

**Story 5.8 — QoS legibility: a real panel + assignment-driven auto-reservation.** The two lavish-approved rulings:
1. **Cmd_Set_Emphasis payload evolves** (preset `u16` → weights `[3]i32`) — same serialized tag, `LOG_VERSION` 3→4, so the auto-ladder and the manual editor write through ONE command → replay equality [E10] by construction. NOT a new command kind (scope guard holds).
2. **Ladder semantics:** in-play lanes = assigned lanes ∪ Standard (always reserved, canon-safe). streaming→Express alone = 70/30; + email→Best-effort = exactly 50/30/20.

Built: `lane_auto_reserve_ladder` in `data/balance.json` ([100]/[70,30]/[50,30,20], fail-fast validated — the canon commit referenced the field but hadn't shipped it); `qos_auto_weights` pure core proc (untouched pipes keep the default preset — no-QoS goldens byte-stable); the QoS panel (`app/qos_panel.odin`, new) — per-type lane rows (click to cycle or 1/2+E/S/B), the split with real numbers + bars, manual editor (presets + ±5 nudges), derived AUTO/MANUAL mode, revert-to-auto; right-click dial retired → selects the pipe (documented choice); harness weights directive + 2 new demos with T2 captures.
Verification: 167 core tests, lint, 27 harness demos green; golden fold proven (4.3 discipline): every `.log.bin` diff = the version byte + 8 catalog-hash bytes ONLY; all T2 PNGs byte-identical; new captures visually confirmed (50/30/20 + 60/25/15 lane splits); replay gate passes for every blessed log. Review swarm findings applied (a committed `tools/raylib-sw` symlink leak blocker fixed; silent manual-tune clobber gated on the pre-edit derived mode; never-drop E6-safety by construction; no cycle deadlock on zeroed lanes).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — serialization + replay equality [E10].** The `Cmd_Set_Emphasis` payload evolution (u16 → weights [3]i32, SAME tag, LOG_VERSION 3→4) must hold replay equality BY CONSTRUCTION: the auto-ladder and the manual editor write through the ONE command; every blessed log replays (the golden fold is the mechanical proof — see next). Any divergence between live and replay = a blocker.
- **🚨 The golden fold must be MECHANICAL.** Every `.log.bin` diff = the version byte + 8 catalog-hash bytes ONLY; all 24+ pre-existing T2 PNGs byte-identical; the 2 new demos' captures visually confirmed. A NON-mechanical golden change (semantic drift hidden in a re-bless) = a blocker. Spot-check the fold by diffing old goldens.
- **Ladder semantics exact:** in-play = assigned ∪ Standard; streaming→Express alone = 70/30; + email→Best-effort = exactly 50/30/20; untouched pipes keep the default preset (no-QoS goldens byte-stable). A wrong split or a Standard-lane regression = a blocker.
- **Never-drop safety:** E6 — future non-Standard defaults can't break the auto path (never-drop by construction); no cycle deadlock on zeroed lanes (the swarm fix). Verify both.
- **Manual editor:** presets + ±5 nudges, derived AUTO/MANUAL mode, revert-to-auto; the silent manual-tune clobber on lane assignment is gated on the pre-edit derived mode.
- **Base = `v2`** — now includes 5.3 pause + 5.3-pause-ux + 5.7 telemetry (all merged; 5.7 touched app/main.odin emission/overlay paths). Carry-forward only; do NOT re-open settled findings.
- **Scope guard:** QoS panel + auto-reservation + the payload evolution ONLY — no new command kinds, no unrelated gameplay changes, nothing 5.7-telemetry or 5.3-pause owns.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.8-qos-panel-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
