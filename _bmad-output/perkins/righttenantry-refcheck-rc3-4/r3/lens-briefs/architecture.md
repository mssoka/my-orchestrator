# LENS: architecture (source tag: `architecture`) — Perkins r3 refcheck

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing verification, output contract).

Architectural fit of the `initReviewSubmit` seam. Verify against the surrounding `reference_form.js`:
- Does it follow the EXISTING pattern? Compare to `initBrowser`: same env-injection seam shape (`function initX(env) { env = env || root; var doc = env.document; if (!doc) return; ... }`), same `clampFocusSeconds` reuse, same CommonJS export under `_`-prefix (`_initBrowser`, `_initReviewSubmit`), same top-level init wiring (DOMContentLoaded + immediate). Drift from this pattern is a finding.
- Does it duplicate logic? `clampFocusSeconds` is correctly shared (not re-implemented). The `initMs`/`currentFocusSeconds` clock is re-implemented inline rather than hoisted/shared — is that a justified narrow scope (the review page is a separate lifecycle from the per-question accumulator) or needless duplication? (The per-question clock is scoped inside `initBrowser` and not exported, so the seam cannot reuse it without a refactor. Weigh: small inline clock vs. a larger hoist. Likely fine — note at most.)
- Does it respect the module boundary (progressive-enhancement JS stays out of server logic; no FFI; no Gleam coupling beyond the `data-testid`/`data-focus-seconds` contract already established by `view_review`)?
- Does it introduce coupling that makes future changes harder? (e.g. two clock sources that could drift.)
- Complexity vs. problem: is the seam the simplest correct fix, or over-engineered? (It's ~13 lines — likely minimal.)
- Does the seam's "find form, bail if absent, bind submit, no preventDefault" structure match the project's capability-gate philosophy (graceful no-op when the element/capability is absent)?

**OUTPUT:** write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/architecture.json`. `source` must be `"architecture"`. `[]` is valid.
