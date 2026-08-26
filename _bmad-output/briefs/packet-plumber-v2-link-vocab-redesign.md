# Briefing — packet-plumber-v2-link-vocab-redesign (design exploration — NO production code)

Skill to execute: **bmad-quick-dev** (design-exploration mode) + **lavish**
(the deliverable IS the lavish page). Briefing is self-contained if the
skill is absent.

## USER DIRECTION (2026-08-26, re-opening the recorded revisit trigger)

"links are SINGLE solid colors, no lanes (queue state moves to an
ingress/egress read on the router...)"

Re-framed per the 08-23 memlog trigger — READ the memlog FIRST:
`_bmad-output/planning-artifacts/architecture/architecture-egress-qos-2026-08-23/.memlog.md`
(the egress migration was withdrawn; its RENDER premise returns now).

## The boundary (state it on the lavish page verbatim)

- **SIM UNTOUCHED** — ODN-3, per-(bundle,lane) queues, FORGE #4: all stand
  (the 08-23 withdrawal holds). This is the [LOOK] layer ONLY. If the ruling
  gate wants the sim migration too, that ESCALATES as its own architecture
  job — never silently.
- Render-side: links stop painting 3 lane strokes; queue/class state moves
  to router surfaces.

## Context — what the link currently encodes (inventory before you cut)

- `app/render/view.odin:698-760` — the spatial-lane canon (2e3acab): three
  per-class strokes alongside each other, lateral packet offsets keyed to
  lane, fiber core under strokes, casing/under-stroke idiom (:854, :935).
- Congestion telegraph (route_glow / bundle_congestion_level :811), tie
  marks (route_tie), drop marks, crisis surfaces — the overlay vocabulary
  that must survive ANY restyle.
- Sibling intake (parallel, in flight): `look-node-legibility-diag` — node
  contrast measurements. Hypothesis to TEST, not assume: lane stripes are
  the dominant visual noise swamping nodes. Cross-reference its numbers
  when they land; your proposals should co-rule at ONE user gate.

## Task: the new link + router vocabulary, as a user-ruled bake-off

1. **Archaeology + encoding inventory.** Enumerate EVERY state the current
   link paint carries (class mix, allocation, congestion, crisis, tie,
   drops, ownership) and where each GOES under the new model. An
   what-carries-what table is a required deliverable.
2. **Single-color link language — 2-3 directions**, each mocked on REAL
   captures (movie-mode craft per field notes; harness via tools/harness.sh
   with ODN_ROOT=the rlsw shadow). Decide and show: what the solid color
   encodes (neutral fiber + state overlay? utilization ramp? class mix?),
   how PACKETS render on a single-color link (single-file center line?
   lateral offsets keyed to class WITHOUT stripes?), what happens to the
   lane-visual on focus zoom.
3. **Router ingress/egress queue read.** The queue state surface at the
   router: per-port depth marks (4-16 ports — solve the density: at-rest
   aggregate vs per-port on focus?), the aggregate per-class read, and the
   NOC rail relabel option (memlog Q6). Deterministic, table-driven, no
   transcendentals (§10.4), reduced-motion aware — the standing render
   contracts all apply to your proposals.
4. **Fold finding D (shape-vocab, era-gated):** the same gate rules the 7
   unshaped packet classes — propose affordance-led shapes riding the same
   language (one [LOOK] decision, not two).
5. **CVD check** every proposed palette pair (palcheck oracle discipline;
   comment-stripped palette copy for the derive script).

## Deliverable

- **Lavish page**: current-state captures vs each direction (side-by-side
  strips), the encoding table, the router-read mockups, the finding-D
  shapes, the ruling checklist (one decision per row), the sim boundary
  statement. USER RULES in the browser.
- Spec-ready encoding table + ruling record under
  `_bmad-output/implementation-artifacts/link-vocab-redesign/` (preserve
  BEFORE any sweep).

## Ledger / reporting

- Row: `packet-plumber-v2-link-vocab-redesign`. No PR. Completion signal:
  `ledger note` + `herdr notification show
  "packet-plumber-v2-link-vocab-redesign" --body "<lavish url>"` (no-PR
  doctrine — verify `shown:true`).
- After the ruling: implementation heists serialize behind crisis-duck
  (shared render surface), pr_review=1, goldens re-blessed deliberately per
  direction.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider), `--thinking max`.
- KYLE mega-minion (if pixel evidence needed): `zai-coding-cn/glm-4.6v`
  pinned, probe first; down = report vision-unavailable, ship numeric
  measurements only.

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: link-vocab-redesign
- base: v2 (head 0b2aeb9 — READ-ONLY: captures + mocks only, touch nothing)
- branch: NONE (read-only exploration)
- model: zai-coding-cn/glm-5.3
- pr_review: 0 (no code; the implementation heists that follow carry 1)
