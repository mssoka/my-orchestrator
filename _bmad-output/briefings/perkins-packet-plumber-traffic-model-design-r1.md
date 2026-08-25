# Perkins briefing — round 1: packet-plumber-traffic-model-design

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/53 (targets `v2`)
- **Reviewed sha:** `72142044dac0b7f661355c9d4c139fbbd2123bda` (short `7214204`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md` + the source design thread at `/Users/moses/code/_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html` (§Section B design notes — the user-endorsed thread) + the user ruling (2026-08-15: the Section B notes are TASKS). The lavish review approved this design — the PR ships it to canon.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED (checks green). Local verification at the sha remains ground truth.

## What the PR does (review scope)

**DOCS/CANON-ONLY** (no code, no balance.json changes — those are the story cards'
jobs): the surge-explainer's Section B design thread becomes canon + story cards.
- **Design spec:** the four threads (1 narrow-pipes = residential access tier —
  congestion is an AGGREGATION event, endpoints never self-congest; 2 per-terminal
  demand caps — no single endpoint saturates alone; 3 aggregation groups — the
  demand director clusters terminals so surge stress lands on aggregation points;
  4 diverse terminal types — residential/small-biz/campus analogues) in
  Given/When/Then shape, real-world rationale (1G/40G/100G math), balance levers
  (catalog/balance.json placement), determinism constraints (seed-derived, no
  wall-clock, replay byte-identical or deliberate LOG_VERSION), explicit
  interaction with existing canon (E22 pool, E9 bounds, 4.1 strain, 5.1 growth
  spawning, 5.8 QoS) — conflicts resolved explicitly (growth-spawn validity vs
  aggregation groups).
- **Story cards 5.9–5.12** appended to stories-v2 with proposed sequencing
  (post-5.4 / slice-6 rationale).
- **GDD decision-log amendment** (M6 + decision-log entries): the traffic-realism
  ruling + the four mechanics — SECTION-ADDITIVE, no terminology rewrites
  (coordinated with the parallel terminology audit — Phase 2 rename PR serializes
  behind 5.2's merge).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — section-additive, no terminology rewrites.** The GDD edits must
  be ADDITIVE (new sections/decision-log entries) — this diff must NOT rewrite
  existing terminology (the terminology audit owns that; its Phase-2 rename PR is
  serialized behind 5.2's merge). A terminology rewrite hiding in this docs PR =
  a conflict-with-a-queued-job blocker (it would collide with the audit's PR).
- **Canon coherence:** the four threads' mechanics must be consistent with EXISTING
  canon — E22 pool, E9 bounds, 4.1 strain/forecast, 5.1 growth spawning, 5.8 QoS —
  and explicit about the resolved conflicts (growth-spawn validity vs aggregation
  groups is the named one). A silent contradiction = a blocker.
- **Determinism constraints stated correctly:** all four threads seed-derived, no
  wall-clock, replay byte-identical OR a deliberate LOG_VERSION bump — the spec
  must state which per thread (the 5.1 derive-don't-record and 5.8 golden-fold
  disciplines are settled canon to follow).
- **Story cards are complete + sequenced with rationale** (post-5.4? slice-6?) —
  missing load-bearing card content (Given/When/Then, balance levers, acceptance)
  = a finding.
- **Base = `v2`** — full shipped line. Carry-forward only; do NOT re-open settled
  findings.
- **Scope guard:** design docs + story cards ONLY — no code, no balance.json
  changes (a code change in this docs PR = a blocker).

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-traffic-model-design-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
