## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-2.3-demolish · **Reviewed sha:** `8a652dd` · **Reviewers:** 7/7 completed
**Verification:** 4/5 reviewer findings confirmed against the code — 1 discarded as false-positive

7 lenses ran (blind, edge, acceptance, security, architecture, codebase, tests) on `zai-coding-cn/glm-5.2`. All named contracts were re-verified against the worktree at `8a652dd`, plus ground-truth: `odin test core` = **54/54 pass**, core is **engine-free (ODN-1)**, the **demolish T1 golden replays byte-identical** (harness PASS, 80 ticks), and **drift-check rejects all 41 mutations** across 7 demos (ODN-11 gate bites — incl. demolish `catalog_hash`/`logic_hz`/`bad_magic`/`bad_version`/`bad_tag`/`truncated`).

### Blockers (0)
None.

### Warnings (0)
None.

### Notes (4)

**N1 — Same-tick draw + demolish apply in append order, not demo file order** `note` · `[edge]` · `harness/run.odin:25,37`
`lower_intents` appends every draw (loop over `demo.draws`) before every demolish (loop over `demo.demolishes`); `step` applies a tick's batch in action_log order. Deterministic (live==replay both use the stored log). Only a same-tick draw+demolish targeting the same entity could diverge from a demo author's file-order expectation; no shipped demo hits this. *Fix (optional):* stably sort `action_log` by `apply_tick` with file-order tie-break, or document that same-tick draws always precede same-tick demolishes.

**N2 — `Edit_Result.id` field comment is stale (mentions draw only)** `note` · `[codebase]` · `core/types.odin:31`
Field comment reads `// the new pipe id on a successful draw`, but `topology_apply_edit` now also returns the demolished entity id (`{id=c.pipe}`/`{id=c.node}`). The proc-level doc was updated; only this field comment wasn't. *Fix:* `// the new pipe id on a draw, or the demolished entity id on a demolish`.

**N3 — E27 incident-pipe demolition order asserted by count only, not by order** `note` · `[tests]` · `core/demolish_test.odin:test_demolish_junction_atomic_batch`
The atomic-batch test asserts `pipe_count==0` (count), never the incident-pipe *order*. `apply_demolish_node` tombstones idempotently with no per-pipe event, so order is state-unobservable today; the slot-order scan + monotonic ids hold the contract (verified), and the replay keystone catches non-determinism. A *deterministic* wrong-order regression isn't directly caught until slice-3 severance events make the order observable. P3 latent gap, no current defect. *Fix (when slice-3 lands):* assert the emitted pipe-id sequence is ascending id order.

**N4 — Advisory test gate: PASS** `note` · `[tests]`
P0 100% (E2/E27-batch/E1-graceful+full-loss/E29-reforward/replay-determinism all FULL, incl. a >2-incident-pipe batch in the replay keystone); P1 100% (E11-ids/missing-dead rejections/binary round-trip/bidirectional-draw carry-forward/cull-stranded all FULL); overall >95%. Meets PASS thresholds.

### Reviewer agreement
No multi-source findings (all four notes are single-source). Highest-confidence signals are the ground-truth checks above, not reviewer overlap.

### Verdict
**READY TO MERGE** — 0 blockers, 0 warnings. The locked routing model earns its keep: E29 auto-migration is structural (no cached route — a demolish → table rebuild → in-flight packets re-forward at the departure junction), E1 graceful shrink holds (bundles re-derive from live members only; full-bundle-loss drops the route), E2/E27 are correct and replay-deterministic. The 4 notes are advisory (1 doc nit, 1 demo-authoring ergonomics, 1 P3 test-assertion gap, 1 gate-PASS).

_Re-review semantics: address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
