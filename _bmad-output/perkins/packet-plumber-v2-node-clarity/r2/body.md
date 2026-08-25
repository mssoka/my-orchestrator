## 🤖 Perkins automated review — round 2 (rebase-delta fix-audit)

**Job:** packet-plumber-v2-node-clarity · **Reviewed sha:** `108a4e3` · **Reviewers:** 7/7 completed
**Verification:** 22/23 findings confirmed against the code — 1 discarded as false-positive

### Fix audit (r1 → r2)

Of round 1's 17 findings (0 blockers / 5 warnings / 12 notes):

- **Fixed (1):** the `palette.json` `_comment` conflict with #77 — the rebase resolution keeps **both** PRs' notes on one line (verified in `data/palette.json`).
- **Obsolete (1):** the "palcheck LED pin will break when #77's `router_led` merges" warning — premise verified **false**: `p.router_led` is read only on the fallback primitive path (`view.odin:1006/1019/1032`, all after the `sprites.ok` early return); the sprite path's LEDs are baked and wash under the steel tier wash (`LED_GREEN {77,137,113}` formula-verified). Pin survives — no wave re-pin needed.
- **Still present (15):** carried below with markers — the r1 warnings remain the only warnings (plus one new one), none folded by the rebase.

### Rebase-delta verification (the r2 questions — all confirmed)

- **Rebase clean:** `_comment` keeps both PRs' content; token additions are additions-only; zero token-key collisions (#77 owns `router_led`/`pipe_*`/`packet_*`/`lane_*` — values untouched by this diff); the r1→r2 code delta on the PR's own files is only #77's rebase context interleaving in `palette.odin`/`palette_polish_test.odin` — the node-clarity bytes are identical to the r1-approved ones.
- **Combined-palette re-bless sound:** zero `.t1`/`.log.bin` hunks in the diff (T1/spine byte-identity); blur gate re-run by the reviewer **GREEN and matching the body exactly** — min pair 22.6° (residential↔campus), sat band 0.289, all 10 pairs ≥ 15° (#77's vivid pipes did **not** shift the σ6 node samples); `palcheck` re-run locally **46/46 PASS** on the merged palette; `odin test app/render` 15/15 (shipped-token pins + token-level hue separation green post-rebase).
- **Not re-litigated (user rulings):** hue-family/chips/tier-marker direction, D2/D3 tuned anchors, the deliberate 45-demo T2 re-bless, D1/D5.

### Blockers (0)

None.

### Warnings (5)

1. **[still present since r1 — strengthened] Tier tokens basic/high excluded from both separation instruments; drawn basic puck lands 0.7° from the host family.** The gate samples only `router_mid`; the token anchors array covers 5 of 7 new tokens. Reviewer-reproduced on `goldens/router_tiers/02500ms.png` at σ6: basic 211.0° vs host 210.3° (token level 7.0°). The audit's router↔host failure class persists for the *default* tier, invisible to both instruments; basic↔mid/high separate fine (30°) and ring+size+LEDs carry the tier read per approved D4. → sample basic/high in the gate + anchors, or pin a documented basic exemption.
2. **[still present since r1] The blur gate — both acceptance criteria — is wired into no automated suite.** `ci-local.sh`'s 10 gates (mirrored step-for-step into CI per its own header rule) never invoke `blur_gate.py`; the sat band is 0.011 under the bar and the wave-final palette reconciliation will touch tokens again. The token-level test can't catch the drawn failure mode (the briefing's own anchors pass token-level at 25° yet blur to ~13° — that's what D2 documents). → add an 11th gate.
3. **[still present since r1] `blur_gate.py` setup errors exit 1 ("gate red") via traceback, violating the documented exit-2 contract.** Unwrapped `getpixel`/`open`/`float`; valueless `--sigma/--out` silently dropped. A wrong-size image or changed fit measures nothing while looking like a measured failure. → try/except + `sys.exit(2)` + size assert.
4. **[still present since r1] Advisory test gate: CONCERNS.** P0 100% (gate reproduced green, T1s untouched, rebase additive-clean), P1 ~80% (drawn separation + sat band manual-only), overall ≈80%.
5. **[NEW this round] Rect family wash tints canvas at peaked/towered silhouettes.** Pixel-verified on the terminal-types golden: 30 px of the exact terracotta-over-canvas composite (211,118,113) form a 3-row squared band above the house's gable — tension with the body's "silhouette survives" claim. Mechanical pixel fact confirmed; **aesthetic severity deferred to the k3 re-check** (non-k3 vision caveat). Pre-existing r1-era behavior, not a rebase regression.

### Notes (16)

Carried from r1 (unchanged code): unused `v` param in the wash procs · duplicated idx/target at the wash sites (draw_router) · `.pyc` deletion undocumented in Files · LED pin floor halved >10→>5 without a stated count · body's "4% inset" vs the disc's 6% · `--sigma/--out` silent-drop · `draw_type_chip` missing the `fam.a==0` guard · "reuse tray icons" wording overstated · `blur_gate.py` Python-mirror of the view fit · wash+chip epilogue ×3 in the fallback branches · D5 chip-skip has no asserting pin.

New this round: SPAWNS comment says "six spawns" over seven entries (the table matches the demo) · `import math` unused + `worst` assigned-never-read · `blur_gate.py` committed 100644 despite shebang + direct-invocation usage line · `router_tier_family` is a third copy of the port→tier predicate (`sprite_index_puck`, `router_tier_scale`) — a future 12-port type desyncs fallback tier draws · the no-sprites fallback path gained wash/chip/ring draws no test executes (compile-checked only).

### Reviewer agreement

Five independent lenses (blind, edge, codebase, tests, + r1's acceptance/tests carries) converged on the tier basic/high exclusion — the strongest signal in the set, now with drawn-level evidence. Four converged on the un-wired blur gate.

**Verdict: READY TO MERGE**

The rebase is clean, every r2 claim verified mechanically (blur numbers, palcheck 46/46, T1 byte-identity, LED-pin survival), and zero blockers — the warnings are durability gaps (wire the gate into CI, widen the token anchors) plus one k3-deferred visual check, none of which block this merge.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
