You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

REPOSITORY (READ-ONLY for you — never edit files, never git checkout/commit/stash, never run mutating commands or builds that write into the tree): /Users/moses/code/packet-plumber-wt-gauge-r1 — a detached checkout at exactly the reviewed state (commit 7114bf3238e9f5c43a89733e52255dbf0ae1dcde). Verify against THIS tree, not origin or any other checkout.

THE DIFF (headless mode: provided as a saved file — those bytes ARE the --- DIFF --- section): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-gauge-telegraph/r1/diff.patch (1353 lines). Read it FIRST and IN FULL (use offset reads until you have seen every line). Never re-fetch, regenerate, or re-derive the diff.

--- PROJECT CONVENTIONS ---
---
project_name: 'Packet Plumber'
user_name: 'Moses'
date: '2026-08-08'
sections_completed: ['technology_stack', 'engine_rules', 'design_locks', 'performance_rules', 'organization_rules', 'testing_rules', 'platform_rules', 'anti_patterns']
status: 'complete'
optimized_for_llm: true
forge: '_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md'
brief: '_bmad-output/planning-artifacts/briefs/brief-Packet-Plumber-2026-08-05/brief.md'
architecture: '_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md'
supersedes: 'the Godot 4.7.1 pin (pre-pivot revision of this file); the engine pivot to Odin + Raylib was decided by the user on 2026-08-08'
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing game code in this project. Focus on unobvious details that agents might otherwise miss. The forge governs locked design decisions; the game brief is the design source of truth; the Odin architecture governs technical structure; this file governs how code gets written._

**Project:** Packet Plumber — a top-down routing puzzle where you are a network engineer keeping the internet alive: draw pipes between nodes, route colored packets by type, predict and survive fair crises, and upgrade infrastructure as the internet evolves through eras. Mini Motorways **light-daytime** visual style (art-direction amendment A1); **desktop-first launch** (Steam PC/Mac; mobile follows when the Odin+raylib toolchain matures — FORGE #6 amended by user ruling, lavish 2026-08-08). At this stage the project is in the **Odin pivot**: the Godot prototype (PR #11/#12) proved the fun and is preserved as the `prototype-fun-gate` tag (removed from main on the first Odin code PR — ruled 2026-08-08); the Odin build (packages at the repo root: `core/`, `app/`, `harness/`) is the real codebase, per `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`.

**Citation tags:** `[FORGE #n]` = a sealed decision from the forge (`_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md`); `[BRIEF]` = sealed at the game-brief level; `[ODN-n]` = an architectural decision in the Odin architecture; `[LOOK]` = look-book v1 visual canon.

## Technology Stack & Versions

- **Language:** Odin **`dev-2026-08`** (pin exact; `.odin-version` + CI enforce; recheck at phase boundaries). Verified against upstream releases 2026-08-08.
- **Renderer/platform lib:** **raylib 6.0** via Odin's shipped `vendor:raylib` bindings (6.0-binding fixes landed in Odin dev-2026-07a). No third-party package manager.
- **Harness raylib build:** the golden-image harness builds raylib from source with the **software renderer (`rlsw`) + memory platform** (`tools/build_raylib_sw.sh`) so pixel goldens are bit-identical on every machine with no GPU/display. The game binary uses the stock `vendor:raylib` GPU build.
- **Viewport & framing:** 1280×720 landscape **design grid**; resizable window reveals more map (camera-fit calculation in the render layer — the GL5.2 `aspect=expand` doctrine re-implemented). Landscape-only doctrine unchanged [RULING — user, 2026-08-05].
- **Typing:** Odin is statically typed by construction; use explicit integer widths (`i32/u32/u64`) on all sim state.
- **Tests:** `odin test` (`core:testing`, `@(test)`) for the pure core; the golden-image harness (`harness/`, ODN-17) for scripted scenarios + visual regression. Everything testable headless, is.
- **Reference build:** `game/` is the frozen Godot prototype — behavioral reference only; never ported line-by-line, never extended.

## Critical Implementation Rules

### Stack-Specific Rules (Odin + raylib — the pivot trap set)

- **The core is pure.** `core/` imports only whitelisted `core:*` packages — never `vendor:*`, never `core:os`, never `core:time` (ODN-1). The sim steps only via `core.step(state, tick, commands)`; nothing in core reads a clock, a file, or a device. CI compile-checks this.
- **Integer-only sim paths.** All state-affecting math is integer or explicit fixed-point (ODN-10). Floats exist only in the view (interpolation, pulses) and never flow back into state. Catalog sim values are integers; cosmetic floats are labeled.
- **Never iterate a `map` in core.** Odin map order is unspecified — core iterates arrays/slices/`#soa` only (insertion-ordered, stable). Maps are lookup-only. Equal-candidate tie-breaks draw from `state.rng` (ODN-9/10).
- **RNG is owned, never global.** Sim randomness comes only from the `Rng` held in `Run_State` (owned splitmix64→PCG32 XSH-RR, test vectors pinned — ODN-9). Cosmetic randomness (SFX variants, jitter) comes only from the app-owned second stream (ODN-15). `core:math/rand` is not used for sim — its internals may drift between Odin releases.
- **Arena discipline (ODN-18).** Three arenas: run (per-run state), snapshot (ping-pong per tick), frame (reset per frame). Core code never calls `new`/`make` without an explicit allocator argument. Dev builds run the tracking allocator; leaks are CI failures.
- **No globals / singletons.** Everything hangs off `App` → `Run_State`, passed by pointer (ODN-13). Per-run reset = create a fresh run context in a fresh arena; never "clean up and reuse."
- **Events, not callbacks.** Cross-layer communication is the per-tick `Event` tagged-union buffer on `Run_State`, drained by the app after each step (ODN-14). No function-pointer webs, no global bus.
- **Errors are values.** Fallible procs return `(T, Error)` with typed error enums; a dropped error return is a CI lint failure (§7.1 of the architecture). Never catch-and-ignore.
- **Save/log is binary, little-endian, versioned** (ODN-11) — no JSON for state (the JSON-int-to-float trap class is deleted at the root). JSON is for catalogs only, loaded once, fail-fast validated, embedded via `#load()` in release.
- **Runtime-gated debug surface.** The v2-noc NOC dashboard ships in the NORMAL build (2026-08-23 user ruling: useful for players), gated at RUNTIME — panel OFF by default (zero pixels until D), D key gated by the availability flag (settings row "NOC PANEL (D)", default ON, in-session only); removal = one-line default flip. The harness `overlay-check` verb remains behind `-define:PP_DEBUG=true` (a harness dev tool); the capture path never calls the overlay, so goldens cannot shift.
- **Raylib idioms:** immediate-mode drawing only inside `BeginDrawing/EndDrawing`; the static map caches into a `RenderTexture` (redraw on pan/zoom); packets are per-frame draw calls from snapshot arrays — there are no per-entity view objects to pool or free. The harness renders to texture / memory framebuffer, never to screen.

### Game-Rules-as-Code (locked design — enforce in every implementation)

- **Core mechanic is Draw + React, not construct.** PRIMARY: draw pipes between nodes, snapping to nodes (no pixel precision — Mini Metro / Mini Motorways model). SECONDARY: react to PREDICTABLE crises the player saw coming. NOT a Factorio-style construction sim (no material selection, production chains, zoning) `[FORGE #2]`.
- **Terminals connect via routers only — never terminal-to-terminal** (art-direction amendment A6 / look-book D11). Houses are leaves; routers are the interconnect. The Command_Bus rejects terminal↔terminal draws.
- **Crises are FAIR and PREDICTABLE, never random.** A crisis is the consequence of a topology flaw the player should have designed around — warning signs first (🟡 congested → 🔴 critical). Random/unfair chaos was explicitly rejected `[FORGE #3]`. The V2 AI disaster system (out of prototype scope) is a stress-test auditor, not a random bully.
- **Differentiator 1 — packet types + QoS class queues.** Not all packets are equal: gaming wants low latency and can't drop, banking must never drop, streaming wants volume and can buffer, email is low priority. The player allocates each pipe's bandwidth across 3 class queues (Express/Standard/Best-effort); every route is a TRADE-OFF `[FORGE #4]`. All traffic starts on Standard; QoS is player-engineered, never auto.
- **Differentiator 2 — era progression + infrastructure lifecycle.** The internet evolves (ARPANET → email → web → streaming → …); old infrastructure obsoletes and must be upgraded or it suffocates `[FORGE #4]`.
- **Visual style is the look-book light canvas:** warm-cream map, literal buildings (6 terminal types), round capacity-scaled router pucks, smooth bezier pipes (glowing cores on fiber/backbone), blue/grey packets with distinct shapes, procedural land/ocean/parks map, warm colors reserved for danger `[LOOK]`. Color is never the sole encoder (shape + icon + pulse).
- **Cross-platform same-game doctrine:** one game, input-agnostic `[FORGE #6]` — amended 2026-08-08 to desktop-first sequencing: ship Steam PC/Mac first, mobile follows at toolchain maturity; the intent-layer input model keeps all inputs additive.
- **Brand satire, never real brand names.** YouTune / Amazoom / Goggle / Glitch (Netflix and Discord are kept) `[FORGE rejections]`.
- **Name is Packet Plumber** `[FORGE #8]`.

### Performance Rules

- **Target: 60 fps sustained** on desktop; optional unlocked-framerate toggle (off by default on battery devices) `[GDD § Performance]`.
- Fixed 20 Hz logic tick + render interpolation (ODN-2); no per-frame work that the tick model can own. SOA hot loops; zero per-frame heap churn (frame arena).

### Code Organization Rules

- Odin packages live at the repo root (the Odin-native convention, ruled 2026-08-08). **Layout:** `core/` (pure sim), `app/` (game executable: `render/`, `ui/`), `harness/` (golden runner), `demos/`, `data/` (JSON catalogs), `goldens/`, `tools/` (see the architecture §16.2). One directory = one Odin package.
- Naming (Odin stdlib style): types/constants `Ada_Case` · procs/vars `snake_case` · files `snake_case.odin` · privates `_prefixed` where needed.
- **Numbers single-source:** balance numbers live in `data/*.json`, never restated in code (ODN-5).
- Keep all catalog data integer-only for sim values; absent fields use explicit load-time defaults (no sentinel values).

### Testing Rules

- **The golden harness is the verification foundation** (ODN-17): built before feature stories; `harness run` must be green before any PR; `harness save` re-blesses goldens only deliberately and is reviewed like code.
- **Pin every design invariant as a regression test at the lowest layer** (`@(test)` in `core/`): determinism/replay equality, fair-crisis contracts, QoS drop precedence + no-starvation, snap precision, no-soft-lock. Acceptance criteria become durable tests, not PR prose.
- Two golden tiers (architecture §10.2): T1 state-hash goldens (every platform, no GPU) + T2 pixel goldens (software renderer, zero-tolerance). On mismatch the harness emits an agent-readable diff bundle (diff PNG + `diff.json` + replay demo) — read it before theorizing.

### Platform & Build Rules

- **Targets:** Steam PC/Mac first (Windows, macOS builds via `odin build -target:...`; native CI runners per OS × amd64/arm64). **Desktop-first launch (ruled 2026-08-08)** — mobile (Android/iOS) is deferred until the Odin+raylib toolchain matures; do not claim mobile support until a maturity spike lands it. Web/wasm is a possible stopgap, not a launch platform. No console `[BRIEF]`.
- Keep `.odin-version`, the CI matrix, and this file's Technology Stack in sync. Version bumps are deliberate, reviewed events (the PRNG/replay contracts depend on toolchain stability).
- No purchased assets before the playtest gate; placeholder art = colored rects + emoji + system shapes drawn with raylib primitives (the prototype is reference, not shippable).
- **Audio/music:** Suno-generated, owned outright by Moses — paid-tier generations only (commercial rights; Content-ID-free for streamer monetization). Soundtrack is a candidate parallel DistroKid release (owned IP).
- Env files are read-only in worktrees and NEVER committed; any API key (future server features) comes from env only.

### Critical Don't-Miss Rules (anti-patterns)

- **Never use real brand names** — trademark risk; use the satire set `[FORGE rejections]`.
- **Never make a crisis random or unfair** — the player must always be able to say "I should have seen this coming" `[FORGE #3]`.
- **Never build a Factorio-style construction layer** — draw + react is the mechanic `[FORGE #2]`.
- **Never soft-lock the player** — there is always a way to reroute or upgrade out of a crisis.
- **Never let the view touch the sim** — presentation reads immutable snapshots only; input reaches the core only as validated Commands (ODN-1/12).
- **Never sample real time in a test** — the harness drives a virtual clock; demos are deterministic by construction.
- **Never catch-and-ignore** — every error path either recovers (logged) or surfaces.
- **Never re-litigate a locked forge decision.** If a task conflicts with a `[FORGE #n]` lock, STOP and surface it. For everything else, when in doubt, prefer the more restrictive reading.

---

## Usage Guidelines

**For AI Agents:** Read this file before implementing any game code; read the forge and brief for design intent, and the Odin architecture for structure. Follow ALL rules exactly. This is a living document — when the prototype reveals new traps or the architecture pins new structure, update it.

**For Humans:** Source of truth for locked design = the forge; for the design narrative = the game brief; for technical structure = the Odin architecture; for code conduct = this file. Keep this lean and focused on agent needs.

Last Updated: 2026-08-08 (Odin pivot — engine pin redone from Godot 4.7.1 to Odin dev-2026-08 + raylib 6.0)

--- SPEC / CONTEXT ---
SPEC 1 — the PR #100 body (what the author claims the diff does):
## viscomm(gauge): gauges telegraph, not snap (audit finding B)

Health / pool / SLA gauges snapped value-to-value; when values move fast
(drain, refill, SLA decay) the player reads a strobe, not a level. Each
gauge now carries a **render-owned display value** that eases toward the
raw sim value:

- **EASE16** — a pinned 16-entry ease-out table (the PULSE16 §10.4
  no-transcendentals pattern), indexed by a tick-derived integer phase.
  `[0]=0` pins tween-start continuity (no pop), `[15]=1` pins exact
  arrival (a finished tween reads raw to the byte). Compile-time `when`
  guards pin endpoints/cadence/threshold (the `BROKEN :: 1/0` idiom).
- **Chunk-flash cue** — an instantaneous delta ≥ `CHUNK_PCT` (25 units)
  fires a one-shot ghost of the jumped region (fill geometry, `CHUNK_FLASH`
  table alpha, 3-tick fade), then the ease carries the level across.
- **Reduced motion** (7.3/E9.2) snaps display to raw immediately and
  suppresses the cue (the `pulse_read` pattern).
- Surfaces: health meter bar fill, pool gauge bar fill, SLA avg-ms +
  loss-pct display numbers. Truth channels stay RAW — numbers, counters,
  breach latches, state colors.

### Golden safety (zero churn, by construction)

The harness capture path never feeds gauge targets, so an **unfed gauge
reads raw exactly** — 49 demos green, zero golden bytes changed (the
`pkt_interp` precedent: the app steps presentation, the harness renders
snapshot-exact). Paused frames step nothing, so the ease freezes with the
sim (phase derives from the tick). A fresh run seeds display = raw (no
fill animation at run start).

### Verification

- `odin test app/render` — 91 (83 + 8 new gauge pins: table/tween/chase/
  chunk/reduced-motion/pause/feed/harness-inert)
- `odin test app` — 46; `odin test core` — 261 (untouched)
- `bin/harness run` — 49 demos green, zero golden diffs
- `bin/harness palcheck` — all green incl. **section 6**, the draw-path
  leg: live rlsw render, pixel-scanned mid-ease fill boundary at the
  EASE16-predicted column (~213px vs raw 182), ghost blend present while
  the cue lives / pure track after expiry, reduced-motion snap to raw
- **Mutation legs (RED→GREEN)**: easing bypassed (`gauge_read` := raw)
  → palcheck section 6 FAILS (fill collapses to raw); restored → green.
  Chunk-cue deleted → ghost leg FAILS; restored → green. Deliberate-fail
  probe run on the new test binary.
- `tools/ci-local.sh --mac` — all 13 gates green

### Decisions & rationale

- **Continuous deltas ride the active tween** (target chases raw, phase
  NOT reset); only a chunk crossing re-anchors from the current display.
  Rationale: re-anchoring on every small delta would make a continuous
  drain crawl (the ease would restart at 4% coverage each tick) — the
  chase keeps motion bounded while preserving continuity (pinned: the
  retarget display move ≤ raw move + the tween's own per-tick step).
- **SLA chunk-flash omitted**: the SLA rows are text (no chunk geometry
  to flash); the eased display numbers kill the strobe. The two BARS
  carry the flash cue (health, pool).
- **`draw_health_meter` gained a `tick` param** — the ease phase derives
  from the tick at read time; the harness passes its existing tick with
  the gauge unfed (byte-identical by construction). Same for the five
  other harness call sites.
- **Roster cap 8** on the SLA ease slots (the node_health card's pinned
  catalog cap); classes beyond it simply never feed — an unfed gauge
  reads raw (the zero value IS the fallback).
- **bmad-build skill render waiver** (standing Silas ruling 2026-08-21):
  `_bmad/scripts/render_skill.py` is absent from this BMAD install — the
  pre-rendered project snapshot at
  `_bmad/render/bmad-build/packet-plumber-c02b60b148b2/d1343645b747d61a6ec8/`
  (generated for this exact repo root) was followed instead, and the
  step-04 review layers (blind-hunter / edge-case-hunter /
  verification-gap) ran as mega-minions per the playbook's
  enforced-from-2026-08-23 rule.
- **No golden re-bless** — none needed (the unfed-gauge contract held
  through every health-on capture; a legit golden shift would have been
  a STOP-and-flag canon decision).

### r1 review round (blind-hunter + edge-case-hunter + verification-gap)

Patched: zombie tween (arrived-but-active ate later small retargets — the
strobe would return after the first tween; re-engage + pin), game-over
freeze (terminal snaps gauges — the empty meter is the loss surface), lazy
SLA seed (a hidden "-" readout no longer seeds at 0 — the first VISIBLE
number is raw), terminal-aware feed folding into feed_drop_sites + 2 app
wiring tests (start_run zeroes; the presentation feed lands targets — the
vacuous-wiring class), single-source derivations (pool_fill_pct /
sla_avg_ms / sla_loss_pct shared by feed + draw), SLA slots 8 → 16 (the
planned roster is 9 classes), per-unit chunk thresholds (CHUNK_PCT vs
CHUNK_SLA_MS), flash-flag expiry hygiene, pool-gauge palcheck draw-path
leg + geometry prelude, this _pr_body_ artifact (the repo convention).

Rejected (rationale): eased numbers transiently near tolerance — bounded
by recent RAW values (the telegraph's purpose, ≤0.4 s); pool/SLA
draw-geometry export — pinned via prelude asserts instead.

Deferred (deferred-work.md): the loop→feed_drop_sites call-site pin (the
pre-existing debug_surface_smoke.sh class — needs a headless app-drive
harness); SLA text draw-path pixel pin (app package not harness-
importable; folds into the same story).


SPEC 2 — the implementing minion's job briefing (the contract this diff must satisfy — the acceptance lens treats THIS as the spec):
# Briefing — packet-plumber-v2-viscomm-gauge-telegraph (viscomm audit finding B)

Skill to execute: **bmad-quick-dev** (step-04 review layers MANDATORY before
reporting done). Briefing is self-contained if the skill is absent.

## Repo / workspace facts

- Repo: `/Users/moses/code/packet-plumber` (Odin `dev-2026-08` + raylib 6.0).
- Base branch: **v2** @ fresh head `0b893ee` (post-#99-merge). Silas creates
  the worktree; work ONLY there; NEVER touch the main checkout (it sits on a
  user branch).
- Read `/Users/moses/code/packet-plumber/project-context.md` first — ODN
  rules and [LOOK] canon govern.
- Field notes (read both): `_bmad-output/field-notes/packet-plumber-v2-viscomm-tie-deconflect.md`
  — they carry the render-test + palcheck + mutation-leg craft you MUST reuse.

## Task: gauges must telegraph, not snap (audit finding B)

Health / pool / SLA gauges currently snap value-to-value. When values move
fast (drain, refill, SLA decay) the player reads a strobe, not a level.
Animate the transitions so the gauge TELEGRAPHS its motion:

1. **Eased display-value, raw truth.** Keep the underlying metric values
   untouched (never alter SLA/health/pool SEMANTICS — render-side only).
   Each gauge carries a display value that eases toward the raw value.
2. **PULSE16-style stepped table, NO transcendentals** (§10.4 canon — see
   `PULSE16 :: [16]f32` at `app/render/view.odin:762` for the pattern, and
   view.odin:1601 for the render-side-table idiom). Define an EASE16-style
   envelope table; index by tick-derived integer phase. No sin/cos/pow/exp
   in draw paths — compile-time enforceable via the `when <bad> { BROKEN ::
   1 / 0 }` idiom if practical.
3. **Deterministic + tick-driven** — animation phase advances from game
   tick, never wall-clock; identical ticks render identical frames
   (golden-safe by construction; zero golden churn expected — if a golden
   legitimately must move, STOP and flag: that is a canon decision).
4. **Reduced-motion** — the 7.3 (E9.2) reduced-motion setting pins PULSE16
   effects (view.odin:94); the gauge easing MUST respect the same setting
   (snap immediately under reduced-motion).
5. **Chunk-flash guard for big jumps** — on a large instantaneous delta
   (e.g. pool drained by event), a single-frame flash/chunk cue is allowed
   ONCE, then ease — the cue is table-driven and deterministic like the rest.

## Testing standard (the r1/r2 lesson — non-negotiable)

- **Mutation leg on the DRAW PATH:** deleting/bypassing the easing (display
  value := raw value) MUST fail a test. A predicate-only pin is bypassable
  (the r1 vacuous-gate burn). Guard what renders: palcheck-style live-render
  checks (ClearBackground + draw the gauge + LoadImageFromScreen, sample the
  fill geometry/pixels mid-ease) or equivalent draw-path assertions — per
  the field notes, palcheck can do live renders without touching goldens.
- Prove RED-then-GREEN: run with the easing deleted (tests RED), restored
  (GREEN). Both runs in your report.
- Deliberate-fail probe on any NEW test binary/case before trusting green
  (field note: cheap confirmation the test actually executes).
- Full suite green: `odin test app` (46), `odin test app/render` (83+ incl.
  your new tests), palcheck.

## PR / ledger

- One PR to base **v2**. Title prefix `viscomm(gauge):`.
- `ledger set packet-plumber-v2-viscomm-gauge-telegraph in-review "<PR url>"`
  THEN `ledger pr packet-plumber-v2-viscomm-gauge-telegraph <PR url>` (the
  pr field arms the PR watcher — both steps, always).
- Perkins r1 arms via the sensor at your stable CI-green head.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider — k3 403, flash 402),
  `--thinking max`.
- Any mega-minion: pin `zai-coding-cn/glm-5.3` explicitly in the spawn
  prompt (bare pi misroutes).

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: viscomm-gauge-telegraph
- base: v2 (head 0b893ee)
- branch: packet-plumber-v2-viscomm-gauge-telegraph
- model: zai-coding-cn/glm-5.3
- pr_review: 1 (render-path change on a canon surface — viscomm series keeps review)

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT (headless mode): Write your final JSON array — and nothing else — to the file /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-gauge-telegraph/r1/edge.json (overwrite it with your file-writing tool). The file content must be exactly the JSON array: no prose, no markdown fencing, no preamble. Then STOP — your work is done when the file is written; a one-line chat confirmation is enough. The FILE is the deliverable, not your chat message.
