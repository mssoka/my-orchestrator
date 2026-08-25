# Perkins briefing — round 2 (fix-audit): righttenantry-refcheck-rc3-4

- **PR:** https://github.com/solarity-services/RightTenantry/pull/599 (targets `develop`)
- **Reviewed sha:** `8c9c87ebe1857a365d820cdb8f518c4bf6abdf21` (short `8c9c87e`; commit "fix(refcheck): Perkins r1 on RC3.4 — B1 dead email CTA + W1-W6 + notes"; r1 was `13ae750`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 2 of 3 — **fix-audit** of r1's CHANGES_REQUESTED
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r2` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-4.md` + the story spec + the architecture (AD-3/AD-6/AD-7/AD-9/AD-14) + UX (§6.5/§7.9/§8.6/§10.2). No GitHub issue.
- **prior_findings:** `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/consolidated.json` (r1 = CHANGES_REQUESTED: 1 blocker / 6 warnings / 14 notes; 25/25 verified). This is a **re-review / fix-audit** — run the fix audit FIRST against prior findings, then scan the delta for new issues.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What changed since r1 (the rework under review)

The impl minion claims ALL of r1's findings addressed in `8c9c87e`:
- **B1 (r1 blocker, REAL prod bug):** reference notifications now pass the RAW `row.origin_domain` (the `notify_application_scored` precedent) instead of the scheme-full `origin_from_domain(...)` → no more double-scheme `https://https://` dead CTA. `origin_from_domain` kept for the invite base_url only.
- **W1:** the review submit form now renders the hidden `_focus_seconds` field + a test that the review page carries it + a flow test (POST 240 → result reads 240).
- **W2:** `decline_reason` server-side `truncate(200)` (the /apply precedent).
- **W3:** AC7 abuse posture pinned on all 4 exit POSTs, incl. `honeypot_filled_stop_post_does_not_object_test` (filled honeypot → 200 stop-confirmed, row stays `contact_initiated`, 0 evidence rows).
- **W4:** notification rows + the late-after-handoff "after all" copy branch pinned.
- **W5:** the 4 new audit terminal events pinned (`reference_call_completed/declined/objected/wrong_person`).
- **W6:** coverage gate lifted by W3/W4/W5 (+13 tests across AC1/AC3/AC4/AC6/AC7).
- **Notes folded:** N1 (character `free_text_signals[]` — AD-9 shape for RC4), N2 (dead `headline()` arms collapsed), N3 (truthful "You asked us to stop contact" page for objector re-visits; rc3-3 terminal_rows test updated), N5 (CSRF-stack test tightened to {200} reachability with fresh live rows), N6 (channel CHECK bite-tested — 'web' ok / 'telegram' rejected).
- **Deferred (claimed low-impact):** N4 (completion_seconds spec contradiction — follows the Completion Notes deferring to rc3-7), N7 (focus clamp — moot post-W1), N8/N11 (purge_after/evidence atomicity — no sweep exists yet), N9/N10 (documented drift, inert), N12-N14 (lower-risk coverage).
- Suite claimed: 1418 unit + 460 integration (0 failures), build + format clean.

## ⚠️ CRITICAL lens-guards (carried from r1 — verify, don't re-litigate)

- **B1's fix must be complete:** no reference notification path still feeds a scheme-full origin into `build_entity_url` (grep `notify_reference_*` + `origin_from_domain` usage — the invite base_url use is legit, the CTA paths must all pass raw domains). The dead `https://https://` must be gone from every notification path.
- **The load-bearing edge cases must still hold** (r1 verified them — confirm the rework didn't disturb them): objection stickiness (AD-6/14 — a late event must not move an objected row), evidence-log single-writer (at objection time, channel 'web'), deterministic result (AD-9), one-submission (AD-3), the registry prefix-match + router arms.
- **The W3 AC7 tests must be REAL + cover the critical branch:** the stop-must-not-object case (honeypot-filled POST → 200 stop-confirmed, row stays `contact_initiated`, 0 evidence rows) — the "fake success without objecting" is the critical AC7 case (a leaked token + fake object would silently opt out real referees). Verify the test asserts the row/evidence state, not just the 200.
- **The W1 flow test must be real** (POST 240 → result reads 240 — not a tautological injection).
- **The W6 coverage claim** (AC1-AC9 gates now ≥80%) — verify the per-AC percentages.
- **Deferred notes:** N4/N7/N8/N11/N12-N14 were deferred with reasons — do NOT re-raise as blockers IF the reasons hold (spec-contradiction-follows-Completion-Notes, no-sweep-yet, documented drift). Re-raise only if a deferral is actually wrong.
- **The N3 change** (objector re-visit page + the rc3-3 terminal_rows test update) — verify the rc3-3 test change is a legitimate copy change, not a weakening.
- **No em-dashes in user-facing copy** (RT CI ban). **JSONB test gotchas** from the field-notes (space-after-colon re-serialisation — use `result->>'field'`; Squirrel's own `sql.ReferenceCallStatus`; no `decode.null`).
- **A Gleam compile/test failure** (minion claims 1418 unit + 460 integration — verify real).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 599 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + the story spec + the architecture (AD-3/AD-6/AD-7/AD-9/AD-14) + the UX (§6.5/§7.9/§8.6/§10.2), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2`, `prior_findings` = r1's consolidated.json (fix-audit FIRST, carry-forward markers). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 599 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 599 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 2 of 3 (fix-audit)` / **Job:** righttenantry-refcheck-rc3-4 / **Reviewed sha:** 8c9c87e (r1 was 13ae750) / **r1 audit:** <b>/<b> blockers FIXED, <w>/<w> warnings fixed / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers / ### Warnings / ### Notes / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-4-perkins-r2 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: zai-coding-cn/glm-5.2** — kimi quota down; glm-5.2 is the sanctioned fallback.
