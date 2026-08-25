# Lens briefing — security-audit / SSR + RENDER (XSS, CSP, HTML construction, public forms)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `zai-coding-cn/glm-5.3` (probe-confirmed back up post cap reset; the user-required model for this audit).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-adversarial-general` — cynical posture; every claim verified against disk.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-ssr.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs. Do not spawn sub-agents.
- Stack: server-side rendered public pages (Lustre `element` trees → HTML): `/apply/:code` SSR form (submit, draft save/resume/erasure), `/reference/:token` referee forms, legal pages, marketing content pages, `/dsar/:token` + `/erase/:token` confirm pages. CSP via `server/src/csp.gleam` (report-only or enforced? check), per-response nonce injection in `middleware.inject_csp_nonce`.
- Evidence discipline: every finding = severity + `file:line` + exploit sketch + remediation + confidence. Verified only; a false positive is a failure.

## Scope

1. **HTML escaping integrity**: Lustre escapes text nodes and attribute values by default — find every place that bypasses it: `lustre/element/html.raw` (or `html.unsafe`/`raw_text` — grep the actual API usage), `string_tree`, direct `bytes_tree` responses, `ssr_response.gleam`, any hand-built HTML string concatenation (`<>` with user data into markup). For each sink, trace the source (user input via form fields, query params, DB values — applicant names, referee answers, landlord names, vacancy fields, resource slugs/content).
2. **Attribute/context injection**: user data into `href`/`action`/`src` (javascript: URLs — referee links, continue-links, resume links), into `<script>` JSON blocks (server-side data blobs for the form — `form_data` embedding draft values? breaking out of a JS string → XSS), into CSS, into URLs (redirect endpoints — `handle_redirect`).
3. **The public apply form** (`application/*`: `application_handler`, `form_pages`, `form_view`, `form_question_pages` if present, `draft_handler`): reflection of submitted values on error re-render (persisted user input re-rendered — escaped?), honeypot + timing anti-fraud (client-side seconds field — server validates or trusts?), consent record integrity, file input rendering, `novalidate` posture.
4. **Referee forms** (`reference_checks/form_*`, `form_handler`, `questions`): token in URL rendered anywhere (reflected token), answers reflected, wrong-person/decline/stop flows.
5. **DSAR/erasure pages** (`dsar/dsar_handler`, `erasure/erasure_handler`): what's reflected (token? email?), referrer-policy no-referrer claims (verify), auto-fetch guards on GET, POST-only data egress.
6. **CSP** (`server/src/csp.gleam` + middleware wiring): policy directives (script-src with nonce — any 'unsafe-inline' leftovers? default-src; object-src; base-uri; frame-ancestors; form-action), report-only vs enforced per environment, nonce uniqueness per response, nonce leakage into logs/caches (deshare_cache logic), Google Fonts/PostHog/Meta allowlist breadth, `robots`/`llms.txt` info leak.
7. **Content pages** (`content/content_handler` + content sql): resource slugs and post content come from the DB — who authors them (seeded? admin?) and is stored XSS possible via any write path that feeds these pages (is there ANY user-writable content rendered raw?).
8. **SPA shell serving** (`serve_spa_shell`, `fallback_shell`): cache-control on nonce-bearing shell, `serve_static_file` traversal filter (`["static", ..rest]` filters `..`/`.` segments — try to defeat: encoded slashes `%2F` producing `/` inside a segment after decode? empty segments? backslash on the joined path? absolute-looking filenames? case tricks on index.html guard). Check `wisp.path_segments` decoding behavior in the vendored wisp source (`build/packages/wisp/`) to ground the verdict.

## Deliverable format

Markdown: summary, findings table (id, severity, title, file:line, confidence), one section per finding with exploit sketch + code-quote evidence + remediation. List verified-clean surfaces (escaping audit trail: which render modules you walked and found safe).
