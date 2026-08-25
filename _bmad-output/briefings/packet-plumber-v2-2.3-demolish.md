# Briefing: packet-plumber-v2-2.3-demolish

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (slice 1 + 2.1 bundles + 2.2 ECMP all in). **PR targets `v2`.**
- **Story:** stories-v2 **Story 2.3 — Demolish + severance under bundles + automatic migration**. **Closes slice 2.**
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (atomic-batch ordering, E29 no-stale-route, determinism over a demolish mid-traversal).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down).
- **bmad-quirk heads-up:** verify every edit lands in YOUR worktree (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Add **demolish** — and this is the story where the locked routing model **earns its keep**. Demolishing a pipe of a bundle **shrinks the pool gracefully** (only full-bundle-loss drops the route); terminal-demolish is forbidden; junction demolish is an atomic batch; and **in-flight packets re-forward at the next junction automatically** (no stale routes — the per-hop-forwarding payoff the prototype's spawn-cached BFS *could not do*). Slice 1–2.2 built the model; 2.3 *exercises* it under topology change.

## The story (from stories-v2 Story 2.3 — read the full card)
- **Slice 2 · Epics E1.3, E1.4 · Systems:** Topology demolish (S1), Flow reroute (S2).
- **Goal:** demolish a bundle member → graceful shrink (traffic continues, no hard cut); only **full-bundle-loss drops** the route `[E1, RR]`; terminal-node demolish rejected `.Terminal_Demolish` `[E2]`; junction demolish = **atomic batch** (incident pipes first in edge-id order, each per E1, then the vertex) `[E27]`; in-flight packets **re-forward at the next junction** (no stale spawn-time routes) `[E29]`; replay byte-identical.

## Carry-forwards
- **2.1** (bundles) — demolish a bundle member shrinks the pooled capacity (re-derives; cap = sum of survivors).
- **2.2** (ECMP) — a demolish that removes one equal-cost path leaves the other(s); the hash re-distributes deterministically.
- **Slice 1** (per-hop flow + the table-rebuild rule 1) — **E29 is structural here**: no cached route, so a demolish → table rebuild → packets re-forward at the next junction with zero special-casing. The flow already has the defensive "pipe vanished mid-traversal → drop back to departure node + re-forward" path (flow.odin); 2.3 makes it live.
- **Bidirectional-draw gap** (surfaced in playtest): while you're touching topology edits, **add `test_reverse_draw_is_bidirectional`** to `core/flow_test.odin` (draw both pipes reversed `rt→res` + `host→rt`, assert the `res→host` packet still delivers). The existing tests only draw forward — this closes the gap. (Test body: mirror `test_per_hop_forwarding_source_to_sink` but reverse the `draw` args.)

## From-scratch mandates (the locked-model discipline — load-bearing)
- **Demolish is a logged command** (like draw) — applied via the validate→apply path, recorded in the action log, replay-reapplied at its tick. Deterministic.
- **Graceful shrink, not a hard cut** — a bundle member demolish reduces pooled capacity (re-derive); traffic continues. Only **full-bundle-loss** (all members gone) drops the route `[E1]`.
- **`.Terminal_Demolish`** — terminal nodes can't be demolished `[E2]`; reject with the typed error.
- **Junction demolish = atomic batch** `[E27]` — incident pipes first (edge-id order, each per E1), THEN the vertex. One atomic edit (replay-deterministic).
- **E29 auto-migration is structural** — NO cached route; the table rebuilds on the demolish (rule 1) and in-flight packets re-forward at the next junction. A Perkins lens-guard confirms no `route[]`/spawn-cached path creeps in.
- **Determinism** — a demolish mid-traversal replays byte-identical (T1); the post-demolish frame is deterministic (T2).
- **No engine types in `package core`** (ODN-1).
- **Golden:** T1 + T2 of the post-demolish state.

## Source material (read)
1. **`_bmad-output/planning-artifacts/sprints/stories-v2.md`** — Story 2.3 (full card, line 199+) + the slice-2 exit criteria.
2. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — E1 (severance-under-bundles), E2 (terminal-forbidden), E27 (junction-batch), E29 (auto-migration), the 4-rule spine (rule 1 = table rebuild), `[RR]` routing, §11.7 headless-test contract.
3. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — E1.3 (demolish), E1.4 (routing/reroute).
4. **Prototype reference (read-only):** `~/code/packet-plumber-prototype-ref/` (mine its demolish UX/feel; its routing was NOT the locked model — the reroute logic is rebuilt clean).

## Verify
- Demolish a bundle member → pooled capacity shrinks, traffic continues; demolish ALL members → route drops `[E1]`.
- Terminal demolish → `.Terminal_Demolish` `[E2]`; junction demolish → atomic batch, incident pipes first in edge-id order `[E27]`.
- In-flight packet on a demolished pipe → re-forwards at the next junction (no stale route) `[E29]`; a demolish that severs the path → packet re-routes via surviving equal-cost paths (2.2).
- Demolish mid-traversal replays byte-identical (T1); post-demolish frame deterministic (T2, structural/hash-verified — pixel deferred per the rlsw-harness gap).
- `test_reverse_draw_is_bidirectional` added + passing (the carry-forward).
- `odin test` + `odin run harness` green; core still engine-free.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-2.3-demolish working` at start
- `bin/ledger set packet-plumber-v2-2.3-demolish in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-2.3-demolish <url>`
- `herdr notification show "pp-v2-2.3" --body "<one-line>"` on finish
- Final message: the demolish summary, the E29 auto-migration verification, the slice-2-closure confirmation, whether slice 3 is next.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-2.3-demolish · **base: v2**
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: (none)
- **PR target: v2** · descriptive tab label `pp-v2-2.3-demolish`
