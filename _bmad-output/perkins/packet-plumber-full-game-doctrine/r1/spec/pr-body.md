Full-game doctrine: v2 IS the full-game build — E11 rebuild superseded (canon cascade)

# Full-game doctrine: v2 IS the full-game build (canon cascade)

Docs-only canon amendment across the five planning docs, applying the user ruling of
2026-08-17. Lavish review **APPROVED 2026-08-17** (session `f21060ddf51c30f9`) before this
PR opened, per the docs-deliverable gate.

## The ruling (user, 2026-08-17 — verbatim anchors)

> "We already had a prototype. We are already building production. We need to update what
> we are building now as the full game build. We need to update the sprint and docs. We are
> building fully. Prototype was already done."

**Doctrine:** the pre-v2 prototype (PR #17) WAS the prototype. v2 is built to production
discipline (deterministic core, command bus, golden-image harness, 9-gate local CI) —
**v2 IS the full-game build.** FORGE #7's intent (never ship prototype code as product) is
satisfied **by design, not by demolition**: no prototype code was ever carried into v2, so
there is **no E11 rebuild**. The **fun-test gate REMAINS** at the slice-7 exit — reframed
as the greenlight for slice-8+ content scaling, never a rebuild trigger. Production
quality is the standard from here; the 7.x juice stories set the production look.

## Per-doc diff summary

- **decision-log.md** (+44) — new append-only entry `2026-08-17 — Full-game doctrine`:
  the ruling verbatim, the six-point doctrine, the consequences, and the explicit
  not-changed list. Every other amendment cites this entry.
- **epics.md** — header scope line reframed (E1–E9 = the full game's CORE + the fun-test
  gate; post-gate = E10 + carried E11 features ON THIS CODEBASE); traceability-matrix E11
  row superseded + MVP-column footnote; build-staging bullets ("juiced GRAYBOX" →
  production quality; "rebuild from scratch" → no-rebuild with the gate kept as the
  content go/no-go); E10 fold-line naming the carried E11 features; **E11 rewritten** as
  SUPERSEDED (original framing quoted for provenance; features listed as backlog; test
  contract reframed); MVP-build-order closing line amended.
- **gdd.md** — Project goal 1 reframed (the gate answers the fun question; the build under
  test is the full game's core); win/loss table row relabeled (`MVP prototype` →
  `MVP core (fun-test gate)`); art-direction + Asset Requirements staging refs (asset
  staging stays, the "prototype is reference, not codebase/shippable" rationale is
  superseded); Development Epics E11 row + MVP? footnote; forge-risk rows 1 & 5 carry
  dated supersede notes. Mechanics, numbers, traceability chain untouched.
- **sprint-plan-v2.md** — mission paragraph gains the doctrine rider; one-breath plan
  re-points slice N; slice-map rows 7 (`MVP done` → `fun-test gate`)/N + MVP? footnote;
  slice 7 goal + playable increment (production look; the gate runs); slice-N E11 bullet
  fully superseded (completes this plan's earlier "partially absorbed" reading); §6.4,
  decision 6, and OQ 3 (E11 shape — RESOLVED) aligned.
- **stories-v2.md** — notation line; slice-7 header + exit line (`MVP COMPLETE (E1–E9)` →
  `the FUN-TEST GATE`, the content greenlight); slice-N header + E11 bullet. **No story
  cards touched.** Hunks sit clear of the in-flight 5.5 (#59) and 7.2 (#60) status lines
  (nearest hunks: slice-7 header ~15 lines above 7.2's card; nothing near 5.5).

## Grep proof (acceptance #2)

| Framing | Remaining occurrences |
|---|---|
| "rebuild the full game fresh" | zero outside dated supersede notes + historical v2-charter facts |
| "prototype is reference, not codebase" | zero outside quoted-and-superseded text |
| "MVP COMPLETE" / "MVP done" / "MVP test" | zero |
| "juiced GRAYBOX" | one — inside the dated supersede note itself |
| "E10–E11" / "E10/E11" | one — a v1-section citation label (sprint-plan §6.4), supersession stated in the same item |

**Intentional historical references kept** (rationale in each case): sprint-plan-v2 title +
§1 mission "from scratch" (the doctrine's premise — v2 *was* the from-scratch build; rider
beside it); §5 harness "mined from the prototype reference" + frontmatter
`prototype_reference` (provenance; that discard already happened at the Odin pivot); gdd
risk-5 title "Prototype methodology" (the forge's proper noun; mitigation cell superseded);
`[ASSUMPTION: prototype tuning]` tags + Assumptions Index (a defined term for tuning
ballparks, not build staging); decision-log history (append-only — superseded forward by
the 2026-08-17 entry); epics.md E1.4 `[PROTO (PR #17)]` routing note (2026-08-10 pattern).

## Decisions & rationale

- **"MVP" retained as a term, redefined** (the full game's core up to the fun-test gate,
  never a throwaway) rather than renamed across five docs — the epic ids, story ids, and
  the fun-test definition are engine-agnostic and keep citing cleanly; both matrices carry
  a footnote pinning the new meaning.
- **E11 kept as a SUPERSEDED section** (with the original framing quoted) instead of
  deletion — the established canon-amendment pattern (strike nothing silently; banner +
  pointer, never silent removal).
- **E11's features folded into E10/slice-N framing as a paragraph, not new numbered
  stories** — the scope guard forbids new stories; slice-N remains coarse by design.
- **Asset staging kept** (placeholder during core slices; custom owned assets post-gate) —
  what died is the discard *rationale*, not the staging; the 7.x juice stories set the
  production look on this codebase.
- **`[ASSUMPTION: prototype tuning]` tags deliberately untouched** — a defined assumptions
  term; a terminology sweep is out of scope for a doctrine amendment.
- **Surgical hunks in stories-v2.md** — placed clear of the in-flight 5.5 (#59) / 7.2
  (#60) status lines so the sibling rebase relay auto-merges.
- Out of scope per the briefing: no slice resequencing, no mechanic changes, in-flight
  jobs (5.5/7.2/7.1) ride as-is, the fun-test gate is reframed never removed.

## Scope / CI

Docs-only: `_bmad-output/planning-artifacts/**`. No code, catalog, balance, or golden
changes; the 9-gate local CI is unaffected (no doc checks in the workflow).
