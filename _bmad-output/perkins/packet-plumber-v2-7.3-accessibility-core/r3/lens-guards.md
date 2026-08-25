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

## Lens-specific guards
- ONE hard blocker class: the never-color-alone invariant (ODN-1) — every state readable WITHOUT color under deutan/protan/tritan.
- Presentation-only discipline: view-lane only — no core/, no LOG_VERSION, no catalog edits; pre-existing goldens untouched; ×1.00 identity holds.
- Do NOT re-litigate: user rulings (scaling knob 100/125/150, settings modal, reduced-motion static), applied canon, prior-round findings already applied.
- Prototype-rigor (NOT defects): ASCII labels, minimal settings surface, follow-up scope exclusions (no remapping/TTS/localization).
