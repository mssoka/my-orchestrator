# Briefing — packet-plumber-v2-3.2-lane-qos (3-lane QoS + emphasis dial)

- **Job id:** `packet-plumber-v2-3.2-lane-qos`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-3.2-lane-qos`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the v2 line's standing bar — 3.1 and the harness both had
  rounds; the round runs on the sanctioned reasoning model per fleet policy).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` — the live dev line. NOTE: story 3.5 (node placement) is IN FLIGHT on the
  same repo; your branch starts from the current `origin/v2` HEAD and must not touch
  placement files. If origin/v2 moves while you work (3.5 merges), rebase onto the new HEAD.

## Mission (story 3.2 — the QoS differentiator, part 2)

Implement **Story 3.2: 3-lane QoS + emphasis dial** from
`_bmad-output/planning-artifacts/sprints/stories-v2.md` (line ~255) — full spec there.
Also read §3 of the architecture (`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`,
esp. `[ODN-3]` QoS-inside-Flow, `[E5]` all-zero fallback, `[E6]` never-drop floor, `[E8]`
largest-remainder) and the GDD lanes section (all traffic starts Standard; player engineers
QoS by promoting/demoting; 3 lanes by design, DiffServ-faithful).

**Acceptance (condensed — stories-v2 is canonical):**

1. **`qos_allocate`** — integer WFQ, largest-remainder distribution, tie order
   E→S→B. **Weight-only** (demand is NOT an input) `[ODN-3]`. Lives inside Flow, not a peer
   system.
2. **Emphasis dial UI** — one per pipe; maps to weight presets in `balance.json` (e.g.
   express-heavy / balanced / best-effort-heavy — presets are YOUR call, keep them few and
   legible; wire via the existing data-driven catalogs/balance pattern, do not hardcode in
   code).
3. **All traffic starts Standard**; the player promotes/demotes per type and can override a
   type's lane per-pipe.
4. **Edge contracts:** all-zero weights → the catalog default preset `[E5]`; a never-drop
   class lane is **floored** and a zeroing edit that would floor it is **rejected** `[E6]`;
   the largest-remainder distribution test passes `[E8]`.
5. **Golden:** T2 of lane proportions changing (bless deliberately; existing goldens must not
   shift — if one does, STOP and flag, do not re-bless).
6. **Launchable increment:** run the app → set a pipe's emphasis → watch the lane proportions
   visibly change (a lane-proportions readout is part of the demo).

**Scope guard:** QoS only. Do NOT implement 3.3 (serialization/contention) or 3.4 (SLA) —
those are separate stories. Do NOT touch placement (3.5, in flight elsewhere): no edits to
`Cmd_Place_Router`-adjacent code or the tray; if a merge conflict appears in `serialize.odin`
(LOG_VERSION), resolve by taking the placement branch's version + your additive changes
(rebase onto origin/v2 first).

**Verify:** `odin test` suites green (core/demos/drift/lint), the `[E5]`/`[E6]`/`[E8]` tests
green, golden blessed, launchable increment demonstrated in the PR body.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-3.2-lane-qos
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
