# Perkins briefing — round 2: packet-plumber-v2-4.2-surge-crisis (FIX-AUDIT)

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/36 (targets `v2`)
- **Reviewed sha:** `f906725c1f2be8911903ecb951c6ad0a44859e22` (short `f906725`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 2 of 3 (r1 = CHANGES_REQUESTED 4925630979 @ b94d54f)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r2` — detached at exactly the reviewed sha. Trust it, not `origin/v2`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-4.2-surge-crisis.md` + Story 4.2 in `/Users/moses/code/_bmad-output/planning-artifacts/sprints/stories-v2.md` (~line 372) + the GDD crisis sections + architecture `[ODN-4]`/`[ODN-7, REVIEW M1]`/`[E13]`/`[ODN-14]`. GitHub issue: none (PP stories live in the sprint doc).
- **prior_findings:** r1 `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r1/consolidated.json` (fix-audit first, carry-forward markers).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro` — bare `pi` falls to the pi default provider. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## Round-2 mandate: verify the r1-rework claims at f906725

Commit: "perkins r1: stable crisis identity, frozen attribution restore, drop-site input, test-gate pins (B1/B2, W1-W7)". Verify EACH r1 finding against the code — the commit message is a claim, not proof.

### (a) B1 — Active_Crisis identity is now STABLE (verify the mechanism)
- `Active_Crisis.bundle` no longer stores the compaction-prone slot index — keyed on the canonical `(bundle_lo, bundle_hi)` node pair or the E11-stable member pipe id, with the bundle slot resolved at eval time (`bundles_slot_for_pair` / `bundle_of_pipe`).
- A mid-crisis topology edit (demolish a FULL bundle whose slot precedes the crisis's bundle) must NOT: spuriously `Crisis_Resolved` while the flaw is still saturated, re-trigger same-tick (E13 chatter), mislabel the banner/bottleneck outline.
- The resolve test must exercise the demolish-and-renumber scenario (not pass by fixture symmetry). B1 closed ONLY if the renumber-proof identity is real and pinned by a test that bites.

### (b) B2 — test gate now PASSES (verify each pin)
- Settled-scan POSITIVE test: queue at bound, no same-tick drop → `crisis_find_saturated_bundle` ok=true branch executes.
- Backward-tick latch test (`tick < state.tick` rejected; `tick == state.tick` behavior asserted — r1 N1).
- Byte-layout pins extended: drop-payload target byte + tags 8/9 + the crises section (not just tags 1–7).

### (c) W1-W7 (verify each; fixed-or-carried-with-reason, no auto-flag)
W1 pool backstop class-filter vs frozen "ANY Pool_Exhaustion" (filter dropped OR frozen text amended) · W2 surge.dem now includes the mid-run capacity fix + `Crisis_Resolved` pin in the launchable golden · W3 byte-identity promise amended (spec-4-2:30 + types.odin:279 + serialize.odin:358 — drop payload is +4B, change-log admits) · W4 trigger attribution matches the pinned slot-order definition (or the frozen block amended) · W5 wrong-typed `archetype_id` type-asserted (`json.String`; key present but non-string → named load error, ODN-5) · W6 drop-site input moved off the ODN-14 event buffer (per-tick drop-site field on `Flow_State` or equivalent) · W7 replay-test leak fixed (no leaks under the tracking allocator).

### (d) N1-N13 — each either fixed or explicitly carried with a reason. Verify the carries are REAL (code matches the claim). FLAG NEW findings ONLY.

### (e) DO NOT re-litigate
- The r1 lens-guards that HELD: crisis engine read-only on topology (ODN-4), Director never reads crisis state (ODN-7/M1 structural signature), LOG_VERSION stays 3, determinism spine, 4.1 wiring (shared set-piece schedule).
- The 9 r1 false-positives (details in r1 consolidated.json) — do not re-raise.
- **Golden discipline:** r1 verified the golden shifts clean (catalog_hash fold + drop-payload byte; warn/qos @65s T2s cause-documented; zero-traffic T2s untouched). Any NEW golden shift in this rework MUST have cause-documented proof — a re-bless without proof = a finding.

## What the PR does (review scope — carried from r1)

**Story 4.2 — Surge SetPiece + Crisis Engine (root-cause, fair):** a data-driven surge archetype in `crises.json` (10× demand spike forecast from the seed, fires on schedule) + the crisis engine: downstream of flow, read-only topology view, dedup by root cause, re-trigger only after `Crisis_Resolved`. Wires with 4.1's forecast panel (names the surge + countdown, engine fires on cue). T1 + event-stream golden (`Crisis_Triggered{Surge}` in the scheduled window). The r1 rework adds: stable crisis identity, frozen-attribution restore, drop-site input, test-gate pins.

## ⚠️ CRITICAL lens-guards (carried from r1 — prevents false positives)

- **🚨 ODN-4 LOAD-BEARING — crisis engine READ-ONLY on topology.** No topology mutation from crisis code. A topology write from the crisis path = a blocker.
- **🚨 ODN-7 / REVIEW M1 — Director never reads crisis state** (structural). A director→crisis read = a blocker.
- **🚨 E13 DEDUP — one crisis per root cause per activation.** Re-trigger only after `Crisis_Resolved`; duplicate `Crisis_Triggered` without a resolve = a blocker (this is the B1 contract — verify the identity mechanism holds it under topology edits).
- **🚨 AC-E13 FAIRNESS — no crisis on a healthy within-capacity topology**; no crisis without a resolvable root cause + `preventive_redesign`.
- **E10 DETERMINISM — same seed → same crisis timeline.** Fires on schedule from the seed; selection inside the deterministic RNG stream (no new draw, no map-iter in the hot path).
- **4.1 WIRING — the telegraph becomes true.** Forecast panel names the surge with a countdown; the engine fires it on cue.
- **GOLDEN DISCIPLINE.** New T1 + event-stream golden blessed deliberately with proof; **existing goldens must NOT shift without cause documentation** — an undocumented shift = a REAL finding.
- **SCOPE GUARD.** Surge archetype + engine + root-cause ONLY. NOT 4.3 (Network Health / win-lose-retry), NOT the other four archetypes, NO new player commands (LOG_VERSION stays 3 — a bump without a flag = flag it).
- **BASE = `v2`** (slices 1–3 + harness + 4.1 in). Do NOT re-open settled prior-story findings (carry-forward only).
- **Em-dashes are OK in PP** (the RT ban does not apply).
- **Determinism spine reminder:** per-hop forwarding, T1 hash rides every serialized state, replay byte-identical — regression-flag any determinism break, but do not re-litigate the settled routing/ECMP/demolish design.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
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
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-4.2-surge-crisis-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
