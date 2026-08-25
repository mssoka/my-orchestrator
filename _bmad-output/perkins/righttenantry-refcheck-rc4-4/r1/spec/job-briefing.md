# Briefing — righttenantry-refcheck-rc4-4 (Attempt Log, Export & Notification Completeness)

- **Job id:** `righttenantry-refcheck-rc4-4`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-rc4-4`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the RC line's standing bar).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` — RC4.3 (row actions) must be MERGED before this dispatches; it
  extends the panel + emit points. If RC4.3's merge is pending at your start, wait and
  rebase. **Standing lesson for this line: NO client-side state re-derivation** (AR-RC13
  blocked RC4.2 r1 and RC4.3 r1 — hooks from the payload/API are the single source of
  truth).

## Mission (epic RC4, story RC4.4 — evidence + trust)

Implement **Story RC4.4: Attempt Log, Export & Notification Completeness** from
`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` (line ~692) —
full spec there; the essentials:

1. **Attempt log** — for a started row, the timeline per UX §7.6 renders in the Audit
   Trail's visual language (`role="list"`, `<time datetime>`), covering every send,
   form-opened, correction, takeover, substitution, and terminal event.
2. **Export** — "Export attempt log" copies a plain-text version (reference, timeline,
   outcome, signals) to the clipboard with the **verbatim toast (OQ-5)** — no file
   download in v1.
3. **Notification completeness** — every reference event gets its UX §7.9 copy verbatim,
   including the late-completion-after-handoff variant (reuses `reference_completed`);
   the **preference-matrix test** proves realtime/daily/off behaviour per landlord
   `notification_preference`; a **no-duplicate-terminals test** proves the T+96h warm
   handoff is the only unreachable-path notification (§8.3).
4. **Emit points** — wire dispatch per emitting story (send/opened/correction/takeover/
   substitution/terminal + late-completion).
5. **Deferred RC2.1 codec (MUST land in THIS story — else reference notifications are
   undecodable):** extend `shared/src/shared/notification.gleam` with the four
   `reference_*` NotificationType variants (+ codec arms) and map them in
   `client/src/components/notification_dropdown.gleam` (exhaustive pattern match — any
   emitted `reference_*` notification is undecodable until the codec lands; the four enum
   values are already in the DB migration from RC2.1).

**Files/areas:** `client/src/components/reference_panel.gleam` ·
`server/src/notification/notification_dispatch.gleam` + templates ·
`server/src/reference_checks/` emit points · `client/src/copy.gleam` (copy verbatim —
no rewriting).

**Verify:** preference-matrix + no-duplicate tests; `make test-server` / `make
test-client` green.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-rc4-4
base: develop
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
