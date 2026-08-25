# Briefing — packet-plumber-v2-4.1-warning-forecast (warning signs + forecast)

- **Job id:** `packet-plumber-v2-4.1-warning-forecast`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-4.1-warning-forecast`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (current: slice 3 complete — placement, QoS, serialize/drops, SLA all in;
  LOG_VERSION 3). Rebase onto origin/v2 if it moves mid-work; clean-rebase hygiene (no
  leftover conflict markers — `git diff --check` before force-with-lease).

## Mission (story 4.1 — the fun loop's telegraph, slice-4 opener)

Implement **Story 4.1: Warning signs + forecast** from
`_bmad-output/planning-artifacts/sprints/stories-v2.md` (line ~331) — full spec there.
Read the GDD slice-4/late-game sections (warning-sign lead times `[FORGE #3]` fair +
predictable), art-direction §6.1 (node health visual: 🟢/🟡/🔴 glow + ring pulse + icon,
triple-redundant — color never sole encoder), and the architecture's strain/forecast notes.

**Acceptance (condensed — stories-v2 is canonical):**

1. **Strain metrics** — utilization vs throughput from Topology + Flow, feeding the warning
   system.
2. **Warning signs** — 🟡/🔴 node states + pipe pressure + demand forecast, **all with lead
   times** `[FORGE #3]`. Node health transitions fire on defined thresholds; a 🔴 node is
   ALWAYS traceable to a measured strain (icon + shape + outline — never color alone).
3. **Forecast "weather report" panel** — names incoming SetPieces with a countdown (the P3
   fairness surface). The forecast READS the SetPiece schedule; it does NOT fire anything
   (that's 4.2).
4. **Scope guard:** warnings + forecast + strain telegraph ONLY. NO crisis firing (4.2
   Surge/Crisis Engine), NO health-meter win/lose (4.3), NO new player commands (LOG_VERSION
   stays 3 unless a command is truly required — flag first). The surge fires in 4.2; 4.1
   only ever *names* it.
5. **Golden:** T1 + T2 of the forecast + warning state (bless deliberately with proof;
   existing goldens must not shift — if one does, STOP and flag).
6. **Launchable increment:** run the app → see the forecast + strain telegraph *before*
   trouble (a node straining shows 🟡 with lead time, then 🔴; the forecast panel names the
   upcoming SetPiece with a countdown).

**Verify:** `odin test` suites green (core/demos/drift/lint), threshold/lead-time tests,
goldens blessed with proof, launchable increment in the PR body.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-4.1-warning-forecast
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
