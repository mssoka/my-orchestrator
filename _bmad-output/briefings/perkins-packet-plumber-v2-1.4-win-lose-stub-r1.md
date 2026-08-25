# Perkins briefing — round 1: packet-plumber-v2-1.4-win-lose-stub

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/24 (targets `v2`)
- **Reviewed sha:** `0b125e2b01472343bbc9119323787fff5fe22ff4` (short `0b125e2`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-1.4-win-lose-stub-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-1.4-win-lose-stub.md` + Story 1.4 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[ODN-13]` App mode FSM, the terminal-event barrier, §11.7 headless-test contract; ODN-1 core-engine-free; ODN-9/10/11 determinism) + GDD E6 (`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` — stub level here). No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out notes (it self-reviewed + fixed an early-return gating bug; 27 tests, harness 5/5, drift 29/29) — useful as leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**v2 Story 1.4 — Win/lose stub (closes slice 1).** The thinnest end-to-end feedback loop: a packet delivered scores (WIN); the tick cap reached short of the goal ends the run (LOSE / "Error 404 stub"); R/Enter retries on a fresh run + fresh seed. Adds `core/win_lose.odin` (`win_lose_eval`), a **terminal-event barrier** in `step` (the run freezes once terminal → exactly ONE terminal event per run), the win/lose/goal/tick_cap/terminal/Outcome state threaded through the T1 hash + serialize, a 7-contract `win_lose_test`, an app **Mode FSM** (Boot/Run/Game_Over) + WIN/LOSE toast + fresh-seed restart, win/lose demos, + re-blessed/new goldens. Built on 1.1 (determinism spine) + 1.2 (window/render) + 1.3 (per-hop flow); 1.4 is the app-mode/feedback layer (NO routing work). **It's a STUB** — full surge/win-lose depth is slice 4.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **THE TERMINAL-EVENT BARRIER (E17) IS LOAD-BEARING.** `step` must FREEZE once the run is terminal (won or lost) so exactly ONE terminal event is emitted per run — a golden captures a clean terminal state, not a mid-transition flicker. Verify the barrier is real: after terminal, subsequent ticks are no-ops (the manifest shows frozen identical ticks post-terminal; the terminal tick itself distinct). A barrier that emits >1 terminal event, or doesn't freeze, is a blocker.
- **DETERMINISM OVER THE FULL LOOP (incl the terminal frame) is load-bearing (ODN-9/10/11, carry from 1.1).** score/goal/tick_cap/terminal/Outcome MUST ride the T1 state-hash; a recorded loop reproduces byte-identical frames INCLUDING the terminal/game-over frame. A determinism break (terminal frame not replay-determinate; an un-logged RNG draw in the win/lose eval or the barrier; a state field not threaded through serialize) is a blocker.
- **NO ENGINE TYPES IN `package core` (ODN-1) — core stays engine-free / headless-testable.** The win_lose logic + barrier live in `package core`; engine/render types (raylib) must NOT leak in. An engine type in `core` is a blocker. (The app Mode FSM + toast can use the engine — that's `app/`, not `core`.)
- **WIN/LOSE INDEPENDENT GATING:** both goal==0 AND cap==0 = disabled (no win, no lose); win-beats-lose (a tick where both fire is a WIN). Verify the gating is correct — the minion flagged it self-fixed an early-return that over-disabled (killed lose when goal==0); confirm the fix (independent gating, the `cap_only_lose_with_no_goal` test pins it).
- **1.4 IS A STUB — full win/lose SURGE/depth is SLICE 4 (out of scope).** Do NOT flag "missing surge mechanics," "missing difficulty scaling," "win/lose too shallow" — the stub is intentionally the thinnest loop. The acceptance is: a delivered packet scores (WIN) + tick-cap LOSE + restart. Depth is later.
- **LOCKED ROUTING IS ALREADY IN (1.3) — NO routing work here.** Do NOT flag routing/forwarding/ECMP/bundles — those are 1.3 (merged) and slice 2. 1.4 is the feedback layer; it consumes 1.3's flow (a packet arriving at the sink = the win trigger).
- **The prototype is REFERENCE-ONLY** (`~/code/packet-plumber-prototype-ref/app/` — its app FSM/game-over DESIGN). Do NOT flag "should port the prototype's app code" — fresh code on v2 is the mandate.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (1.1 + 1.2 + 1.3 IN), not `main`. Don't flag "wrong base."
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas synced it). Review the PR content as-is at the sha.
- **Do NOT re-open 1.1/1.2/1.3 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- A **terminal-event barrier that doesn't freeze** or emits >1 terminal event (violates E17) — a blocker.
- A **determinism break** over the loop (terminal frame not replay-determinate; un-logged RNG; a state field not in the hash/serialize) — a blocker.
- **An engine type leaking into `package core`** (violates ODN-1) — a blocker.
- **Win/lose gating wrong** (both-0 doesn't disable; win doesn't beat lose; the goal==0 early-return bug resurfacing) — a real defect.
- **Restart not resetting cleanly** (stale state across runs; seed not fresh).
- A packet delivered that **doesn't score**, or a tick-cap that **doesn't lose**.
- An `odin test` / `odin build` / `harness` failure at `0b125e2`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 24 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `0b125e2`), `spec_files` = this briefing + the job briefing + Story 1.4 + the architecture (`[ODN-13]`, terminal-event barrier, §11.7, ODN-1/9/10/11) + GDD E6, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.4-win-lose-stub/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 24 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 24 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `0b125e2`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-1.4-win-lose-stub / **Reviewed sha:** 0b125e2 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-1.4-win-lose-stub-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. If a lens 429s mid-turn, one `continue` may revive it; if it hard-fails, note the degraded lens.
