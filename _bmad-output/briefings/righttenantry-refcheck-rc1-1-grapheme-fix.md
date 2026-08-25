# Briefing — righttenantry-refcheck-rc1-1-grapheme-fix (codepoint-bounded client IP/UA)

- **Job id:** `righttenantry-refcheck-rc1-1-grapheme-fix`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `rc1-1-grapheme-fix`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow).
- **Perkins:** `pr_review: 1` (the RC line's standing bar — small but correctness-sensitive:
  DB write path).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `develop`.

## Mission (deferred-work item, spec-rc1-1 — unblocked, do now)

From `RightTenantry/_bmad-output/implementation-artifacts/deferred-work.md`
(spec-rc1-1-attestation-capture-schema-submission-write-path):

> `request_helpers.client_ip`/`client_user_agent` slice by **graphemes** (Gleam
> `string.slice`) while the DB CHECK bounds count **characters** (Postgres `length()`) — a
> multi-codepoint header can exceed the bound post-slice and 500 the write path. The helpers
> feed `cookie_consent_log`, `payment_terms_acceptance`, and `application.submitted_*` — all
> share the same 64/512 CHECK idiom, so the fix (codepoint-bounded slicing) belongs in one
> focused change across all three callers.

**Acceptance:**

1. Fix `request_helpers.client_ip` / `client_user_agent` to slice **codepoint-bounded**
   (never split a multi-byte character, never exceed the DB CHECK character bounds) —
   one focused change in the helper, applied across all three callers
   (`cookie_consent_log`, `payment_terms_acceptance`, `application.submitted_*`).
2. Add a regression test with a multi-codepoint header that previously would exceed the
   bound post-slice (e.g. emoji-heavy UA / IP-shaped garbage) proving the write path no
   longer 500s.
3. Existing suites green: `make test-server` / `make test-shared` (and client if touched).
4. Scope guard: the helper + the three callers ONLY — no unrelated refactors, no
   notification work (RC4.4 owns that).

**Verify:** regression test passes; full server/shared suites green.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: rc1-1-grapheme-fix
base: develop
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
