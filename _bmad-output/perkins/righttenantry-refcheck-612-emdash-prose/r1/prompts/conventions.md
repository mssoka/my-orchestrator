## PROJECT CONVENTIONS — RightTenantry

Gleam/Lustre monorepo: `shared/` (types + JSON codecs), `client/` (Lustre SPA, landlord dashboard), `server/` (Wisp/Mist API + SSR public application form).

- **Em-dash ban (2026-08-05 user ruling; hardened by #612):** no U+2014 em dash in ANY landlord/applicant-facing copy. Enforced by `scripts/lint_em_dash.py` (CI) + `client/test/copy_test.gleam` `no_em_dash_test` + pinned const tests. Developer-facing log/telemetry call arguments are the only exemption.
- **Brand voice:** calm confidence, contractions ("couldn't", "it's"), never expose raw server/API error strings, never "Error"/"Failed" — use "Couldn't"/"Something didn't work". Toasts one sentence. All landlord-facing strings live in `client/src/copy.gleam`.
- No JavaScript FFI. No `let assert` in production code (tests only). Explicit HTTP timeouts on outbound calls. All data from DB via API (no hardcoded data).
- Squirrel for type-safe SQL (`server/src/<module>/sql/*.sql` + `bash run_squirrel.sh`).
- Tests: gleeunit (client, shared), unitest (server). `make test` = unit tests; integration tagged and separate.
- Scope discipline: PRs do one thing; no unrelated changes.
