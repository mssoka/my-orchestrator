# Perkins briefing — packet-plumber-wire-aesthetics r1

- **Job:** packet-plumber-wire-aesthetics · **Round:** 1 (of the loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/70 (Story 7.5: wire aesthetics — routing + junction shaping, shipped as routing-only infrastructure)
- **Reviewed sha:** `2aaaa255490f02f9507ef8aabf2ff6aa5cdbe499` (head of `wire-aesthetics`, base `v2`)
- **repo_root:** `/Users/moses/code/packet-plumber` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/v2`
- **Spec pointers:** the original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-wire-aesthetics.md` (canon context: 7.1 light-canvas language, D9 map, 5.12 estates; lane note: view-lane, T2 handshake) — no GitHub issue exists for this job; canon fold lives in `stories-v2.md` (§Story 7.5 card) + `decision-log.md` (2026-08-19 entry).
- **Model:** kimi k3 (reasoning tier; probed OK 08:14Z + 08:36Z). Lens mega-minions: name the model explicitly at every spawn per the code-review skill's headless template — and PIN `--cwd <this worktree>` on every lens tab (mis-rooted lenses = Gru-contamination + dead panes; the 08-18 class).

## Lens-guards (standard since 2026-08-08)

- **ONE hard blocker class — the cost-immunity spine:** cost MUST stay on the LOGICAL geometry; the detour/routing machinery is presentation-only and must never change gameplay, connect/anchor/cap semantics, or cost. The shipped pin suite (`wire_path_test.odin`, 6 tests) includes a **negative-controlled** cost-immunity pin (phantom +3 detour span → red 390 vs 300) and determinism pins (same map → same paths; routed frame rendered twice → identical SHA-256). A regression here = real blocker.
- **Gate verdict C (user ruling 2026-08-19, the lavish gate):** "Ship pure straight (routing OFF, anchors OFF) — Story 7.5 becomes routing-only infrastructure." The diff ships the machinery OFF by default — the game render is byte-identical to the pre-7.5 straight look, and **no re-bless was performed** (goldens unchanged; 34/34 demos pass on committed goldens). Routing/anchors OFF by default is the DESIGN, not a defect — do NOT flag "feature not visible".
- **What NOT to re-litigate:** the 08-17 "want it" ruling (detours + junction shaping are wanted), the 08-19 gate verdict C, the shipped flags-off state, canon rulings already applied (7.1 light-canvas, D9 map, 5.12 estates).
- **What to flag for verification:** the canon fold (stories-v2.md §7.5 + decision-log 2026-08-19) matches the diff; the harness `wire-preview` gate tool + preview-check gate; T1/T2/replay pass with **zero golden churn**; determinism claim (render twice → same hash) actually reproducible in-tree.
- **CI note:** GitHub Actions is billing-blocked today (runners never start — "log not found"). The LOCAL suite is ground truth: `tools/ci-local.sh --mac` 10/10 (the minion ran it; re-run if you need to verify). CI-red on GitHub ≠ code instability.

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 70` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1`, no `prior_findings` (r1). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 70 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 70 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 1 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 70 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-wire-aesthetics-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
