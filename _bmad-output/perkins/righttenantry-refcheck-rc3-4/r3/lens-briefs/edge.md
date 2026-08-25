# LENS: edge (source tag: `edge`) — Perkins r3 refcheck

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing verification, output contract).

You are a pure **path tracer**. Do not comment on whether the code is good or bad — list ONLY unhandled paths reachable from the changed lines (the `initReviewSubmit` seam + the 4 new tests).

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself. Examples relevant to this seam:
- `initMs` stamped at seam-init; what if submit fires in the SAME tick (0ms → "0")? is that intended?
- `env.Date` absent → falls back to `Date.now()` (browser global) — but in the test fake, `env.Date` is always present. Is the no-`env.Date` branch reachable/dead in practice? (note, not blocker)
- `focusField` captured by closure at bind time; what if the DOM is re-rendered after bind (the field node is replaced)? Would `focusField.value =` write to a detached node?
- The seam finds the form ONCE; if `reference-review-form` is not in the DOM at DOMContentLoaded (async render) it bails — but this is server-rendered SSR HTML, so it's present. Confirm.
- The submit listener has NO `event` param — confirm it genuinely cannot throw on a real submit event (no property access on an undefined event).
- `clampFocusSeconds`: NaN/negative/infinite → "0"; very large ms → could `String(Math.floor(...))` exceed Number.MAX_SAFE_INTEGER precision? (page-load + years — implausible, note at most)
- Double-submit / rapid re-entry: the listener sets `focusField.value` synchronously each time — idempotent, fine.
- Race: `initMs` uses `env.Date.now()`; if the clock is mocked/non-monotonic the value could go negative → floored to "0" (safe).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard; discard handled ones silently. No editorializing.

**OUTPUT:** write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/edge.json`. `source` must be `"edge"`. `[]` is valid.
