# Story 7.5 — Wire aesthetics: routing + junction shaping shipped as routing-only infrastructure

## What ships

The network's drawn-wire layer gains a complete, deterministic, presentation-only routing + junction-shaping
machinery — shipped **OFF by default** per the user's gate verdict. The shipped render is the **pre-7.5 straight
look, byte-for-byte** (T2 goldens untouched — no re-bless needed; the harness run proves it).

**LAVISH GATE VERDICT (2026-08-19, recorded verbatim):**

- Round 1: *"straight looks better for a network topology"* (the detour look rejected).
- Round 2: **"Ship pure straight (routing OFF, anchors OFF) — Story 7.5 becomes routing-only infrastructure."**

The gate was presented side-by-side routed-vs-straight on a real busy map (the Story 7.1 dense core + the 5.12
estates) with junction close-ups (anchor spread + ribbon fan), iterated until the explicit approve above.

## What the machinery does (one flag flip away)

- **`app/render/wire_path.odin`** (NEW, pure): a deterministic drawn polyline per bundle that (1) detours around
  crossings with other pipes (preferring to SLIDE alongside), node/terminal sprites, and the map edge; (2) attaches
  at router puck-rim anchors allocated evenly around the disc (n pipes → n anchors; n=4 → 90° ✕/＋); (3) renders
  parallel-pipe bundles as ONE ribbon that fans open at each end into the member anchors; (4) degrades to STRAIGHT
  whenever a detour would be longer/uglier than the crossing.
- **Cost immunity (the load-bearing guard):** pipe cost = `pipe_span × cost_per_tile` on the LOGICAL straight
  A→B geometry — the drawn detour never changes what the player pays. T1 state-hashes + replay logs are
  byte-identical `[E10]`; the view never perturbs the sim `[ODN-1]`.
- **Determinism:** same map → same paths; no RNG, no seed, order-free obstacle set (other bundles' straight
  logical segments), no transcendentals (CIRCLE16 rotation only — §10.4). Proven twice: the 6-test pin suite +
  a pixel-level determinism check (two renders of the same frame, byte-identical hashes).
- **Degradation thresholds** (named render constants, never catalog-poisoned): `WIRE_DETOUR_MAX_LEN_RATIO`
  (1.5× — a longer detour falls back to straight), `WIRE_DETOUR_MAX_BENDS` (3), `WIRE_SLIDE_GUTTER` (6 px),
  `WIRE_SPRITE_MARGIN` (3 px), `WIRE_STUB_TILES` (3 tiles — short terminal drops keep their crossing: the right
  look for a stub).
- **Two View flags:** `route_wires` (detours) + `wire_anchors` (rim anchors + ribbon fan), both OFF in the
  shipped game. The legacy draw branches (both flags off) are byte-for-byte the pre-7.5 render.

## Files changed

| File | Change |
|---|---|
| `app/render/wire_path.odin` (NEW) | the pure path module: anchor allocation, obstacle scan, bend insertion, fan apexes, arc-length sampling, path-band draw helpers |
| `app/render/wire_path_test.odin` (NEW) | 6 pins: cost immunity (logical span, negative-controlled), determinism, degradation bounds, anchor even-spread (n=4 → 90°), ribbon fan apex |
| `app/render/view.odin` | `route_wires`/`wire_anchors` flags; draw_world computes paths only when a variant is active; draw_bundles/draw_packets/draw_selection legacy-branch-preserved + variant branches |
| `app/render/crisis.odin` | crisis outline follows the drawn path in the variants; pre-7.5 inline branch preserved |
| `app/render/assist.odin` | committed-bundle glow follows the drawn path in the variants; pre-7.5 inline branch preserved |
| `harness/wire_preview.odin` (NEW) + `harness/main.odin` | `harness wire-preview` — the gate tool (routed / anchors / straight frames + close-ups on juice + estate scenes) |
| `harness/goldens.odin` + `app/main.odin` | shipped flags OFF + the verdict comment |
| `_bmad-output/.../stories-v2.md` | §Story 7.5 card |
| `_bmad-output/.../decision-log.md` | decision-log note (user ruling + gate verdict) |
| `_bmad-output/implementation-artifacts/spec-7-5-wire-aesthetics.md` (NEW) | the story spec |

## Verification

- `tools/ci-local.sh --mac` — **10/10 green** (purity, core tests, app build, golden harness incl. T1 + T2 +
  replay, palcheck, drift-check, preview-check, PP_DEBUG builds, stats replay-identity, input parity).
- `odin test app/render` — 6/6 green; the cost-immunity pin was **negative-controlled** (a phantom +3 detour
  span flips it red: `got 390 want 300`), then restored green.
- **Goldens:** ZERO changes (the shipped flags-off render is byte-identical to the blessed T2 frames — the
  harness run passes all 34 demos on the committed goldens; no re-bless was performed or needed). T1 manifests
  + replay logs byte-identical by construction (view-only, ODN-1).
- **Determinism:** pixel-level proof — the routed gate frame rendered twice produces identical SHA-256 hashes.

## Decisions & rationale

- **Ship the mechanism OFF** — the user's gate verdict is explicit and load-bearing; the machinery is fully
  tested + cost-immune so a future aesthetic ruling is a one-flag change, not a rebuild. The alternative
  (shipping the detour look despite the verdict) was rejected at the gate.
- **No T2 re-bless** — the briefing's re-bless requirement was conditioned on the shipped look changing. The
  verdict kept the shipped look identical, so re-blessing would have been an unjustified golden churn. The
  harness run on the committed goldens is the proof.
- **Routable obstacles = other bundles' straight logical segments** (not their detoured paths) — keeps the path
  a pure function of topology (order-free, deterministic), per the briefing's "deterministic from topology".
- **Thresholds are render-side constants, not catalog data** — catalog edits are golden-poisoned (field-notes
  trap); render constants follow the PULSE16/ROUTER_TIER_SCALE precedent.
- **Terrain-aware routing (rivers) is a named follow-up, FLAG not build** — per the briefing's scope guard.
- **T2 handshake (4.3):** this job is view-lane (app/render + harness + goldens). The in-flight slice-6 era work
  (core+catalogs) touches disjoint files; if both jobs' branches merge, the goldens stay compatible (this job
  changed none).

## Citation

- 7.1 gate verdict (tier-band pipes, two-tone roofs, flat-MM) — `_bmad-output/planning-artifacts/art-renders/look-book-v1.md`
- Look-book D9 map (background-maps job) — decision-log 2026-08-18 + story 7.4 card
- 5.12 estate placement — decision-log + story 5.12 card
- User ruling 2026-08-17 ("want it") + the gate verdict 2026-08-19 (verbatim above) — decision-log 2026-08-19 entry

