# LENS: security (source tag: `security`) — Perkins r2 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

OWASP-oriented security review of the diff. This is a display-only client PR (plus an additive server payload key), so the surface is small — focus on:

- **§4.2 strip integrity (the RC4.1 boundary).** The new `form_opened_at`/`submitted_at` SELECT columns in `list_reference_calls_for_detail.sql` must not disturb the existing §4.2 strip: `form_token`, `objection_detail.payload_ref`, raw referee IP/UA inside `fraud_signals.form_session` must still be absent from the wire. The strip assertions in `server/test/application/application_detail_handler_test.gleam` must be UNTOUCHED (not weakened, not removed). Also check the `jsonb_typeof` guards around the `#-` path-deletes survived (one corrupt row must not 500 the whole endpoint).
- **Client-side parsing of server payloads.** The panel `json.parse`s the stored `result` text client-side (`parsed_result_decoder`, `signals_decoder`, `form_session_decoder`). Are decoders total (malformed input → graceful degradation, never a crash/`let assert`)? Any `let assert` in new client code = a defect. Does the client render raw referee text (free-text, notable quotes) safely (Lustre escapes text — verify no `inner_html`/`html.raw` usage with referee-supplied content)?
- **XSS surface.** Free-text referee answers, headline, notable quotes, attempt `detail` strings — all rendered via `html.text`? Any attribute interpolation with referee data (e.g. `datetime` attributes, ids)? Verify no unescaped HTML injection path.
- **localStorage usage (r1 W6 rework)** — the explainer dismissed-state hydration. Check: no sensitive data stored; reads are wrapped (a `localStorage.getItem` throw must not crash the app); the stored key is namespaced (`rt_refcheck_explainer_dismissed`); only a boolean is persisted.
- **No new endpoints, no new auth surface** — confirm nothing in the diff adds a route, handler, or state mutation. Any scope drift into server routes = scope drift flag.
- **Error handling** — any new failure path that could leak internal error strings to the UI.

For each finding, quote the exact lines. Verify against the worktree.
