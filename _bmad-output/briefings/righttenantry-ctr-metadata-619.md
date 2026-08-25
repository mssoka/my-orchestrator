# Briefing — righttenantry-ctr-metadata-619 (issue #619 — guide/tool page metadata rewrites)

- **Job id:** `righttenantry-ctr-metadata-619`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `ctr-metadata-619`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 0` — pure copy swap of user-supplied EXACT strings into SSR
  templates, no logic. (User-supplied spec-verbatim text = the one case where a
  lightweight review suffices; do your own adversarial pass + pin with copy tests.)
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr righttenantry-ctr-metadata-619 <url>` yourself.
- **Base:** `develop` @ latest origin. No sibling contention expected.
- **CI:** green. Full local suite must pass regardless.

## Mission — implement issue #619 EXACTLY (the issue IS the spec — read it in full first)

**The task:** GSC 90-day data shows 5 guide/tool pages with healthy impressions but
below-average CTR (~150–300 clicks/mo lost). The issue contains the EXACT new titles
and meta descriptions for each page, in priority order. Your job is to apply them
VERBATIM — no rewording, no "improvements", no extra pages.

**The pages (priority order, from the issue):**

1. `/guides/property-management-fees` — 7,723 imp, pos 6.0, CTR 0.5%
2. `/resources/dublin-rents-q1-2026` — 175 imp, pos 7.8, ZERO clicks
3. `/tools/rpz-calculator` — 1,657 imp, CTR 0.3%
4. `/guides/rtb-registration` — 5,270 imp (portal-seekers: snippet pre-filters intent)
5. `/guides/letting-agent-costs` — commercial wedge page

**The rules:**

1. Apply the `→ New title` and `→ New description` strings from the issue EXACTLY,
   character for character (they include the `| RightTenantry` suffix where shown).
   If a template mechanism makes exact application impossible (e.g. the suffix is
   auto-appended), adapt the mechanism so the RENDERED output is character-identical
   to the issue's strings — document any such adaptation in the PR body.
2. The tenancy-agreement-template page is explicitly OUT of scope (its meta is
   performing).
3. These are SSR pages — the meta lives in the page templates at build time. Find
   the template layer, not runtime JS.
4. Pin the change: extend/add copy tests asserting the rendered `<title>` and meta
   description for all 5 pages match the issue strings exactly (follow the existing
   copy-test pattern from #612/#614).

**Acceptance:**

1. All 5 pages render the new title + description exactly as specified in the issue
   (pinned by tests).
2. No other pages' metadata touched (grep/test proof).
3. Full local suite green; PR body lists the 5 pages + `Fixes #619`.

**Scope guard:** metadata strings + their tests ONLY. No content changes, no schema
markup, no new pages, no canonical/OG tags beyond what already exists (if OG
description mirrors the meta description in these templates, update it to match the
new description — same string — and note it in the PR).

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: ctr-metadata-619
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 619
pr_review: 0
```
