# Briefing — packet-plumber-v2-4.3-network-health (Network Health + win/lose/retry)

- **Job id:** `packet-plumber-v2-4.3-network-health`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-4.3-network-health`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (canon-surface: terminal event flow, win/lose state machine — the
  v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (current: slices 1–3 + 4.1/4.2 + the capacity-cost routing model
  (Job A) + readability assist (B) + forecast flow-shift (C) + W1 pin — all merged).
  Rebase onto origin/v2 if it moves mid-work; clean-rebase hygiene (`git diff --check`).
- **CI NOTE:** GitHub Actions billing is blocked at the account level (user action pending) —
  CI on your PR will be red/not-started until fixed. That is NOT a code failure. You still
  run the FULL local suite (`odin test`, `harness run`) green before opening the PR; Perkins
  verifies locally at review. Do not let the red CI stamp slow your work.

## Mission (story 4.3 — closes Slice 4)

Implement **Story 4.3: Network Health meter + win/lose/retry** from
`_bmad-output/planning-artifacts/sprints/stories-v2.md` (line ~402) — full spec there.
This story closes the surge-survival loop: **Slice 4 exit = THE FUN-TEST LOOP.** Read the
GDD win/lose sections, architecture `[E16]`/`[E17]`/`[E30]`, and the 3.4 SLA + 4.1 telegraph +
4.2 crisis engine the meter consumes (SLA breach feeds drain; forecast surfaces the countdown).

**Acceptance (condensed — stories-v2 is canonical):**

1. **Network Health meter** — drains on sustained SLA breach: grace countdown starts on
   breach; drain = **max(severity) + per-tick cap** (never instant) `[E16]`; SLA hysteresis
   (enter/exit thresholds); re-breach during active grace = no-op `[E30]`; recharges when
   healthy; **empty → `Run_Lost` (Error 404)**.
2. **Terminal-event barrier** — after `Run_Lost`, the rest of the tick is skipped; **one
   terminal event per run** `[E17]`.
3. **Win condition** — uptime ≥ 90% through the surge → `Run_Won`.
4. **Retry** — creates a fresh run context (fresh arena, no leakage — the ODN-13 pattern);
   no-soft-lock property test passes `[FORGE #3]`.
5. **Goldens** — T1 + T2 of win AND lose frames; the no-soft-lock property test.
6. **Launchable increment** — the full surge-survival loop: predict → survive or drain →
   win/lose → retry.
7. **Scope guard:** the meter + win/lose/retry ONLY. NOT 4.4+ (no such story — Slice 5 is
   next), NOT the remaining four crisis archetypes (post-fun-gate), NOT era content.
   LOG_VERSION stays unless the new terminal events truly require it — flag first.

**Verify:** `odin test` green (core/demos/drift/lint), `harness run` green, `[E16]`/`[E17]`/
`[E30]` + no-soft-lock pins green, goldens blessed with proof (win + lose frames),
launchable increment in the PR body (you can LOSE — Error 404 — and retry).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-4.3-network-health
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
