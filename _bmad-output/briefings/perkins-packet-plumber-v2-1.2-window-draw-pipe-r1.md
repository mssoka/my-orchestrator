# Perkins briefing — round 1: packet-plumber-v2-1.2-window-draw-pipe

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/22 (targets **`v2`** — the from-scratch rewrite branch, NOT main)
- **Reviewed sha:** `8509fc23dd37d1d603ffb591e090b84bf7efa121` (short `8509fc2`; commit "v2 slice-1 story 1.2: first runnable app.bin — window + static map + draw one pipe")
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-1-2-window-draw-pipe-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-1.2-window-draw-pipe.md` + `_bmad-output/planning-artifacts/sprints/stories-v2.md` (Story 1.2 card) + `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (S1 Topology, Command_Bus, §11.7, the ODN spine) + the GDD (E1.1 node+pipe model, E1.2 draw interaction). No GitHub issue.
- **prior_findings:** the 1.1 round's consolidated.json (`_bmad-output/perkins/packet-plumber-v2-1.1-walking-skeleton/r1/consolidated.json`) — CONTEXT (1.2 builds on 1.1's spine; the 1.1 invariants carry forward). This round's findings are about the 1.2 delta.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **Model:** zai-coding-cn/glm-5.2 (kimi quota down — the sanctioned review fallback).

## What the PR does (review scope)

**The first runnable `app.bin`** (slice-1 story 1.2, building ON story 1.1's determinism spine — the spine is already merged in v2):
- A 1280×720 raylib window rendering a hardcoded static map.
- The player can **draw one pipe** (drag node→node, snap, cost) and watch it appear.
- Minimal `Topology` (node + pipe data model), a `Command_Bus` (draw command, validation, apply), and the render/view loop — on top of the 1.1 spine.
- **T2 pixel golden** for the drawn-frame state (the harness captures + the replay gate verifies).
- **W1 carry-forward (from #21):** a CI-exercised drift-rejection NEGATIVE test — a deliberately-drifted action log must be REJECTED by the replay gate, proven in CI.
- **No routing / no packet flow yet** (deliberate — that's story 1.3).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

This is the first playable surface, built on the load-bearing spine. Verify directly against the code + empirically where possible.

- **REPLAY-EQUALITY OVER DRAW IS THE LOAD-BEARING INVARIANT (E10 carried):** the draw/apply path must route through the action-log + state-hash — a RECORDED draw sequence reproduces **byte-identical frames** (re-stepping `(seed, action_log)` with the draw actions → identical `state_hash` sequences + identical rendered frames). Verify the replay test actually covers a draw sequence (not just the 1.1 empty-map case) + is non-vacuous.
- **ODN-1 (carried):** `package core` must STILL have no engine symbols — the topology/draw/command logic in core must be engine-free; raylib must live ONLY in the app layer. A raylib type leaking into `package core` is a blocker (breaks the determinism spine).
- **ODN-10 (carried):** integer-only, no map-iteration in core — the new Topology/Command_Bus code must respect this.
- **The T2 pixel golden must be REAL:** the harness captures the drawn-frame state + the replay gate verifies it. Verify the golden exists + the comparison is byte/pixel-exact (not a fuzzy or absent check).
- **The W1 CI negative test must actually be in CI** (the whole point of W1 was the #599-r2 gap: the gate worked locally but nothing exercised the rejection path in CI). Verify: a deliberately-drifted action log is fed + the gate rejects it, in a CI-exercised test (not a local-only manual check). A W1 that's "folded in" only as a local script = the gap persists = a legitimate finding.
- **The draw interaction is real:** drag node→node, snap, cost — verify the interaction works (the Command_Bus validates + applies; the drawn pipe appears + is recorded in the action-log). A draw that doesn't route through the action-log breaks replay-equality.
- **From-scratch, not a copy** — the prototype is reference-only; flag any wholesale copy of its render/topology code.
- **Do NOT flag the absence of routing/packet-flow** — story 1.3 by design (the briefing is explicit).
- **The window is now EXPECTED** (story 1.2 IS the window) — this is the first visible surface; headless-only was 1.1.
- **The harness/CI still green** (`odin test` + `odin run harness` + the T2 golden + the W1 test).

### Legitimate findings here would be
- **A draw/apply path that bypasses the action-log** (a drawn pipe that isn't recorded → replay-equality breaks) — a blocker.
- **An engine type in `package core`** (ODN-1 violation) — a blocker.
- **The T2 golden is absent/fuzzy** (no byte-exact comparison) — a blocker (the golden is the story's acceptance).
- **The W1 CI negative test is missing or local-only** (the #599-r2 gap persists) — a blocker-class finding (it was the explicit carry-forward).
- **A float/map-iteration leak in core** (ODN-10) — a blocker.
- **A wholesale copy of the prototype's render/topology code.**
- **A test failure** or the app not building/launching.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 22 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + the stories-v2 card + the architecture (S1, Command_Bus, §11.7, ODN spine) + the GDD (E1.1/E1.2), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1`, `prior_findings` = none for this PR (the 1.1 round is CONTEXT). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 22 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 22 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-1.2-window-draw-pipe / **Reviewed sha:** 8509fc2 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-1.2-window-draw-pipe-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
