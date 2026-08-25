# Lens briefing — security-audit / DATA LAYER (SQL injection, FFIs, PII in logs/analytics, DSAR scope)

- **Job:** righttenantry-security-audit (mega-minion lens; parent minion audits the repo)
- **Model policy:** `deepseek/deepseek-v4-pro` (glm-5.3 provider-capped 429 code 1308 until 17:54:28Z — sanctioned fallback per the playbook's fallback chain; briefing override).
- **Repo/worktree (READ-ONLY):** `/Users/moses/.herdr/worktrees/RightTenantry/security-audit` @ develop (17d5f32)
- **Skill:** `bmad-review-edge-case-hunter` — exhaustive path enumeration, mechanism-only, every claim verified against disk.
- **Output:** write findings to `/Users/moses/code/_bmad-output/implementation-artifacts/righttenantry-security-audit/lens-data.md`, then end with a one-paragraph summary in your pane.

## Ground rules

- READ-ONLY: no edits, no commits, no installs. Do not spawn sub-agents.
- Stack: Squirrel-generated SQL (`server/src/<module>/sql/*.sql` → generated `<module>/sql.gleam`), pog (Postgres, Supabase transaction pooler), hand-written Erlang FFIs (`server/src/db@db_ffi.erl`, `payment@invoice_cache_ffi.erl`, `ai@audit_report_ffi.erl`, `auth@session_cache_ffi.erl`, `auth@reset_nonce_store_ffi.erl`, `server@signal_ffi.erl`). App connects with a privileged role; RLS is defense-in-depth only (auto-enabled, default-deny for anon).
- Evidence discipline: every finding = severity + `file:line` + trigger + consequence + remediation + confidence. Verified only; a false positive is a failure.

## Scope

1. **SQL injection inventory**: Squirrel parameterizes by design — audit every place that ISN'T Squirrel: grep all `.sql` files for string concatenation patterns, dynamic ORDER BY / LIMIT / identifier interpolation (pagination params interpolated as identifiers? sort columns whitelisted?), `fracture`/raw `pog.query`/`pog.exec` call sites, and EVERY Erlang FFI that touches SQL (read `db@db_ffi.erl` fully — how are queries built? iolists with interpolated values?). Also `$1::text::inet`-style double casts in sql files (safe? note any `$n` used inside string literals).
2. **Erlang FFI audit** (all six `*.erl` files): unsafe input handling (atom() from user input → atom exhaustion? binary_to_atom call sites), file writes (audit_report PDF generation — path traversal in report ids? injection into the PDF toolchain?), ETS usage (public tables — cross-process tampering within the BEAM is same-trust, but note world-readable file paths), process spawning (os:cmd? open_port?).
3. **PII in logs**: grep `wisp.log_info|log_warning|log_error` + `console.log`/`echo` across `server/src` — flag every call site that interpolates user data (emails, names, tokens, IPs, phone numbers, application content, subject lines) into logs (Cloud Logging). The codebase has a token-redaction discipline (`redact_token_route`) — verify coverage gaps: Sentry event builders (`sentry/sentry_client.gleam` — what goes into HttpErrorEvent/CrashEvent `headers`? CrashEvent sends raw request headers — auth headers redacted?), error paths that echo `resp.body` from third parties (Supabase bodies contain emails — `supabase.gleam` logs some bodies — enumerate all such log lines).
4. **Analytics payload leakage** (data egress): `posthog/posthog_client.gleam`, `meta/meta_client.gleam` call sites — which events carry PII (emails, names, vacancy addresses, application ids), consent gating before CAPI insert (#568/#583 prior art — verify current wiring on OAuth signup + apply submit + payment verify), IP forwarding (x-forwarded-for passed to Meta/PostHog?).
5. **DSAR/erasure scoping** (`dsar/dsar_handler.gleam`, `erasure/erasure_handler.gleam`, `retention/*`): does the DSAR export include ONLY the requesting applicant's data (co-applicant separation — co-applicant PII inside the export? referee PII?)? Token validation (entropy, single-use, expiry), export contents (any OTHER landlord's or referee's personal data reachable via joins — landlord name/address in the applicant's export is expected-ish; flag anything excessive), erasure completeness vs over-deletion (erasing shared rows affecting others).
6. **audit_log discipline** (`audit/audit_log.gleam`, `retention/audit_log_schema.gleam`): what's written on AI decisions/status changes/payments (must fire — verify call sites exist for payment unlock, status change, AI decision), PII in audit details (non_pii helper usage), pseudonymisation job coverage.
7. **Consent record integrity** (`consent/consent_handler.gleam`, application consent capture): can consent be forged/faked (applicant_ip recorded from where — X-Forwarded-For trust chain), does the SSR form record consent BEFORE storing PII (draft saves without consent? — draft_handler stores form data pre-consent: is that lawful/flagged?).
8. **Retention job** (`retention/retention_job.gleam`, `landlord_deletion.gleam`, `storage_purge.gleam`): what deletion misses (Supabase Storage orphans? Stripe data? audit_log pseudonymisation actually runs?), account deletion gating on pending payments — bypassable?

## Deliverable format

Markdown: summary, findings table (id, severity, title, file:line, confidence), one section per finding with trigger + evidence (code quotes) + remediation. Include a "logs that carry PII" inventory table (every call site + field) and verified-clean list.
