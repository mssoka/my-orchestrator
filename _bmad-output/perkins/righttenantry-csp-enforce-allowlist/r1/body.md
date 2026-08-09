## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-csp-enforce-allowlist · **Reviewed sha:** `6b6ba477` · **Reviewers:** 7/7 completed
**Verification:** 3/3 findings confirmed against the code — 0 discarded as false-positive

### Blockers (0)

### Warnings (1)
- **Hardcoded volatile Cloud Run host has no config/drift guard despite admitted brittleness** [blind] — `server/src/csp.gleam:121` — `connect-src` carries `mpc2-prod-23-is5qnl632q-ue.a.run.app` hardcoded; the doc comment itself admits it changes if the sGTM container is ever recreated. Verified: only `CSP_ENFORCE` is env-driven in this module; no drift guard. Mitigations in place: the staging Sentry soak before the prod flip would surface a changed-host violation, and the PR body lists this under open questions. Spec-sanctioned comment-only approach — follow-up, not merge-blocking. _Fix: accept as documented follow-up, or drive from env/config with a drift test when the container is next recreated._

### Notes (2)
- **Regional Google pixel domains only partially allowlisted by the diff's own admission** [blind] — `server/src/csp.gleam:119` — only `google.ie` + `google.com.gh` added; doc comment + PR body flag that `google.co.uk`, etc. will surface per-country. Spec-sanctioned narrow-allowlist posture; each is a one-line addition. Track the remainder as a bead/issue.
- **Advisory test gate: PASS** [tests] — `server/test/csp_test.gleam:policy_allows_enforcement_additions_test` — all 4 additions (5 tuples) asserted bound to their full directive line, exactly once (split-length 2), in **both** nonce and empty-nonce branches; well-formedness guards (no trailing `;`, no `;;`, no `*`, no `'unsafe-eval'`). Ran `make test-server`: **1185 passed, 0 failures** (7/7 CSP tests); client suite 107 pass. Optional hardening: negative assertions that the three rejected hosts stay absent.

### Reviewer agreement
No multi-source findings. Independent verification pass (my own) covered the three investigation items:
- **RT-PROD-D** (AWS ECS host) — confirmed parked: host referenced nowhere in the codebase; the public unauthenticated report endpoint forwards any parseable body → junk-report class holds.
- **RT-PROD-9** (bare `properties`) — confirmed junk: no code path builds it; not a resolvable browser target.
- **RT-PROD-5** (self-origin) — confirmed junk: `'self'` in script-src verified; www→apex 301 redirect verified in `cloudflare-redirects.tf` (`redirect_ie_www_to_apex`) with `http_origin.gleam` server-side fallback.

CSP string well-formedness verified by direct read of `policy/1` and the new test: no trailing semicolon, no `;;`, quotes balanced, no wildcard slipped in.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
