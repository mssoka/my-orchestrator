# Perkins briefing — round 2: packet-plumber-v2-5.7-runtime-telemetry

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/47 (targets `v2`)
- **Reviewed sha:** `86ef8f8b479f1f10a82ab04951d4097959057797` (short `86ef8f8`) — the r1 rework push
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 2 of 3 — **FIX-AUDIT on the r1 rework** (`prior_findings` = r1)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r2` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.7-runtime-telemetry.md` + **r1's `consolidated.json`** at `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/consolidated.json` (your prior_findings — fix-audit FIRST, carry-forward markers) + the r1 review body.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green); local verification at the sha remains ground truth.

## What the rework claims (r1 → r2 delta to audit)

r1 = NEEDS CHANGES (B1 P0 record-math pins, B2 advisory gate, W1–W10 doc/integrity).
The minion's r2 push claims:
- **B1** — `test_stats_derivation_congested` now value-pins the class rows: `loss_pct == dropped*100/(delivered+dropped)`, `avg_latency_ms == total_latency_ms/delivered`, the `flow.sla` accumulator mapping, and the `sla_breach` latch copies.
- **B2** — gate raised: D-row accounting (`offered == carried + drops*bandwidth`), bundle-member replication (2-member parallel-pipe bundle), shared `stats_emit` path, CI wiring (`-define:PP_DEBUG=true` build + `stats-check` step).
- **W1/W2** — app rejects a dangling `--stats-out` (exit 2, mirroring the harness); unwritable path exits 1 per the spec's I/O matrix.
- **W3** — the PR-body excerpt is now the VERBATIM tick-21 stream (no fabricated D row).
- **W4** — seed-column claim corrected (sim_hash folds the seed).
- **W5** — AC5 checkbox ticked. **W6** — D rows aggregate per (pipe,class,reason) via map-free find-or-append (deterministic).
- **W7/W8** — D-row accounting + 2-member bundle replication pinned in stats_test.
- **W9** — `stats_emit` is the ONE emission proc; harness drivers AND the app loop call it.
- **W10** — CI builds with PP_DEBUG + runs stats-check (pause, qos_contention).
- Notes picked up: N1 (CI stats-check), N2 (streams under gitignored `bin/`), N4 (overlay-check fails loud on zero stepped ticks), N5 (demo_destroy extracted), N6 (usage string), N7 (overlay_on comment), N9 (header comment).
- Verification claimed: 164 core tests (158+6), lint 6/6, 25/25 demos goldens byte-identical, stats-check byte-identical on pause/qos_contention/surge/health_lose, both app builds, CI YAML valid.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **Fix-audit mandate:** verify each r1 finding's fix BITES (a fix that doesn't fail on regression = not a fix): B1's class-row pins fail on an identically-wrong formula; W3's excerpt is the verbatim artifact; W9's shared emission proc is actually called by BOTH drivers; W6's aggregation is deterministic (map-free find-or-append) and correct; W10's CI gates are real. Do NOT re-litigate findings r1 verified — carry them as fixed/marked per the consolidated.json.
- **🚨 LOAD-BEARING (carried from r1):** the determinism contract — the stats stream is derived ONLY from existing deterministic state (NO wall-clock, NO render sampling); the one-CSV-serializer byte-identity contract (harness == app) and replay-identity (live == replay) must STILL hold at 86ef8f8. The overlay stays golden-safe (compile-excluded from non-PP_DEBUG builds, off by default, unreachable from capture). Any new nondeterminism or a golden shift = a blocker.
- **Base = `v2`** — 5.3 pause + 5.5/5.6 + 5.7-r1 state; carry-forward only; do NOT re-open settled findings (the pause determinism spine is settled).
- **Scope guard:** telemetry export + overlay only — no new capture semantics, no event-stream shape changes. Sibling 5.3-pause-ux (a presentation-only overlay change) may merge mid-round; its file set is `app/main.odin` presentation paths — if it lands, carry-forward only.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2`, `prior_findings` = the r1 `consolidated.json`. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.7-runtime-telemetry-perkins-r2 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
