# righttenantry-refcheck-rc3-4 (field-note shard)

- **2026-08-10 (refcheck-rc3-4 Perkins r2 B2):** a progressive-enhancement
  field rendered in the HTML is INERT unless the JS that populates it
  actually runs on that page. reference_form.js `initBrowser` bailed on the
  review page (different testid), and `onSubmit` bound only `.ref-question`
  forms — so the review submit's `_focus_seconds` shipped dead (always 0).
  The integration test MASKED it via `simulate.form_body` (which bypasses the
  browser). Lesson: any client-populated hidden field needs (a) the JS wiring
  on the SPECIFIC page that renders it, AND (b) a Node/browser-path test that
  drives the wiring seam — never rely on a server-side `simulate.form_body`
  test alone to prove a client-side population. The fix was a narrow
  page-specific seam (`initReviewSubmit`), not relaxing the form-page gate.
- **2026-08-10 (refcheck-rc3-4 Perkins r1):** the canonical double-scheme
  CTA trap — `origin_from_domain` returns scheme-full (`https://domain`),
  but `email_client.build_entity_url` prepends `https://` itself. Passing
  the scheme-full origin to ANY notification CTA builder yields
  `https://https://domain/...` — a dead link in every email. Pass the RAW
  `origin_domain` to `build_entity_url`; reserve `origin_from_domain` for
  message-body links (the invite base_url). The `notify_application_scored`
  precedent (ai_client.gleam) does it right; mirror it.
- **2026-08-10 (refcheck-rc3-4 Perkins r1):** a hidden field rendered on ONE
  form (per-question `_focus_seconds`) but NOT the form that actually POSTs
  the terminal action (the review submit) silently zeroes a downstream
  signal. The integration test masked it by injecting the field manually.
  When a field flows submit→result, render it on EVERY form that POSTs that
  action + assert the end-to-end flow (don't just inject in the test).
- **2026-08-10 (refcheck-rc3-4):** the briefing's "register EACH route in ALL three registries" rests on a per-arm mental model; the registries are **prefix-matched** `"reference", ..` (one arm covers any depth). The router is the only per-arm registry. Verify the briefing's mechanism claims against disk before acting — the work was router arms + coverage tests, NOT registry edits (which would be dead code). Same lesson as the canonical "verify briefing premises" note, now with a concrete routing instance.
- **2026-08-10 (refcheck-rc3-4):** Postgres JSONB re-serialises stored JSON with a **space after colons** (`"key": value`) and may reorder keys — substring assertions on `result::text` (e.g. `"schema_version":"refcall-v1"`) FAIL. Use `result->>'field'` extraction (`test_db.query_text`) for JSONB field assertions; reserve raw-text substring matches for non-JSONB columns.
- **2026-08-10 (refcheck-rc3-4):** Squirrel generates its OWN `ReferenceCallStatus` type inside `reference_checks/sql.gleam` (mirroring the PG enum), SEPARATE from `shared.reference_call.ReferenceCallStatus`. Status args to the sql functions must be `sql.Refused`/`sql.Objected`/etc. (the trigger module is the precedent — `sql.Skipped`). Don't pass the shared variants; it's a type mismatch that compiles to "Expected sql.ReferenceCallStatus".
- **2026-08-10 (refcheck-rc3-4):** `decode.null` does NOT exist in gleam/dynamic/decode (this Gleam version). To detect a JSON null in a Dynamic, use `decode.dict(...)` (succeeds on an object, fails on null) or the `decode.optional(string)` trick. `has_draft_key` for completeness must count object-valued answers (tenancy_period, rent_amount) as answered, not just strings.
