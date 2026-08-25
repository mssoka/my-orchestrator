You are reviewing a code diff as ONE specialist lens in a multi-lens headless review (Perkins round 3 — FINAL automated round, fix-audit). You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. NEVER edit any repository file.

Read these inputs first, exactly:
- DIFF (canonical review surface — the r2->r3 fix delta, d91109e..b467f9d; review exactly these bytes; never re-fetch or regenerate the diff): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r3/delta.patch
- FULL PR DIFF (context only, if you need the surrounding change the delta sits in — already reviewed in rounds 1-2): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r3/diff.patch
- WORKTREE (checkout at exactly the reviewed sha b467f9d — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.4-input-parity-r3
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.4-input-parity-r3/project-context.md
- SPEC / CONTEXT (read both):
  - /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.4-input-parity.md (original job briefing — the spec)
  - /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r3/spec-story-5.4.md (story card)

--- ROUND-SPECIFIC LENS GUARDS (from the chief reviewer — obey strictly) ---
This is ROUND 3 — the FINAL automated round, a fix-audit re-review. Round 2 (sha d91109e) filed 2 blockers + 17 warnings + 14 notes (CHANGES_REQUESTED); the minion's fix commit b467f9d IS this diff (one fix commit + a two-manifest golden re-bless). The chief reviewer has SEPARATELY audited every r2 finding as fixed/still-present, WITH live mutation testing of the two blocker pins. Your budget goes to NEW defects: defects the fix delta itself introduces (app/input/mouse.odin, app/main.odin, harness/parity.odin, harness/main.odin, tools/ci-local.sh, goldens/) and anything rounds 1-2 missed in those files. The rest of the PR was already reviewed twice — do not re-review it.

**The ONE hard blocker — mouse-path parity.** The intent layer is parity-BY-CONSTRUCTION [FORGE #6]/[ODN-12]: raw device event -> typed Intent -> validated Command. Any behavioral delta in the mouse path vs the pre-change handle_input is a blocker. This round the parity-critical edits are exactly: the map-time `esc_deselect` (sel_pipe/sel_node cleared at MAP time when ESC + not placing), `drag_eff := inp.drag.active && !esc_cancelled` gating the release chain's drag branch, the Press_Anchor re-gating in the right+left chord (`has_left && placing_eff >= 0 && !esc_cancelled`), and the Game_Over retry `break`. Trace same-frame combinations (ESC/right/left/release/keys) through map-time state -> queued intents -> executor order (Cancel always executes before later same-frame intents; Select/Drag_Release/Place_Release re-check their latches at EXECUTION time) before filing.

**Do NOT re-file these KNOWN / already-tracked items** (filing them wastes the round):
- VERIFIED-FIXED this round (mutation-tested or code-verified by the chief): r2-B1 (map-time ESC deselect; pinned by input_parity_esc_ui — deleting the deselect block FAILS the suite); r2-B2 (drag_eff; behaviorally correct — the true non-moved shape [board press while placing, then ESC + same-point release] is a no-op via the Select executor's execution-time latch re-check, and WITH drag_eff removed that shape DOES click-select); ci-local.sh input-parity gate; drive_parity single-apply (pp.step empty batch) + the two re-blessed manifests; reject assert && -> || + last_reject != .None assert; demolish sel_pipe=-1 preset + post-demolish clear assert; esc_press press_swallowed assert; pad_cursor split into up/wrap; pan scenario re-scripted to the live order; input-parity arg validation; zero-device scenario guard; sc.mouse/touch/pad deletes; core:os import removal; Weights/Set_Weights label fixes; class_cycle comment fix; rename-note fix (Cmd_Set_Emphasis); Game_Over R+Enter break; Press_Anchor chord gating.
- ALREADY-FILED by the chief this round (do not duplicate): (a) input_parity_esc_release_place's shipped shape scripts a MOVED release (anchor at the tray chip, release at n1) — deleting drag_eff's `!esc_cancelled` keeps the suite green, so the drag_eff leg of the B2 fix is unpinned by the shipped scenario [test-fidelity warning]; (b) `esc_pressed` (app/input/mouse.odin:58) is write-only dead state [note].
- CARRIED, still open (tracked from r1/r2 — do not re-file): phase2_blocked tray/placement-press disjuncts unpinned; on_ui_release + QoS-row hook legs unpinned (only the demolish-button hook stub is wired); pad Start unpinned; pad_alive guard + pad dead-slot skip unexercised; placement release gates unpinned; click_select terminal/empty-ground-clear branches unpinned; lane keys S/B + class key .One undriven; class-key catalog cap (One/Two hard-stop); moves[] buffer silent overflow (now [4] + comment); check_lane_emphasis comment claims equality 'already proved'; bless-hint verb names `harness save`; touch placing gates unreachable in the harness; one shared drag slot across devices; Game_Over retry surface unpinned; right-press-WHILE-placing / right-press-mid-drag / U-preview-arm transcription legs unpinned; touch press clearing the mouse swallow latch; demolish-node flavor + Delete-key twin unscripted; mixed-device same-frame scenarios unscripted; .memlog.md content staleness.
- ACCEPTED-STANDING (never re-litigate): untyped rawptr effect-hook `user`; QoS helpers hosted in the input package; the FORGE #6/ODN-12 intent-layer architecture itself; validation at the Command stage; no LOG_VERSION bump (inputs never serialized); the #55 terminology adoption (Cmd_Set_Emphasis -> Cmd_Set_Weights); the deliberate two-finger-pan no-op (camera work deferred per §18 OQ-1); the pre-existing view-only hover card's rl.GetMouseX/Y.

**Verify specifically:**
- The delta is fix-shaped: no new scope, feature work, or mechanics smuggled into the fix commit.
- NO LOG_VERSION bump, NO serialization change (inputs are never serialized — replay [E10] unaffected).
- The new/changed scenarios (esc_ui, esc_release_place, pad_cursor_up, pad_cursor_wrap, demolish, reject, esc_press, pan) must ASSERT what their comments promise — a vacuous or self-fulfilling pin is a finding (but see ALREADY-FILED (a) above).
- The re-blessed goldens: catalog_hash + seed + ticks unchanged, only the per-tick hashes changed (consistent with the double-apply removal). Any OTHER golden drift is a finding.

**Severity calibration:** this is a gameplay prototype slice in its FINAL automated round. Prototype-rigor concerns (missing mobile UI polish, no physical-device testing, deferred camera work) are NOT blockers. Reserve "blocker" for genuine correctness/parity/determinism defects. Do not manufacture blockers from the carried warning set.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

--- OUTPUT ---
When your analysis is complete, write your final answer as ONE valid JSON array to this EXACT absolute path using the Write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r3/security.json
The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The JSON file is your ONLY deliverable. Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not do anything else.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.
