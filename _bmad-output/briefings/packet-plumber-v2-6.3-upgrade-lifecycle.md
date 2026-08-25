# Briefing — packet-plumber-v2-6.3-upgrade-lifecycle (slice 6: legacy decay)

- **Job id:** `packet-plumber-v2-6.3-upgrade-lifecycle`
- **Repo:** packet-plumber · **Base:** `v2` @ post-6.2 merge head (HELD — Silas
  resolves the exact sha at release) · **Slug:** `v2-6.3-upgrade-lifecycle`
- **HOLD (Silas):** do NOT dispatch on receipt. Release trigger = the
  `packet-plumber-v2-6.2-advance-trigger` merge close-out (decay composes on
  the landed advance + the legacy predicate 6.2 left as a seam). Record the
  hold on the row (`blocked_by`).
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `gds-quick-dev` (core+topology work); `project-context.md`
  for code conduct. No lavish gate.
- **Perkins:** `pr_review: 1` (gameplay-rule + topology canon surface — decay
  changes throughput semantics). **Loop ruling (user, 2026-08-17):** rounds run
  UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-6.3-upgrade-lifecycle <url>` yourself.
- **CANON CONTEXT:** stories-v2 §Story 6.3; GDD E5.3 + §M4 (metaphor boundary:
  Eras 1–4 literal, Era 6 abstracted); ODN-16 (Era FSM S6), Topology (S1); the
  landed 6.1 eras.json infrastructure table + 6.2 advance gate + legacy
  predicate seam (read those PRs first); 2.3 demolish (the demolish path this
  story composes with); 5.6 router tiers (the tier-up mechanic modernize
  builds on).
- **CI:** `tools/ci-local.sh` (10 gates incl. palcheck) is the merge ground
  truth.

## Mission — implement the upgrade lifecycle (legacy decay + modernize)

**Goal (stories-v2 6.3, verbatim intent):** pipes become legacy in later eras;
effective throughput decays; modernize (tier up) or demolish. Legacy decay is
MEASURABLE (effective throughput decays); modernizing or demolishing restores
full throughput; metaphor-boundary rules hold [GDD §M4].

**Deliverables:**

1. Legacy-decay model: on era advance, pipes left behind by the new era's
   infrastructure table become legacy; effective throughput decays by an
   integer-only, catalog-driven factor (the [ODN-5] pattern — decay data in
   eras.json or a sibling catalog, fail-fast validated). Decay is DETERMINISTIC
   and measurable — the sim's routing/drop behavior reflects reduced effective
   capacity, never a view-only illusion.
2. Modernize: tier-up on a legacy pipe (build on the 5.6 tier mechanic)
   restores full throughput; demolish (2.3 path) also clears the legacy state.
   Both paths observable + tested.
3. Fill the 6.2 predicate seam: the legacy-pipe predicate 6.2 stubbed now
   resolves against the real decay state (gate + lifecycle agree — add the
   cross-test).
4. Metaphor boundary [GDD §M4]: Eras 1–4 stay literal; if anything in this
   implementation would force Era 6 abstraction, FLAG it in the PR — don't
   invent Era 6 content.
5. Golden: T1 of decayed vs modernized throughput; T1/replay determinism.
6. **Canon fold:** mark §Story 6.3 `Status: implemented` in stories-v2.md
   (same-PR edit) + note the slice-6 exit condition is now met pending 6.1/6.2
   merges.

**Acceptance:**

1. GWT from stories-v2 6.3 demonstrably green; decay measurable, modernize +
   demolish restore paths tested, the 6.2-gate cross-test green.
2. `tools/ci-local.sh` 10/10; goldens pinned; byte-identity where no advance
   fired.
3. PR body: the decay model (factor source, determinism argument), the
   modernize flow, citations (GDD §M4, stories-v2 6.3, the 6.1/6.2 PRs).

**Scope guard:** decay + modernize ONLY, this era transition (Email→Streaming).
No multi-era ladders beyond what eras.json already carries, no Era 6 content,
no view work beyond existing canon surfaces.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-6.3-upgrade-lifecycle
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
