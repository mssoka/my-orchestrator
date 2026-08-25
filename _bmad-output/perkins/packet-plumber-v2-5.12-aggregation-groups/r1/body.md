## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-5.12-aggregation-groups · **Reviewed sha:** `035c733` · **Reviewers:** 7/7 completed
**Verification:** 14/14 findings confirmed against the code — 0 discarded as false-positive

**Diff note:** the PR diff is 46,484 lines (mostly the golden re-bless). Lenses reviewed the 1,284-line code chunk (core+data+demos+docs); the goldens were verified **mechanically** in the round worktree:

- **Local suite (independent run):** `tools/ci-local.sh --mac` → **10/10 gates green** (lint, 199 core tests incl. the 5 new group pins, app build, 34-demo harness + replay gate, palcheck, drift 240/240, assist cross-check, PP_DEBUG, stats replay-identity, input parity 24/24).
- **Fold partition exact:** `harness fold-check 17d3baf8c6e1df7f d1d2e53b7b1037ce` → **PASS** (era-0 tick-1 shift is the catalog fold alone). All **33 pre-existing .log.bin** byte-compared vs `v2`: diffs confined to bytes 17–24 (the catalog_hash field) — no command bytes moved, no LOG_VERSION bump needed. All **15 changed PNGs** match the claimed partition: 6 banner-copy frames (pixel-diff confined to rows 30–40 — the banner strip; map byte-identical), 7 growth-map frames, 2 new estate_surge frames.
- **estate_surge T2 golden vision-verified:** 3-campus estate cluster, red-outlined shared uplink, banner names the group uplink under the ×10 streaming surge.
- **Mutation checks (pins bite):** re-introducing the `/1000` truncation in `flow.odin` → `test_groups_demand_concentrates_on_estate` **FAILS** (800 == 800, attribution dead). Forcing drop-site bundle attribution off the uplink → `test_groups_surge_aggregation_at_shared_uplink` **FAILS**. Both reverted; worktree clean.
- **Adversarial fixes confirmed in tree:** proc-scope `defer if gview_built` (the block-scoped-defer UAF class) and the integer-exact **multiplication** (`w * group_pick_scale`) in `flow.odin` — plus the same proc-scope defer in `growth.odin`.
- **The estates ruling is honored:** bias coin per attempt (750‰, data-driven, fail-fast 1..999), biased candidate still faces the full E31 test, rejection-sampling unchanged, uplink never forced; NOT-100% pinned (`estate_seen` + `isolated_seen` on seed 9). The derived view is pure (union-find, seed-derived, never serialized).

### Blockers (0)
None.

### Warnings (4)
1. **Diagonal biased draws overshoot the group radius** [blind, edge, acceptance, codebase] — `core/growth.odin:561-568`. Diagonal dir × dist 4–5 = Euclidean 5.66/7.07 > `radius_tiles` 5, so ~1/3 of biased draws land outside the anchor's radius and may not join the derived cluster — the "candidate JOINS the estate" claim overstates. E31-safe and deterministic; the measured mix still pins. Fix: clamp diagonal dist to `floor(radius/√2)` (integer) or soften the claim.
2. **`growth_groups` parsed with `jint`, not `jint_strict`** [edge, security, codebase] — `core/catalog.odin:791-795`. Silent float truncation + i32 wrap at the data boundary; the 5.9 sibling (`cap_fraction_permille`) hardened this exact class. Shipped values are integers, so no live bug. Fix: `jint_strict` all five keys + decimal/wrap fail-fast rows.
3. **`estate_surge.dem` header quotes stale banner copy** [blind] — the quoted banner includes a trailing "— the surge is an aggregation event" the shipped `crises.json` string doesn't have. Fix: quote the shipped `preventive_redesign` verbatim.
4. **`max_members` cap branch unpinned** [tests] — `core/growth.odin:519`. Deleting the eligibility check fails no test; the ruling's 3–8 size band rests on an unverified branch. Fix: pin a full-estate fixture asserting cap exclusion / uniform-family fallback.

### Notes (5)
- Concentration control discards its spawn total (`_ = total_wo`) — assert `total_wo > 1000` so the attribution baseline has a volume floor. [blind]
- `radius_tiles` has no upper bound — an oversized radius silently merges the whole map into one "estate". [edge]
- The uniform-family placement draw is duplicated verbatim in two branches of `growth_plan_demand` — extract a helper so the E10 draw order can't drift. [architecture]
- Credit-starvation neutrality of the group weight is documented but unpinned (P3). [tests]
- **Advisory test gate: PASS** — P0 100%, P1 100%, overall ~95%. [tests]

### Reviewer agreement
- Diagonal-overshoot: 4 lenses (blind + edge + acceptance + codebase).
- `jint` vs `jint_strict`: 3 lenses (edge + security + codebase).

**Verdict:** READY TO MERGE

The hard blocker class is clean: the bias is soft and E31-respecting, the view is pure, the weight math and pins bite (mutation-verified), the surge names and sheds at the group uplink, and the re-bless partition is exact (fold-check PASS + byte-verified logs + pixel-partitioned PNGs). Warnings ≠ blockers — the four above are worth a follow-up sweep but none gates the merge.

_Address findings and push — I re-review automatically on the new sha._
