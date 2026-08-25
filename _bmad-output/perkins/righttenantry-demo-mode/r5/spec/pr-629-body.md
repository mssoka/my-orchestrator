## Interactive landing demo (mock-data sandbox) — issue #628, Option B

**The goal:** a first-fold "Try the demo" CTA opens a fully clickable landlord dashboard seeded with believable mock data — mock vacancies, mock applicants with full AI reports, comparison view, downloadable mock reports. Everything a landlord does, **non-persistent** (refresh or reset wipes it), **ungated** (no signup).

### Lavish verdict (2026-08-19) — recorded verbatim

The demo-flow design went through the mandatory in-browser lavish gate (`_bmad-output/mocks/demo-flow-design.html`). Queue-button answers + annotations:

- **CTA moment — B: "Use CTA moment option: B - Persistent in banner"** — the in-demo CTA is persistent in the demo banner (not a felt-value-triggered moment).
- **CTA copy — annotation: "I don't know why this says real? also start your real vacancy? this should read better."** → copy revised from the briefing's "Start your real vacancy →" to **"Create your vacancy →"** (matches the dashboard's own "Create vacancy" button).
- **Analytics FFI — "Approve narrow FFI"** — the narrow one-function PostHog FFI ships in this PR (consent-gated, no PII).
- **Fixtures — "3 vacancies + 9 applicants (rich)"**.
- **Entry — "Hero CTA + navbar link"**.
- **Dashboard fidelity — closing message: "the demo dash, should match the actual dash"** → the demo renders the **real** view components (`dashboard.gleam`, `vacancy_card.gleam`, leaderboard, application detail, comparison) with mock data behind them — the mock is not a look-alike, it is the product.

### What shipped

**1. Demo entry + placement** — `/demo` (shareable, ungated route) reached from: a hero secondary CTA ("Try the demo"), a desktop-nav link, and a mobile-menu link on the landing page. Direct deep links work too (`/vacancies/v-maples` boots into the demo — the `v-` prefix identifies demo fixture ids; real UUIDs never match).

**2. Mock adapter (the seam)** — `client/src/demo/`:
- `demo_fixtures.gleam` — the fixture JSON (landlord, notifications, 3 vacancies, 9 applications), decoded **through the production `shared/` decoders** at seed time.
- `demo_store.gleam` — the pure in-memory store on the Model. **Derived, not serialized**: dashboard list, vacancy detail, leaderboard, application detail, comparison, archived list all compute on demand from one source of truth. Mutations (create/edit/archive/restore/close/publish, status changes, bulk-reject, reference-check actions, notifications) mutate the store; every surface re-derives consistently.
- `demo_api.gleam` — mirrors the real `api/*` signatures, dispatching responses through the **same `msg` constructors** (`ApiReturnedDashboardData(Ok(..))` etc.), so `update_inner`'s response handlers render the mock identically to a live response. The real api modules are **untouched** — zero regression surface on the live path.
- `demo_update.gleam` — the single demo-mode dispatch point (`update/2` routes here when `model.demo_mode`), plus ~20 tiny `case model.demo_mode` branches inside `update_inner` for response-side refetch side-effects (all marked `// demo:`).
- `components/demo_banner.gleam` — the persistent chrome: "Demo — nothing is saved", "Create your vacancy →", "↺ Reset demo".
- `demo_analytics.gleam` + `demo_analytics_ffi.mjs` — PostHog demo events (entry, reset, vacancy/app detail, comparison, report download, CTA click) behind the existing consent gate, no identify, no PII. **The narrow FFI was explicitly approved in the lavish verdict.**

**3. Fixture dataset (the craft)** — 3 vacancies: The Maples (Dublin 4, active+paid, 8 applicants across every score band), 2 Harbour Court (Galway, active+free-tier, 1 pending analysis), Sunningdale (Cork, archived). 9 applicants with believable Irish stories (product designer with co-applicant, first-time renter with character ref, self-employed plumber with guarantor, a possession-order cautionary tale, a pending-analysis "why pay" case), full-shaped AI reports (category scores, flags, positives, insight, disclaimer), documents, audit trails, reference calls. Synthetic on close inspection — `example.ie` emails, no real persons, protected characteristics never used as criteria.

**4. Mock downloads** — 8 report PDFs pre-baked **once** through the real Typst pipeline (`ai/audit_report.gleam` → `typst compile` on the production template + fonts; regeneration via `gleam run -m demo/pdf_prebake`), shipped as static assets (`server/priv/static/demo/`, whitelisted in `.gitignore`). Download buttons serve the static bytes — zero per-call AI/typst cost. Verified by vision-read: real 9-page branded reports.

**5. Demo chrome** — persistent banner, reset button, in-demo CTA (verdict B).

**6. Drift guard** — fixtures decode through the production decoders at seed **and** in `make test` (`client/test/demo/fixtures_conformance_test.gleam`), plus encode→decode round-trips of derived surfaces. A drifted API shape fails the build.

**7. Analytics** — see above.

**8. Non-persistence, proven** — demo state lives purely on the Model (re-seeded on every `/demo` entry and on reset); the store and all `demo/` modules make **no network calls** — enforced by a new CI grep lint (bans `rsvp`/`api_helpers` and any `gleam/fetch` outside the one documented static-PDF fetch in `demo_api.download`). A client test drives the demo through the real update path and asserts every request resolves.

### What was NOT built (flagged, per #628)
- No backend sandbox (Option A) — the real-backend sandbox is the named follow-up.
- No vendor demo tools (Option D), no isolated demo deployment (Option C).
- No Stripe/email/AI endpoint invocation from demo mode — payment surfaces are hidden in demo (settings link removed from the shell; both fixture vacancies are paid or free-tier-remaining so no unlock CTAs appear).
- No persistence of any kind; no gated entry.

### Decisions & rationale
- **Message-level demo dispatch instead of api-module edits** — keeps the real api modules byte-identical (zero regression on the live path); demo logic lives in one place and reuses `update_inner`'s response handlers (no duplicated handler logic). Cost: ~20 small demo branches in `update_inner` for response-side refetch side-effects.
- **Demo store on the Model (pure MVU)** — Gleam/JS has no module-level mutability; the store is re-seeded state. "Refresh = reset" and "Reset demo" fall out of the architecture.
- **"v-" prefix heuristic for deep-link demo boots** — a full-page refresh on a demo URL re-enters the demo; real UUIDs never collide. `ArchivedVacancies` deliberately excluded (ambiguous with the real page).
- **Direct-/demo boot doesn't use `modem.init`'s boot dispatch** (it doesn't dispatch at boot) — `init` enters demo mode itself, and `modem.init` still runs to install the SPA click interceptor.
- **PostHog FFI approved by the user** in the lavish gate (Q2) — one `capture(event, props)` call, fail-open, consent-checked inside, zero PII, mirroring the pre-approved `meta_pixel` bridge shape.

### Acceptance checklist
1. ✅ Ungated demo entry from the first fold; every landlord surface clickable in demo state (verified end-to-end in a real browser: dashboard → vacancy detail/leaderboard → applicant detail incl. AI report + documents + reference panel → comparison → download mock report → archive/restore → create/edit → reset).
2. ✅ Non-persistence proven — client test + CI grep lint (no network from demo/).
3. ✅ Lavish verdict recorded verbatim above (design artifact committed at `_bmad-output/mocks/demo-flow-design.html`).
4. ✅ `make test` green (shared 119, client 595, server 1527 + 549 skipped integration).
5. ✅ PR body: adapter design, fixture summary, CTA moment, citations (#628 + lavish verdict), what was NOT built.

No breaking changes: additive only (new route, new model fields, new modules; `shared/routes.Route` gained a constructor).
