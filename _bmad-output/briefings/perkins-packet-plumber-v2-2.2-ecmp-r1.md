# Perkins briefing — round 1: packet-plumber-v2-2.2-ecmp

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/26 (targets `v2`)
- **Reviewed sha:** `a1c6e6444dca4d62e4dcdaea10810f0dca45acb7` (short `a1c6e64`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.2-ecmp-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-2.2-ecmp.md` + Story 2.2 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (full card line 179+) + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (4-rule spine rule 2 = pure hash, no sim-rng/map-iter; `[ODN-9/10]` ECMP; `[E10]` replay-equality; `[RR]` routing rules; §11.7 headless-test contract; ODN-1 core-engine-free) + GDD E1.4. No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (hash-purity self-grep + behavioral pin, no-map-iter lint gate 3, flow affinity pinned, 43 core tests, harness 6/6; it hit + recovered the bmad-quirk) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**v2 Story 2.2 — ECMP across equal-cost next hops.** Among N equal-cost next hops, the pick is a **pure hash** — `splitmix64(src, dst, class, pkt_id) mod N` — deterministic per packet (flow affinity, no intra-flow reordering). Changes single-next-hop → hash-over-equal-cost-set in the forwarding loop (slice 2 story 2 of 3: bundles ✓ → ECMP → demolish). New/changed: `core/routing.odin`, `core/flow.odin`, `core/ecmp_test.odin` (new). **Backward-compatible by construction:** the routing table is derived (not serialized); count==1 reproduces slice-1/2.1 single-hop forwarding → existing goldens stay valid, no re-bless.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 PURE HASH, NO SIM-RNG — THE load-bearing invariant (4-rule spine rule 2).** The routing decision is `splitmix64(src,dst,class,pkt_id) mod N` — a PURE function of packet identity. **NEVER a sim-rng draw** (`rng_next`/`rng_range`/`state.rng` in the routing path). The Perkins lens-guard GREPS for sim-rng in the routing path. A sim-rng draw in the pick (or the pick touching `state.rng`) is a REAL blocker. The minion pinned it behaviorally (`test_ecmp_pick_is_pure_no_sim_rng` — a flow run vs a no-flow run end with bit-identical `state.rng`); verify the grep is clean + the pin is real.
- **🚨 NO MAP ITERATION IN THE HOT PATH.** The equal-cost next-hop set must be **array-indexed** (the pick is `hops[offset + hash % count]`) — iterating a map would break determinism (map order is undefined). The lens-guard greps for map iteration in the routing path. A map-iter in the hot path is a REAL blocker.
- **FLOW AFFINITY.** Same `(src,dst,class,pkt_id)` → SAME path every replay; no intra-flow reordering. Verify the hash inputs are exactly those four fields (a missing/extra input field would break affinity or determinism). Pinned by `test_ecmp_flow_affinity`; verify it's real.
- **DETERMINISM (E10, ODN-9/10 — carry from slice 1).** Per-packet paths are IN the state hash (T1) and replay byte-identical `[E10]`; the split frame is deterministic (T2). The routing table stays DERIVED (not serialized) — verify the restructure didn't add serialized routing state (that would be a determinism break on replay).
- **BACKWARD-COMPAT (count==1) is a feature, not a gap.** count==1 reproduces slice-1/2.1 single-hop forwarding → existing goldens stay valid, NO re-bless needed. Do NOT flag "missing re-blessed goldens."
- **T2 PIXEL HARNESS GAP is a DOCUMENTED CARRY-FORWARD, not a defect.** The T2 pixel ("packets split across paths") is **structurally/hash-verified**; the pixel re-diff needs a node-spawn demo directive (the harness `.dem` fixture is fixed at 3 nodes; a diamond needs 4). The minion flagged a mini-story for it (the rlsw harness itself EXISTS + works — 2.1 blessed pixel goldens). Do NOT flag "T2 pixel not verified" as a blocker — it's the flagged carry-forward (a mini-story recommendation, the user/Gru's call).
- **CORE ENGINE-FREE (ODN-1)** — `routing.odin`/`flow.odin` in `package core`; zero engine imports.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slice 1 + 2.1 bundles IN), not `main`.
- **The prototype is REFERENCE-ONLY** (multi-path DESIGN only; its routing was NOT the locked model).
- **CONTEXT NOTE (not a finding):** the implementing minion hit the bmad-tooling quirk (edits briefly mis-resolved to the main checkout) and RECOVERED it correctly (caught at the git-status gate, synced byte-identical into the worktree, reverted the main checkout, re-ran all gates before committing). Review the PR content as-is at the sha.
- **Do NOT re-open 1.1–2.1 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- A **sim-rng draw in the routing path** (or the pick touching `state.rng`) — a blocker (rule 2).
- **Map iteration in the hot path** (the equal-cost set not array-indexed) — a blocker (determinism).
- **Flow affinity broken** (same packet → different path across replays; hash inputs wrong/missing a field) — a blocker.
- **A determinism break** (per-packet paths not in the T1 hash; routing state serialized; E10 replay divergence on the split) — a blocker.
- **An engine type leaking into `package core`** (ODN-1) — a blocker.
- An `odin test` / `odin build` / `harness` failure at `a1c6e64`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 26 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `a1c6e64`), `spec_files` = this briefing + the job briefing + Story 2.2 + the architecture (rule 2, `[ODN-9/10]`, `[E10]`, `[RR]`, §11.7, ODN-1) + GDD E1.4, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.2-ecmp/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 26 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 26 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `a1c6e64`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-2.2-ecmp / **Reviewed sha:** a1c6e64 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-2.2-ecmp-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. **🚨 BURST WARNING (live this session, PROVEN 3x): the ZAI account rate-limit (429, code 1302) trips at ~9+ concurrent glm panes.** A righttenantry MINION (rc3-7) is concurrently working on glm-5.2 right now, so your 7-lens fan-out + orchestrator + that minion = the burst recipe. **STAGGER the lens spawns (≤4 concurrent) or accept + recover via one continue per 429'd pane** (short-window burst). If the orchestrator's own turn 429s, one continue revives it.
