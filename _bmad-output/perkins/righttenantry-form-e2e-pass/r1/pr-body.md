## What

Two workstreams on one branch (test additions ride the migration PR per dispatch):

1. **Skill migration (user ruling — Claude Code retired):** all 18 tracked skill dirs moved `.claude/skills/` → `.pi/skills/` (pi's native project discovery location — no settings.json needed). `git mv` preserves history. Claude Code loses these skills by design; pi gains them natively.
2. **E2E full applicant journey verification pass** over the fully-upgraded form (F1 stepper + F4 field diet + F5 upload copy + RC1.2 attestation + F3 save-resume + W0 instrumentation + W1a copy) — plus the test-gap scenarios it surfaced.

## E2E pass result: **clean — no app defects**

Local Docker DB (full migration chain) + seeded vacancy + local server + dev-analytics-proxy; real Chromium, mobile 375×812 primary, desktop secondary. Evidence (screenshots, DB dumps, no-JS HTML, analytics capture notes, journey checklist) committed at `_bmad-output/implementation-artifacts/e2e-form-pass-2026-08-03/`.

| Journey step | Result |
|---|---|
| Arrival → 8 named stepper steps, prep block + F3-SEAM line, sticky mobile progress | PASS |
| Attestation gating — blocked without choice ("Choose one option to continue."), Yes advances | PASS |
| Documents — camera-roll image accepted, >5MB fails LOUDLY (r1 dead-end dead), per-slot helpers | PASS |
| Submit — §5.4 Yes-path line; application + `reference_contact_attestation` + IP/UA columns (IP empty locally by design: XFF absent; UA written) | PASS |
| Save-resume — debounced draft save on step-change (r2 fix live in real browser), continue-link, resume banner + full restore (date/select/radios), `resumed_at` stamped, submit from draft | PASS |
| No-JS fallback — SSR long form (all 8 sections, no hidden attrs), attestation radio posts, submit persists | PASS |
| Analytics — section funnel with stable `data-section-id`s; resume token in NO captured payload (r3/r4) | PASS |

**Baselines:** 58/58 form-bug-hunt scenarios (5 parallel runners; `closed-vacancy-url` covered separately via seeded closed vacancy; anti-fraud silent-accept verified at DB depth — 0 spam rows), `make test` green, 377 integration green BEFORE and AFTER (app code untouched between runs).

## Test gaps closed in this PR

- **`save-resume/round-trip.yaml`** (new category) + `save_resume_round_trip` runner key in SKILL.md — the F3 round trip the suite couldn't express: debounced saves, continue-link, local-DB token seam, resume restore, submit from draft. Verified end-to-end against the local stack.
- **Fixed pre-existing scenario defect:** `validation/missing-required-text-fields` had `consent: false` contradicting its own description — the disabled submit could never reach the server. Now `consent: true` per intent; re-verified (banner + all 7 inline spans).
- **Fixed runner trap:** the documented `{SCENARIO}` email template produced local parts with `/` that `shared/email.is_valid` rejects (hit by 3 independent runners). SKILL.md now documents slug sanitisation (`/`→`-`, ≤64 chars).

## Decisions & rationale

- **Migration scope:** only tracked dirs moved (18). The user's main checkout has additional *untracked* `.claude/skills/` locals (arize-*, bmad-* — gitignored here); those aren't in git and are out of this PR's reach. `.claude/launch.json` + `.claude/settings.json` left in place per ruling; historical `_bmad-output` docs keep old paths (history not rewritten). Living refs updated: both SKILL.mds' scenario/fixture paths, `.gitignore` fixtures exception, `scripts/dev-analytics-proxy.js` comment, `AGENTS.md` E2E bullet.
- **Follow-up (not fixed here, per ruling):** form-bug-hunt's agent-browser dependency lives machine-globally at `~/.claude/skills/agent-browser` — pi does NOT natively discover that path. The `agent-browser` CLI itself is on PATH and works regardless; moving/copying the global skill is a Gru-level decision.
- **Save-resume token seam:** the continue token is an emailed capability URL — no browser-observable surface by design. The new scenario documents a LOCAL-ONLY DB seam (read `continue_token` from the local test DB) and must be marked skipped on staging. The emailed URL correctness stays pinned by Perkins r1 tests.
- **Continue-link send in dev:** Resend 422s `example.com` recipients (sandbox rule); `delivered(+tag)@resend.dev` sends fine — the scenario email rides the Resend test sink with a `{RUN_ID}` tag so reruns stay unique.
- **Analytics verification method:** posthog-js `_is_bot()` drops all capture for HeadlessChrome UAs (automation artifact, not a defect) — assertions made by wrapping `window.posthog.capture` in-page and recording the call stream on both the fresh form and the resume render.
- **Empty `submitted_ip_text` locally:** `request_helpers.client_ip` reads X-Forwarded-For only; absent locally → `""` by design (columns tolerate it; Cloudflare sets XFF in production). Pinned by `gdpr_integration_test`.
- **Seed choice (0 free analyses, unpaid vacancy):** scoring gate blocks AI dispatch so the pass makes zero calls to the real ADK service.

Never merge — human reviews.

