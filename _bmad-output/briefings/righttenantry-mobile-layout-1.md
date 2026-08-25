# Briefing: mobile layout + notification deep-link — real-path UX fixes

**Job id:** righttenantry-mobile-layout-1
**Repo:** RightTenantry

## Context

User field-tested on mobile (iPhone 14 @390×844 DPR3 + 320px sweep,
agent-browser + vision forensics). Zero demo-specific bugs, but shared
REAL-PATH layout exposures found (these affect the live product, not just
the demo). Fix all five.

## Fixes

1. **Compare bar overlap on app-detail.** With a comparison active, the
   45px fixed bar sits at y≈783 and hides ~49px of bottom content — the
   final Documents(4) toggle (y≈832) can't scroll clear. `application_detail.gleam`
   lacks bottom padding for the fixed bar (vacancy detail handles this —
   match its pattern).
2. **Status stepper collapses to a ragged 2-col grid on mobile** — orphaned
   "Approved" + centered Reject read as a button grid; the step progression
   is lost. Mobile layout that keeps the left-to-right step semantics
   (horizontal scroll rail or compact single-line stepper).
3. **Filter chip truncates mid-word** ("Needs r…") with no ellipsis — add
   text-overflow: ellipsis so it reads as intentional.
4. **Demo CTA/Reset tap targets 30–32px** — under the 44px touch guideline.
   Raise to 44px (padding, not layout shift).
5. **Application notifications don't deep-link** (product inconsistency the
   user approved fixing 2026-08-19: "cheap, high-value, kills a feels-broken
   moment in demo and real life"). Today `client.gleam`
   `UserClickedNotification` navigates only for `entity_type == "vacancy"`.
   Make `entity_type == "application"` navigate to that application's detail
   (`/vacancies/<vid>/applications/<aid>`). The notification payload carries
   only the application id — either include the vacancy id at notification
   creation (server, audit where application notifications are inserted) or
   resolve client-side on click. Keep vacancy behavior unchanged; demo
   fixtures already carry entity_type "application" so the demo inherits the
   fix. Add a navigation test (click → route) for BOTH entity types.

## Acceptance

- Mobile re-sweep at 390 + 320: zero new overflow; compare bar clears bottom
  content on app-detail; stepper keeps step semantics.
- Notification click: vacancy → vacancy detail (unchanged), application →
  application detail (new); both marked read; demo fixtures navigate too.
- Full client suite green; no regression on demo r1–r5 gauntlet classes.

## Skills policy

- Workflow: **bmad-quick-dev**.

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash).

## Review

- `pr_review: true` — real-path UX + a server/client notification contract
  change; Perkins round on the PR head.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: mobile-layout-1
- base: develop
- pr_review: 1
