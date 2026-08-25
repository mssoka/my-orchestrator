# Perkins briefing — packet-plumber-ue-bootstrap r1

- **Job:** packet-plumber-ue-bootstrap · **Round:** 1 (loop-until-APPROVED budget)
- **PR:** https://github.com/solarity-services/Packet-Plumber-UE/pull/1 (UE 5.8 scaffold, MCP wiring, determinism spine port, research report)
- **Reviewed sha:** `836f44e38989f83c50b936e02a01d1c584efcbfe7` (head of `bootstrap`, base `main` — a NEW repo's first PR)
- **repo_root:** `/Users/moses/code/packet-plumber-ue` · **Your cwd:** detached worktree at exactly the reviewed sha — trust it, not `origin/main`
- **Spec pointers:** original job briefing `/Users/moses/code/_bmad-output/briefings/packet-plumber-ue-bootstrap.md` + the PR body's Decisions & rationale + the PP canon (the game design + routing canon [RR] + determinism rules [ODN-*] carry over as requirements — the Odin repo's GDD/spine are the spec).
- **Model:** zai-coding-cn/glm-5.3 (standing reasoning primary; probed OK at dispatch). Lens mega-minions: name the model explicitly at every spawn (`zai-coding-cn/glm-5.3` — the MODEL PIN, resolve from this briefing, never bare) + `--thinking max` + PIN `--cwd <this worktree>` on every lens tab.

## Lens-guards

- **ONE hard blocker class — the determinism spine port (the canon
  surface):** the UE scaffold must carry the PP determinism spine as
  REQUIREMENTS — seeded RNG, state hash, replay equality (the v2 slice-1
  equivalent) via Unreal AutomationTests + a commandlet entry runnable
  headlessly. The shipped golden (docs/goldens/probe-seed42-ticks100.json)
  is the first pin — verify the golden file exists + the test skeleton
  actually asserts against it. The spine port is the reason this repo
  exists; a scaffold that defers or abstracts the determinism contract =
  blocker.
- **Scaffold audit:** 48 files — Source/**, Config/, scripts/ (local-ci.sh
  with engine-free vs engine-gated gates + docs/timings.md), tests/, docs/,
  AGENTS.md, README.md, .mcp.json, .gitignore/.gitattributes (the LFS/
  uasset strategy — decided explicitly per the briefing), .clang-format.
  The local CI's engine-free gates (format/spine/static) must be green at
  this sha; the engine-gated gates (build/headless/probe/golden) activate
  on engine presence with documented timing expectations (first build
  30-60min+ — NOT a defect at this sha; the engine isn't installed yet —
  that's a documented manual step awaiting the user).
- **MCP wiring:** .mcp.json + the plugin config — the official 5.8 MCP
  plugin path (and/or the UE-MCP community option per the user's ruling).
  Verify the wiring is real (config present, documented drive commands:
  editor, assets, builds, screenshots) — an agent command must be able to
  drive the editor once the engine lands.
- **The research report** (the lavish-reviewed gate — 4 user rulings: UE-MCP
  ✓, 3 slices ✓, install now ✓, LFS ✓): do NOT re-litigate the rulings;
  verify the report's substance (5.9 timeline + AI features, MCP landscape,
  determinism-in-UE analysis vs Odin's spine, comparison criteria, slice-1
  scope, upgrade path — cited sources) is accurately reflected in the repo
  docs.
- **What NOT to re-litigate:** the user's 4 lavish rulings; the game design
  (same game, second engine — the PP GDD is canon); the engine choice
  (comparison track, evidence-based).
- **What to flag for verification:** the .gitignore/.gitattributes LFS
  strategy is explicit; the AGENTS.md + project-context are present with
  build commands + conventions; the .clang-format is configured; the
  headless commandlet + AutomationTest skeleton are real (not stubs); the
  golden pin is wired into a test.
- **CI note:** GitHub Actions is billing-blocked (the standing class).
  Local suite is ground truth — the engine-free gates at minimum (the
  engine-gated loop runs when the user completes the UE download).

## Perkins standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 1` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-bootstrap/r1/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the original job briefing, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-ue-bootstrap/r1`, no `prior_findings` (r1). Headless mode owns pane mechanics, the `<lens>.json` output contract, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and `consolidated.json`. Visual checks: verify MECHANICALLY first (byte/hash/capture-diff); when a visual judgment is unavoidable, run the `vision-read` skill on `lmstudio/qwen/qwen3.8-27b` — never trust a text-only model's eye. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 blockers → `--request-changes`; 4+ → `--request-changes`, body leads with "MAJOR REWORK". **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — STDOUT ONLY, never `2>&1` (stderr cache warnings corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → mint failed; fall back to `gh pr comment 1 --body-file <body.md>`, note `fallback-comment` in your ledger note, call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 1 --<event> --body-file <body.md>`
- Body format: `## 🤖 Perkins automated review — round 1 of 3` header (loop-until-APPROVED), Job, Reviewed sha, Reviewers x/7, Verification counts, Blockers/Warnings/Notes sections, Reviewer agreement, Verdict line, "_Address findings and push — I re-review automatically on the new sha._"
- Before posting, re-fetch `headRefOid` (gh pr view 1 --json headRefOid). If it moved mid-review, post anyway but note "reviewed <old>, head now <new> — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set packet-plumber-ue-bootstrap-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
