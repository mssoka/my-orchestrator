## 🤖 Perkins automated review — round 3
**Job:** packet-plumber-v2-motion-readability · **Reviewed sha:** 44ebc25 · **Reviewers:** 7/7 completed
**Verification:** 27/27 findings confirmed against the code — 0 discarded as false-positive

### Fix audit (r1 → this head)
Both r1 blockers landed, verified by **execution** at the reviewed sha:
- **B1 FIXED** — `motion_test.odin`: 13 `@(test)`s pin the interp core (4 continuous kinds, spawn/sever/reroute snaps, row-roll alpha endpoints, tick-gap/anchor no-ghost, prune/reset, reduced-motion predicate). `odin test app/render` = **28/28 green** (Perkins-run).
- **B2's P0 lifted** — the interp core is pinned, so P0 = 100%. The recomputed gate still FAILs, now on the P1 activation-wiring gap (B1 below).
- All 12 r1 warnings/notes re-audited in code: 11 FIXED (W3/W4/W5/W12 guards, N9/N10/N16 notes verified at their sites), 1 still present (F13 AC wording → N5), 1 escalated (F15 driver copy → W4, now with proof the strip path has no hash safety net).
- **Rebase deltas verified:** `git diff origin/v2..HEAD -- core/` is **empty** (view-layer only on the true head); 46/47 sim-truth artifacts byte-identical vs merged v2 — only `motion.t1`/`motion.log.bin` differ, and the base's own catalog_hash change re-hashes all 60 lines consistently (re-bless legitimate); golden harness **47/47 green**; **Rule-4 reproduces exactly: 30.6px → 11.2px** (fresh strips, Perkins-run); `draw_packet_shape` extraction held goldens byte-identical.

### Blockers (2)
- **B1 · The interpolation ACTIVATION is unpinned — the feature can silently die with every gate green** (`app/render/view.odin:1535` + `app/main.odin:461-465`) — the 13 pins call `packet_interp_pos` directly and all goldens render alpha=1.0, but `interp_alpha` is a **default param**: dropping the arg at the call site compiles green, kills the glide, and passes every gate. The PR's entire purpose is unpinned liveness. *Fix: extract main.odin's accum→alpha into a testable helper + unit pin, and add an rlsw render test asserting the drawn pixel at alpha=0.5.*
- **B2 · Advisory test gate: FAIL** — P0 100%, but P1 67% (activation wiring + app alpha untested) and overall 57% (trail ring / echo draw / tooling at 0%). Deliver B1 + W2, wire W1 → PASS.

### Warnings (4)
- **W1 · The motion pins run only in the LOCAL CI mirror** — `.github/workflows/ci.yml` never runs `odin test app/render` (its only unit step is `odin test core`); the 13 pins execute via `tools/ci-local.sh` gate 2 only, and the mirror's step-for-step parity claim is already divergent. Not dead files (verified running locally) — but remote green doesn't enforce them.
- **W2 · Trail ring mechanics zero coverage** (`view.odin:315-347`) — ring order, drop-oldest shift, 0.5px move gate, `fades[trail_n-1-k]` indexing never run under any gate; r1 B2's fix prescription explicitly listed "trail order" and it wasn't delivered.
- **W3 · The 'delivery snap' pin doesn't test delivery** — `interp_continuous` never reads `p.delivered`; the test passes via the anchor mismatch. Production is safe (`draw_packets:1386` skips delivered before interp), but the header claim "every teleport (…delivery) is FALSE" isn't what's pinned. Rename it or make the predicate read the flag.
- **W4 · Still present since r1, sharpened: motion-strip's third driver copy has NO drift safety net** (`motion_strip.odin:59-133`) — zero `state_hash` references on the strip path; the "T1 manifest pins it" comment is aspirational here. Cheapest net: hash-compare against the blessed `.t1` while rendering.

### Notes (14)
N1 dead `pos` + "hmm" scratch in motion_test.odin:241-242 [blind·architecture·codebase] · N2 echo RGB×fade vs "body color at low alpha" comment (`view.odin:1584`; aesthetic verdict deferred to k3) [blind·codebase] · N3 mangled indentation in the W5 export guard (`motion_strip.odin:165-171`) [blind·codebase] · N4 motion.dem "2200..2450 strip window" vs 2200..2600 commands · N5 *(still present since r1)* AC "100 ms" letter vs documented 60 Hz substitution · N6 `--xmax` valueless crash, reproduced [blind·edge·security] · N7 ms-arg i64 overflow unbounded · N8 `scale<=0` frame pollutes the glide base (self-healing) · N9 "PRE-2.1 render" claim includes +15% radius · N10 alpha derivation duplicated app/strip, no equivalence pin (pairs with B1's fix) · N11 hardcoded BODY color + exit-0-on-total-loss in the measure tool · N12 README holds table predates lost≠hold hardening — **arithmetic proof: 21=9+12, 10=1+9**; mean-jump headline reproduces exactly · N13 README says 46 demos, tree runs 47 · N14 evidence tooling untested (P3).

### Reviewer agreement
`--xmax` crash (blind·edge·security) · dead scratch lines (blind·architecture·codebase) · echo RGB×fade (blind·codebase) · W4 driver-copy/no-safety-net (architecture·codebase) · mangled indent (blind·codebase)

**Verdict:** NEEDS CHANGES

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
