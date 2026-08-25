# Briefing — righttenantry-refcheck-rc4-2 (Reference Panel — Status & Summary)

- **Job id:** `righttenantry-refcheck-rc4-2`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-rc4-2`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (this epic's standing bar — every RC story gets a Perkins round;
  the round runs on the sanctioned reasoning model per fleet policy).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` (RightTenantry convention; RC4.1 merged there).

## Mission (epic RC4, story RC4.2 — the landlord reference panel)

Implement **Story RC4.2: Reference Panel (Status & Summary)** from
`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (line ~629) —
full spec there, this briefing names the essentials + the gotchas.

**Acceptance (condensed — the epics doc is canonical):**

1. **Placement:** right column of the application detail page (v3 layout), below Applicant
   Information, above Audit Trail; mobile position 8 (UX §7.1–7.3). Heading "Reference Checks
   ({n})"; state-tracking sub-line per UX §10.3 **as amended** (pre-trigger: "Starts
   automatically when you mark the viewing as done.", A5); collapsed-by-default "What this
   tells you" explainer (§7.8 verbatim).
2. **Testids:** `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`,
   `refcheck-expand-{slot}`, `refcheck-overflow-{slot}`.
3. **All 12 lifecycle states** render per UX §4.2/§7.4 verbatim: Off (attestation declined —
   referee contact chips, NO re-ask affordance), pre-trigger queued, Invitation sent /
   Reminder sent / Form opened (mini timeline + what-happens-next), Reference received,
   Partially completed ("answered {m} of {n}", confidence capped medium), Contact details
   didn't work, Couldn't be reached, Declined to take part, Declined contact (no route-around
   suggestion), Skipped by you, Something went wrong.
4. **Status-pill colours per §13:** received teal, waiting slate, reminder/opened navy,
   needs-attention amber, declined/objected slate — **never red**.
5. **Completed reference detail** (expanded by default on first view): headline pull-quote
   (amber left border), key-facts definition table with **"Not answered"** for unanswered
   fields (never hidden, never guessed), ≤3 notable quotes, "Worth knowing" block when ≥1
   signal (§7.5: header + per-signal copy verbatim, amber `border-l-2`, innocent explanation +
   suggested action), free-text unmoderated flag (§9.3), confidence line verbatim.
6. **A11y + loading:** skeleton shimmer during load; card `role="region"` with
   `aria-label="Reference checks"`; rows are buttons with `aria-expanded`/`aria-controls`;
   status never colour-only.
7. **Data:** render from RC4.1's `reference_calls[]` payload + `attestation_on_file` +
   `reference_contact_choice` — NEVER re-derive state rules client-side (RC4.1's contract
   principle). Honest framing: a state that tells the landlord nothing about the applicant
   must say so — no invented confidence.

**Files/areas:** `client/src/components/reference_panel.gleam` (new) · application detail
page wiring · `client/src/copy.gleam` · shared types from RC4.1 (do not modify the RC4.1
payload contract).

**Verify:** `make test-client` green; visual check against UX §7 wireframes; the 12-state
matrix rendered. Copy is verbatim from the cited UX sections — no rewriting.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-rc4-2
base: develop
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
