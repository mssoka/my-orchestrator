# Briefing: demo-polish-2 — toast position + report at real-audit depth

**Job id:** righttenantry-demo-polish-2
**Repo:** RightTenantry

## Context

The user re-tested the demo after #630 merged. Two of the original 6 field-test
issues DID NOT hold:

1. **Toast still wrong.** Demo toasts still appear at the top of the page.
   Polish-1 verified "toast = real twin, pinned" — but the user says the REAL
   app's toasts appear elsewhere. The verification compared the wrong thing.
   **Re-investigate against the real app's RUNTIME behavior**: find the real
   app's toast component(s) and where they actually render (position, stacking,
   offset — check the landlord dashboard + app detail + compare-bar interplay),
   then make the demo toast match THAT. Constraint: the #615 guarantee (toasts
   must remain visible above the consent banner) — whatever position is chosen
   must keep that guarantee; add a pin for both (position + banner survival).

2. **Downloaded report still scanty.** Fix 4's enrichment landed unpinned
   (r1 W-fold) and the result is still thin. Target = the REAL staging
   reports. The user provided real exemplars (structural reference ONLY —
   real PII, never commit or copy content):
   - `/Users/moses/Downloads/RightTenantry-Report-Emily-Manina.pdf` (18 pages)
   - `/Users/moses/Downloads/RightTenantry-Report-Willian-Rodrigues.pdf` (19 pages)

### Real report structure (extracted — the target)

Cover (applicant, vacancy, prepared date, GDPR confidentiality block) →
**At a glance** KPIs (rent coverage %, documents processed, references on
file) → **Top concerns (n) + Top strengths (n)** with specific one-line
findings → **Recommended next steps** (prioritized, with detail + "N more
actions") → **Score Dashboard** (overall score /100, assessment, 6 weighted
tenancy criteria with weights) → **Employment & Income** (status, type,
start date, tenure analysis) → **Income affordability** (rent-to-income
ratio vs thresholds) → **Rental history** → **References** (on file,
recency checks) → **Guarantor** (income coverage analysis) → **Identity &
Contact** → **Documents Provided** → **Verification Methodology** →
credit-check-out-of-scope note → GDPR footer + page numbers.

3. **Compare Top 3 STILL missing from the demo** (user re-test, same
   failed-parity pattern as the toast). Polish-1 claimed "Compare = real
   twin" — the user says the demo vacancy detail does NOT show the Compare
   Top 3 button that the real vacancy detail has. Re-investigate against
   the REAL app's vacancy detail at runtime: find the exact render
   condition for the Compare Top 3 button (what state/data it needs —
   comparison set populated? N applications analyzed?) and make the demo
   vacancy detail satisfy that condition with demo-universe data so the
   button renders AND works (opens the demo comparison).

The demo's baked reports must carry the SAME sections at comparable depth,
populated with demo-universe data (contradictions/concerns included — a
flawless report is as unconvincing as a scanty one). Regen path:
`gleam run -m demo/pdf_prebake -- server/priv` (Typst pipeline, committed
PDFs). The demo analysis data must RICH enough to feed these sections —
extend the demo fixtures/analysis if needed. If the real pipeline renders
from the real analysis JSON, feed the demo analyses through the SAME
renderer so layout can't drift.

## Acceptance

- Demo toast position = real app runtime position (verified in both, side
  by side), #615 consent-banner guarantee holds, both pinned by tests.
- Each demo applicant's baked PDF carries every section above with
  substantive demo data; page count in the same league (not 3-page stubs).
- Side-by-side against the exemplars: same skeleton, demo-specific content.
- No regression on the demo gauntlet classes (exit leak, deep-links,
  session stash, no-network); full client suite green.

## Skills policy

- Workflow: **bmad-quick-dev**.

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash).

## Review

- `pr_review: true` — demo surface, same standard as #629/#630.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: demo-polish-2
- base: develop
- pr_review: 1
