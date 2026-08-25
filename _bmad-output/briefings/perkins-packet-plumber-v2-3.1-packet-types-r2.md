# Perkins briefing — round 2: packet-plumber-v2-3.1-packet-types

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/28 (targets `v2`)
- **Reviewed sha:** `abe578b00c13c468331c2c0fc33caa4ae435f7c1` (short `abe578b`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.1-packet-types-r2` — detached at exactly the reviewed sha. **r2 of the SAME PR (r1 = NEEDS CHANGES, 13/13 confirmed findings ALL addressed in a980194 + the abe578b rebase — verify the fixes, do NOT re-open the findings).**
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-3.1-packet-types.md` + Story 3.1 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` (full card line 233 + slice-3 framing line 228) + §3 of `_bmad-output/planning-artifacts/sprints/sprint-plan-v1.md` (the v1 demand model: `PressurePlan`/`DemandSpec`/`SetPiece`, §3.3 the dst-distribution pinned test) + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[ODN-5]` catalogs, `[ODN-7]` director, `[ODN-3]` QoS-inside-Flow, `[E10]` replay, §11.7; ODN-1 core-engine-free) + GDD E2.1/E2.4. No GitHub issue.
- **prior_findings:** r1 review 4914400407 (13/17 confirmed, 4 FP incl. the empirically-falsified 'era never written' blocker). ALL 13 were addressed in a980194 + the abe578b rebase — VERIFY each fix landed (the minion's map: P0 -> 46-row table-driven catalog_test.odin; color_rgba !okc; pre-cast lane/weight range checks; i32 tick validation; demand_weight bounds; weighted_pick_excluding suite; bad_era drift mutation w/ divergence assertion; duplicate-era fail-fast; jint_strict; aprintf'd T2 fails; demolishes-free loaders; corrected weighted_pick comment; qos.dem convention) — do NOT re-open the findings as new; a missing/wrong fix = a finding. CONTEXT (r2): the minion's rebase badge-out (qos_fixture folded into #29's Demo_Replay single-source refactor — now in base v2; superseded per-piece loaders dropped; era stays in the log header — the drift pin depends on that semantic; fixture on|off|qos merged into one directive; ecmp/demolish captures re-blessed for the catalog-hash fold + class-0 render; 61 core / 9 demos bit-for-bit / 62 drift mutations / lint 5/5) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**v2 Story 3.1 — Packet types + the demand director (OPENS SLICE 3, the QoS differentiator).** Two packet types (**email** low/low/low + **streaming** med/med/high) with distinct shapes/icons (never color alone — accessibility), spawned per a demand plan via the `scripted_plan_pressure` director, with **seeded weighted-random destination selection**. Replaces slice 1's trivial 1-packet `flow_seed_demand` with the real demand model (ported Odin-native from v1 §3: `PressurePlan`/`DemandSpec`/`SetPiece`). New `packet_types` catalog; the director emits a `PressurePlan` per source-class with typed source/sink selectors + weighted dst. 3.2 (lanes), 3.3 (contention), 3.4 (SLA) build on this.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 DISTINCT SHAPES, NOT COLOR ALONE — THE accessibility invariant.** email + streaming MUST be visually distinguishable by SHAPE/icon (color is secondary). The lens-guard checks the render isn't color-only (a colorblind player must still tell them apart). A render that differentiates by color alone = a REAL blocker (accessibility).
- **🚨 SPAWN DETERMINISM [E10] — load-bearing.** The `(class, src, dst)` spawn sequence is byte-identical for a fixed seed. The dst selection is **seeded WEIGHTED_RANDOM** — it uses the run's RNG **inside the deterministic RNG stream** (no new/unseeded draw; same discipline as ECMP: no map-iter in the hot path, array-indexed). A determinism break (an unseeded draw, a `state.rng` mutation outside the stream, a map iteration in the spawn/dst path) = a blocker. Verify the §3.3 dst-distribution pinned test is real + the era-3 QoS golden replays bit-for-bit.
- **CATALOGS INTEGER-ONLY + FAIL-FAST [ODN-5].** Sim values are integers; the `packet_types` loader validates + **fails fast on bad data** (NO silent defaults on malformed JSON). A silent-default path or a non-integer sim value in the catalog = a real defect.
- **DIRECTOR READ-ONLY ON TOPOLOGY [ODN-7].** `scripted_plan_pressure` takes a read-only topology view and EMITS a `PressurePlan` — no mutation of the topology. A director that mutates topology = a blocker.
- **QOS PROCS INSIDE FLOW [ODN-3]** — the QoS procs live inside Flow (not a peer system). Don't flag "QoS not a separate system" — that's the design (slice-3 framing; 3.1 sets up the data, 3.2 adds the lane logic).
- **round_robin DELIBERATELY DROPPED (routing-ruling lens-guard).** Load-balancing (round-robin/weighted-LB) is BANNED by the locked routing model — the weighted-random dst selection is the DESIGN. Do NOT flag "missing round-robin" — its absence is correct. (ECMP, 2.2, is a hash; the demand director's weighted-random is a spawn-time dst pick, both deliberate.)
- **T2 PIXEL DEBT CLOSED — goldens VERIFIED + blessed by the merged harness (#29, now in base v2).** Do NOT re-litigate golden pixel content — the harness re-diff ran (bundle/flow/draw/win/lose matched bit-for-bit; ecmp/demolish first-blessed) and #29 was Perkins-APPROVED. A golden CHANGE in THIS PR would be a finding; golden files as-is are the blessed contract.
- **DEMO_REPLAY SINGLE-SOURCE FOLD (from #29's merge — base, NOT this PR).** Run setup now flows through #29's Demo_Replay single-source refactor; this PR's qos_fixture folds into it (demo_apply_setup seeds identically in live + replay). Do NOT flag 'qos fixture not loaded separately' — the fold is the merged design.
- **ERA RIDES THE LOG HEADER — load-bearing (drift-pin semantic).** Replay applies header.era; the log is authoritative, NOT the demo file. The drift bad_era divergence pin depends on exactly this. Do NOT flag 'era not in the demo file' — that's the design.
- **APP ERA-0 UNTIL THE ERA-FSM STORY (flagged, NOT a defect).** The app still renders era 0; the era-FSM is a later story. Do NOT flag "app doesn't show era 3" — the data/director/golden are this story's scope.
- **CORE ENGINE-FREE (ODN-1)** — the packet_types catalog + director live in `package core`; zero engine imports (the shape/icon render lives in `app/render`).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–2 complete), not `main`.
- **The prototype is REFERENCE-ONLY** (mine its packet-type shapes/icons + demand model DESIGN; rebuild the logic clean).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas synced it). Review the PR content as-is at the sha.
- **Do NOT re-open 1.1–2.3 findings** (merged, Perkins-verified) — carry-forward only.

### Legitimate findings here would be
- **A color-only differentiation** (no distinct shape/icon per packet type) — a blocker (accessibility).
- **A spawn/dst determinism break** (unseeded or extra RNG draw; map-iter in the hot path; the weighted-random not inside the deterministic stream) — a blocker [E10].
- **A silent-default catalog path** (malformed JSON → default instead of fail-fast) or a non-integer sim value — a real defect [ODN-5].
- **A director that mutates topology** — a blocker [ODN-7].
- **An engine type leaking into `package core`** (ODN-1) — a blocker.
- **The §3.3 dst-distribution test missing/fake** (the pinned test).
- An `odin test` / `odin build` / `harness` failure at `37f5581`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 28 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `abe578b`), `spec_files` = this briefing + the job briefing + Story 3.1 + sprint-plan §3 + the architecture (`[ODN-5]`/`[ODN-7]`/`[ODN-3]`/`[E10]`/§11.7/ODN-1) + GDD E2.1/E2.4, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.1-packet-types/r2`, `prior_findings` = the r1 review (4914400407) — verify the 13 fixes, don't re-open. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 28 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 28 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `37f5581`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 2 of 3` / **Job:** packet-plumber-v2-3.1-packet-types / **Reviewed sha:** 37f5581 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-3.1-packet-types-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `kimi-coding/k3`** — the permanent policy for Perkins (reasoning roles; the frontier reviewer). kimi was restored this morning (credits topped up, verified live). If a lens 403s (a residual quota edge), one continue may revive it; if the round hard-fails on 403, self-report `blocked` — Silas redirects to the deepseek interim.
