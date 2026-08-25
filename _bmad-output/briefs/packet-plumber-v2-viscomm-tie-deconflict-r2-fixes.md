# Briefing — packet-plumber-v2-viscomm-tie-deconflict (r2 fixes: fold Perkins r1 verdict)

Model: zai-coding-cn/glm-5.3 (pinned; flash is 402-down — ops interim per 08-19
precedent). You are the fix minion for PR #99, round 1 verdict NEEDS CHANGES.

## Repo / workspace

- Repo: /Users/moses/code/packet-plumber (remote: solarity-services/Packet-Plumber)
- Worktree (yours, already checked out on the PR branch, clean @4b3a887):
  /Users/moses/code/packet-plumber-wt-viscomm-tie
- Branch: packet-plumber-v2-viscomm-tie-deconflict (PR #99, base v2 — plain
  commits on top; NEVER force-push)
- Verdict (full detail): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-tie-deconflict/r1/verdict.md
- Ledger CLI: /Users/moses/code/bin/ledger
- Job row: packet-plumber-v2-viscomm-tie-deconflect

## Fixes (in priority order)

### BLOCKER (must fix; r2 will re-verify by mutation)

Shape gate is vacuous against the draw path: deleting the
`if !tie_dash_on(i) { continue }` guard in `draw_tie_mark`
(app/render/assist.odin:~505-509) passes ALL tests (proven twice by mutation
probe — 83/83 green with a solid ring).

Fix: pin the draw path itself — factor the per-segment draw enumeration into a
pure proc (e.g. `tie_dash_segments() -> [dynamic]int` or equivalent) that
`draw_tie_mark` CONSUMES for its loop, and test that the enumeration equals
`{i : tie_dash_on(i)}`. ACCEPTANCE = MUTATION LEG: revert `draw_tie_mark` to a
solid ring (guard deleted / enumeration bypassed) → tests MUST FAIL. Run the
mutation leg yourself before pushing: delete the guard, `odin test app/render`,
confirm a FAILURE, restore, confirm green. Record both runs in your final note.

### WARNING W2 — hue canon (must fix)

`route_tie` violet (264.35°) is only 14.03° from `router_tier_high` (250.32°) —
below the 15° node-signal canon; both are node-centered rings drawn on routers.
The hue test at app/render/palette_polish_test.odin:~158 only checks pipe tiers.

Fix: add `router_tier_basic/mid/high` to the tiers array AND shift route_tie's
hue to clear 15° from router_tier_high (toward blue/magenta). Update: the
palette.json token bytes, the byte-pin test (expect_color), the palette.json
_comment_ claims, and re-derive/verify CVD separations still pass worst-pair
thresholds. Keep state_congested separation ≥ 90° (see note N8 — add the
explicit numeric pin while you're in there).

### WARNINGS W3+W5 — CVD oracle pair (must fix; one fix in two oracles)

The exact pair this PR de-conflicts (route_tie vs state_congested) is missing
from both oracles: add `[2]rl.Color{p.route_tie, p.state_congested}` to the
signal pairs in `a11y_separation_check` (harness/palcheck.odin:~96-110) AND the
same pair to `pair_list` in tools/derive_a11y_palettes.py.

### WARNING W1 — derive script reproducibility (must fix, small)

tools/derive_a11y_palettes.py:97 bare `json.load` chokes on the `//` comments
in data/palette.json (reproduced: strict parse fails at line 11). Fix: strip
`//` comments (regex prefilter) before json.load. Then RE-RUN the derive script
against the SHIPPED data/palette.json and commit reproducible output — the a11y
numbers must regenerate from repo bytes, not a private stripped copy. (With W2's
hue shift, re-derive and confirm the modes tables still separate — W2 and W1
interact.)

### NOTES (fold the cheap ones; judgment allowed, don't gold-plate)

- N4: PR-body 225° claim is impossible (wraps to ~135°). Post a short PR
  comment correcting the number (225° unwrapped → state the circular distance).
- N7: replicate draw_ring_annulus's degenerate guard (`r_out <= 0 || r_in < 0
  || col.a == 0 → return`) at the top of draw_tie_mark.
- N3: drop or compile-time-assert the hard-coded "6 dashes"/"30 deg" comments.
- N2/N6 (geometry dedup into draw_ring_annulus with a segment predicate):
  fold ONLY if it falls out of the blocker fix naturally — the blocker's pure
  enumeration proc may make this trivial; otherwise leave with a note.
- W4-advisory + N9: the palcheck presence assertion (route_tie bytes unchanged
  across all three modes) — add it alongside W3 (cheap, same file).

## Verify (all must pass before push)

```bash
tools/lint.sh
odin test core
odin test app -out:bin/app-test && odin test app/render -out:bin/render-test && odin test app/input -out:bin/input-test && odin test app/audio -out:bin/audio-test && odin test harness -out:bin/harness-test
tools/harness.sh palcheck   # if that's the entry — check tools/harness.sh
```

Plus the mutation leg (blocker acceptance) with both runs recorded.

## Deliverable

Commits on packet-plumber-v2-viscomm-tie-deconflict, push to origin. Then:

```bash
/Users/moses/code/bin/ledger set packet-plumber-v2-viscomm-tie-deconflect in-review "r2 fixes pushed @<short-sha>: blocker (draw-path pin + mutation leg), W2 hue shift, W3+W5 oracle pair, W1 derive reproducibility, notes folded <list>"
```

(The row is currently `working` — this set is a real transition; the note rides it.)

Final message back: sha pushed, per-finding disposition (fixed/folded/deferred
+ why), mutation-leg run results (fail-on-solid proof + green restore), verify
suite results, W2's new hue value + computed deltas (vs router_tier_high, vs
state_congested, worst CVD pair).

## Rules

- Never force-push; never merge; Perkins r2 fires on your new head automatically.
- Worktree ends `git status --porcelain` EMPTY (build artifacts in bin/ are fine
  if gitignored).
- Perkins review of THIS code is adversarial: a gate that can't fail is a
  blocker. Make every gate you touch able to fail.
