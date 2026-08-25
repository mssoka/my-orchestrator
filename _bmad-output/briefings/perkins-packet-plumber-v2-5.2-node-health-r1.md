# Perkins briefing — round 1: packet-plumber-v2-5.2-node-health

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/54 (targets `v2`)
- **Reviewed sha:** `088fdcd76946d1d3bf2df1c8ac91c918fda58b67` (short `088fdcd`) — the CI-font fold (v2 merge incl. #52 Open Sans + deliberate 3-PNG T2 re-bless)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.2-node-health-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.2-node-health.md` + the story 5.2 card in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + arch (4.3 health, E30 seam). No GitHub issue.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI is green (the CI-font fold fixed the earlier red — re-verified at the sha).

## What the PR does (review scope)

**Story 5.2 — per-node health states (🟢 healthy → 🟡 strained → 🔴 critical),**
readable at a glance, every 🔴 traceable:
- **Measure (the minion's probed choice):** stuck-pile (un-forwardable packets)
  bandwidth ÷ node throughput ceiling, thresholded by the balance warnings 70/90 —
  SHARED with the 4.1 aggregate for coherence by construction; reusing the block
  keeps `catalog_hash` untouched (no golden re-bless for the measure).
- **Seam:** new `core/node_health.odin` beside the 4.3 health layer — NOT stats.odin
  (a derived surface; an N stats row would churn the 5.7 schema for zero replay
  value).
- **Derive-don't-record:** `crisis.node_health` is never serialized — pinned by
  replay identity + a byte-dump negative control (mutate the array → the dump must
  not change).
- **Traceability:** a hover inspect card (`NODE n · CRITICAL · util 150% (load 120 /
  80 u)`) — APP-LAYER ONLY, so T2 goldens are untouched.
- **Golden:** `node_health.dem` (era 3 + growth on): amber pin @t1, red host +
  growth-born terminals red @t200, host resolution @t400, connected legs green
  throughout. Existing 28/28 demos byte-identical. PLUS the CI-font fold: the v2
  merge (#52 Open Sans) + deliberate 3-PNG T2 re-bless (T1 + `.log.bin`
  byte-identical — font is presentation-only).
- Verification: 183 core tests, 29/29 demos (T1+T2+replay), drift 204 mutations
  rejected, lint, all builds incl. PP_DEBUG.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — derive-don't-record.** `crisis.node_health` must be derived
  per-tick, NEVER serialized: no LOG_VERSION change; replay byte-identity holds;
  the byte-dump negative control pins it (mutate → dump unchanged). A serialized
  health state = a blocker (it would break the 5.1/5.7 derive-don't-record
  discipline).
- **Measure correctness:** stuck-pile bandwidth ÷ throughput ceiling, thresholds
  shared with 4.1 (70/90) — verify the measure is game-correct (the minion's probe
  finding: a transit-inclusive utilization measure makes the healthy map scream —
  the chosen stuck-pile measure is the coherent one); catalog_hash untouched.
- **T2 immutability + the font fold:** existing 28/28 demos byte-identical; the
  node_health T2 fold is the ONLY new capture + the deliberate 3-PNG re-bless from
  the #52 font swap — T1 + .log.bin byte-identical (font is presentation-only; a
  T1 move = determinism break).
- **Traceability surface:** the hover inspect card is app-layer only (no harness
  T2 impact); every 🔴 node traceable to its numbers.
- **Readability canon:** icon + outline (+ pulse for 🔴) — never color alone.
- **Base = `v2`** — now includes #52 (Open Sans) + the full shipped line; carry-
  forward only; do NOT re-open settled findings.
- **Scope guard:** per-node health surface ONLY — no aggregate-meter changes, no
  crisis-engine changes, no a11y overhaul beyond the no-color-alone canon, no input
  work.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.2-node-health/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.2-node-health/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.2-node-health-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
