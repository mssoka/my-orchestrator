# Perkins briefing — round 1: packet-plumber-v2-5.1-map-growth

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/51 (targets `v2`)
- **Reviewed sha:** `ef858e880fcde8f59d3e4c7656e3f76638afc6b3` (short `ef858e8`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.1-map-growth-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.1-map-growth.md` + the story 5.1 card in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + arch §S1 (Topology), `[ODN-7]` (director seam), `[E31]` (spawn validity), `[ODN-6]` (portable-core re-sim) + the 3.5 amendment commit 9a5a35b (routers never director-spawned).
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Local verification at the sha remains ground truth.

## What the PR does (review scope)

**Story 5.1 — the map must GROW (GDD Mini Motorways model):** nodes appear over
time, deterministically from the seed; growth proceeds outward from the
player-placed router mesh; every spawned terminal is connectable.
- **Determinism spine:** growth fully seed-derived (derive, don't record) — timing
  = tick % 120 (executed tick), placement = the owned RNG stream (type pick +
  bounded rejection draws), mesh/validity = the topology. NO action-log entries, NO
  LOG_VERSION bump. Spawned terminals ride the existing topology section of the T1
  hash. Proofs: replay byte-identity test, same-seed identity test, growth.dem T1 +
  replay gate, new drift-check growth_flip class (a growth-toggled replay diverges
  loudly).
- **E31 spawn validity:** every spawn is in-bounds + min-separated from every node
  and pipe segment (integer segment distance, no division) + connectable-within-span
  of a junction (era-unlocked tier: 14 era 1, 18 era 3); invalid candidates
  rejection-sampled from the same rng stream, bounded (8 attempts), NO wall-time
  retry loops.
- **Routers NEVER director-spawned** (3.5 amendment): growth spawns terminals only,
  waits until the player places the first router; the player's mesh is the growth
  anchor.
- **Director seam [ODN-7]:** growth.odin is the pressure-family branch (sibling of
  demand.odin), reading a read-only topology view, applied by Topology.
- **Golden stability:** growth tuning as core consts (NOT balance.json — catalog
  edits are golden-poisoned); existing 27 demos byte-identical/unshifted; new
  growth.dem + goldens (T1 + T2 ×4).
- Swarm fixes already applied: same-tick re-step double-spawn → growth_last_tick
  guard + pin test; growth on era-0 → fail-loud parse guard; doc fix + drift
  hardening.
- Verification: 177 core tests, 28/28 demos (T1+T2+replay), drift-check 196
  mutations rejected, lint, app + PP_DEBUG builds.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — determinism spine.** Growth derives ONLY from the seed + the
  executed tick (the rng stream): NO wall-clock timing, NO wall-time retry loops, NO
  hidden nondeterminism (e.g. hash-map iteration order, environment-dependent
  geometry). Same seed → IDENTICAL growth timeline; replay stays byte-identical (a
  replayed run grows the same map at the same ticks with zero logged input). The
  growth_flip drift class proves a growth-toggled replay diverges loudly. Any
  nondeterministic path = a blocker.
- **🚨 Derive-don't-record integrity:** growth must NOT need log entries (no
  LOG_VERSION bump) — verify the replay byte-identity holds WITHOUT growth entries
  (if any run-scoped growth parameter was serialized, that's a LOG_VERSION question
  and must follow the 5.8 3→4 discipline). The topology section of the T1 hash
  carries the growth state.
- **E31 validity exact:** every spawn in-bounds + min-separated (integer distance)
  + connectable-within-span of a junction (14 era 1 / 18 era 3); rejection sampling
  bounded (8 attempts) from the SAME rng stream — a spawn that violates E31 or a
  wall-clock retry = a blocker.
- **Routers NEVER director-spawned** (3.5 amendment, 9a5a35b): growth spawns
  TERMINALS ONLY; a director-spawned router = a blocker (the amendment is
  load-bearing canon).
- **Golden stability:** all 27 pre-existing demos' goldens byte-identical/unshifted;
  growth tuning in core consts (NOT balance.json — a catalog edit = golden-poisoned
  = a blocker); the new growth goldens byte-stable.
- **Base = `v2`** — includes the full shipped line (5.5/5.6/5.3/5.7/5.3-ux/5.8).
  Carry-forward only; do NOT re-open settled findings (the 5.8 golden-fold discipline
  and the 5.7 determinism contract are settled).
- **Scope guard:** map growth ONLY — no health states (5.2), no touch/controller
  (5.4), no new packet types, no economy.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.1-map-growth/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.1-map-growth/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.1-map-growth-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
