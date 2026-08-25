# Briefing — righttenantry-refcheck-621-reminder-hint (issue #621 — taken-over row still promises a future reminder)

- **Job id:** `righttenantry-refcheck-621-reminder-hint`
- **Repo:** RightTenantry · **Base:** `develop` @ latest head (Silas resolves the exact
  sha at dispatch; RT board is clean — sibling `analytics-568-617` is parallel-safe,
  disjoint areas) · **Slug:** `refcheck-621-reminder-hint`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (user-facing reference-checks surface; consistent with
  the bug-hunt fix precedents 611/612/613/615).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr righttenantry-refcheck-621-reminder-hint <url>` yourself — the pr field
  does NOT self-populate from a status note.
- **CI:** green. Full local suite must pass (`make test-all`).

## Mission — fix issue #621 (read it in full first — the issue IS the spec; it carries a screenshot + a scenario pin)

**The bug:** the reference-check panel promises a future automated reminder on a row
the landlord has **taken over manually**. On `reference_panel.gleam`, the
`has_next_reminder` hint keys ONLY on the call status:

```gleam
let has_next_reminder = case call.status {
  ContactInitiated -> list.length(send_batches(call.attempt_log)) < 4
  _ -> False
}
```

A taken-over `contact_initiated` row still renders **"Next reminder in ~2 days if
there's no reply"** — while the sweep that would send that reminder explicitly
excludes taken-over rows (`sweep_due_reference_calls.sql`: `AND rc.taken_over_at
IS NULL`). The takeover toast already says "automated messages stopped" — the hint
is a promise the system will not keep.

**The fix (the issue's steer — one-line panel change):** gate the hint on the
taken-over flag — e.g. `ContactInitiated if not taken_over(call) -> batch_count < 4`,
or drop the hint whenever the row is taken over. Pick the cleanest form; the hint
must agree with the takeover toast.

**Constraints (from the issue):**

1. Fix the APPLICATION code, not the scenario.
2. Re-run with `/bug-hunt reference_checks taken-over-reminder-hint` — expected
   PASS (the scenario yaml lives at
   `.pi/skills/bug-hunt/scenarios/reference_checks/taken-over-reminder-hint.yaml` in
   the repo — locate the run path and follow the bug-hunt suite instructions; the
   verification-rerun precedent re-created the suite from the scenario specs).
3. No regressions in sibling scenarios (run the sibling reference_checks scenarios
   too).

**Acceptance:**

1. Root cause confirmed + fix landed (hint gated on the taken-over flag).
2. `/bug-hunt reference_checks taken-over-reminder-hint` passes; sibling scenarios
   green; full local suite green (`make test-all`).
3. PR body carries: the one-line change, the scenario evidence, and a note that no
   sweep behavior changed (this is a panel-presentation fix only).

**Scope guard:** panel hint ONLY. No sweep logic, no cadence, no DB, no toast
changes, no other surfaces.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-621-reminder-hint
base: develop
model: deepseek/deepseek-v4-flash
pr_review: 1
github_issue: 621
```
