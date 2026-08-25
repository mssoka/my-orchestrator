# Perkins briefing — round 2: righttenantry-refcheck-rc4-4 (FIX-AUDIT)

- **PR:** https://github.com/solarity-services/RightTenantry/pull/609 (targets `develop`)
- **Reviewed sha:** `8e48605930a90e7319ddcc7024544016aa88073a` (short `8e48605`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3 (r1 = CHANGES_REQUESTED 4928115400 @ 1a3839c)
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-4-r2` — detached at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-4.md` + Story RC4.4 in the epic (~line 692) + UX §7.6/§7.9/OQ-5 + `AR-RC13`. GitHub issue: none.
- **prior_findings:** r1 `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r1/consolidated.json` (fix-audit first, carry-forward markers).
- **Model:** `deepseek/deepseek-v4-pro` (Perkins reasoning tier). Launch EVERY lens pane with `pi --model deepseek/deepseek-v4-pro`. NEVER glm-5.2 (retired).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## Round-2 mandate: verify the r1-rework claims at 8e48605

Commit: "fix(refcheck): RC4.4 r1 — post-correction cadence restart latches once; lifecycle-line survival, legacy terminal fallback, label/scan/pin gaps". Verify EACH r1 finding — the commit message is a claim, not proof.

### (a) B1 — cadence restart latches ONCE (verify the mechanism)
- build_send_entries (application_detail_handler.gleam ~1356-1387): the fold now carries a `restarted` flag / post-restart position — ONLY the first batch strictly after `corrected_at` resets to 0; later post-correction batches do NOT re-fire the restart.
- `attempt_log_restarts_cadence_after_correction_test` extended with ≥2 post-correction batches, pinning co_nudge + reminder ordinals (the r1 one-batch test gap is closed). Corrected rows' post-correction co_nudge + reminders must NOT render as "Invitation sent" with empty detail.
- B1 closed ONLY if the latch is real AND the ≥2-batch pin bites (neutralizing the latch turns it red).

### (b) B2 — test gate now PASSES (verify each pin)
- OQ-5 export toast pinned: firing arms + verbatim copy ("Attempt log copied — paste it into your records or a message.").
- 3 of 5 terminal writers' `terminalized_at` stamps have integration assertions (terminalize refused/objected, exhaust, sweep_mark_failed — a dropped stamp turns red).

### (c) W1-W8 (verify each; fixed-or-carried-with-reason)
W1 kind-blind same-`at` collapse restricted to send kinds + boundary test (lifecycle/terminal lines survive) · W2 legacy terminal fallback skips `updated_at` when `taken_over_at` set · W3 failed/`completed` rows get consistent labels (timeline vs export) · W4 queued taken-over rows keep the export affordance (§7.7 export-beside-the-chips — the RC4.3 regression is closed) · W5 em-dash enforcement covers the new surface ("Closed — no reply" fixed; the nine new consts on a scan list; no em-dash in implementer-authored strings) · W6 skipped co_nudge has no dangling " — " and keeps its skip reason · W7 OQ-5 toast pinned (see B2) · W8 stamps pinned (see B2).

### (d) N1-N13 — each either fixed or explicitly carried with a real reason. Verify the carries. FLAG NEW findings ONLY.

### (e) DO NOT re-litigate
- r1 VERIFIED-CLEAN: AR-RC13 server-built timeline (no client re-derivation), codec completeness 5/5, expand-only migration, §7.9 bodies verbatim, preference matrix, no-duplicate-terminals pin, back-compat decode.
- The 2 r1 false-positives (chunk-boundary artifact + covered-decode claim) — do not re-raise.
- RC4.1/4.2/4.3 mechanisms are settled (TOCTOU/correct/substitute) — verify only that this story's dispatch wiring doesn't break them.

## What the PR does (review scope — carried from r1)

**RC4.4 — attempt-log timeline, export & notification completeness** (32 files at r1; r1-rework adds the cadence latch + the W1-W8 fixes): deferred RC2.1 codec (FIVE reference_* variants + codec arms + dropdown icon match); §7.6 server-built attempt-log timeline (typed, server-ordered, RFC3339-normalized, cadence restart after corrections); Export (plain-text clipboard + verbatim OQ-5 toast); notification completeness (§7.9 bodies verbatim as pure builders + preference-matrix + no-duplicate-terminals pins); expand-only migration (substituted_at + terminalized_at).

## ⚠️ CRITICAL lens-guards (carried from r1 — prevents false positives)

- **🚨 AR-RC13 LOAD-BEARING — server-built timeline, NO client re-derivation.** A client-side re-derivation/re-sort of event state = a blocker.
- **🚨 CODEC COMPLETENESS — every emitted reference_* notification decodes** (an emitted variant without a decode arm = the bell-breaks blocker class).
- **🚨 EXPAND-ONLY MIGRATION** — back-compat decodes must still work (old payload WITHOUT the new keys decodes).
- **🚨 NOTIFICATION COMPLETENESS — §7.9 verbatim + preference matrix + no-duplicate-terminals pins** (a missing pin or duplicated terminal = a blocker).
- **VERBATIM TOAST (OQ-5)** — exact copy, by-construction em-dash-free; verify the toast fires with the exact copy at the right arms.
- **RT em-dash ban APPLIES** to all other implementer-authored user-facing strings (check new strings + composition sites by hand).
- **Timeline correctness** — every event class present; cadence restarts exactly once per correction.
- **base = `develop`** (RC4.1/4.2/4.3 merged — carry-forward only).
- **a11y + AC testids** on the new timeline/export UI.
- **bmad-quirk heads-up (context, not a finding):** review the PR content as-is at the sha.

## Standing orders (from the playbook — verbatim)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job briefing** and **GitHub issue** (your spec), and your cwd — a detached worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first: `gh pr diff <pr>` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2/diff.patch`. Every lens reviews these identical bytes. (Absolute path — the round worktree is destroyed at close-out, so artifacts live in the orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = the original job briefing + the GitHub issue (dump it with `gh issue view <n> --json title,body,comments` into the round dir first), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2`, and `prior_findings` = the previous round's `consolidated.json` when N > 1 (re-review: fix audit first, carry-forward markers). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, and writing `consolidated.json`. Its verdict thresholds are yours below. You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — capture STDOUT ONLY. NEVER append `2>&1`.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment <pr> --body-file <body.md>`, note `fallback-comment` in your ledger note, and call it out in your final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review <pr> --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N> of 3
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  After round 3, the human takes over._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc4-4-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
