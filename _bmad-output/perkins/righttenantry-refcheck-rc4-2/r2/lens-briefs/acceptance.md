# LENS: acceptance (source tag: `acceptance`) — Perkins r2 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Audit the diff against the spec. Identify:
- Violations of specific acceptance criteria (Story RC4.2 AC in the epics file, line ~629)
- Deviations from spec intent (UX §4.2/§7.1–7.8/§9.3/§10.3/§12/§13, architecture §8.1/§8.2/§9.5, amendment A5)
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

**Round-2 priority — the r1 fix audit (verify EACH, don't re-open):** r1 blockers/warnings are listed in `_shared.md`'s fix map. Re-read the cited code in THIS worktree and classify each `fixed` or `still-present`. A missing/wrong fix = a finding at the r1 severity. Then run the AC walk below for fresh deviations the rework may have introduced.

Walk the Story RC4.2 AC line by line against the diff:

1. **AC1 — Placement & chrome.** Right column below Applicant Information, above Audit Trail (BOTH the AI and no-AI branches of `application_detail.gleam`); heading "Reference Checks ({n})"; sub-line §10.3 as amended (pre-trigger: "Starts automatically when you mark the viewing as done." — the A5 VIEWING wording, NOT the superseded shortlist wording); collapsed-by-default "What this tells you" explainer (§7.8 verbatim); testids `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}`.
2. **AC2 — 12-state matrix.** Every lifecycle state renders per UX §4.2/§7.4 verbatim: Off (contact chips, NO re-ask), Queued (A5 copy), Invitation sent / Reminder sent / Form opened (mini timeline + what-happens-next), Reference received, Partially completed ("answered {m} of {n}", confidence capped medium — server-side, panel must NOT cap), Contact details didn't work, Couldn't be reached, Declined to take part, Declined contact (NO route-around suggestion), Skipped by you, Something went wrong. **Check ALL 13 §4.2 rows** (off, queued, contact_initiated, reminded, form_opened, form_completed, partial, awaiting_correction, unreachable, refused, objected, skipped, failed) — the pill labels must match §4.2's landlord label column verbatim ("Off — contact directly", "Queued", "Invitation sent", "Reminder sent", "Form opened", "Reference received", "Partially completed", "Contact details didn't work", "Couldn't be reached", "Declined to take part", "Declined contact", "Skipped by you", "Something went wrong").
3. **AC2 colours — §13 semantics:** received teal, waiting/queued slate, reminder/opened navy, needs-attention (unreachable/awaiting correction) amber, declined/objected slate — **never red**.
4. **AC3 — Completed detail:** headline pull-quote (amber left border), key-facts dl with "Not answered" for unanswered (never hidden, never guessed), ≤3 notable quotes, "Worth knowing" when ≥1 signal (§7.5 header + per-signal copy verbatim, `border-l-2 border-amber-400`, innocent explanation + suggested action), free-text unmoderated flag (§9.3), confidence line verbatim.
5. **AC4 — a11y & loading:** skeleton shimmer during load; card `role="region"` + `aria-label="Reference checks"`; rows are buttons with `aria-expanded` + `aria-controls`; status never colour-only; no keyboard/focus traps.
6. **W6 check — explainer dismissed-state:** UX §7.3 says "collapsed by default, per-user dismissed state". r1 W6 flagged the missing localStorage persistence. Verify the final state: either `rt_refcheck_explainer_dismissed` localStorage hydration implemented per the PR's own spec (model field, hydration, save on dismiss), OR the PR spec was amended to document a session-scoped decision. A silent spec drift with no code AND no spec amendment = still-present.

For each finding, reference the violated AC or spec phrase in `detail` (quote the exact phrase). Verify against the worktree.
