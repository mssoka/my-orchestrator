# Perkins briefing — round 2: packet-plumber-traffic-model-design

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/53 (targets `v2`)
- **Reviewed sha:** `da3a50eaeafc62ad9474872fd6aad5a72906f4bd` (short `da3a50e`) — the r1 rework push
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 2 of 3 — **FIX-AUDIT on the r1 rework** (`prior_findings` = r1)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r2` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md` + **r1's `consolidated.json`** at `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r1/consolidated.json` (prior_findings — fix-audit FIRST) + the r1 review body (4945036620).
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Docs/canon PR — local verification + diff checks are the ground truth.

## What the r1 rework claims (r1 → r2 delta to audit)

r1 = NEEDS CHANGES (B1 fractional cap unenforceable on integer spawns; B2 cap
value > residential throughput; W3-W11). The minion's r2 push claims:
- **B1** — the cap is now a per-terminal SPAWN ACCUMULATOR: accrue cap/tick, spawn
  costs 1, MAX_CREDIT = 2 burst ceiling, eligible-set gating (one rng draw per pick
  preserved), state home named (`spawn_credit[terminal_slot]`, DERIVED — never
  serialized, T1 surface = the spawn stream), integer alternative (1 per N ticks)
  noted. In Thread 2, card 5.9, GDD M6, decision-log.
- **B2** — caps now THROUGHPUT-RELATIVE + UNIFORM: `cap(type) = CAP_FRACTION ×
  throughput ÷ packet_bandwidth` (0.5 → residential ≈ 0.083 pkts/tick = 2.5 u/s,
  ~2× headroom pre-5.10; content_host ≈ 1.33 long-run); invariant holds BY
  CONSTRUCTION (source demand ≤ a fraction of the terminal's own forwarding
  capacity); 5.9/5.10 DECOUPLED explicitly (5.9's zero-drop acceptance works at
  the current narrow).
- **W3** — the surge-explainer artifact is COMMITTED (html + 3 assets) — citations
  resolve. **W4** — GDD M1-vs-shipped reconciliation sentence added to M6.
  **W5** — group radius → ~4-6 tiles (≥ GROWTH_MIN_SEP_TILES = 3 + 1). **W6** —
  invariant scoped SOURCE-SIDE explicitly; sink concentration bounded by dst
  distribution + E9. **W7** — card 5.11 names the Terminal_Role touch points
  (enum, role_from_name, collect_terminals, growth type-pick). **W8** — M6 vs the
  six post-fun-gate mechanics disambiguated. **W9/W10** — post-cap surge-lands +
  one-subscriber-at-cap zero-drop pinned as card acceptances.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **Fix-audit mandate:** verify each r1 fix BITES: B1's accumulator spec is
  coherent with INTEGER spawns (core/flow.odin:646 `for k in 0..<vol`), the state
  home is named + derived/never-serialized + its T1 surface stated; B2's cap
  formula is uniform + the invariant holds by construction at the stated numbers
  (residential 5 u/s → 0.083 pkts/tick ≈ 2.5 u/s = ~2× headroom; content_host caps
  at/under its throughput); W3's committed artifact actually resolves the citations
  (git log --all contains the html); W5's radius ≥ GROWTH_MIN_SEP_TILES+1.
- **🚨 LOAD-BEARING (carried):** section-additive only, NO terminology rewrites
  (the terminology audit owns that — its Phase-2 PR serializes behind 5.2's merge);
  no code/balance.json changes in this docs PR; determinism constraints stated
  correctly per thread (derive-don't-record; a serialized state home would be a
  LOG_VERSION question). A code change or a terminology rewrite in this diff =
  a blocker.
- **Base = `v2`** — full shipped line; carry-forward only; do NOT re-open settled
  findings.
- **Scope guard:** design docs + story cards ONLY.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2`, `prior_findings` = the r1 `consolidated.json`. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-traffic-model-design-perkins-r2 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
