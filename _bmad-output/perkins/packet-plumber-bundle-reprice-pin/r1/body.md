## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-bundle-reprice-pin · **Reviewed sha:** c42a9ec · **Reviewers:** 7/7 completed
**Verification:** 16/16 findings confirmed against the code — 0 discarded as false-positive

### Blockers (0)

### Warnings (1)

**1. The new pin dereferences `hops[off]` / `pipe_tier[rep_slot]` after non-fatal `expectf` checks — in the pin's own bite scenario (count 0) the asserts mis-read an unrelated hop row instead of the pinned message (7-lens agreement; repeats r1 note #3's shape, whose count-guard fix was not applied here)** *(blind, acceptance, architecture, codebase, edge, security, tests)*
`core/routing_cost_test.odin:254-258, 286-288`

Odin `testing.expectf` records and **continues**. With the re-pricing branch broken, `count == 0` and the subsequent `hops[int(off)].node` / `hops[int(off)].pipe` asserts read an unrelated Hop row (the PR body's own bite output shows the mis-reads: "got 3", "got 2"), and `pipe_tier[rep_slot]` indexes `-1` if no live member is found — misleading failure output instead of the pinned `count == 1` message. The pin still bites (the count expectf fails the run), so this is hygiene, not a hole — but r1 note #3 recommended exactly this guard and the new pin repeats the shape.
**Fix:** guard the hop-node/pipe asserts with `if ok && count == 1`, and the tier/pipe asserts with `if rep_slot != -1`.

### Notes (3)

**1. The pin's bite-vector comment says a broken re-pricing branch would "FLIP the route to m2" — the toggle-verified behavior (and the PR body's own bite output) is the route VANISHING (count 0)** *(acceptance, architecture, blind, codebase, edge, tests)*
`core/routing_cost_test.odin:223-226`

With `else if c < min_cost[ns]` disabled, per-pipe relaxation still gives `dist[m1]=5` but pass-1 `min_cost` stays 20, so pass-2 equality matches neither neighbor (5+20=25≠10, 10+10=20≠10) — count 0, route vanishes. The flip math (20+5=25>20) describes only a consistent first-seen model, which the toggle is not. Cosmetic: the body's bite-output line numbers (251/253/283) are 3–4 lines stale vs the committed file (254/256/286) — the pin was polished after the bite run; messages match verbatim.
**Fix:** reword comment (a) to describe the vanish (count 0); optionally refresh the body's line numbers.

**2. The reverse-direction expectf (host→res next hop m1) does NOT bite — it passes even with the re-pricing branch removed — and its "(re-priced bundle, 5+5=10)" attribution is misleading** *(edge)*
`core/routing_cost_test.odin:260-262`

Host→m1 is a single wide pipe (min == representative cost) and `dist[m1]=5` comes from per-pipe relaxation — both branch-independent. My toggle run failed exactly three asserts (count, forward node, representative pipe); the reverse assert did not fail. It still pins forward/reverse symmetry, but adds no re-pricing bite.
**Fix:** reword the reverse comment (the result holds with the branch broken), or make the reverse check re-price-dependent, or drop it.

**3. Advisory test gate: PASS** *(tests)*
P0 100%: the re-pricing branch genuinely executes (narrow drawn first, wide re-prices 20→5 — not vacuous) and is bite-proven (toggle → count 0). P1 100%: ECMP/next-hop forward + reverse, representative lowest-slot. P2 100%: pooled view (2 members, cap 45, tier wide). `odin test core` 127/127.

### Reviewer agreement
- **Unguarded `hops[off]`/`pipe_tier[rep_slot]` derefs after non-fatal checks** — all 7 lenses
- **Bite-vector comment "FLIP to m2" vs actual vanish** — 6 lenses

### Perkins' own verification (all reproduced at c42a9ec)
- `odin test core` **127/127** · `tools/lint.sh` **all gates green** · `tools/harness.sh run` **16/16 demos green** (T1 + T2 + replay)
- **Goldens byte-untouched**: diff = 1 file (+94/−0, test-only); `git status goldens/` clean — as claimed
- **Bite proof REPRODUCED independently**: toggling the re-pricing branch to first-seen-wins in a scratch worktree fails exactly the new pin with the PR body's signature (count 0 · "got 3" · "got 2", 126 others green) — the claimed toggle test is genuine; toggle restored, scratch tree removed
- **Pin is non-vacuous**: the wide member must take the `else if` path to re-price 20→5; the standard-tier path (min == representative) would not fire it
- **No mismatch with the r1 fuzz claim**: the green outcome matches the fuzz-verified behavior (400 graphs, 0 mismatches); no real bug surfaced

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
