# sheep-shards — candidate patterns (dream-2026-08-27)

Sources: 11 field-note shards, jobs 2026-08-24 → 2026-08-27 (PP v2 viscom/arch chain, dublin map/spawn, RT watermark + rents, DSH dashboard leftover).

## C1 — Suppressed-output build commands run a STALE binary (masked-rc trap)
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-25 — "the masked-rc trap bit THREE times in one job: `odin build ... | head` and `2>/dev/null` both hide build failures and re-run a STALE bin/harness (once 'confirming' a mutation leg that hadn't compiled, once 'passing' palcheck)"
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 — "a deliberate-fail probe is the cheap way to confirm a test binary actually executes your new test before trusting a green run"
- Note: after ANY suppressed-output build command, the rc captured must be the BUILD's rc, not the pipe's — and rebuild before trusting any binary run; a deliberate-fail probe proves the test binary runs the new test. Generalizes beyond Odin (any `build | head`).

## C2 — Odin procs do NOT capture enclosing scope (3 bites, 2 jobs)
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph 2026-08-25 — "Odin proc literals do NOT capture enclosing locals — bitten twice in one job (palcheck render/count closures): write file-level helper procs with explicit params, never inline `proc` values over loop/config locals"
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "Odin nested procs do NOT capture the enclosing scope — pass the struct pointer as an explicit parameter (the seg-grid builder bit once)"
- Note: recurring PP trap; the fix idiom is always file-level helpers with explicit params/struct pointers.

## C3 — Vacuous-pin craft facets (extends the 2026-08-23 mutation-leg doctrine)
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-26 — "an `|| true` inside an expect is a vacuous pin wearing a seatbelt (shipped one AGAIN, caught again — grep every new expect for it)"
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-26 — "never re-derive the 'before' value inside an assertion AFTER mutating the fixture — capture it before"; "`pop()` removes the LAST row — resolving a specific crisis in a fixture needs swap-remove"
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 (r2) — "the r1 'mutation leg' passed because the pin covered the PREDICATE, not the draw path — a pure-proc pin is bypassable at the call site"
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "a clamp-at-100 util read needs an ASYMMETRIC fixture (60/30) — a saturated both-directions fixture cannot discriminate max from sum"
- Evidence: packet-plumber-v2-dublin-spawn-director 2026-08-24 — "every new director pin needs its mutation leg (uniform-pick mutation caught the vacuous ratio test — caps bound the sample at step level, so pin the exclusion not the ratio)"
- Note: amendments to the existing mutation-leg law: grep new expects for `|| true`; capture "before" pre-mutation; swap-remove (not pop) to remove a specific row; asymmetric fixtures to discriminate max-vs-sum; pin the draw path/call site, not the predicate; pin the exclusion, not the derived ratio.

## C4 — Verification must bind to an independent anchor (self-confirming loops)
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-25 — "enumerate crisis state AT THE CAPTURE TICK, never from demo comments" (golden-set predictions came from stale 4.2-era captions)
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "the bake's --verify PASSED because it compared the same buggy output twice" (polygonize shadowing returned nothing for a full round)
- Evidence: packet-plumber-v2-arch-latency-egress-queue-model 2026-08-26 — "`bandwidth_demand` is catalog-loaded but UNWIRED (zero consumers) — never cite a catalog knob in a formula without grepping consumers; 'documented in the loader comment' ≠ consumed"
- Note: three flavors of self-confirmation — stale captions, a verify that compares its own output to itself, documented-but-unconsumed knobs. Anchor verification to an independent source (capture-time state dump, second derivation, consumer grep).

## C5 — The user iterates on MOCKS fast: parameterize the mock tool + KYLE per round
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 — "the user iterates on MOCKS fast (7 rounds, ~10 min) — keep the mock tool parameterized per-direction, regenerate strips in one command, and let KYLE verify each round before replying"
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "the mock gate evolved the design 7 rounds in one lavish session (fabric blocks -> Blender low-poly base -> topology-on-the-map -> zoom LOD model); the user APPROVED from the gallery with three final rulings"
- Note: 2 jobs, both exactly 7-round lavish mock loops. One-command regeneration + per-round KYLE verification is what makes the loop cheap; rulings land from the gallery.

## C6 — KYLE corroborates, measurement decides (extends the vision-screening law)
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 — "vision (KYLE) corroborates but ranks colors perceptually (called dark-ring variant 'wrong' where WCAG said best contrast — both true: contrast vs board ≠ separation from the dark puck rim)"; remedy: "emit geometry.json anchors FROM the renderer, then PIL-measure against them (radial ring scans + token classification + WCAG contrast)"
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — KYLE mock-gate iterations narrowed the look ("GIS export" → "game map") but byte/pixel gates decided (byte-identical re-bakes, --verify)
- Evidence: righttenantry-dublin-rents-q2-2026 2026-08-24 — "verify the render via `bin/vision-read`" (og cards)
- Note: extends the 2026-08-23 law (a) — vision ranks perceptually; WCAG contrast and separation-from-adjacent-dark-surface are DIFFERENT axes. Verdicts anchor in renderer-emitted geometry + programmatic measurement; KYLE corroborates.

## C7 — shadow_clone clone-list is a per-story trap (PP)
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "EVERY new step()-touched dynamic array must be added to spawn_fx.odin's clone list AND its flow_init mirror (capacity-1) — the shadow silently aliases the LIVE run's pointers and the abort surfaces far away at run_destroy (malloc_error_break backtrace finds it; the tx-ring comment in the same proc is the prior incident)"
- Note: recurring within PP with a prior incident; symptom (far-away abort at destroy) is disjoint from cause — grep the clone list whenever a step()-touched dynamic array is added.

## C8 — Diff at the MERGE-BASE before believing a "deleted files" blocker
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "'this branch deletes the spine' was a merge-base artifact — the spine landed on v2 via #103 after the branch point; always diff at the merge-base before believing a hunter blocker about missing files"
- Note: diffing against a moving remote tip fakes deletions; re-diff at merge-base before escalating any missing-file blocker.

## C9 — Index-keyed derived state must reset on regeneration (B1 generalization)
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "Same-count bundle renumber (demolish+draw in one batch) silently inherits the dead pair's history unless derived-ring layouts reset on Topology.gen — the B1 slot-renumbering class generalizes to every ring keyed by a regenerated index (hunter-probed at 120 phantom ticks)"
- Note: any derived structure keyed by an index that can be renumbered must reset at generation time; incremental maintenance inherits dead entries' history.

## C10 — Odin fmt/syntax micro-traps (the silent ones are the killers)
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 — "literal `{`/`}` in format strings need `{{`/`}}` (a stray single `}` renders literally and breaks the JSON silently); `geom += str` is illegal (use an appendf helper with fmt.aprintf); `import` keyword mandatory per import line"
- Evidence: packet-plumber-v2-dublin-spawn-director 2026-08-24 — "Odin fmt has NO `%-3d` left-justify flags — `%-3d` renders value×100 garbage silently; plain `%d` only. Also NO `var x T` declaration (use `x: T`), and `for p in [4][2]i32{...}` literals need a named var first"
- Evidence: packet-plumber-v2-arch-egress-migration 2026-08-26 — "Odin for-in over array literals is still a syntax error"
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 — "Odin has no #error directive — the compile-time assert idiom is `when <bad> { BROKEN :: 1 / 0 }` (constant division by zero = compile error, proven by mutation leg 3)"
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 — "`odin test app` runs only the app package's tests (46); the render pins live under `odin test app/render` (83)"
- Note: recurring; %-3d and missing {{}} produce NO compile error — silent garbage.

## C11 — Edit-tool escaping: literal `\n` in mermaid labels must be `\\n`-escaped
- Evidence: packet-plumber-v2-arch-latency-egress-queue-model 2026-08-26 — "mermaid label strings contain LITERAL `\n` two-char sequences — in edit oldText they must be `\\n`-escaped (a raw `\n` in the JSON silently becomes a newline, the match fails, and the whole multi-edit call atomically no-ops)"
- Note: sibling of the backtick-in-template-literal class (AGENTS.md Extensions): raw control characters in edit oldText corrupt the match and the ENTIRE multi-edit call no-ops atomically.

## C12 — PIL does NOT alpha-blend on draw
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "PIL does NOT alpha-blend on draw — RGBA pixels are stored raw; composite manually before pixel-scanning mock renders (a scan that skips this reads raw-alpha garbage and lies)"
- Note: any PIL pixel gate over alpha content must composite first or it silently lies.

## C13 — Module-level def shadows a library import (silent no-op)
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "a module-level `def polygonize()` SHADOWS the shapely import of the same name — build_sea silently called the ring helper and returned nothing for a full round"
- Note: when a library call "does nothing", check for a same-name module-level def first; cost here was a full round.

## C14 — Typst byte-identity normalization + place semantics (RT)
- Evidence: righttenantry-demo-pdf-watermark 2026-08-24 — "typst PDFs embed CreationDate/ModDate (info dict + XMP) AND a random xmpMM:InstanceID + trailer /ID pair — byte-identity tests must normalize all six patterns (re:replace chain in the FFI)"
- Evidence: righttenantry-demo-pdf-watermark 2026-08-24 — "`alignment` aligns within the CONTAINER then dx/dy OFFSET it; centering = `place(dx: 0%, dy: 0%, center + horizon, body)`; a page `background:` is painted UNDER content — a full-bleed cover block hides it"
- Note: RT-specific; the six-pattern chain is the reusable byte-stability recipe for typst PDFs.

## C15 — Blender unlit flat colors: pure ShaderNodeEmission + explicit sRGB→linear
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "Principled BSDF 'Emission' still receives the WORLD's ambient light on its diffuse term — a flat paper color renders blown-out white. Use a pure ShaderNodeEmission node; convert palette hex sRGB->linear explicitly and keep view_transform='Standard' for hex-exact PNGs. bpy materials assigned sRGB values directly render +50% brighter (double conversion bites silently)"
- Note: reusable recipe for hex-exact unlit renders out of Blender.

## C16 — Erlang: rebind = badmatch; a fun-per-step is NOT a chain
- Evidence: righttenantry-demo-pdf-watermark 2026-08-24 — "Erlang REBINDS a var in one scope = badmatch, and a fun closing over `Bin` for every step is NOT a chain (B1..B5 were independent replaces)"
- Note: RT/Erlang micro-trap.

## C17 — RT worktree bootstrap: restore the `server/.env -> ../.env` symlink
- Evidence: righttenantry-dublin-rents-q2-2026 2026-08-24 — "Worktree bootstrap missed `server/.env -> ../.env` (main checkout has it) — without it `make run` panics 'DATABASE_URL not set'; add the symlink before smoke-testing"
- Note: sibling of the rsync --exclude='_bmad' class — worktree bootstraps must restore untracked symlinks, not just copy trees.

## C18 — RT og-card orphan test + og pipeline (RT convention)
- Evidence: righttenantry-dublin-rents-q2-2026 2026-08-24 — "OG-card orphan test (`content_pages_point_at_their_own_og_cards_test`) fails on ANY committed `priv/static/og/*.png` not pinned in its pairs list — every new series post needs its card pinned there (plus the `let assert Ok(post)` lookup)"
- Evidence: righttenantry-dublin-rents-q2-2026 2026-08-24 — "`rsvg-convert -w 1200 -h 630 card.svg -o card.png` is the pipeline (PNG 1200x630 RGB)... never sed a `</` inside an SVG text tag (it ate `</text>`)"
- Note: RT convention; sed-eating-`</` is the general micro-trap.

## C19 — Lavish artifact asset paths are `<dir>/img/...`, never bare `img/...`
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "the HTML at .lavish/<name>.html must reference images as <dir>/img/... — a bare img/… path fails as 8 fatal artifact-asset-unavailable failures (the poll returns them, not user feedback — repair + re-poll)"
- Note: tool-level; read the poll output for asset failures before interpreting user silence.

## C20 — bmad-build without render_skill.py: the pre-rendered snapshot is complete
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph 2026-08-25 — "the pre-rendered snapshot at `_bmad/render/bmad-build/packet-plumber-*/` (hash dir) is complete + project-resolved — follow its step files directly (worktree needs `cp -R <repo_root>/_bmad .` first, per the annex bootstrap)"
- Note: sanctioned fallback when the render skill is unavailable; carried the waiver canon note in the PR body "per the standing Silas ruling".

## C21 — Palette pins must check ALL variant surfaces (mode tables, text variants)
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 — "the old CVD mode tables remapped route_tie to pale amber RGB-identical to state_congested's remap — a11y overrides can silently reintroduce a base-palette collision you just fixed; always diff the mode tables too"
- Evidence: packet-plumber-v2-viscomm-gauge-telegraph 2026-08-25 — "the health meter's bar FILL + pct draw the darkened `state_*_text` variants (not the raw state colors)... pixel-scan pins must match the text variant or they read 0 px and look like a geometry bug"
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 — "tools/derive_a11y_palettes.py cannot parse palette.json's inline `//` comments (json.load) — run it on a comment-stripped copy; pre-existing breakage worth an issue"
- Note: the drawn color is often NOT the base palette — check CVD mode tables and text-variant darkening before writing pixel pins.

## C22 — Enumerate existing payload slots before declaring a serialization bump
- Evidence: packet-plumber-v2-arch-latency-egress-queue-model 2026-08-26 — "Serialization-conflict blockers often dissolve against EXISTING tag-conditional payload slots + derived scratch (the Event.direction reuse kept LOG_VERSION at 6) — enumerate existing payload slots before declaring a bump unavoidable"
- Note: arch-craft; serialization-bump blockers are frequently premature.

## C23 — Scratch rlsw capture recipe is PER-BINARY (never assume the harness recipe)
- Evidence: packet-plumber-v2-look-node-legibility-diag 2026-08-26 — "a scratch binary linking the same `app/render` package on the same raylib-sw shadow needed: TWO warmup content frames (first content EndDrawing = black), TWO presents per capture (LoadImageFromScreen reads the LAST PRESENTED buffer — one-frame lag), and NO flip/NO swizzle while the harness binary's needs flip+swizzle — same shadow, unexplained; verify per-binary against palette tokens + geometry anchors"
- Note: even same-package scratch binaries can differ in readback orientation/lag; calibrate each capture binary against known tokens + anchors.

## C24 — Render-surface realities defeat pixel gates (probe before trusting)
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-26 — "rlsw renders DrawTriangle FILLS opaque too — an alpha-only 'recede' on a hand-built triangle surface is a goldens-path no-op... dublin_node_block_draw's street-oriented quads are BACKFACE-CULLED for some windings — a mutation that changes only the fill can stay pixel-inert because THE FILL NEVER RENDERS there; probe with distinct-color dumps before trusting any block-surface gate"
- Evidence: packet-plumber-v2-viscomm-crisis-duck 2026-08-25 — "when the highlight owns the surface, pin the neighbor surface" (crisis outline overdraws the whole band; non-recede pinned one layer out at the type-chip glyph + doorstep riders)
- Evidence: packet-plumber-v2-viscomm-tie-deconflict 2026-08-25 — "palcheck sections can do full live-render checks (ClearBackground + draw_route_glow + LoadImageFromScreen) without touching goldens — the 'harness capture path never invokes assists' doctrine applies to golden CAPTURES, not to analysis renders"
- Note: before trusting a pixel gate, confirm the surface actually renders (distinct-color dumps); if the target is overdrawn, pin an adjacent clear surface; analysis renders may invoke assists where golden captures may not.

## C25 — sqlite3 CLI cannot open the ledger DB read-only; node:sqlite readOnly is the sanctioned path
- Evidence: orchestrator-dashboard-perkins-bridge (DSH interlude, ~08-24..26) — "sqlite3 CLI cannot open this ledger DB read-only on this machine (rc=14); node:sqlite DatabaseSync {readOnly:true} works and is the sanctioned read path"
- Note: ops-relevant to anything reading `orchestrator.db` externally (bin/ledger stays the write path).

## C26 — DSH app-boot: a rejected loader entry is FATAL (guard + degrade)
- Evidence: orchestrator-dashboard-perkins-bridge (DSH interlude) — "A rejected cordis loader entry is FATAL to dsh-app-boot (exit 1) — host halves must guard every import/registration path and degrade to a log line"
- Note: DSH-specific; belongs with the dsh-orchestrator-setup/AGENTS.md rulings if kept.

## C27 — Static demo mesh bounds growth claims; derived views are the honest audit
- Evidence: packet-plumber-v2-dublin-spawn-director 2026-08-24 — "the dublin board's growth is E31-bounded by the STATIC demo mesh (2 routers → ~15 terminals/90s) — the estate lens (derived cluster view) is the honest audit (per-district counts read 1-2 because estates straddle Voronoi boundaries by design)"
- Evidence: packet-plumber-v2-dublin-spawn-director 2026-08-24 — "a zero-weight band must be excluded from the ELIGIBILITY list, not just the weighted draw (the single-eligible shortcut would pick it)"
- Note: PP domain — capacity/growth claims on demo boards must account for the static mesh bound; exclusion semantics live in the eligibility list, not the weighted draw.

## C28 — Map-bake geometry micro-traps (PP dublin bake tool)
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "a seed ON the bbox edge is `touches`, never `contains` — keep the seed inside the bbox"
- Evidence: packet-plumber-v2-dublin-map-beautify 2026-08-24 — "nearest street segment via shapely STRtree — deterministic, ties break by input order"; sea is bake-time constructed from clipped coastline + unary_union + polygonize (OSM never maps open sea as a polygon; coastline ways are OPEN lines that can't close_ring)
- Note: PP map-bake tool specifics; useful if the bake is revisited (sea %, LOD follow-ups flagged).

## Stale/duplicate entries NOTICED (not verified against live store)
- C2 (Odin proc non-capture) appears in TWO shards (08-24 gap-window + 08-25 post-marker) — consolidate as ONE store entry with both sightings.
- C3 should AMEND the existing dream-2026-08-23 (f) mutation-leg law, not a new sibling entry; C6 similarly amends law (a) (vision screening).
- gauge-telegraph cites "the standing Silas waiver ruling" (bmad-build canon note in PR body) — not visible in root AGENTS.md; may live only in the playbook (location worth checking at consolidation).
- orchestrator-dashboard-perkins-bridge is titled "perkins-bridge" but contains zero Perkins content (3 lines of DSH dashboard tech notes) — possibly mis-titled shard.
