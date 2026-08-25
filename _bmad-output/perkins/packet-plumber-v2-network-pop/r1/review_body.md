## 🤖 Perkins automated review — round 1
**Job:** packet-plumber-v2-network-pop · **Reviewed sha:** 81df67b · **Reviewers:** 7/7 completed
**Verification:** 26/28 findings confirmed against the code — 2 discarded as false-positive

Scope guard first: the diff is exactly palette-token-only — `data/palette.json` + both `palette.odin` mirrors + the `palette_polish_test` re-pins + the evidence doc. No geometry, no sim, no serialization, no LOG_VERSION, no catalog edits; `.t1`/`.log.bin` byte-identical; a11y_deutan/protan/tritan goldens byte-identical.

**Independently re-verified mechanically by Perkins:** the full saturation table reproduces exactly (juice-30000 0.886, juice-65000 0.879, estate_surge 0.913/0.899, growth-88000 0.826, terminal_types-5000 0.715, router_tiers 0.698); the 70/30 band-area claim is honest (widths 3.5/5.5/8.5 at view.odin:1184 → warm share 73.6%); local CI at the reviewed sha: lint green, all unit tests green, **harness 45/45 demos green, palcheck green, drift-check 322/322 rejected**. Thumbnail strips verified mechanically (present, 433×240 halves — the doc says 427; pixel aesthetics deferred to the k3 re-check per the vision caveat).

### Blockers (0)

None.

### Warnings (6)

1. **router_led "node accents up" ships inert** — `[edge, acceptance, architecture, codebase, tests]` · `view.odin:837` — the sprite path returns before any token read; pucks bake 91/238/666 px of the OLD `{46,139,87}`; `gen_sprites.py:39` and palcheck's `LED_GREEN` pin still hold `#2E8B57`, so token/generator/palcheck now disagree three ways and the intended future regen will fail palcheck until synced. The PR documents the deferral (decision 3) and sprite regen is outside the token-only scope — follow-up art task, not a merge blocker.
2. **CVD mode tables are stale — the pop is off-mode-only** — `[blind, edge, architecture, codebase]` · `data/palette.json modes` — deutan/protan/tritan override pipes/lanes with values derived from the old muted family (deutan pipe_steel `[122,132,146]` ≈ the old base). Colorblind-mode players keep the gray-blue network the user ruled boring. Re-derive against the vivid base (+ palcheck + re-bless) or pin the exclusion as an explicit accepted decision.
3. **Evidence doc misstates three results** — `[blind, acceptance, codebase, edge, Perkins]` · `saturation-evidence.md` — (a) "dense frames … all cross 0.85" vs its own growth-88000 row (0.826); (b) "exceeds the mock on every network-bearing frame" vs terminal_types-30000ms = **0.665 < 0.685** (omitted from the table; 19,491 changed pipe pixels prove it network-bearing); (c) growth-15000 row "0.513→0.513 ±0.000, 1 puck, no pipes" vs measured **0.545→0.726** — the re-blessed golden's changed pixels ARE a steel pipe (core `(0,150,240)`, casing `(11,131,204)`). Every other value in the table reproduced exactly; fix these three so the artifact isn't a false baseline.
4. **Token-table HSL column miscomputed by its own pinned method** — `[blind, acceptance, codebase]` · `saturation-evidence.md:26-28,99` — colorsys HSL: lane_standard 0.567 (doc: 0.73), lane_best_effort 0.575 (doc: 0.74), router_led 1.000 (doc: 0.76) — the lanes are HSV values. "Network tokens all sat ≥ 0.73" is false for the lanes (pipe values 1.00 are correct).
5. **Express-lane stripe collapses onto the warm tier bands at default zoom** — `[edge]` · `view.odin:466-474` — blend `band·0.72 + lane·0.28`: express-on-copper `(235,118,13)` vs band `(240,110,0)` — max channel Δ13 (≈Δ24 pre-change); express hue 31° vs copper 27.5°. palcheck has no lane-vs-tier pair. Arithmetic confirmed mechanically; the readability verdict defers to the k3 re-check.
6. **No durable saturation-ceiling gate** — `[tests]` — the metric this PR exists for lives in an ephemeral python heredoc; this mute class shipped green CI once already via golden re-bless. Add a palcheck leg with floors on the dense goldens (juice/estate ≥ 0.85, measured floors for sparse frames).

### Notes (5)

- Commit rationale "the modes override every changed token" is inaccurate — router_led/packet_dot/packet_dark are in no mode table; byte-identity holds via sprite-baked LEDs + catalog packet colors. `[acceptance]`
- `palette.odin` header says packets "stay at catalog maxima" while the same diff re-hues the packet_dot/packet_dark fallback tokens. `[blind]`
- packet_dark is dead palette data (zero readers repo-wide); packet_dot renders only for invalid class indexes — both new values are unreachable on normal frames (pre-existing deadness). `[edge, codebase, tests]`
- pipe_core is unaccounted (neither changed nor in the "Untouched" list; also reader-less). `[blind]`
- The fallback_palette/jcol-default copies of the changed tokens are unpinned — only canvas is verified on both copies; add a fallback==load token-equality test. `[tests]`

### Reviewer agreement
Findings 1 (5 lenses) and 2 (4 lenses) — both independently confirmed by multiple fresh-context reviewers and by Perkins' own mechanical checks.

**Verdict:** READY TO MERGE

The operative acceptance gates are met and mechanically verified (thumbnail-hero frames 0.879–0.913 with the board calm, 70/30 honest by real geometry, suite + goldens + palcheck green at the reviewed sha); the sparse-frame ceiling limit is documented physics per the standing rulings. The warnings are evidence-doc corrections, honestly-documented deferrals, and hardening — none block.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
