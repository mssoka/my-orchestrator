## Summary

Closes the draft-loss gap between vacancy close and landlord extension. Previously `delete_expired_application_drafts` (retention job) hard-deleted drafts the moment a vacancy was `closed` **or** `closes_at` was past — so a landlord who bought the pay-to-extend SKU after the sweep found every applicant's draft destroyed (tokens dead, journey gone), even though the webhook restores the vacancy + auto-closed applications.

Drafts now get a **7-day grace** after vacancy close. Within grace, an extension (webhook reopens the vacancy, restores auto-closed applications) resurrects the full save-resume journey — token works, draft intact. After grace, deletion proceeds exactly as before. Grace applies regardless of `closed_via` (auto vs manual).

**Spec amendment:** the F3 spec said drafts "expire at vacancy close" — this amends it to "expires 7 days after vacancy close (extension grace)".

## Decisions & rationale

- **Close-moment derivation (no `closed_at` column exists).** Per branch:
  - *Time-based branch:* `closes_at` itself is the contractual expiry moment — exact whether or not the lifecycle job has flipped `status` yet, and covers every auto-close (all auto-close paths require `closes_at < now()`).
  - *Manual branch:* `close_vacancy.sql` stamps `closed_notified_at = now()` in the same UPDATE that flips status, so it **is** the close moment. `COALESCE` falls back to `closes_at` for rows with no stamp (auto-closes pre-notification, legacy rows closed before the 2026-05 lifecycle migration). `vacancy.updated_at` was rejected: its trigger only bumps on editable-field changes, so it never records the close.
- **Earliest anchor wins (the OR).** Grace starts at the *first* close event and never resets on later bookkeeping. Corollary, accepted and documented in the SQL comment: manually closing a vacancy whose `closes_at` is already >7 days past grants no fresh 7 days — the expiry, not the click, started the grace. Also accepted: an active-but-expired vacancy that stays unswept for >7 days (requires a ≥7-day lifecycle outage AND no landlord dashboard visit) loses drafts while still technically extendable — strictly kinder than the old behavior (deletion AT `closes_at`) and an edge-of-edge.
- **No `archived_at` guard** (unchanged from the old predicate). Archived vacancies follow the same rules; the old comment's claim that archived drafts always survive was never true of the expired branch — the new comment documents the actual semantics. **Open question for follow-up:** should archiving an expired vacancy shield drafts from the time-based sweep? Pre-existing behavior, deliberately not changed here.
- **Copy changes (mission step 3 — only where sentences became false):**
  - Draft-erasure confirm page ("What stays"): "until the vacancy closes — then it's gone too" → "for about 7 days after the vacancy closes". The tombstone email now lives up to close+7d (+ daily sweep cadence), so the old sentence became false; "about" because the sweep runs daily.
  - Continue-link email ("This link works until the vacancy closes") **unchanged** — still true: the link renders the closed page once closed; grace only makes resurrection possible, it never promised deletion timing.
  - Privacy retention page has no draft row — nothing to amend.
- **`closes_at IS NOT NULL` guard dropped** from the time-based branch — the column is `NOT NULL` (initial schema), so the check was dead.

## Review pass

Two mega-minions (bmad-review-adversarial-general + bmad-review-edge-case-hunter), all findings verified against source before acting: stale `email_client` comment fixed, earliest-anchor edge documented, erasure copy cadence-corrected, dead guard dropped, and the extend→re-close cycle pinned by a new test (both reviewers independently flagged that `extend_vacancy` clearing `closed_notified_at` was unpinned — a future edit dropping the NULL-clear would silently void the second grace).

## Test evidence (grace window)

Integration suite against Docker Postgres: **379 passed, no failures**. New pins in `server/test/integration/draft_integration_test.gleam`:

- `retention_sweep_grace_keeps_recent_close_deletes_old_close_test` — manual close 3d ago **survives**, manual close 8d ago **deleted** (closed_notified_at branch isolated with future closes_at); auto-close with closes_at 3d past **survives**, 8d past **deleted** (time-based branch); active + archived vacancies untouched. Exactly 2 swept.
- `closed_then_extended_within_grace_resume_and_submit_test` — auto-close 1d ago → sweep (draft survives) → resume renders closed page while closed → `extend_vacancy` (previous_status=closed, previous_closed_via=auto) → resume via token renders the resume page with saved fields → real form submit succeeds (200) and strips the draft.
- `extend_clears_close_stamp_so_reclose_gets_fresh_grace_test` — extend clears `closed_notified_at`; a re-closed vacancy gets a fresh grace (fails if the NULL-clear is ever dropped).

Full gates green: `make format && make test && make build`; integration via `TEST_DATABASE_URL` against a local Docker Postgres (`make test-integration` equivalent, 379 passed).

🤖 Generated with an orchestrated minion (pi + herdr)

