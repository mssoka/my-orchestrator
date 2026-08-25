# SHARED CONTEXT — Perkins r3 fix-audit lenses (righttenantry-refcheck-rc3-4)

You are one lens in a parallel code-review wave. Read-only access to the repository. Verify every claim against the actual codebase — no claim is taken at face value.

## Round & scope

- Round 3 of 3 (FINAL automated round). PR #599 → `develop`. Reviewed sha `9fddf2c`.
- This is a **fix-audit**. Prior round (r2) verdict was NEEDS CHANGES with exactly ONE blocker: **B2-r2** (the W1 fix was inert — the review form's `_focus_seconds` was never populated by client JS, so `focus_seconds_reported` was always 0 in production; the r1 flow test masked it via `simulate.form_body`).
- The **r2→r3 delta under review is TINY: 2 files, 93 insertions** — a new `initReviewSubmit` JS seam in `server/priv/static/reference_form.js` (+25) and 4 new Node browser-path tests in `scripts/js-tests/reference_form_wiring.test.js` (+68). NO Gleam/server changes, NO notification/form_handler changes, NO middleware/router changes.
- Do NOT re-open r1/r2 findings that are dispositioned fixed/holding in the prior_findings file. Scan the DELTA for NEW issues only. The prior findings are context, not targets.

## Inputs (absolute paths)

- `diff_file` (the r2→r3 delta — review EXACTLY these bytes): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/delta.patch`
- `worktree` (checkout at exactly `9fddf2c`; verify here): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r3`
- `prior_findings` (r2 consolidated.json — fix-audit reference): `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/consolidated.json`
- Round briefing (lens-guards + standing orders): `/Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-4-r3.md`
- Story spec: `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r3/_bmad-output/implementation-artifacts/spec-rc3-4-form-completion-exit-routes-submit-decline-objection-wrong-person.md`
- Architecture (AD-3/AD-6/AD-7/AD-9/AD-14): `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r3/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`

## ⚠️ The load-bearing verification of THIS round (verify, don't assume)

The delta claims to fix B2-r2. **Prove by CODE TRACE, not by the commit message**, that `initReviewSubmit` in `server/priv/static/reference_form.js`:

1. **Actually binds** the review form's submit — find `reference-review-form` + its `[data-focus-seconds]` field, and confirm the rendered HTML in `server/src/reference_checks/form_pages.gleam` (`view_review`) emits matching `data-testid="reference-review-form"` + `attribute("data-focus-seconds", "")` so the selector resolves.
2. **Populates `_focus_seconds` from the page clock** — uses the SAME `clampFocusSeconds(ms)` logic the per-question `onSubmit` uses (whole seconds via `Math.floor(ms/1000)`).
3. **Does NOT `preventDefault`** — the review submit must stay a native POST. Check the listener signature + body for any `event.preventDefault()`.
4. Is **called from the top-level init alongside `initBrowser`** (both DOMContentLoaded AND the immediate readyState path) and **exported as `_initReviewSubmit`** for testing.

And confirm the **4 Node tests drive the BROWSER path (NOT a server-side `simulate.form_body` mask)** — the r2 lesson. The tests must invoke the `_initReviewSubmit(env)` seam with a fake DOM and the seam's bound submit listener directly; the negative cases (off-page no-op, native POST preserved, floor-to-whole-seconds) must be real assertions, not tautologies.

## Lens-guards that must still hold (the delta must not disturb them)

The delta is purely additive JS; these server-side invariants are untouched, but flag any delta interaction: objection stickiness (AD-6/14), evidence-log single-writer (channel 'web'), deterministic result (AD-9), one-submission (AD-3), registry prefix-match + router arms, B1's raw-origin fix on all notification paths, em-dash ban in user-facing copy.

## OUTPUT CONTRACT (mandatory)

Write ONLY a single valid JSON array to your assigned output file (path given in your lens brief). No prose, no markdown fencing, no preamble. `[]` is valid and expected when you find nothing real. Do not invent findings to fill a quota.

Each element must match this schema exactly:
```json
{
  "source": "<your assigned source tag>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. If you cannot quote the lines, you have not verified it — drop the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```

ACCURACY MANDATE: every finding will be independently re-verified against the worktree before reaching the report. Findings whose `evidence` cannot be located, or whose claims contradict the actual code, are DISCARDED silently. Open the file. Read the lines. Quote them verbatim. Hedging ("might", "could") = you have not verified it → drop it. Accuracy > volume.
