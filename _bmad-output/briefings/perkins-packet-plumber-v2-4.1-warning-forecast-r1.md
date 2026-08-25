# Perkins briefing — round 1: packet-plumber-v2-4.1-warning-forecast

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/35 (targets `v2`)
- **Reviewed sha:** `9820a55e0541d8d7b5e114f9a486726e4df83141` (short `9820a55`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.1-warning-forecast-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-4.1-warning-forecast.md` + story 4.1 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[E9]` contention bound, `[E10]` replay, `[ODN-11]` golden re-bless gate, §11.7). No GitHub issue.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (core/warnings.odin: warning_evaluate after flow before win/lose — node strain = stuck-packet backlog (Packet.waiting_ticks, a NEW serialized field; a healthy transit never strains — the no-flicker contract) ÷ node throughput; pipe pressure = fullest lane vs its E9 bound (lone packet 17% healthy, lane at bound 100% = dropping); forecast = era set-pieces in [start−lead, start+duration) with exact countdowns — reads the schedule, never fires; Crisis_State on Run_State derived/tick, absent-when-empty T1; Warning_Raised/Cleared events tags 6/7; balance.json warnings block (70/90 ladder, 30s/10s/20s leads, fail-fast); render: health rings + !/!! glyphs (tick-derived pulse, never color alone), pressure halos, WEATHER REPORT panel (shared app/harness, zero pixels when empty); era-3 sandbox session (goal/cap 0 — win/lose is 4.3's); 97 core (6 new warning pins incl. exact event streams + replay byte-identity) / 14 demos + replay / 97 drift / lint 5/5; LOG_VERSION stays 3; re-bless deliberate (catalog_hash fold mechanical + T2 telegraph shifts cause-documented per demo; boot/draw/flow/win/bundle/ecmp/place/demolish T2s byte-identical — negative proof)) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Story 4.1 — Warning signs + forecast (slice 4 opener):** a warning/forecast system — node strain (waiting_ticks backlog ÷ throughput), pipe pressure (fullest lane vs E9 bound), and a set-piece forecast (reads the schedule, exact countdowns, never fires). `Crisis_State` derived per tick (absent-when-empty T1); `Warning_Raised`/`Warning_Cleared` events (tags 6/7, sign+target); health rings + pressure halos + a WEATHER REPORT panel; an era-3 sandbox launchable.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 THE ODN-11 RE-BLESS — verify the CAUSE-DOCUMENTATION, don't auto-flag.** Re-blessed deliberately: (a) catalog_hash fold — mechanical (new balance.json warnings block); (b) T2 telegraph shifts — cause-documented PER DEMO; negative proof claimed: boot/draw/flow/win/bundle/ecmp/place/demolish T2s byte-identical. VERIFY the negative proof (those demos' T2 pixels unchanged) + the cause-docs. A re-bless with an unaccounted shift = a BLOCKER.
- **🚨 THE NO-FLICKER CONTRACT — load-bearing.** Node strain uses `Packet.waiting_ticks` (a NEW serialized field — packets that failed a forward attempt); a HEALTHY transit must NEVER strain. A flicker (a healthy node flashing a warning) or a strain signal without a real backlog = a blocker. Also: `waiting_ticks` is NEW SERIALIZED STATE — verify LOG_VERSION stays 3 (the claim) and old-log acceptance is intact [E10]; if the new field changed the log format, that's a blocker.
- **PIPE PRESSURE vs [E9].** Pressure = fullest lane ÷ its E9 bound (the 3.3 ladder's bound). Verify it reads the E9 bound correctly (a lane at bound = 100% = dropping). A pressure computation disconnected from the real E9 bound = a real defect.
- **FORECAST READS THE SCHEDULE, NEVER FIRES.** The forecast derives from era set-pieces in [start−lead, start+duration) with exact countdowns — it must be PURE (no state mutation, no side effects). A forecast that mutates state or fires events = a blocker.
- **EVENTS TAGS 6/7 + SIGN/TARGET.** Warning_Raised/Cleared with sign+target, tag-conditional payload like the 3.3/3.4 events; replay byte-identity pinned. A broken tag or a payload that breaks replay = a real defect.
- **NEVER COLOR ALONE.** Health rings + !/!! glyphs + tick-derived pulse — the warning render must be distinguishable without color (the accessibility invariant from 3.1). A color-only warning render = a blocker.
- **WEATHER REPORT PANEL — ZERO PIXELS WHEN EMPTY.** The panel is shared app/harness and renders nothing when no warnings are active. A panel that draws pixels while empty = a real defect.
- **ERA-3 SANDBOX (goal/cap 0 — win/lose is 4.3's).** The sandbox session intentionally has no win/lose. Do NOT flag "win/lose not implemented" — 4.3 owns it. The launchable must still be launchable + the demos honest.
- **No re-open of slice-1..3.4 findings** (merged + Perkins-approved; 3.3's re-bless proven; 3.4's proven zero-T2-pixels) — carry-forward only.
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–3 + 3.5 + 3.2–3.4 + canon).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

### Legitimate findings here would be
- **A re-bless with an unaccounted shift or a broken negative proof** — a blocker [ODN-11].
- **A healthy-transit strain (flicker)** — a blocker (no-flicker contract).
- **A LOG_VERSION bump or old-log breakage from waiting_ticks** — a blocker [E10].
- **A forecast that fires/mutates** — a blocker.
- **A color-only warning render** — a blocker (accessibility).
- **A pressure computation disconnected from the E9 bound** — a real defect.
- **An `odin test` / `odin build` / `harness` failure at `9820a55`** (core 97, demos 14 incl. warn.dem, drift 97, lint 5/5).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 35 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `9820a55`), `spec_files` = this briefing + the job briefing + story 4.1 + the architecture (`[E9]`/`[E10]`/`[ODN-11]`/§11.7), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.1-warning-forecast/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 35 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 35 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `9820a55`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-4.1-warning-forecast / **Reviewed sha:** 9820a55 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-4.1-warning-forecast-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek on API access, FULL THROTTLE (no glm cap, no serialization — rounds may run parallel with other rounds). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
