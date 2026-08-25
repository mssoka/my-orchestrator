# Briefing — packet-plumber-v2-6.2-advance-trigger (slice 6: the era gate)

- **Job id:** `packet-plumber-v2-6.2-advance-trigger`
- **Repo:** packet-plumber · **Base:** `v2` @ post-6.1 merge head (HELD — Silas
  resolves the exact sha at release) · **Slug:** `v2-6.2-advance-trigger`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-v2-6.1-era-definition` merge close-out (the advance gate
  composes on 6.1's landed FSM + catalogs). Record the hold on the row
  (`blocked_by`).
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `gds-quick-dev` (core logic work); `project-context.md`
  for code conduct. No lavish gate.
- **Perkins:** `pr_review: 1` (gameplay-rule canon surface — advance semantics
  change win conditions). **Loop ruling (user, 2026-08-17):** rounds run UNTIL
  APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-6.2-advance-trigger <url>` yourself.
- **CANON CONTEXT:** stories-v2 §Story 6.2; GDD E5.2; E15 (advance
  blocked on crisis); the landed 6.1 era FSM (read its PR + eras.json first —
  the gate composes on its advance surface); 3.4 per-class SLA (the ≥95%
  measure builds on the SLA system); 4.2 crisis engine (the active-crisis
  signal).
- **CI:** `tools/ci-local.sh` (10 gates incl. palcheck) is the merge ground
  truth.

## Mission — implement the era advance trigger (the modernization gate)

**Goal (stories-v2 6.2, verbatim intent):** advance requires sustaining
SLA ≥ 95% across active classes for the milestone window AND modernizing all
in-service legacy pipes AND no active crisis. Advance fires only when all
three hold; an active crisis BLOCKS advance [E15]; unmodernized legacy pipes
block advance.

**Deliverables:**

1. The advance gate: three conditions evaluated on the milestone window —
   sustained per-class SLA ≥ 95% (build on the 3.4 SLA metrics), all in-service
   legacy pipes modernized (the legacy state 6.3 will own — until 6.3 lands,
   define the legacy-pipe predicate against 6.1's era infrastructure table and
   document the seam), no active crisis (the 4.2 signal).
2. Advance fire/block semantics: E15 — an active crisis blocks; conditions
   re-evaluate deterministically when the crisis clears. Both the fire path
   and each block path are observable (the 6.1 advance surface).
3. Golden: T1 of the advance (conditions met → fires); T1 of each block
   branch; T1/replay determinism holds.
4. **Canon fold:** mark §Story 6.2 `Status: implemented` in stories-v2.md
   (same-PR edit).

**Acceptance:**

1. GWT from stories-v2 6.2 demonstrably green; all three conditions + the
   E15 crisis block tested (fire path + every block path).
2. `tools/ci-local.sh` 10/10; goldens pinned; byte-identity proven where the
   sim is un-advanced.
3. PR body: the gate formula (window, SLA measure, legacy predicate), the
   6.3 seam for the legacy-pipe predicate, citations (E15, 3.4, 4.2,
   stories-v2 6.2).

**Scope guard:** the advance CONDITIONS only. Legacy decay/modernize mechanics
= 6.3 (next job on the belt) — leave the predicate seam, don't build decay.
No view work; era advance presentation rides 6.1's existing canon.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-6.2-advance-trigger
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
