# Briefing — packet-plumber-v2-6.1-era-definition (slice 6: Email → Streaming)

- **Job id:** `packet-plumber-v2-6.1-era-definition`
- **Repo:** packet-plumber · **Base:** `v2` @ post-5.12 merge head (HELD — Silas
  resolves the exact sha at release) · **Slug:** `v2-6.1-era-definition`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-v2-5.12-aggregation-groups` merge close-out (slice 5B must
  land first — era demand signatures compose on the terminal-type data 5.11/5.12
  shipped). Record the hold on the row (`blocked_by`).
- **COORDINATE (Silas):** at release this job runs PARALLEL to
  `packet-plumber-wire-aesthetics` if that job is still in flight — era work is
  core+catalogs lane, wires are view lane; files disjoint. Link them
  `coordinate_with` and note the T2 handshake both ways (per the 4.3
  discipline): if you ever need the same file, STOP and flag in the PR instead
  of racing.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `gds-quick-dev` (core+data work); `project-context.md` for
  code conduct. No lavish gate (no user aesthetic verdict needed — the era
  presentation rides the existing 7.1 light-canvas canon).
- **Perkins:** `pr_review: 1` (canon-surface: catalogs, serialization, likely
  LOG_VERSION — the 2026-08-12 scope guard applies). **Loop ruling (user,
  2026-08-17):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-6.1-era-definition <url>` yourself.
- **CANON CONTEXT:** stories-v2 §Story 6.1 (read it first —
  `_bmad-output/planning-artifacts/sprints/stories-v2.md`); GDD E5.1; ODN-16
  (Era FSM S6), ODN-5 (integer-only catalogs, fail-fast), E14 (no mid-crisis
  demand spawn); the `[LATER]` seam reserved for this. The 5.11/5.12
  terminal-types + aggregation-groups data model is the substrate era demand
  signatures build on.
- **CI:** `tools/ci-local.sh` (10 gates incl. palcheck) is the merge ground
  truth.

## Mission — implement era definition (Email → Streaming data + era FSM advance)

**Goal (stories-v2 6.1, verbatim intent):** era data (Era 2→3: per-era packet
types, demand signature, infrastructure) loads from an `eras.json` catalog; the
era FSM advances the active era. When an era advance fires, the new era's
unlocks load (streaming becomes available, new demand signature) — catalog data
integer-only + fail-fast validated [ODN-5]; no mid-crisis demand spawn [E14].

**Deliverables:**

1. `eras.json` catalog: per-era packet types, demand signatures, infrastructure
   unlock table — integer-only, fail-fast validated at load (the [ODN-5]
   pattern from packet_types.json / pipe_tiers).
2. Era FSM (S6): the active-era state, the advance event, and the seam
   integration on the reserved `[LATER]` boundary — advance mechanics only
   (the advance CONDITIONS are story 6.2, out of scope here; wire the advance
   so 6.2 has a clear gate surface to compose on).
3. Demand-signature era switch: on advance, new-era demand spawns under the new
   signature; E14 holds — no mid-crisis spawn (an active crisis defers new
   demand until it clears, deterministic).
4. Golden: T1 of the era-advanced state; T1/replay determinism proven for the
   advance event. If LOG_VERSION bumps, cite the canon rule (serialization
   changes) in the PR.
5. **Canon fold:** mark §Story 6.1 `Status: implemented` in stories-v2.md
   (same-PR edit, the 7.4 pattern).

**Acceptance:**

1. GWT from stories-v2 6.1 demonstrably green (the Given/When/Then as tests or
   harness evidence, cited in the PR).
2. Edge contracts: E14 no-mid-crisis spawn tested; catalog validation
   fail-fast on a malformed fixture (negative test).
3. `tools/ci-local.sh` 10/10; T1 + replay byte-identical pre-advance;
   golden-advanced state pinned.
4. PR body: the eras.json schema, the FSM advance surface 6.2 composes on,
   citations (ODN-16, ODN-5, E14, stories-v2 6.1).

**Scope guard:** era DATA + FSM ADVANCE only. Advance conditions/gates = 6.2;
legacy decay/modernize = 6.3 — name them as follow-ups in the PR, don't build.
No view work (wires lane is parallel; presentation of the era switch rides
existing canon).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-6.1-era-definition
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
