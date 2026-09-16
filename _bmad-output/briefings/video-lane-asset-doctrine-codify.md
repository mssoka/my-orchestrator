# Briefing: codify Video-Lane Asset Doctrine as standing canon (Silas self-edit micro-PR)

**Ruling provenance:** user approved Gru's asset-doctrine recommendation in chat
2026-09-08 and ordered: "codify this as the standing Video-Lane Asset Doc."
The content below is VERBATIM from the user-approved recommendation — do not
reword, do not re-litigate, do not expand scope.

## Lane shape (user-ruled canon self-edit)

- **No minion, no lavish, no review swarm.** Silas' own micro-PR.
- Worktree @ `origin/main` of `youtube-channel`.
- `pr_review=0`. Lavish NOT needed — PR directly (user-ruled verbatim canon;
  the exemption is the intent here, stated explicitly).
- Target files:
  - NEW `docs/video-lane-asset-doctrine.md` — content VERBATIM from the
    fenced block below (headings intact).
  - `README.md` — append ONE pointer line under existing content:
    `- Standing asset sourcing rules for all videos: [docs/video-lane-asset-doctrine.md](docs/video-lane-asset-doctrine.md)`
- PR body: write from a FILE (never a heredoc — backtick-eating class).
  Body: one paragraph (what/why/ruling provenance) + receipt list.
- Ledger row: id `youtube-channel-video-lane-asset-doctrine`, `pr_review=0`,
  note carries "user-ruled canon self-edit, content verbatim from briefing".
- Base branch: `main`.

## Receipt contract (verify ALL in `git diff` before opening the PR)

1. Title line exactly: `# Video-Lane Asset Doctrine (standing)`
2. Core-rule line exactly: `**Screen-time × proximity decides asset budget. If the camera studies it → build it bespoke. If the camera glances → take it free.**`
3. Matrix present with exactly 6 route rows (hero / humanoids / environments / textures-HDRI / effects / background props).
4. The rule line: `**Never re-rig a third-party creature.**`
5. README pointer line present.
6. NOTHING else changed (no drive-by edits, no reformatting of README).

## Dispatch parameters

- repo: `youtube-channel`
- repo_root: `/Users/moses/code/youtube-channel`
- slug: `video-lane-asset-doctrine`
- base: `main`
- model: n/a (Silas self-edit)
- pr_review: 0
- lavish: not needed, PR directly
- Does NOT touch the live Selva Blender session, PID 59538, or any lane
  currently in flight.

---

## VERBATIM DOC CONTENT (copy into docs/video-lane-asset-doctrine.md exactly)

```
# Video-Lane Asset Doctrine (standing)

**Status:** Standing canon, user-ruled 2026-09-08 (user approved Gru's
recommendation and ordered it codified). Applies to ALL music-video
production in this repo. Complements the 2026-09-07 user ruling: direct
Blender MCP is the primary production route; the Higgsfield bridge is
retired for native work.

## Purpose

Make music videos faster without losing control: how assets, effects,
rigs, and environments are sourced; when we build bespoke vs take
free/third-party; what compounds into the in-house library.

## The core rule — screen time decides the budget

**Screen-time × proximity decides asset budget. If the camera studies it → build it bespoke. If the camera glances → take it free.**

Rationale: a bespoke asset gives full art control, a rig built for our shot
vocabulary, fixable weights and naming, and MCP-scriptability — but costs
days. A third-party asset is instant but generic and license-encumbered,
and modifying someone else's rig is *debugging a stranger's scene graph*:
renamed bones, mystery drivers, baked constraints, naming that breaks every
script. Our own evidence (Selva hero moth, 2026-09-08): the bespoke 61-bone
rig is the reason the wing-collision fix was possible at all; a downloaded
moth with the same defect would be unfixable without reverse-engineering
foreign weights — slower than modeling clean.

## The asset matrix

| Asset class | Route | Why |
|---|---|---|
| Hero characters/creatures (close-up, long screen-time, stylized) | Bespoke, always | Full control, own rig conventions, MCP-scriptable, fixable; cost amortizes into the library |
| Humanoids | Auto-rig third-party (Mixamo-style) | The one category where auto-rigging genuinely works; never hand-rig humans |
| Environments/nature (jungle, terrain, sky) | Free + procedural (PolyHaven CC0, geometry-nodes scatter, alpha-card foliage at distance) | The camera never studies an individual background tree; dense scenery = alpha cards, not 4K-poly trees |
| Textures / HDRI / materials | Free libraries (PolyHaven, ambientCG, BlenderKit free tier) | CC0 = monetized-YouTube-safe; MCP download tools fetch directly into the scene |
| Effects (explosions, smoke, splashes) | VDB libraries + particle presets | Baked caches render in seconds; sim time is the silent killer |
| Background props (one-glance objects) | AI-gen or free | Good silhouette, bad topology — irrelevant at distance |

## Rules that ride the matrix

1. **Never re-rig a third-party creature.** Modifying a stranger's rig
   usually costs more than a clean rebuild (the modify-lose rule). Only
   exception: humanoids via auto-rig.
2. **MCP-scriptability:** anything animated or controlled via MCP needs
   clean, predictable, convention-following naming. Self-made or
   explicitly cleaned assets only.
3. **Licenses:** CC0 or clearly-permissive only (monetized channel).
   Record provenance per asset in the project's asset log. The MCP
   download tools are the standard intake lane for free assets.
4. **IP guardrail:** reference assets staged outside repos (orchestrator
   `_local-refs/`) are cite-only — never copied into a repo tree.
5. **Baked over live:** never re-simulate what a VDB cache or particle
   preset can fake.
6. **EEVEE-first:** EEVEE for animatics and most stylized finals; Cycles
   only where light transport demands it.
7. **Preservation-first on live .blend state:** unexpected dirty state =
   hold + timestamped checkpoint copy + headless comparison BEFORE any
   restore/discard (the frame129/frame69 anomaly class, standing since
   2026-09-08).

## The compounding library

Every bespoke hero asset is versioned, hashed, and documented (checkpoint
pattern in use: hero_showcase-v5/v6 with SHA receipts). The library is the
moat: video two costs half of video one. Never discard superseded versions;
archive them.

## Build-once pipeline gaps (one-time tasks, reused every video)

- Curated CC0 PBR material set (PolyHaven via MCP download)
- HDRI set + 2-3 saved lighting templates ("moods")
- VDB/particle effects pack (splashes, smoke, dust)
- Geometry-nodes scatter rig for environments
- Compositing/grade node-group template
- Storyboard step: grease pencil or reviewed HTML beat sheet — catches bad
  shots before the expensive render

## Gates preserved

Final visual/look verdicts stay with the user (Lavish session). Nothing in
this doctrine authorizes remote, paid, destructive, or upload actions by
itself.

## Changelog

- 2026-09-08: adopted (user approved Gru's recommendation; content
  codified verbatim).
```
