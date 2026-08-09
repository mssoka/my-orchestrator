## 🤖 Perkins automated review — round 1 of 3
**Job:** righttenantry-csp-posthog-allowlist · **Reviewed sha:** b37c2d7 · **Reviewers:** 7/7 completed
**Verification:** 2/2 findings confirmed against the code — 0 discarded as false-positive

### Blockers (0)

None.

### Warnings (0)

None.

### Notes (2)

- **[tests] No CSP test asserts eu.posthog.com stays absent** — `server/test/csp_test.gleam:128-135`. The suite pins presence of intended sources (contains + exactly-once) and well-formedness, but never asserts `eu.posthog.com` is absent; appending it to a directive line end would pass every existing check. Optional hardening: `p |> string.contains("eu.posthog.com") |> should.be_false` in the enforcement-additions loop would lock the documented absence in as an invariant.
- **[tests] Advisory test gate: PASS** — comment-only diff; zero behaviour changes; existing tests pin every directive line + exactly-once + no-wildcard/eval.

### Reviewer agreement

No multi-source findings (no two reviewers independently flagged the same item).

### Review verification notes (Perkins, on top of the lenses)

- **No-op confirmed at the byte level:** `server/src/csp.gleam` minus `///` comment lines is byte-identical to `origin/develop` (`diff` after stripping comment lines → empty). All CSP directive values (`script-src`, `connect-src`, `img-src`, `style-src`, `frame-src`) and the nonce case-branch are untouched.
- **Comment's factual claims verified against the code:**
  - `ui_host:'https://eu.posthog.com'` present in all three inits: SPA shell (Makefile/Dockerfile RT_ANALYTICS snippet), `/apply` form (`server/src/application/form_view.gleam:265`), content pages (`server/src/content/tracking_snippets.gleam:66`). ✓
  - `api_host:'/_ph'` same-origin proxy in all three inits; the ad-blocker rationale is documented at `form_view.gleam:220-221`. ✓
  - SDK script loads from `/_ph_assets/static/array.js` (`server/src/posthog/posthog_js_snippet.gleam:23`, Makefile/Dockerfile `<script defer src="/_ph_assets/static/array.js">`); both `/_ph` and `/_ph_assets` are same-origin, covered by `'self'`. ✓
  - Toolbar is not enabled anywhere in production code (no toolbar config; only `opt_out_capturing_by_default:true` + consent listener). ✓
- **Lens-guard honoured:** no lens flagged the intentional absence of `eu.posthog.com` as a defect — it is user-ruled correct.

**Verdict:** READY TO MERGE

_No-op doc-comment PR (user-ruled Q3): the reviewed change is comment-only by design; eu.posthog.com is intentionally absent._
