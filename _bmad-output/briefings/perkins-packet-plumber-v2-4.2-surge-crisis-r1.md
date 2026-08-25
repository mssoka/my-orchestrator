# Perkins briefing — round 1: packet-plumber-v2-4.2-surge-crisis

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/36 (targets `v2`)
- **Reviewed sha:** `b94d54f8a010a54316bad5f84f0ac864ee503dda` (short `b94d54f`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r1` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-4.2-surge-crisis.md` + Story 4.2 in `/Users/moses/code/_bmad-output/planning-artifacts/sprints/stories-v2.md` (~line 372) + the GDD crisis sections + architecture `[ODN-4]`/`[ODN-7, REVIEW M1]`/`[E13]`. GitHub issue: none (PP stories live in the sprint doc).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro` — bare `pi` falls to the pi default provider and would run the wrong model. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair):** a data-driven surge archetype in `crises.json` (10× demand spike forecast from the seed, fires on schedule) + the crisis engine: downstream of flow, read-only topology view, dedup by root cause, re-trigger only after `Crisis_Resolved`. Wires with 4.1's forecast panel (names the surge + countdown, engine fires on cue). T1 + event-stream golden (`Crisis_Triggered{Surge}` in the scheduled window).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology.** The engine is downstream of flow and never writes topology (no topology mutation from crisis code — grep the crisis modules for topology writes). A topology write from the crisis path = a blocker.
- **🚨 ODN-7 / REVIEW M1 — Director never reads crisis state** (structural — grep the director for crisis references). A director→crisis read = a blocker.
- **🚨 E13 DEDUP — one crisis per root cause per activation.** Re-trigger only after `Crisis_Resolved`; a duplicate `Crisis_Triggered` for the same root cause without a resolve = a blocker.
- **🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology**; and **no crisis without a resolvable root cause + `preventive_redesign`** (every crisis carries the ref to the topology flaw + what the player could have built). A crisis firing on a healthy topology, or a missing root-cause ref = a blocker.
- **E10 DETERMINISM — same seed → same crisis timeline.** The surge fires on schedule from the seed; selection lives inside the deterministic RNG stream (no new draw, no map-iter in the hot path). A nondeterministic schedule (wall-clock, sim-rng outside the stream) = a blocker.
- **4.1 WIRING — the telegraph becomes true.** The forecast panel names the surge with a countdown; the engine fires it on cue. Verify the wiring actually exists (panel data → engine trigger); "panel exists but the engine never reads it" = a real defect.
- **GOLDEN DISCIPLINE.** New T1 + event-stream golden (`Crisis_Triggered{Surge}` in the scheduled window) blessed deliberately with proof; **existing goldens must NOT shift** — if one shifted, that is a REAL finding (re-bless-without-proof is the trap), not a routine update.
- **SCOPE GUARD.** Surge archetype + engine + root-cause ONLY. NOT 4.3 (Network Health meter / win-lose-retry), NOT the other four crisis archetypes (post-fun-gate), NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it). Out-of-scope content = a finding; do NOT demand features 4.3 would add.
- **BASE = `v2`** (slices 1–3 + harness + 4.1 in). Do NOT re-open settled prior-story findings (3.x / 4.1 / harness — carry-forward only). `correction`-era RT stories don't apply here.
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical — regression-flag any determinism break, but do not re-litigate the settled routing/ECMP/demolish design.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN (a failed command substitution would fall through to the ambient `mssoka` credential and 422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache warnings to stderr, which would corrupt the token and make a good mint look like a failure.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> of 3
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-4.2-surge-crisis-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
