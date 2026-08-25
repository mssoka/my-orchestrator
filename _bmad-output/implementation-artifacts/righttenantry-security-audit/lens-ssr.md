# Lens report — SSR/RENDER (completed: dispatched lens + parent)

**Note:** the dispatched SSR lens was killed by pane reclamation after
verifying scopes 1-3 + 6-8 (its transcript findings are folded in below,
marked †). The parent completed scopes 4-5 (referee forms, DSAR/erasure).

## Verified CLEAN

- † **HTML escaping integrity**: all text nodes and attribute values render
  through Lustre → houdini full-set escape; `form_sections` re-render of
  user-submitted values (error paths) escapes cleanly.
- † **Raw-JS sinks**: PostHog snippet interpolates `vacancy_short_code`
  (server-generated charset-safe) + public API key; resume token reaches raw
  JS but `wisp.random_string` is URL-safe base64 (no quotes/backslash) and is
  exact-match verified against DB before render.
- † **Content pages**: the two `unsafe_raw_html` sinks render compile-time
  constants (rent-data posts); no DB write path feeds them — no stored-XSS
  path via content.
- † **Static serving**: traversal clean (also independently parent-verified:
  stdlib `uri.path_segments` splits raw + RFC dot-segment removal, no
  percent-decode).
- **Referee forms** (`reference_checks/form_pages.gleam`): token (from URL
  path) is reflected into `href`/`action` values — Lustre escapes attribute
  values, and all URLs are relative (`/reference/...`) so no `javascript:`
  scheme injection is constructible; unknown token 404 "never reveals whether
  a token was ever valid"; expired/resend views take the same escaped path.
- **DSAR/erasure pages** (`dsar_handler`, `erasure_handler`): GET renders a
  static page with identical bytes for valid/invalid tokens (no token-validity
  oracle, no auto-fetch egress); POST-only data egress; referrer-policy
  `no-referrer` override respected by middleware (`with_default_referrer_policy`
  keeps handler-set values); used/unknown tokens → friendly 404.
- **CSP**: Report-Only in prod (I-1 in report); nonce minted per response,
  request-header stash overwrites client-supplied values; `deshare_cache`
  downgrades public→private on nonce-bearing bodies.

## Findings

| ID | Severity | Title | Location | Confidence |
|----|----------|-------|----------|------------|
| S-1 | Info | CSP `style-src 'unsafe-inline'` + `script-src https://connect.facebook.net` broaden the (currently report-only) policy | `csp.gleam:policy` | High (documented tradeoff) |
| S-2 | Info | `*.run.app` origin-suffix trust in the `origin_domain` allowlist — bounded to the project's own suffix (project-number-scoped); abuse requires project access (M-3 class) | `domain_helpers.validate_origin_domain` | High |

No Medium+ SSR findings. The rendering layer's escaping discipline held at
every sink walked.
