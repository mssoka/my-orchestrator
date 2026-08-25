# Briefing: righttenantry-find-stuck-terminal

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, base `develop`). **Small ops-script change** to `deployment/db.sh`.
- **Workflow:** `bmad-quick-dev` (tiny, well-defined edit). Perkins: **OFF** (`pr_review=0` — ops helper, not application code; you verify via `db.sh` + the user reviews the diff).
- **Model:** `zai-coding-cn/glm-5.2` (kimi down; trivial SQL/shell edit).
- **bmad-quirk heads-up:** the create-story/dev-story tooling has been mis-resolving edits to the main checkout. **Verify your edit lands in YOUR worktree** (`git status` from your cwd); commit/push/PR from the worktree only.

## Mission

Broaden `deployment/db.sh`'s `find-stuck` command so it surfaces **terminally-failed analyses** (exhausted, `next_retry_at IS NULL` — not retryable), which it currently hides. These are the silently-stuck ones that won't self-heal (no retry queued) — exactly what an ops "find-stuck" tool should catch. (Discovered live: an analysis failed terminally with the #172 `COMPLIANCE_VIOLATION` error, `retry_count=0`, `next_retry_at=NULL`, idle 22h+ — invisible to `find-stuck`.)

## The current `find-stuck` (in `deployment/db.sh`, the `find-stuck)` case)

```sql
WHERE aa.status = 'failed'
  AND aa.next_retry_at IS NOT NULL      -- hides terminal failures
  AND v.archived_at IS NULL
  AND v.status = 'active'
  AND aa.retry_count > ${min}           -- default 5; also hides low-retry terminal fails
ORDER BY aa.retry_count DESC, stuck_for DESC;
```

## The change

1. **Broaden the `WHERE`** so terminal failures show regardless of retry_count (retrying ones keep the threshold):
```sql
WHERE aa.status = 'failed'
  AND v.archived_at IS NULL
  AND v.status = 'active'
  AND (aa.next_retry_at IS NULL          -- TERMINAL: show regardless of retry_count
       OR aa.retry_count > ${min})       -- retrying: only above threshold (default 5)
ORDER BY aa.next_retry_at NULLS FIRST,   -- terminal first
         stuck_for DESC;
```

2. **Add a `kind` column** so the output distinguishes them:
```sql
CASE WHEN aa.next_retry_at IS NULL THEN 'terminal' ELSE 'retrying' END AS kind,
```

## ⚠️ Watch-out: the enum-CASE type trap

`aa.status` is an **enum** (`ai_analysis_status`). If a `CASE` expression mixes string literals with `aa.status`, Postgres infers the enum type and the literals fail with `invalid input value for enum`. **Keep the `kind` CASE all-string** (both branches are literals — no `aa.status` inside it), as written above. Do NOT put `aa.status` in a `CASE` without `::text`.

## Also

- Update the `find-stuck` doc-comment in `db.sh`'s header to reflect that it now includes terminal failures (and the `kind` column).
- Do **not** touch the `reset` command (it already handles `status <> 'completed'`, so it covers both kinds).

## Verify
- `./deployment/db.sh staging find-stuck` runs **without the enum error** + shows the `kind` column (run it; staging is safe).
- A terminal failure (`status='failed'`, `next_retry_at IS NULL`) now appears (or 0 rows if staging has none — the point is no error + the column exists).
- The header doc-comment is updated.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set righttenantry-find-stuck-terminal working` at start
- `bin/ledger set righttenantry-find-stuck-terminal in-review "PR <url>"` + `bin/ledger pr righttenantry-find-stuck-terminal <url>`
- `herdr notification show "find-stuck-terminal" --body "<one-line>"` on finish

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: find-stuck-terminal · base: develop
- model: zai-coding-cn/glm-5.2 · pr_review: 0 · github_issue: (none)
