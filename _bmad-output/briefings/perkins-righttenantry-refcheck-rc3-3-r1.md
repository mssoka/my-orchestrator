# Perkins briefing — round 1: righttenantry-refcheck-rc3-3

- **PR:** https://github.com/solarity-services/RightTenantry/pull/596 (targets `develop`)
- **Reviewed sha:** `a0b6910816f119eb8485c3d959419f194d4af820` (head `refcheck-rc3-3`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-3-r1` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-3.md` + the story spec at `_bmad-output/implementation-artifacts/spec-rc3-3-referee-form-session-open-answer-autosave.md` + `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (AD-3 route registration + capability token + resumable, AD-10 form_opened_at, AD-15 abuse, A2 draft_answers, A3 TTL) + `_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md` (§6.5 landing + question tables, §8.5 token-state pages). No GitHub issue.
- **prior_findings:** none (round 1). CONTEXT: the rc3-2 Perkins r1 **warning #1** flagged that `middleware.redact_token_route` had NO `/reference` arm (the spec asserted it covered `/reference/*`). rc3-3 was MANDATED to add it. Verify rc3-3 applied the fix correctly + completely (the `/reference` arm added + the regression pins) — do NOT re-litigate (the fix is mandated; verify it's done).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

**RC3.3: the referee form session** — the `/reference/:token` route, the referee-facing no-login form the rc3-2 templates link to. The referee opens the link, answers one question at a time with autosave, resumes across visits — or hits an honest exit page. Perkins mandate per the job briefing: **ON (code — referee-facing form); one round.**

Key systems to verify:
- **Route registration (AD-3 checklist):** `/reference/:token` in all three places — `middleware.redact_token_route` (THE Perkins fix — verify the `/reference` arm + the regression pins), `middleware.is_public_path`, the router arms. Token ~288-bit with the RC2.1 partial index.
- **Valid token on a live row:** first GET stamps `form_opened_at` (AD-10, once); the landing screen (UX §6.5) — the **second Art 14 moment** + both escape routes (wrong person, decline) BEFORE any question; per-slot question sets (previous-landlord 11, employer 8, character 5) one-per-screen mobile / single max-w-[48rem] desktop; as-stated checks pre-filled.
- **Autosave + resume:** each answer persists to `draft_answers` (A2) — PUT with JS, equivalent per-question POST **without JS** (SSR never requires JS — the PRG pattern); re-opening resumes at the next unanswered question.
- **Unknown/expired/terminal token:** branded pages (UX §8.5) with distinct **truthful** copy (expired / already completed / declined / landlord handling) — no dead ends; expired-but-open offers "Send me a new link" (guarded remint → old links die → re-sent to contact on file → `reference_call_link_resent` audit). Link TTL 10 days (`form_token_expires_at`, A3).
- **Abuse posture (AD-15):** honeypot + submission-timing on POSTs (the `/apply`-class posture).

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

This is **server-side Gleam SSR code** for the referee form. RT-specific constraints:

- **No em-dashes in user-facing copy** (RT CI-guarded ban) — the form copy, question text, token-state pages. A single em-dash in copy is a legitimate finding.
- **SSR never requires JS** — the per-question POST (PRG) is the first-class path; the PUT (JS) is the enhancement. Do NOT flag "the JS path should be the primary" — the no-JS PRG path is the spec.
- **The Perkins r1 fix is MANDATED** — rc3-3 was required to add the `/reference` arm to `redact_token_route`. Verify it's done + the regression pins exist; do NOT flag "why add it" or suggest reverting.
- **Do NOT flag the truthful/decline/escape-route copy as "missing features"** — the design is honest-first (the referee is doing the applicant a favor; respect their time). The escape routes (wrong person, decline) BEFORE any question is the spec, not a UX gap.
- **Do NOT flag the silent-drop-with-fake-success on honeypot/timing** as deception — it's the documented abuse posture (AD-15), the same as `/apply`.
- **Do NOT flag the form as "no authentication"** — the capability token IS the auth (AD-3). No-login is the design.

### Legitimate findings here would be
- **The redact fix is incomplete** — the `/reference` arm missing in `redact_token_route` OR the regression pins absent OR the Sentry/access-log/CSP redaction not actually covering `/reference/*`.
- **SSR secretly requires JS** — the no-JS POST path broken (autosave only works with JS), or the resume/reload flow needs JS.
- **A token-state page dead end or UNtruthful copy** — a terminal state that loops, or copy that lies (e.g., "expired" when it's completed).
- **A resume bug** — re-opening doesn't resume at the next unanswered, or duplicate answers, or `form_opened_at` stamped more than once.
- **The resend-link is abusable** — the remint isn't guarded (old links survive), or the audit row is missing, or it re-sends to a different contact.
- **The token handling has a security gap** — token enumeration, the remint race, the honeypot/timing trivially bypassable.
- **Em-dashes in user-facing copy.**
- **A Gleam compile/test failure** (the minion reports 1371 unit + 432 int + 124 JS green — verify they're real, not tautological).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 596 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r1/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the story spec + the architecture (AD-3/AD-10/AD-15) + the UX (§6.5/§8.5), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-3/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1`), `<lens>.json` + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 596 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 596 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** righttenantry-refcheck-rc3-3 · **Reviewed sha:** a0b6910 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]
  ### Blockers (<n>) / ### Warnings (<n>) / ### Notes (<n>)
  ```
- Close out: `bin/ledger note <your-round-row> "verdict ..."` (Silas owns the row status); remove your worktree; close lens panes. Final message: verdict + blocker count + the report path.
