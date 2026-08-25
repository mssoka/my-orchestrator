# Perkins round 1 — packet-plumber-v2-5.12-aggregation-groups

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/68 (PR #68)
**Reviewed sha:** `035c73327677645860ffd3f9b894faec92816169`
**repo_root:** /Users/moses/code/packet-plumber (repo `packet-plumber`, base `v2`)
**Round:** 1 (fresh PR) · **CAP LIFTED (user ruling 2026-08-17): rounds run until APPROVED** · **Model:** `kimi-coding/k3` (HOLD LIFTED 08-18 late evening — reasoning resumed k3; probed OK 00:08Z) — **FALLBACKS in order: zai-coding-cn/glm-5.3 (down till ~06:48Z 1308 cap) → deepseek/deepseek-v4-pro → deepseek/deepseek-v4-flash.**
**STATUS: LIVE — r1 on the fresh sha.**
**prior_findings:** none (fresh PR).
**Spec files:**
- Original job briefing: /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.12-aggregation-groups.md
- Story card: `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 5.12 (in-repo)
- PR body: `_bmad-output/pr-bodies/5.12.md`
- 5.11 context (the roster this builds on): _bmad-output/briefings/perkins-packet-plumber-v2-5.11-terminal-types-r4.md

---

## Perkins standing orders

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff <pr>` →
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (dump it with `gh issue view <n> --json
  title,body,comments` into the round dir first), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` when N > 1.
  The headless mode owns: pane mechanics (dedicated tab,
  `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence
  check, one retry per failed lens, big-diff chunking, the mandatory
  verification pass, consolidation, and writing `consolidated.json`. Its
  verdict thresholds are yours below. You MUST close every lens pane
  before finishing.
- **LENS ROOTING (MANDATORY — the 08-18 mis-rooted class):** every lens
  tab MUST be created with `herdr tab create --cwd <this round worktree>`
  — the lens panes root at the round worktree, NEVER at the orchestrator
  root or the repo main checkout. A lens pane whose cwd is not the round
  worktree is mis-rooted: close + relaunch it.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT
    approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then
  review — never run gh with an empty GH_TOKEN (a failed command
  substitution would fall through to the ambient `mssoka` credential and
  422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` —
     capture STDOUT ONLY. NEVER append `2>&1` (stderr cache warnings would
     corrupt the token).
  2. Check for an EMPTY token, NOT `$?`:
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr>
     --body-file <body.md>`, note `fallback-comment` in your ledger note,
     and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file
     <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> (cap lifted — loop until approved)
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start (round id: `packet-plumber-v2-5.12-aggregation-groups-perkins-r1`); final
  message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

---

## r1 guards (round-specific — fresh PR, the aggregation-groups canon)

**The ONE hard blocker class — the estates ruling is honored WITHOUT
breaking the determinism spine:**

- **The estates ruling (user 2026-08-17 night — canon):** terminals
  cluster into estates — majority clustered, minority isolated, NOT 100%.
  The bias is a SOFT preference: `bias_prob_permille 750` in
  balance.json (data-driven, fail-fast validated at load), a bias coin per
  rejection-sampling attempt, and the biased candidate still faces the
  FULL E31 test; rejection-sampling unchanged; the uplink is never forced.
  VERIFY: (a) the bias is genuinely inside the E31 envelope (a biased
  draw can fail E31 and fall back); (b) it is NOT a hard 100% cluster
  (the ruling's "NOT 100%" is load-bearing — check the measured majority
  vs the isolated minority on the pinned seed); (c) the draw counts are
  pure functions of state — replay byte-identical [E10].
- **The derived estate view is PURE and NEVER serialized:** union-find
  under radius adjacency, seed-derived, no LOG_VERSION bump. Verify the
  view isn't persisted and doesn't touch the serialization/replay path
  (the 5.4/5.8 derive-don't-record discipline).
- **Group-scoped demand weight [ODN-7]:** an estate member's source-pick
  weight scales as `1000 + (size-1) * member_weight_permille` (250) —
  aggregate group demand rises as members join. Verify the math + the
  concentration pin (estate >= 750 per-mille vs the no-bonus control —
  non-vacuous; the r3/N5 lesson: a literal that silently stops biting on
  re-tune is a defect).
- **The surge is an aggregation event at the group uplink:** crisis
  naming updated ("Add a parallel pipe or a higher tier on the group
  uplink's path"), the shed happens at the shared uplink — never on the
  estate's own access. Verify the crisis test pins the uplink bundle.
- **The deliberate re-bless is cause-partitioned:** fold-check PASS
  (17d3baf8 → febe2afc, era-0 tick-1 shift = the catalog fold alone), all
  33 pre-existing .log.bin fold-only (bytes 17–24), T2 shifts partitioned
  (6 banner-copy + 7 growth-map frames + 1 new estate_surge.dem;
  everything else byte-identical). Verify the partition mechanically
  (byte-compare the .log.bin set vs v2; PNG diff on the non-partition
  frames) and that the new T2 golden was vision-verified (estate cluster
  + red-outlined uplink + banner naming the group uplink — the 7.1
  golden discipline).
- **The adversarial catches landed:** the Odin block-scoped defer
  use-after-free on the view and the /1000 truncation that silently
  neutralized the weight for weight-1 terminals — verify BOTH fixes are
  in the tree (the use-after-free class is the r3 double-free's sibling:
  check it isn't masked by the tracking allocator).
- **5 new pins non-vacuous:** estates + isolated spawns on seed 9
  (radius-connected compactness + E31 audit) · pure view/scale units ·
  weight concentration · surge sheds at the shared uplink · E10 replay
  spine with both live. Mutation-check at least the weight and the
  surge-shed pins.

**What NOT to re-litigate:** the 5.11 roster + era gates + W9 honest pin
(4-round approved); the #65 sprite canon (lavish-APPROVED); the 5.9/5.10
accumulator contracts; the fair-crisis grown-mesh start map; the estates
ruling itself (a user decision — the question is whether the CODE honors
it, not whether it's right); the fold-check harness (N11 of 5.11 — done);
the fallback-model caveat.

**Verdict severity:** cap lifted — if the bias is soft + E31-respecting,
the view is pure, the weight math + pins bite, the surge names the
uplink, and the re-bless partition is exact, APPROVE. Warnings ≠
blockers.

**CI note:** GitHub Actions on Packet-Plumber is org-billing-blocked
(runners never start — the retired-caveat class) — NOT a signal; the
local suite is ground truth (minion reports 10/10 gates, 199 tests,
34-demo harness + replay, drift 240/240, input parity 24/24).
