# Briefing — righttenantry-refcheck-rc4-3 (Row Actions — Start, Skip, Take Over, Correct, Substitute)

- **Job id:** `righttenantry-refcheck-rc4-3`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-rc4-3`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the RC line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` — RC4.2 (the panel) must be MERGED before this dispatches; this story
  extends the panel (overflow menus, inline edit-trio wireframes). If RC4.2's merge is
  pending at your start, wait for it and rebase.

## Mission (epic RC4, story RC4.3 — the landlord's control surface)

Implement **Story RC4.3: Row Actions — Start, Skip, Take Over, Correct, Substitute** from
`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (line ~659) —
full spec there; the essentials:

1. **Pre-trigger row** — `⋯` overflow: "Start this check now" asks once, inline (§7.4
   confirm copy), starts via the **RC2.3 API**; "Skip this reference" excludes the row
   (re-enable-able).
2. **In-flight row** — "Take over manually": inline confirmation per §7.7 (**never a
   modal**); on confirm: row gets `taken_over_at` (A7), the sweep stops sending, referee
   contact chips + attempt-log export render inline, label "You're handling this one"; the
   form link stays live — a late completion still transitions to `form_completed`, updates
   the panel, notifies (§8.6).
3. **`awaiting_correction` row** — inline edit-trio wireframe per §8.3 with the applicant's
   contact chips; "Save & resend" is audit-logged, writes `corrected_email`/
   `corrected_phone` (snapshot immutable, A1), updates the application trio, sets
   `correction_cycles = 1`, re-queues (`queued`, `next_attempt_at = now()`). A second
   failure → `unreachable` with `referee_contact_invalid` (AD-7, wired by RC3.7).
4. **Terminal `objected`/`unreachable`** — "Substitute referee" (`can_substitute_referee`):
   same inline edit captures the NEW referee trio; a NEW `reference_call` row for the slot
   (prior row retained as history); audit entry carries old + new row ids (AD-16).
5. **Every action endpoint** — ownership-checked + guarded on the row's expected pre-state
   (AD-14); manual actions **hidden entirely** in the Off (declined) state.

**Files/areas:** `client/src/components/reference_panel.gleam` + `client/src/api/` ·
`server/src/reference_checks/actions_handler.gleam` · `server/src/router.gleam` ·
`client/src/copy.gleam` (copy verbatim from cited sections — no rewriting).

**Verify:** server tests per transition (correction-cycle counting + substitution history);
client tests; `make test-server` / `make test-client` green.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-rc4-3
base: develop
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
