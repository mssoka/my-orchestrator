# Perkins briefing — round 1: packet-plumber-v2-3.2-lane-qos

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/31 (targets `v2`)
- **Reviewed sha:** `7c07a80eb6d8274dc6aa49a4e5d7d8dde92bac7c` (short `7c07a80`)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-3.2-lane-qos-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-3.2-lane-qos.md` + story 3.2 in `_bmad-output/planning-artifacts/sprints/stories-v2.md` + the architecture `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (`[ODN-3]` QoS-inside-Flow, `[E5]` all-zero fallback, `[E6]` never-drop floor, `[E8]` largest-remainder, `[ODN-11]` golden re-bless gate, `[E10]` replay determinism, §11.7). No GitHub issue.
- **prior_findings:** none (this is r1 — the story was dispatch-held for 3.5's file overlap and released on 3.5's APPROVED verdict; the 3.5 branch is APPROVED but UNMERGED — this PR's base does NOT contain 3.5). CONTEXT: the implementing minion's badge-out (core/qos.odin allocator + floor + lane resolution, weight-only demand-free; E5/E6/E8 tests + replay pins; qos_emphasis.dem demo; data/balance.json + palette.json changes; 44 files; **ODN-11 re-bless DELIBERATE + PROVEN**: (a) every existing demo's T2 pixels passed byte-identical against the OLD PNGs before blessing, (b) a reconstruction proof — old catalog_hash spliced into the new state dump — re-derived the blessed flow.dem tick-1 golden exactly; zero sim behavior changed) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Story 3.2 — 3-lane QoS (opens the QoS differentiator):** per-class lanes (E→S→B) with a weight-only allocator (demand is NOT an input) living INSIDE Flow [ODN-3]: all-zero weights fall back to the catalog default preset [E5]; a never-drop class lane is floored and a zeroing edit that would floor it is REJECTED [E6]; the largest-remainder distribution test passes [E8]. Includes the golden T2 of lane proportions changing (blessed deliberately through ODN-11) + the allocator/floor/lane resolution in core + app/render lane emphasis + data balance/palette changes.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 THE ODN-11 RE-BLESS — THE load-bearing invariant (verify the PROOF, don't auto-flag).** The story's own rule says "existing goldens must not shift — if one does, STOP and flag, do not re-bless". The minion DID re-bless — but deliberately, through ODN-11's defined gate, WITH a two-part proof: (a) every existing demo's T2 pixels passed byte-identical against the OLD PNGs (no drift before blessing), and (b) a reconstruction proof — the old catalog_hash spliced into the new state dump — re-derived the blessed flow.dem tick-1 golden exactly (behavioral identity). VERIFY both parts of the proof are real and that zero sim behavior changed. A re-bless WITHOUT a real proof, or with evidence of drift, = a BLOCKER. A proven deliberate re-bless = NOT a finding.
- **🚨 [E5]/[E6]/[E8] EDGE CONTRACTS — load-bearing.** All-zero weights → catalog default preset [E5]; a never-drop class lane is FLOORED and a zeroing edit that would floor it is REJECTED [E6] (the rejection must be test-pinned — neutralize it → the test goes red); largest-remainder distribution passes [E8]. A missing/broken edge contract = a blocker.
- **WEIGHT-ONLY [ODN-3] — demand is NOT an input.** The allocator takes lane weights only; a demand input sneaking into the lane resolution = a real defect. QoS procs live INSIDE Flow (not a peer system) — do NOT flag "QoS not a separate system" (established 3.1 guard).
- **REPLAY DETERMINISM [E10] + LOG_VERSION.** Same seed + same commands → identical map. NOTE: 3.5's LOG_VERSION 2→3 is UNMERGED (approved, waiting on the human) — this PR's base is pre-3.5 v2, so its own version bump is consistent with ITS base. Verify: old logs reject cleanly, replay byte-identical, the version value internally consistent. Do NOT flag "LOG_VERSION collides with the placement branch" — the 3.5-vs-3.2 version collision at merge time is a merge-order concern (Silas flagged it to Gru; the user should merge #30 first), NOT a defect in this PR's code.
- **ZERO SIM BEHAVIOR CHANGE (claimed).** The minion claims the re-bless changed no simulation behavior — verify (drift suite + demo gates + the reconstruction proof). A sim-behavior change riding the re-bless = a blocker.
- **DATA-DRIVEN BALANCE [ODN-5]-adjacent.** data/balance.json + palette.json carry the lane weights/emphasis — data, not hardcoded sim logic. A hardcoded weight where the catalog/balance file should decide = a real defect.
- **No re-open of 3.1 findings** (merged + Perkins-approved) **or 3.5's** (approved round 4916019621, unmerged) — carry-forward only. This PR's diff is reviewed at its own sha (it does not contain 3.5's files).
- **Em-dashes are FINE in Packet-Plumber copy** (the RT CI ban does NOT apply to PP).
- **The base is `v2`** (slices 1–2 + 3.1 merged; the harness #29's Demo_Replay single-source + era-in-log-header semantics are in base; 3.5 is NOT).
- **CONTEXT NOTE (not a finding):** possible bmad-tooling quirk (edits briefly mis-resolving to the main checkout; Silas syncs it). Review the PR content as-is at the sha.

### Legitimate findings here would be
- **A re-bless without a real proof, or with evidence of pixel drift / sim-behavior change** — a blocker [ODN-11].
- **A broken edge contract** ([E5] fallback wrong, [E6] floor-zeroing not rejected, [E8] distribution fails) — a blocker.
- **A demand input in the lane resolution** (weight-only violated) — a blocker [ODN-3].
- **A determinism break** (unseeded draw, command not recorded, LOG_VERSION inconsistency with its own base, old logs not rejected) — a blocker [E10].
- **A hardcoded weight/balance where the data file should decide** — a real defect.
- **An `odin test` / `odin build` / `harness` failure at `7c07a80`** (core incl. E5/E6/E8 pins, demos incl. qos_emphasis, drift, lint).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 31 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `7c07a80`), `spec_files` = this briefing + the job briefing + story 3.2 + the architecture (`[ODN-3]`/`[E5]`/`[E6]`/`[E8]`/`[ODN-11]`/`[E10]`/§11.7), `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-3.2-lane-qos/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 31 --repo solarity-services/Packet-Plumber --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 31 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `7c07a80`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** packet-plumber-v2-3.2-lane-qos / **Reviewed sha:** 7c07a80 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-3.2-lane-qos-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek (kimi's 403 is a false dawn — no k3 flips until the user explicitly says so; never glm-5.2). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
