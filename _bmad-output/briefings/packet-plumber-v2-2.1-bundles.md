# Briefing: packet-plumber-v2-2.1-bundles

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (@ `1e8ebe9` — slice 1 is COMPLETE: 1.1 spine + 1.2 window/draw + 1.3 per-hop flow + 1.4 win/lose all in). **PR targets `v2`.**
- **Story:** stories-v2 **Story 2.1 — Parallel-pipe bundles (cap = sum)**. **First story of slice 2** ("routing the locked way: bundles → ECMP → demolish").
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (the no-LB grep-gate, determinism over the merge-pop).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **bmad-quirk heads-up:** verify every edit lands in YOUR worktree (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Add **bundles**: parallel pipes between a node pair **bundle into one pooled-capacity link** (cap = sum of members), derived from adjacency at table-build time. This is the locked routing model extended from slice 1's single-path — **redundancy becomes active capacity the moment a second pipe is drawn.** The load-bearing discipline: a bundle is **one fat edge** to the routing, NOT round-robin/load-balanced across the individual pipes.

## The story (from stories-v2 Story 2.1 — read the full card)
- **Slice 2 · Epics E1.5, E1.4 · Systems:** Topology bundles (S1), render bundle viz.
- **Goal:** parallel pipes between a node pair → one pooled link (cap = sum), computed as a **static sum at table-build time** (4-rule spine rule 3); a merge "pop" animation when pipes join a bundle.
- **Then:** routing sees **one fat edge per pair**; **NO load balancing** (round-robin/weighted LB are **DELETED**, grep-gated absent) `[RR]`; bundle-capacity-equals-sum unit test passes; bundled-link frame matches the T2 golden.

## Carry-forwards
- **Slice 1** (all in v2) — the per-hop forwarding + topology + render + win/lose loop this grows onto.
- **W1/W2 test-debt from 1.4** (Perkins r1 flagged, carried here): add a **headless app-layer restart test** (restart → fresh seed, full FSM cycle) + a **LOSE-loop replay test** (a losing run replays byte-identical). These close the 1.4 coverage gaps; land them in this story's test pass.

## From-scratch mandates (the locked-model discipline — load-bearing)
- **Static sum at table-build** (4-rule spine rule 3) — capacity computed once at table-build, never dynamically mid-flow.
- **NO load balancing** — a bundle is ONE pooled edge. Round-robin/weighted-LB patterns must be **absent** (a Perkins lens-guard greps for them; ECMP, in 2.2, is a *hash*, not LB). This is the same anti-spawn-time-route / anti-BFS discipline slice 1 enforced.
- **Determinism holds** — the bundle state is IN the state hash (T1 golden), so a parallel-pipe draw replays byte-identical; the merge-pop is itself deterministic.
- **No engine types in `package core`** (ODN-1).
- **Golden:** T1 (bundle state in the hash) + T2 (the merge-pop frame).

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 2.1 (full card) + the slice-2 framing (line 152+).
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — the 4-rule spine (rule 3 = static sum), `[RR]` routing rules, `[ODN-10]` bundles, §11.7 headless-test contract.
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E1.5 (bundles / redundancy-as-capacity), E1.4 (routing).
4. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/` (mine its bundle RENDERING, rebuild the logic clean — the prototype's routing was NOT the locked model).

## Verify
- Two parallel pipes between a pair → one pooled link, cap = sum (unit test).
- Routing sees ONE fat edge per pair; **grep confirms no round-robin/LB patterns** (the lens-guard).
- Bundle state in the state hash → parallel-pipe draw replays byte-identical; merge-pop deterministic (T1 + T2 golden match).
- W1/W2 carried: headless restart test + LOSE-loop replay test pass.
- `odin test` + `odin run harness` green; core still engine-free.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-2.1-bundles working` at start
- `bin/ledger set packet-plumber-v2-2.1-bundles in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-2.1-bundles <url>`
- `herdr notification show "pp-v2-2.1" --body "<one-line>"` on finish
- Final message: the bundle summary, the no-LB grep-gate result, whether 2.2 (ECMP) is next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-2.1-bundles · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2** · descriptive tab label `pp-v2-2.1-bundles`
