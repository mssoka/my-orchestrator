# Perkins briefing — round 1: packet-plumber-v2-1.1-walking-skeleton

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/21 (targets **`v2`** — the from-scratch rewrite branch, NOT main)
- **Reviewed sha:** `0419ba65fe269dcef13d74a43b3dd0eb3cee19aa` (short `0419ba6`; commit "v2 slice-1 story 1.1: headless determinism spine + golden harness")
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-1-1-walking-skeleton-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-1.1-walking-skeleton.md` + `_bmad-output/planning-artifacts/sprints/stories-v2.md` (Story 1.1 card) + `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (ODN-1/ODN-9/ODN-10/ODN-11/ODN-17/E10, §11.7). No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **Model:** zai-coding-cn/glm-5.2 (kimi quota down — the sanctioned review fallback).

## What the PR does (review scope)

**The foundational determinism spine of the from-scratch v2 build** (slice-1 story 1.1) — everything downstream depends on this code being exactly right:
- `package core` scaffold: `Run_State`, `step` (no-op), `state_hash` (per-tick FNV-1a-64 over the state, incl rng + events), `log_read`/`log_write` (binary action log).
- An owned `Rng` (splitmix64 → PCG32 XSH-RR, ~40 lines, constants in source) with pinned first-8-output test vectors.
- A golden harness skeleton (`tools/build_raylib_sw.sh` software renderer + memory platform; T1 manifest path `goldens/<demo>.t1`; the replay gate over `log.bin`) + one trivial `boot.dem` (seed, empty map, N ticks, capture).
- **Headless only** (deliberate — no window; the first runnable `app.bin` is story 1.2).
- From-scratch fresh code on v2 — the prototype's `core/`/`harness/` were REMOVED from v2 (preserved at `~/code/packet-plumber-prototype-ref` + git history, reference-only).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

This is the **load-bearing foundation** — the whole game's replay-equality depends on these invariants. Verify them directly against the code + empirically where possible.

- **ODN-1 — the no-engine-symbols gate (verify with `nm`/`odin build`):** `package core` must compile to an object with NO `vendor:*` / `core:os` / `core:time` symbols. This is THE gate the whole determinism argument rests on — a single engine symbol leaks nondeterminism. Verify empirically, not by claim.
- **ODN-9 — the RNG is correct + pinned:** the owned `Rng` (splitmix64 → PCG32 XSH-RR) must be integer-only, seeded deterministically, and its **first 8 outputs must match the pinned vectors** (the test asserts them). Verify the constants + the splitmix64→PCG32 derivation against the pinned vectors — a wrong constant that still passes the test (vectors written to match the wrong impl) is the failure mode to catch.
- **ODN-10 — integer-only, no map-iteration in core:** no floats in the core state/step path, no map iteration (ordered iteration is deterministic only by accident). Verify the core package has no float ops / no `map` iteration in the state path.
- **ODN-11 — state-hash + binary action-log:** `state_hash` is a per-tick FNV-1a-64 over the state (incl rng + events); the action log is a binary `log.bin`. Verify the hash covers the right state (rng + events included — a hash that misses the rng would let rng drift go undetected, defeating the replay gate).
- **E10 — replay-equality is real:** re-stepping `(seed, action_log)` twice yields **byte-identical** `state_hash` sequences. Verify the replay test actually does this (not a tautological same-object comparison).
- **ODN-17 — the harness's replay gate actually rejects drift:** the T1 manifest for `boot.dem` matches on re-run AND the gate **rejects** catalog / `logic_hz` drift. Verify the negative control is real (a drift → gate rejects) — the same "is the test a mask?" lesson as the #599 r2 inert-fix case.
- **From-scratch, not a copy:** the code must be a clean rebuild (mine the prototype-ref's DESIGN — RNG, serialize, harness shape — but fresh code). Flag any wholesale copy of the prototype's buggy code (the prototype was crash-prone; the whole point is a clean rebuild). A verbatim copy of the prototype's `core/` is a legitimate finding.
- **The boot.dem golden is trivial but real** — verify it captures per-tick hashes (incl rng + events), not an empty stub.
- **No BFS / no routing expected** — this story is the spine only; do NOT flag the absence of routing (it's a later slice by design).
- **No window expected** — headless is the deliberate lavish-approved choice; do NOT flag the absence of a window.
- **The build/harness tooling** (`tools/build_raylib_sw.sh` + the harness) — verify it builds + runs headless (`odin run harness -- run boot` green) — the "launchable increment" for this story.

### Legitimate findings here would be
- **An engine symbol in core** (ODN-1 violation) — a blocker (breaks the determinism spine).
- **The RNG vectors don't pin the real impl** (a wrong constant or a test written to match a wrong impl) — a blocker.
- **A float / map-iteration leak in the core state path** (ODN-10 violation) — a blocker.
- **The state_hash misses the rng or events** — replay drift would go undetected — a blocker.
- **The replay gate is a mask** (doesn't actually reject drift; the negative control doesn't bite) — the #599 r2 failure mode — a blocker.
- **A wholesale copy of the prototype's buggy code.**
- **A test failure** (Rng vectors, replay-equality) or the harness not building/running.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 21 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.1-walking-skeleton/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + the stories-v2 card + the architecture (ODN-1/9/10/11/17, E10, §11.7), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.1-walking-skeleton/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 21 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 21 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-1.1-walking-skeleton / **Reviewed sha:** 0419ba6 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-1.1-walking-skeleton-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
