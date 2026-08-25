# Perkins briefing — round 2 (FIX-AUDIT): righttenantry-refcheck-rc3-7

- **PR:** https://github.com/solarity-services/RightTenantry/pull/603 (targets `develop`)
- **Reviewed sha:** `5576ccbb37f8a1d3cc8196fde7a44b2e71e104c1` (short `5576ccb`; commit "refcheck rc3-7: address Perkins r1 (B1 blocker + W1-W4 + N1-N8)")
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-7-r2` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-7.md` + story RC3.7 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (AD-10, FR-RC12, §6.4, §9.4) + the architecture (`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`: AD-10, §4.2, §4.6/§6, §9.4) + GitHub issue #548 (dump in the r1 dir: `_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/issue-548.json`).
- **prior_findings:** **`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/consolidated.json`** — this is a FIX-AUDIT round. The implementing minion (pTQ) pushed fixes for r1's B1 + W1-W4 + N1-N8 (claims 13/13 addressed). Read `prior_findings` FIRST; verify each is actually fixed at this sha + the load-bearing invariants still hold (no regression). r1 verdict: CHANGES_REQUESTED (1 blocker).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (the fix-audit scope)

The head moved `2bf2577` (r1) → `5576ccb` (this round). The commit message says "address Perkins r1 (B1 blocker + W1-W4 + N1-N8)". **Fix-audit-first** — verify each r1 finding is actually fixed at this sha, THEN a normal pass over the delta for any new issue the fix introduced. The r1 findings to verify (pTQ's claimed fixes in parentheses):

- **B1 (BLOCKER — stamp_creation_fraud wholesale-overwrite):** re-triggering (handle_start/viewed re-fire) wiped submitted fraud_signals because stamp_creation_fraud ran unconditionally (even inserted==0), read ALL rows with no status filter, wholesale SET. **Verify FIXED:** a guard skips stamping when `inserted==0` (or equivalent — a re-trigger must NOT wipe an existing submitted form_session fraud_signals).
- **W1 (DRY — duplicated helpers):** pTQ claims it extracted the duplicated helpers into `reference_checks/fraud_inputs.gleam` (opt_nonempty/opt_to_str/parse_count/parse_int_opt/effective_contact/other_refs_from_rows/cross_application_reuse), with trigger + form_handler both importing them. **Verify FIXED** (and that the extraction is behavior-preserving).
- **W2 (carry_line_type untested):** pTQ claims a 3-branch unit test. **Verify FIXED** (real, passing).
- **W3 (Phase-1 trigger wiring never asserted):** pTQ claims an integration test asserting fraud_signals after run_create_checks (the trigger glue). **Verify FIXED** (real, passing).
- **W4 (advisory gate CONCERNS):** pTQ claims closing W2/W3 lifts P1. Verify the gate is now clean.
- **N1-N8 (the notes):** N1 extra device_fingerprint_match_strength key dropped (AD-10 "exactly these keys" preserved); N2 SQL-stamp mechanism recorded; N3 stale comments fixed; N4 orphaned claim_webhook_event.sql deleted + Squirrel regen; N5/N6 submit test extended to the full form_session block + line_type_from_string round-trip + Unknown fallback; N7 effective_contact Some("")→snapshot fallback; N8 stamp directive TEXT→JSONB. **Verify each** is addressed + correct (not just present) — a wrong "fix" is a NEW finding.

**r1's 2 false-positives (already discarded — do NOT re-flag):** `opt_to_str` is pre-existing in trigger.gleam:1067; `submitted_ip_text`/`submitted_user_agent` are `TEXT NOT NULL DEFAULT ''` (the minion correctly took no action on them).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **Do NOT re-litigate the r1 findings as NEW findings.** B1/W1-W4/N1-N8 are in fix-audit scope — you VERIFY each is fixed (mark "FIXED" with the new code location, or "STILL OPEN" with evidence). A correctly-fixed r1 finding is NOT a round-2 blocker. Only re-flag one if the fix is WRONG/INCOMPLETE or introduced a new defect.
- **AD-10 HONESTY remains load-bearing (carry from r1).** Signals are clues, never fabricated detections, never verdicts; they never auto-reject or alter a score; v2-reserved signals emit `unknown`/`null`/`absent` exactly. The B1 guard fix touches the stamping path — verify it doesn't break the honesty contract (a skipped stamp must leave the honest state, not a fabricated one).
- **§4.2 boundary (raw IP/UA internal-only) + `referee_number_wrong` superseded + innocent-reuse != fraud** — carry from r1; only flag if the fix delta touched them.
- **Regression guard:** the r1-confirmed invariants (AD-10 honesty exact, superseded slug, §4.2 boundary, innocent-reuse) + the full test suite must still pass at `5576ccb` (r1: 1458 unit / 488 integration-skip; pTQ reports 1465 unit / 491 integration). A fix that regressed a test = a NEW finding.

### Legitimate round-2 findings would be
- An r1 finding (B1/W1-W4/N1-N8) **still open or wrongly fixed** at `5576ccb` (re-flag, mark "not fixed in r2").
- A **new defect the fix introduced** (e.g. the B1 guard breaks honest stamping for legitimately-new rows; the DRY extraction changed behavior; the JSONB change breaks a query).
- A regression in the r1-confirmed invariants or tests.
- A `make test` / `make build` / migration failure at `5576ccb`.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 603 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `5576ccb`), `spec_files` = this briefing + the job briefing + RC3.7/FR-RC12/AD-10/§6.4/§9.4 + the architecture (AD-10, §4.2, §4.6/§6, §9.4) + issue #548, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2`, `prior_findings` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/consolidated.json` (fix-audit-first: verify r1 B1+W1-W4+N1-N8 addressed, then delta pass). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 603 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 603 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `5576ccb`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 2 of 3 (FIX-AUDIT)` / **Job:** righttenantry-refcheck-rc3-7 / **Reviewed sha:** 5576ccb / **Fix-audit:** r1 B1+W1-W4+N1-N8 (FIXED|STILL OPEN per item) / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-7-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `zai-coding-cn/glm-5.2`** — kimi quota is DOWN this billing cycle (confirmed 403 on k3); glm-5.2 is the sanctioned Perkins fallback. **BURST WARNING (proven, mitigation VALIDATED):** stagger the lens spawns (wave-1 ≤4 → wave-2 rest) keeps peak glm concurrency ≤6 and avoids the ZAI 429 entirely (validated 3 rounds this evening, zero 429s). No other glm panes are active right now, but stagger anyway per the validated pattern. If a lens 429s, one continue revives it.
