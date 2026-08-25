# Briefing: packet-plumber-v2-2.2-ecmp

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (@ `ff757d3` — slice 1 complete + 2.1 bundles in). **PR targets `v2`.**
- **Story:** stories-v2 **Story 2.2 — ECMP across equal-cost next hops**. Slice 2, story 2 of 3 (bundles ✓ → **ECMP** → demolish).
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (hash purity, no sim-rng/map-iter in the hot path, flow affinity).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **bmad-quirk heads-up:** verify every edit lands in YOUR worktree (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Add **ECMP**: among N equal-cost next hops, the pick is a **pure hash** — `splitmix64(src, dst, class, pkt_id) mod N` — deterministic per packet (flow affinity, no intra-flow reordering). This is the locked routing model's multi-path piece: slice 1 was single-path, 2.1 pooled parallel pipes into one fat edge, **2.2 spreads across equal-cost paths** — and it does so without touching sim-rng or iterating a map in the hot path (4-rule spine rule 2).

## The story (from stories-v2 Story 2.2 — read the full card)
- **Slice 2 · Epic E1.4 · Systems:** Flow ECMP (S2) `[ODN-9/10]`.
- **Goal:** N equal-cost next hops → pick = pure hash `splitmix64(src, dst, class, pkt_id) mod N`; deterministic per packet; no sim-rng draw; no map iteration in the hot path (4-rule spine rule 2).
- **Then:** packets **deterministically spread** across equal-cost paths; the **same packet always takes the same path** on every replay (flow affinity, no intra-flow reordering); re-running `(seed, action_log)` yields **byte-identical per-packet paths** `[E10, ODN-10]`; the ECMP-determinism unit test passes.

## Carry-forwards
- **2.1** (bundles) — ECMP spreads across equal-cost next hops, which may themselves be bundled edges; 2.1's pooled-capacity model is the substrate.
- **Slice 1** (per-hop flow) — the forwarding loop this slots into; 2.2 just changes single-next-hop → hash-over-equal-cost-set.
- **T2 pixel-harness gap** (deferred from 2.1): the T2 golden here (packets split across paths) is also pixel-unverified until the `rlsw` harness exists — **structural/hash verification stands in**; flag in your final message whether building that harness should be a mini-story before slice 2 closes.

## From-scratch mandates (the locked-model discipline — load-bearing)
- **Pure hash, no sim-rng** (4-rule spine rule 2) — the routing decision is `splitmix64(src,dst,class,pkt_id) mod N`, a pure function of packet identity. **Never** a sim-rng draw; a Perkins lens-guard greps for sim-rng in the routing path.
- **No map iteration in the hot path** — the equal-cost next-hop set must be **array-indexed** (so `mod N` is deterministic); iterating a map would break determinism (map order is undefined). Lens-guard checks this too.
- **Flow affinity** — same `(src,dst,class,pkt_id)` → same path, every replay; no intra-flow reordering.
- **Determinism holds** — per-packet paths are IN the state hash (T1) and replay byte-identical `[E10]`; the split frame is deterministic (T2).
- **No engine types in `package core`** (ODN-1).
- **Golden:** T1 (per-packet paths in the hash) + T2 (packets split across paths).

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 2.2 (full card, line 179+).
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — the 4-rule spine (rule 2 = pure hash, no sim-rng/map-iter), `[ODN-9/10]` ECMP, `[E10]` replay-equality, `[RR]` routing rules, §11.7 headless-test contract.
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E1.4 (routing / ECMP).
4. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/` (mine its multi-path DESIGN only — its routing was NOT the locked model; rebuild clean).

## Verify
- Diamond topology (2 equal-cost paths) → packets spread via the hash; **same packet → same path every replay** (flow affinity).
- Re-run `(seed, action_log)` → byte-identical per-packet paths `[E10]`; ECMP-determinism unit test passes.
- Grep confirms: **no sim-rng in the routing path, no map-iter in the hot path** (the lens-guards).
- Per-packet paths in the state hash (T1); split frame deterministic (T2, structural/hash-verified — pixel deferred per carry-forward).
- `odin test` + `odin run harness` green; core still engine-free.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-2.2-ecmp working` at start
- `bin/ledger set packet-plumber-v2-2.2-ecmp in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-2.2-ecmp <url>`
- `herdr notification show "pp-v2-2.2" --body "<one-line>"` on finish
- Final message: the ECMP summary, the hash-purity/no-map-iter lens-guard results, the T2-pixel-harness recommendation, whether 2.3 (demolish) is next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-2.2-ecmp · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2** · descriptive tab label `pp-v2-2.2-ecmp`
