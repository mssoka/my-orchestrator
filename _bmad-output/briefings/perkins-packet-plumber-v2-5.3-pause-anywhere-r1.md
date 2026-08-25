# Perkins briefing — round 1: packet-plumber-v2-5.3-pause-anywhere

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/46 (targets `v2`)
- **Reviewed sha:** `9ae86121743955a8a8685ce2c2ca51447d5c54e5` (short `9ae8612`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.3-pause-anywhere-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.3-pause-anywhere.md` + the plan card in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (story 5.3). No GitHub issue.
- **Model:** `zai-coding-cn/glm-5.3` (Perkins reasoning tier — the live top tier; VERIFIED routing 2026-08-14; a "glm-4.7" self-id from the model is a hallucination, not a misroute). Launch EVERY lens pane with `pi --model zai-coding-cn/glm-5.3`. Interim fallback if the provider errors: `deepseek/deepseek-v4-pro`.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **CI note:** GitHub CI is account-billing-blocked — YOUR local verification at the sha is the ground truth (`odin test`, `harness run`, drift-check, preview-check).

## What the PR does (review scope)

**Story 5.3 Pause-anywhere** (deterministic pause + planning under the veil):
- **App** (`app/main.odin`): Mode.Paused (ODN-13 Run ↔ Paused), P/SPACE toggle (GDD controls canon, no collisions), stepping gated to Run (no accumulation, no steps → deterministic freeze), dim veil + PAUSED label, and the full planning surface live under the veil (draw/place/demolish/QoS + glow/preview + demolish popover).
- **Harness** (`harness/demo.odin`, `harness/run.odin`): `<n>ms pause|resume` run directives (threaded through Demo_Replay); commands lower to `apply_tick` = the next tick the sim will execute (ODN-2 — mid-pause edits log at paused tick + 1, landing on the first resumed step; no-pause demos byte-identical). The virtual clock records ONE T1 hash per wall tick — paused windows repeat one hash with a loud stability check in both live + replay paths.
- **Core** (`core/pause_test.odin`, new): pins the driver contract — stable window, resume from the exact tick, mid-pause edits, replay byte-identical [E10].
- **Golden** (`demos/pause.dem` + `goldens/pause.*`): era-3 mid-crisis pause at tick 1210 — window 1211–1400 is one repeated hash (crisis frozen; T2 banner strip pixel-identical across the pause), mid-pause standard-pipe edit lands exactly at the first resumed step, replay gate + 174 drift mutations cover it. All 24 pre-existing goldens unshifted (additive).
- **Canon:** story 5.3 card status note in `stories-v2.md` (the GDD Controls amend was already in 5f51236 — not re-amended).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 LOAD-BEARING — the determinism spine.** Pause must freeze the sim deterministically: the paused window is ONE repeated T1 hash (stability-checked in live + replay), resume continues from the EXACT tick, and a run with pause/resume + mid-pause edits replays byte-identical [E10]. Any path where the paused window drifts, resume lands on the wrong tick, or the replay diverges = a blocker. Do NOT bless a "state stable" claim that excludes the fast-path channel (mid-pause edits render instantly in the app while the harness defers to the step boundary — two models converging at boundaries; the T1 pin freezes the sim, the log pins the edits).
- **Known-legit, do NOT flag:** the FIRST paused wall-tick hash legitimately differs from the last stepped tick's hash (the T1 hash advances one more wall tick into the pause window); Pause is DRIVER-level (harness), never core.
- **Additive goldens:** existing goldens MUST NOT shift — pause is additive (no pause in any existing log). Any old-golden drift = a blocker.
- **Mid-pause edit semantics:** edits while paused must log at paused tick + 1 and land on the first resumed step — a mid-pause edit that applies at the wrong tick (or drops) = a blocker.
- **Scope guard:** pause mechanics + indicator ONLY — no speed controls, no save/load, no other bindings, no telemetry. GDD Controls canon is settled (P = P / Space) — do not re-litigate.
- **Base = `v2`** — 5.5/5.6 merged into it (bcf2f45); carry-forward only, do NOT re-open settled findings. CI is billing-blocked; local suite = ground truth.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-anywhere/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = the issue dump + job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-anywhere/r1`, `prior_findings` = N/A. Headless mode owns pane mechanics, lens JSONs, one retry per failed lens, chunking, verification pass, consolidation. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK"; degraded guard: any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` (STDOUT ONLY, never 2>&1); `if [ -z "$TOKEN" ]` → fallback `gh pr comment` + note fallback-comment; else `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`.
- Body format per the playbook (round N of 3, findings counts, verdict line).
- Before posting, re-fetch `headRefOid`. Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-5.3-pause-anywhere-perkins-r1 working` at start; final message = verdict + review URL + counts. Skip Step 5 (no fixing).
