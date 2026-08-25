# Job B: the readability package — R2a live cost-sum preview + assist tiers, R3 post-draw glow, T2 tie cue

App-layer, **view-only** (ODN-12): the package reads the topology + flow + the
public pure `core.routing_rebuild` and never feeds sim state. **No core
changes.** Base `v2` @ `69fc2e5` (post-#37, Job A merged).

## What ships

- **R2a — live cost-sum flow preview while drawing.** While a valid pipe drag
  is snapped, the ghost's winning path lights up: a what-if routing table is
  computed on a scratch CLONE of the topology + the candidate pipe (the same
  pure rebuild the sim runs post-commit, so the previewed path is exactly the
  path packets WILL take), the FIRST live packet whose equal-cost DAG contains
  the candidate edge and reaches its dst wins, and the full DAG glows. ONE
  number ("route N" — the path total, shared by every DAG path by the ECMP
  invariant) draws near the cursor. Never a candidate spreadsheet.
- **R2a — assist graduation tiers.** Full (glow + number, DEFAULT for
  beginners) → glow-only → off (pros), cycled with **T**; the tier persists
  across in-session restarts. A graduation nudge fires ONCE after N successful
  draws (`data/assist.json` `graduation_n`, default 8) as a HUD line — opt-in,
  never forced; any T press dismisses it.
- **R3 — post-draw route glow.** The committed DAG glows for `glow_ticks`
  (default 120 = 6 s at 20 Hz) — the visible payoff of a tier upgrade. The
  committed DAG lives in its OWN buffer (copied at commit) so a cancelled drag
  can never corrupt the running glow.
- **T2 — equal-cost tie cue.** At an ECMP split on the previewed DAG, BOTH
  paths glow and the split node is ringed + captioned "equal cost - split by
  hash" (ASCII — gate 6). A split never looks random.
- **Cross-check (the launchable increment).** New `harness preview-check`
  verb + CI step: 7 scenarios drive the PRODUCTION preview helper against the
  real sim and prove the preview DAG edge set + cost + split nodes equal the
  sim's rebuilt routing table, and the packet's actual hash-picked path rides
  the previewed DAG. Negative control verified locally (corrupting the preview
  cost → 3 reds).

## Verification

- `tools/lint.sh` — all gates green (ASCII gate 6 included)
- `odin test core` — 126/126, unchanged
- `tools/harness.sh run` — 16/16 demos green (T1 + T2 + replay)
- `tools/harness.sh preview-check` — 7/7 scenarios green
- `odin build app -out:app.bin` — links
- `shasum -a 256 goldens/*.t1 goldens/*.log.bin` — **byte-identical to the
  pre-change snapshot** (the acceptance's STRICT golden clause)

## Decisions & rationale

- **Assist config lives in `data/assist.json`, NOT balance.json** (deviation
  from the briefing's literal "N in balance.json", flagged for the human).
  `cat.hash` folds EVERY balance.json byte, so any field addition there
  re-blesses all blessed goldens — a direct violation of acceptance 5
  (STRICT: any golden shift = violation). `assist.json` follows the
  palette.json pattern: cosmetic-class, app-loaded, never handed to
  `catalogs_load`, never hashed. Precedent: `PLACEMENT_MIN_SEP_TILES` in
  core/topology.odin carries the same comment. When the balance catalog next
  legitimately re-blesses, this block can move there.
- **Preview semantics: "first affected packet".** The preview shows the full
  equal-cost DAG from the first live packet (spawn order) whose path contains
  the candidate edge and reaches its dst. Waiting packets (the fixture loop),
  arrival-window packets at junctions, and the upgrade shift are all covered;
  a draw that changes no packet's path (e.g. a parallel-pipe routing no-op)
  shows no glow — honest, never misleading. Future-demand forecasting is
  [LATER] (Job C's territory).
- **Two preview buffers.** The live drag DAG and the committed R3 glow DAG
  are separate (the glow is deep-copied at commit) — a cancelled drag can
  never render its never-committed path over the running glow (review finding).
- **R3 glow is gated on assist != Off.** Off = no routing visuals at all, a
  clean "pros opted out" contract (the fun-gate tiers are about the assist,
  and R3 reuses its visual language).
- **Glow invalidation is gen-coarse.** Any topology mutation (including a QoS
  emphasis edit, which bumps gen without changing routing) drops an early
  glow — conservative direction (glow off, never stale), accepted.
- **Per-frame temp-arena growth during drags.** The what-if rebuild allocates
  ~1 KB/frame of `core.routing_rebuild` scratch in the app's temp arena (the
  app never free_all's — a pre-existing pattern the HUD strings already
  follow). Bounded per drag; a future arena pass (ODN-18) owns this.
- **No app-package unit tests.** The assist glue (tier cycle, nudge latch) is
  thin + build-verified; the pinned gate is the preview==sim cross-check, and
  the app package isn't in the CI test matrix (raylib link).
- **Spec/UX amendment:** Off mode keeps the assist-mode indicator + the draw
  cost readout (the toggle's discoverability) — spec I/O matrix amended to
  match.

## Files changed

- `app/render/assist.odin` (new) — the readability package: config load, what-if preview, DAG walk, glow/tie/render
- `app/main.odin` — assist state + T toggle + nudge + wiring + HUD
- `app/render/palette.odin` + `data/palette.json` — route_glow/route_tie colors (additive only)
- `data/assist.json` (new) — cosmetic-class assist config (not hashed)
- `harness/assist_check.odin` (new) + `harness/main.odin` — the `preview-check` verb (7 scenarios)
- `.github/workflows/ci.yml` — the preview-check CI gate
- `_bmad-output/implementation-artifacts/spec-routing-readability-assist.md` — the story spec (done)

Job C (forecast shift) runs in parallel and owns `app/render/forecast.odin` —
untouched. `app/main.odin` is touched by both jobs (disjoint regions;
sequential merge ready-first per the dispatch plan). No goldens changed.

