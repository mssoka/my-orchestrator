## 🤖 Perkins automated review — round 2 of 3
**Job:** packet-plumber-ue-bootstrap · **Reviewed sha:** `11bf6ad` · **Reviewers:** 7/7 completed
**Verification:** 32/33 findings confirmed against the code — 1 discarded as false-positive (26 distinct findings after dedupe). Diff: 3187 lines, single wave (~6% over the soft ~3000 threshold — kept whole because the delta's findings live at docs↔code↔gate seams that file-group chunking would sever).

**Engine gates verified first-hand this round** (UE 5.8.1 installed): I ran the full `scripts/local-ci.sh` suite in a **fresh detached worktree at exactly this sha** — **7/7 PASS**, including the first engine-golden 3-way match (engine PPProbe == standalone spine-check == committed golden, `state_hash=fbe6fae2655cadf7`), 8/8 automation tests `Result={Success}`, module-static `LogPPProbe` emitting in the engine log. (One dispatch note: the initial 7-lens wave hit account-wide 429 rate limits; 4 lenses were re-dispatched staggered per the one-retry policy — all completed.)

### Fix audit (r1 → r2): **32/32 FIXED** ✅
Every r1 finding re-verified against the code at this sha, not trusted from the PR description:
- **B1–B6 all fixed.** B6 audited hardest per the round guard: the golden re-bless changes **only** `state_hash`; `SAVE_MAGIC` feeds exactly one `PutU32` in serialization (never sim math), `StateHash` is FNV-1a-64 over the serialized buffer, and `tick_nonce`/`rng_first4` are byte-identical to r1's golden — the re-bless is the legitimate 4-byte cascade, **not a masked regression**.
- **W1–W11 all fixed** (shared `engine.sh` discovery, `rng_first4` compared, check-count derived at runtime, golden asserted engine-free by inline CHECKs in both runners, Step guards tested both runners, probe artifact asserted, `bin/vision-read` committed, `ue-mcp.yml` dropped, published FNV vectors pinned, `ue-mcp@1.2.4` pinned, advisory gate recomputed).
- **N1–N15 all fixed** (N9 resolved by canon-accurate documentation — Odin `step.odin:39` guards only `tick < state.tick`).

### Blockers (0)

None. The hard bar held: all 7 gates genuinely pass at this sha.

### Warnings (6)
1. **`PP_Rng.h:84` — RngRange final addition can UB for spans ≥ 2³¹** *(blind+edge+architecture agree)*. r1-N8 fixed the `Hi-Lo` subtraction, but for `Lo=INT32_MIN, Hi=INT32_MAX` the offset equals `RngNext` ∈ [0,2³²−1]; the `int32_t` cast wraps negative and `Lo + negative` underflows. Latent (no spine caller; tests span [6,34]) but violates the ODN-10 well-definedness the header comment claims. Fix: compute the result in `int64_t`.
2. **Engine gate runs dirty the tree** *(codebase; reproduced first-hand in my own run)*: tracked `Config/DefaultEngine.ini` gains a machine-generated AndroidFileServer section (incl. `SecurityToken`) and untracked-not-ignored `Config/DefaultInput.ini` appears on every editor boot. Commit/strip/ignore as appropriate.
3. **Briefing AC unmet: MCP editor-driving proof.** The AC says "screenshot or asset query **proven in the PR body**"; the body shows verified-boot only and still lists the screenshot proof as staged-pending — while the engine is now installed and everything else staged (build, headless tests, timings) got proven. Drive one asset query/screenshot via ue-mcp and record it before slice-1.
4. **Format gate soft-skip false-greens** (`format-check.sh:21-24`): no clang-format ≥ 14 → prints SKIP but exits 0 → local-ci summary shows gate 1 as ✅ PASS. Narrower than r1-B2 (hosts here have clang-format) but the same false-green class on bare hosts. Distinguish SKIP from PASS in the summary.
5. **PPProbe commandlet error paths have zero automated coverage**: the new fail-loud branches (bad `-seed`, bad `-ticks`, JSON write failure) are exactly this round's fix surface, yet only the happy path runs (gate 6). Add a negative-args gate or test.
6. **Advisory test gate: CONCERNS** (P0 100%, P1 ~85% — the gaps above). Closing #5 plus a compare-golden negative test lifts it to PASS.

### Notes (20)
Terminology/comments: "Developer type" comments vs `UncookedOnly` uproject declaration *(3 sources)* · engine.sh usage comment sources a nonexistent path · stale "until UE lands"/"pending install" text in README Quickstart + project-context ODN-2 row · playbook `npx` commands unpinned vs `.mcp.json@1.2.4`.
Coverage/robustness: Step equal-tick re-entry unpinned (behavior is canon-consistent — Odin guards only `tick <`) · full-int32-span RngRange test standalone-only · compare-golden mismatch branches untested · `bash -n` gate misses `scripts/lib/` + `bin/` · StateHash 64-byte buffer will confuse-fail (loudly, via non-vacuity CHECKs) when slice-1 outgrows it · `-ticks ≥ 2³²` relies on Atoi wrap/clamp · `--json-out` with no value runs artifact-less and green.
Hygiene: `Saved/` twice in .gitignore · unused `using System.Collections.Generic` (×2 Target.cs) · unused `UnrealEd` dep · format-check's engine-bundled clang-format path is Windows-layout, dead on macOS 5.8.1 · golden JSON schema triplicated (spine printf / commandlet Printf / compare-golden KEYS) · no cold first-build timing ever recorded (timings.md starts warm) · ue-mcp pin without integrity lock · loopback MCP endpoint discipline-mitigated only.

### Reviewer agreement
`RngRange UB` (3 sources) · `Developer/UncookedOnly comments` (3 sources) · `Step equal-tick` (2 sources)

**Verdict: READY TO MERGE**

Fix audit 32/32, all 7 gates green first-hand at this sha, golden re-bless proven surgical, zero blockers. The 6 warnings are non-blocking (latent UB with no current caller, hygiene, one now-unblocked AC proof, coverage gaps) — address them on the follow-up; W-3 (MCP proof) should land before slice-1 begins.

*(CI on this PR shows no checks — GitHub Actions billing block, standing ruling; local verification is the ground truth and was performed first-hand. Pixel checks: none needed this round — the golden compare is byte/hash-based.)*

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
