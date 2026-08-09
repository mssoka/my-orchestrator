You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools (read files under the worktree path below). The diff file is the canonical reviewed bytes.

--- SPEC / CONTEXT ---
You have read-only access to the repository at /Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r1 and MUST verify the diff's claims against the actual codebase (read files there). The diff file is the canonical reviewed bytes; the worktree is pinned at the reviewed commit.

Specs (read them):
- Round briefing (Perkins mandate + LENS-GUARD — read first): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/spec/round-briefing.md
- Job briefing (acceptance): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/spec/job-briefing.md
- THE CANON SPEC — Odin architecture (ODN-1..18, §10 harness, E1..E32 contracts): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/spec/odin-architecture-v1.md
- GDD (engine-agnostic design: M1..M5, QoS lanes, crisis model): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/spec/gdd.md

LENS-GUARD (from the round briefing — prevents false positives; read the full version in the round briefing):
This is an EARLY PROTOTYPE for an engine A/B, not production code. Perkins mandate: "the determinism spine is the ONE hard blocker; otherwise prototype-rigor for the comparison gate, not production-grade."
- Do NOT flag "not production-grade" / "missing full-game features" as blockers (era tree, leaderboard, mobile, save system are deliberately NOT built).
- Do NOT flag Odin/Raylib as "wrong engine" or suggest Godot/GDScript/C# (the pivot is the user's ruling).
- Do NOT flag prototype debt (hardcoded values, stubbed systems, minimal validation) as BLOCKERS — warnings/notes only.
- Do NOT re-litigate the Godot #11 findings (prior round: 46 findings on the merged Godot prototype). Those informed this re-implementation; verify the lessons were APPLIED (e.g. serialization is field-wise canonical, never raw in-memory bytes).
- CI: the `.odin-version` pins `dev-2026-08-nightly` (not a valid upstream branch) so the CI verify job fails to clone Odin — KNOWN issue, do NOT re-flag (note it's known).
Legitimate blocker-class findings: determinism spine compromised (seeded run does not reproduce; sim tangled with raylib; vendor/OS imports in core/; float nondeterminism in sim; unowned PRNG; iteration-order dependence); golden harness fake (tautological compares, raw-bytes T1 hash, false replay claims); core-loop BUG (packets don't flow, QoS priority broken, surge unsurvivable, port limits not enforced, NetworkHealth/Error 404 broken); committed app.bin binary; compile/runtime crash.

Prior-round context (Godot #11, 46 findings — the lessons to verify APPLIED, not re-litigate):
- NetworkHealth win/lose/drain had ZERO test coverage; QoS priority behavior untested
- Upgrade validation charged full tier cost but applied only the delta; span check skipped on upgrade
- Junction demolish left ghost pipes; batch budget could go negative; null-deref in batches
- logic_hz=10 vs ADR-2's 20Hz contradictions; balance never passed to PacketFlow (ms_per_tick stuck at 50)
- Determinism fingerprint OMITTED in-flight packet state + latency (replay-equality could pass while internals diverged) — THE raw-bytes/canonical-form lesson
- Replay-equality keystone ran on a no-pipes topology; submit_command fast-path had an undocumented +1 convention
- Terminal-to-terminal pipes were legal (bypassing routers) — the art-canon rule E26
- QoS emphasis preset was a hardcoded literal, not catalog data; clean_span default read before max_span loaded
- MCPRuntime autoload exposed an unauthenticated TCP control server (security)
- span_between used float sqrt for a state-affecting value

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
Your diff file (read it fully): /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/chunk-2-core-tests.patch

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Worktree: /Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r1

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
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
- Write ONLY the JSON array to: /Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/codebase-b.json. No prose, no markdown fencing, no preamble in the file.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, finish with one line in the pane: "codebase done: N findings".

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
