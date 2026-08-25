## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-v2-blender-silhouettes · **Reviewed sha:** 087d23a · **Reviewers:** 6/7 completed (architecture lens failed twice on provider 429/timeouts — account-wide congestion; compensated wave, findings exist so the degraded guard is not triggered)
**Verification:** 14/15 findings confirmed against the code — 1 discarded as false-positive

### Fix audit (r1 → r2, verified against the code, not the fix message)

| r1 finding | status | verification |
|---|---|---|
| **B1** order drift vs `files[]` | **FIXED** | `SPRITE_ORDER` mirrors `files[]` exactly (puck_1..3 at 6-8, small_biz 9, campus 10); `main()` asserts build == pin before writing; JSON order emitted from the const by construction |
| **B2** P0 contract zero coverage | **FIXED as specified** | `tools/test_sprite_order.py` wired as lint gate 7 (CI-enforced); **mutation-tested both legs** — swapping the terminals AND re-introducing the exact r1 order both fail loudly. Residual third-leg gap → W2 below |
| W1 determinism wording | FIXED | attributed to unchanged-SPEC re-runs (docstring + spec §intro/§3) |
| W2 ring convention | FIXED | 0.03/side (+0.06 total) unified in spec §0, README, code |
| W3 ridge axis | FIXED | spec §1 now says short axis (Y), matching `add_gable` |
| W4 camera range | PARTIAL | real range ~49–67° now stated — but the steepest/shallowest labels are inverted → W1 below |
| W5 sculpted fold-in path | **NOT FIXED** | §2 way-2 unchanged; no bbox-only mode exists → W5 below |
| W6 no durable artifact | LARGELY FIXED | gate 7 is the durable artifact; bbox-plausibility leg open (notes) |
| N1–N6 | all still present | carried below (N5 upgraded to warning — now sits under an explicit "pinned by" claim) |

**PR-body note:** the fix summary says "all 6 warnings folded" — W5 is verifiably not folded (W1–W4 only). Please keep fix-summary claims literal.

### Blockers (0)

None. 🎉

### Warnings (6)

1. **Tilt labels inverted** `docs/silhouette-spec.md:29` · `assets/blender/README.md:23` · `tools/gen_sprites.py:30-31,145-146` · `_pr_body.md` — campus ≈49° is called "steepest" and pucks ≈67° "shallowest"; under the elevation convention the docs themselves use (the old comment called ~66° "steep"), it's backwards. Numbers are right, adjectives are wrong — in 4 committed copies + the PR body, in the tables the user is sculpting against live. [blind + fix-audit]
2. **Order pin covers 2 of 3 copies** `tools/test_sprite_order.py:20-21` — the committed `sprites.json` `order` array (the copy `sprites_parse_boxes` actually binds bboxes by) is never compared to `files[]`. A consistent `SPRITE_ORDER`+`files[]` reorder without a Blender re-render (CI has none), or a hand-edited sidecar, passes gate 7 green and mis-crops at runtime — the B1 class. Verified consistent today. **Land the one-line extension before the fold-in re-render/T2 re-bless.** [edge + codebase + tests — agreement]
3. **Docstring documents output in the pre-fix (drifted) order** `tools/gen_sprites.py:25` — "…{house_0..3, host, dc, small_biz, campus, puck_1..3}.png" contradicts `SPRITE_ORDER` 60 lines below in the same file; delta-introduced by the fix commit's own docstring rewrite. [blind + fix-audit]
4. **Gate 7 has no negative-leg self-test** `tools/test_sprite_order.py:44-56` — repo convention is that drift gates prove they bite (`ci-local.sh:60` "W1 drift-rejection negative test"). It bites today (mutation-verified), but a comparator regression would pass CI unflagged. [tests]
5. **§2 way-2 still promises a fold-in path that doesn't exist** *(still present since round 1)* `docs/silhouette-spec.md:117-118` — "export the PNGs yourself; the minion folds them in (bbox regen)" — but `main()` unconditionally re-renders all 11 sprites, overwriting the user's exports. The user is live in Blender NOW; this is the path they hit. Needs `--bbox-only` mode or a reword. [fix-audit]
6. **README export list order contradicts the pin it cites** *(still present since round 1, was N5)* `assets/blender/README.md:30-33` — small_biz/campus listed before `puck_1..3` under a "pinned by sprites.odin" header. The user exports PNGs by this list. [blind]

### Notes (9)

1. Zero-alpha render writes a negative bbox `[256,256,-256,-256]` and exits 0 — assert positive dims in the generator (`gen_sprites.py:322-333`). [edge]
2. `add_outline` docstring says "flush at the fill's base"; flat fills hover 0.01 above it (only gable eaves are flush) (`gen_sprites.py:190-196`). [codebase]
3. KYLE §3 hue targets are optional-swap comments; the ≥15° blur-test hue-separation cure has no tracked merge-gate item — add it to the fold-in checklist (`gen_sprites.py:72-76`). [acceptance]
4. `/Users/moses/...` absolute paths committed as canonical references — relativize (`silhouette-spec.md:10,104`, `README.md:41`). *(since r1)* [blind + security]
5. `PUCK_TIER[ports]` direct index — KeyError mid-render with a half-overwritten sheet; `{4:1,8:2,16:3}` map still duplicated (`gen_sprites.py:300,346-347`). *(since r1)* [edge]
6. `mat_hex` slices wrong-length hexes silently — `len(h)==6` assert (`gen_sprites.py`). *(since r1)*
7. `.blend` policy lacks the auto-run caveat — one line ("open foreign .blend with auto-run disabled"). *(since r1)*
8. Camera pads live outside the SPEC table; frame-edge clipping is silent (`gen_sprites.py` main()/content_bbox). *(since r1)*
9. **Advisory test gate: PASS** — P0 order pin 100% + CI-enforced + verified biting; two P2 coverage warnings (negative leg, third order leg) don't breach thresholds. [tests]

### Reviewer agreement

- **W2 (third order leg)** — edge + codebase + tests independently, with matching evidence on the positional-bind mechanics. Highest-confidence finding in the round.
- **W1 (tilt labels)** — blind + the fix audit's independent elevation math.
- **/Users paths** — blind + security.

**Verdict:** READY TO MERGE

Stage-1 stands (PNGs intentionally unchanged; no runtime drift — diff touches docs + tooling only). The 6 warnings are doc/coverage items, none block the stage-1 contract; W2 + W4(negative-leg) should land with the fold-in pass before the T2 re-bless. Merge order unchanged: LAST, after scale-depth.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
