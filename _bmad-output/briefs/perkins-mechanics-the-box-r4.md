# Perkins round: packet-plumber-v2-mechanics-the-box-perkins-r4

**PR:** https://github.com/solarity-services/Packet-Plumber/pull/107 (number 107)
**Reviewed sha:** 6e3a3c8db4f4a18da235f5a729043d59cbfd96ed (re-fetch headRefOid before posting; if moved, post anyway + note)
**Repo root:** /Users/moses/code/packet-plumber · **Your cwd:** your detached round worktree at exactly the reviewed sha
**Spec:** the original job briefing /Users/moses/code/_bmad-output/briefs/packet-plumber-v2-mechanics-the-box.md + the ratified design record
/Users/moses/code/implementation-artifacts/mechanics-quinn-2026-08-27.md (or /Users/moses/code/_bmad-output/implementation-artifacts/mechanics-quinn-2026-08-27.md)
**Round dir:** /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-mechanics-the-box/r4/
**prior_findings:** /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-mechanics-the-box/r3/consolidated.json — FIX-DELTA ROUND: fix-audit first (each r3 finding resolved / still-open / superseded), then delta review.
**Model:** zai-coding-cn/glm-5.3-flash (natively multimodal; pixel measurements decide). Bash 3.2 — NO arrays in wave scripts.

## R3 → R4 context

r3 (review 5051378887, 6/7 lenses, blind disclosed) found 4 blockers: (B1) balance gate VACUOUS — `check_reject_balance` omits the `crises` source; all 79 rows reject trivially; the 2^40 row could never match (`jint_strict` i32 overflow); mutation-proven. (B2) 11 of 27 conflicted goldens resolved with STALE pre-rebase bytes (pulse absent; commit message false for them) — named: a11y_protan/a11y_reduced/a11y_scale/a11y_tritan/advance_block_sla/health_lose/juice/qos_emphasis/sla/surge/warn at their beats. (B3) `goldens/a11y_reduced/30000ms.png` = uniform BLACK frame (min=0,max=0) masking a real failure. (B4) ruling-1 wiring ZERO coverage (no row references `app_start_era()`/`advance_gate_enabled`). Plus 4 warnings (box_check_* box-on untested; place-refusal toast branch untested; crisis-stall gate manual-only; PR body over-claims ×3 + stale L5 econ table). Root-cause census: TWO blessing machines with R/B-swapped raster conventions blessed the two lanes; directive = settle the corpus on ONE machine.

The rework commit claims: golden corpus settled (one machine), balance fail-fast table REBUILT, ruling-wiring coverage added, PR body corrected.

## USER RULINGS in force (unchanged; review implementation only)

1. `APP_START_ERA = 1` ships; 6.2 advance gate live in start_run; `APP_ERA=3` = PP_DEBUG override only.
2. Goldens LOCAL-canon: byte-exact local-only; CI = environment-blind subset (`--skip-raster`, `palcheck --structural`, drift) — no byte-exact raster in CI.
3. Saves disposable PLAIN; stamp idea = one-line deferred-work note, no code.

## Your r4 mandates (re-run / verify INDEPENDENTLY)

- **B1**: the rebuilt balance table must be mutation-usable — pick 2 rows and PROVE they fail when their expected rule is mutated (RED), then restore (GREEN); confirm `crises` is a real source (no trivial-branch rejection); confirm no i32-overflow dead rows (the 2^40 case re-expressed so it can actually match, or dropped with the bound enforced elsewhere).
- **B2**: blob-verify all 11 named goldens are now byte-fresh from the MERGED tree (pulse present) — machine-convention census: the ENTIRE committed corpus must carry ONE raster convention (count the R/B-swapped stragglers; any straggler = finding).
- **B3**: `a11y_reduced/30000ms.png` is no longer solid black (min/max check) AND the beat's content matches the merged render lane's reduced-motion output.
- **B4**: rows referencing `app_start_era()`/`advance_gate_enabled` EXIST and FAIL on revert (mutation: revert the era-1 start in a scratch → the row goes RED).
- Warnings: box_check_* box-on pin, place-refusal toast row, crisis-stall automated row, PR-body corrections (the 3 over-claims fixed; L5 econ table matches the shipped build) — each verified or still-open.
- Fix-audit: every r3 finding itemized.
- Minion-claimed sweep at 6e3a3c8: re-run what is cheap (suites, drift, fold-check, econ-check), trust nothing.

CI context: billing-block signature (0 steps) — note-only, NOT a gate. MEGA-DIFF shape: full PR ~180k cumulative lines; THIS round's canonical diff = `git diff 0431813..6e3a3c8` (~88,825 lines) — overwhelmingly the one-machine golden re-settle. CHUNK: full lens attention on the CODE chunk (odin/md/json, small); the PNG bulk gets MECHANICAL blob verification (convention census, black-frame scan, pulse-presence spot PIL checks on the named beats) — chunk, never drop; disclose the shape.

Self-report: `/Users/moses/code/bin/ledger set packet-plumber-v2-mechanics-the-box-perkins-r4 working` at start; final message = verdict + review URL + findings counts. Round row already exists — work it, do not create one.

---

## Standing orders (paste verbatim)

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
  orchestrator's `_bmad-output`.) **[r4 note: gh pr diff is API-capped
  on this MEGA-DIFF PR. Save the delta canonically as `git diff
  0431813..6e3a3c8` (~88,825 lines, mostly the one-machine golden
  re-settle). Chunk: code chunk gets the full lens wave; PNG bulk gets
  mechanical blob verification. Disclose the shape.]**
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (here: no issue; use the briefing + the
  record + this briefing's rulings), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` (fix audit
  first, carry-forward markers). The headless mode owns: pane mechanics
  (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output
  contract + existence check, one retry per failed lens, big-diff
  chunking, the mandatory verification pass, consolidation, and writing
  `consolidated.json`. Its verdict thresholds are yours below.
  **Lens-spawn rooting (user-approved 2026-08-18):** the headless spawn
  template pins `--cwd <worktree>` on every lens tab FOREVER — a lens
  pane whose cwd is not the round worktree is mis-rooted: close +
  relaunch with `--cwd`.
  **Empty-lens doctrine (2026-08-18/19):** acceptance/architecture
  lenses back 3-byte-EMPTY a THIRD straight generation → sweep those
  lens panes + regenerate (intervene — an empty-lens verdict never
  ships); a g-wave COMPENSATION verdict (a subset of lenses delivering a
  valid verdict) counts as valid.
  Visual checks (goldens, sprites): verify MECHANICALLY first
  (byte/hash/capture-diff); your model is natively multimodal — vision
  is INLINE for screening, but pixel measurements decide, never a bare
  visual impression. Never fake a measurement.
  You MUST close every lens pane before finishing.
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
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)` —
     capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache
     warnings to stderr, which would corrupt the token and make a good
     mint look like a failure.
  2. Check for an EMPTY token, NOT `$?` (an intervening command can
     clobber `$?`, and a `2>&1` capture makes it lie — the 2026-08-09
     rc3-2 round posted a fallback-comment instead of a formal approve
     on exactly this):
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment
     <pr> --body-file <body.md>`, note `fallback-comment` in your ledger
     note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr>
     --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N>
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  The loop runs until an APPROVED verdict._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.
