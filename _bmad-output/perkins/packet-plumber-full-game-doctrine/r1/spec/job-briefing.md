# Briefing — packet-plumber-full-game-doctrine (canon cascade: v2 IS the full game)

- **Job id:** `packet-plumber-full-game-doctrine`
- **Repo:** packet-plumber · **Base:** `v2` @ latest (Silas resolves the exact sha at
  dispatch) · **Slug:** `full-game-doctrine`
- **Model policy:** `kimi-coding/k3` (doctrine-level canon editing — reasoning tier).
  Any mega-minion you spawn launches with the same model — name it explicitly.
- **Skills policy:** `gds-gdd` (GDD/epics amendment intent) for the canon edits;
  **`lavish` is MANDATORY — this is a DOCS deliverable: present the full amendment
  set via lavish for the user's in-browser review BEFORE the PR opens** (iterate on
  annotations; PR only after an explicit approve).
- **Perkins:** `pr_review: 1` (canon surface). **Loop ruling (user, 2026-08-17):**
  rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-full-game-doctrine <url>` yourself.
- **Docs in scope (all under
  `/Users/moses/code/packet-plumber/_bmad-output/planning-artifacts/`):**
  `gdds/gdd-packet-plumber-2026-08-05/epics.md`, `.../gdd.md`,
  `.../decision-log.md`, `sprints/sprint-plan-v2.md`, `sprints/stories-v2.md`.
- **CI:** docs-only — keep any doc checks green; the local suite is unaffected.

## The ruling (user, 2026-08-17 — verbatim anchors)

> "We already had a prototype. We are already building production. We need to
> update what we are building now as the full game build. We need to update the
> sprint and docs. We are building fully. Prototype was already done."

**Doctrine:** the pre-v2 prototype WAS the prototype. v2 is built to production
discipline (deterministic core, command bus, golden-image harness, 9-gate local CI)
— **v2 IS the full-game build.** FORGE #7's intent (never ship prototype code as
product) is satisfied BY DESIGN, not by demolition: there is **no E11 rebuild**.
The fun-test gate REMAINS — as the greenlight for slice-8+ content scaling, not as
a rebuild trigger.

## Mission — the canon cascade (surgical amendment, not a rewrite)

1. **decision-log.md — record the ruling FIRST** (everything else cites it):
   date, the verbatim anchors, the rationale (v2's production discipline:
   deterministic core, command bus, golden harness, local CI; the pre-v2
   prototype fulfilled the prototype role), and the consequences below.
2. **epics.md:**
   - **E11 — rewrite**: "Production Rebuild (fresh codebase)" → SUPERSEDED by v2
     graduation (no rebuild, code is NOT discarded). E11's FEATURES live on as
     full-game backlog on this codebase: leaderboard backend, deterministic-seed
     run validation, the Blender-MCP asset pipeline, full custom art/audio +
     accessibility at production quality (fold into E10/slice-N framing).
   - Header scope line: "MVP = E1–E9 (fun-test gate); full game = E10 + E11" →
     reframe: E1–E9 build the full game's CORE + the fun-test gate; E10 content +
     E11-features continue ON THIS CODEBASE post-gate.
   - Build-staging section: remove/replace "Then rebuild from scratch" and
     "prototype = reference, not codebase" framings; keep the fun-test gate as
     the go/no-go for content scaling.
   - "MVP = juiced GRAYBOX" framing → production quality is the standard from
     here (the 7.x juice stories set the production look).
   - The closing line of "MVP build order" (rebuild reference) — amend.
3. **gdd.md** — the Development Epics summary (§611+) + any prototype/rebuild
   staging refs — align with the above; keep the traceability chain intact.
4. **sprint-plan-v2.md** — slice map (the MVP? column's meaning), executive
   summary, slice 8+ "(post-fun-gate)" framing, slice N "(E10) + production
   polish (E11)" framing → full-game-on-v2 language; the fun-test gate stays at
   the slice-7 exit as the content greenlight.
5. **stories-v2.md** — the slice-7 exit line ("MVP COMPLETE (E1–E9)") →
   "fun-test gate"; slice 8+/N coarse framing lines — align. Story cards
   themselves (Given/When/Then) are NOT touched.
6. **Provenance discipline:** strike nothing silently — superseded lines get a
   dated supersede note citing the decision-log entry (the established canon
   amendment pattern). NO code changes, NO catalog changes, NO story-card
   edits.

**Acceptance:**

1. Lavish review passed BEFORE the PR (the user approved the amendment set).
2. All five docs consistent: zero remaining "rebuild the full game fresh" /
   "prototype is reference, not codebase" framings (grep-verified; list any
   intentional historical references kept with supersede notes).
3. Decision-log entry complete + cited by every amended section.
4. PR body: the ruling, the per-doc diff summary, the grep proof.
5. `pr_review=1` Perkins loop until APPROVED (docs lens).

**Scope guard:** doctrine amendment ONLY. No resequencing of slices, no new
stories, no scope changes to in-flight jobs (5.5/7.2/7.1 ride as-is), no GDD
mechanic changes. The fun-test gate is REFRAMED, never removed.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: full-game-doctrine
base: v2
model: kimi-coding/k3
pr_review: 1
```
