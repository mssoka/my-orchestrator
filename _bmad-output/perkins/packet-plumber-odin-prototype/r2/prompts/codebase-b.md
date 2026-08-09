You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools (read files under the worktree path below). The diff file is the canonical reviewed bytes.

--- SPEC / CONTEXT ---
You have read-only access to the repository at /Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r2 and MUST verify the diff's claims against the actual codebase (read files there). The diff file is the canonical reviewed bytes; the worktree is pinned at the reviewed commit (ea678a8).

Specs (read them):
- Round briefing (Perkins mandate + LENS-GUARD — read first): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/spec/round-briefing.md
- Job briefing (acceptance): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/spec/job-briefing.md
- THE CANON SPEC — Odin architecture (ODN-1..18, §10 harness, E1..E32 contracts): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/spec/odin-architecture-v1.md
- GDD (engine-agnostic design: M1..M5, QoS lanes, crisis model): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/spec/gdd.md

THIS IS ROUND 2 (fix-audit). Round 1 reviewed sha 0118cc0 and posted CHANGES_REQUESTED; Perkins has already personally audited every r1 finding against the worktree. The r1 blockers (committed app.bin; UI-dead demolish) are CONFIRMED FIXED — do not re-report them. These r1 findings are CONFIRMED STILL PRESENT — do NOT re-report them either (they are carried forward by Perkins; your budget is for NEW issues):
- E7 WRR-floor test still vacuous (weights {100,1,1} > MAX_WEIGHT=64 silently rejected; submit_c discards the error)
- severance-reroute test still can't distinguish reroute-survival from fresh spawns (`_ = sev_drops_before`)
- harness `save` still blesses failed demos (`return ok || save`)
- harness demo_parse 'demolish node' with no name still indexes fields[2] OOB
- crises.json parsed but never consumed; jint i64->i32 truncation + unknown keys accepted
- zero-traffic neutral ticks still drain at max severity mid-breach (health.odin:73)
- pick_dst still allocates two dynamic arrays per spawned packet on the run arena
- grace countdown in the HUD still computes ticks*hz, discards it, draws a static "!"
- grace-reset test still can't distinguish gradual refill from instant re-arm
- draw_and_reject.dem header still overclaims (and now references the REMOVED budget system)
- nearest_pipe bezier hit-testing still untested; committed r1 review docs still stale
- note-level: dead symbols (state_dump, PCG32_INC, TICK_SECONDS), write_file/write_log dup, raylib tag pin, replay bare=false, rng-test name, tier_by_name dropped ok, app.mode dead, catalog jarr leaks

LENS-GUARD (from the round briefing — prevents false positives; read the full version in the round briefing):
- The determinism spine is the ONE hard blocker: a seeded run MUST reproduce byte-identical T1 state-hash + T2 pixel goldens cross-platform. Perkins has empirically verified it at ea678a8 on macOS (7/7 demos green, replay 3000/3000 bit-for-bit) and CI is green on ubuntu — flag it ONLY if you find a concrete NEW compromise in the diff (e.g. a new float-contraction path the -ffp-contract=off fix misses, an unhashed state field, map iteration, unowned RNG).
- Do NOT re-litigate USER RULINGS: the Mini-Motorways hardware inventory replacing the budget (0b92fa4), desktop-first launch, mouse-only prototype, root layout, the Odin/Raylib pivot, the Godot game/ removal. Review their CORRECTNESS, never their existence.
- Do NOT re-litigate the Godot #11 findings; verify lessons APPLIED.
- Prototype-rigor, not production-grade: missing full-game features (era tree, leaderboards, mobile, save system) are NOT defects. Prototype debt is warning/note, never blocker.
- NEW since r1 — hunt here especially: the hardware-inventory system (Inventory slices on Run_State; validate/apply move stock; Cmd_Place_Router; tick-scheduled grants; Ev_Stock_Arrived; action-log tag 7; tray HUD; autopilot port-reserve/midpoint relay chains), the crash fixes (hint buffer, allocator ownership, MSAA drop + --soak), the -ffp-contract=off T2 fix, the new tests (node-health, queue-overflow), the CI rework (Odin release-tarball install, gdb fallback, per-arch vendor dirs).
Legitimate blocker-class findings: determinism spine compromised (seeded run does not reproduce; sim tangled with raylib; vendor/OS imports in core/; float nondeterminism in sim; unowned PRNG; iteration-order dependence); golden harness fake (tautological compares, raw-bytes T1 hash, false replay claims); core-loop BUG (packets don't flow, QoS broken, surge unsurvivable, inventory stock goes negative / placement bypasses stock, NetworkHealth/Error404 broken); committed binary; compile/runtime crash.

PROJECT CONVENTIONS (from project-context.md, redone for Odin in this branch):
- core/ imports ONLY whitelisted core:* packages — never vendor:*, never core:os, never core:time (ODN-1; CI compile-checked)
- Integer-only sim paths (ODN-10); floats only in the view, never flow back into state
- Never iterate a map in core (map order unspecified) — arrays/slices/#soa only; maps are lookup-only
- RNG is owned (splitmix64→PCG32 XSH-RR, pinned vectors) — never core:math/rand for sim
- Arena discipline (ODN-18): no new/make without an explicit allocator in core
- No globals/singletons (ODN-13); events not callbacks (ODN-14); errors are values (typed enums, no dropped returns)
- Save/log is binary little-endian versioned (ODN-11); JSON only for catalogs, loaded once, fail-fast validated
- Balance numbers live in data/*.json, never literals
- Odin stdlib naming: types/consts Ada_Case, procs/vars snake_case
- Harness (ODN-17): T1 = per-tick FNV-1a-64 of canonical serialized state (field-wise LE, lengths-not-capacities, no padding, includes rng state + event stream); T2 = pixel goldens via rlsw software renderer + PLATFORM_MEMORY, zero-tolerance compare


--- DIFF ---
Your diff file (read it fully): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/chunk-2-core-tests.patch

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Round-2: the budget->inventory rename — are there leftover budget references (symbols, comments, docs, HUD strings, demo headers) now orphaned by the ruling? Does the game/ removal orphan anything on main (docs referencing game/, the prototype-fun-gate tag story)? Does the CI reference paths that exist?

Worktree: /Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r2

--- OUTPUT ---
Write ONE valid JSON array to /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/codebase-b.json. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The file /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/codebase-b.json must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, finish with one line in the pane: "codebase b done: N findings".

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
