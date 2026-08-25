# Perkins lens prompt — security (health_win.t1 [fragment 1/2]; health_win.log.bin, 3176 lines, 2 files, round 1)

**You are the `security` lens. Your assigned `source` tag is `security`. Your output file is `/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1/security-g4.json`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3) reviewing Packet-Plumber PR #55 (the 2026-08-15 terminology-canon rename). Perkins reviews; lenses find; nobody fixes. You run as a pi agent (model deepseek/deepseek-v4-flash) with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — health_win.t1 [fragment 1/2]; health_win.log.bin (3176 lines, 2 files) (review exactly these bytes): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1/g4.patch
- WORKTREE (verify every claim against the actual code here — ground truth, detached at sha b9d5006): /Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-terminology-audit-r1
- SPEC / CONTEXT (read the sections named; full files):
  - Perkins briefing (your charter + lens-guards): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1/spec/perkins-briefing-r1.md
  - Job briefing (the implementing minion's spec — Phase 1 audit + Phase 2 rename discipline): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1/spec/job-briefing.md
  - The terminology audit record (the lavish decision table the user ruled on): /Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-terminology-audit-r1/_bmad-output/implementation-artifacts/terminology-audit-v1.md
  - The canon entry (2026-08-15 ruling, THE spec this PR must match): /Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-terminology-audit-r1/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md (search "Terminology canon")


## The PR (scope)
Phase 2 of the 2026-08-15 terminology-canon ruling (networking-first vocabulary): a pure rename PR — drop ladder→drop precedence, strain→congestion, pressure→congestion, Pressure_Plan→Demand_Plan, Cmd_Set_Emphasis→Cmd_Set_Weights (tag 5 kept), lane→class queue in docs/comments only (two-tier), balance.json warning-key renames fold catalog_hash → deliberate proven T1 re-bless of all 29 demos; serialized contracts + LOG_VERSION 4 untouched; T2 pixels byte-identical. THIS chunk = a GOLDENS wave: health_win.t1 [fragment 1/2]; health_win.log.bin. Mechanical catalog_hash fold re-blesses — see the lens-guards for what is (not) a finding here.

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
- **🚨 THE ONE HARD BLOCKER — serialized contracts untouched.** LOG_VERSION stays 4 (only its comment may change); the wire format is byte-identical on all 29 `.log.bin` — Perkins has ALREADY VERIFIED: old-vs-new differ in EXACTLY the 8 catalog_hash bytes at offset 17 (old `bdc90b1363c93d8b` → new `8f94df8eb817dddb`), sizes identical, and the command tag constant keeps value 5 (only its NAME changed `CMD_TAG_SET_EMPHASIS`→`CMD_TAG_SET_WEIGHTS`). ANY non-catalog-hash wire delta (a tag value, a payload layout, LOG_VERSION, a serialized field) = a BLOCKER.
- **🚨 GOLDEN DISCIPLINE — Perkins has ALREADY verified the fold mechanically.** (a) `harness run` is green at the reviewed sha: all 29 demos reproduce the NEW goldens tick-for-tick (T1 manifest + replay bit-for-bit + T2 captures). (b) THE SPLICE PROOF IS REPRODUCED: in a scratch copy with ONLY `cat.hash` forced to the OLD value (sim code untouched), all 29 demos reproduce the OLD blessed goldens EXACTLY — every tick of ~22k ticks — and the OLD .log.bin files replay green. The fold is provably the only change. (c) Every changed line in goldens/*.t1 is either the `catalog_hash` header or a `<tick> <16-hex>` hash line; tick numbering is continuous 1..N with old count == new count on all 29; all 29 carry the same old→new hash pair. (d) ZERO PNGs in the diff — T2 untouched (the harness capture path never calls the app's `draw_hud`; the renamed HUD legend string renders no golden pixel). DO NOT file "every tick hash line changed" — that IS the verified fold. DO file: a non-hash line changed inside a golden (seed/ticks/demo/logic_hz), a numbering gap/dupe/reorder, a catalog_hash value other than the ruled pair, a .t1 without its .log.bin pair, an existing golden whose header did NOT change (stale bless), ANY .png anywhere in the diff.
- **🚨 DO NOT RE-LITIGATE THE 2026-08-15 VERDICT.** The rename IS the ruling, applied: drop ladder→drop precedence; strain→congestion/utilization; pressure→congestion; Cmd_Set_Emphasis→Cmd_Set_Weights; Pressure_Plan→Demand_Plan; lane→class queue is TWO-TIER BY DESIGN — docs/architecture/comments say "class queue", the player-facing surface + HUD + core identifiers KEEP "lane" (the 2026-08-12 spatial-lane visual + EF/AF/DF class names stand). GDD §M4 keeps "pressure" as the plumbing-metaphor gloss in prose where it names the metaphor itself. A doc saying "class queue" where code keeps `lane` is CORRECT, not a contradiction.
- **Historical specs keep authoring-time spellings.** spec-3-2 / spec-5-8 / spec-traffic-model etc. record what a story did WHEN it landed (e.g. spec-5-8's "`Cmd_Set_Emphasis` evolves its payload … LOG_VERSION 3→4" is history) — do NOT file old identifiers in historical narrative as misses. DO file old identifiers in LIVE surfaces the sweep should have caught (code comments, demo comments, catalog _comment strings, canon docs).
- **Scope guard:** vocabulary ONLY. Any mechanic/balance/rendering/behavior change hiding in the hunks = a blocker. No new player commands (the command SET is unchanged — only a rename). No HUD pixel changes beyond the ruled legend string (which renders no golden).
- **The balance.json `_comment` + key renames fold catalog_hash (ODN-11)** — this is the declared, proven reason for the T1 re-bless; do not file the fold itself. data/demand.json's `_comment` still says `scripted_plan_pressure` and demos/qos_manual.dem + qos_auto.dem comments still say `Cmd_Set_Emphasis` — Perkins already found these sweep residues; a lens may corroborate at NOTE level (do not escalate; demand.json folds catalog_hash so a later fix re-blesses).
- **Em-dashes are OK in PP** (the RT ban does not apply). Prose grammar warts created by the mechanical rename (e.g. "congested/congested", "never congestion" as a verb) are legitimate NOTE-level findings — name the file:line.
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical. A rename that touches ANY serialized byte (beyond the proven catalog_hash fold) breaks the spine.

## Legitimate findings here WOULD be
- **A re-bless beyond the fold**: a non-hash line changed (demo name, seed, logic_hz, ticks count), a hash-line numbering gap/dupe/reorder within the fragment, a tick line added/removed (count must equal the header's `ticks`), a catalog_hash value other than `bdc90b1363c93d8b`→`8f94df8eb817dddb`, a missing .log.bin for a demo with a .t1 (or vice versa).
- **Do NOT file**: per-tick hash lines changing (that IS the verified fold), the catalog_hash header changing, .log.bin binary diffs (Perkins verified exactly 8 header bytes per demo), the fragment split itself (the CHUNK NOTE is review tooling, not content).

## OUTPUT CONTRACT (follow exactly)
Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
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
}

ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer.

## YOUR LENS BRIEF

OWASP-oriented security review of the diff. This is a single-player desktop game core (Odin) with JSON catalogs + a binary replay log + a demo parser — most OWASP categories do not apply. The realistic surface: the renamed balance.json keys' load path (jint validation unchanged? a missing-key default changed?), the renamed palette key's jcol fallback, and the demo parser's handling of comments/directives. A rename that weakens a fail-fast validation or changes a default = a finding. `[]` is an honest answer. `source` = "security".

## DONE
Write your JSON array to `/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1/security-g4.json` and stop. Do not fix anything. Do not run the interactive fix flow.
