# Field notes shard — righttenantry-refcheck-verification-rerun (2026-08-14)

- RT apply-form POST is MULTIPART (415 on urlencoded) and mandates PDF uploads for
  `landlord_ref_primary` + `employer_ref_primary` (reportlab on the machine); application
  status updates are **PATCH** `/api/v1/vacancies/:id/applications/:id/status`, not POST — the
  fastest way to arm the reference_checks scenarios is: submit via the real form (unique
  email per app, `_form_loaded_at` 5s back) → PATCH-walk to `viewed` (mints landlord_ref +
  employer_ref) → SQL per-scenario call states.
- agent-browser `click @ref` silently no-ops on Lustre refcheck buttons (row expand, Correct
  details, Substitute, stepper tabs) — the native `.click()` eval fallback is mandatory; the
  referee form's `reference-continue` clicks must be scoped to `[data-question="<id>"]` (the
  stacked-forms trap), and the success export toast needs a
  `navigator.clipboard.writeText` stub in headless (no clipboard permission).
- Sandbox: `.env` → gitignored `server/.env` copy (PORT=4100, DATABASE_URL→local Docker
  Postgres on a free port, Resend/Twilio/Stripe/AI blanked, Supabase GoTrue kept for login);
  `make build-client` reads the ROOT .env, not server/.env, so build first or the PostHog
  perl pass warns.
