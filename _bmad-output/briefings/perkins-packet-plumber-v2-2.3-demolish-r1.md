# Perkins briefing — round 1: packet-plumber-v2-2.3-demolish

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/27 (targets `v2`)
- **Reviewed sha:** `8a652dd798607a57ea7de2a2e45b930612eade9d` (short `8a652dd`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-2.3-demolish-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-2.3-demolish.md` + Story 2.3 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (full card line 199+ + slice-2 exit criteria) + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (E1 severance-under-bundles, E2 terminal-forbidden, E27 junction-batch, E29 auto-migration, the 4-rule spine rule 1 = table rebuild, `[RR]` routing, §11.7 headless-test contract; ODN-1 core-engine-free; ODN-9/10/11 determinism) + GDD E1.3/E1.4. No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (54 core tests incl 11 demolish contracts + the bidirectional-draw carry-forward; harness 7/7; drift 41/41; T2 pixels deferred per the rlsw gap) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**v2 Story 2.3 — Demolish + severance under bundles + automatic migration (CLOSES SLICE 2).** The locked-model payoff: demolishing a pipe of a bundle **shrinks the pool gracefully** (only full-bundle-loss drops the route); terminal-demolish is forbidden (`.Terminal_Demolish`); junction demolish is an **atomic batch** (incident pipes first in edge-id order, each per E1, then the vertex); and **in-flight packets re-forward at the next junction automatically** (no stale routes — the per-hop-forwarding payoff). Demolish is a **logged command** (like draw — validate→apply, action-log, replay-reapplied at its tick). Changed: core/{types,topology,flow,serialize}, demolish_test.odin (new, 11 contracts), flow_test.odin (+ bidirectional carry-forward), harness/{demo,run}, demolish.dem + goldens.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 E29 AUTO-MIGRATION IS STRUCTURAL — THE load-bearing invariant (the story's whole point).** NO cached route — a demolish → table rebuild (4-rule spine rule 1) → in-flight packets re-forward at the NEXT JUNCTION with zero special-casing. The Perkins lens-guard CONFIRMS no `route[]` / spawn-cached path creeps in. A cached-route/spawn-time-route path (or per-packet pre-computed reroute) = a REAL blocker (it would be the prototype's BFS model sneaking back). The ABSENCE of a cached route is correct.
- **GRACEFUL SHRINK, NOT A HARD CUT [E1].** A bundle-member demolish reduces the POOLED capacity (re-derive, cap = sum of survivors); traffic continues. ONLY full-bundle-loss (all members gone) drops the route. A hard cut on a member demolish (traffic stops when it shouldn't) = a blocker.
- **`.Terminal_Demolish` [E2].** Terminal nodes can't be demolished — rejected with the typed error. A terminal demolish accepted (or the typed error missing) = a blocker.
- **JUNCTION DEMOLISH = ATOMIC BATCH [E27].** Incident pipes first (edge-id order, each per E1), THEN the vertex — ONE atomic edit, replay-deterministic. A junction demolish that's non-atomic, wrongly ordered, or non-deterministic = a blocker.
- **DEMOLISH IS A LOGGED COMMAND.** Applied via the validate→apply path, recorded in the action log, replay-reapplied at its tick (like draw). A demolish that mutates state outside the action-log/replay path = a determinism break.
- **DETERMINISM (ODN-9/10/11, carry from slice 1).** A demolish MID-TRAVERSAL replays byte-identical (T1); the post-demolish frame is deterministic (T2). Verify: the demolish's table rebuild + the re-forward decision ride the hash; the flow's defensive "pipe vanished mid-traversal → drop back to departure node + re-forward" path (flow.odin) is what 2.3 makes LIVE — verify it's deterministic.
- **BIDIRECTIONAL-DRAW CARRY-FORWARD** — `test_reverse_draw_is_bidirectional` (draw both pipes reversed, assert the packet still delivers) must be present + real + passing.
- **T2 PIXELS DEFERRED per the rlsw gap (documented carry-forward, NOT a defect).** demolish.dem pins the post-demolish state via T1 hashes + the replay gate (structural verification). Do NOT flag "T2 pixel not verified" as a blocker — it's the flagged carry-forward (mini-story with the rlsw harness, Gru's call).
- **CORE ENGINE-FREE (ODN-1)** — zero engine imports in `package core` (the minion reports `odin check app` + `odin check harness` clean).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slice 1 + 2.1 bundles + 2.2 ECMP IN), not `main`.
- **The prototype is REFERENCE-ONLY** (mine its demolish UX/feel; its routing was NOT the locked model — the reroute logic is rebuilt clean).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas synced it). Review the PR content as-is at the sha.
- **Do NOT re-open 1.1–2.2 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- **A cached-route / spawn-time-route path** (violates E29 structural; the prototype's BFS sneaking back) — a blocker.
- **A hard cut on a bundle-member demolish** (traffic stops when the pool should shrink) — a blocker [E1].
- **A terminal demolish accepted** (or the typed error missing) — a blocker [E2].
- **A junction demolish that's non-atomic / wrongly ordered / non-deterministic** — a blocker [E27].
- **A determinism break** (a demolish mid-traversal replays differently; the re-forward not in the hash path; the demolish not action-logged) — a blocker.
- **The bidirectional-draw carry-forward missing or fake** — a finding.
- **An engine type leaking into `package core`** (ODN-1) — a blocker.
- An `odin test` / `odin build` / `harness` failure at `8a652dd`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 27 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.3-demolish/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `8a652dd`), `spec_files` = this briefing + the job briefing + Story 2.3 + the architecture (E1/E2/E27/E29, rule 1, `[RR]`, §11.7, ODN-1/9/10/11) + GDD E1.3/E1.4, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-2.3-demolish/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 27 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 27 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `8a652dd`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-2.3-demolish / **Reviewed sha:** 8a652dd / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-2.3-demolish-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. **BURST WARNING (proven, mitigation VALIDATED):** the ZAI account 429 trips at ~9+ concurrent glm panes; **staggering the lens spawns (wave-1 ≤4 → wave-2 rest) keeps peak ≤6 and avoids it entirely** (validated twice this evening, zero 429s). A righttenantry minion (rc3-7, pTQ) is mid-fix on glm right now, so stagger anyway. If a lens 429s, one continue revives it.
