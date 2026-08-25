# sheep-shards — dream-2026-08-23 candidate patterns

Reader: SHEEP-SHARDS (mega-minion of Bob). Marker: 2026-08-21T18:49:59Z.

**Coverage / provenance:**
- 17 shards read in full — ALL post-marker (earliest mtime: dream-2026-08-21.md @ 19:49Z, the prior dream's own badge-out notes — Bob-meta, included since Bob's own shard is not consolidated by his own dream).
- 2 tail-reads: `packet-plumber-ue-slice-1.md` (mtime 2026-08-21T12:46Z) and `orchestrator-night-watchman.md` (mtime 2026-08-21T07:15Z). **Tail verdict: BOTH are entirely pre-marker** (tails = whole files, 40 and 22 lines; no post-marker dates in content; content matches the 08-19/20 UE-slice arc and the 08-21 watchman build). Likely already consolidated by dream-2026-08-21 — cited below ONLY as `[PRE-MARKER corroboration]` where they independently confirm a new pattern.

---

## 1. Vision reads are a screening layer, never evidence — measure pixels before believing [2+ SIGHTINGS — strongest pattern in this batch]

Sightings:
- packet-plumber-v2-design-audit (2026-08-22): "Kyle's vision verdicts need pixel verification before they drive decisions — pass-1 '3D shading on sprites' was wrong (sprites measured 90-93% flat canon hexes, residual = AA only); 'shapes identical' was wrong (aspects 1.01 vs 1.45-1.48)."
- packet-plumber-v2-blender-silhouettes (2026-08-22): "port-ring dots … the first cut stacked all dots at the disc center … KYLE caught nothing at contact-sheet scale — the bbox geometry table + a zoomed per-sprite check caught it."
- packet-plumber-v2-camera-zoom (2026-08-23): "never eyeball zoom claims; vision (KYLE quick-read) is the secondary check on the committed captures."
- [PRE-MARKER corroboration] packet-plumber-ue-slice-1: "VERIFY SCREENSHOTS WITH PIXEL SCANS, not vision alone: the r1 'mid-traversal' frame had zero dot pixels (the vision model hallucinated it — I trusted a single vision read). … Never re-bless evidence on a vision claim."

Generalizes: a vision model's aesthetic/geometric claim is a hypothesis — mechanical pixel scans (PIL coverage, bbox aspects, diff-frac) are the admissible evidence; never re-bless goldens or drive a "needs Blender"-class decision on a vision verdict alone.

## 2. KYLE (glm-4.6v) spawn mechanics — one-shot and full-agent recipes + their pitfalls [2+ SIGHTINGS]

Sightings:
- packet-plumber-v2-look-polish (2026-08-21): "5v-turbo is subscription-blocked (429/1311); 4.6v works. … prompts written to FILES (shell quoting eats multi-line prompts), absolute OUT paths (the spawn cds into the worktree — relative outputs land there)."
- packet-plumber-v2-design-audit (2026-08-22): "Kyle (glm-4.6v) full-agent spawn works like the one-shot recipe — herdr pane split, `pi --model zai-coding-cn/glm-4.6v --thinking max`, hand over via `herdr agent prompt` with `@file` absolute paths; verify the session modelId in the pane title. … Long turns hit provider 500/timeouts — nudge with 'write NOW compactly, do not re-read' when the file is overdue; his findings land on disk even when the final DONE message errors."

Generalizes: KYLE spawns are reliable if prompts go to files, all paths are absolute, and output is read from disk (not the final message); long vision turns need a "write NOW" nudge rather than a re-dispatch.

## 3. Piped / scripted command runs mask failures — capture rc, verify output FRESHNESS, byte-check rewrites [2+ SIGHTINGS]

Sightings:
- packet-plumber-v2-blender-sculpt (2026-08-23): "Never trust a piped Blender run: `blender -b -P … | grep` masks the exit code AND the traceback — two 'determinism-proof' runs had crashed on a bad API call … while `cmp` compared stale files. Capture `rc` first, then sanity-check output FRESHNESS (mtimes / expected new values) before believing a byte-compare."
- orchestrator-playbook-diet (2026-08-21): "a `tr '\n' ' '` command inside a rewritten heredoc got corrupted into a literal newline — byte-check commands after any scripted rewrite (grep for the exact token)."
- orchestrator-playbook-diet (2026-08-21): "heredoc + triple-quote Python strings with embedded quotes self-terminate (SyntaxError) — write replacement scripts to files or use the edit tool for exact-match replacements instead."

Generalizes: any piped/generated/subshell execution can silently no-op — the verification is (rc captured un-piped) AND (output proven fresh) AND (the generated artifact byte-checked), never the downstream compare alone. (Sibling of the existing AGENTS.md herdr pipe-mask gotcha — the class is broader than herdr.)

## 4. bmad-build / bmad-quick-dev render is broken on this install — the waiver protocol [2+ SIGHTINGS, two distinct causes]

Sightings:
- orchestrator-playbook-diet (2026-08-21): "bmad-quick-dev → bmad-build render HALTs on this install (`ambiguous config value implementation_artifacts`) — waiver carried as a canon note in the PR body; the briefing was self-contained."
- packet-plumber-v2-noc-player-toggle (2026-08-23): "bmad-build is UNUSABLE on packet-plumber: `_bmad/scripts/` has NO render_skill.py (only memlog.py/resolve_*.py) — skill waived per Silas ruling 08-21; the briefing was self-contained; carry the waiver as a canon note in the PR body."
- [PRE-MARKER corroboration] orchestrator-night-watchman: "bmad-build render HALT on this install (upstream 6.11.0, not repo drift) … Waived by Silas ruling — briefings should avoid bmad-build until upstream fixes the template; carry the canon note in PR bodies."

Generalizes: when a mandated skill cannot render/run on an install, the standing response is: waive per Silas ruling + make the briefing self-contained + carry the waiver as a canon note in the PR body — not a local fix attempt. Two root causes now on record (upstream ambiguous config; repo missing render_skill.py).

## 5. rlsw/raylib dual-render-path traps: LINE alpha is opaque, winding is CCW-only, GPU captures lie — the SW shadow build is the only truth [2+ SIGHTINGS — 5 independent]

Sightings:
- packet-plumber-v2-look-polish (2026-08-21): "FILLED shapes … alpha-blend in the software renderer; LINE primitives render alpha as OPAQUE — a translucent line draw diverges between the GPU app and the rlsw goldens."
- packet-plumber-v2-spawn-feel (2026-08-22): "rlgl ENABLES backface culling with front = CCW — any hand-built triangle fan/quad … must wind CCW in screen space or it renders NOTHING in both the rlsw captures AND the GPU app; and the rlsw software renderer ignores LINE alpha (fills only) — a fading ring must be filled geometry, never DrawCircleLines/DrawLineEx."
- packet-plumber-v2-spawn-feel (2026-08-22): "NEVER build the harness with a bare `odin build harness` — the rlsw shadow link requires `tools/harness.sh` … a stock build links GPU raylib, the BGRA swizzle then corrupts EVERY capture … and the suite 'fails' with misleading full-frame diffs."
- packet-plumber-v2-font-overhaul (2026-08-23): "the GPU path lies twice: the compositor freezes the GL front buffer for occluded windows (TakeScreenshot repeats frames) AND RenderTexture readbacks carry glyph-coverage in the alpha … — the SW framebuffer (LoadImageFromScreen + flip + r/b swizzle) is the ONLY reliable capture."
- packet-plumber-v2-noc-readability-2 (2026-08-23): "The PP_DEBUG harness verbs need the rlsw software build (bin/harness-debug is GPU and renders a SOLID BLACK frame headless — the 08-11 trap, still live)."

Generalizes: in a GPU-app + software-golden dual renderer, translucent effects must be fill geometry, hand-built fans must wind CCW, and ALL capture/verification goes through the rlsw shadow build — GPU screenshots and readbacks are inadmissible (occlusion freeze, alpha pollution, headless black frames).

## 6. Golden/asset determinism: compare decoded pixels, never file bytes; strip PNG metadata; per-commit re-bless verification pays [2+ SIGHTINGS]

Sightings:
- packet-plumber-v2-blender-silhouettes (2026-08-22): "gen_sprites.py re-render on Blender 5.2 is PIXEL-DETERMINISTIC (decoded RGBA identical; md5 diffs are PNG-encoder metadata only) — a no-op re-render is golden-safe … T2 compares decoded pixels, never file bytes."
- packet-plumber-v2-blender-sculpt (2026-08-23): "PNG byte-determinism fix that works on 5.2: strip tEXt/iTXt/zTXt chunks post-render (the wall-clock `Date` tEXt is the only mover; IDAT is stable run-to-run)."
- packet-plumber-v2-look-polish (2026-08-21): "The per-commit re-bless loop pays: 5 deliberate re-blesses, each verified by (a) `cmp -l` every `.log.bin`/`.t1` vs HEAD … (b) diff-bbox pixel scans matching PREDICTED blend colors ±0 … (c) palcheck re-pins with measured floors — CI stayed 10/10 at every commit."

Generalizes: file-byte compares (md5) mislead on encoded assets — determinism lives in the decoded payload; strip encoder metadata chunks for byte-stability; and a re-bless is only trustworthy when every commit carries a byte/pixel/pin triple-verification.

## 7. Event-stream additions move T1 manifests even with zero pixel/log delta; live path must emit identical wire events as replay [SINGLETON]

Sightings:
- packet-plumber-v2-sound-immediacy (2026-08-22): "adding two zero-payload append-only event tags (PIPE_DRAWN/NODE_SPAWNED) moved 44 T1 manifests; ZERO pixels/logs changed (verify with `git status` before claiming the re-bless is pure). Divergence ticks line up exactly with first-draw/first-spawn ticks — that's the cause check."
- packet-plumber-v2-sound-immediacy (2026-08-22): "The live fast-path emits the SAME wire event as replay, at the SAME apply_tick (`inp.tick + 1` …): emit from BOTH step's command loop and commit_draw or the app's stream silently diverges from a log replay."

Generalizes: in an append-only event-sourced sim, ANY new event tag invalidates the recorded streams (budget the re-bless, prove purity via git status + divergence-tick alignment); and every event must be emitted on both the live and replay emission sites at the identical apply_tick or the two paths silently fork.

## 8. Deterministic-sim prediction = shadow clone + bounded replay; deep-copy ALL state, replay pending commands [SINGLETON]

Sightings:
- packet-plumber-v2-spawn-feel (2026-08-22): "Predicting the next growth-window spawn is a SHADOW CLONE + ≤10-step replay (deterministic sim — bit-exact); the clone must deep-copy every Run_State array (routing/bundles/flow/crisis/health/era_gate) — pinned by a hash round-trip test. Pending commands (apply_tick in (tick, window]) must be replayed by the shadow or demo draws mid-window diverge the telegraph."

Generalizes: telegraph/prediction features on a deterministic sim are a cloned-state replay — the correctness pins are a full deep-copy (hash round-trip test) plus replay of the pending-command window, not just the committed state.

## 9. Odin `#load` embeds data at COMPILE time — rebuild after any data-token edit [SINGLETON]

Sightings:
- packet-plumber-v2-node-clarity (2026-08-22): "Odin #load embeds data files at COMPILE time — after any palette.json token edit, REBUILD the harness before re-rendering (a stale embed silently renders old colors and wastes a re-bless cycle)."

Generalizes: compile-time-embedded assets make "edit data → re-run" silently stale — the rebuild is part of the edit, and the failure mode (old data, green-looking render) is invisible.

## 10. Offline sims under-predict the real render — calibrate a new gate on the real baseline first; screen with sim, settle with real renders [SINGLETON]

Sightings:
- packet-plumber-v2-node-clarity (2026-08-22): "The blur-gate sampler must be calibrated before trusting it: build the σ6 sampler first, confirm it reproduces the audit's baseline deltas (res↔sbiz ~3-4°, res↔campus ~13°, router↔host ~9.7°) on the OLD golden, then iterate. Offline PIL sprite-composition sims under-predict the real render's saturation (real board surroundings darken/mix) — screen with the sim, settle with real renders."
- packet-plumber-v2-node-clarity (2026-08-22): "Keep token edits ADDITIONS-ONLY when a sibling job owns shared tokens (POP owns the network) — and re-emit palette.json in its original aligned format (json.dump reformat churns 700 lines)."

Generalizes: a new measurement gate earns trust by reproducing known baseline numbers on the OLD golden before it judges new work; offline sims are for screening only. Sibling-shared data files: additions-only edits + preserve the file's exact formatting.

## 11. Discrete tick clamps falsify continuous rate formulas; a global pace re-tune ripples into EVERY exact-tick pin [SINGLETON]

Sightings:
- packet-plumber-v2-pace-tuning (2026-08-21/22): "the raw accrue/1000 formula OVERSTATES the rate whenever accrue > 500 milli; demand tests must derive from the clamp."
- packet-plumber-v2-pace-tuning (2026-08-21/22): "A 4× pace re-tune ripples into EVERY exact-tick/unit test pin (17 files, 46 pins) AND the health stagings … the 'exit just after the expiry' staging needs the fix ≥300 (at 241 the exit beats the expiry and the meter never drains)."

Generalizes: in a tick-sim, effective rates come from the integer clamp (`1/ceil(1000/accrue)`), not the continuous formula — tests derived from the formula are wrong; and any global pace change is a suite-wide re-derivation, not a local re-pin (staged scenarios have minimum-distance constraints between events).

## 12. Headless daemon (launchd) hardening: absolute PATH resolution, PATH error ≠ provider verdict, sandbox isolation hooks, self-test literal trap [SINGLETON job, 4 lessons]

Sightings:
- orchestrator-night-watchman-hardening (2026-08-22): "quota-probe + night-watchman resolve pi/herdr/jq absolutely (PI_BIN env → … → command -v); a PATH error is NEVER a provider verdict — probe exits 2 with NO regime write, watchman startup FATALs on unresolvable herdr/jq, and a broken probe is logged+notified as TOOL-BROKEN (the 23:38Z misread class)."
- orchestrator-night-watchman-hardening (2026-08-22): "Sandbox isolation hooks (NIGHT_WATCHMAN_LOG/STATE_DIR/LOCK_DIR/NOTIFY=0) keep test runs out of the live service's files — the live watchman never skipped a tick during the whole verification (isolated lock matters: --once shares the lock dir)."
- orchestrator-night-watchman-hardening (2026-08-22): "Self-test assertions that grep $0 must not contain the literal word they assert (the no-create regex's `kill` flagged itself) — break the literal with a bracket class (kil[l])."

Generalizes: launchd/headless tools must resolve every binary absolutely and distinguish TOOL-BROKEN from a real verdict; verification of a live service runs under env-var sandbox isolation (never on the live state); self-tests grep their own script only with broken-literal patterns.

## 13. pi extension authoring/loading facts: jiti ESM-only, JSON.stringify emission kills the template-literal ParseError class, discovery glob depth [SINGLETON job]

Sightings:
- orchestrator-role-skills (2026-08-22): "Generator emission trick: JSON.stringify/json.dumps double-quoted strings (ensure_ascii=False) — backticks/${}/quotes/backslashes become inert; no template literal, so the 2026-08-01 ParseError class is impossible."
- orchestrator-role-skills (2026-08-22): "The extension discovery glob is `.pi/extensions/*.ts` + `*/index.ts` (no deeper recursion, loader.js) — generated helper modules importable from extensions belong in a subdir WITHOUT index.ts."
- orchestrator-role-skills (2026-08-22): "jiti/static is ESM-only … from CJS use dynamic import of the absolute lib path, never createRequire." Plus: a `pi -e <ext> -p --no-session -nt "Reply OK"` boot from a NEUTRAL cwd is the zero-side-effect full-load test (hardcoded-cwd guards short-circuit; verify via session jsonl).

Generalizes: generated extension code should be emitted as JSON-stringified literals (structurally immune to the backtick ParseError class); extension load-testing = a neutral-cwd one-shot boot; helper modules live in index.ts-less subdirs.

## 14. Vision-model provenance: the auto catalog may already declare image input; `--no-session` writes NO jsonl; pin sessions by prompt text, never model name [SINGLETON job]

Sightings:
- orchestrator-vision-tooling (2026-08-22): "glm-4.6v needs NO ~/.pi/agent/models.json entry — the auto-fetched models-store.json catalog already declares `input: [\"text\",\"image\"]` and the E2E proved the attachment passes … only add a user-level override when a target model genuinely lacks the declaration."
- orchestrator-vision-tooling (2026-08-22): "a `--no-session` run writes NO session jsonl — for a provenance check run without it; pin the session by its exact prompt or file-attachment TEXT PART, never by grepping the model name (the AGENTS.md canon puts \"glm-4.6v\" into EVERY session's context)."
- orchestrator-vision-tooling (2026-08-22): "~/.pi/agent/skills/vision-read symlink is MISSING (pre-existing …); the skill ships repo-only at .agents/skills/vision-read and agents in other cwds may not resolve it."

Generalizes: check the fetched model catalog before writing models.json overrides; provenance forensics need a session (--no-session leaves none) and a unique prompt-text key (model-name greps false-positive when canon mentions the model); repo-only skills don't resolve from other cwds without the user-level symlink.

## 15. Edit-batch anchor traps: em-dashes atomically reject the whole batch; store-copy wrapping differs from in-context rendering — grep the exact anchor first [2+ SIGHTINGS]

Sightings:
- packet-plumber-v2-noc-player-toggle (2026-08-23): "an em-dash in oldText can silently fail the WHOLE batch (atomic reject, 'edits[N] not found' while the block is verifiably present) — use minimal ASCII-only anchors, or a python replace for em-dash-heavy regions."
- dream-2026-08-21 (Bob, 2026-08-21): "Store-copy anchors WRAP differently than the in-context project_instructions rendering — grep the exact anchor text in the copy before authoring edit batches (first 8-edit batch bounced cleanly on wrapping, second landed whole)."

Generalizes: edit-tool batches are atomic and anchors must be verified against the ACTUAL bytes of the target file (special chars, wrapped copies) — one bad anchor rejects every edit in the batch; minimal ASCII anchors or scripted replaces for punctuation-heavy regions.

## 16. Large-doc diet: segmented line surgery beats full-file rewrites; report the honest floor [SINGLETON]

Sightings:
- orchestrator-playbook-diet (2026-08-21): "full-file rewrites from memory re-inflate to ~950+ lines — the reliable diet is SEGMENTED line surgery (measure per section → exact-string replace → re-measure), not whole-file rewrites."
- orchestrator-playbook-diet (2026-08-21): "the 650-line core target has a doctrine floor ~700: the keep-list sections … are irreducible without cutting doctrine — report the honest number (713) and flag it in the PR."

Generalizes: shrinking a large canon doc = measure→replace→re-measure per section (rewrites from memory re-inflate); when a target is unreachable without cutting doctrine, ship the honest measured number flagged in the PR rather than a fake hit.

## 17. lavish verdict retrieval: check state.json chat when the poll returns dom_snapshot / 0 prompts [SINGLETON]

Sightings:
- orchestrator-playbook-diet (2026-08-21): "lavish session 'ended by user' with the verdict in the session chat (`~/.lavish-axi/state.json` → sessions.<id>.chat) even when prompts shows 0 — check chat when the poll returns a dom_snapshot."

Generalizes: a lavish session's verdict can live in the chat channel of state.json rather than the prompts/annotations path — a 0-prompt poll on an ended session means "look in chat", not "no verdict".

## 18. Local reference assets for lavish reports: keep out of repo, serve via a local http.server pane (symlinks get 403) [SINGLETON]

Sightings:
- packet-plumber-v2-design-audit (2026-08-22): "MM images must stay in _local-refs (never in repo). A symlink into the artifact dir gets 403'd by lavish's static root; serve the refs from a tiny `python3 -m http.server 4388 --bind 127.0.0.1` pane rooted at _local-refs and reference `http://127.0.0.1:4388/mm/...` in the HTML — browser-safe, repo-clean."

Generalizes: IP-guardrailed reference assets reach a lavish HTML report via a loopback http.server pane rooted at the refs dir — never via symlinks into the artifact (static-root 403) and never committed to the repo.

## 19. Input ownership: ONE consumer per input source; shared input-struct field-name collisions; dispatch-time vs step-loop event semantics [2+ SIGHTINGS]

Sightings:
- packet-plumber-v2-camera-zoom (2026-08-23): "The wheel-ownership trap: the OLD NOC scroll read GetMouseWheelMove in the render block — keep ONE wheel consumer (the effect), or the same notch double-fires as a scroll AND a zoom."
- packet-plumber-v2-sound-immediacy (2026-08-22): "`Input.events` is already the Device_Event scratch buffer — name the app-side event ref `sim_events` (the `ictx.events[:]` dispatch call shadows any field named `events`)."
- packet-plumber-v2-sound-immediacy (2026-08-22): "Parity (drive_parity) dispatches ALL frames BEFORE its step loop — a dispatch-time event lands before the hash mark and never rides the pinned stream; keep `sim_events` nil there."

Generalizes: polled inputs and shared input structs are single-owner resources — two readers of one source double-fire, a colliding field name silently shadows, and events injected at dispatch-time bypass the step loop's recorded stream.

## 20. Sibling-PR merge folds: index-based pins re-point; obsolete sibling gates AND their pinned tests must be retired [SINGLETON]

Sightings:
- packet-plumber-v2-noc-player-toggle (2026-08-23): "when a sibling PR (camera) adds a settings row at the SAME index you did, the merge keeps BOTH — your row moves up (PULLBACK=4, NOC=5, SETTINGS_ROW_COUNT 6) and the W2 nav pin must be re-pointed to the new depth."
- packet-plumber-v2-noc-player-toggle (2026-08-23): "a sibling's PP_DEBUG compile gate around a runtime feature (effect_overlay / wheel scroll) is OBSOLETE once you ungate the feature — ungate their gate too (a PP_DEBUG-only scroll body dead-zones the wheel in every normal build) and update THEIR test that pinned the old two-build behavior."

Generalizes: a post-merge fold is not just conflict resolution — merged siblings shift index/ordinal pins (both rows survive a same-index add), and ungating a feature retroactively invalidates a sibling's compile gate plus the test that pinned the gated behavior.

## 21. Top-down look-gate doctrine: what actually reads at ~60° elevation (two-tone roofs, proportional cast shadows); coplanar plates z-fight [SINGLETON]

Sightings:
- packet-plumber-v2-blender-sculpt (2026-08-23): "at the MM top-down tilt (~60° elevation), sub-mass stacking (setback blocks) reads as MUDDY STRIPES, and wall-band shading alone stays subtle — the depth that actually reads is (a) the two-tone ROOF (gable barns / hip caps …) and (b) the engine-drawn CAST SHADOW (12-18% ink @ fixed 2px offset is an invisible sliver; 25-33% ink @ proportional offset 0.08w/0.10h down-right reads). Coplanar plate overlaps z-fight — butt-joint instead."

Generalizes: depth modeling effort must be spent where the camera can see it — at steep top-down tilts, roof tone-splitting and proportional cast shadows carry depth; sub-roof massing and wall bands are wasted polygons; coplanar geometry must butt-joint.

## 22. Blender-MCP exec chunking: fresh globals per call, driver_namespace for helpers, small chunks, rebuild-don't-patch partial state [SINGLETON]

Sightings:
- packet-plumber-v2-blender-sculpt (2026-08-23): "Blender-MCP exec chunks run in a FRESH globals namespace per call — imports don't persist; park helpers in `bpy.app.driver_namespace` and re-import `bpy/os/Vector` at the top of every chunk (and if a helper needs a module, inject it into `helper.__globals__`). Keep chunks small (~<100 lines — a big one died mid-write with a broken pipe, and a partial exec leaves partial scene state; clear and rebuild, don't patch)."

Generalizes: MCP-exec surfaces with per-call namespaces need self-contained small chunks and helper-parking in a persistent namespace; a partially-executed chunk leaves corrupt scene state — the recovery is clear-and-rebuild, never incremental patching.

## 23. Downloaded-asset pipeline: verify magic bytes, fail LOUDLY on load fallback; raylib LoadFontData compacts glyph arrays [SINGLETON]

Sightings:
- packet-plumber-v2-font-overhaul (2026-08-23): "a font-load failure must FAIL LOUDLY: the ibmplex gallery frames were silently Open Sans because a curl'd TTF was actually a 404 HTML page and LoadFontEx fell back quietly … google/fonts raw URLs for IBM Plex static TTFs 404 … ALWAYS verify TTF magic bytes (00 01 00 00) after any font download."
- packet-plumber-v2-font-overhaul (2026-08-23): "raylib LoadFontData COMPACTS the glyph array (missing codepoints are SKIPPED — lookup is by glyph.value, never index) — a fallback merge must APPEND fallback glyphs into a MemAlloc'd array (raylib's UnloadFont frees it; never mix allocators)."
- packet-plumber-v2-font-overhaul (2026-08-23): "macOS PLATFORM_MEMORY GetTime() returns 0 → SetTargetFPS(60)'s busy wait … spins FOREVER in EndDrawing … — skip the limiter in SW builds"; "the raylib-sw shadow has NO raudio — the app's audio package needs `when #config(PP_SW_AUDIO,false)` gating to link."

Generalizes: any curl'd binary asset is unverified until its magic bytes check out (404-HTML poisons goldens via silent fallback — loaders must fail loudly); library "load" APIs may compact/reindex arrays (lookup by semantic key, never index) and free what they allocated (never mix allocators).

## 24. Mechanical-evidence E2E for view-layer features (PP_CAM_E2E); keep view state out of the deterministic harness path [SINGLETON]

Sightings:
- packet-plumber-v2-camera-zoom (2026-08-23): "PP_CAM_E2E (PP_DEBUG + env) is the mechanical-evidence pattern for view-layer features: real Device_Events injected in handle_input, TakeScreenshot after EndDrawing, pixel-scan the before/after (paper-fraction + diff-frac)."
- packet-plumber-v2-camera-zoom (2026-08-23): "the 7.1 camera model (eased cam_zoom/cam_wx/cam_wy targets on App, camera_update deriving view scale/off) is the WHOLE camera — zoom/pan = set the targets, zero render-layer changes; the harness never runs camera_update so T2 stays byte-identical by construction."

Generalizes: view-layer features get their evidence from an env-gated E2E harness that injects real input events and pixel-scans committed captures; architecting the feature as pure target-state outside the sim/harness loop keeps goldens byte-identical by construction.

## 25. Dream/minion self-verification: a dispatch can arrive before its ledger row; tail-read marker-dated sources (backfill caveat confirmed again) [SINGLETON — Bob-meta, prior dream's own shard]

Sightings:
- dream-2026-08-21 (Bob, 2026-08-21): "Dream dispatch can arrive WITHOUT a ledger row (first `set` said 'no such job'; Silas' add raced my start) — self-verify with `ledger show` before assuming either way."
- dream-2026-08-21 (Bob, 2026-08-21): "The U1 backfill caveat paid off AGAIN: wire-aesthetics' tail (mtime pre-marker) still carried undreamed Odin facets — tail-read every marker-dated source, not just the mtime-newer set."

Generalizes: a ledger row can race its dispatch — verify row existence with `ledger show` rather than trusting the first set's error; and mtime is not a dreaming boundary — every marker-dated source gets a tail-read. (This dream applied the second lesson to the two tail-reads above: both were clean pre-marker.)

## 26. Small language/tooling traps: Odin const float arithmetic truncates [SINGLETON]

Sightings:
- packet-plumber-v2-noc-readability-2 (2026-08-23): "Odin const arithmetic: `NOC_PANEL_W :: i32(360 * 1.4)` TRUNCATES to 503 (float const 503.999...) — use int math `360 * 14 / 10` for the 504 rail."

Generalizes: float-constant arithmetic in Odin const decls truncates on i32 conversion at exact-looking values — express integer UI geometry in int math.

## 27. Harness `overlay-check`-class verbs take the `ms`-suffixed duration form [2+ SIGHTINGS — minor]

Sightings:
- packet-plumber-v2-noc-player-toggle (2026-08-23): "The harness `overlay-check` verb's ms arg needs the `ms` suffix (`parse_ms` requires it): `harness-debug overlay-check surge 3000ms`, not `3000` — a bare number falls to usage()."
- packet-plumber-v2-noc-readability-2 (2026-08-23): "the overlay-check verb takes the `12000ms` suffix form; both overlay verbs must view_set_rail(true) so the capture matches the app."

Generalizes: harness debug verbs fail silently to usage() on bare-number durations — the `ms` suffix is mandatory (and overlay captures must set the same view flags as the app or the capture doesn't represent it).

## 28. A geometrically-impossible design ruling → surface the math, ship the sanctioned resolution, document in the PR [SINGLETON]

Sightings:
- packet-plumber-v2-noc-readability-2 (2026-08-23): "The DOCK-RIGHT ruling's geometry is IMPOSSIBLE to satisfy by re-anchoring the top band into the shrunken playfield (title 180 + health 460 + forecast 250 = ~890px > play_w 756 at 1280) — the sanctioned resolution is: fit-to-rail camera … + top band cards KEEP win_w anchors and draw OVER the rail … Document in the PR."

Generalizes: when a design ruling is arithmetically unsatisfiable, the minion move is to show the arithmetic, implement the explicitly-sanctioned alternative, and document the deviation in the PR — not to silently approximate the ruling.

---

## Cross-cutting observations for Bob

- **The 2+ cluster is dominated by the verification stack**: patterns #1 (vision ≠ evidence), #3 (piped runs mask failure), #5 (GPU captures lie / SW shadow only), #6 (decoded pixels not bytes) are four facets of ONE meta-doctrine — *every capture/compare/verdict step in the render pipeline has a known silent-failure mode, and evidence only counts when produced by the mechanical path*. The PP v2 crew has converged on this across 8+ jobs in 48h.
- **Provider/model layer stayed quiet** this window (only the KYLE 4.6v-vs-5v-turbo note in #2 and the TOOL-BROKEN-vs-provider-verdict line in #12) — no new quota/403 incident classes in these shards.
- dream-2026-08-21's own notes (#15, #25) confirm the backfill caveat and add the ledger-row race — worth folding into the dream template if not already there.

DONE (sheep-shards, 28 candidates)
