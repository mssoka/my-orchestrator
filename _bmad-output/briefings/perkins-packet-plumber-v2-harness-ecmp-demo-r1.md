# Perkins briefing — round 1: packet-plumber-v2-harness-ecmp-demo

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/29 (targets `v2`)
- **Reviewed sha:** `f90351da1054d2b213ceb1a22afedc7e718c3d38` (short `f90351da`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-harness-ecmp-demo-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-harness-ecmp-demo.md` + the harness/ECMP architecture sections of `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[E10]` replay determinism, §11.7; `[ODN-1]` core engine-free) + the rlsw SW-renderer harness contract (bit-exact `PLATFORM_MEMORY` rendering, no GPU). No GitHub issue.
- **prior_findings:** none (this is r1 — the harness mini-story is new). CONTEXT: the implementing minion's badge-out (spawn_node demo directive with deterministic spawn-order ids, `ecmp.dem` demo, T2 retro-verify for 2.1/2.2/2.3: bundle/flow/draw/win/lose goldens matched bit-for-bit with NO drift, ecmp (2.2) + demolish (2.3) NEW goldens first-blessed via the pixel-verification path — no silent re-bless; gates: 8/8 demos T1+T2+replay, drift 47/47, odin 54/54, lint green, core untouched; decisions: fixture opt-out, Demo_Replay single-struct, `-ffp-contract=off` platform-independent goldens) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**PP infra mini-story (deferred from 2.2's rec): the rlsw SW-renderer harness + node-spawn demo directive + ecmp.dem + T2 retro-verify for 2.1/2.2/2.3.** Builds the harness that runs the demos headless in the SW renderer (`PLATFORM_MEMORY`, no GPU — bit-exact rendering), adds a `spawn_node` directive to the demo scripting so scenes can spawn nodes deterministically, ships the `ecmp.dem` demo (2.2 ECMP hash routing shown live), and retro-verifies the T2 pixel fidelity of the 2.1/2.2/2.3 goldens (bundle/flow/draw/win/lose matched; ecmp + demolish are NEW first-blessed goldens). This is the story that CLOSES the T2-pixel debt flagged since 2.2.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 GOLDEN-BLESSING DISCIPLINE — THE load-bearing invariant.** A pixel MISMATCH against an ALREADY-blessed golden (bundle/flow/draw/win/lose) = a REAL blocker (drift). But the ecmp + demolish goldens are **FIRST-BLESS**: their pixel content was blessed in this very PR — do NOT flag "new golden files added" as a defect; instead VERIFY the blessing path actually ran pixel-verification (mismatch → finding, never a silent re-bless / blind accept). A first-bless done through the real comparison path is the contract; a skip/force-accept is a defect.
- **🚨 rlsw BIT-EXACTNESS [PLATFORM_MEMORY] — load-bearing.** The harness renders in the SW renderer (`PLATFORM_MEMORY`, no GPU) so goldens are platform-independent (`-ffp-contract=off`). Do NOT flag "goldens are platform-dependent" or "no GPU path" — that's the design. A golden generated through a NON-deterministic path (unbounded float ops, unseeded RNG in the render, map-iter order in the pixel path) = a blocker.
- **NODE-SPAWN DETERMINISM [E10].** `spawn_node` assigns ids in SPAWN ORDER (deterministic); the demo script drives a fixed sequence. An id assigned by anything order-independent-in-practice but not guaranteed (map iteration, hash order, pointer value) = a real defect — the same discipline as ECMP (array-indexed, no map-iter in the hot path).
- **HARNESS IS INFRA, NOT PRODUCTION.** The harness/demos live OUTSIDE the core engine and the app's production path (core engine-free [ODN-1] — zero core imports in the harness). Do NOT flag "harness code isn't in the game binary" or "demo content is trivial" — the harness is a dev/verification tool; its job is to prove the demos, not ship gameplay.
- **Demo_Replay SINGLE-STRUCT decision (routing-ruling lens-guard).** The replay is a single struct (`Demo_Replay`), NOT per-demo variants — a deliberate simplification the minion documented. Do NOT flag "replay should be per-demo polymorphic".
- **FIXTURE OPT-OUT (documented decision).** The demo fixture (T2 pixel fixtures) is opted out of the `odin test` runner deliberately — the pixel verification runs through the harness demos instead (8/8 demos T1+T2+replay). Do NOT flag "fixture tests missing from odin test" — the harness demos ARE the fixture verification.
- **CORE UNTOUCHED.** The 2.1/2.2/2.3 core stories are MERGED and Perkins-verified — do NOT re-open their findings; carry-forward only. If this PR touches core engine logic, THAT is worth flagging (it claims to be harness/demo-only).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`**, not `main`.
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

### Legitimate findings here would be
- **Golden DRIFT** — a previously-blessed golden (bundle/flow/draw/win/lose) whose pixels changed without a matching, documented, verified re-bless — a blocker.
- **A silent re-bless / forced-accept golden path** (skipped pixel verification, blind overwrite) for the NEW ecmp/demolish goldens — a blocker.
- **A non-deterministic render or spawn path** (unseeded RNG draw, map-iter in the pixel/spawn path, float-op order dependence) — a blocker [E10]/bit-exactness.
- **A `spawn_node` id assigned by hash/pointer/map order** instead of spawn order — a real defect.
- **Core engine logic changed by this PR** (it claims harness/demo-only) — a real defect [ODN-1].
- **An `odin test` / `odin build` / `harness` failure at `f90351da`** (the drift + demo gates are real: drift 47/47, demos 8/8).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 29 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-harness-ecmp-demo/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `f90351da`), `spec_files` = this briefing + the job briefing + the architecture (`[E10]`/`[ODN-1]`/§11.7), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-harness-ecmp-demo/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 29 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 29 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `f90351da`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-harness-ecmp-demo / **Reviewed sha:** f90351da / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-harness-ecmp-demo-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `kimi-coding/k3`** — the permanent policy for Perkins (reasoning roles; the frontier reviewer). If a lens 403s: one `continue` may revive it; if the round hard-fails on 403, self-report `blocked` — Silas redirects to `deepseek/deepseek-v4-flash` (the sanctioned failover; glm-5.2 is RETIRED — never use it).
