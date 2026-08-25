## 🤖 Perkins automated review — round 2
**Job:** packet-plumber-v2-noc-player-toggle · **Reviewed sha:** 726cf7f · **Reviewers:** 7/7 completed
**Verification:** 5/6 findings confirmed against the code — 1 discarded as false-positive, 0 kept as [unverified]

### Fix audit (r1 fold)

| r1 finding | status | proof on this head |
|---|---|---|
| **B1 (blocker)** stuck-on panel | ✅ **FIXED** | `effect_settings_adjust` clears `overlay_on` when `noc_enabled` flips off (main.odin:966-969); pin `noc_disable_while_visible_dismisses_the_panel` drives the exact D→row-OFF sequence. Mutation re-run: deleting the dismissal fails the pin. |
| **W1** boot defaults unpinned | ✅ **FIXED** | `noc_boot_defaults` (main.odin:218-223) is the ONE proc — main() (:309) and the suite both drive it. Mutation re-run: flipping the default fails exactly 3 tests, reproducing the commit claim. |
| **W2** row count unpinned | ✅ **FIXED** | `test_settings_nav_reaches_noc_row` drives the real nav chain (open → 4 Downs → activate). Mutation re-run: `SETTINGS_ROW_COUNT→4` wraps to row 0 and fails (`got [0]`). |
| **W3** advisory gate CONCERNS | ✅ **PASS** | P0 100%, P1 ≥90% with the three pins landed. |
| r1 note: e2e drive in every build | ◼ still present | env-gate unchanged; security re-audited (fixed literal paths, no interpolation) — held as note per the r1 ruling |
| r1 note: presentation layer unpinned | ◼ still present | chip color + snapshot wiring remain unpinned (cosmetic) |

Perkins independently re-ran on this head: **11/11 ci-local native**, **48/48 goldens** (diff touches zero `goldens/` files), suites **core 236 / app 28×3 / render 52 / input 6 / audio 18 / harness 2** all green, e2e pixel-scan **0.0% OFF / 98.1% ON** (PR body says 0.0%/98.5% — within tolerance), all three claimed mutations reproduced and reverted.

### Blockers (0)
— none —

### Warnings (0)
— none —

### Notes (6)
1. **Advisory test gate: PASS** [tests] — all three r1 pins mutation-biting; only the two accepted r1 notes remain unpinned.
2. **README wording: "behind a runtime flag — OFF by default"** [blind] — README.md:28. The flag boots ON (default available); the *panel* is what's OFF. Intent clear from context ("zero extra pixels"); suggested reword: "the availability flag is ON by default; the panel itself is OFF until D".
3. **`value_chip_color` polarity** [blind] — settings_panel.odin:155-179. Every other row colors its *non-default* state; the NOC row colors ON (the default) and leaves OFF unhighlighted. Cosmetic.
4. **PR-body suite counts stale** [acceptance] — body says app 26 / input 5; post-fold reality is app 28 / input 6 (both green). Doc drift only.
5. **[still present since round 1]** PP_NOC_E2E drive compiles into every build behind the env var — documented decision, CWE-489 class; no new surface this round.
6. **[still present since round 1]** NOC-row chip color + snapshot wiring unpinned — cosmetic, consistent with the four pre-existing rows.

**Discarded as false-positive:** blind's blocker "unused range-loop variable `i` — Odin rejects this test file" — empirically disproven: `odin test app/input` compiles and runs green with this exact code (6/6, repeatedly, incl. ci-local gate 2). Odin does not reject an unused range-loop index.

### Reviewer agreement
- Fix-claim genuineness independently confirmed by architecture + codebase + tests lenses; security + edge audited their lenses clean; all three pins mutation-proven by Perkins on this head.
- e2e-drive note: r1 blind+security → r2 blind re-flag; held at note per the r1 ruling.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
