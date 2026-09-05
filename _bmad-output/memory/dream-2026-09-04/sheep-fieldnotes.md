# sheep-fieldnotes

Sources: 8 shards, window 2026-09-02T22:38Z → 2026-09-04T23:58Z. Note: the
brief's filename `packet-plumber-v2-viscomm-tie-deconflect.md` does not
exist — actual shard is `...-tie-deconflict.md` (read in full regardless).

## Candidates

### 1. `ledger pr` BEFORE `set in-review` — the guard now fires on minions in the wild
- **Evidence**: packet-plumber-3d-gdd-v1, 2026-09-04: "it REFUSES unless the
  `pr` field is already set — run `bin/ledger pr <id> <url>` FIRST, then
  `set in-review`". righttenantry-agents-prod-scale-to-zero, 2026-09-04:
  "the natural order is backwards: run `ledger pr <id> <url>` BEFORE
  `set in-review` (error is loud, no harm, but it's a guaranteed re-run
  otherwise)".
- **Why it recurs / rule**: the 2026-08-18 ledger guard works exactly as
  designed, but two different crews (PP, RT) hit it the same day because
  the pr-first order is counterintuitive and lives only in gotchas. Rule:
  bake the sequence `ledger pr → set in-review` into briefing templates /
  minion standing orders so the guard becomes noise, not a re-run.

### 2. Prove the test can FAIL before trusting green (deliberate-fail probes + negative controls)
- **Evidence**: packet-plumber-v2-viscomm-tie-deconflict, 2026-08-25: "a
  deliberate-fail probe is the cheap way to confirm a test binary actually
  executes your new test before trusting a green run". righttenantry-
  agents-prod-scale-to-zero, 2026-09-04: "prove with a negative control
  (revert the value → suite must FAIL)".
- **Why it recurs / rule**: the mutation-leg doctrine (Perkins side) has a
  minion-side twin: any new test or guard needs one demonstrated red before
  its green counts. Cross-lane (Odin render tests, RT tfvars extractor
  regexes). Rule: no green is trusted without a witnessed red — cheap, one
  command, catches non-executing tests and vacuous assertions.

### 3. Gate on the real output surface, not the predicate
- **Evidence**: tie-deconflict r2, 2026-08-25: "render tests alone still
  pass under the bypass, palcheck is the gate that fails" (a pure-proc pin
  was "bypassable at the call site"). packet-plumber-3d-e1-tiny-planet,
  2026-09-04: "Always verify pose changes with a SCREENSHOT, not just
  transform asserts". packet-plumber-3d-e2-flow-qos, 2026-09-04: "Caught by
  white-box probe before first suite run".
- **Why it recurs / rule**: predicates and unit-level asserts verify the
  mechanism, not the observable; bypasses and engine-coordinate surprises
  (global-vs-local camera coords, wrong hemisphere) live between them. The
  vacuous-pin blocker class extends into the 3D lane unchanged. Rule: the
  acceptance gate for visual/geometry/flow claims is the end artifact
  (pixel scan of a real render, captured screenshot, probe against the
  live admission path) — everything weaker is a sanity check, not a gate.

### 4. A value lives in ≥2 places — census ALL encodings before any flip
- **Evidence**: tie-deconflict, 2026-08-25: "a11y overrides can silently
  reintroduce a base-palette collision you just fixed; always diff the
  mode tables too". scale-to-zero, 2026-09-04: "a value flip without the
  pin flip = red suite on the NEXT unrelated PR … it detonated on the
  #177 promote" (RT pins terraform values in tests/unit/test_concurrency.py).
- **Why it recurs / rule**: production values get mirrored into test pins
  and override/compat tables, and the mirror detonates later on an
  unrelated PR. Cross-repo (PP palette modes, RT tfvars test pins). Rule:
  before flipping any config value, grep the test suite AND all override /
  mode tables for the old value; flip them together or not at all.

### 5. Measure, don't trust metadata or competing quotes
- **Evidence**: packet-plumber-3d-asset-scout, 2026-09-04: "authoring
  scales ranged 0.08x–25x across sources … normalize by MEASURED world
  bbox". dream-2026-09-02: "Verify contract numbers against the repo,
  never pick a winner from two quotes" (max_span 10-vs-14/16/18 resolved
  against data/pipe_tiers.json — 10 was the DISABLED tier).
- **Why it recurs / rule**: third-party asset metadata and remembered
  numbers are unreliable in both directions; the repo's canon file or a
  direct measurement is the only ground truth. Rule: numbers and scales
  get re-derived from the source (canon JSON, measured bbox carried in
  explicit scene metadata like `PP3D_NormalizedScale`), never quoted from
  memory or picked between claims.

### 6. Godot editor surface is its own failure class, orthogonal to game-run
- **Evidence**: e2-flow-qos, 2026-09-04: "Godot EDITOR windows at macOS
  off-screen positions (-3000) freeze to a 2x2 viewport texture (game
  windows render fine there)" and "non-tool scripts attached to scene
  nodes are PLACEHOLDER instances in the editor". e1-tiny-planet,
  2026-09-04: "nodes added during `_initialize` aren't inside the tree
  yet — run the suite on the first `process_frame`" and "Any pre-quit
  crash = engine hangs forever".
- **Why it recurs / rule**: the PP 3D lane will keep hitting
  editor-vs-runtime divergence: @tool gating, editor viewport capture
  (`EditorInterface.get_editor_viewport_3d(0)`), SceneTree `-s` lifecycle,
  engine hangs on runner crashes. Rule: editor-path verification and
  headless/runtime verification are separate legs — plan both, never
  assume one covers the other; null-guard every `load()` in runners so a
  crash fails loud instead of hanging.

### 7. Dream sheep must read the ledger DB directly — catches record loss journals miss
- **Evidence**: dream-2026-09-02: "independent DB reads caught the EMPTY
  review anchor in a close-out note AND that a minion's 'dispatch add was
  missing' self-create claim was FALSE (the row existed under the long
  id)" — "Small windows still earn sheep (2nd dream)".
- **Why it recurs / rule**: minions' prose claims about ledger state
  (self-create, anchors) are unreliable, and close-out notes truncate
  URLs; only the DB is ground truth. Two dreams running. Rule: keep the
  DB-reading sheep in every dream regardless of window size; treat
  minion-claimed ledger facts as allegations until DB-checked.

## Watch items

- **pi `edit` is atomic across the whole edits[] array** — one failed
  oldText silently rolls back ALL edits ("caught by re-grep"). Re-grep
  after every multi-edit apply. (gdd-v1, 2026-09-04)
- **"already in managed-repos.txt" can mean the orchestrator root's LIVE
  uncommitted tree** — verify the live checkout before treating it as a
  missing record; phrase doc refs as "recorded", not "committed". (p4-p5,
  2026-08-31)
- **`herdr notification show` `shown:false` = relay busy → retry once,
  then escalate**; the exact `shown:true` JSON paste is the checklist-gate
  proof shape. (p4-p5, 2026-08-31)
- **`herdr pane split` REQUIRES `--direction`** — bare split's RC is
  masked by parse pipes; "3 'failed' splits created ZERO panes" — verify
  via agent list before assuming debris. (dream-2026-09-02)
- **Keywalled-API scouting fallbacks**: Poly Pizza embeds full search JSON
  in `window.__SERVER_APP_STATE__` + GLBs at static URLs; tri counts via
  HTTP-range fetch of just the GLB JSON chunk; Sketchfab model API is
  public with thumbnails at `.thumbnails.images[].url` (not `.urls`).
  (asset-scout, 2026-09-04)
- **Odin idioms**: no `#error` — compile-time assert is `when <bad> {
  BROKEN :: 1 / 0 }`; test scope matters (`odin test app` ≠ `app/render`).
  (tie-deconflict, 2026-08-25)
- **RT repo facts**: tfvars PRs are merge-inert (deploy workflow path
  filter excludes `deployment/terraform/**` — state "merge ≠ prod change"
  in the PR body); pre-commit builds a uv `.venv` (~1 min) even on
  tfvars-only commits — bootstrap, not a hang. (scale-to-zero, 2026-09-04)
- **Bursty admission needs persistent deficit CREDIT (banked reserve)** —
  per-tick allowance alone starves packets larger than one tick's budget.
  (e2-flow-qos, 2026-09-04)
- **derive_a11y_palettes.py can't parse palette.json `//` comments** —
  run on a comment-stripped copy. (tie-deconflict, 2026-08-25)
- **Lavish: first `poll --agent-reply` returns only the dom_snapshot** —
  re-poll to actually wait for feedback. (gdd-v1, 2026-09-04)
- **Godot micro-traps**: icosphere Kahler table is CW = back-facing (swap
  two verts, let generate_normals follow); GDScript has no `%e`;
  INFERENCE_ON_VARIANT is an error by default; never `.free()` RefCounted.
  (e1, 2026-09-04)
- **Sheep brief listed a nonexistent shard filename** (deconflect →
  deconflict) — briefs should glob-resolve shard paths against the
  filesystem before handing to sheep. (this dream, 2026-09-04)
