You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1/project-context.md if you need project conventions. The repo is Packet-Plumber (Odin), a sim-core + raylib-view architecture: core/ is pure sim (no I/O, integer math, deterministic per-tick hashes), app/ is the raylib presentation layer, harness/ drives demos + goldens. Golden discipline is strict: goldens are blessed artifacts; shifts must trace to documented causes. Never modify any file in the worktree — read-only.

--- DIFF ---
The canonical diff under review is at: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/diff.patch
Read it. It is the complete diff for PR #44 (reviewed sha 23e1704eae1abed8cdcdb635d85dd4ec30d8aca2, base v2), saved by Perkins as the canonical bytes. You review exactly these bytes.

--- SPEC / CONTEXT ---
Spec file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/spec-context.md — read it (job briefing + story 5.5 card + arch pins [E1]/[E2]/[E10]/[E27]/[E29] + lens-guards LOCKED list + implementer claims). Section 4 lens-guards lists LOCKED items — do not file findings on locked items. Section 5's implementer claims are claims to verify, not truth.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New input paths (click_select, popover_click, release_ui_hit, X/DEL keys) without matching coverage
- Error paths missing negative tests (reject toast paths for Missing_Pipe/Missing_Node/Terminal_Demolish)
- New state transitions without boundary tests (sel_node/sel_pipe exclusivity, press_swallowed lifecycle, selection after junction batch)
- The two new demos + replay gate coverage of the demolish command path
- Existing goldens claimed byte-identical — is there a gate that verifies it (harness run)?
Test level mix: this is an app-layer input diff — the core mechanic tests live in core/demolish_test.odin (existing, settled). The demos + harness replay gate are the E2E layer. Flag gaps between those layers.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array to this exact file path (use your file-writing tool): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/tests.json
- Then reply with exactly one word: done
- Do not print the JSON in chat. Do not create or modify any other files. Do not fix anything.
- Empty array [] is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

The repository worktree (read-only for you) is at: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1
