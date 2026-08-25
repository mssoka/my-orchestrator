# Perkins briefing — round 3 (FINAL automated): packet-plumber-traffic-model-design

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/53 (targets `v2`)
- **Reviewed sha:** `42e4eb69d79ab8c9103ba0b61d39ae15510c2d1a` (short `42e4eb6`) — the r2 rework push
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 3 of 3 — **FIX-AUDIT on the r2 rework** (`prior_findings` = r2). **This is the last automated round** — after this the human takes over.
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r3` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md` + **r2's `consolidated.json`** at `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (prior_findings — fix-audit FIRST) + the r2 review body (4945108979).
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Docs/canon PR — local verification + diff checks are the ground truth.

## What the r2 rework claims (r2 → r3 delta to audit)

r2 = NEEDS CHANGES (B1 fractional-state violation of ODN-10; W2-W7). The minion's
r3 push claims:
- **B1** — re-spec in INTEGER/FIXED-POINT: milli-packet credit accrual,
  `cap_fraction_permille` (int permille) + int pair, MAX_CREDIT 2 covered —
  coherent across spec Thread 2 + card 5.9 + GDD M6 + decision-log. ODN-10-
  compliant (integer-only state paths; catalog parse_integers + jint_strict
  loadable).
- **W2** — state home moved to **Flow_State beside lane_caps** (flow.odin:96),
  updated in place by the flow.odin §1b pass (accrue + consume); the "rebuilt by
  the spawn pass" contradiction removed; card 5.9's Systems line points at flow,
  not demand.odin.
- **W3** — decision-log item 4's "data change, not a code change" falsehood fixed.
- **W4** — MAX_CREDIT type-relative: `MAX_CREDIT_MILLI = 1000 × max(1, ceil(cap))`;
  campus 150 u/s (2.5 pkts/tick) → ceiling 3, achieves its cap long-run, no silent
  clamp.
- **W5** — residential ceiling 1 → no burst; the 600ms > 500ms latency math
  verified; W10 pin asserts burst-transit ≤ tolerance.
- **W6** — W9/W10 pins now QUANTITATIVE (rate envelopes on a known seed: spawns ≤
  cap × window + burst allowance, credit ≤ MAX_CREDIT, ≥ 0.95 × expected surge
  volume).
- **W7** — unit-test re-pin surface named: demand_test.odin (volume/histogram +
  effective_volume surge pin), flow_test.odin, determinism_test.odin, with
  positive/negative assertions.
- Notes: N1 E24 pin cited at sla_test.odin:88 (sla_check_invariant); N5 card
  5.10's wrong [E3] tag removed; N8 GROWTH_MIN_SEP_TILES at :76; N9 "never at
  endpoints" scoped to director-spawned demand (legacy §1a flow_seed_demand
  exempt); N11 provenance disclaimer added to the decision-log entry.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **Fix-audit mandate (final round):** verify each r2 finding's fix BITES: B1's
  re-spec is genuinely integer/fixed-point and LOADABLE (catalog.odin parse —
  parse_integers + jint_strict accepts the permille/int-pair form; no residual
  float state); W2's Flow_State home is real (flow.odin:96 beside lane_caps, in-
  place accrue/consume — the cross-tick accrual actually persists); W4's
  type-relative ceiling covers campus; W5's no-burst + transit pin; W6's pins are
  quantitative; W7's re-pin surface is named + coherent.
- **🚨 LOAD-BEARING (carried):** section-additive only, NO terminology rewrites;
  no code/balance.json changes in this docs PR; determinism constraints stated
  correctly (derive-don't-record — a serialized state home would be a LOG_VERSION
  question; the spec must keep spawn_credit derived/never-serialized with its T1
  surface stated).
- **This is round 3/3:** deliver the verdict as cleanly as possible — approve if
  blockers are zero; a blocker here sends it to the human (cap hit), so be precise
  about what is a genuine blocker vs. advisory.
- **Base = `v2`** — carry-forward only; do NOT re-open settled findings.
- **Scope guard:** design docs + story cards ONLY.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3`, `prior_findings` = the r2 `consolidated.json`. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-traffic-model-design-perkins-r3 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
