#!/usr/bin/env python3
"""Generate the 21 lens briefs (7 lenses x 3 chunks) for Perkins r2."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-spawn-director/r2"
WORKTREE = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-dublin-spawn-director-r2"

CHUNKS = {
    "code": {
        "file": f"{OUT}/chunk-code.patch",
        "desc": ("1,461 lines, 9 files: core/growth.odin (the director: SEED/ATTACH weighting, "
                 "district caps, the r1-fold W1 drawn-tile cap check), core/map.odin (loader + "
                 "map_board_partition — the shared partition builder), core/map_test.odin (the "
                 "pins, incl. the r1-fold B1 bias pin + W1 cross-boundary cap pin + fractional/"
                 "floor-667/zero-tile pins), core/growth_test.odin, core/catalog.odin + "
                 "catalog_test.odin (growth_districts rows), core/determinism_test.odin, "
                 "harness/dublin_shot.odin (dublin-grown verb: ms bound, audit header, census "
                 "line), harness/main.odin (usage). Read the chunk IN FULL."),
    },
    "data": {
        "file": f"{OUT}/chunk-data.patch",
        "desc": ("541 lines, 10 files: data/balance.json (growth_districts tunables — district_cap_permille, "
                 "per-kind seed_weights), demos/dublin_board.dem, docs/captures/v2-dublin-spawn-director/ "
                 "(4 gate PNGs + spawn-audit.txt — the committed gate evidence: audit header, census line, "
                 "per-district live/pool table), .memlog.md (the fold entry + amended badge-out line), "
                 "_bmad-output/implementation-artifacts/spec-v2-dublin-spawn-director.md (the spec — W2 "
                 "vacuous-by-design acknowledgment, 603 census, pin 3 wording), _bmad-output/pr-bodies/"
                 "v2-dublin-spawn-director.md (the PR body — r1-fold section). Read the chunk IN FULL."),
    },
    "goldens": {
        "file": f"{OUT}/chunk-goldens.patch",
        "desc": ("83,126 lines, 102 files — RE-BLESS DATA, not hand-written code: 51 re-blessed .t1 golden "
                 "captures (full text diffs — every catalog_hash-anchored byte shifts), 49 .log.bin golden "
                 "logs (binary 'files differ' stubs — byte claims verified elsewhere; you verify the SHAPE), "
                 "2 re-blessed dublin_board PNGs (binary stubs). The r1-fold commit (04ef6a9) touched ZERO "
                 "golden bytes — this chunk is identical to r1's reviewed goldens; you audit the cumulative "
                 "determinism claims still standing at 04ef6a9. Method: read the first ~300 lines to learn "
                 "the .t1 shape, enumerate EVERY file boundary (grep '^diff --git' on the chunk file), then "
                 "sample hunk interiors across several .t1 files (e.g. a11y, growth, surge, dublin_board) "
                 "and diff-compare what changed vs what did not. You can read the .t1/.log.bin files at HEAD "
                 "in the worktree read-only and compare against the chunk's '---' side."),
    },
}

ROUND_CTX = """## ROUND CONTEXT — r2 is a FIX-AUDIT round

- This chunk is part of the CUMULATIVE PR #96 delta (origin/v2...04ef6a9), 85,128 lines, split into 3 chunks (code / data / goldens). You see exactly ONE chunk.
- Head 04ef6a9 = the r1-fold commit (B1 bias pin + W1 drawn-tile cap + W2 acknowledgment + N-folds) on top of 93333cd (the feature commit, r1-reviewed).
- DELTA-INTRODUCED issues (bugs the FOLD commit itself introduced) are the norm to hunt — but report any real issue you can ground, from either commit.
- r1's consolidated findings (for context): %s/prior_findings.json — 1 blocker (B1: ATTACH weighted cluster-pick had no bias pin), 5 warnings (W1 cross-boundary cap leak; W2 vacuous demolish clause; W3 routers-not-in-live-count unpinned; W4 loader pass-3 partition unasserted; coverage gate CONCERNS), 17 notes.
- Claimed fold dispositions: B1 -> test_growth_dublin_attach_cluster_pick_bias (distinct weights city 4 vs suburb 1, 10 windows x 6 seeds, 1.5x bar; uniform mutation fails A=27 B=27); W1 -> drawn-tile cap check in the attach branch + test_growth_dublin_attach_tile_district_cap (mutation fails); W2 -> acknowledged vacuous-by-design in spec + PR; N-folds -> 111/113 tally, 603 census, shared map_board_partition, dead predicate removed, fractional/floor-667/zero-tile pins, audit header + census line, dublin-grown ms bound + usage + comment.
- The fold claims: goldens byte-untouched (49/49 green — no district reaches cap in the demo), 261 core tests green, 13/13 CI.
""" % OUT

REPO = f"""## REPOSITORY (read-only verification ground)
Your cwd is a detached git worktree at EXACTLY the reviewed sha (04ef6a9) — trust it, not origin branches. Verify diff claims here read-only. You modify NOTHING except your OUTPUT FILE (which lives outside the worktree).
"""

CONV = """## PROJECT CONVENTIONS
Read project-context.md in your cwd first (the project's own conventions doc).
"""

SPEC = f"""## SPEC / CONTEXT (the job's acceptance reference)
1. {OUT}/job-briefing.md — the original job briefing (the spec — read IN FULL)
2. {OUT}/pr96-body.md — the PR body: the minion's claims + r1-fold section (its ACCOUNT of the work — verify, never trust)
3. {OUT}/pr95-body.md — the approved mock-gate canon (round history of PR #95 — the 7-round rulings the job implements)
4. In-worktree canon: data/maps/dublin.json (rulings block — density 1in6), docs/captures/dublin-map-mock/ (the approved mock captures), docs/captures/v2-dublin-spawn-director/ (the gate evidence + spawn audit)
"""

LENS_BRIEFS = {
    "edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.
Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.
For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
r2 hint (verify, don't trust): the W1 drawn-tile cap is a ZERO-DRAW REJECTION predicate (a `continue` inside the bounded attempt budget) — trace what happens when every ring tile is in capped districts (starvation? budget burn? window skip?); the B1 bias pin lifts max_members to 40 — any interplay with the 36-tile dense cells; the dead-predicate removal in the procedural branch claims byte-identical rng stream.""",
    "acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec
For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
r2 fix-audit targets (verify each against the CODE at HEAD, not the PR body's word): (1) B1 — spec §3 pin 3 'the rich district's estate extends more' now has a real pin at DISTINCT weights; (2) W1 — the hard bound covers the DRAWN TILE (enforcement in the attach branch, not just seed); (3) W2 — the demolish-frees-budget clause is acknowledged vacuous-by-design in the spec + PR (honest acknowledgment, not a silent drop, not a claim of verified behavior); (4) the 603-tile census + 111/113 tally corrections are now what the spec/PR/memlog say; (5) r1's W3 (routers excluded from district live counts) + W4 (loader pass-3 partition unasserted) — check whether the fold delivered or carried them, and whether any carried item is honestly dispositioned.""",
    "security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
This is an offline deterministic game engine (Odin) — map the OWASP lens onto its real boundaries: JSON/data file loading, harness CLI argument parsing, file writes (PNG/log outputs), and anything that could trap, overflow, or read out of bounds. r2 hint: the new 24h ms bound in run_dublin_grown (verify the product run_ms * logic_hz cannot wrap before the bound fires at ANY plausible logic_hz), the census/audit printfs (format strings), map_board_partition allocations.""",
    "architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
r2 hint (verify, don't trust): the fold EXTRACTED map_board_partition (one definition for loader + 4 test fixtures) — is the extraction clean (allocator threading, doc comments, call order contract)? The dead board predicate was deleted from the procedural re-walk — does the remaining comment honestly describe the branch? The census loop + terminal/router recount in the harness verb — placement/complexity fit vs the project's harness conventions? r1 carried notes: O(districts x nodes) live-count re-derivation per attempt (still unfixed?), the 5th hand-rolled Demo_Replay construction.""",
    "codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
r2 hint (verify, don't trust): every partition-build site must now call map_board_partition (loader map.odin + fixtures in map_test.odin AND growth_test.odin — enumerate ALL former copy-paste sites; r1 counted 5 sites); growth_board_cluster_has_room still used elsewhere (the deletion was the DEAD one)?; usage() line now lists dublin-grown; the dublin_shot_capture doc comment names both framings; the audit artifact spawn-audit.txt matches what the current dublin_shot.odin code would print (header + census line + per-district lines — including whether live counts exclude routers).""",
    "tests": """Test coverage analysis via traceability.
For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap
Blind-spot heuristics to check:
- New/modified core paths without matching coverage
- Determinism/replay invariants without boundary tests
- Happy-path-only coverage where error handling is implied
- New data tunables without validation tests
r2 pin audit (read each pin, judge whether it can pass vacuously — the memlog records the trap: 'a mutation leg can pass vacuously when a fixture's E31 occupancy blocks the target tile'): test_growth_dublin_attach_cluster_pick_bias (distinct weights? measurable bias? could it pass under a uniform regression? does the 1.5x bar + 6 seeds make it robust or fragile?), test_growth_dublin_attach_tile_district_cap (does the mutation leg actually land the tile in B — E31 occupancy of the OTHER ring tiles?), test_map_district_assign_fractional_anchors, test_growth_district_cap_formula (floor + 667 branches), test_map_district_zero_tile_clause, the r1 pins still present (partition/tie-break, weighted SEED majority, band exclusions x2, cap contract, attach band exclusion + positive control, board replay byte-identity). Also: r1's W3 (routers-excluded-from-live-count has NO pin) + W4 (loader pass-3 partition assert — did the shared-builder fold close it or narrow it?) — re-classify their coverage honestly.
Test level mix: flag mismatches as findings.
Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate
Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%""",
}

BLIND_BODY = """You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

ISOLATION CONTRACT (hard): You may read ONLY the diff chunk file below. Reading ANY other file, listing directories, or browsing the repository INVALIDATES your lens — do not do it. Your only tools for this task: read the diff chunk file (in slices if large).

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (the fold commit's message, quoted below)

CLAIMED PURPOSE of the newest commit visible in this diff (the r1 fold): 'B1: the ATTACH weighted cluster-pick now has a REAL bias pin — two eligible estates at distinct weights (city 4 vs suburb 1), 10 windows x 6 seeds, the honest bar 1.5x. W1: the hard bound now covers the DRAWN TILE — a cross-boundary attach cap-checks the member tile's OWN district. W2: the demolish-frees-budget clause acknowledged vacuous-by-design in the spec/PR comments. N-folds: 111/113 T2 tally; the loader census settles the pool dispute (603 tiles); the shared map_board_partition builder; the statically-dead board predicate removed from the procedural re-walk; fractional-anchor + cap floor/667 + zero-tile clause pins; the spawn-audit header + census line; dublin-grown ms bound + usage + comment fixes. Goldens untouched by the fold. 261 core tests green.'
Audit the diff against these claims: does the diff content actually deliver each one?
"""

SCHEMA = """## OUTPUT FILE (write ONLY your JSON array here — do not derive another path, do not write elsewhere)
%s

## OUTPUT SCHEMA
{
  "source": "%s",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, coverage-gap, boundary>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array (a bare JSON array, no markdown fencing, no prose) to the OUTPUT FILE path above, using a file-write tool. Do not print the array to your terminal as your final answer INSTEAD of writing it — the file IS the deliverable. Your final terminal message may be a one-line confirmation.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction in this brief:
NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume, do not generalise.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, drop the finding.
- Hedging ("might", "could", "possibly") signals you have not verified. Verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings. An empty array is an honest answer."""

GENERIC_HEAD = """You are a review lens in an automated review fleet (headless Perkins round). Execute exactly this brief, then stop. You post nothing to GitHub; you modify nothing; the ONLY file you write is your OUTPUT FILE.

## DIFF CHUNK (the exact canonical bytes under review — read the chunk IN FULL)
{chunk_file}
{chunk_desc}
"""

def brief(lens, chunk):
    parts = [f"# Lens brief — {lens.upper()} ({chunk} chunk) — Perkins r2, packet-plumber-v2-dublin-spawn-director\n"]
    if lens == "blind":
        parts.append(GENERIC_HEAD.format(chunk_file=CHUNKS[chunk]["file"], chunk_desc=CHUNKS[chunk]["desc"]))
        parts.append(BLIND_BODY)
    else:
        parts.append(GENERIC_HEAD.format(chunk_file=CHUNKS[chunk]["file"], chunk_desc=CHUNKS[chunk]["desc"]))
        parts.append(ROUND_CTX)
        parts.append(REPO)
        parts.append(CONV)
        parts.append(SPEC)
        parts.append("## YOUR LENS (review through this lens ONLY)\n" + LENS_BRIEFS[lens] + "\n")
    parts.append(SCHEMA % (f"{OUT}/{lens}-{chunk}.json", lens))
    return "\n".join(parts)

os.makedirs(OUT, exist_ok=True)
for lens in ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]:
    for chunk in ["code", "data", "goldens"]:
        path = f"{OUT}/brief-{lens}-{chunk}.md"
        with open(path, "w") as f:
            f.write(brief(lens, chunk))
print("wrote 21 briefs to", OUT)
