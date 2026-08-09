## 🤖 Perkins automated review — round 1 of 3

_FYI review — PR was merged 13:37Z before this round concluded; findings are follow-up notes, no rework loop unless the user says so._

**Job:** righttenantry-form-e2e-pass · **Reviewed sha:** 26c5cc0 · **Reviewers:** 7/7 completed (×3 chunk waves — diff 3,544 lines, chunked by file group: skills-move ×2 + evidence/misc)
**Verification:** 29/32 findings confirmed against the code — 3 discarded as false-positive

### Blockers (1)

1. **No-JS fallback renders the only submit button disabled — step 6 "full submit succeeds" is evidenced only by curl; a real JS-disabled browser cannot submit** [blind] — `server/src/application/form_sections/review_consent.gleam:117` renders `attribute("disabled", "")` unconditionally (present since PR #97); the committed `17-nojs-long-form.html` shows `<button class="btn-submit" data-testid="submit-application" disabled type="submit">`; `form.js:26` is the only enabler; zero `<noscript>` fallback. The pass's curl POST bypasses the button, so journey step 6 is not demonstrated for a real no-JS browser — and the pass reported "Defects found: none — clean pass" instead of halting/escalating per the briefing's defect rule. Pre-existing app behavior, but catching exactly this was the pass's job. Needs a product decision: enable submit server-side when JS is absent, or amend the no-JS-submit claim and re-evidence with a real JS-disabled browser.

### Warnings (4)

1. **`application_draft_resumed` claimed to fire at load on the resume page, but the committed capture records no such event** [acceptance, blind] — `21-analytics-notes.md` claims it fires; `20-analytics-resume-page.json` holds 15× `$autocapture` + 1× `application_draft_saved`, zero `draft_resumed`. Re-capture with the wrapper installed pre-navigation, or amend the claim.
2. **`round-trip.yaml` description claims `resumed_at` coverage no flow step asserts** [blind] — description advertises "resumed_at stamping on the first post-resume save"; Flow steps 1–7 never assert it. Add a DB assertion via the token-seam psql pattern, or trim the description.
3. **`{SCENARIO}` 64-char local-part truncation silently eats `{RUN_ID}` digits** [blind, edge] — verified math: the 3 longest slugs produce 65–67-char local parts (`test+validation-missing-guarantor-when-first-time-renter-1785759182` = 67), so truncation eats 1–3 epoch digits; two runs inside the same ~1000s window collide as duplicate applications. Truncate the slug portion, always preserve RUN_ID.
4. **`generate-fixtures.sh` fails on any checkout lacking `fixtures/`** [codebase] — `set -eu` + `cd "$(dirname "$0")/fixtures"` with no `mkdir -p`; fixtures are gitignored, so the migration re-breaks every existing working copy at the new `.pi` path (old untracked fixtures stay behind at `.claude`). Add `mkdir -p` before the `cd`.

### Notes (17)

- Stale `~/.claude/skills/agent-browser/SKILL.md` pointer in migrated `form-bug-hunt/SKILL.md:325` [acceptance, architecture]
- Migrated `wds-4-ux-design/steps-w/step-00-nb-setup.md:80` still instructs editing `.claude/mcp.json` [architecture]
- README's "no hidden attrs" no-JS claim contradicted by its own committed HTML (8 `hidden` attrs; co-applicant/extra-income blocks unreachable without JS — by design, but the claim needs qualifying) [acceptance, blind, edge]
- AC requires suites green "BEFORE and AFTER your pass" — only the BEFORE baseline is documented [acceptance]
- Step-5 (save-resume) DB claims cite uncommitted "verify-run DB checks" — no draft DB dump in the evidence dir [acceptance]
- Pre-existing duplicate `data-section="5"` (guarantor + tell_us_more) in SSR markup — inert, no JS consumer; cosmetic [blind]
- `12-confirmation-mobile.png` and `16-resume-submitted-confirmation.png` are byte-identical (same md5) — resume-submit confirmation not independently distinguishable [blind]
- DB dumps alias the UA column inconsistently (`submitted_user_agent` vs `ua`); journey UA truncated mid-string [blind]
- `20-analytics-resume-page.json` is doubly-encoded (root is a string) [codebase, edge]
- Notes claim 10× `$autocapture` on the resume page; companion JSON records 15 [codebase, tests]
- `.gitignore` keeps stale `.claude/skills/arize-*` / `bmad-*` guards; no `.pi/skills/bmad-*` re-add guard [codebase]
- Dropped `.claude` fixtures ignore leaves stale fixtures unignored on pre-migration working copies [edge]
- wds-6 data docs duplicate numeric prefixes (two each of 04/05/06, skip 01–02) — pre-existing, cosmetic [blind]
- Fresh-form funnel evidence is prose-only, 2 of 8 sections; token-scrub regression IS evidenced (`tokenInAnyPayload: false`) [tests]
- Advisory test gate: PASS (chunk 1) [tests]
- Advisory test gate: PASS (chunk 2) [tests]
- Advisory test gate: PASS (chunk 3) [tests]

### Reviewer agreement

- "no hidden attrs" contradicted by committed no-JS HTML — **acceptance + blind + edge**
- `application_draft_resumed` absent from committed capture — **acceptance + blind**
- `{SCENARIO}` truncation eats RUN_ID — **blind + edge**
- Stale `~/.claude` agent-browser pointer — **acceptance + architecture**
- Double-encoded analytics JSON — **codebase + edge**
- Autocapture count 10 vs 15 — **codebase + tests**

**Verdict:** NEEDS CHANGES

One blocker on the deliverable's headline claim (no-JS submit dead-end reported as a clean pass), four warnings on evidence accuracy and migration breakage. In FYI mode these land as follow-up notes for the record — no automatic re-review on this PR.

_Discarded as false-positive after re-verification: `monthly_income_cents` "4100" (EUR-entry convention, server ×100), "migration leaves dangling repo-internal `.claude/skills` refs" (grep-verified none remain), "employer_name optional in no-JS HTML contradicts stepper gating" (form.js:143-208 toggles `required` with JS; no-JS optional-by-default is the designed backstop)._
