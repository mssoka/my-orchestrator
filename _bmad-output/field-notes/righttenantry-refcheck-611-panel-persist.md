# Field notes — righttenantry-refcheck-611-panel-persist

- The issue's root-cause theory (Lustre `decode2` → `DispatchedEvent` swallow) was WRONG — instrument the compiled bundle in a live browser repro (add console.log to `decode2`/`dispatch2` in `server/priv/static/client.js`, restart server) before trusting a runtime-layer diagnosis; the real bug was a view-level dict-key mismatch (`text_input(slot, …)` vs `dict.get(edit, call.reference_call_id)`), a 3-line app fix.
- `lustre/dev/simulate` (with the REAL `client.update` + page view) is the runtime-faithful pin harness — `simulate.input` drives `cache.handle` → decode2 → update → view with zero DOM; negative-control it (revert fix → red) before trusting it.
- Rebasing onto origin/develop after the sibling merged was clean (disjoint areas), but re-ran the FULL suite + lint gates afterwards — em-dash lint now scans 125 files post-#612; test files aren't in its scope.
