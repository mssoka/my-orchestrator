# Perkins briefing — round 1: packet-plumber-v2-5.6-router-tiers

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/45 (targets `v2`)
- **Reviewed sha:** `4d637e72dd8ac6291147619b789a5e210eebe364` (short `4d637e7`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.6-router-tiers-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.6-router-tiers.md` (incl. rule 7 — the placement-separation rework, user ruling 2026-08-14) + GDD M3 (4/8/16) + look-book A3 (capacity-scaled router pucks). GitHub issue: none.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** GitHub CI is account-billing-blocked — YOUR local verification at the sha is the ground truth.

## What the PR does (review scope)

**Story 5.6 — router TYPES (mid 8 / high 16) + the PLACEMENT-SEPARATION REWORK (rides this PR):**
mostly data + render: `data/node_types.json` gains mid/high (port_capacity 8/16), tray auto-populates (6 chips), the puck scales with tier (A3), `Cmd_Place_Router.type_idx` already serialized → NO LOG_VERSION bump; placement validation splits by node kind (user ruling): router↔router 4 tiles (tunable), router↔terminal snap-floor + ~2-tile margin (floor derives from snap_radius E4), terminals never block routers the way the old blanket 7-tile rule did (`PLACEMENT_MIN_SEP_TILES` removed). No economy (tiers free; upgrade-in-place deferred to 8.6 — documented [ASSUMPTION]).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the kind-split placement separation.** (a) Router↔router min = 4 tiles (tunable via balance.json — verify it's data-driven, not hardcoded); (b) router↔terminal = snap-disambiguation floor + ~2-tile readability margin ONLY — a router can now sit near a house/terminal (the old blanket rule that blocked routers near houses is GONE); (c) terminals never block router placement the way the old rule did. A regression to the blanket rule, a missed kind-split, or a tunable that isn't data-driven = a blocker.
- **🚨 The old `PLACEMENT_MIN_SEP_TILES` is actually removed** (not shadowed) — grep-verify no residual blanket-separation path in core/topology.odin.
- **Tier correctness:** mid = 8 ports, high = 16 ports (GDD M3) with the capacity-scaled puck (A3); `port_capacity` wiring (catalog.odin:32 comment "0 = unlimited terminals; 4/8/16 routers") honored; placing mid/high goes through the SAME `Cmd_Place_Router` path with the right `type_idx` (verify the tray chips arm the correct tier — a chip that places the wrong tier = a real defect).
- **No LOG_VERSION bump** (no new command kinds — verify; a bump without a flag = flag it).
- **Golden discipline:** 22 golden pairs claimed hash-fold-only (the catalog-hash fold) + 4 NEW captures — verify the fold-only claim mechanically (like the A splice proof: old hash into new dump reproduces the old golden) and that the 4 new captures are new files. An undocumented/behavior-shifting golden delta = a blocker.
- **No economy is expected** (free tiers, upgrade deferred — the [ASSUMPTION] is in the PR body + story card; do NOT flag missing costs/upgrade).
- **Locked:** the demolish input surface (5.5 — merged), the routing/crisis models, the HUD fix, canon docs (5f51236 — GDD/arch/stories; the docs are the SPEC, not the diff).
- **Scope guard:** tiers + placement-separation ONLY — NOT pause (5.3), telemetry (5.7), QoS panel (5.8) content; NO unrelated refactors.
- **BASE = `v2`** (through 5.5 + canon — carry-forward only). **Em-dashes OK in PP.**

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.6-router-tiers/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.6-router-tiers/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.6-router-tiers-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
