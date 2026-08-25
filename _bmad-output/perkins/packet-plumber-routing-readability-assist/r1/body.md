## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-routing-readability-assist · **Reviewed sha:** `b0a6def` · **Reviewers:** 7/7 completed
**Verification:** 17/21 findings confirmed against the code — 4 discarded as false-positive

**Empirical gate (all green at the reviewed sha):** `odin build app` links · `tools/lint.sh` 5/5 · `odin test core` 126/126 · `tools/harness.sh run` 16/16 demos · `tools/harness.sh preview-check` 7/7 (preview == sim routing cross-check) · 70/70 golden files byte-identical to baseline `69fc2e5` · zero `core/` files in the diff · LOG_VERSION untouched, no new commands. The four acceptance surfaces (R2a ONE-number preview + cost-aware ghost, T-tier toggle + data-driven opt-in nudge, R3 post-draw glow, T2 tie cue) all function; the glow-gen gate was traced manually (fast-path apply precedes the capture — post-apply gen, correct).

### Blockers (0)

None.

### Warnings (5)

1. **[tests, blind] S5 does not pin the E29 mid-flight rule** — `harness/assist_check.odin` (S5): the candidate `{1,3,wide}` with no 3-4 pipe is excluded from the DAG from *either* `at_node` or `heading`, so the `on_edge → start = heading` branch has zero discriminating coverage. The code is correct; the test that claims to pin it does not.
2. **[architecture] A parallel-pipe routing no-op ON the winning path still fires the preview** — `app/render/assist.odin` `dag_has_edge` is pure pair membership; drawing a second pipe on an existing bundle changes no routing (min edge cost unchanged) yet previews "route N". The I/O matrix's "no glow, no route number for a no-op draw" is pinned only for the pair-upstream case (S7). Misleading preview for a redundant draw — suppress when the winning path is unchanged, or document as intended.
3. **[architecture, tests, codebase] The preview-vs-sim cost cross-check uses a mirrored pricing scan** — `min_bundle_cost` (assist.odin), `check_min_cost` (harness), and the table's pass-1 min scan are three copies of the same rule; the check compares two copies of the scan, so a systematic pricing error would pass. The literal pins (`want 20/10/15`) anchor the fixtures, but non-fixture topologies are self-referential. Consider exporting the scan from core.
4. **[tests] The app-layer surfaces have zero automated pins** — the R3 glow lifecycle, the two-buffer copy (this round's HIGH glow-buffer fix), the T toggle, and the nudge latch are untested (no `app/` test file; the harness drives only `preview_compute`). A regression in any of the four acceptance surfaces would ship green. Recommend a headless app-level pin or an extended `preview-check`.
5. **[security, edge] Per-drag-frame preview rebuild leaks temp-arena memory** — `routing_rebuild` allocates 4 temp arrays per call and the app never `free_all`s (arena-free, ODN-18 [LATER]); every drag move frame leaks ~1-2 KB to the default temp allocator, unbounded across a session of heavy dragging. Cache the rebuild scratch in `Preview_Scratch` or add the per-frame arena.

### Notes (7)

1. **[blind] `topology_clone_into` hand-copies an explicit field list** — complete today (all 17 Topology fields verified); the hazard is future fields silently missed. Add a struct-adjacent comment or shared clone.
2. **[blind] `draws_since_nudge` counts every commit, not "N draws in Full mode"** — a player toggling back to Full can see the nudge after fewer than N Full-mode draws.
3. **[blind] A commit with no live preview truncates a running R3 glow** (`glow_until = 0` on the no-preview branch) — defensible design, but a literal R3 read says "keeps glowing for glow_ticks". Name the truncation as intended if keeping it.
4. **[blind] An active drag blanks the committed R3 glow** even with no valid candidate (flicker during the window; returns on release). Cosmetic.
5. **[edge] The graduation nudge lingers frozen on the Game_Over screen** where its dismiss key (T) is dead — gate the nudge draw to Run mode.
6. **[acceptance] N lives in `data/assist.json`, not balance.json** — deviation correctly documented in-spec and flagged for the human; rationale (balance.json folds into cat.hash → re-blesses ALL goldens) verified sound. Move at the next legitimate re-bless. Validation + fallbacks are solid.
7. **[tests] The preview-check negative control is a manual local run, not committed** — consider a committed mutation pin (drift-check pattern).

### Reviewer agreement

Multi-lens confirmations: W1 (security+edge), W3 (architecture+tests+codebase), W4 (tests+blind). No lens disagreements on verdict-relevant claims; the single "high"-severity blind claim (glow_gen captured pre-apply) was rejected on re-verification — the ODN-2 fast-path applies the edit before the capture.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
