- `odin test app` runs only the app package's tests (46); the render pins live under `odin test app/render` (83) — a deliberate-fail probe is the cheap way to confirm a test binary actually executes your new test before trusting a green run.
- tools/derive_a11y_palettes.py cannot parse palette.json's inline `//` comments (json.load) — run it on a comment-stripped copy; pre-existing breakage worth an issue.
- The old CVD mode tables remapped route_tie to pale amber RGB-identical to state_congested's remap — a11y overrides can silently reintroduce a base-palette collision you just fixed; always diff the mode tables too.

# r2 fixes (2026-08-25, Perkins r1 NEEDS CHANGES)

- The r1 "mutation leg" passed because the pin covered the PREDICATE, not the draw path — a pure-proc pin is bypassable at the call site no matter how good it is; the closure was a palcheck pixel scan of the REAL render (ECMP diamond topology + preview_compute + draw_route_glow, mid-angle sampling against tie_dash_on) — render tests alone still pass under the bypass, palcheck is the gate that fails.
- Odin has no #error directive — the compile-time assert idiom is `when <bad> { BROKEN :: 1 / 0 }` (constant division by zero = compile error, proven by mutation leg 3).
- palcheck sections can do full live-render checks (ClearBackground + draw_route_glow + LoadImageFromScreen) without touching goldens — the "harness capture path never invokes assists" doctrine applies to golden CAPTURES, not to analysis renders.
