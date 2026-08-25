# Perkins briefing — round 1: packet-plumber-v2-5.7-runtime-telemetry

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/47 (targets `v2`)
- **Reviewed sha:** `6b0949765340f1233e31b498bccfea73b4ca9f5e` (short `6b09497`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.7-runtime-telemetry-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.7-runtime-telemetry.md` + the story 5.7 card in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + canon `odin-architecture-v1.md` **§7.2 Logging / §7.4 Event system / §7.6 Debug tools** (the story realizes those sections). No GitHub issue.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — live; a "glm-4.7" self-id is a hallucination, not a misroute). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** CI billing is FIXED — checks run green again (migration/unit/integration/terraform). Use CI if helpful; YOUR local verification at the sha remains ground truth (`odin test`, `harness run`, drift-check, overlay-check).

## What the PR does (review scope)

**Story 5.7 — high-fidelity runtime telemetry (stats stream + debug overlay), derived ONLY from the existing deterministic state:**
- **Part A — the stats stream (`--stats-out <path>`, CSV):** `core/stats.odin` — a deterministic per-tick `Stats_Record` derived exclusively from existing state (SLA accumulators, bundle view, per-tick drop sites, health meter, T1 hash). ONE CSV serializer shared by harness and app → byte-identity by construction. Harness: `run <demo> --stats-out` writes the stream through the real loop; `stats-check <demo>` pins replay-identity (live == replay byte-for-byte via the blessed-log replay path). App: same flag, same format, per stepped tick. Pins: 4 core unit tests + byte-identical across 9 demos incl. pause (5.3 schedule, 555KB), surge (crisis re-fire), health_lose (terminal).
- **Part B — the debug overlay (`D` key, `-define:PP_DEBUG=true`):** per-pipe readout (on select), per-class table, congestion heat (util% tint ladder), global line, live event tail — all reading the SAME stats record the stream pins. Golden-safe by three layers: compile-excluded from every non-PP_DEBUG build (harness never defines it), off by default, capture path never calls it. AC3 verified via `overlay-check` rendering the shipped overlay over `qos_contention` — panel showed Email 84% loss / Streaming 65% loss (both LAT+LOSS), 100% util heat, t60 drop events.
- Verification (minion-claimed): 162 core tests green (158 + 4 new), lint 6/6, full harness suite green, both app builds compile, sample congested stream excerpt in the PR body. The briefing's open decisions were delegated + documented in the PR (CSV over JSONL, metric definitions, per-sim-tick emission, Decisions & rationale section).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the determinism contract.** The stats stream must be DERIVED ONLY from the existing deterministic state/event stream: NO wall-clock timing, NO render sampling, NO new nondeterminism. Any wall-clock/render-sampled value in the emitted stream = a blocker (it breaks the determinism spine 5.3 just pinned). The one-CSV-serializer-shared-by-harness-and-app is the byte-identity contract — verify it holds (same code path both sides), and replay-identity (live == replay) must hold (the `stats-check` pin).
- **🚨 Golden-safety of the overlay.** The overlay must be compile-excluded from every non-PP_DEBUG build (harness never defines it), off by default, and unreachable from the capture path — all 24+ pre-existing goldens + the 5.3 pause goldens must be byte-identical. A leak of overlay output into the golden/capture path = a blocker.
- **Faithful shaping, no invented metrics:** the Stats_Record shapes EXISTING counters (per-pipe offered/carried/dropped by class + Drop_Reason, utilization; per-class demand/delivered/dropped/loss%/avg latency/SLA; global tick/gen/sim-hash/score/meter from `core/flow.odin`) — verify no double-counting, no invented metric, and the derived values match the state they claim to summarize (spot-check against the sim).
- **Delegated decisions documented, not re-litigated:** CSV-over-JSONL (byte-determinism + diffability), per-sim-tick emission, metric definitions — the minion documented the rationale in the PR. Verify the choices honor the determinism contract; do NOT re-open them unless a choice breaks the contract.
- **Base = `v2`** — includes 5.5/5.6/5.3 (pause, 7b56485). Carry-forward only; do NOT re-open settled findings (the pause determinism spine is settled/verified — this diff must not weaken it).
- **Scope guard:** telemetry export + overlay only — no new capture semantics, no changes to the existing event-stream shape, no QoS gameplay changes (5.8 is a separate held job).

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.7-runtime-telemetry/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.7-runtime-telemetry-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
