# Briefing — packet-plumber-v2-4.2-surge-crisis (Surge SetPiece + Crisis Engine)

- **Job id:** `packet-plumber-v2-4.2-surge-crisis`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-4.2-surge-crisis`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (current: slice 3 + 4.1 forecast/warnings in; LOG_VERSION 3). Rebase onto
  origin/v2 if it moves mid-work; clean-rebase hygiene (no leftover conflict markers —
  `git diff --check` before force-with-lease).

## Mission (story 4.2 — the surge hits)

Implement **Story 4.2: Surge SetPiece + Crisis Engine (root-cause, fair)** from
`_bmad-output/planning-artifacts/sprints/stories-v2.md` (line ~372) — full spec there.
Read the GDD crisis sections (five archetypes; crises = consequence of a topology flaw the
player should have designed around; every crisis foreshadowed by readable warning signs with
lead time — 4.1 built the telegraph), the architecture `[ODN-4]` (crisis engine downstream of
flow, READ-ONLY topology view in — never writes topology), `[ODN-7, REVIEW M1]` (Director
never reads crisis state), and `[E13]` dedup.

**Acceptance (condensed — stories-v2 is canonical):**

1. **Surge SetPiece** — data-driven in `crises.json`: a forecast 10× demand spike that
   cascades into saturation if the player is unprepared. Fires **on schedule from the seed**
   (deterministic — same seed → same crisis timeline, `[E10]`).
2. **Crisis Engine** — downstream of flow, read-only topology view `[ODN-4, REVIEW M1]`; the
   Director never reads crisis state (structural, `[ODN-7]`).
3. **Fairness contracts:** **no crisis without a resolvable root cause** + preventive
   redesign; **no crisis on a healthy within-capacity topology** `[AC-E13]`; **one crisis
   per root cause per activation** — dedup, re-trigger only after `Crisis_Resolved` `[E13]`.
4. **Structured `root_cause`** — every crisis carries a ref to the topology flaw + a
   `preventive_redesign` (what the player could have built).
5. **Wiring with 4.1:** the forecast panel NAMES the surge with a countdown; the engine
   FIRES it on cue. The telegraph exists; this story makes it true.
6. **Golden:** T1 + event-stream golden (`Crisis_Triggered{Surge}` within the scheduled
   window) — bless deliberately with proof; existing goldens must not shift (if one does,
   STOP and flag).
7. **Scope guard:** surge archetype + engine + root-cause ONLY. NOT 4.3 (Network Health
   meter / win-lose-retry), NOT the other four crisis archetypes (post-fun-gate), NO new
   player commands (LOG_VERSION stays 3 unless truly required — flag first).

**Verify:** `odin test` suites green (core/demos/drift/lint), `[AC-E13]` fairness +
`[E13]` dedup + schedule-determinism tests, golden blessed with proof, launchable increment
(the surge hits on cue; you can see WHY — the root cause) in the PR body.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-4.2-surge-crisis
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
