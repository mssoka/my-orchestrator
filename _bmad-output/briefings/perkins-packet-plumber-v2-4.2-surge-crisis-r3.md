# Perkins briefing — round 3: packet-plumber-v2-4.2-surge-crisis (FINAL automated round, FIX-AUDIT)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/36 (targets `v2`)
- **Reviewed sha:** `121d8a07420ad9fc8638f33664d631a77fb5b90a` (short `121d8a0`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 3 of 3 — **FINAL automated round** (after this: the human takes over)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r3` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-4.2-surge-crisis.md` + Story 4.2 in `stories-v2.md` (~line 372) + GDD crisis sections + architecture `[ODN-4]`/`[ODN-7, REVIEW M1]`/`[E13]`/`[ODN-14]`/`[ODN-9/10]`. GitHub issue: none.
- **prior_findings:** r2 `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/consolidated.json` (fix-audit first, carry-forward markers).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## Round-3 mandate: verify the r2-rework claims at 121d8a0

Commit: "perkins r2: renumber-proof test, qos churn root fix, pool under-fire fix, mojibake fix (B1, W-qos/W-pool/W-render)". Verify EACH r2 finding — the commit message is a claim, not proof.

### (a) B1 — the demolish-and-renumber pin now EXISTS and bites (the r2 blocker)
- The resolve test: crisis active on pair P at slot 1, demolish a FULL bundle at slot 0 mid-crisis, rebuild renumbers P to slot 0 → assert the crisis STAYS active, still names P, no spurious `Crisis_Resolved`, no same-tick re-trigger, banner/outline still correct.
- Neutralizing the renumber-proof identity (or the test's demolish) turns it red. A vacuous or symmetry-preserving fixture = B1 stays open.
- surge.dem @2381 pair-gone branch: the banner-GONE T2 bracket @119500ms now pins the resolve/re-fire cycle visually (no longer T1-only).

### (b) W-qos — churn disclosed AND/OR root-fixed
- The @1200 trigger → same-tick `Crisis_Resolved` b0 + `Crisis_Triggered` b1 @1201 churn (probe-verified at r2): either the change-log now discloses it accurately AND the re-bless scope is corrected (only qos.t1 moved; log + PNGs byte-identical), OR a trigger confirmation delay / root fix removed the churn. A still-undisclosed churn contradicting "one trigger per activation" = a real defect.

### (c) W-pool — drop-evidence trigger with anti-flap guard + routed fixture
- Pool_Exhaustion triggers on the E22 drop evidence (admission-time) with the eval-time check as the anti-flap guard — NOT the eval-time-only check that under-fired in delivering networks.
- A routed-network pool fixture (pipes delivering, pool shedding) pins the map-wide crisis naming.

### (d) W3-carry + W-render
- types.odin:293 amended to match serialize.odin/change-log (the +4B drop-payload fold); the frozen Events bullet marked superseded (human renegotiation noted).
- Both banner title strings use ASCII (the mojibake em-dash replaced) — verify NO non-ASCII runes in the draw_text_c-fed strings (the file header's own warning class); the re-blessed T2 captures render clean glyphs.

### (e) Notes — each either fixed or explicitly carried with a real reason
B2-3 pin depth (size-only → byte-level or fixed message) · W5 branches (absent-key + wrong-typed pinned) · pool marginal regime · surge.dem T2 bracket (see (a)) · N4 restructured (cooldown-blocked cause no longer skips alternative causes past the pool backstop — verify the per-path `continue` is actually gone) · N2/N7 explicit recorded reasons · frozen-text residues marked superseded. Verify the carries. FLAG NEW findings ONLY.

### (f) DO NOT re-litigate
- r1/r2 VERIFIED: B2 settled-scan positive + backward-tick latch + equal-tick, W1 class filter dropped, W2 surge.dem demolish/resolve/relief, W4 slot-order + qos.t1 cause, W5 json.String assert, W6 flow.drop_sites (ODN-14 buffer no longer an engine input), W7 replay leak, N1/N3/N5/N6/N8/N9/N10/N11/N12.
- The 24 r2 false-positives + 2 r1 false-positives — do not re-raise.
- Held lens-guards (ODN-4 read-only topology, ODN-7 Director isolation, LOG_VERSION 3, determinism, 4.1 wiring) — the r1/r2 guards that held stay closed.
- **Round 3 of 3: this is the final automated review.** If the verdict is NEEDS CHANGES, the relay will go straight to the human — be exhaustive but fair: only REAL defects block.

## What the PR does (review scope — carried from r1/r2)

**Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair):** data-driven surge archetype in `crises.json` (10× demand spike, fires on schedule from the seed) + the crisis engine (downstream of flow, read-only topology view, dedup by root cause, re-trigger only after `Crisis_Resolved`), wired to 4.1's forecast panel. T1 + event-stream golden. The r2 rework adds: renumber-proof identity test, qos churn root fix/disclosure, pool drop-evidence trigger, mojibake fix.

## ⚠️ CRITICAL lens-guards (carried from r1/r2 — prevents false positives)

- **🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology.** A topology write from the crisis path = a blocker.
- **🚨 ODN-7 / REVIEW M1 — Director never reads crisis state** (structural). A director→crisis read = a blocker.
- **🚨 E13 DEDUP — one crisis per root cause per activation.** Re-trigger only after `Crisis_Resolved`; duplicate `Crisis_Triggered` without a resolve = a blocker (the B1 contract — the identity mechanism must hold it under topology edits).
- **🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology**; no crisis without a resolvable root cause + `preventive_redesign`.
- **E10 DETERMINISM — same seed → same crisis timeline** (inside the deterministic RNG stream; no new draw, no map-iter in the hot path).
- **4.1 WIRING — the telegraph becomes true** (forecast panel names the surge + countdown; the engine fires it on cue).
- **GOLDEN DISCIPLINE** — new goldens blessed with proof; existing goldens MUST NOT shift without cause documentation (an undocumented shift = a REAL finding).
- **SCOPE GUARD** — surge archetype + engine + root-cause ONLY; NOT 4.3; NOT the other four archetypes; NO new player commands (LOG_VERSION stays 3 unless flagged).
- **BASE = `v2`** — do NOT re-open settled prior-story findings (carry-forward only).
- **Em-dashes are OK in PP code comments but NOT in draw_text_c-fed render strings** (the mojibake class — non-ASCII in byte-truncated render paths).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r3/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r3`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
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
  (Round-3 note: this IS round 3 — if NEEDS CHANGES, the human takes over per the cap.)
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-4.2-surge-crisis-perkins-r3 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
