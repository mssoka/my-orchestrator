# Briefing: rt-643-guide-demo-cta

**Repo:** /Users/moses/code/RightTenantry (managed). **Issue:** https://github.com/solarity-services/RightTenantry/issues/643
**Type:** enhancement, code. **Skill:** bmad-build. **Model:** deepseek/deepseek-v4-flash.
**Dispatch:** worktree on the repo's default branch; one PR titled "Add Try the demo CTA to SSR guide template (#643)"; `ledger pr` the PR url; pr_review=1.

## Task

Add a secondary "Try the demo" CTA to the SSR guide template so EVERY `/guides/*` page links to `/demo`.

## Where

- SSR template: `server/src/content/content_pages.gleam` (guide rendering), possibly `content_handler.gleam` for the shared layout wrapper.
- Pattern to mirror: `demo_cta_button` in `client/src/pages/landing.gleam` (~line 83) — match its secondary visual weight. The landing's hero CTA usage is at ~line 345 for reference.

## Requirements (from the issue — follow them exactly)

- Plain anchor to `/demo` in the SSR template, rendered on every guide page.
- `data-testid="guide-demo-cta"` on the anchor (PostHog autocapture).
- SECONDARY weight only — the guide's primary signup CTA must stay primary. One primary CTA per view.
- Brand copy rules: no exclamation marks, no em dashes, outcome-led. Use this block:
  - Heading: "See it work before you sign up"
  - Button: "Try the demo"
  - Subline: "A live sandbox with a mock vacancy and ranked applications. No signup."
- No new analytics instrumentation (demo_entry already fires on /demo entry).

## Acceptance

- [ ] Every /guides/* page renders the demo CTA linking to /demo
- [ ] Anchor carries `data-testid="guide-demo-cta"`
- [ ] Secondary visual weight vs the signup CTA
- [ ] Mobile renders cleanly (no horizontal scroll)
- [ ] Build + existing tests pass (`cd server && gleam test` if a suite exists; `gleam build` otherwise; client untouched)

## Notes

- Small, targeted change. Lavish not needed — open the PR directly.
- Verify by rendering one guide locally if a dev server is cheap (`make run` needs `server/.env` symlink to the repo root `.env`); otherwise show the rendered HTML in the PR description.
