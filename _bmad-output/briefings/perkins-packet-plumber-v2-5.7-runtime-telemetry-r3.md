# Perkins briefing — round 3 (final automated): packet-plumber-v2-5.7-runtime-telemetry

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/47 (targets `v2`)
- **Reviewed sha:** `47494702c1a460ddc281f1381a7489111881d70d` (short `4749470`) — the r2 rework push
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 3 of 3 — **FIX-AUDIT on the r2 rework** (`prior_findings` = r2). **This is the last automated round** — after this the human takes over.
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r3` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.7-runtime-telemetry.md` + **r2's `consolidated.json`** at `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r2/consolidated.json` (prior_findings — fix-audit FIRST, carry-forward markers) + the r2 review body (4941186683).
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing FIXED (checks green); local verification at the sha remains ground truth.

## What the r2 rework claims (r2 → r3 delta to audit)

r2 = NEEDS CHANGES (R2-B1 aggregation-shape pin, R2-B2 gate, R2-W1 vacuous bundle
pin, R2-W2 harness PP_DEBUG gate, R2-W3 empty-token, R2-W4 free_all). The minion's
r3 push claims:
- **R2-B1** — discriminating pin: (a) assert no two `rec.drops` rows share
  (pipe,class,reason), (b) the known tick-12 tuple (pipe 1, class 1, reason 0,
  count 2) asserted verbatim (fixture-probed first — era-3 director demand
  produces the count-2 aggregation).
- **R2-B2** — gate passes (aggregation shape + non-vacuous bundle loads + harness
  PP_DEBUG CI line).
- **R2-W1** — bundle-replication pin now computes MID-FLIGHT at tick 3 (not the
  drained tick-20): member loads asserted identical AND non-zero (carried=30,
  util=100).
- **R2-W2** — CI PP_DEBUG gate compiles the harness too
  (`odin build harness -define:PP_DEBUG=true`) — covers overlay.odin + the
  overlay-check dispatch.
- **R2-W3** — `--stats-out ""` (unset shell var) is now a usage error, exit 2, in
  BOTH CLIs (flag-seen tracked separately); all four error shapes verified live
  (dangling/duplicate/empty/flag-shaped → exit 2; valid → exit 0).
- **R2-W4** — the app loop calls `free_all(context.temp_allocator)` once per frame;
  the per-step `state_hash` no longer grows the temp arena unboundedly at 20 Hz.
- Notes: N1 (555KB → 369,452 B), N2 (harness rejects `-`-prefixed path tokens),
  N3 (app*.bin gitignore), N4 (dead captures deleted), N5 (fmt_tmp shim dropped),
  N6 (builder comment corrected), N7 (draw_heat_tints guards node_slot ok),
  N9 (literal CSV row of each kind pinned).
- Verification claimed: 165 core tests (158+7), lint 6/6, 25/25 demos goldens
  byte-identical, stats-check byte-identical ×4 demos, app + harness build in
  plain AND PP_DEBUG variants, CI YAML valid, .gitignore covers the CI binary.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **Fix-audit mandate (final round):** verify each r2 finding's fix BITES — R2-B1's
  discriminating pin fails on a per-event regression (both directions); R2-W1's
  mid-flight pin asserts non-zero loads (0==0 vacuity gone); R2-W3's empty-token
  path actually exits 2; R2-W2's harness gate is in CI. Do NOT re-litigate what r1/r2
  verified — carry forward via the consolidated.json.
- **🚨 LOAD-BEARING (carried):** the determinism contract — the stats stream is
  derived ONLY from existing deterministic state (NO wall-clock, NO render sampling);
  the one-CSV-serializer byte-identity contract (harness == app) and replay-identity
  (live == replay) must hold at 4749470. The overlay stays golden-safe (compile-
  excluded from non-PP_DEBUG builds, off by default, unreachable from capture). Any
  new nondeterminism or a golden shift = a blocker. R2-W4's `free_all` must not
  affect determinism (temp arena is scratch, not state).
- **Base = `v2`** — 5.3 pause + 5.5/5.6 + the 5.7 line; carry-forward only; do NOT
  re-open settled findings.
- **Scope guard:** telemetry export + overlay only. Sibling 5.3-pause-ux (PR #49, a
  presentation-only overlay change on app/main.odin) may be reviewed in parallel by
  another round — its file set overlaps app/main.odin presentation paths; if it
  merges mid-round, carry-forward only.
- **This is round 3/3:** deliver the verdict as cleanly as possible — approve if
  blockers are zero; a blocker here sends it to the human (cap hit), so be precise
  about what is a genuine blocker vs. advisory.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r3`, `prior_findings` = the r2 `consolidated.json`. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.7-runtime-telemetry-perkins-r3 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
