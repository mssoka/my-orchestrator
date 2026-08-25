# Kyle Mega-Mission: Lead Design Analyst for Packet Plumber v2 Audit

## Goal
Produce a **design-directions spec** for the Packet Plumber v2 audit against Mini Motorways (MM) aesthetic bar. The spec must be designer-facing: per problem area = current state vs MM target vs exact proposed direction (palette hex pairs with 70/30 weighting, node silhouette specs, depth/shadow treatment, motion-read notes). Cite which MM ref image supports each direction.

## Materials (all in cwd + _local-refs)
- Our captures: captures/stills/juice-30000ms.png, captures/stills/terminal_types-05000ms.png, captures/stills/router_tiers-02500ms.png, captures/crops/tt_residential.png, captures/crops/tt_small_biz.png, captures/crops/tt_campus.png
- MM refs: /Users/moses/code/_local-refs/mm/Mini-Motorways-images/Mini-Motorways-image_01.jpg, /Users/moses/code/_local-refs/mm/Mini-Motorways-images/Mini-Motorways-image_05.jpg, /Users/moses/code/_local-refs/mm/Mini-Motorways-images/Mini-Motorways-image_07.jpg
- Design direction: /Users/moses/code/_local-refs/design-videos/DIRECTION.md (Brush 5-steps + Hokkori palette-as-mood)
- Render code pointers: app/render/view.odin (draw_nodes ~607, draw_router ~836, draw_building ~684, draw_packets ~880), app/render/sprites.odin (sprite_index_building ~138, sprite_shadow ~16% ink blob), core/flow.odin (packet_progress_frac ~1048 — 20Hz quantized), data/palette.json (canvas #EDE2C8, ink #33414F)

## Task
Analyze the above materials and produce a design-directions spec file with the following sections:

### 1. Scale & Node Footprint
- Current: Our house = 1.5 tiles (36px at 1280x720), campus = 2.2 tiles (53px), router puck = 12px base → 21.6px diameter. Standard pipe band = 11px wide.
- MM target: MM houses ≈ 0.5–1.0× road width; large blocks ≈ 1.0–2.7× road width (image_01, 07). Road width MM ≈ 68px (image_07) / 228px (image_01).
- Proposed direction: Exact node footprint targets (e.g., house → 0.8–1.0 tiles, campus → 1.4 tiles) and pipe width tuning (standard tier → 15px?).
- Evidence: Cite MM image_01/07 and our captures.

### 2. Palette & Saturation (POP)
- Current: Our top-2% saturation ceiling = 0.51–0.57 (calm frames) vs MM 0.91–1.00 (image_01/05). LEFOU system-tone muted the network.
- MM target: MM's network pops with saturated roads/cars (image_01/05).
- Proposed direction: Exact palette hex pairs with 70/30 weighting (e.g., calm board 70% cool-cyan, 30% warm-gold; network 70% warm-gold, 30% cool-cyan). Target saturation ceiling ≥0.85.
- Evidence: Cite MM image_01/05 and our saturation measurements.

### 3. Node Identifiability
- Current: Small_biz/campus share warm-brown (aspect 1.45/1.48), content_host blue (1.45), residential red-brown (1.01). Blur-test hue deltas: residential↔small_biz 3°, residential↔campus 13° (borderline).
- MM target: MM buildings have distinct shapes per type (image_02/04/06/08) and color families.
- Proposed direction: Exact hue families (e.g., small_biz → cool-stone, campus → brick) + type icon chips + router tier markers. Blur-test cure: ≥15° hue separation, sat band ≤0.3.
- Evidence: Cite MM image_02/04/06/08 and our blur-test.

### 4. Packet Motion
- Current: Packets render at 20Hz quantized positions (no sub-tick interpolation). Motion strips show choppy motion.
- MM target: MM cars read with consistent speed and trails (image_01/03/05/07).
- Proposed direction: Exact motion specs (sub-tick lerp, 2–4 frame fading trails, packet size +15%, glint tuning).
- Evidence: Cite MM image_01/03/05/07 and our motion strips.

### 5. Spawn Feel
- Current: Instant pop, zero telegraph (code-verified: no spawn animation).
- MM target: MM has spawn telegraph and reveal (image_01/03/05/07).
- Proposed direction: Exact spawn animation specs (telegraph ring, scale/fade reveal, pipe highlight).
- Evidence: Cite MM image_01/03/05/07 and our spawn strips.

### 6. Shadows & Depth
- Current: Our shadow = 0.64w×0.36w ellipse (16% ink) under every node (uniform). Background map: 34% canvas, 49% water, 9% park.
- MM target: MM uses soft drop shadows offset down-right, scaling with building size (image_07). MM background: 51% plain paper, 26% water, 11% warm land tint.
- Proposed direction: Exact shadow specs (per-footprint scale, offset, ink %) + atmospheric depth (haze/vignette, far-node blur).
- Evidence: Cite MM image_07 and our background measurements.

## Output Format
Write to `kyle-design-directions.md` in this directory. Use this structure:

```
# Packet Plumber v2 Design Directions (MM Bar)

## 1. Scale & Node Footprint
- Current: ...
- MM Target: ...
- Proposed Direction: ...
- Evidence: ...

## 2. Palette & Saturation
- Current: ...
- MM Target: ...
- Proposed Direction: ...
- Evidence: ...

## 3. Node Identifiability
- Current: ...
- MM Target: ...
- Proposed Direction: ...
- Evidence: ...

## 4. Packet Motion
- Current: ...
- MM Target: ...
- Proposed Direction: ...
- Evidence: ...

## 5. Spawn Feel
- Current: ...
- MM Target: ...
- Proposed Direction: ...
- Evidence: ...

## 6. Shadows & Depth
- Current: ...
- MM Target: ...
- Proposed Direction: ...
- Evidence: ...
```

## Constraints
- Max 3-6 images per batch (already curated to 6 key images + code pointers).
- Write compactly; do not re-read the materials unless necessary.
- Cite specific MM ref images (image_01, 05, 07, etc.) and our captures (juice-30000ms, terminal_types-05000ms, etc.).
- Include exact hex pairs and numeric targets where possible.