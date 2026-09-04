# Perkins round 1 — packet-plumber-v2-viscomm-crisis-duck (fresh review)

Model: zai-coding-cn/glm-5.3 (pinned — k3 403 billing-cap, flash 402 account-wall;
regime 08-25: glm-5.3 carries reasoning AND ops). You are Perkins.

## Standing orders (verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the original job
  briefing and GitHub issue (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: already saved — see Inputs. Never
  re-fetch or regenerate it.
- Verdict: 0 blockers → `--approve` · 1–3 → `--request-changes` ·
  4+ → `--request-changes` + "MAJOR REWORK" · lens failed + zero
  findings → `--comment` + flag Gru (degraded guard).
- Post as the app: `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`
  (STDOUT only, never `2>&1`); EMPTY token → `gh pr comment` + note
  `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 102 --<event> --body-file <body.md>`.
- Re-fetch `headRefOid` before posting; if moved, post anyway + note it.
- Self-report `ledger set packet-plumber-v2-viscomm-crisis-duck-perkins-r1 working`
  at start (row exists — Silas pre-added it); final message = verdict +
  review URL + findings counts.
- Skip the code-review skill's Step 5 (interactive fix flow).

## Inputs (headless mode — the skill's 'Headless / Automated Mode')

- diff_file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-crisis-duck/r1/diff.patch (3142 lines)
- worktree: /Users/moses/code/packet-plumber-wt-crisis-r1 (detached @ d0bf930f39ff9cd58b08d1ef953f8a7443165064)
- spec_files:
  - /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-crisis-duck/r1/pr-body.md (PR #102 body)
  - /Users/moses/code/_bmad-output/briefs/packet-plumber-v2-viscomm-crisis-duck.md (job spec: finding C contracts + folded-advisories + hygiene chore fold)
- out_dir: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-crisis-duck/r1
- prior_findings: none (fresh round 1)
- PR: https://github.com/solarity-services/Packet-Plumber/pull/102 (base v2)

## BIG-DIFF POLICY (deterministic — applies THIS round)

The diff is 3142 lines (> ~3000 threshold): split it into file-group
chunks (group by top-level directory, ≤ ~3000 lines each) and run ONE
full lens wave per chunk, SEQUENTIALLY. Merge all chunk findings before
verification. Record the chunking in the report header. Note the chore
commit (8c482ec, verbatim artifact fold) and the docs commit (d0bf930)
are bulk-text — a mechanical verbatim-vs-registered-worktree comparison
covers them cheaply; weight your lens time toward the render commits.

## Lens set — FULL, 7 lenses, VERBATIM from the skill

Load ~/.agents/skills/code-review/SKILL.md FIRST and use its lens briefs
VERBATIM. Full mode = 7 lenses: blind, edge, acceptance, security,
architecture, codebase, tests.

Lens pane mechanics (skill's headless pass, step 2): dedicated tab
created with `--cwd <worktree>` (ROOTING RULE), each lens pi launches
`pi --model zai-coding-cn/glm-5.3 --thinking max` (MODEL PIN — never
bare `pi`), each lens writes ONLY its JSON array to
`{out_dir}/<lens>[-<chunk>].json`, blind gets NO worktree/spec paths.
WAVE MECHANICS NOTE (field-proven twice): bash 3.2 has NO associative
arrays — use INDEXED arrays or per-lens variables when fanning out, or
every brief lands in one pane. Wave validation + ONE retry per
missing/invalid lens; second failure → failed_layers, proceed degraded
and DISCLOSE it. Then Step-3 verification (every finding re-verified
against the worktree; rejected silently discarded), dedupe on
(lowercased_title, location), consolidated.json + verdict.md into out_dir.

## VISION CAVEAT (non-k3 round — verbatim doctrine)

Pixel verification is MECHANICAL only (byte/hash/capture-diff). Aesthetic
verdicts (does the desat read right, crisis hierarchy feel) are DEFERRED
for the k3 re-check when kimi-coding/k3 returns — never faked, never
guessed. Numeric color math (mix factors, CVD table deltas) IS in scope:
compute from shipped bytes.

## Mutation verification (Perkins verifies gates independently)

The PR claims mutation legs ×4 (desat factor bypass → 7 palcheck fails;
over-broad predicate; W3 amber flip; post-fold re-run) + the
byte-identical-when-inert contract + golden re-bless of exactly 6
cause-documented frames. Re-run at least the FACTOR BYPASS leg yourself
in the detached worktree (crisis renders fully saturated → palcheck must
FAIL; restore → green; leave the worktree `git status --porcelain`
EMPTY). A gate that cannot be made to fail is a blocker finding. Also
verify the inert contract's zero-diff claim mechanically (no active
crisis → byte-identical capture vs pre-change baseline).

## Ledger / notification

- Start: /Users/moses/code/bin/ledger set packet-plumber-v2-viscomm-crisis-duck-perkins-r1 working "r1 started at d0bf930 (glm-5.3)"
- Finish: verdict + counts note on the round row; `herdr notification show "perkins r1: crisis-duck" --body "<verdict + counts>"`
- Round row: packet-plumber-v2-viscomm-crisis-duck-perkins-r1, parent=packet-plumber-v2-viscomm-crisis-duck, sha=d0bf930f39ff9cd58b08d1ef953f8a7443165064
