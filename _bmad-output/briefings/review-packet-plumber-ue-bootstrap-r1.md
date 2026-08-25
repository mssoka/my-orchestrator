## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-ue-bootstrap · **PR:** #1 (new repo, `bootstrap` → `main`)
**Reviewed sha:** `836f44e38989f83c50b936e02a01d1c584efcbfe7`
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — no failed lenses
**Verification:** 55/55 reviewer findings survived independent re-verification against the worktree — 0 discarded as false-positive, 0 speculative. Mechanical checks run first-hand: standalone spine-check built + executed **green**, its `--json` output **byte-identical** to `docs/goldens/probe-seed42-ticks100.json`; `clang-format --dry-run --Werror` over `Source/` → **8/16 files fail**; `format-check.sh` exits 1 when actually run; the AGENTS.md rebuild one-liner reproduces a linker failure on a fresh clone; greps confirm no writer of `docs/goldens/.engine-probe.json` and `UE_ROOT` honored by only one of three scripts.

*(Process note: the host rebooted mid-round; this review resumed with 5 lens outputs already durable on disk and regenerated only the tests + security lenses against the identical canonical diff bytes.)*

**Scope framing:** per the review contract, engine-gated gates not being runnable at this sha (UE 5.8 download pending user login) is documented staging, **not** a defect and not counted below. Every blocker below is a statically verifiable source/config defect that survives engine install.

# MAJOR REWORK

**Verdict: NEEDS CHANGES — 6 blockers, 11 warnings, 15 notes.** To be clear about what's *right*: the standalone determinism spine itself is sound — the Odin pinned vectors reproduce, replay-equality holds, and the committed golden matches the runner byte-for-byte (I reproduced it). The blockers cluster on the **engine-side spine surface being non-functional as shipped** (three compile-breakers + one reversed assertion in the exact code the engine gates will run) and **two gate-integrity defects** that make currently-published acceptance claims false.

### BLOCKERS (6)

**B1. The golden gate's engine leg is structurally dead — nothing ever writes `docs/goldens/.engine-probe.json`** — `scripts/compare-golden.sh:26` [acceptance, architecture, blind, codebase, edge, tests — **6-lens agreement**]
The engine-vs-standalone branch is unreachable forever (repo-wide grep: no producer), and `--bless` (the golden's documented engine-side producer) requires the engine and has never executed. The ODN-11 cross-runner contract is enforced on two of three legs; the engine PPProbe can never land in the comparison. *Fix: have `run-tests-headless.sh --probe` (gate 6) write `.engine-probe.json` via `--json-out` so gate 7's engine branch becomes reachable.*

**B2. Format gate is false-green: `ENGINE:`-labeled so it skips at this sha, while `format-check.sh` is engine-free and **8/16 Source files fail clang-format when actually run** — `scripts/local-ci.sh:70` [acceptance, architecture, blind, codebase, tests — 5-lens agreement]
README/AGENTS/PR all claim the pre-engine "format, spine, static" loop is green; it isn't — gate 1 silently skips, and the script I ran directly exits 1 (spine headers' one-line braced returns vs the committed Allman `.clang-format`). This is exactly the false-green class AGENTS.md's own pitfalls forbid, and it violates the review contract's "engine-free gates must be green at this sha". *Fix: drop the `ENGINE:` prefix (the script self-skips gracefully with no clang-format) + `clang-format -i` the 8 files.*

**B3. `PPProbeCommandlet` cannot compile: 2-arg `ParseCommandLine` — UE has only the 3-arg (Tokens, Switches) overload; even arity-fixed, `-seed/-ticks/-json` route to Switches, never Tokens** — `PPProbeCommandlet.cpp:25-26` [codebase, edge]
The headless probe entry — a named requirement of the spine port — is non-runnable as shipped and defaults-parsing even if it compiled. *Fix: 3-arg overload + iterate Switches (dash-stripped) for `seed=`/`ticks=`/`json=`.*

**B4. `LogPPCore` used without including its declaring header** — `PPProbeCommandlet.cpp` uses `UE_LOG(LogPPCore, …)` ×3 but never includes `PacketPlumberCore.h` (the `DECLARE_LOG_CATEGORY_EXTERN` site) — second independent compile-breaker in the commandlet. [codebase]

**B5. Module-prefixed spine includes can't resolve: flat layout + no `Public/` + no explicit include paths + `BuildSettingsVersion.V5`** — every test/editor TU does `#include "PacketPlumberCore/PP_*.h"` while the headers sit at the module root; V5 default rules put the module dir (not `Source/`) on dependents' paths, so `PacketPlumberCoreTests` and `PacketPlumberEditor` cannot build when the engine lands. [codebase] *Fix: move spine headers to `Source/PacketPlumberCore/Public/PacketPlumberCore/` (standard layout) or add explicit include paths.*

**B6. Magic-byte assertion is reversed: test asserts `'P','P','U','E'`, the LE serializer emits `'E','U','P','P'` for `SAVE_MAGIC 0x50505545`** — `PP_DeterminismTests.cpp:73-76` vs `PP_SimState.h:18` [blind]
The UE determinism suite is guaranteed to fail at engine time — a false FAIL on the spine contract. *Fix: pick one truth (assert `E,U,P,P` as-written, or change the constant) and document the wire format.*

### WARNINGS (11)

- **W1** `UE_ROOT` honored only by `local-ci.sh`; `run-tests-headless.sh` + `install-engine.sh` duplicate `find_engine` without it → engine gates false-fail for non-default installs [blind, architecture, edge]. *Fix: one shared `find_engine` lib.*
- **W2** `compare-golden.sh` never compares `rng_first4` — carried by the golden and both runners, enforced nowhere (not covered by `state_hash`: drawn before the re-seed) [blind].
- **W3** **"34 checks" is false everywhere** — 15 CHECK statements / 25 executions; hardcoded in the runner's output and repeated in README, project-context, research-report.md/.html, and this PR's body [acceptance, blind, codebase, tests].
- **W4** The committed golden is asserted by **no engine-free gate** (compare-golden is gate 7 `ENGINE:`; spine-check prints but doesn't assert) — a serialization-layout regression passes `--fast` [tests]. *Fix: inline CHECKs pinning `tick_nonce=2381141952` / `state_hash=e8046b49de0f2447`.*
- **W5** `PP::Step` guard branches (backward-tick ignore, `bTerminal` freeze) have zero tests in either runner [tests].
- **W6** `--probe` echoes "probe JSON written" without asserting the artifact exists; `RESULT=OK` is logged before the JSON write, so a failed write can still pass the log-grep [edge].
- **W7** `bin/vision-read` is the documented screenshot-verification entry point (AGENTS.md + 6 docs) but exists nowhere — not in the repo, not on PATH, not in the main checkout (verified) [acceptance, blind].
- **W8** AGENTS.md claims `ue-mcp.yml` flows are committed project config; the file is absent from the repo [blind].
- **W9** FNV-1a conformance partially tautological: `Fnv1a64(x) == Fnv1a64(x)` pins nothing; only the empty-input offset-basis vector is real. Pin published vectors (`"a"` → `0xaf63dc4c8601ec8c`) [blind, wording softened on verify — the empty-basis check is a real pin].
- **W10** `.mcp.json` runs unpinned `npx -y ue-mcp` with agent/editor-write privileges — supply chain + non-reproducible tooling [security]. *Fix: pin the version.*
- **W11** **Advisory test gate: CONCERNS** — P0 100% (RNG vectors dual-runner + Odin-exact, replay equality, non-vacuity; golden byte-match reproduced), P1 ~85% (the gaps are exactly B1/B2/W4/W5), overall ~85% [tests]. Fixing those lifts the gate to PASS.

### NOTES (15)

N1 dead includes in PPProbeCommandlet.cpp (PlatformFileManager.h, OutputDeviceNull.h) · N2 unused `os` import in static-check.py · N3 static-check.py ignores `git ls-files` failure (CRLF scan silently scans zero files outside a repo) · N4 local-ci.sh header gate table (8 gates, "gate 4 engine presence") ≠ the 7-entry GATES array · N5 UE-side `SerializeVersioned` test has no standalone byte-level counterpart ("Mirrors spine_check" is one-way) · N6 `SerializeState` capacity-guard branch untested · N7 ODN-2 fixed-20Hz ini pin has no engine-free assertion · N8 `RngRange` computes `Hi - Lo` in `int32_t` before the cast (UB for spans > `INT32_MAX`) · N9 backward-tick swallow is unobservable ("logs via the caller" — no caller logs) · N10 PPProbe accepts negative/zero `-ticks` + garbage `-seed` silently, reports initial hash as OK · N11 PacketPlumberCore declares unused CoreUObject/Engine deps · N12 PacketPlumberEditor declares unused dep on game module PacketPlumber · N13 AGENTS.md spine-check rebuild one-liner fails on fresh clone (no `mkdir -p tests/build`; reproduced) · N14 playbook security rules omit the same-host browser→localhost origin threat to the unauthenticated bridge · N15 research-report.html loads CDN scripts without SRI.

### Reviewer Agreement

Highest-confidence multi-lens findings: **B1** (6 lenses), **B2** (5 lenses), **W3** (4 lenses), **W1** (3 lenses), **B3** (2 lenses), **W7** (2 lenses).

### Verdict

**NEEDS CHANGES (MAJOR REWORK band: 4+ blockers).** The spine's standalone core is verified sound; what ships for the engine side is not: the commandlet and test modules cannot compile (B3/B4/B5), one committed spine assertion is reversed (B6), the golden's engine leg can never execute (B1), and a headline gate claim is false at this sha (B2). All six are precisely localized with one-truth fixes — none re-litigates the user's rulings, the GDD, or the engine choice.

_Address findings and push — I re-review automatically on the new sha._

