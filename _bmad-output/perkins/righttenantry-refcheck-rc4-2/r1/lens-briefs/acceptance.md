# LENS: acceptance (source tag: `acceptance`) — Perkins r1 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Audit the diff against the spec. Identify:
- Violations of specific acceptance criteria (Story RC4.2 AC in the epics file, line ~629)
- Deviations from spec intent (UX §4.2/§7.1–7.8/§9.3/§10.3/§12/§13, architecture §8.1/§8.2/§9.5, amendment A5)
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

Walk the Story RC4.2 AC line by line against the diff:

1. **AC1 — Placement & chrome.** Right column below Applicant Information, above Audit Trail (BOTH the AI and no-AI branches of `application_detail.gleam`); heading "Reference Checks ({n})"; sub-line §10.3 as amended (pre-trigger: "Starts automatically when you mark the viewing as done." — the A5 VIEWING wording, NOT the superseded shortlist wording); collapsed-by-default "What this tells you" explainer (§7.8 verbatim); testids `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}`.
2. **AC2 — 12-state matrix.** Every lifecycle state renders per UX §4.2/§7.4 verbatim: Off (contact chips, NO re-ask), Queued (A5 copy), Invitation sent / Reminder sent / Form opened (mini timeline + what-happens-next), Reference received, Partially completed ("answered {m} of {n}", confidence capped medium — server-side, panel must NOT cap), Contact details didn't work, Couldn't be reached, Declined to take part, Declined contact (NO route-around suggestion), Skipped by you, Something went wrong. **Check ALL 13 §4.2 rows** (off, queued, contact_initiated, reminded, form_opened, form_completed, partial, awaiting_correction, unreachable, refused, objected, skipped, failed) — the pill labels must match §4.2's landlord label column verbatim ("Off — contact directly", "Queued", "Invitation sent", "Reminder sent", "Form opened", "Reference received", "Partially completed", "Contact details didn't work", "Couldn't be reached", "Declined to take part", "Declined contact", "Skipped by you", "Something went wrong").
3. **AC2 colours — §13 semantics:** received teal, waiting/queued slate, reminder/opened navy, needs-attention (unreachable/awaiting correction) amber, declined/objected slate — **never red**.
4. **AC3 — Completed detail:** headline pull-quote (amber left border), key-facts dl with "Not answered" for unanswered (never hidden, never guessed), ≤3 notable quotes, "Worth knowing" when ≥1 signal (§7.5 header + per-signal copy verbatim, `border-l-2 border-amber-400`, innocent explanation + suggested action), free-text unmoderated flag (§9.3), confidence line verbatim.
5. **AC4 — a11y + loading:** skeleton shimmer during load (existing page skeleton covers detail-load — verify the AC's stance vs the implementation); card `role="region"` + `aria-label="Reference checks"`; rows are buttons with `aria-expanded`/`aria-controls`; status never colour-only.
6. **AC5 — data contract discipline:** renders from `reference_calls[]` + `attestation_on_file` + `reference_contact_choice` only; Off ⇔ choice == "declined"; card hidden for pre-v1 (NULL choice, no rows); pre-trigger (attested, no rows) shows sub-line + explainer. **No client-side state-rule re-derivation** (hooks/status rules come from the server).
7. **Expand-only contract:** `form_opened_at`/`submitted_at` additive — encoder nullable, decoder back-compat (absent key → None), RC4.1 strip assertions untouched in `application_detail_handler_test.gleam`.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
