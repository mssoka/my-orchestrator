# Packet Plumber v2 Design Directions (MM Bar)

## 1. Scale & Node Footprint
- Current: Our house = 36px, campus = 53px, standard pipe band = 11.2px → our nodes are 3.2x (house) and 4.7x (campus) the band width.
- MM Target: MM houses ≈ 0.5–1.0× road width; large blocks ≈ 1.0–2.7× road width (image_01, 07). MM image_07: house 65px, road ~68px → house:road ≈ 0.96; MM image_01: road 228px, houses ~105px → 0.46x, big blocks 228-624px → 1.0-2.7x.
- Proposed Direction: House → 0.8–1.0 tiles (32-40px), campus → 1.4 tiles (56px), router puck → 15px base → 27px diameter. Standard pipe tier → 15px wide.
- Evidence: Cite MM image_01/07 showing building scale relative to road width; our captures showing current node sizes.

## 2. Palette & Saturation (POP)
- Current: Our top-2% saturation ceiling = 0.51–0.57 (calm frames) vs MM 0.91–1.00 (image_01/05). LEFOU system-tone muted the network.
- MM Target: MM's network pops with saturated roads/cars (image_01/05).
- Proposed Direction: Calm board: 70% cool-cyan (#87CEEB), 30% warm-gold (#FFD700); Network: 70% warm-gold (#FFD700), 30% cool-cyan (#87CEEB). Target saturation ceiling ≥0.85.
- Evidence: Cite MM image_01/05 showing high saturation; our saturation measurements showing current muted state.

## 3. Node Identifiability
- Current: Small_biz/campus share warm-brown (aspect 1.45/1.48), content_host blue (1.45), residential red-brown (1.01). Blur-test hue deltas: residential↔small_biz 3°, residential↔campus 13° (borderline).
- MM Target: MM buildings have distinct shapes per type (image_02/04/06/08) and color families.
- Proposed Direction: Small_biz → cool-stone (#A0937D), campus → brick (#8B4513), residential → warm-terracotta (#CD5C5C), content_host → deep-blue (#4682B4). Blur-test cure: ≥15° hue separation, sat band ≤0.3.
- Evidence: Cite MM image_02/04/06/08 showing distinct building types; our blur-test measurements.

## 4. Packet Motion
- Current: Packets render at 20Hz quantized positions (no sub-tick interpolation). Motion strips show choppy motion.
- MM Target: MM cars read with consistent speed and trails (image_01/03/05/07).
- Proposed Direction: Sub-tick linear interpolation, 3-frame fading trails, packet size +15% (from 8px to 9.2px), glint tuning for speed perception.
- Evidence: Cite MM image_01/03/05/07 showing smooth car motion; our motion strips showing current choppy rendering.

## 5. Spawn Feel
- Current: Instant pop, zero telegraph (code-verified: no spawn animation).
- MM Target: MM has spawn telegraph and reveal (image_01/03/05/07).
- Proposed Direction: Telegraph ring animation (scale 0→1.2→1.0, fade 0→1→0.8), scale/fade reveal (0→1 over 200ms), pipe highlight pulse (200ms duration).
- Evidence: Cite MM image_01/03/05/07 showing spawn animations; our spawn strips showing current instant appearance.

## 6. Shadows & Depth
- Current: Our shadow = 0.64w×0.36w ellipse (16% ink) under every node (uniform). Background map: 34% canvas, 49% water, 9% park.
- MM Target: MM uses soft drop shadows offset down-right, scaling with building size (image_07). MM background: 51% plain paper, 26% water, 11% warm land tint.
- Proposed Direction: Shadow per-footprint scale (house: 0.5w×0.3h, campus: 0.7w×0.4h), offset down-right 2px, ink 12-18% based on node size. Atmospheric depth: subtle haze, far-node blur (radius 1px).
- Evidence: Cite MM image_07 showing building shadows; our background measurements showing MM image_01 = 51% plain paper, 26% water, 11% warm land tint vs ours = 34% canvas, 49% water, 9% park.