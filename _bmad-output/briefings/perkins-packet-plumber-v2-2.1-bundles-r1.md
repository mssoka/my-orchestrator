# Perkins briefing — round 1: packet-plumber-v2-2.1-bundles

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/25 (targets `v2`)
- **Reviewed sha:** `cb497ab9bdc1c6e584d643d56209eae2d083ba37` (short `cb497ab`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.1-bundles-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-2.1-bundles.md` + Story 2.1 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (full card + the slice-2 framing line 152+) + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (the 4-rule spine rule 3 = static sum, `[RR]` routing rules, `[ODN-10]` bundles, §11.7 headless-test contract; ODN-1 core-engine-free; ODN-9/10/11 determinism) + GDD E1.5/E1.4 (`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`). No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (36/36 core, lint 5/5, harness 6/6, drift 35/35; W1/W2 test-debt from 1.4 folded in) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**v2 Story 2.1 — Parallel-pipe bundles (cap = sum).** Parallel pipes between a node pair bundle into ONE pooled-capacity link (cap = sum of members), derived from adjacency at table-build time (4-rule spine rule 3). Routing sees **one fat edge per pair**; **NO load balancing** (round-robin/weighted LB are DELETED, grep-gated absent). A "merge pop" animation when pipes join a bundle. New `core/bundles.odin` + `bundles_test.odin`, `demos/bundle.dem`, bundle goldens; modified core/{types,step,flow,win_lose_test}, app/{main,render/view}, harness/{run,goldens}, `tools/lint.sh` (a new comment-stripped grep-gate). **First story of slice 2** (routing the locked way: bundles → ECMP → demolish), on slice-1-complete v2 (1.1-1.4 in).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 NO LOAD BALANCING — THE load-bearing invariant.** A bundle is ONE pooled edge to the routing — round-robin / weighted-LB patterns MUST be ABSENT. The minion enforced it two ways: lint gate 5 (a **comment-stripped grep-gate** — the Perkins lens-guard) + a **behavioral transit-time pin** (a 2-pipe bundle crosses in 1 tick vs 2 for a lone pipe; an RR-split would also take 2). Do NOT flag "missing per-pipe distribution" — pooling is the REQUIREMENT. A round-robin/weighted-LB pattern sneaking in (or the grep-gate not actually catching one) is a REAL blocker. (ECMP, next story 2.2, is a *hash* across equal-cost next-hops — NOT this story, NOT LB.)
- **STATIC SUM AT TABLE-BUILD (4-rule spine rule 3).** Capacity is computed ONCE in `bundles_rebuild` (folded from the composing pipes), never per-packet, never dynamically mid-flow. A dynamic per-packet capacity computation is a blocker.
- **BUNDLE STATE IS DERIVED, NOT SERIALIZED — determinism is load-bearing (ODN-9/10/11, carry from slice 1).** The `Bundles` struct is DERIVED from the composing pipes (rebuilt from topology), `Packet.edge` stays a **pipe id (a representative member)** — so zero serialized state changed, and a parallel-pipe draw replays byte-identical (T1 golden) + pixel-identical (T2 golden). Verify: the bundle rebuild is deterministic (same topology → same derived state), the T1 hash covers the composing pipes, and the bundle goldens are real. A determinism break (replay divergence on a parallel-pipe draw; bundle state serialized where it shouldn't be; Packet.edge semantics changed) is a blocker.
- **CORE ENGINE-FREE (ODN-1)** — `bundles.odin` lives in `package core`; zero engine imports (the minion's slice-1 precedent holds).
- **W1/W2 CARRY-FORWARDS FROM 1.4 MUST LAND (Perkins r1 on #24 flagged them).** W1 = the headless app-layer restart test (restart → fresh seed, full FSM cycle, no state leakage); W2 = the LOSE-loop replay test (a losing run replays byte-identical). Verify both are present + real in this PR's test pass (the minion claims they landed). A missing/wrong carry-forward is a legitimate finding.
- **CONTEXT — the minion flagged a 2.3-severance concern for the 2.2 minion (in the PR's Decisions & rationale):** when a representative pipe is demolished but the bundle survives (2.3 severance), `Packet.edge` may point to a dead pipe. This is a FUTURE-story concern (2.3), NOT a 2.1 defect — do NOT flag it as a blocker here (it's a documented carry-forward note for the downstream story).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slice 1 complete: 1.1 spine + 1.2 window/draw + 1.3 per-hop + 1.4 win/lose IN), not `main`. Don't flag "wrong base."
- **The prototype is REFERENCE-ONLY** (`~/code/packet-plumber-prototype-ref/` — mine its bundle RENDERING, rebuild the logic clean; its routing was NOT the locked model). Do NOT flag "should port the prototype's bundle logic."
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas synced it). Review the PR content as-is at the sha.
- **Do NOT re-open 1.1–1.4 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- **A round-robin / weighted-LB pattern** in the routing path (or the grep-gate failing to catch one) — a blocker (the load-bearing invariant).
- **A dynamic (per-packet/mid-flow) capacity computation** instead of the static table-build sum — a blocker.
- **A determinism break** (a parallel-pipe draw replays differently; bundle state serialized where it should stay derived; `Packet.edge` semantics broken) — a blocker.
- **An engine type leaking into `package core`** (ODN-1) — a blocker.
- **The W1/W2 carry-forward tests missing or fake** (headless restart test + LOSE-loop replay test).
- **The merge-pop non-deterministic** (the animation frame varies run-to-run).
- An `odin test` / `odin build` / `harness` failure at `cb497ab`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 25 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `cb497ab`), `spec_files` = this briefing + the job briefing + Story 2.1 + the architecture (rule 3, `[RR]`, `[ODN-10]`, §11.7, ODN-1/9/10/11) + GDD E1.5/E1.4, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.1-bundles/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 25 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 25 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `cb497ab`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-2.1-bundles / **Reviewed sha:** cb497ab / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-2.1-bundles-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. **BURST WARNING (live this session): an 8-pane glm fan-out tripped the ZAI account rate-limit (429, code 1302) TWICE.** The headless mode's concurrent dispatch is the risk — **stagger/batch the lens spawns (≤4 concurrent) or accept + recover via one continue per 429'd pane** (short-window burst). If the orchestrator's own turn 429s, one continue revives it.
