# Briefing — righttenantry-demo-mode (landing demo sandbox, mock data)

- **Job id:** `righttenantry-demo-mode`
- **Repo:** RightTenantry · **Base:** `develop` @ fresh head at dispatch (Silas
  resolves) · **Slug:** `demo-mode`
- **GitHub issue:** #628 (research + design live there — read it first). Carry
  `github_issue=628` into the ledger row.
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any
  mega-minion you spawn launches with the same model — name it explicitly at
  every spawn.
- **Skills policy:** `bmad-quick-dev` (client feature work);
  **`lavish` is MANDATORY — present the demo-flow design for the user's
  in-browser verdict BEFORE the PR opens** (mock-data story, demo chrome,
  CTA placement + moment; iterate on annotations). `project-context.md` /
  AGENTS.md for code conduct.
- **Perkins:** `pr_review: 1` (public-facing marketing surface + client API
  seam). **Loop ruling (user, 2026-08-17):** rounds run UNTIL APPROVED.
  Reasoning tier = kimi k3 (user ruling 2026-08-18 night; probe-first at
  dispatch, guards armed).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr righttenantry-demo-mode <url>` yourself.
- **CANON CONTEXT:** issue #628 (conversion research + the 4-option analysis —
  this job IS Option B); `client/src/api/` (the seam the mock adapter
  replaces); `shared/` decoders (the drift guard); `client/src/pages/` landing
  + dashboard + application_detail* (the surfaces the demo lights up);
  `make test` discipline (test-shared/test-client/test-server/test-js); the
  existing consent gate + CSP nonce pattern (demo chrome must respect both);
  the 2026-08-18 security-audit findings (no new backend surface is part of
  WHY Option B was chosen — honor it).
- **CI:** `make test` green — local suite is the merge ground truth.

## Mission — build the interactive landing demo (mock-data sandbox)

**The goal (user, 2026-08-18 night — "let's work on the RT demo. mock
data."):** a first-fold "Try the demo" CTA on the landing page opens a FULLY
CLICKABLE landlord dashboard seeded with mock data — mock vacancies, mock
applicants with believable AI scores/reports, comparison view, downloadable
mock reports — everything a landlord does, **non-persistent**. Ungated entry.
The point: RT's first paying customers feel the product before paying.

**Deliverables:**

1. **Demo entry + placement:** first-fold CTA on the landing page → the demo
   dashboard (a dedicated route, e.g. `/demo`, so it's shareable). Ungated.
2. **Mock adapter:** a demo-flagged path swaps `client/src/api/` calls for an
   **in-memory store** seeded with fixture JSON. Create/edit/archive vacancy,
   applicant detail (AI report, documents, audit trail), comparison — all work
   locally in SPA state. Refresh = reset; "reset demo" button is trivial.
3. **Fixture dataset (the craft):** believable Irish-rental mock data — 2–3
   vacancies (varied states), 6–10 applicants across score bands with
   full-shaped AI reports, documents, reference statuses. Realistic names/
   addresses/prices; obviously synthetic on close inspection (no real persons).
4. **Mock downloads:** pre-bake report PDFs ONCE through the real Typst
   pipeline from the fixtures; ship as static assets; the download buttons
   serve them. Zero per-call AI cost, ever.
5. **Demo chrome:** persistent banner ("Demo — nothing is saved"), reset
   button, and the in-demo CTA — "Start your real vacancy →" — surfaced at the
   felt-value moment (e.g. right after a mock report download / score view;
   the lavish gate picks the exact moment).
6. **Drift guard:** fixtures typed against `shared/` decoders so the mock
   can't silently rot as the real API evolves — compile-time + `make test`
   conformance.
7. **Analytics:** PostHog demo-flagged events behind the existing consent
   gate — no identify, no PII — capturing entry, key surfaces, downloads,
   CTA clicks.

**Acceptance:**

1. Ungated demo entry from the first fold; every landlord surface clickable in
   demo state (create/edit/archive vacancy, applicant detail incl. AI report +
   documents, comparison, download mock report).
2. Non-persistence PROVEN: refresh and reset both wipe demo state; demo mode
   issues **no writes to real endpoints** (test or documented proof — network
   assertions in a client test).
3. Lavish verdict recorded verbatim in the PR body (the approved demo-flow
   design is what shipped).
4. `make test` green incl. the demo conformance coverage.
5. PR body: the adapter design, the fixture dataset summary, the CTA moment,
   citations (#628, lavish verdict), and explicitly what was NOT built
   (backend sandbox, vendor tooling).

**Scope guard:** client-side demo mode ONLY. No backend route changes, no new
backend surface, no Stripe/email/AI endpoint invocation from demo mode, no
vendor tools, no gated entry, no persistence of any kind. The real-backend
sandbox (Option A from #628) is a named follow-up — FLAG, don't build.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: demo-mode
base: develop
model: deepseek/deepseek-v4-flash
pr_review: 1
github_issue: 628
```
