# Perkins briefing — round 1: packet-plumber-bundle-reprice-pin

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/38 (targets `v2`)
- **Reviewed sha:** `c42a9ec3b4362005a008cc782003b62c98a6e0ac` (short `c42a9ec`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-bundle-reprice-pin-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-bundle-reprice-pin.md` + YOUR OWN r1 artifacts from Job A: `/Users/moses/code/_bmad-output/perkins/packet-plumber-routing-bandwidth-cost/r1/` (body.md + consolidated.json — the W1 wording + the branch it names: the mixed-tier bundle re-pricing branch, `core/routing.odin:221-225`, `else if c < min_cost[ns]`).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**TINY diff — the W1 follow-up pin:** +94 lines test-only in `core/routing_cost_test.odin`: a dedicated pin for the mixed-tier bundle re-pricing branch (parallel narrow(20)+wide(5) pipes between a pair; edge priced at min member cost (5); ECMP/next-hop reflects it; representative Hop.pipe stays the lowest-slot member). The minion claims a bite-proof (toggle test) + goldens byte-untouched.

## ⚠️ CRITICAL lens-guards (this is a PIN review — scope is the pin itself)

- **Verify the pin pins the RIGHT branch:** the mixed-tier bundle re-pricing path (`else if c < min_cost[ns]` — a fatter later member re-pricing a bundle edge). A pin that exercises only the standard-tier path (where min == representative cost) is VACUOUS (the exact r1 W1 gap — do not accept a re-wrap of the same hole).
- **Verify the pin asserts the LOCKED behavior:** edge priced at the min member cost; the ECMP/next-hop reflects it; the representative `Hop.pipe` stays the lowest-slot member. Assertions must be on the routing table + next-hop behavior, not just "no crash".
- **Verify the bite-proof claim:** the PR body must document the toggle test (temporarily breaking the re-pricing logic → pin fails → restored). A claimed-but-absent proof = a finding.
- **Verify goldens are byte-untouched** (0 diffs in goldens/ — the minion claims this; an undocumented golden shift = a blocker).
- **Test-only scope:** any production-code change in this diff = a finding (the scope guard says none).
- **BASE = `v2`** (Job A merged — the Dijkstra model is settled; do NOT re-litigate the cost model, the splice-proof re-bless, or anything beyond the pin).
- **Em-dashes OK in PP.**
- **NOTE:** your own r1 fuzz-verification (400 graphs, 0 mismatches) is the ground truth for the branch's correctness — the pin should MATCH that behavior. If the pin reveals a mismatch, that is a REAL finding (the minion was told to STOP and flag, not silently patch).

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-bundle-reprice-pin/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the job briefing + the W1 artifacts, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-bundle-reprice-pin/r1`, `prior_findings` = N/A (first round). Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-bundle-reprice-pin-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
