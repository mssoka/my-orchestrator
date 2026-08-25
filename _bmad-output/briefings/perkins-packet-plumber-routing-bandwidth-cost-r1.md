# Perkins briefing — round 1: packet-plumber-routing-bandwidth-cost (Job A)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/37 (targets `v2`)
- **Reviewed sha:** `32a1b653609eb12a478142a902e8bdf262ad9868` (short `32a1b65`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-routing-bandwidth-cost-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-routing-bandwidth-cost.md` + the canon at `/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md` (PROBLEM DEFINITION, SUCCESS CRITERIA, RECOMMENDED SOLUTION — the user ruling drives this job) + the locked routing model (canon #18, `core/routing.odin`, architecture §6.2). GitHub issue: none.
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Job A — capacity-cost routing (the canon amendment):** unit-weight BFS → **Dijkstra over integer static pipe costs** (per-tier `cost` 20/10/5 in `data/pipe_tiers.json`, fixed at draw time — never dynamic utilization); equal end-to-end cost → ECMP (pure hash, UNCHANGED); unequal → the fatter path wins. `routing_equal_cost_hops` API shape unchanged; the table stays DERIVED + NOT serialized into the T1 hash; `flow.odin` forward pass untouched. New `demos/ecmp_cost.dem` + NEW golden files; **15 existing goldens re-blessed with a splice proof (fold-only: old hash into new dump FNV == old golden; .log.bin diffs = exactly the 8 header bytes; zero T2 pixels moved)** — the minion's claim; verify it. Architecture §6.2 + ODN-10 + OQ-5 + GDD player rule amended in the same PR.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — Dijkstra correctness + determinism.** (a) The algorithm is Dijkstra over integer pipe costs (cheapest-first, array-backed, NO map iteration [ODN-10], NO floats, NO rng draws in routing); equal-cost condition `dist[v] + cost(pipe) == dist[u]`; the ECMP set = the neighbors satisfying it; `routing_equal_cost_hops` (offset, count) shape unchanged. (b) A wrong shortest-path (path cost ≠ sum of tier costs) or a nondeterministic tie-break = a blocker. (c) The table stays a pure function of Topology, rebuilt only on topology change (rule 1), NOT serialized (rule 3) — the T1 hash is unchanged in WHAT it covers (the fold below is the only serialization delta).
- **🚨 LOCKED — do not flag as defects:** `ecmp_pick`/`ecmp_hash` (pure identity hash, spine rule 2 — unchanged by design); the table being derived-not-serialized; the forward pass reusing `(offset, count)` + `ecmp_pick`; static (never dynamic) costs; congestion avoidance being the player's job (QoS/engineering) — NOT routing's.
- **🚨 GOLDEN-DISCIPLINE — the splice proof is the claim to verify.** The minion re-blessed 15 existing goldens claiming fold-only shifts (catalog-hash fold rides every per-tick hash; .log.bin = exactly the 8 header bytes; old-hash-into-new-dump FNV == old golden on all 16 demos; zero T2 pixels moved). Verify: (a) the proof is REAL (reproduce the splice on a sample); (b) NO behavior-shifting golden delta hides in the re-bless (a golden that moved beyond the fold = a REAL finding — the "STOP and flag" class); (c) the new `ecmp_cost.dem` goldens are new files. An undocumented/unproven shift = a blocker; a proven fold-only shift = expected.
- **ODN-5 — the `cost` field:** integer, validated `cost >= 1` at catalog load (zero-cost edges would break the per-hop progress guarantee — reject at load; the minion claims fail-fast rows). A zero/negative cost slipping load = a blocker.
- **The four core test contracts:** mixed-tier diamond picks the fat path as a UNIQUE next hop (no ECMP when costs differ); different-tier equal-sum tie → ECMP set of 2 (the S→R1 standard(10)+R1→D fast(5)=15 vs S→R2 fast(5)+R2→D standard(10)=15 TRUE tie); re-step determinism (byte-identical); ladder read from data (a data change moves behavior — ODN-5 wiring proof).
- **Demo:** `demos/ecmp_cost.dem` captures the fat-path unique hop mid-flight AND the true different-tier tie split; `expect hash stable`.
- **Scope guard:** Job A ONLY — capacity-cost routing + the canon docs. NOT 4.3, NOT the other crisis archetypes, NOT Job B (readability assist) or Job C (forecast-shift) content, NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it). Do not demand features B/C will add.
- **BASE = `v2`** (slices 1–3 + harness + 4.1 + 4.2 in — the 4.2 crisis engine is merged; carry-forward only; do NOT re-open 4.2 findings).
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> of 3
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-routing-bandwidth-cost-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
