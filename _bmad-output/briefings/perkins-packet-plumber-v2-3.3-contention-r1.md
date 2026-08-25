# Perkins briefing — round 1: packet-plumber-v2-3.3-contention

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/32 (targets `v2`)
- **Reviewed sha:** `ffc9b7b91c1719e98c696b898d62fbc55436a314` (short `ffc9b7b`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.3-contention-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-3.3-contention.md` + story 3.3 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[ODN-3]` QoS-in-Flow, `[E7]` no-starvation floor, `[E9]` contention ladder, `[E22]` pool backstop, `[E10]` replay, `[ODN-11]` golden re-bless gate, §11.7) + the CANON COMMITS (both merged into base v2): `2e3acab` (QoS lanes SPATIAL — user ruling) + `8ece056` (no auto-assigned lanes + lane-speed visibility — user ruling). No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (qos_serialize pure cyclic-WRR service inside flow_step — packets queue per (bundle, lane), exit Express → Standard → Best, work-conserving gap-fill + E7 floor; E9 contention ladder at admission (a full lane queue sheds the lowest-priority non-empty lane's newest; the arriving packet drops when it is the target); E22 pool backstop with the strict-priority rule (an Express resident never pays for a Standard arrival); Packet_Dropped{class,reason} events tag-conditional — LOG_VERSION stays 3, no new commands, zero new serialized state (queues/lanes/budgets all derived); spatial-lane canon built in (3 painted strokes width=WFQ share, in-lane riding end-to-end at lane speed, default Standard — game never assigns lanes); qos_contention.dem launchable (pipe 0 oversubscribed ~2.4×); 84 core tests (E7/E9-all-21-combos/E22/double-shed/lone-packet keystone) / 12 demos + replay gate / 83 drift / lint 5/5; re-bless DOCUMENTED with 3 reasons; review swarm (2 hunters): 1 blocker + 5 warnings all fixed + pinned) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Story 3.3 — Contention (the QoS differentiator's teeth):** a cyclic-WRR serialization service inside Flow — packets queue per (bundle, lane) and exit Express → Standard → Best-effort with work-conserving gap-fill and the E7 no-starvation floor (a lone packet in ANY lane still crosses at full capacity — the light demos' transits are pinned unchanged). E9 contention ladder at admission (a full lane queue sheds the lowest-priority non-empty lane's NEWEST; the arriving packet drops when it IS the target). E22 pool backstop with the strict-priority rule (an Express resident never pays for a Standard arrival). `Packet_Dropped{class, reason}` events (tag-conditional payload — LOG_VERSION stays 3, no new commands, zero new serialized state: queues/lanes/budgets are all derived). Plus the two canon rulings' visuals: three painted lane strokes per pipe (width = WFQ allocation share), packets ride their lane end-to-end AT LANE SPEED (Express streaks / Standard cruises / Best-effort crawls), and the game NEVER auto-assigns lanes — every packet type rides Standard until the player categorizes it (default pipe = plain-router behavior).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 THE ODN-11 RE-BLESS — THE load-bearing invariant (verify the REASONS, don't auto-flag).** The minion re-blessed goldens DELIBERATELY with THREE documented reasons: (a) catalog_hash header drift — new `balance.json` keys (the 3.2 precedent); (b) the canon T2 repaint (all pipe demos — spatial lanes); (c) genuine contention shifts in qos/qos_emphasis/ecmp. VERIFY each reason holds at the byte level: the light demos (non-contention) must show ZERO sim change (pinned transit tests), and the STOP-and-flag discipline must be honored (reasons in the PR, no silent re-bless). A re-bless whose documented reason doesn't hold, or evidence of unaccounted drift = a BLOCKER.
- **🚨 SPATIAL-LANE CANON (2e3acab + 8ece056 — BOTH MERGED INTO BASE v2, user rulings 2026-08-12).** Three painted lane strokes per pipe; stroke width = WFQ allocation share; packets ride IN their lane (lateral offset) end-to-end AT LANE SPEED (Express streaks, Standard cruises, Best-effort crawls/slips gaps). **NO auto-assigned QoS lanes** — every packet type rides Standard until the player categorizes it (per-type/per-pipe override); the game NEVER assigns lanes; default pipe = all traffic on Standard (plain router). A render that assigns lanes, lacks the lane strokes, or mis-maps lane position/speed = a real defect. Do NOT flag "uncategorized packets are all on Standard" — that's the design.
- **🚨 [E9] CONTENTION LADDER — load-bearing.** A full lane queue sheds the lowest-priority non-empty lane's NEWEST packet; the arriving packet drops when it is the target. All 21 combos must be test-pinned. A shed that hits the wrong lane/priority, or a drop when a shed was possible = a blocker.
- **🚨 [E22] POOL BACKSTOP — strict-priority rule.** An Express resident NEVER pays for a Standard arrival (the inversion catch). A priority inversion (lower-class arrival evicting a higher-class resident) = a blocker.
- **[E7] NO-STARVATION FLOOR.** Work-conserving gap-fill; a lone packet in ANY lane crosses at full capacity. Starvation under continuous Express = a blocker. The light demos' transits unchanged (pinned) — verify the pins are real.
- **SERIALIZATION / REPLAY [E10].** LOG_VERSION stays 3 (events are tag-conditional; zero new serialized state). Same seed + same commands → identical map; `Packet_Dropped` events replay byte-identically. A serialization change that bumps state shape (or breaks old-log acceptance) WITHOUT the documented mechanism = a blocker.
- **Zero new serialized state (claimed).** Queues/lanes/budgets are DERIVED — verify no hidden serialized field crept in.
- **No re-open of 3.1/3.2 findings** (merged + Perkins-approved; 3.2's re-bless proven independently) — carry-forward only. The canon commits are IN BASE (reviewed as canon, not as this PR's findings).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–3 + harness + 3.5 + 3.2 + both canon commits).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

### Legitimate findings here would be
- **A re-bless with an unproven/unaccounted reason, or evidence of unaccounted drift** — a blocker [ODN-11].
- **A canon violation** (auto-assigned lanes, missing lane strokes, wrong lane-speed mapping, no lateral offset) — a blocker [2e3acab/8ece056].
- **An E9 ladder error** (wrong shed target/priority, missing drop) — a blocker.
- **An E22 priority inversion** — a blocker.
- **E7 starvation or a broken lone-packet pin** — a blocker.
- **A serialized-state change without the tag-conditional mechanism** — a blocker [E10].
- **An `odin test` / `odin build` / `harness` failure at `ffc9b7b`** (core 84, demos 12 incl. qos_contention, drift 83, lint 5/5).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 32 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `ffc9b7b`), `spec_files` = this briefing + the job briefing + story 3.3 + the architecture (`[ODN-3]`/`[E7]`/`[E9]`/`[E22]`/`[ODN-11]`/`[E10]`/§11.7) + the two canon commits, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.3-contention/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 32 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 32 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `ffc9b7b`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-3.3-contention / **Reviewed sha:** ffc9b7b / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-3.3-contention-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek on API access, FULL THROTTLE (no glm cap, no serialization — rounds may run parallel with other rounds). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
