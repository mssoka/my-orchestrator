# Lens: Codebase Fit (source: `codebase`)

Read your shared context first: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/_shared.md — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `codebase`. Your output path is: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/codebase.json

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. `dispatch_signup_meta` in auth_handler.gleam, `attribution.clamp_value` / `max_value_len`, `cookie_names.with_host_prefix`, `meta_client.Recording` / `drain_recording` / `Disabled`, `ctx.config.meta`, `model.first_touch_params` in the client Model, `gleam_uri.query_to_string`, `simulate.cookie` with `wisp.Signed`)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.) Note `find_set_cookie` is defined in BOTH server/test/auth/auth_test.gleam and server/test/auth/first_touch_cookie_test.gleam and server/test/integration/auth_integration_test.gleam — check whether a shared helper already exists (e.g. cookie_attributes_test) and whether this duplication matches existing convention.
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.) The `complete_oauth_flow` signature gained a `meta` parameter — find every caller.
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
