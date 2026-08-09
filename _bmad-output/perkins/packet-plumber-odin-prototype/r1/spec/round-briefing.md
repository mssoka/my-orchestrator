# Perkins briefing — round 1: packet-plumber-odin-prototype

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/17 (targets `main`)
- **Reviewed sha:** `0118cc0b1a981a65e541b49fe00a7e5f1fc20997` (head `odin-prototype`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r1` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-odin-prototype.md` + `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (THE canon spec — determinism-native) + `_bmad-output/planning-artifacts/gdds/.../gdd.md` (the engine-agnostic design). No GitHub issue.
- **prior_findings:** none (round 1). CONTEXT: the Godot prototype FYI review (`_bmad-output/perkins/packet-plumber-prototype-build/r1/consolidated.json`, 46 findings on merged #11) — the Odin prototype was built to APPLY those lessons (e.g., field-wise canonical serialization, never raw bytes). Verify the lessons were correctly applied; do NOT re-litigate the Godot findings.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

The **Odin early prototype (Heist 2)** — a re-implementation of the proven-fun Godot design in **Odin + Raylib**, from the Odin architecture (#15). This is the empirical engine A/B (the user compares it to the Godot prototype). Perkins mandate per the job briefing: **"the determinism spine is the ONE hard blocker; otherwise prototype-rigor for the comparison gate, not production-grade."**

Key systems to verify:
- **Determinism spine (THE hard blocker):** the pure-Odin `core/` package (zero vendor/OS imports, compile-enforced), integer-only sim paths, owned PRNG (splitmix64→PCG32 XSH-RR with pinned reference vectors — NOT core:math/rand), SOA pools {slot,gen} ids, array-only iteration, arena discipline, headless-safe. **A seeded run MUST reproduce byte-identical state-hash goldens.** The minion reports: replay bit-exact, replay manifest-matched 2501 ticks. VERIFY this is real.
- **The golden-image harness (§10):** scripted demos (test frames on a virtual clock) → render-to-texture → golden compare (T1 state-hash everywhere + T2 pixel goldens bit-exact via raylib 6.0 rlsw software renderer + PLATFORM_MEMORY) → agent-readable diffs. goldens/{boot,draw_and_reject,flow_basics,qos_dial,surge_basics,error404}/ + .t1 manifests, reported 6/6 green. Verify the goldens are REAL (not tautologies) + the T1 state-hash is a canonical form (field-wise LE, never raw in-memory bytes — the Godot lesson).
- **The fun-test systems:** Topology (terminal→router-only), PacketFlow (BFS, flow by type), QoS (priority lanes + junction triage), Crisis (node strain 🟡→🔴), NetworkHealth (drain/recharge, Error 404 on empty), router port limits (canon #14: basic 4/mid 8/high 16) + router select/triage.
- **Raylib rendering:** light-canvas canon (literal buildings, round capacity-scaled routers, bezier pipes, blue/grey packets), mouse-only, snap-to-node. The 0118cc0 polish: pipe hit-testing follows the rendered bezier, router right-click inspects, HUD font.
- **45 tests + 7 demos green** (reported). Verify they're real.

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

This is an **early prototype for an engine A/B**, not production code. The briefing scoped Perkins as **"prototype-rigor for the comparison gate, not production-grade."**

- **Do NOT flag "not production-grade" / "missing full-game features" as blockers.** The full game (the era tree, the leaderboard/meta backend, mobile, save system) is deliberately NOT built — this is the early prototype slice. The user rulings (lavish session ef5a2724): **desktop-first launch, mouse-only, root layout + game/ removal via a prototype-fun-gate tag, 1-2 juice stings** — these are deliberate, NOT defects.
- **Do NOT flag the choice of Odin/Raylib as "wrong engine."** The Odin pivot is the user's ruling (the whole point of this PR). Do NOT suggest Godot/GDScript/C#.
- **Do NOT flag prototype debt (hardcoded values, stubbed systems, minimal validation) as BLOCKERS** — warnings/notes only. This is an A/B prototype; some debt is expected if the determinism spine + the fun-test loop are correct.
- **Do NOT re-litigate the Godot #11 findings.** Those informed this re-implementation. Verify the lessons were APPLIED (e.g., the serialization is a field-wise canonical form, not the raw-bytes Godot bug).

### Legitimate findings here would be
- **The determinism spine is compromised** — a seeded run does NOT reproduce (byte-identical state-hash goldens fail); the sim is tangled with Raylib rendering; vendor/OS imports leak into `core/`; float nondeterminism in sim paths; unowned PRNG (core:math/rand) used; iteration-order dependence. **This is the ONE hard blocker.**
- **The golden harness is fake** — goldens that don't actually exercise the behavior, tautological compares, the T1 state-hash is raw in-memory bytes (pointers/padding/arena slack — the Godot bug repeated), or the "replay bit-exact" claim is false.
- **A core-loop BUG** — packets don't flow, QoS priority doesn't work, the surge isn't survivable, the port limits (canon #14) aren't enforced, NetworkHealth/Error 404 broken.
- **The committed `app.bin` (2MB binary)** — the 0118cc0 commit added a built binary to the repo. Build artifacts should not be committed (bloats the repo, platform-specific). Verify + flag (likely a blocker-level hygiene issue unless deliberate).
- **A compile/runtime crash** (the prototype doesn't build/run per the briefing's instructions).
- **CI broken** — NOTE: the `.odin-version` pins `dev-2026-08-nightly` (not a valid upstream branch) so the verify job fails to clone Odin. This is a KNOWN issue being fixed separately by the minion — do NOT re-flag as a finding (note it's known).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 17 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/diff.patch`. (This is a LARGE diff — the full Odin prototype. Headless mode handles big-diff chunking.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the Odin architecture + the GDD, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1`), `<lens>.json` + existence check, one retry per failed lens, **big-diff chunking**, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 17 --repo solarity-services/Packet-Plumber --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 17 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** packet-plumber-odin-prototype · **Reviewed sha:** 0118cc0 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  ### Blockers (<n>) / ### Warnings (<n>) / ### Notes (<n>)
  ```
- Close out: `bin/ledger note <your-round-row> "verdict ..."` (Silas owns the row status); remove your worktree (`git worktree remove --force`); close lens panes. Final message: verdict + blocker count + the report path.
