# packet-plumber-v2-blender-sculpt

## Task

Stage-2 of the Blender heist — an agent sculpts the node-type
silhouette sprites IN Blender via the Blender MCP server, renders them
through the stage-1 pipeline, and integrates them into the game.
User intent (2026-08-22/23): the user launched Blender as the
WORKBENCH for a minion driving the blender-mcp — the sculpting is
AGENT work, not the user's.

## Source of truth (all merged/preserved — read first)

- Stage-1 silhouette spec + pipeline: PR #79 (merged) —
  `assets/blender/README.md` (the landing zone), `tools/gen_sprites.py`
  (the deterministic render), the per-type spec (residential = gable
  rect + footprint/outline ring; the other types per the spec).
- KYLE's design directions:
  `_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/kyle-design-directions.md`
  (palette/shape/depth targets) + `design-audit.html`.

## Rules (hard)

1. **MCP first**: verify the Blender addon link
   (`blender_get_addon_status`) before any sculpting. If the addon is
   not listening in the user's running Blender, ESCALATE via Silas →
   Gru → user (they enable the addon/start the listener) — never fake
   renders outside the pipeline.
2. **Original silhouettes only** — the spec is original art direction;
   no Mini Motorways assets copied or traced. IP guardrail stands.
3. **Determinism**: re-running `tools/gen_sprites.py` on the same
   .blend must produce byte-identical sprites (stage-1 proved the
   harness; keep it true). Commit the .blend sources under
   `assets/blender/` so the pipeline is reproducible.
4. **W4/W5 fold-ins (from #79 r2, carried)**: W4 camera labels inverted
   (steepest/shallowest) — fix + verify; W5 bbox-oversize guard on the
   sculpted fold-in path — add + test. Both verified in the PR body.
5. **Sim untouched**: sprites are assets — T1/T2/replay .log.bin stay
   byte-identical. Golden PNG re-bless is EXPECTED (sprite art change)
   and cause-documented.
6. **Vision gates**: k3 native vision reviews renders in-loop; KYLE
   (remote glm-4.6v, local 4.6v-flash fallback) grades the pre-merge
   gallery. **Lavish before/after gallery for the user BEFORE merge** —
   the user eye-judges the look (the look-polish precedent).
7. **Merge order**: AFTER font-overhaul's merge (font's golden storm
   lands first; sculpt rebases onto it). Coordinate with Silas.

## Acceptance

- Each node type renders from its .blend via the pipeline; sprites
  integrate into the game.
- In-game before/after captures (silhouettes live on the board) +
  lavish gallery reviewed by the user.
- W4/W5 verified; determinism re-run proven; goldens re-blessed with
  cause; T1/T2/replay hash-equal.
- KYLE readability/aesthetic verdict on the gallery.
- pr_review: 1 (Perkins on the final sha).

## Skills policy

bmad-quick-dev; lavish for the gallery. Blender via the blender-mcp
server tools (25 tools: execute_blender_code, viewport_screenshot,
scene_info, etc.).

## Model policy

kimi-coding/k3 (user-specified — native vision for in-loop render
review; probe at dispatch — k3 flapped tonight, glm-5.3 per the chain
if capped). Mega-minions: same. KYLE: glm-4.6v (remote; local fallback
lmstudio/zai-org/glm-4.6v-flash via bin/vision-read --local).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-blender-sculpt
- base: v2 (settled head; rebase after font-overhaul merges)
- model: kimi-coding/k3
- worktree: yes
- pr_review: 1
- merge order: after font-overhaul (coordinate with Silas)
