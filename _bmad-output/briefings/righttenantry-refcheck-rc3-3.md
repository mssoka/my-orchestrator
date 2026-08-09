# Briefing: righttenantry-refcheck-rc3-3

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (develop has rc3-1's sms_client + rc3-2's templates). PR targets develop.
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion (learning-loop pattern). Perkins: **ON** (code — referee-facing form). Self-review: bmad-review-edge-case-hunter (token states, autosave, resume, abuse).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; one round).

## Mission

Story **RC3.3: Referee Form Session — Open, Answer, Autosave.** The sprint is at 7/18 (rc3-1 + rc3-2 just merged). rc3-3 ships the **`/reference/:token` route** — the referee-facing no-login form the rc3-2 templates link to. The referee opens the link, answers one question at a time with autosave, resumes across visits — or hits an honest exit page.

## ⚠️ MANDATORY: fold in the Perkins r1 fix from #595

Perkins r1 on rc3-2 flagged (warning #1): **`middleware.redact_token_route` has NO `/reference` arm** — the spec asserts it covers `/reference/*`, but the registry only has dsar/erase/apply arms. No leak today, but rc3-3/rc3-4 trust that false assurance. **rc3-3 MUST add the `/reference` arm to `redact_token_route`** (Sentry/access-log/CSP redaction) as part of the AD-3 route-registration checklist. Fix the spec + add the arm when the route lands (i.e., now).

## The story (acceptance — from the epics + AD-3)

1. **Route registration (AD-3 checklist):** `/reference/:token` registered in all three places — `middleware.redact_token_route` (**the Perkins fix**), `middleware.is_public_path`, router arms. Token ~288-bit with the unique partial index from RC2.1.

2. **Valid token on a live row:** `GET /reference/:token` stamps `form_opened_at` (AD-10), renders the landing screen per UX §6.5 — the **second Art 14 moment** + both escape routes (wrong person, decline) BEFORE any question. Questions follow per-slot sets (previous-landlord 11, employer 8, character 5 — UX §6.5 tables), one per screen on mobile with progress ("Question 4 of 11"), single `max-w-[48rem]` page on desktop, as-stated checks pre-filled from application data.

3. **Autosave + resume:** each answer persists to `draft_answers` (A2) — `PUT /reference/:token/answer` with JS, equivalent per-question POST **without JS** (SSR never requires JS). Re-opening resumes at the next unanswered question (resumable until submitted, AD-3 as amended).

4. **Unknown/expired/terminal token:** branded pages per UX §8.5 with distinct truthful copy (expired / already completed / declined / landlord handling) — no dead ends. Expired link on a still-open check offers "Send me a new link" (re-sends to the contact on file, audit-logged). Link TTL 10 days from invitation (`form_token_expires_at`, A3).

5. **Abuse posture (AD-15):** honeypot field + submission-timing validation on POSTs (the `/apply`-class posture).

## Source material (read)
1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — RC3.3 (the full AC above).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — AD-3 (route registration + capability token + resumable), AD-10 (form_opened_at), AD-15 (abuse), A2 (draft_answers), A3 (TTL). The `redact_token_route` middleware row.
3. **`_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`** — §6.5 (landing + per-slot question tables + progress), §8.5 (the branded token-state pages).
4. **rc3-2 (merged #595)** — the templates that link here; the stop-link `/reference/:token/stop` (rc3-4 owns the stop/decline/object routes — rc3-3 ships the form session, rc3-4 the submit/exit).
5. **`server/src/middleware.gleam`** (redact_token_route — the Perkins fix) + the `/apply` form pattern (honeypot/timing precedent).
6. **`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`** — rc3-3 → in-progress → done.

## Flow
1. **bmad-create-story** — rc3-3 spec (the form session + the redact_token_route Perkins fix). Update tracker.
2. **bmad-dev-story** — the `/reference/:token` route + form session: route registration (incl. the redact arm fix), landing (Art 14 + escape routes), per-slot questions, autosave (draft_answers, JS + no-JS), resume, token-state pages, TTL, resend-link, honeypot/timing.
3. **Test:** token states, autosave, resume, TTL/expiry pages, resend-link, honeypot/timing rejection, SSR render checks, the redact_token_route /reference arm. `make test-server` + `make test-integration` green.
4. **Update tracker:** rc3-3 → done/review.

## Constraints (RT-specific)
- **No em-dashes in user-facing copy** (RT CI-guarded ban) — the form copy, question text, token-state pages.
- **SSR never requires JS** (per-question POST works without JS).
- **The Perkins fix is mandatory** — `redact_token_route` gets the `/reference` arm.
- The Art 14 notice (second moment) on the landing screen.
- The referee-facing copy is truthful + plain (the referee is doing the applicant a favor — respect their time).

## Acceptance
- `/reference/:token` ships: registered in all 3 places (incl. the redact arm fix), landing with Art 14 + escape routes, per-slot questions, autosave (JS + no-JS), resume, token-state pages, 10-day TTL, resend-link, honeypot/timing.
- `make test-server` + `make test-integration` green.
- No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-3 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-3 in-review "PR <url>"` when PR opens
- `herdr notification show "refcheck-rc3-3" --body "<one-line>"` on finish
- Final message: the route + form session summary, the Perkins redact-arm fix confirmed, test results, story-spec path, PR URL, + whether rc3-4 (submit/exit routes) is the natural next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-3 · base: develop
