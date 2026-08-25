# Lens: Architecture (source: `architecture`)

Read your shared context first: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/_shared.md — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `architecture`. Your output path is: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/architecture.json

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions? (Compare the new `server/src/auth/first_touch_cookie.gleam` module and the Meta dispatch wiring against existing modules like `auth/attribution.gleam`, `auth/cookie_names.gleam`, and the password path's `dispatch_signup_meta` call site.)
- Does it introduce unnecessary coupling between modules? (e.g. the new `meta: Meta` parameter threading through `handle_oauth_callback` / `process_oauth_callback` / `complete_oauth_flow`, and the router change.)
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
