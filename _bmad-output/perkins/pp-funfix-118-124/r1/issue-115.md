title:	[PLAYTEST-UX] Core HUD signifiers undefined in-game: POOL, red !! rings, tier-vs-lane colors, the E/S/B third lane
state:	OPEN
author:	mssoka (MSS)
labels:	enhancement, playtest
comments:	0
assignees:	
projects:	
milestone:	
number:	115
--
## Confusion moments (blind + informed sessions)
The HUD's core signifiers are never defined anywhere a player can reach. Each of these cost me a stopped-and-squint moment, and two I **never** resolved even in the informed session:

1. **`POOL 58/512`** (bottom-left, with a progress bar). I guessed money, then ammo, then packet budget. In the sim it relates to bundle pooled capacity (a demolish mid-traversal "shrinks the pool gracefully"), but what the HUD number aggregates — the selected bundle? the whole network's pooled cap vs offered load? — is nowhere stated. It also *drains in real time*, which reads like a fail-state ticking down (it isn't, or is it? I still can't say).
2. **Red `!!` rings around buildings.** At 90s into a Dublin run the map was covered in them while the stats stream reported 0% loss, 100% health, 506 delivered. Unconnected estate during surge? SLA breach? pressure warning? Each implies a different player action (build, upgrade, wait). No legend, no tooltip, no doc.
3. **Pipe color = tier or lane?** Standard renders blue-ish/thin, wide renders yellow/fat — but a QoS-categorized pipe also repaints. A player cannot tell from color whether they're looking at capacity or policy, and the a11y hint line ("ring + glyph, never color alone") implies glyphs exist for state but none were identifiable at map zoom.
4. **The weights ladder `basic x6 / mid x0 / high x0` chips and `E/S/B` thirds.** Only two packet types ship (email, streaming — per `data/packet_types.json`), yet the QoS ladder has three lanes (50/30/20). What the third lane (B) is, and what "x6" counts (placed nodes? available slots?), is unexplained.

## What I assumed
POOL = currency; red rings = SLA breach; chip counts = inventory.

## Concrete clarity fix
A one-screen legend (toggle `?` or first-run overlay) defining: POOL (with its denominator), ring/glyph severity ladder, tier-vs-lane color ownership (one of them should own color; the other gets weight/texture/glyph per the game's own a11y doctrine), and the lane roster. Cheap unit: reuse the stats-stream header grammar — the systems are all named there, just never in-game.

## Evidence
Build `61ea014`. Captures: `neweyes-informed1` 90s frame (red rings + healthy stats), `neweyes-informed2` 30s/65s (thin-blue → fat-yellow modernize), `neweyes-informed3` (repainted categorized pipe).

