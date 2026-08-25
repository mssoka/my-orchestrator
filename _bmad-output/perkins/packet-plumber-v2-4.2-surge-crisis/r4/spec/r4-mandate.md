# Perkins briefing — round 4: packet-plumber-v2-4.2-surge-crisis (USER-APPROVED CAP OVERRIDE, fix-audit)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/36 (targets `v2`)
- **Reviewed sha:** `f9184fa2de6ab5d8fbd76b957bf2d318834aca8f` (short `f9184fa`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 4 (cap overridden by the user — U1 cap-override doctrine, rc4-3 r5 precedent; Gru ruling 2026-08-13)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r4` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-4.2-surge-crisis.md` + Story 4.2 in `stories-v2.md` (~line 372) + GDD crisis sections + architecture `[ODN-4]`/`[ODN-7, REVIEW M1]`/`[E13]`/`[ODN-14]`/`[ODN-9/10]`. GitHub issue: none.
- **prior_findings:** r3 `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r3/consolidated.json` (fix-audit first, carry-forward markers).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## Round-4 mandate: VERIFY-DON'T-REOPEN on the r3-rework at f9184fa

Commit: "perkins r3: same-tick double-trigger fix, pool-cap clamp, ASCII render gate (B3, W-1/W-2/W-3, N-1..N-13)". The r3 round (4929654425 @ 121d8a0) was CHANGES_REQUESTED with ONE blocker (B3). The user overrode the cap for this verify round. **Verify each claim — the commit message is a claim, not proof. FLAG NEW findings ONLY.**

### (a) B3 — the same-tick double-trigger is structurally closed (THE r3 blocker)
- The post-trigger `continue` is restored in `core/crisis.odin:430-483`: after a successful `crisis_trigger` in (a)/(b), control moves to the next set-piece — the (c) pool backstop is NOT reached on the same tick by the same activation.
- The cooldown-BLOCKED (a) still falls through to (c) (N4's intent survives — verify the fall-through, don't over-restrict).
- The E13 dedup holds: ONE activation = at most ONE Crisis_Triggered; the probe scenario (pool cap 11-14, seed 3003, tick 1200) must now emit exactly one event + one active row. A test pins it (the minion claims 3 new pins — one should be this). A still-reproducible double-trigger at any legal cap = a blocker.
- The probe-verified evidence at the sha is the ground truth (run the probe if needed: pool cap 14, email BE + streaming standard, narrow bottleneck, seed 3003).

### (b) W-1 — the re-bless scope line now names warn.t1
- warn.t1's 300-hash shift (ticks 1201-1500, the margin fix) is named in the re-bless scope with the cause; the unchanged qos.log.bin dropped from the scope list. "Everything else byte-identical" must be TRUE (harness-verified claim — spot-check it).

### (c) W-2 — the pool-cap unresolvable-crisis hole is closed
- Margin clamped for the pool cap AND/OR `pool_max_packets >= 3` validated at catalog load (legal caps 1-2 no longer produce a crisis that can never resolve). A legal cap 1-2 crisis still firing = a finding.

### (d) W-3 — types.odin self-contradiction resolved
- The Event comment no longer claims byte-identity for pre-4.2 streams in the same breath as admitting the +4B fold.

### (e) Notes N-1..N-13 — each either fixed or carried with a real reason
N-12 became lint GATE 6 (the ASCII render-string invariant — verify the gate exists + bites; the minion claims it caught 14 pre-existing mojibake strings). N-13 recorded as accepted-by-design (one-tick latency). Verify the carries. Do not re-raise the r3 21 false-positives or the r2 24 / r1 9.

### (f) DO NOT re-litigate
- r3 verified-FIXED (do not re-open): B1 demolish-and-renumber pin (bites both ways), W-qos root-fix (probe-clean single trigger @1200), W-pool drop-evidence trigger + routed fixture, W-render ASCII (PNG decode clean).
- The held lens-guards (ODN-4 read-only topology, ODN-7 Director isolation, LOG_VERSION 3, determinism, 4.1 wiring) — closed since r1.
- Golden discipline: only surge PNGs re-blessed at this sha (new capture) — everything else byte-identical (harness-verified claim; an undocumented shift = a finding).

## What the PR does (review scope — carried)

**Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair):** data-driven surge archetype in `crises.json` (10× demand spike, fires on schedule from the seed) + the crisis engine (downstream of flow, read-only topology view, dedup by root cause, re-trigger only after `Crisis_Resolved`), wired to 4.1's forecast panel. T1 + event-stream golden. The r3 rework adds: post-trigger guard (B3), pool-cap clamp, ASCII render gate.

## ⚠️ CRITICAL lens-guards (carried — prevents false positives)

- **🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology.** A topology write from the crisis path = a blocker.
- **🚨 ODN-7 / REVIEW M1 — Director never reads crisis state** (structural). A director→crisis read = a blocker.
- **🚨 E13 DEDUP — one crisis per root cause per activation.** Re-trigger only after `Crisis_Resolved`; duplicate `Crisis_Triggered` without a resolve = a blocker (the B3 contract).
- **🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology**; no crisis without a resolvable root cause + `preventive_redesign`.
- **E10 DETERMINISM — same seed → same crisis timeline** (inside the deterministic RNG stream; no new draw, no map-iter in the hot path).
- **4.1 WIRING — the telegraph becomes true** (forecast panel names the surge + countdown; the engine fires it on cue).
- **GOLDEN DISCIPLINE** — new goldens blessed with proof; existing goldens MUST NOT shift without cause documentation.
- **SCOPE GUARD** — surge archetype + engine + root-cause ONLY; NOT 4.3; NOT the other four archetypes; NO new player commands (LOG_VERSION stays 3).
- **BASE = `v2`** — do NOT re-open settled prior-story findings.
- **Em-dashes OK in PP code comments but NOT in draw_text_c-fed render strings** (the mojibake class — N-12 gate territory).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r4/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r4`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
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
  (Round-4 note: the human already overrode the cap for this round; a NEEDS
  CHANGES verdict goes straight to the user.)
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-4.2-surge-crisis-perkins-r4 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
