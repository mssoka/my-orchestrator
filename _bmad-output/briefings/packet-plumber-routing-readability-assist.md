# Briefing — packet-plumber-routing-readability-assist (Job B: readability package)

- **Job id:** `packet-plumber-routing-readability-assist`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `routing-readability-assist`
- **Prereq:** Job A (`packet-plumber-routing-bandwidth-cost`) MERGED — branch from post-A
  `origin/v2` (fresh fetch at dispatch).
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (player-facing gameplay surface — the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.

## Canon source (READ FIRST)

`/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md` — read the RECOMMENDED
SOLUTION (R2a/R3/T2) + the fun-factor analysis + Step 8 gameplay metrics (M6-M9). This
briefing is the condensed mission; the artifact is the canon.

## Mission (Job B — the readability package, app layer)

The capacity-cost routing (Job A) makes "flows prefer fat pipes" real. Job B makes it
**readable and satisfying** — the fun gate (user ruling 2026-08-13): players must be able
to predict routing by looking at the map; upgrades must produce visible, satisfying flow
shifts; ties must be explained. Perception, not mental arithmetic.

**Acceptance:**

1. **R2a — live cost-sum flow preview while drawing:** the draw ghost shows the path
   packets WILL take (per the cost-aware routing table) plus the best path's total cost
   readout — **ONE number or the delta**, never a candidate spreadsheet.
2. **R2a — assist graduation tiers:** full assist (sum + winning-path glow, DEFAULT for
   beginners) → partial (glow only) → off (pros). Settings toggle. Graduation nudge after
   N successful draws (N in `balance.json` — data-driven, ODN-5), opt-in, NEVER forced.
3. **R3 — post-draw route glow:** the current winning path lights up — the visible payoff
   of a tier upgrade (flow visibly shifts to the fat pipe).
4. **T2 — equal-cost tie cue:** when ECMP ties, BOTH tied paths are marked ("equal cost —
   split by hash") so a split never looks random.
5. **View-only, STRICT (ODN-12):** reads the routing table + tier costs; NEVER feeds sim
   state. No core changes. Determinism untouched by construction — **the harness T1/T2
   goldens MUST NOT shift; any shift = violation, STOP and flag.**

**Reference:** `docs/routing-explorer.html` — the existing flow-preview prototype; mine it
for the ghost/preview patterns, don't copy wholesale.

**Verify:** build green, harness green, goldens unchanged, assist toggle + graduation nudge
launchable, and the preview path CROSS-CHECKED against actual sim routing (a launchable
increment where the previewed path matches the simulated one).

**Scope guard:** NO core/sim changes; NO forecast flow-shift prediction (Job C owns R4);
minimal settings UI. This job owns `app/render` ghost/glow + the assist toggle; Job C runs
in PARALLEL and owns the forecast panel — if you touch a file it owns, flag to Silas.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: routing-readability-assist
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
