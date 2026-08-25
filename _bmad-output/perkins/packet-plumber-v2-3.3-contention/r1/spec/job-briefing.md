# Briefing — packet-plumber-v2-3.3-contention (node serialization + contention drop ladder)

- **Job id:** `packet-plumber-v2-3.3-contention`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-3.3-contention`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the v2 line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` (current HEAD: 3.2 merged, LOG_VERSION 3). Rebase onto origin/v2 if it moves
  mid-work; **clean-rebase hygiene is a standing lesson** — NO leftover conflict markers
  (a `>>>>>>>` marker shipped in a force-push compiled nowhere and failed CI, 2026-08-12:
  verify locally, `git diff --check`, before force-with-lease).

## Mission (story 3.3 — the contention half of the QoS differentiator)

Implement **Story 3.3: Node serialization + contention drop ladder** from
`_bmad-output/planning-artifacts/sprints/stories-v2.md` (line ~275) — full spec there.
Read the architecture `[ODN-3]` (QoS inside Flow), `[E7]` no-starvation, `[E9]` drop ladder,
`[E22]` pool exhaustion, and the GDD lanes/contention sections. Builds directly on 3.2's
`qos_allocate` (weight-only WFQ per pipe).

**Acceptance (condensed — stories-v2 is canonical):**

1. **`qos_serialize`** — at each node, packets serialize by lane **Express → Standard →
   Best-effort**, work-conserving with gap-fill + a **WRR floor** (≥1 slot per non-empty
   lane per window — no starvation) `[E7]`. Inside Flow, not a peer system `[ODN-3]`.
2. **Contention drops** — when a pipe is oversubscribed, drops by the **full ladder
   BE → Standard → Express** `[E9]`; pool-exhaustion drops the lowest-priority lane first
   `[E22]`.
3. **The serialization visual** — packets visibly **queue and exit in lane order** at
   nodes (this is the launchable demo: oversubscribe a pipe → watch best-effort drop first,
   see the queue serialize by lane).
4. **Golden:** T2 of the queue + drops (bless deliberately with proof, per the 3.2
   precedent; existing goldens must not shift — if one does, STOP and flag, do not re-bless
   without documenting why).
5. **Scope guard:** serialization + drops ONLY. Do NOT implement 3.4 (SLA accumulators) or
   any new player commands — if a command kind is genuinely required, flag it in the PR
   before touching LOG_VERSION (currently 3).

**Verify:** `odin test` suites green (core/demos/drift/lint), `[E7]`/`[E9]`/`[E22]` tests
green, golden blessed with proof, launchable increment demonstrated in the PR body.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-3.3-contention
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
