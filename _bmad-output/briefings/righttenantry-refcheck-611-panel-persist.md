# Briefing — righttenantry-refcheck-611-panel-persist (issue #611 — edit-trio inputs swallow keystrokes)

- **Job id:** `righttenantry-refcheck-611-panel-persist`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-611-panel-persist`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (persistence-correctness — this bug silently saved STALE
  data with a success toast).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop` @ 758f1d8. A sibling job (`refcheck-612-emdash-prose`) may merge
  while you work — disjoint areas; rebase onto origin/develop if it lands first.
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will
  be red/not-started until the user fixes it. NOT a code failure. Run the FULL local
  suite green (`make test-all`) before opening the PR; Perkins verifies locally.

## Mission — fix issue #611 (the issue IS the spec — read it in full first)

**The bug (user-confirmed live, repro'd by two bug-hunt agents):** in the refcheck
panel-correct AND panel-substitute forms, the edit-trio inputs (Name/Email/Phone)
swallow keystrokes: typed text snaps back to the prefilled value ~150ms after every
input event, and **Save persists the ORIGINAL contact with a success toast** — the
landlord believes the correction saved, but the old contact survives and the single
correction cycle is burned (DB proof: `correction_cycles=1` with the old value).

**Root cause (from the issue):** the input event reaches the Lustre runtime but the
message never dispatches — `decode2` returns `DispatchedEvent` (handler-path lookup /
decode failure) and silently swallows the event. The event path is recorded as
"dispatched", so `is_controlled()` flips the input to **controlled**; the attribute
diff then treats `value` as always-changed (`controlled || prev.value !== next.value`
in `client.js`), and every render (including the 1s notifications poll) re-asserts
`node.value` from the model. Since the model never got the keystroke, the OLD value
comes back — with zero DOM mutations. The Gleam wiring (view →
`UserEditedRefcheckTrio` → `refcheck_edit` dict) is CORRECT at every level and matches
the compiled bundle; the failure is in the runtime event path/cache layer for these
specific inputs — they live in a **conditionally-rendered, list-mapped row**, unlike
the login-page inputs (which work, control-verified).

**The fix:** the runtime event-path/cache layer must dispatch (or fail LOUDLY) for
these inputs — never silently swallow. Whatever the precise repair (handler-path
lookup for conditionally-rendered list-mapped inputs, decode/cache invalidation, or a
controlled-input diff fix), it must:
1. Land text in the fields (Name/Email/Phone) on both panel-correct and
   panel-substitute forms — user-confirmed repro from the issue.
2. Save the TYPED value — DB shows the new contact and the correction cycle consumed
   only then.
3. Not regress the login-page inputs (control-verified working) or the other
   controlled inputs.
4. Fail loud, not silent: if an event path can't dispatch, it must surface an error —
   no `DispatchedEvent` swallow without a log/exception (the silent class is what made
   this bug invisible for days).

**Acceptance:**

1. Repro from the issue passes: type into all three fields — text stays; Save →
   success toast AND the row's contact updates in the DB (verify `correction_cycles`
   + the new value).
2. Same for the substitute form (new referee actually submitted).
3. Regression suite green: full `make test-all`; a pin test reproducing the
   keystroke-swallow (the issue's controlled repro) so this class cannot silently
   return.
4. PR body: root-cause writeup (why the swallow happened), the fix, and the loud-
   failure guarantee; PR closes issue #611 (`Fixes #611`).
5. Local suite green; Perkins verifies locally (CI billing blocked).

**Scope guard:** the input event-path fix only. No copy changes (that's #612's job),
no feature work, no other UI movement.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-611-panel-persist
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 611
pr_review: 1
```
