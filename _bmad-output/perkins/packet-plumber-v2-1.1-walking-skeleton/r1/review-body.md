## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-1.1-walking-skeleton · **Reviewed sha:** 0419ba6 · **Reviewers:** 7/7 · **Verification:** 4/4 findings confirmed against the worktree (6 raw → 4 unique after dedup; 0 rejected)

**Determinism spine — verified empirically, not by claim:**
- **ODN-1** ✅ `core` imports nothing forbidden (only `core:testing`, in `_test.odin` only); `tools/lint.sh` 4-gate purity check is green. The `core` obj build carries only allocator-runtime syscalls (`close`/`fstat`/`fsync`/`getenv`) — **zero** `core:time` / `vendor:*` / clock / entropy symbols. (The literal "no `core:os` symbols in the object" phrasing is unsatisfiable as written: user `package core` collides with Odin's runtime `core` for obj-output naming — already documented in `ci.yml`, which makes the import lint the authoritative gate. That gate holds.)
- **ODN-9** ✅ An **independent** splitmix64→PCG32-XSH-RR reference reproduced the `seed 0` first-8 and `seed 42` first-4 vectors **exactly** — the vectors pin the canonical-correct impl, not a test written to match a wrong one.
- **ODN-10** ✅ No floats, no `map` iteration anywhere in `core` (grep + lint gate 3).
- **ODN-11** ✅ `state_hash` covers seed / tick / **rng.state + rng.inc** / era / catalog_hash / logic_hz / tick_nonce / action_log / applied / **events**; `boot.log.bin` decodes perfectly (magic `PPL1` / v1 / seed 42 / era 0 / catalog_hash `52075c6ea4c9f1b2` / logic_hz 20 / count 0).
- **E10** ✅ `test_replay_byte_identical` is real — two independent `Run_State`, 300 ticks, non-vacuous sanity (`applied==3`, `hashes[0]!=hashes[1]`). All 8 `odin test core` green.
- **ODN-17** ✅ Negative controls **bite**: `logic_hz 20→21` → `FAIL` (catalog + logic_hz + tick drift); catalog-only drift via `harness replay` → `"catalog drift … (defined rejection, ODN-11)"`, exit 1. The gate is not a mask.
- **From-scratch** ✅ Clean rebuild of the prototype's proven *design* (symbolic constants, modernized test API, dropped unused `PCG32_INC`); vectors independently confirmed canonical — not a copy.
- `odin test core` green · `odin run harness -- run` green · `tools/lint.sh` green.

### Blockers (0)
None.

### Warnings (1)

**W1 — No automated negative test for the replay-gate drift rejection (the #599-r2 "mask" risk).** *[tests]* — `.github/workflows/ci.yml:76` runs only the harness happy path (`odin run harness -- run`), and no `core/*_test.odin` exercises catalog/`logic_hz` drift rejection. The gate **works today** (proven above), but a future regression weakening the `header.catalog_hash != current` / `logic_hz != current` checks in `harness/run.odin::replay_hashes` would still pass CI — silently turning the gate into a mask on the spine's most load-bearing invariant.
*Fix:* add a CI-exercised negative test — e.g. `harness replay <demo> <drifted-log>` (or a core unit test) asserting non-zero exit / "defined rejection" on catalog and `logic_hz` drift.

### Notes (3)

**N1 — Dead/unused serialization helpers.** *[blind, codebase]* — reviewer agreement. `core/serialize.odin` defines `w_u16` (l.27), `w_bool` (l.41), `state_dump` (l.58), `r_u16` (l.148); none are called anywhere in `core/` or `harness/`. Forward-looking/debug helpers per their comments, but currently dead in the foundational spine. *Fix:* annotate as deliberate forward-prep, or drop until needed.

**N2 — Replay tick-loop duplicated (test vs harness).** *[blind, architecture]* — reviewer agreement. `core/determinism_test.odin::record_run` (l.42) and `harness/run.odin::run_demo` (l.79) each reimplement the §11.1 "apply tick-N entries before stepping N" loop + per-tick `state_hash` + event drain. If the convention evolves they can drift apart silently. *Fix:* extract a shared `core` proc both call.

**N3 — Advisory test gate: PASS (with one concern).** *[tests]* — P0 paths (replay-equality, RNG vectors, log round-trip + 5 corrupt-input rejections) are fully covered by `odin test core`. Gate is PASS; the sole concern is W1.

**Verdict:** READY TO MERGE — the foundational determinism spine is correct and empirically verified (ODN-1/9/10/11/17 + E10 all hold; from-scratch clean). The single warning is forward-looking test-debt (no CI negative test for the drift gate), not a defect in the submitted code.

---
Address the findings and push for re-review if you'd like them carried into round 2, or merge as-is — the notes are non-blocking. Round 2 will re-verify any changes and carry forward anything unresolved. — *Perkins · model `zai-coding-cn/glm-5.2` (kimi quota down — sanctioned review fallback)*
