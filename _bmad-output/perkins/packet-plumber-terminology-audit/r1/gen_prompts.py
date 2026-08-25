#!/usr/bin/env python3
"""Generate Perkins lens prompts for packet-plumber-terminology-audit r1 (16 chunks x 7 lenses)."""
import json, os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-terminology-audit-r1"
SHA = "b9d5006"
MODEL = "deepseek/deepseek-v4-flash"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec — Phase 1 audit + Phase 2 rename discipline): {OUT}/spec/job-briefing.md
  - The terminology audit record (the lavish decision table the user ruled on): {WT}/_bmad-output/implementation-artifacts/terminology-audit-v1.md
  - The canon entry (2026-08-15 ruling, THE spec this PR must match): {WT}/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md (search "Terminology canon")"""

GUARDS = """- **🚨 THE ONE HARD BLOCKER — serialized contracts untouched.** LOG_VERSION stays 4 (only its comment may change); the wire format is byte-identical on all 29 `.log.bin` — Perkins has ALREADY VERIFIED: old-vs-new differ in EXACTLY the 8 catalog_hash bytes at offset 17 (old `bdc90b1363c93d8b` → new `8f94df8eb817dddb`), sizes identical, and the command tag constant keeps value 5 (only its NAME changed `CMD_TAG_SET_EMPHASIS`→`CMD_TAG_SET_WEIGHTS`). ANY non-catalog-hash wire delta (a tag value, a payload layout, LOG_VERSION, a serialized field) = a BLOCKER.
- **🚨 GOLDEN DISCIPLINE — Perkins has ALREADY verified the fold mechanically.** (a) `harness run` is green at the reviewed sha: all 29 demos reproduce the NEW goldens tick-for-tick (T1 manifest + replay bit-for-bit + T2 captures). (b) THE SPLICE PROOF IS REPRODUCED: in a scratch copy with ONLY `cat.hash` forced to the OLD value (sim code untouched), all 29 demos reproduce the OLD blessed goldens EXACTLY — every tick of ~22k ticks — and the OLD .log.bin files replay green. The fold is provably the only change. (c) Every changed line in goldens/*.t1 is either the `catalog_hash` header or a `<tick> <16-hex>` hash line; tick numbering is continuous 1..N with old count == new count on all 29; all 29 carry the same old→new hash pair. (d) ZERO PNGs in the diff — T2 untouched (the harness capture path never calls the app's `draw_hud`; the renamed HUD legend string renders no golden pixel). DO NOT file "every tick hash line changed" — that IS the verified fold. DO file: a non-hash line changed inside a golden (seed/ticks/demo/logic_hz), a numbering gap/dupe/reorder, a catalog_hash value other than the ruled pair, a .t1 without its .log.bin pair, an existing golden whose header did NOT change (stale bless), ANY .png anywhere in the diff.
- **🚨 DO NOT RE-LITIGATE THE 2026-08-15 VERDICT.** The rename IS the ruling, applied: drop ladder→drop precedence; strain→congestion/utilization; pressure→congestion; Cmd_Set_Emphasis→Cmd_Set_Weights; Pressure_Plan→Demand_Plan; lane→class queue is TWO-TIER BY DESIGN — docs/architecture/comments say "class queue", the player-facing surface + HUD + core identifiers KEEP "lane" (the 2026-08-12 spatial-lane visual + EF/AF/DF class names stand). GDD §M4 keeps "pressure" as the plumbing-metaphor gloss in prose where it names the metaphor itself. A doc saying "class queue" where code keeps `lane` is CORRECT, not a contradiction.
- **Historical specs keep authoring-time spellings.** spec-3-2 / spec-5-8 / spec-traffic-model etc. record what a story did WHEN it landed (e.g. spec-5-8's "`Cmd_Set_Emphasis` evolves its payload … LOG_VERSION 3→4" is history) — do NOT file old identifiers in historical narrative as misses. DO file old identifiers in LIVE surfaces the sweep should have caught (code comments, demo comments, catalog _comment strings, canon docs).
- **Scope guard:** vocabulary ONLY. Any mechanic/balance/rendering/behavior change hiding in the hunks = a blocker. No new player commands (the command SET is unchanged — only a rename). No HUD pixel changes beyond the ruled legend string (which renders no golden).
- **The balance.json `_comment` + key renames fold catalog_hash (ODN-11)** — this is the declared, proven reason for the T1 re-bless; do not file the fold itself. data/demand.json's `_comment` still says `scripted_plan_pressure` and demos/qos_manual.dem + qos_auto.dem comments still say `Cmd_Set_Emphasis` — Perkins already found these sweep residues; a lens may corroborate at NOTE level (do not escalate; demand.json folds catalog_hash so a later fix re-blesses).
- **Em-dashes are OK in PP** (the RT ban does not apply). Prose grammar warts created by the mechanical rename (e.g. "congested/congested", "never congestion" as a verb) are legitimate NOTE-level findings — name the file:line.
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical. A rename that touches ANY serialized byte (beyond the proven catalog_hash fold) breaks the spine."""

LEGIT_CODE = """- **A behavior change hiding in the rename**: any hunk that changes a VALUE (not just an identifier/comment/string) — a number, a threshold, a comparison, a control-flow shape, a serialization byte. Everything must be name-only.
- **A missed rename in a LIVE surface**: an old identifier (`Cmd_Set_Emphasis`, `Strain_Level`, `node_strain`, `pipe_strain`, `strain_level`, `state_strain`, `Pressure_Plan`, `plan_pressure`, `node_strained_lead_ticks`, `pipe_pressure_lead_ticks`, `Node_Strained`, `Pipe_Pressure`, `CMD_TAG_SET_EMPHASIS`) still referenced in a NON-historical code comment, demo comment, or catalog string. (Two demo comments + demand.json's _comment are already Perkins-found — corroborate, don't re-discover.)
- **A rename inconsistency**: an identifier renamed in one place but not at a use site (the build is green — so this would show as a deliberate-looking exception that ISN'T documented, e.g. `validate_set_emphasis`/`apply_set_emphasis` keeping the old word — the audit doc's scope column is the check), or a renamed test whose comment now misdescribes it.
- **A serialized-contract breach**: LOG_VERSION value touched, tag value 5 changed, payload layout touched, event bytes touched, the absent-when-empty logic touched. (The comments ON those lines may change; the bytes may not.)
- **The renamed HUD string**: must read exactly "node congestion ~%ds to critical / node critical ~%ds / pipe ~%ds to saturation" and stay ASCII (lint gate 6) — a typo or a non-ASCII char = a finding.
- **A test weakened**: an assertion dropped/loosened under cover of the rename (expected-event streams must be identical modulo the enum renames)."""

LEGIT_DOCS = """- **A canon-doc contradiction**: GDD/arch/stories/sprint/project-context text that contradicts the 2026-08-15 canon entry (decision-log.md) or the audit table's ruled column.
- **A missed rename in a CANON doc** (GDD, architecture, stories-v2, sprint-plan-v2, project-context) — old coinage where the verdict ruled a rename, EXCEPT the deliberate two-tier "lane" and the §M4 plumbing-metaphor gloss.
- **Scope drift**: a doc change that alters a RULE, number, AC, or mechanic rather than vocabulary.
- **The audit record itself**: a verdict-table row whose "ruled" action the PR did NOT apply (compare the table to the code diff coverage)."""

LEGIT_GOLDEN = """- **A re-bless beyond the fold**: a non-hash line changed (demo name, seed, logic_hz, ticks count), a hash-line numbering gap/dupe/reorder within the fragment, a tick line added/removed (count must equal the header's `ticks`), a catalog_hash value other than `bdc90b1363c93d8b`→`8f94df8eb817dddb`, a missing .log.bin for a demo with a .t1 (or vice versa).
- **Do NOT file**: per-tick hash lines changing (that IS the verified fold), the catalog_hash header changing, .log.bin binary diffs (Perkins verified exactly 8 header bytes per demo), the fragment split itself (the CHUNK NOTE is review tooling, not content)."""

CONTRACT = """Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "<your assigned source value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory.>",
  "detail": "<why this is a problem, <=40 words; for acceptance findings quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, <=40 words>"
}"""

ACCURACY = """ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer."""

BRIEFS = {
"blind": """You are a cynical, jaded reviewer with zero patience for sloppy work. BLINDNESS RULE: the diff file is ALL the context you may use. Do NOT read the worktree, the specs, or any other file — reading anything beyond the diff INVALIDATES your lens. Assume problems exist; be skeptical; look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place renamed, another missed — this is a RENAME diff: inconsistency IS the bug class)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (a pure vocabulary rename that touches a VALUE)

Your `evidence` MUST be exact diff lines pasted verbatim from the diff file. `source` = "blind".""",

"edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

This is a rename diff: the reachable paths are the ones the renamed identifiers flow through. Walk: the renamed enum variants (Warning_Sign.Node_Congested/Pipe_Congested) through event emit/read/render switch arms; the renamed command (Cmd_Set_Weights) through validate/apply/serialize/replay; the renamed balance keys through load/fail-fast/HUD read; the renamed palette key through load/fallback/render. Any path where the OLD name still binds (or BOTH names now exist) is an unhandled path.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack coverage in the diff; discard handled ones silently. No editorializing. `source` = "edge".""",

"acceptance": """Audit the diff against the spec and context docs above (the job briefing's Phase-2 discipline + the audit record's ruled table + the 2026-08-15 canon entry). Identify:
- A ruled rename NOT applied where the audit table says it applies (check the table's scope column against the diff's coverage)
- Violations of the Phase-2 discipline: "serialized contracts + LOG_VERSION untouched", "vocabulary ONLY", the T1/T2 fold rules
- Deviations from the two-tier ruling (docs say class queue; code/HUD keep lane)
- Scope drift — changes not asked for by the verdict

For each finding, reference the violated AC/constraint in `detail` (quote the exact phrase from the spec when possible). `source` = "acceptance".""",

"security": """OWASP-oriented security review of the diff. This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories do not apply. The realistic surface: the renamed balance.json keys' load path (jint validation unchanged? a missing-key default changed?), the renamed palette key's jcol fallback, and the demo parser's handling of comments/directives. A rename that weakens a fail-fast validation or changes a default = a finding. `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does the rename follow the codebase's naming conventions (snake_case procs, Pascal_Case types)?
- Residual inconsistency: `validate_set_emphasis`/`apply_set_emphasis` keep the retired word while the command is `Cmd_Set_Weights` — assess against the audit doc's scope column (deliberate or oversight?)
- Does the two-tier lane/class-queue split stay coherent (docs vs identifiers)?
- Any coupling/boundary change smuggled in with the rename (ODN-1 core purity, ODN-5 data-driven catalogs)?

`source` = "architecture".""",

"codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do the renamed identifiers' use sites ALL appear in the diff? Grep the worktree for each old name; every live hit outside historical docs is a finding (classify: code comment / demo comment / catalog string / canon doc).
- Does `state_congested` (palette.json key) match what palette_load reads? Does `node_congested_lead_ticks` match the loader + the HUD read + the tests?
- Are there existing tests this diff breaks? (The suite is green at this sha — a break would contradict that; file the CONTRADICTION, not the break.)
- Orphan code: any symbol no longer referenced after the rename?

`source` = "codebase".""",

"tests": """Test coverage analysis via traceability. This is a rename diff — the contract is: EVERY renamed identifier's tests renamed identically, expected event streams unchanged modulo enum renames, no assertion dropped or loosened, no test deleted. Verify per renamed symbol: its tests exist and assert the SAME behavior (the warnings_test event streams, the qos_test rejection matrix, the catalog fail-fast rows, the determinism/replay pins). A renamed test whose expected values shifted = a blocker. A deleted test = a blocker.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale (rename coverage: every renamed symbol's tests renamed + green)
- recommended_fix: what would raise the gate

Gate thresholds: PASS = every renamed symbol's tests intact + green at this sha (odin test core 183/183 — Perkins ran it); CONCERNS = a rename-coverage gap with tests still green; FAIL = a dropped/weakened assertion. `source` = "tests".""",
}

TEMPLATE = """# Perkins lens prompt — @LENS@ (@CHUNKDESC@, round 1)

**You are the `@LENS@` lens. Your assigned `source` tag is `@LENS@`. Your output file is `@OUTFILE@`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3) reviewing Packet-Plumber PR #55 (the 2026-08-15 terminology-canon rename). Perkins reviews; lenses find; nobody fixes. You run as a pi agent (model @MODEL@) with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — @CHUNKDESC2@ (review exactly these bytes): @DIFFPATH@
@WTLINE@@SPECLINE@

## The PR (scope)
@SCOPE@

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
@GUARDS@

## Legitimate findings here WOULD be
@LEGIT@

## OUTPUT CONTRACT (follow exactly)
@CONTRACT@

@ACCURACY@

## YOUR LENS BRIEF

@BRIEF@

## DONE
Write your JSON array to `@OUTFILE@` and stop. Do not fix anything. Do not run the interactive fix flow.
"""

man = json.load(open(f"{OUT}/chunk-manifest.json"))
SCOPE_BASE = ("Phase 2 of the 2026-08-15 terminology-canon ruling (networking-first vocabulary): a pure rename PR — "
 "drop ladder→drop precedence, strain→congestion, pressure→congestion, Pressure_Plan→Demand_Plan, "
 "Cmd_Set_Emphasis→Cmd_Set_Weights (tag 5 kept), lane→class queue in docs/comments only (two-tier), "
 "balance.json warning-key renames fold catalog_hash → deliberate proven T1 re-bless of all 29 demos; "
 "serialized contracts + LOG_VERSION 4 untouched; T2 pixels byte-identical. ")
SCOPES = {
 "c1": SCOPE_BASE + "THIS chunk = the CODE wave (core/ app/ harness/ demos/ data/ project-context.md): every identifier rename + the one ruled HUD legend string. The behavior must be bit-identical — name changes only.",
 "c2": SCOPE_BASE + "THIS chunk = the DOCS wave (_bmad-output canon docs: GDD + decision-log canon entry + architecture + stories-v2 + sprint-plan + specs + the audit record + field notes). Vocabulary-only prose edits + the new canon entry + the audit table.",
}
for c in man:
    if c["chunk"] not in SCOPES:
        SCOPES[c["chunk"]] = SCOPE_BASE + f"THIS chunk = a GOLDENS wave: {c['contents']}. Mechanical catalog_hash fold re-blesses — see the lens-guards for what is (not) a finding here."

def build(lens, chunk, desc, lines, files):
    diffpath = f"{OUT}/{chunk}.patch"
    outfile = f"{OUT}/{lens}-{chunk}.json"
    if lens == "blind":
        wtline = ""
        specline = ""
    else:
        wtline = f"- WORKTREE (verify every claim against the actual code here — ground truth, detached at sha {SHA}): {WT}\n"
        specline = f"- SPEC / CONTEXT (read the sections named; full files):\n{SPEC_BLOCK}\n"
    legit = LEGIT_CODE if chunk == "c1" else LEGIT_DOCS if chunk == "c2" else LEGIT_GOLDEN
    t = TEMPLATE
    t = t.replace("@LENS@", lens)
    t = t.replace("@CHUNKDESC@", f"{desc}, {lines} lines, {files} files")
    t = t.replace("@CHUNKDESC2@", f"{desc} ({lines} lines, {files} files)")
    t = t.replace("@OUTFILE@", outfile)
    t = t.replace("@DIFFPATH@", diffpath)
    t = t.replace("@WTLINE@", wtline)
    t = t.replace("@SPECLINE@", specline)
    t = t.replace("@SCOPE@", SCOPES[chunk])
    t = t.replace("@GUARDS@", GUARDS)
    t = t.replace("@LEGIT@", legit)
    t = t.replace("@CONTRACT@", CONTRACT)
    t = t.replace("@ACCURACY@", ACCURACY)
    t = t.replace("@BRIEF@", BRIEFS[lens])
    t = t.replace("@MODEL@", MODEL)
    return t

manifest = []
for c in man:
    for lens in ("blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"):
        p = f"{OUT}/prompts/{lens}-{c['chunk']}.md"
        with open(p, "w") as f:
            f.write(build(lens, c["chunk"], c["contents"][:600], c["lines"], c["files"]))
        manifest.append([c["chunk"], lens, p, f"{OUT}/{lens}-{c['chunk']}.json"])
with open(f"{OUT}/brief-manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
print("manifest:", len(manifest), "briefs across", len(man), "chunks")
