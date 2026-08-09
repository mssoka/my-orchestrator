# righttenantry-form-stepper-f1 — field notes

- `server/priv/static/*` is git-ignored with a per-file whitelist — every new static asset needs its `!` line in `.gitignore` or it deploys as a dead script tag while SSR pins (which only assert the tag) stay green (review swarm caught it).
- Error-summary hrefs are already full anchors (`#field-<key>`) and upload-slot `.field-error` spans need inline `display:flex` (they never get `.has-error`) — same display bug also exists in form.js's preflight `showInlineError` (deferred).
- `dot_env.load_default()` overrides the process env — to repoint a local dev server, replace the `server/.env` symlink with an edited copy (gitignored); staging DB lags develop migrations (submissions 500 on `submitted_ip_text`), so E2E against a local Docker DB + seeded vacancy; timing trap rejects <2s fills as spam — sleep before scripted submits.
