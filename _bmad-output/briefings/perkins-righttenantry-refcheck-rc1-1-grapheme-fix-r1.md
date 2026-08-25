# Perkins briefing — round 1: righttenantry-refcheck-rc1-1-grapheme-fix

- **PR:** https://github.com/solarity-services/RightTenantry/pull/608 (targets `develop`)
- **Reviewed sha:** `c25201910827ec49f6a58ccad15929b43c64eb32` (short `c252019`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc1-1-grapheme-fix-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc1-1-grapheme-fix.md` + the deferred RC1.1 item in `_bmad-output/implementation-artifacts/spec-rc1-1-grapheme-fix.md` (tracked in-repo) + the DB CHECK constraints (512-codepoint name / 64-codepoint fields) + the write path (request_helpers + consent/payment/submitted callers). GitHub issue: none.
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (server/src/request_helpers.gleam fix + doc contract; 7 new unit tests — emoji UA → exactly 512 codepoints, emoji XFF → 64, ASCII byte-identical, absent → '', short passthrough; /apply write-path integration with emoji UA/XFF persists (200); consent write path stays in bounds; NEGATIVE CONTROL proven — reverting to string.slice makes 2 unit + 2 integration tests fail and /apply returns 500, the exact reported bug; make test green 1484 server + 108 shared + 521 client, integration 501; build/format clean, no let assert; review swarm zero blockers/highs, 2 Low doc findings folded: stale payment_terms_acceptance CHECK citations dropped by the parity migration + mid-grapheme cut intent documented) — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Deferred RC1.1 item — grapheme-slice vs DB CHECK 500 on the write path:** the server sliced user-supplied name/contact strings with `string.slice` (codepoint-based) while the DB enforces a GRAPHEME-aware CHECK (512 codepoints on the name, 64 on the short fields). A string whose codepoint count is under the limit but whose grapheme expansion exceeds it (e.g. emoji with variation selectors/ZWJ) passes the slice but 500s on INSERT. The fix slices at grapheme boundaries in `request_helpers` across the 3 callers (consent/payment/submitted).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 GRAPHEME-BOUNDARY SLICING — THE load-bearing invariant.** The fix must slice at GRAPHEME boundaries (emoji + variation selectors + ZWJ sequences stay intact as one grapheme) — NOT codepoint counts. A slice that still splits a grapheme (a ZWJ family emoji cut mid-sequence, a flag pair split) = a blocker. The DB CHECK is the contract: every accepted value must satisfy it (512/64).
- **🚨 EXACT-BOUNDARY SEMANTICS.** Emoji UA must slice to EXACTLY 512 codepoints (a grapheme that would cross the boundary must be excluded whole, not truncated mid-grapheme); emoji XFF → 64; ASCII must be byte-identical to the old behavior (no regression on plain strings); absent → ''; short values pass through untouched. Any deviation = a real defect. NOTE: the tests assert codepoint counts AFTER slicing (512/64) — verify the grapheme-intactness separately (no lone ZWJ/selector at the cut).
- **ALL 3 CALLERS + THE DB CONSTRAINT.** The fix lives in request_helpers and must cover consent + payment + submitted callers (the 500 happened on /apply). A caller that bypasses the helper (still 500s on a grapheme-heavy input) = a blocker. Verify the DB CHECK constraints are the grapheme-aware ones (512/64) and the fix targets exactly those.
- **NEGATIVE CONTROL REAL.** The claim: reverting to string.slice → 2 unit + 2 integration failures + /apply 500. Verify the tests would actually bite (a neutralized fix goes red). A vacuous pin = a finding.
- **NO REGRESSION.** Format/build clean, no let-assert, server 1484 / shared 108 / client 521 / integration 501 green at the sha. A suite regression = a finding.
- **base = `develop`** (RC1–RC4.3 merged — do NOT re-open their findings; carry-forward only. The rc4-3/rc4-4 in-flight files are NOT touched by this PR — verify no overlap).
- **RT CI: em-dash ban** applies to user-facing copy only — this is server-side slicing; N/A unless copy changed (it didn't).
- **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR content as-is at the sha.

### Legitimate findings here would be
- **A mid-grapheme cut** (ZWJ/selector split at the boundary) — a blocker.
- **A caller bypassing the helper** (still 500s) — a blocker.
- **An off-by-one on the 512/64 boundaries** — a real defect.
- **A vacuous negative control** (revert doesn't go red) — a real defect.
- **An ASCII/absent/passthrough regression** — a real defect.
- **A `make format` / `make build` / `make test-server` / `make test-shared` / integration failure at `c252019`.**

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 608 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc1-1-grapheme-fix/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `c252019`), `spec_files` = this briefing + the job briefing + the spec-rc1-1-grapheme-fix.md, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc1-1-grapheme-fix/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 608 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 608 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `c252019`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc1-1-grapheme-fix / **Reviewed sha:** c252019 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc1-1-grapheme-fix-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek on API access, FULL THROTTLE (no glm cap, no serialization — rounds may run parallel with other rounds). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
