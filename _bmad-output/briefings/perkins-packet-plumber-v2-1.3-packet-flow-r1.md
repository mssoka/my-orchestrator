# Perkins briefing — round 1: packet-plumber-v2-1.3-packet-flow

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/23 (targets `v2`)
- **Reviewed sha:** `6265802b5e6c62ca770c212869f15be46248978d` (short `6265802`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-1.3-packet-flow-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-1.3-packet-flow.md` + Story 1.3 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (S2 Flow, the **per-hop forwarding + ECMP/bundles model** = the locked routing, §6.2 as amended by canon #18; ODN-9/10/11 determinism) + GDD E1.4 (`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`). No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out field-note shard at `_bmad-output/field-notes/packet-plumber-v2-1.3-packet-flow.md` (it flagged 3 traps it hit — id-0 sentinel, replay re-creating flow demand, T2 rlsw software-renderer — useful as leads, NOT as a substitute for your own verification).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**v2 Story 1.3 — One packet flows (per-hop forwarding).** The first routing: a packet spawns at a source, the router forwards it **per-hop** along the drawn pipe(s) to the sink, and you see it move across the render. Trivial flow (one packet, one path source→router→sink), but the **forwarding-DECISION shape is per-hop** (a junction function picks the next hop) — the foundation the locked routing model builds on. Built fresh on `v2` (1.1 determinism spine + 1.2 window/render/topology IN); the prototype is **reference-only** (mine its `flow.odin` flow-sim design — progress/bandwidth/vis — but its routing was BFS, which is explicitly NOT the model here).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **PER-HOP FORWARDING, NOT BFS, NOT A SPAWN-TIME ROUTE CACHE — this is THE load-bearing invariant.** The `Packet` struct has NO `route[]` field by construction; each junction the packet reaches decides the next hop. Do NOT flag "missing route computation" or "should cache the route at spawn" — per-hop is the REQUIREMENT (canon #18), not a gap. A BFS-on-packet, a `compute_route`, or a spawn-time cached `route` sneaking in is a REAL blocker (violates the locked model); the ABSENCE of them is correct.
- **1.3 = SINGLE PATH only (one packet, source→router→sink).** ECMP across equal-cost paths (the seeded `splitmix64(src,dst,class,pkt) mod N`) + parallel-pipe **bundles** are LATER slices, explicitly OUT OF SCOPE for 1.3. Do NOT flag "missing ECMP" or "missing bundles" — those are deferred by design, not defects. The forwarding-DECISION shape is per-hop even though there's only one path to pick here.
- **DETERMINISM over the flow is load-bearing (carry from 1.1).** The per-hop decision + packet motion MUST route through the action-log + state-hash; a recorded flow reproduces byte-identical motion on replay. A determinism break (replay divergence over the flow) is a blocker.
  - **Replay re-creates run-setup, NOT flow demand by default** (a known trap): flow demand is run-setup (like the fixture), NOT in the action log — so any new run-setup added to the sim must be threaded through `replay_hashes` in BOTH the live (`lower_spawns`) and replay paths, or replay diverges at tick 1. Verify the flow demand is handled in both paths.
  - The spine's `step` is a heartbeat — one owned-RNG draw/tick folded into a `tick_nonce` state field; verify the per-hop decision + motion tie into this (no un-logged RNG).
- **The id-0 sentinel trap** (a known gotcha): PP node/pipe ids are 0-based, so `edge==0` / `at_node==0` CANNOT be the on-edge/at-node sentinel (a packet on pipe id 0 looks "at a node" and never moves). Verify an explicit `on_edge: bool` flag (or a +1 id scheme) is used, NOT a 0-sentinel.
- **Engine-free core (headless testable)** — the Simulation Core stays separate from rendering; verify the flow/forwarding logic is testable headless (the harness can drive it without a GPU).
- **T2 pixel goldens need the rlsw SOFTWARE renderer** (`tools/harness.sh`) — `odin run harness` linking the stock GPU `vendor:raylib` renders a SOLID BLACK frame headless. If a T2 golden looks suspicious (all-black), that's a renderer-setup issue, not a logic defect — flag it as a verification gap, not a code bug.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP) — do NOT flag em-dashes here.
- **The base is `v2`, not `main`** — the PR targets `v2` (1.1 spine + 1.2 IN). Don't flag "wrong base."
- **CONTEXT NOTE (not a finding):** this PR may have been affected by the bmad-tooling quirk (edits briefly mis-resolving to the main checkout instead of the worktree; Silas synced it). Review the PR's content as-is at the sha.
- **Do NOT re-open 1.1/1.2 findings** (merged, verified) — carry-forward only.

### Legitimate findings here would be
- A **BFS / spawn-time route cache** sneaking in (violates canon #18 per-hop) — a blocker.
- A **determinism break** over the flow (replay divergence; un-logged RNG; flow demand not in the replay path) — a blocker.
- A **0-sentinel bug** (on-edge/at-node keyed on a 0 id) — a real defect (a packet stuck or mis-located).
- A **non-per-hop decision** (e.g., the route pre-decided at spawn, or the "junction" not actually deciding per-hop).
- A packet that **doesn't visibly move** source→router→sink, or a wrong path.
- **Core not engine-free** (flow logic entangled with rendering such that it can't run headless).
- An `odin test` / `odin build` / `harness` failure at `6265802`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 23 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `6265802`), `spec_files` = this briefing + the job briefing + Story 1.3 + the architecture (S2 Flow, §6.2 canon #18, ODN-9/10/11) + GDD E1.4, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.3-packet-flow/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 23 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 23 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `6265802`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-1.3-packet-flow / **Reviewed sha:** 6265802 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-1.3-packet-flow-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. If a lens 429s mid-turn, one `continue` may revive it; if it hard-fails, note the degraded lens. (This round was SERIALIZE-HELD behind the rc3-5 r2 round until it closed out — now released.)
