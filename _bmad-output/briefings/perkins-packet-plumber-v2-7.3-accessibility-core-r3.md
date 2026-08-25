# Perkins briefing — packet-plumber-v2-7.3-accessibility-core r3

- **Job:** packet-plumber-v2-7.3-accessibility-core · **Round:** 3 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/72 (Story 7.3: accessibility core)
- **Reviewed sha:** `70e3e9195dbc5e989c0eef7880fef2f5f1c4c9b8` (head of `v2-7.3-accessibility-core`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-7.3-accessibility-core.md` + the r2 verdict (`prior_findings` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/consolidated.json` — 4 blockers @217f6a8) + the PR body's r2→r3 section.
- **Model:** zai-coding-cn/glm-5.3 (STANDING reasoning primary — user ruling 08-19 night; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3`) — and PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards (fix-audit round — r3)

- **Verify EACH r2 blocker fix BITES (the round's bar: each fix BITES):**
  - B1 (r2) — delta-0 activate NO-OP: the adjust site must normalize `delta==0 → +1` for the cycle rows (or cycles advance on 0), AND the tap path (touch row-tap) must be pinned — a touch-only player must be able to change palette + scale in BOTH directions (the r2 miss was a no-op; r1's was a one-way ratchet). Verify with a probe/test that the step and mode actually change.
  - B2 (r2) — QoS manual editor: label/value positions must derive from the SAME scaled rects as the hit tests (no raw x+44 / font 14 draw at ×1.25/×1.50; values must not render inside the [−]/[+] buttons, lanes 1–2 values must not land on the previous lane's [+]). Verify the geometry at both scales.
  - B3 (r2) — linear_to_srgb WRONG in BOTH `tools/derive_a11y_palettes.py:40` AND `harness/palcheck.odin:45`: the fix must implement the correct inverse (`c * 12.92 if c <= 0.0031308 else 1.055·c^(1/2.4) − 0.055` — multiply, not divide; the forward threshold is 0.0031308, not 0.04045) in BOTH files, re-derive/re-emit the mode tables, re-verify separation (the pinned min sim-dists 51.3/54.7/43.0 may MOVE — re-bless if they do, fold-only), and the oracle must measure in the corrected space. The derivation record must now actually implement the Machado sRGB↔linear pipeline it claims.
  - B4 (r2) — test gate: the delta-0 path must be pinned (no longer a live no-op that's unpinned), the modal world-input suppression + S-ownership gate pinned (the two new parity scenarios per the badge-out: settings_modal_blocks_world + settings_s_ownership; 27/27 parity). Verify the parity scenarios bite (a regression in the suppression/ownership fails them).
- **ONE hard blocker class (carried): the never-color-alone invariant (ODN-1)** — every state readable WITHOUT color under deutan/protan/tritan; the palcheck oracle must measure in the CORRECTED sRGB space (verify the fix didn't break the oracle's bite).
- **Presentation-only discipline (carried):** view-lane only — no core/, no LOG_VERSION, no catalog edits; pre-existing goldens untouched; ×1.00 identity holds.
- **What NOT to re-litigate:** the r2 4-blocker fixes (this round audits they LANDED, it doesn't re-argue them); user rulings (scaling knob, settings modal, reduced-motion static); applied canon.
- **CI note:** GitHub Actions is billing-blocked today. Local suite is ground truth: `tools/ci-local.sh --mac` 10/10 per the badge-out (incl. the four test binaries + palcheck + 27/27 parity) — re-run at minimum the palcheck (with a poison pair) + parity + settings/hud binaries.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 72` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r3`, `prior_findings` = the r2 `consolidated.json` (fix audit first, carry-forward markers). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 72 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 72 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 3 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 72 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-7.3-accessibility-core-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
