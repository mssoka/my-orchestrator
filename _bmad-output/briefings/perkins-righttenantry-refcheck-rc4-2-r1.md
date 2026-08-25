# Perkins briefing — round 1: righttenantry-refcheck-rc4-2

- **PR:** https://github.com/solarity-services/RightTenantry/pull/605 (targets `develop`)
- **Reviewed sha:** `9d66ce9240a8159d06f7250acfafa9b25cbe3110` (short `9d66ce9`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-2-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc4-2.md` + Story RC4.2 in `_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` + the UX spec (§4.2 lifecycle copy, §7.4 panel copy, §13 pill colours, §7.8 explainer, §9.3 unmoderated flag, §9.5 disclaimer) + the architecture (RC4.1 contract: `reference_calls[]`, hooks, `display_disclaimer`, §4.2 strip). GitHub issue: none (RC4.2 has no issue; parent story in the epic doc).
- **prior_findings:** none (this is r1). CONTEXT: the implementing minion's badge-out (reference panel: 12 lifecycle states with UX copy verbatim; §13 pill colours teal/slate/navy/amber never red, test-pinned; completed summary with 'Not answered' never guessed + 'Worth knowing' only when the payload carries signals; §7.8 explainer collapsed-by-default + first-view auto-expand; full a11y contract + all AC testids; expand-only contract addition form_opened_at + submitted_at with back-compat decoders, RC4.1 strip assertions untouched; 502 client / 108 shared / 1476 server / 498 integration green; CI 4/4; decisions: overflow button deliberately NOT click-wired [RC4.3 owns actions], notable quotes only when ai_summary.notable_quotes exists [RC5.1 will emit them], key-facts Period = confirmed dates not the wireframe's 'As stated') — leads, NOT a substitute for your own verification.
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**Epic RC4 Story 2 — Landlord Reference Panel (Status & Summary):** the landlord UI renders the RC4.1 `reference_calls[]` contract — all 12 lifecycle states, the completed-summary pull-quote, key-facts table, 'Worth knowing' signals, the §9.5 disclaimer — with the §13 pill colour system (never red), a §7.8 explainer, and the full accessibility contract. Plus an expand-only contract addition (`form_opened_at`, `submitted_at`) with back-compat decoders.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

- **🚨 UX COPY VERBATIM — the load-bearing invariant.** All 12 lifecycle states render the UX spec's §4.2/§7.4 copy VERBATIM. **RT CI ban: NO em-dashes in user-facing copy** — flag any deviation (a missing state, reworded copy, or an em-dash in shipped strings = a real defect).
- **🚨 PILL COLOURS — NEVER RED (§13).** Teal/slate/navy/amber only; a red pill anywhere = a blocker (test-pinned; a neutralization must go red).
- **NEVER GUESS.** The key-facts table renders "Not answered" where the payload has no answer — NEVER a guessed value. A fabricated value, or a derived value presented as a fact (the wireframe's "As stated" Period) = a real defect. The Period deliberately shows the confirmed dates instead of "As stated" (not client-side derivable — the minion documented it) — do NOT flag the deviation from the wireframe; DO flag any invented date.
- **"WORTH KNOWING" ONLY WHEN PRESENT.** Signals render only when the payload carries them; notable quotes only when `ai_summary.notable_quotes` exists (v1 deterministic summaries never emit them — RC5.1 will). Do NOT flag "quotes missing" — that's the design.
- **OVERFLOW BUTTON DELIBERATELY NOT WIRED (guard!).** The ⋯ overflow button renders with its testid but is deliberately not click-wired — RC4.3 owns the actions (no dead-menu placeholder items). Do NOT flag "dead button" — a click-wired menu with placeholder items WOULD be a defect.
- **EXPAND-ONLY CONTRACT (back-compat).** `form_opened_at` + `submitted_at` are additive on `ReferenceCallDetail`; the decoders are back-compat (old payloads still decode) and the RC4.1 §4.2 strip assertions are untouched. A breaking change (old payloads fail to decode, strip assertions weakened) = a blocker.
- **HOOKS/DISCLAIMER INTEGRITY (from RC4.1 — the panel must not re-derive).** The panel renders the server-computed hooks + `display_disclaimer`; it must NOT re-derive state rules client-side (one-stable-contract AR-RC13). A client-side re-derivation of hook/status rules = a blocker.
- **a11y CONTRACT + AC TESTIDS.** Full a11y contract (keyboard, focus, aria) + every acceptance testid present. A missing testid on a stated AC element, or a keyboard/focus trap = a real defect.
- **§9.5 DISCLAIMER VERBATIM + confidence line** on written-channel results; minimal terminals carry none.
- **base = `develop`** (RC1–RC4.1 merged — do NOT re-open their findings; carry-forward only).
- **bmad-quirk heads-up (context, not a finding):** the create-story/dev-story tooling historically mis-resolved edits to the main checkout; Silas syncs it. Review the PR content as-is at the sha.
- **Em-dashes in code/commits are fine; in USER-FACING COPY they are banned (RT CI).**

### Legitimate findings here would be
- **A red pill** — a blocker [§13].
- **Reworded/deviated §4.2/§7.4 copy, an em-dash in user-facing copy, or a missing lifecycle state** — a real defect.
- **A guessed/derived-presented-as-fact value** (incl. invented dates) — a real defect.
- **A breaking contract change** (back-compat decoder failure, strip assertions weakened) — a blocker.
- **A client-side re-derivation of hook/status/state rules** — a blocker [AR-RC13].
- **An a11y break (focus trap, missing testid on an AC element)** — a real defect.
- **A `make format` / `make build` / `make test-client` / `make test-shared` / `make test-server` / integration failure at `9d66ce9`.**

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 605 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree at `9d66ce9`), `spec_files` = this briefing + the job briefing + Story RC4.2 + the UX spec (§4.2/§7.4/§13/§7.8/§9.3/§9.5) + the architecture (RC4.1 contract), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1`, `prior_findings` = none. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (stderr cache warnings would corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 605 --repo solarity-services/RightTenantry --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 605 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `9d66ce9`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantry-refcheck-rc4-2 / **Reviewed sha:** 9d66ce9 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc4-2-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
- **Model: `deepseek/deepseek-v4-flash`** — fleet-wide ruling 2026-08-12 (user override): the ENTIRE fleet rides deepseek (kimi's 403 is a false dawn — no k3 flips until the user explicitly says so; never glm-5.2). Launch every lens mega-minion with `pi --model deepseek/deepseek-v4-flash` — never bare `pi` (resolves to the kimi default) and never glm-5.2. If the round hard-fails, self-report `blocked`.
