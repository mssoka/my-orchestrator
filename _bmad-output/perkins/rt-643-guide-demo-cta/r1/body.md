## 🤖 Perkins automated review — round 1
**Job:** rt-643-guide-demo-cta · **Reviewed sha:** a014a43 · **Reviewers:** 7/7 completed
**Verification:** 7/10 findings confirmed against the code — 3 discarded as false-positive

### Blockers (0)

None. All five r1 mandates verified independently at this sha:

- **Every `/guides/*` render path carries the CTA** — the anchor lives in the shared `layout.guide_demo_cta()` (layout.gleam), wired once per composition list in all **11** view files (10 after `view_cta()`, part-4-tenancy after `view_sources()` per its no-closing-CTA shape). `content_pages.gleam` registers exactly 11 `/guides/*` routes — full match, no hand-patching.
- **Anchor attributes** — `href="/demo"`, `attribute("data-testid", "guide-demo-cta")` on the anchor; `import lustre/attribute.{attribute}` pre-exists.
- **Secondary weight** — `demo_cta_base` is lifted verbatim from landing.gleam's `demo_cta_button` (outline: bg-white, border-2 border-navy/15, hover→amber); card is border-only `mt-4` vs the primary's shadow `mt-12`; heading `text-base` vs `inline_cta`'s `text-lg`. Primary signup CTA untouched — still `cta_base` amber, one per view.
- **Brand copy exact** — heading "See it work before you sign up", button "Try the demo", subline "A live sandbox with a mock vacancy and ranked applications. No signup." All three strings byte-exact per the issue; no exclamation marks, no em dashes, outcome-led. (Em dashes appear only in code comments, never in rendered strings.)
- **Client untouched** — `git diff 61586bb..a014a43 --stat`: zero `client/` paths, 14 files, +243/−0, server + test + spec artifact only.
- **Build + tests green locally at this sha**: `make test-server` → **1535 passed, 0 failures** (550 integration skipped as designed). The new `guide_demo_cta_present_on_every_guide_test` renders all 11 views and asserts testid + href — a real rendered-HTML check, and dropping any one call fails it (mutation-verified shape).

CI note: the billing-block signature (0 steps) is noted, not gated — local gates are the merge ground truth per standing ruling.

### Warnings (3)

1. **Scope guard has no negative test** `server/test/content/content_test.gleam:1829-1847` — _[blind + tests agree]_ The spec AC "no demo CTA on `/tools/*`, `/resources`, `/resources/:slug`" is behaviorally true today (grep: `guide_demo_cta` is called only in the 11 guide views; tools/resources handlers don't route through it) but nothing pins it. A future composition or handler change could silently leak the CTA onto out-of-scope pages. Fix: assert the rendered /tools + /resources HTML does not contain `guide-demo-cta`.
2. **Placement + secondary-weight unasserted** `content_test.gleam:1843-1846` — the test checks testid + href presence only; the "directly under the signup CTA" ordering and the outline-vs-amber class split (the actual secondary-weight AC) have no assertion.
3. **Advisory test gate: CONCERNS** — P0 100% (presence on all 11 guides), P1 <90% via the two gaps above. Closing them raises the gate to PASS.

### Notes (3)

1. **Doc comment overclaims "closing signup CTA"** `layout.gleam:383-385` — true for only 4 of 10 `view_cta()` guides; rtb_disputes, property_management_fees (plus letting_agent_costs, notice_periods, rental_income_tax, rtb_registration) render FAQ/sources after the CTA block, so it's mid-page there too. Comment-only; reword when convenient.
2. **Verbatim copy asserted nowhere** — the three brand strings are exact today but unpinned; copy drift would pass CI.
3. **Card scaffold duplication** `layout.gleam:389-418` — `guide_demo_cta` re-implements `inline_cta`'s card anatomy (card div / max-w-xl column / shrink-0 button column). Two variants with different styling make a shared helper borderline; worth it only if a third CTA variant appears.

### Reviewer agreement

- **Scope-guard negative test gap** — reported independently by the blind and tests lenses (highest-confidence finding in this round).

### False positives discarded (3)

All three from the blind lens, each disproven by direct read: the "undefined render helpers" exist at content_test.gleam:80/:1021/:1339; the `lustre/attribute.{attribute}` import pre-exists at layout.gleam:24; `rental_income_tax_view.gleam` already imports `content/layout` (4 pre-existing uses) — the unified-diff hunk context simply didn't show them.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
