# righttenantry-demo-polish-2 field notes

- Toast mismatch root cause = PRODUCTION STALENESS, not demo code: prod
  bundle ships pre-#615 `fixed bottom-4 right-4 z-50` (main last merged
  Aug-10, 36 commits behind staging); demo/staging/develop all render
  `fixed top-20 right-4 z-[2147483001]` through the ONE shared toast
  component. Grep the deployed client.js for the position class — that IS
  the runtime truth; component-level parity checks (polish-1's) can't see
  a stale deploy. Matching prod would regress the #615 banner guarantee.
- polish-1's "real twin" verdicts failed the same way twice: verify the
  DATA feeding a render gate, not the gate's existence. Compare-top-3 hid
  because demo_store set `score_based_rank` = overall SCORE (86, 78...)
  instead of competition rank (1..8) — `top_three_ids` needs rank in
  {1,2,3} so the button never rendered. Port the server's competition_ranks
  + score-DESC-NULLS-LAST ordering (application_list_handler.gleam) into
  the demo store.
- Real demo PDF depth came from data, not the template: the typst template
  already renders Analyst's Brief/Category Notes/Recommendations/Scoring
  priority — they were absent because pdf_prebake's extras lacked
  detailed_insight/category_notes/recommendations/category_weights.
  Evidence items carry a `structured` BOOL — don't decode them as
  string-dicts in tests (gleam_json 3.x Json is opaque; parse with
  decode.field chains). Keep screen↔PDF consistent: same flags arrays in
  demo_store analysis_for AND pdf_prebake payloads; co-applicant income
  must not double-list as an additional income source.
