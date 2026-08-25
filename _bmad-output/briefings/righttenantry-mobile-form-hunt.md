# Briefing: mobile bug hunt — ALL RT forms (applicant, reference, vacancy, auth)

**Job id:** righttenantry-mobile-form-hunt
**Repo:** RightTenantry

## Mission

A systematic MOBILE bug hunt across every form surface in RightTenantry,
using the proven method from the demo hunt (2026-08-19): agent-browser
device emulation (iPhone 14 @390×844 DPR3 + 320px edge sweep), programmatic
overflow probes (every element vs scrollWidth/innerWidth), viewport
screenshots, and vision-read forensics on the captures (local qwen — every
finding verified against live DOM measurement, no guessing).

## Scope — every form surface

1. **Applicant forms** — the rental application flow (all steps/sections,
   incl. file uploads, validation errors, step transitions).
2. **Reference forms** — the referee/reference-check flow (refcheck —
   keystroke entry, edit-trio, save/submit, error states; note: keystroke
   keying by reference_call_id landed recently — verify it holds on mobile).
3. **Vacancy create/edit forms** — landlord-side, incl. deep-link edit boot.
4. **Auth/signup/login forms** — incl. OAuth buttons on mobile.
5. **Account/settings/payment forms** — whatever exists; sweep it.
6. **Any other form discovered** during the sweep — include it.

## What to hunt

- Viewport-width overflow / horizontal scroll at 390 and 320.
- Tap targets < 44px; truncated labels without ellipsis.
- Keyboard behavior: input focus scroll, keyboard covering the active
  field, next/previous field navigation, submit on enter.
- Validation errors: visible, positioned correctly, not clipped.
- Multi-step/stepper forms: step state survives viewport changes,
  progress readable (the ragged-2-col stepper class is FIXED on develop —
  regression-check it).
- Fixed bars/CTAs overlapping bottom content (the compare-bar class is
  FIXED on develop — regression-check the pattern everywhere else).
- File upload UX on mobile (photo/library picker).
- Select/date inputs rendering natively vs custom.

## Method requirements

- Both real app AND demo paths where forms differ.
- Regression-check the just-merged fixes (#631: compare-bar padding,
  stepper rail, 44px targets, chip ellipsis, notification deep-link).
- Every 🐛 finding needs: repro steps, viewport, element, measured
  numbers, and a screenshot reference. Classify: 🐛 bug / ⚠️ cosmetic /
  ℹ️ note. Do NOT auto-fix — findings are flagged for the user's decision
  (the demo-hunt pattern).

## Deliverable

A structured findings report (per form surface: verified-good list +
findings) — the user reviews it via **lavish** (HTML artifact, per the
review-loop doctrine for reports).

## Completion discipline (no-PR job)

On finish: `herdr notification show "righttenantry-mobile-form-hunt"
--body "<verdict one-liner>"` + preserve the report + screenshots to
`_bmad-output/implementation-artifacts/mobile-form-hunt/`.

## Skills policy

- **agent-browser** (device emulation, interaction, screenshots)
- **vision-read** (screenshot forensics)
- **lavish** (the findings-report review artifact)
- No code changes — report only.

## Model policy

- Minion: pi default (ops tier — deepseek/deepseek-v4-flash).

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: mobile-form-hunt
- base: develop (fresh — includes #630 + #631)
- pr_review: 0 (no PR — findings report)
