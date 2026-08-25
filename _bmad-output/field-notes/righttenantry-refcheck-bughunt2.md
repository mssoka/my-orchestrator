# Field notes shard — righttenantry-refcheck-bughunt2 (2026-08-15)

- The reference-form `data-current` marker NEVER advances on desktop (the reference_form.js `showOnly` stepper is mobile-only) — id-scope continues to `[data-question="<id>"]` and verify via the autosave toast/draft; also `a_tenancy_from` (YYYY-MM) is required even when the ongoing checkbox is set.
- Toasts render `role="status"` + `data-testid="toast-message"`, NOT `[role=alert]` (the bug-hunt skill doc is stale on this) — poll the data-testid; and the panel's `has_next_reminder` cadence hint ignores `taken_over` (filed #621) — gate any "next step" copy on the taken-over flag.
- The RC3.5 reference-check sweep never runs in the sandbox (Cloud Scheduler in prod) — fire `POST /api/v1/internal/reference-checks` with INTERNAL_SECRET to tick it; the take-over/start actions re-arm rows (`next_attempt_at=now()`) so one manual tick sends everything due.
