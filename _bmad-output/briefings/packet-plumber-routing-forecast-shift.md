# Briefing — packet-plumber-routing-forecast-shift (Job C: R4 forecast flow-shift prediction)

- **Job id:** `packet-plumber-routing-forecast-shift`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `routing-forecast-shift`
- **Prereq:** Job A (`packet-plumber-routing-bandwidth-cost`) MERGED — branch from post-A
  `origin/v2` (fresh fetch at dispatch). Job B (`routing-readability-assist`) runs in
  PARALLEL — coordinate file ownership with Silas.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (player-facing gameplay surface — the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.

## Canon source (READ FIRST)

`/Users/moses/code/_bmad-output/problem-solution-2026-08-13.md` — read the RECOMMENDED
SOLUTION (R4) + the fun-factor analysis (thundering-herd trap) + Step 8 (M7/M8 metrics).
This briefing is the condensed mission; the artifact is the canon.

## Mission (Job C — R4 forecast flow-shift prediction)

With capacity-cost routing, a tier upgrade is a magnet: "flows prefer fat pipes" means an
upgrade can attract EVERYTHING — the thundering herd. R4 defuses the trap by predicting it:
the forecast panel (4.1 built the panel + strain telegraph) must show the player what an
upgrade WILL cause — "this upgrade attracts everything" — BEFORE they commit.

**Acceptance:**

1. **Predictive helper (core, PURE):** given the current Topology + a hypothetical tier
   change on one pipe, compute the predicted post-upgrade routing (re-run A's Dijkstra
   against the hypothetical topology) and the predicted flow shift. PURE function — no
   state mutation, no rng, integer-only, array-only (ODN-9/10). It is a look, never a write.
2. **Forecast panel integration:** when the player considers upgrading a pipe's tier, the
   panel shows the predicted reroute ("traffic will reroute to X"; "equal-cost — flow will
   split") before commitment.
3. **Prediction accuracy, property-pinned:** apply the upgrade FOR REAL in a demo and
   assert prediction == actual post-upgrade behavior (the helper's output matches the
   sim's outcome — this is the honest-prediction pin, the determinism twin of `expect hash
   stable`).
4. **Golden discipline:** NEW golden files only; existing goldens MUST NOT shift (any
   shift = violation, STOP and flag).

**Verify:** helper unit tests + the property pin green, build green, harness green, goldens
unchanged except new files, launchable increment (preview the upgrade → commit it → watch
the prediction come true).

**Scope guard:** prediction ONLY — no auto-routing, no new player commands, LOG_VERSION
stays unless truly required (flag first). NOT Job B's assist/glow/tie-cue (Job B owns
`app/render` ghost/glow + assist toggle; this job owns the forecast panel + the predictive
helper). Per-class routing preferences remain scope-guarded out (full-game idea).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: routing-forecast-shift
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
