# Kyle Final Note: Packet Plumber v2 Design Audit Status

## Current State
- The Lavish Editor session was **ended by the user** (status: ended, ended_by: user). No further visual mockup iterations were completed after the user's feedback that mockups did not show meaningful redesign changes.
- The design-directions spec (kyle-design-directions.md) contains complete specifications for all 6 required areas (Scale & Node Footprint, Palette & Saturation, Node Identifiability, Packet Motion, Spawn Feel, Shadows & Depth) with:
  - Current state vs MM target state comparisons
  - Exact proposed directions (palette hex pairs with 70/30 weighting, node silhouette specs, depth/shadow treatment, motion-read notes)
  - Specific MM reference images cited for each direction
  - Pixel-verified numeric targets and measurements

## Design Directions Summary
### 1. Scale & Node Footprint
- **Current**: House = 36px, campus = 53px, standard pipe band = 11.2px → nodes 3.2x (house) and 4.7x (campus) band width
- **MM Target**: Houses ≈ 0.5–1.0× road width; large blocks ≈ 1.0–2.7× road width (MM image_01/07)
- **Proposed**: House → 0.8–1.0 tiles (32-40px), campus → 1.4 tiles (56px), router puck → 15px base → 27px diameter, standard pipe tier → 15px wide

### 2. Palette & Saturation (POP)
- **Current**: Top-2% saturation ceiling = 0.51–0.57 (calm frames) vs MM 0.91–1.00 (image_01/05)
- **MM Target**: MM's network pops with saturated roads/cars
- **Proposed**: Calm board: 70% cool-cyan (#87CEEB), 30% warm-gold (#FFD700); Network: 70% warm-gold (#FFD700), 30% cool-cyan (#87CEEB); Target saturation ≥0.85

### 3. Node Identifiability
- **Current**: Small_biz/campus share warm-brown, content_host blue, residential red-brown; blur-test hue deltas: residential↔small_biz 3°, residential↔campus 13° (borderline)
- **MM Target**: MM buildings have distinct shapes per type (image_02/04/06/08)
- **Proposed**: Small_biz → cool-stone (#A0937D), campus → brick (#8B4513), residential → warm-terracotta (#CD5C5C), content_host → deep-blue (#4682B4); Blur-test cure: ≥15° hue separation, sat band ≤0.3

### 4. Packet Motion
- **Current**: Packets render at 20Hz quantized positions (no sub-tick interpolation); motion strips show choppy motion
- **MM Target**: MM cars read with consistent speed and trails (image_01/03/05/07)
- **Proposed**: Sub-tick linear interpolation, 3-frame fading trails, packet size +15% (8px → 9.2px), glint tuning for speed perception

### 5. Spawn Feel
- **Current**: Instant pop, zero telegraph (code-verified: no spawn animation)
- **MM Target**: MM has spawn telegraph and reveal (image_01/03/05/07)
- **Proposed**: Telegraph ring animation (scale 0→1.2→1.0, fade 0→1→0.8), scale/fade reveal (0→1 over 200ms), pipe highlight pulse (200ms duration)

### 6. Shadows & Depth
- **Current**: Shadow = 0.64w×0.36w ellipse (16% ink) under every node (uniform); Background map: 34% canvas, 49% water, 9% park
- **MM Target**: MM uses soft drop shadows offset down-right, scaling with building size (image_07); MM background: 51% plain paper, 26% water, 11% warm land tint
- **Proposed**: Shadow per-footprint scale (house: 0.5w×0.3h, campus: 0.7w×0.4h), offset down-right 2px, ink 12-18% based on node size; Atmospheric depth: subtle haze, far-node blur (radius 1px)

## Next Steps
- The orchestrator will now handle user conversation regarding the design directions and mockup feedback.
- No further tool calls should be made until explicitly requested by the user or orchestrator.