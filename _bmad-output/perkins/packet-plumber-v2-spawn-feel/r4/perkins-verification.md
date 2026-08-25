# Perkins r4 — fix audit + mechanical verification (reviewed sha 9c0f11e)

## Fix audit (prior r1 findings, classified against the r4 worktree)

### Blockers
- **B1 FIXED ✓** — app/render/spawn_fx.odin spawn_fx_draw_highlight: `rad := f32(SPAWN_HIGHLIGHT_RADIUS_TILES)`;
  tile units both sides; comment cites Perkins r1 B1. Pixel-verified: r1→r3 04000ms diff bbox = 305x6+656+357 —
  EXACTLY the PR body's documented "removed far-pipe band, x 656→960 at the pipe's y". Non-highlight frames
  byte-identical (03600/03900/04250/04400 md5-equal r1↔r3).
- **B2 FIXED ✓** — spawn_fx_test.odin pending pin reworked: legal Cmd_Place_Router at (13,6) @t77; materialization
  assert (3 junctions), !replay_error, predict==actual, ANTI-VACUITY (no-pending P0 != with-pending P1), NEGATIVE
  leg (out-of-separation (13,10) rejected both sides, prediction still matches). Suite-green (render 53/53).

### Warnings — ALL SIX STILL PRESENT
- W1 reduced-motion highlight: spawn_fx.odin:435-437 `if v.reduced_motion { return }` — header/PR body still say
  "the highlight is steady". Doc/code divergence persists.
- W2 chip hairline line-alpha: view.odin:1232 `out.a = u8(255 * fade)` before DrawRectangleLinesEx — rlsw trap
  reintroduced, still present.
- W3 init/destroy dead code + reveals latch: ZERO callers of spawn_fx_init/spawn_fx_destroy repo-wide (grep).
  Observable: `+++ leak 192B @ spawn_fx.odin:146:spawn_fx_feed()`; render suite 3,794 leak lines (r1: 3,318 added).
- W4 clone-completeness residual: clone still field-for-field complete (re-checked ALL [dynamic] struct fields in
  core — topology 14, routing 3, bundles 6, flow 7, crisis 6, health 9, era_gate 5 vs clone list — complete;
  rebases added no Run_State [dynamic] fields). Residual-risk warning stands.
- W5 reveal-buffer >4 trim untested: no 5+-event feed test in spawn_fx_test.odin (walkback covers 2). Still untested.
- W6 reduced-motion ring/highlight untested: only reveal reduced-motion pin exists. Still untested.

### Notes (carry-forward status)
- N1 PR body nh-20000 "ring burst" mis-description: wording unchanged in _pr_body_spawn_feel.md ("+ the ring
  burst"); analysis stands (harness capture at t400 targets window 480, lead 80 > 10 → no telegraph predicted
  for t400). STILL PRESENT (note).
- N3 sfx_fixture != demo recipe: harness seed_fixture = (8,15)/(20,15)/(32,15) (harness/catalogs.odin:53-55);
  sfx_fixture = (10,10)/(12,10)/(14,10) + (34,15); fixture comment claims "the demo's exact spot"; ALSO the
  fixture omits the recipe's second draw (0→1) and its 1→3 draw (span ~22.6 > 14) is silently rejected →
  pipe-less topology. STILL PRESENT (note; B2's rework made the pending pin real, so severity stays note).
- N6 unreachable dedup-reset branch: still in spawn_fx_predict. STILL PRESENT (note).
- N7 `_ = before` residue: still in test_spawn_fx_feed_and_reveal_math. STILL PRESENT (note).
- N8 telegraph guard u64 wrap at interval<10: still unguarded. STILL PRESENT (note; unreachable at shipped 80).
- N10 render-owns-Run_State-deep-copy: settled ruling — NOT re-litigated (documented accepted risk).
- NEW delta candidates from blind lens: demo capture comments misstate reveal math (4100ms comment claims
  scale ~0.75/fade ~0.8; actual envelope at age 2: k=0.25 → scale 0.494, fade 0.409 — CONFIRMED misstatement);
  negative-leg comment says "2 tiles" but (13,10)→(12,10) is 1 tile (CONFIRMED).

## Mechanical checks (all run by Perkins in the r4 worktree)
- `odin test core`: **236/236 PASS**; bad frees = exactly 2, both health_test.odin:877/910 (pre-existing,
  untouched files) ✓
- `odin test app/render`: **53/53 PASS** (suite grew past the PR body's "22/22" via wave-rebase tests); 0 bad frees
- `tools/harness.sh run`: **48/48 demos green** ✓ (PR body claim verified)
- `tools/ci-local.sh --mac`: **11/11 gates green** ✓ (incl. golden harness T1+T2+replay, input parity 27/27)
- Goldens vs demo: 9 captures in spawn_feel.dem ↔ 9 committed PNGs ✓; spawn_feel.t1 + log.bin present ✓
- Pixel audit (ImageMagick, mechanical only per the non-k3 vision caveat):
  - r1→r3 delta: 04000/04100 = 1584px (the B1 band, exact documented coords); 07600/07900 = 254px each
    (24×114 vertical band = #82 packet trails on in-flight packets — the documented rebase cause);
    08000 = 1838px (trails + band); nh-20000 = 5254px (same two causes). No UNDOCUMENTED drift found.
  - Ring center: 03600↔03900 within-generation diff isolates the two annuli (58×58 + 46×46), centroid
    (351.5,263.5) IDENTICAL in r1, r3, r4 — the telegraph ring did not move a pixel across B1 and #83. ✓
  - Reveal envelope vs settled 04400: r4 = 3176→3272→1907→0 (the +96px 04100 bump = the ring burst at max
    radius/age 2 — same shape as r1's accepted 5513→5633→2746→0; envelope math unit-pinned by
    test_spawn_fx_feed_and_reveal_math: age0 (0.4,0.3) → mid-interpolated → expired ✓). Footprint counts
    shrink r1→r3→r4 exactly per the documented causes (band removal, #83 smaller sprites).
- Aesthetic verdict: DEFERRED (non-k3 round; mechanical only, per the vision caveat).

## Lens wave status (429/1308 provider cap)
- glm-5.3 (zai-coding-cn) hit the account 5-hour usage cap mid-wave (code 1308; reset 2026-08-23 09:31:51
  provider-TZ). blind.json delivered (11 findings, parses). edge/acceptance/security/architecture/codebase/tests
  died after retry exhaustion. Serial re-dispatch planned after the reset (r1 playbook: the wave recovered via
  serial re-dispatches under the same provider's 429 pressure).
