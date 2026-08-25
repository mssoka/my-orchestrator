---
title: 'Packet Plumber - Art Direction v1'
doc_type: art-direction-spec
project: packet-plumber
status: approved (lavish review 2026-08-07), v1.2 (light-cascade amendment 2026-08-08)
version: v1.2
created: 2026-08-07
approved: 2026-08-07
amended: 2026-08-08
amendment_summary: 'canvas finalized LIGHT (daytime) per A/B verdict; dark retained as reference alt; routers = ROUND capacity-scaled hub pucks (supersedes substation); 6 literal buildings; bezier pipes; procedural map; topology rule - see Amendment log (A1-A7)'
author: Samus Shepard (Game Designer) via minion `packet-plumber-art-direction`
sources:
  forge: '_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md'
  gdd: '_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md'
  architecture: '_bmad-output/planning-artifacts/architecture/architecture-v1.md'
  project_context: 'project-context.md'
  references: '/Users/moses/code/docs/game-design-references.md'
  data_catalogs: 'game/data/{packet_types,node_types,pipe_tiers,eras,balance,demand}.json'
  narrative: '_bmad-output/planning-artifacts/narrative/narrative-v1.md'
  mini_motorways_research:
    - 'Thumbsticks: How Mini Motorways built its Wuselfaktor (GDC 2023, Tana Tanoi)'
    - 'GameDeveloper: Mini Motorways and the delicate art of marrying complexity and minimalism (Dinosaur Polo Club)'
visual_lock: '[FORGE #5] Mini Motorways clean-minimalist, 2D top-down, LIGHT daytime canvas, vivid packet flow + subtle glow for emphasis'
---

# Packet Plumber - Art Direction v1

> **The thesis.** Packet Plumber is *the internet, always on, seen from above.* A light, living map where vivid flows are the lifeblood, and the player is the keeper of the connection. Mini Motorways gave us the clean line and the cheerful daytime canvas; Packet Plumber gives the line a *pulse*, a *personality*, and a *temperature*. Color is not decoration here: it is the gameplay signal. A warm flood means streaming is surging. A cool calm means email is idling. A flicker means something is about to break. The "save the internet" fantasy is felt the instant the player sees their network *flow back to life* after a crisis.

This spec proposes the visual identity that makes that fantasy felt, and that distinguishes Packet Plumber from its Mini Motorways baseline (packet personalities, era evolution, crisis juice, and a global internet map rather than a city's roads). **Status: approved via lavish review on 2026-08-07** ("go with your recommendations"); the resolved decisions are in the final section. Concrete hex values are given throughout so the look is buildable, not vibes.

**Tone alignment with the narrative spec** (`narrative-v1.md`, merged via PR #5): the look is **urgent-warm, never grimdark**. The light canvas is a *warm*, cheerful daytime (the Dispatcher's always-on ops center, watched 24/7, `[narrative §2.2]`), not cold tech or bleak dystopia. Saturated packet colors and subtle glow carry the personality; the relief of restored flow is the emotional payoff. The art serves the narrative's three voice layers visually (`narrative §2.3`): **L2 brand/system alerts lead as the on-screen alarm; L1 (the Dispatcher) is audio + on-screen caption; L3 UI chrome stays peripheral.** When all three fire, the eye goes to the alert tile first.

**Citation tags:** `[FORGE #n]` = sealed forge decision · `[GDD §x]` = GDD source · `[UX-DRn]` = UX decision record (from `sprints/stories-v1.md`) · `[ADR-n]` = architecture decision · data-catalog = `game/data/*.json` (the runtime single source, `[ADR-5]`).

---

## Amendment log

### Amendment 2026-08-08 - light-cascade + PR #9 render canon (A1-A7: light canvas · 6 literal buildings · round routers · bezier pipes · procedural map · topology rule)

The reference renders in PR #9 (`packet-plumber-blender-art`) are the visual north star; their decision trail is `../art-direction/art-direction-v1-amendments.md` (A1-A7) and the palette/recipe is `../art-renders/look-book-v1.md` (both PR #9). This amendment folds ALL of A1-A7 into the canon so `art-direction-v1.md` is the single comprehensive source. The look-book is the authoritative palette; tokens in §4-§7 mirror it. Cited for provenance (2026-08-08, user A/B verdict + render review).

**A1 — Canvas = LIGHT (Mini-Motorways daytime).** Warm cream land (`canvas #E8DDC2`) + soft-blue water + green parks, flat cheerful colour, minimal/no bloom. Supersedes the §1 dark lock, §4.1 dark palette, and the "internet at night" thesis; resolves the render-review amendment's "PENDING A/B." Dark retained as reference (`01a-vista-dark.png`). The glow/contrast principle is palette-agnostic: on light it reads as saturated packet colours + subtle glow, not bloom-on-black. (Folded into §1, §3, §4.1, §8.5, §9; narrative-v1 + forge #5 reconciled in their own amendments.)

**A2 — Terminals = 6 LITERAL BUILDINGS.** Residential (peaked-roof house) · content host (server/broadcast block) · gaming server (indigo + green sign) · financial hub (warm-stone bank + gold columns) · data center (big low block + rooftop units) · CDN cache (bay-door warehouse). Supersedes §6.2's abstract glowing shapes (and the render-review amendment's partial building reversal) — fully literal silhouettes; shape+icon accessibility (§5) preserved via distinct silhouettes + facade accents. (Folded into §6.2.)

**A3 — Routers = ROUND capacity-scaled hub PUCKS** (supersedes the render-review amendment's "switching-substation building" AND this spec's original abstract "octagon"). A circular disc + ring of indicator LEDs + glowing core — a distinct *shape family* from the rectilinear buildings, so a router is never mistaken for a destination (user: "the typical router icon is round"; colorblind-safe). Tier 1 basic hub → tier 2 switch (+ core) → tier 3 switch-fabric (double ring, larger). **Note:** this corrects an earlier draft of this very amendment that described routers as a rectilinear "chassis with ports" — the approved render form is ROUND. (Folded into §6.2, OQ-4.)

**A4 — Pipes = smooth BEZIER conduits** with rounded caps + a glowing inner **core** on fiber/backbone. Tier = width + colour + luminosity + core (the core lights up as you modernize). Refines §7.1; adopts the look-book's render-accurate pipe hexes. (Folded into §7.1.)

**A5 — Map background = canonical procedural land/ocean + parks**, MM-style, not a flat void (now implemented in the renders). (Folded into §3.3.)

**A6 — Topology rule:** terminals are leaves — every building connects to a ROUTER, never terminal-to-terminal; routers interconnect terminals and each other. No house↔house links. New rule refining `[GDD § M3]`. (Folded into §6.2.)

**A7 — Unchanged (rest of v1 stands):** blue streaming / grey email packet personalities (§2, §5) and warm-reserved-for-alarms (§2); the 9-type colorblind-safe shape+icon system (§5); pipe tiers copper→backbone (§7.1); 6 eras + the electrification arc (§9); the QoS-as-art flow readout (§5.3).

**Packet-shade adoption (user decision, expansion review):** streaming/email now use the look-book's render shades `#1E4A98` / `#5A6270` (adopted per user to match the approved renders) — supersedes v1 §2/§5's original `#3B82F6` / `#B8C0CE`. Concept unchanged (blue streaming / grey email, A7); only the exact shade moved to the render values. §4.3 state-triad contrast on the light base remains deferred to build-time tuning.

**Scope lock.** This amendment folds in A1-A7 (light canvas, 6 buildings, round routers, bezier pipes, procedural map, topology rule) plus the light-canvas adaptations of Error 404 (bleach-to-white, §8.5) and the era arc (saturation/density carries the electrification cue, §9). Packet-color concept, pipe-tier concept, 6 eras, colorblind-safety, and the warm/cool signal principle are unchanged and locked. The Dispatcher's voice/personality and satirical brands belong to narrative-v1 (reconciled separately).

### Amendment 2026-08-08 - render-review corrections (user override)

Two decisions from the Blender-art render review on 2026-08-08 correct the canon toward the user's intent. **Everything else in this spec is unchanged and remains locked.** Cited for provenance.

> **Two items below are superseded by the light-cascade amendment above: item 1 (router = substation building, now ROUND capacity-scaled hub puck) and item 2 (canvas palette PENDING, now FINALIZED light).**

**1. Nodes = LITERAL BUILDINGS (reverses "abstract nodes").** §6.2 and OQ-4 previously specified abstract glowing shapes (rounded-rect / hexagon / diamond / octagon) with a role icon. The user overrode this after reviewing the renders:

> "we need the buildings instead of boring shapes" · "it has to be beautiful art, not abstract shapes" · "we want to copy what we know works"

Nodes are now **literal buildings in the proven Mini Motorways aesthetic** (the place/building lessons already documented in §3.1) - little houses and destination buildings, representational and readable (residential = a little house; content host = a studio/server building; etc.; see the §6.2 table). The glow treatment and role icons carry over **within** the building forms: nodes are *lit buildings*, not bare shapes. ~~Junctions (routers) are literalized as switching-substation buildings~~ *(SUPERSEDED: routers are now ROUND capacity-scaled hub pucks — see §6.2 / Amendment A3).* Note: §5 packet shapes (circle / triangle / diamond / etc.) are a *different* system - the moving dots - and are **unchanged**.

**2. Canvas palette = PENDING a light/dark A/B render verdict.** The spec previously LOCKED the dark "internet at night" canvas (§1, OQ-6, the decision table). The user is on the fence about light vs dark and will decide visually from an A/B comparison (same scene, dark + light palettes) the Blender-art minion is rendering.

The palette choice is now **PENDING the A/B verdict** - neither light nor dark is locked. The dark draft's analysis (glow/contrast principle, warm/cool signal encoding, Error 404 flash-to-black) stands as the argument FOR dark and adapts to whichever palette wins. Dark is the current draft; light (MM-daytime) is the alternative under evaluation. Once the user picks, a follow-up amendment finalizes it.

**Scope lock.** Only (1) and (2) changed. Packet colors (streaming blue, email grey), pipe tiers/wear/pulse, the 6 eras, the identity thesis, colorblind-safety, and every other resolved decision are **unchanged and locked**. This amendment corrects toward user intent; it does not re-litigate the forge (Mini Motorways style stays; buildings ARE the MM building aesthetic).

---

## 1. Locked constraints (what this spec honors, never re-litigates)

| Constraint | Source | What it means for art |
|---|---|---|
| Mini Motorways clean-minimalist, 2D top-down | `[FORGE #5]` | Vector/canvas clarity; no clutter, no realism, no occlusion. Readable at a glance. |
| Canvas palette = **LIGHT (daytime)** (light-cascade amendment 2026-08-08) | `[GDD § Art Style]` | The play canvas is the **light, daytime Mini Motorways look** (clean, readable, cheerful), finalized per the A/B verdict. The dark "internet at night" alt is **retained as reference** (`01a-vista-dark.png`, §4.1). Gameplay encoding is palette-agnostic: saturated packet colors + subtle glow for emphasis; the loss-state on light is bleach-to-white/desaturate (§8.5). |
| Color is NEVER the sole encoder | `[UX-DR4]` `[GDD § Accessibility]` | Every packet type and node state carries **icon + shape** in addition to color. Palette toggles ship. |
| Colorblind-safe by design | `[GDD § Accessibility]` | Deuteranopia / Protanopia / Tritanopia palette toggles; shape/value/hue triads, never red-green-only encoding. |
| Cross-platform same-game, landscape | `[FORGE #6]` `[RULING]` | 1280x720 base is a coordinate reference only; `aspect=expand` reveals more map on wider/taller screens `[Arch §9.1]`. Readable on phone and monitor. |
| Renderer: `gl_compatibility` / OpenGL | `[project-context]` `[Arch §9.1]` | No heavy GPU particles or post-process bloom pipelines; glow is additive-blend sprites, gradients, and Line2D tricks. Must hold 60 fps on a 2021 mid-range phone. |
| Simulation is 20 Hz, rendered at 60 fps | `[Arch §9.1, ADR-2]` | Dot positions **interpolate** between the last two snapshots for smoothness. Juice is cosmetic on top of deterministic state. |
| No purchased assets before the playtest gate | `[project-context]` `[GDD § Asset]` | Prototype = placeholder art (colored rects + emoji + system shapes). This spec defines the **target** look AND a placeholder path that proves the concept. |
| Custom/owned art + Suno audio only | `[project-context]` `[GDD § Audio]` | Full-game art is custom (Blender-MCP orthographic pipeline). No stock; streamers monetize let's plays without flags. |
| Satirical brand names only | `[FORGE rejections]` | YouTune, Amazoom, Goggle, Glitch; Netflix/Discord kept. Never real trademarks. |
| No em-dashes in any copy | briefing global ban | Applies to all in-game strings and this doc. |

---

## 2. Color conflict resolved (designer's veto)

Three committed design docs agree: the brief addendum palette, the GDD M2 roster, and the narrative capsule (`narrative-v1 §5.4`) all specify **streaming = blue** and **email = white/grey**. The lone outlier is `game/data/packet_types.json` (email `#5B9BD5` blue, streaming `#FF7043` orange), and that file is currently **uncommitted** (only `game/data/.gitkeep` is tracked): a local working file owned by the prototype/data job, not a committed source of truth.

**Verdict (designer's veto; shades render-adopted per PR #9 / user): streaming = blue `#1E4A98`, email = grey `#5A6270`.** The earlier OQ-1 recommendation (catalog orange) is vetoed. The committed design consensus wins, and a stronger principle confirms it.

**The decisive principle: warm is reserved for danger.** Packet Plumber's primary alarm system is **amber (strain) + red (critical)**, on screen whenever anything nears failure. If the MVP's most ubiquitous traffic (streaming, the dominant flood) is ALSO orange/amber, then warm color is wallpaper, not a warning, and the alarm stops alarming. Keeping ambient traffic COOL (blue streaming, grey email, cyan IoT, lavender voice) and reserving WARM exclusively for attention (high-stakes packets like gold banking / tangerine multicast AND the crisis states) is what makes "something turned amber/red" actually mean something. This signal-to-noise argument outweighs the earlier "warm = high-volume" instinct.

Email = grey (not blue) for the same reason: grey is the neutral "background / fills-the-gaps" read a lowest-priority Best-effort class should have; blue reads as "primary/important," which contradicts email's role.

**Action:** this spec declares blue/grey canonical. The uncommitted catalog is a handoff item for the prototype/data job (Open follow-ups); this art-direction PR does not commit it (out of scope, owned elsewhere). *(Render-shade adoption, PR #9: streaming/email now use the look-book's render shades `#1E4A98` / `#5A6270` — adopted per user (expansion review) to match the approved renders; deeper than v1's original `#3B82F6` / `#B8C0CE` for contrast on the cream canvas. Concept unchanged.)*

---

## 3. The map: layout, geography & background texture

Addresses the lavish-review directive: a textured, place-evoking map, not a flat void. Grounded in what makes Mini Motorways' map work, adapted (not copied) to Packet Plumber's global-internet subject.

### 3.1 What worked for Mini Motorways (lessons we borrow)

Per the Dinosaur Polo Club GDC/design interviews (`Wuselfaktor` talk; GameDeveloper feature):

- **Sense of place.** MM's map is a stylized "novelty tourist map" with bright colours and a scale that highlights important roads/buildings. The player feels they are building *somewhere*. Geography (rivers, parks, coastline) is identity *and* a gentle constraint (a river needs a bridge).
- **Painted weighted spawn regions + procedural variability.** Designers paint weighted areas for house vs destination types, layered with procedural generation so each seed differs but plays well.
- **Neighborhoods.** Same-color houses cluster into neighborhoods, giving the map organic structure.
- **Tile-based construction.** The breakthrough was abandoning free-draw for a tile system: precision without fiddliness. (Packet Plumber already uses snap-to-node `[FORGE #2]`.)
- **The colorblind caution.** MM's own team noted that **terrain + a more detailed background made their colorblind mode harder**, and that **color + shapes + neutral background** (Mini Metro's approach) is the friendly formula.

### 3.2 What Packet Plumber adapts (differentiation, not copying)

The internet is **global**, not municipal. Packet Plumber cannot copy MM's city-road aesthetic, and the design is stronger for not trying:

| Mini Motorways | Packet Plumber |
|---|---|
| City roads, identical cars | Pipes carrying 9 distinct packet personalities |
| A single timeless city | The internet evolving across 6 eras on one growing map |
| Bright novelty-tourist palette | Light daytime canvas: vivid flow + subtle glow IS the priority signal |
| Rivers / parks as terrain | **Landmasses vs oceans**: the global internet's geography |
| Bridges cross rivers | **Undersea cables cross oceans** (the cable-cut crisis arena) |

The decisive hook: the brief addendum's **"undersea cable cut - entire continents isolated"** crisis archetype demands a map with land and water. Geography is not decoration; it is a gameplay surface and the "save the internet" fantasy made *spatial*. The player keeps *the world's* internet alive, not a city's roads.

### 3.3 The map treatment

- **A stylized light world/region map — now canonical & implemented** (PR #9 A5 renders; user: "a map background, just like in Mini Motorways"), not a flat void. The warm-cream `canvas` (`#E8DDC2`) base carries layered, **value-based (desaturated) texture** — procedural landmasses (coastlines/bays) + soft-blue ocean + **green park blobs**, MM-style. **All vivid hue is reserved for gameplay elements** (packets, node states, pipe tiers); terrain stays low-saturation so it never competes with the signal colors — the key lesson from MM's colorblind struggle, honored up front.
- **Land vs water + parks geography.** Landmasses (subtle topographic contour texture, a faint "city-tint speckle" where populations concentrate, and **green park blobs**) host terminal nodes and free pipe routing. **Oceans** render as a calmer, muted soft-blue (slightly cooler/desaturated than land, a very faint still-ripple) - the domain of undersea cables. Undersea cables are a distinct visual (thicker, cool vivid core, a subtle "submerged" desaturation) and are the arena for the severance / cable-cut crisis.
- **Region/district texture.** Faint topographic contour lines and a subtle region tint (value only) give each landmass identity without color. Residential neighborhoods cluster (MM's neighborhood lesson) as a soft warm city-tint glow; data-center districts pulse faintly; brand hubs (YouTune, Amazoom) carry their satirical brand glyph.
- **Layered depth** (back to front): (1) `canvas` (`#E8DDC2`) light field; (2) faint topology grid (the coordinate reference `[Arch §9.1]`, the snap lattice); (3) monochrome topographic/region texture; (4) city-tint speckle on populated land; (5) the gameplay layer (nodes, pipes, packets). Era 1 overlays a faint CRT scanline (ARPANET's "early terminal" personality); the scanline fades as eras advance and the city-tint speckle saturates - the map literally electrifies as the internet evolves (Section 9).
- **Procedural but curated.** Fresh seed per run `[GDD § Run]`; weighted spawn regions for node types (residential clusters, brand hubs, data-center districts) with procedural placement. Geography (coastlines, landmass shapes) is seeded so undersea-cable routes and the cable-cut crisis always have a spatial home.

### 3.4 Mini Motorways caution honored

MM's team explicitly noted terrain + a detailed background made colorblind encoding harder. Packet Plumber avoids the trap: terrain is **monochrome value texture only**, and the shape+icon system (Section 6) plus palette toggles (Section 11) carry all gameplay encoding. The map has a sense of place without ever using terrain hue as a signal.

---

## 4. Core palette

### 4.1 The canvas (the day)

The light/daytime canvas (PR #9 A1; finalized per the user's A/B verdict). The authoritative 2D palette + recipe is the **look-book** (`../art-renders/look-book-v1.md`, PR #9); tokens below mirror it. A warm, cheerful, **flat-colour** map — minimal/no bloom (the light render uses no compositor). Brightness is *not* the priority signal here (that was the dark-canvas argument); readability and approachability are. Crisp coloured lines on a cream map.

| Token | Hex | Use |
|---|---|---|
| `canvas` | `#E8DDC2` | Warm cream play surface (the map's land). |
| `grid` | `#C2B694` | Subtle darker grid lines (the snap lattice / coordinate reference `[Arch §9.1]`). Toggled off in reduced-density / late-era sprawl if it adds noise. |
| `canvas-ocean` | soft blue *(derived — look-book §3 shows soft-blue water; exact hex tuned at build)* | The calm water undersea cables cross. Slightly cooler/desaturated than the cream land; very faint still-ripple. |
| `canvas-wash` | near-white *(derived loss-state)* | Reserved for the **Error 404** loss state (the vivid play field bleaches out / desaturates, §8.5) and full-screen crisis washes. Never the play canvas. |

The canvas is the cheerful, readable Mini Motorways daytime field. On a light, low-saturation ground, *every vivid thing matters* — saturation and motion become priority. This is Brush's color-theory lens applied as a gameplay signal; the glow/contrast principle is palette-agnostic.

**Dark alt (retained as reference).** The dark "internet at night" canvas from the original draft is retained as a reference alternative (`01a-vista-dark.png`, rendered in PR #9), should light ever need re-evaluating. Its tokens, for reference only (NOT the current palette):

| Token | Hex | Use (dark alt — reference only) |
|---|---|---|
| `canvas-void` | `#000000` | Pure black. Reserved for the Error 404 loss state and full-screen crisis fades. |
| `canvas-base` | `#0E1320` | Deep blue-black. The base play surface (land). |
| `canvas-ocean` | `#0A0E1A` | Slightly deeper than land. The ocean void. |
| `canvas-lift` | `#161D2E` | Lifted navy. Radial vignette. |

### 4.2 Neutral chrome (UI/HUD surfaces)

Ink values per the look-book (PR #9); chrome-panel/border are derived (HUD surfaces not pinned there — tune at build).

| Token | Hex | Use |
|---|---|---|
| `chrome-panel` | warm-white ~88% alpha *(derived)* | Translucent panels for the HUD (health meter, forecast, popovers). Let the map read through them; never opaque blocks. |
| `chrome-border` | `#C2B694` *(derived, matches grid)* | Hairline borders on panels, dividers. |
| `ink-bright` | `#33414F` | Primary text/labels on light (look-book `ink`). |
| `ink-soft` | `#6A7078` | Secondary text, captions, inactive labels (look-book `ink-faint`). |
| `ink-faint` | `#9AA0A8` | Tertiary: countdown numerals at rest, placeholder copy (derived). |

### 4.3 The semantic state triad (health, warning, critical)

These three are reused across node health, pipe pressure, SLA gauges, and crisis alerts. They are the single most-sighted colors in the game, so they are tuned for maximum separation in both hue **and** lightness (colorblind safety), and they always pair with an icon/outline (`[UX-DR4]`).

| Token | Hex | Lightness | Meaning | Paired icon |
|---|---|---|---|---|
| `state-healthy` | `#37D67A` (spring green) | ~72% | Healthy / within SLA / good uptime | steady ring, check glyph |
| `state-strain` | `#F2B544` (amber) | ~58% | Approaching capacity (node strain >= 70% `[balance.json]`) | pulsing ring, `!` glyph |
| `state-critical` | `#E84545` (red) | ~47% | Imminent failure / critical (node strain >= 90% `[balance.json]`) | fast urgent pulse, `!!`/flame glyph |

Strain and critical differ by ~11 lightness points **and** hue (amber vs red), and by **pulse rate** (kinetic), so they are distinguishable even for protan/deutan viewers. The green-to-amber-to-red ramp is never the *only* encoder: every state also changes the node's ring pulse and its icon.

---

## 5. Packet-type identity system (the core differentiator)

Nine types, each learnable at a glance. **Color is never the sole encoder** (`[UX-DR4]`): each type carries a **shape**, an **icon**, a **size** (bandwidth), and a **motion signature** (latency/behavior). Color is the fast-recognizer; shape and icon are the durable distinguishers.

### 5.1 The roster

Ordered by era of introduction `[GDD § M2]`. Lane = the natural priority lane `[GDD § M2 QoS]`.

| # | Type | Color | Shape | Icon | Size (bandwidth) | Motion (latency tol) | Lane | Era |
|---|---|---|---|---|---|---|---|---|
| 1 | **Email / Browsing** | `#5A6270` cool grey *(render-adopted)* | small circle | `✉` | small | slow, drifts in gaps | Best-effort | 1 |
| 2 | **Web (rich media)** | `#B07A52` warm clay | rounded square | `🌐` | medium | steady | Standard | 2 |
| 3 | **Streaming** *(MVP)* | `#1E4A98` blue *(render-adopted; ambient river)* | large triangle | `▶` | **large** (flood) | steady torrent | Standard | 3 |
| 4 | **Gaming** | `#37D67A` spring green | diamond | `🎮` | small | **fast, zippy, bursty** (low latency, can't lag) | Express | 4 |
| 5 | **Banking / Secure** | `#F5C842` gold | hexagon | `🔒` | small | measured, never-stops (can't drop) | Express | 4 |
| 6 | **Voice / Video call** | `#9D7BE0` lavender | pill / capsule | `📞` | medium | low-latency, continuous | Standard | 4 |
| 7 | **Multicast / Broadcast** | `#FF9E3D` tangerine *(approved OQ-2)* | star (1-to-many fan) | `📡` | medium, fans outward | spreads to many sinks | Standard | 5 |
| 8 | **IoT / Telemetry** | `#36C5D8` cyan | tiny square | `📶` | **tiny, huge count** | trickle, high volume | Best-effort | 5 |
| 9 | **AI / adaptive** | `#F06292` rose-pink | morphing blob (self-shaping) | `🧠` | variable | **adaptive** (reshapes to spare capacity) | Best-effort | 6 |

**Why these shapes (the durable layer, colorblind-proof):** circle, rounded-square, triangle, diamond, hexagon, pill, star, tiny-square, blob are nine distinct silhouettes. Even with color removed entirely, a player can tell a streaming triangle from a gaming diamond from a banking hexagon. The icon is a second redundant channel. This is what makes the palette safe, not the hue choices alone.

**Why these colors (cool = ambient, warm = attention):**
- **Cool colors carry the ambient, ever-present flow** (blue streaming, grey email, cyan IoT, lavender voice). They breathe on the light canvas without competing for attention. Reserving cool for ambient traffic is what lets warm MEAN something.
- **Warm colors are the attention channel** for anything that matters in the moment: high-stakes packets (gold banking, tangerine multicast, clay web) AND the crisis states (amber strain, red critical). When something turns warm, the eye goes there.
- **Green** (gaming) and **rose** (AI) are accent hues for special behaviors (bursty / adaptive).
- This keeps the MVP's ubiquitous traffic (streaming) clearly OFF the crisis-color spectrum, so an amber/red node never fights an orange river for attention (the principle that vetoed the catalog's orange, Section 2).

### 5.2 The warm cluster and colorblind safety

Three types live in the warm band (multicast tangerine, banking gold, web clay), with gaming green adjacent; streaming is cool blue (Section 2), which both shrinks the warm cluster and removes the MVP's ubiquitous traffic from the crisis-color spectrum. For deuteran/protan viewers the warm band can still compress. The safety system, in priority order:

1. **Shape + icon carry the type** (above). Color is a bonus, not the key.
2. **Lightness separation inside the warm band:** clay (dark, ~42%), tangerine (mid, ~62%), red-orange (mid-bright, ~58%), gold (bright, ~70%). No two warm types share a lightness band.
3. **Palette toggles** (Section 11) remap the warm cluster for each vision type, pushing more lightness separation.
4. **Simulator-verified before lock** (Section 11): the warm cluster is the highest-risk set and gets explicit Deut/Protan/Tritan simulation as a defined sign-off step.

### 5.3 In-pipe visualization (the QoS-as-art readout)

Per `[GDD § M2]` and `[Arch §9.1]`, flow within a pipe renders **spatially — three painted
lanes per pipe, packets riding in their lane** (*user ruling 2026-08-12: Mini Motorways
cars-on-roads clarity; supersedes the proportion-only colored-dot stream*):

- **Lane position = lane allocation.** Each pipe paints **three lane strokes** (Express /
  Standard / Best-effort); every packet rides **in its lane** (lateral offset), so a pipe
  70% Standard shows a fat Standard lane with most packets in it. The player reads the
  *decision* spatially on the pipe. Proportion remains readable via lane-stroke width +
  per-lane packet counts, but position does the work.
- **Lane stroke weight = allocated share.** The three strokes' widths reflect the WFQ
  weights (3.2), so the dial's effect is visible as a geometry change.
- **Lane speed = priority.** Packets move **fastest on Express, slowest on Best-effort**
  (user ruling 2026-08-12): Express streaks, Standard cruises, Best-effort crawls and
  slips through the gaps. Motion is a per-lane readout, independent of per-type shape.
- **No auto-assignment.** Nothing moves off Standard until the player categorizes a type
  (per-type, or per-pipe override) — the default pipe shows all traffic riding the
  Standard lane, like a plain router.
- **Exit order = serialization.** At each node, dots exit Express, then Standard, then
  Best-effort, with lower-priority packets slipping through the gaps (work-conserving). The player reads the *consequence* at the node.
- **Dot speed = latency.** Express gaming diamonds streak; degraded email circles crawl.
- **Dot density = bandwidth.** A streaming flood is a dense orange river; a banking trickle is sparse gold.

This makes the QoS differentiator `[FORGE #4]` legible *without numbers*: the player sees who gets bandwidth and who waits by watching colored shapes move. That is the secret educational byproduct made visual `[FORGE #1]`.

---

## 6. Nodes: states and types

### 6.1 Node health (the primary warning surface, `[GDD § M3/M5]`)

A node glows its state color with a ring outline, plus an icon. The ring **pulses**, and the pulse rate is itself the escalation signal:

| State | Glow | Ring | Pulse | Icon | Trigger `[balance.json]` |
|---|---|---|---|---|---|
| Healthy | `state-healthy` green | steady solid ring | none (or slow ambient breathe) | check / role glyph | strain < 70% |
| Strained | `state-strain` amber | pulsing ring | slow, ~1.2 Hz | `!` | strain >= 70% (lead ~30s to failure) |
| Critical | `state-critical` red | fast urgent ring | fast, ~2.5 Hz | `!!` or flame | strain >= 90% (lead ~10s) |

Color + ring-pulse-rate + icon is a triple-redundant signal (colorblind-safe and reduced-motion-safe: with motion off, the icon and steady ring still carry the state).

### 6.2 Node types (terminals vs junctions)

Terminals (locations) and junctions (routers) are visually different *families*, so the player reads "who generates/receives" vs "where flows meet" instantly `[GDD § M3]`.

**Terminals** (sources/sinks): **6 literal building types** in the proven Mini Motorways tradition (PR #9 A2 — supersedes the old "abstract glowing shapes" entirely; see the MM place/building lessons in §3.1), each a distinct *silhouette* per role with the role icon set *within* the building. The glow treatment carries over: nodes are *lit buildings* (state-coloured glow + ring pulse around the building form), not bare shapes; the shape+icon accessibility system (§5) is preserved via distinct silhouettes + facade accents. Throughput reads as a faint size/glow scale. Varied cheerful body colours + darker roofs give a neighbourhood feel.

| Terminal | Building form (per look-book/PR #9) | Icon | Era |
|---|---|---|---|
| Residential | **peaked-roof house** (gable ridge to camera; varied cheerful body + dark roof, lit windows) | `🏠` | 1 |
| Content host (YouTune, Glitch) | **server/broadcast block** (brand-blue body/roof, e.g. `#3E78D0`) | `🎬` | 3 (MVP) |
| Gaming server | **indigo block + green gaming-sign** | `🎮` | 4 |
| Financial hub | **warm-stone bank with gold columns** | `🏦` | 4 |
| Data center | **big low block with rooftop units** (e.g. `#4E8AA0` body) | `🖥️` | 5 |
| CDN cache (reservoir) | **bay-door warehouse** with an inner reservoir-ring marker | `📦` | 5 |

*(Building/roof hexes — house bodies coral/gold/sage/sky, host, dc — are pinned in the look-book, `../art-renders/look-book-v1.md`, the authoritative palette source.)*

**Junction (router) = ROUND capacity-scaled hub puck** (PR #9 A3 — supersedes BOTH the original abstract "octagon" AND the render-review amendment's "switching-substation building"; also corrects this spec's earlier "chassis-with-ports" wording). Routers are **circular infrastructure pucks** — a **disc + a ring of indicator LEDs + a glowing core** — a deliberately different *shape family* from the rectilinear terminal buildings, so a router is never mistaken for a destination (user: "the typical router icon is round"; round beats a colour-only distinction, colorblind-safe). The puck **scales with capacity/tier** — tier 1 basic hub (ring of lights) → tier 2 switch (+ glowing core) → tier 3 switch-fabric (double light ring, larger) — paralleling the pipe-tier language (§7.1). Router state shows its LB mode in the LED ring: round-robin = evenly spaced lit LEDs; weighted-LB (smart) = proportional LEDs. This makes junction upgrades (a modernization decision, `[GDD § M3]`) visible at a glance — bigger disc, more LEDs, brighter core. Junctions also double as repeaters (reset pipe span budget), hinted with a small repeater glyph on long-haul links. (Router puck hex `#5E6E80` body / `#3E4A5C` roof / `#2E8B57` LEDs — look-book.)

**Topology rule (PR #9 A6 — refines `[GDD § M3]`):** terminals are **leaves**. Every house/building connects to a **router** (the round interconnect hub), never terminal-to-terminal; routers route between terminals and between each other. **No house↔house links** — the player draws house→router and router→router.

### 6.3 Brand tile identity (from `narrative-v1 §4.5`)
Content-host terminal nodes and crisis-alert tiles carry the satirical brand roster. Per the narrative's naming convention, **each brand has one icon + one color (never the name alone)**. The brand's color ties to its packet-type category, so a brand tile reads as its traffic class at a glance:

| Brand | Category | Icon | Category color |
|---|---|---|---|
| YouTune | streaming video | `▶` | `#1E4A98` blue |
| Glitch | live streaming | `▶` | `#1E4A98` blue |
| Netflix (kept) | streaming | `🎬` | `#1E4A98` blue |
| Goggle | web/search | `🌐` | `#B07A52` clay |
| Joypad | gaming | `🎮` | `#37D67A` green |
| Bankly | banking | `🏦` / `🔒` | `#F5C842` gold |
| Discord (kept) | voice/video | `📞` | `#9D7BE0` lavender |
| Amazoom Cloud | cloud | `☁` | `#6FA8DC` cloud accent |
| Smarthut | IoT | `📶` | `#36C5D8` cyan |
| Gabble | AI/adaptive | `🧠` | `#F06292` rose |

Brand glyphs on content-host nodes are larger and carry a subtle brand-tinted glow; alert tiles use the `⚠️ <BRAND>: <STATE>` format (`narrative §4.1.4`), color + glyph + caption, never color alone.

---

## 7. Pipes and flow (the "draw" feel)

The pipe is the player's primary creation. Drawing it must feel *good* (P1), and its tier must read at a glance (P4 modernization).

### 7.1 Tier language (width + material + luminosity)

Each tier is a distinct *material* rendered as a **smooth bezier conduit** (rounded joins/caps — Mini-Motorways road elegance; PR #9 A4) with a width, a colour, a luminosity, and — on fiber/backbone — a glowing inner **core**. As the player modernizes, the network literally brightens and crystallizes (the fiber/backbone core lights up); this is era-progression made visual `[FORGE #4]`. Tier = width + colour + luminosity + core. Hexes below are the render-accurate values from the look-book (`../art-renders/look-book-v1.md`, PR #9); v1's placeholder pipe hexes are superseded.

| Tier (era) | Color / material | Width | Surface | Read |
|---|---|---|---|---|
| **Narrow Copper** (1) | `#8E5E2E` copper, matte | thin | flat, slight grain | cheap, short-range, the baseline legacy |
| **Standard Line** (1) | `#78808C` cool steel | medium | subtle horizontal sheen | the workhorse |
| **Wide Fiber** (3, MVP) | `#2E5494` deep-blue + glowing inner core (`#7AA8E6`) | wide | glassy, lit core | premium, long-haul |
| **Backbone** (5, full game) | deep blue-white + bright core (`#AECBFF` core) | very wide | strong lit core | data-center scale, very long-haul |

An **unallocated** pipe (no lane set, or multi-class default) renders in a neutral luminous teal-grey `#3A4A5C`; once flow is assigned, the packet colors tint it. An **undersea cable** (Section 3) is a distinct thicker variant with a cool luminous core and a "submerged" desaturation.

### 7.2 The draw feel (juice)

- **Snap glow:** on snap-to-node (within `snap_radius` = 36 `[balance.json]`), the node flares and the pipe draws with a bright leading edge that settles to its tier color. A small haptic + a draw SFX (Brush: every input gets an answer).
- **Flow pulse:** once connected, a subtle traveling brightness moves along the pipe at the flow rate. *The internet is alive.* Pulse speed reads as latency.
- **Cost ghost:** while drawing, a faint cost tally follows the cursor (length x tier `[GDD § M1]`), so the budget pressure is felt in real time.

### 7.3 Wear, legacy, and failure (P4 + P5)

- **Legacy wear:** an in-service legacy pipe under new-era load loses saturation and gains a material-specific degrade overlay: copper gets verdigris `#3D7A6A`; steel gets rust pocks `#6B4A3A`. A pulsing amber `state-strain` halo flags impending failure on the same surface crises use `[GDD § M1]`.
- **Burst / leak (the crisis juice):** a failed pipe spews its packet color as a fountain-spray of dots (e.g., blue streaming packets arcing out across the map), pressure drops, the pipe edge fractures. This is the signature "uh oh" moment.
- **Severance / cable cut:** a cut link goes flat/desaturated (drops toward `canvas-wash`), packets that were en route scatter/bounce. The missing link reads as a gap. On an undersea cable, continents on the far side visibly desaturate/fade - the "continents isolated" fantasy beat.

---

## 8. UI / HUD chrome

The map IS the UI (`[UX-DR1]`): near-zero chrome, all state on the elements. The HUD only adds what the map cannot show at scale.

### 8.1 Inherited from Mini Motorways (the foundation)
- State read from the flow (Wuselfaktor): congestion = dots piling; lane allocation = dot color proportion; node health = glow; degradation = the wear indicator.
- Camera pan + zoom (drag/scroll, pinch) is the primary navigation for a growing map.
- Pause-to-plan; color + icon + glow coding throughout. **Paused presentation** (*user ruling 2026-08-14, prototype-aligned*): the paused world stays at **full brightness — no dim veil, no centered label**; the paused state is a **small edge chip** ("PAUSED — P/Space to resume", sized + styled like the other HUD chips) at a screen edge, never over the play area.

### 8.2 The HUD elements (what the map cannot show)

| Element | Where | What it shows | Reads without color? |
|---|---|---|---|
| **Network Health meter** (the loss mechanic) | top-center bar | aggregate internet health; drains red on breach, recharges green on recovery; empty = Error 404 | yes: bar length + the `ERROR 404` mono lockup |
| **SLA chips** (per active class) | top row, small | one chip per active packet type: its uptime as a mini green/amber/red bar + the type icon + % | yes: % numeral + icon |
| **Demand forecast ("weather report")** | bottom or right panel | active demand + incoming SetPieces (the surge) with countdowns; affected demand highlighted `[GDD § M5]` | yes: countdown numerals + icons `[UX-DR5]` |
| **Era indicator** | top-corner timeline | current era stamp + a mini era-evolution ribbon (Section 9) | yes: era name + ordinal |
| **Crisis alerts** | toast, top | satirical brand copy ("⚠️ YOU_TUNE: DOWN - 2.3B users affected"); clickable to pan-to-problem `[UX-DR3]` | yes: captioned `[UX-DR5]`; all audio alerts also captioned on screen |
| **Budget tally** | top-corner | remaining draw/upgrade budget (MVP action cap; full-game currency) | yes: numeral |
| **Minimap** (late era) | corner | overview of sprawling ~20-30 node maps; click-to-jump `[GDD § UI]` | n/a |

### 8.3 Contextual controls (progressive disclosure, `[UX-DR1]`)
Selecting a pipe or node opens a **contextual popover/radial** near it (Mini Motorways' upgrade-radial model): upgrade tier, allocate lane weights (the single "priority emphasis" dial in MVP; full WFQ in full game), set junction policy, designate a lane. The default view stays a clean topology. Same interaction everywhere, input-agnostic (touch/mouse/controller).

### 8.4 Filter / focus modes (essential at 9 types, `[UX-DR2]`)
Toggles that isolate a view: "only strained/critical nodes," "only Express lanes," "highlight one packet type's flow," "only degrading/legacy pipes." These are the density management for 9-type maps and double as low-vision aids.

### 8.5 The Error 404 loss lockup (aligned with `narrative-v1 §3.4`)
When the Network Health meter empties, the loss beat is the internet going down: **flowing dots freeze and fade, every brand tile flips to DOWN, gauges flatline, the canvas bleaches out to `canvas-wash` warm white (color desaturates and washes flat)**, a crisp mono `ERROR 404` centers, and the soundtrack drops to a single low tone under the Dispatcher's non-punitive last transmission ("Network's gone down... it happens, engineer... pull it back together") shown as a caption. Retry prompt follows; the map resets to a fresh seed. This is the emotional inverse of the vivid play field, by design, and never a scolding game-over (`[FORGE #3]`).

---

## 9. Era visual evolution (the internet grows, `[FORGE #4]` P4)

The six eras must *feel* different. The progression cue is a rising arc of **color saturation and density** — the electrification arc: the map literally gets richer, denser, and more complex as the internet evolves (starting near-monochrome in Era 1 and saturating through Era 6). Era-advance is a fanfare + a visual "evolution" wipe that seeds the new era's signature elements.

| Era | Palette mood | Density | Signature visual | Feels like |
|---|---|---|---|---|
| **1 Foundations (ARPANET)** | muted, near-monochrome cool; dim narrow copper only | very sparse, few nodes | faint CRT scanline texture over the canvas; small map | 1969, a quiet experiment |
| **2 Email & Web** | cool with creeping warmth; standard steel appears | calm, growing | clean efficient topology, the "build cleanly" era | early web, satisfying order |
| **3 Streaming Surge** *(MVP ends here)* | blue flood; wide fiber glows hot | rising, urgent | streaming blue dominates; a swelling blue wave, nodes straining amber to red as the surge hits | the internet gets loud |
| **4 Real-Time** | full multi-color; Express lanes glow brightest | high, triage-intense | green gaming + gold banking + lavender voice all flowing in dedicated lanes | always-on, multi-priority |
| **5 Cloud Era** | dense neon city-grid | massive sprawl (~20-30 nodes) | data-center hexes + CDN reservoir rings; multicast stars fan out; IoT cyan specks like a sensor cloud | the city of light, fully realized |
| **6 Software-Defined Edge** | cleaner, abstracted overlay layer | dense base + translucent overlay | dashed translucent secure-tunnel overlays; flow paths shimmer/reshuffle (programmable reroute); AI rose blobs self-shape to spare capacity | the future: software over hardware |

The metaphor boundary (`[GDD § M4]`) is honored visually: eras 1-4 are literal glowing-plumbing; era 5 adds the reservoir ring abstraction; era 6 layers clean *overlays* (dashed translucent conduits, shimmering reroutes) rather than faking literal SDN hardware. The city-tint speckle on landmasses saturates across the arc, so the world map electrifies as the internet evolves. This visual arc serves the narrative's emotional arc (`narrative-v1 §3.2-3.3`): the internet as a character *growing up* (born, gets a job, learns to binge, stops sleeping, eats the world, thinks for itself). Era 6's abstracted rose-pink overlay is where the internet "starts having opinions" and, per the narrative's optional hand-off, gains its own voice.

---

## 10. Juice and feedback (Thomas Brush, six lenses)

"Every input gets an answer. Every pixel reacts." Mapped to Packet Plumber:

| Brush lens | Packet Plumber application |
|---|---|
| **Measurement** | Tile/grid sized to the playfield; generous snap radius (36 `[balance.json]`); packet sizes and densities tuned to read instantly; gauge thresholds pinned (70/90 `[balance.json]`). |
| **Color theory** | Light, low-saturation canvas + saturated packet colors + subtle glow; saturation and motion encode priority; the palette IS the gameplay signal (Sections 4-5). |
| **Reactive sound** | Pipe-draw, packet-arrival (per-class variants, 3-4 each), leak-patch, junction-cool, era-transition fanfare, and the signature "YOU_TUNE: DOWN" crisis sting. Never ship silence. |
| **Animation curves** | Gravity-shaped easings: packet-arrival ease-out bounce; leak-spray ease-out burst; gauge recovery ease-in-out; crisis flash quick-in/slow-out. Avoid flat linear motion. |
| **Reactive particles** | Leak spray (packets fountaining from a burst pipe), router-overheat sparks, "surge survived" celebration burst, era-advance confetti in the new type's color. |
| **Music & ambience** | Suno ambient beds between crises, pressure-riser stings as warnings climb, alert stings on crisis trigger, resolution cues on flow-restore. Mood-driven by sim state `[Arch §9.6]`. |

**Signature moments:**
- **Draw-and-snap:** the leading-edge flare on snap is the core satisfaction beat (P1).
- **Surge survived:** the wave recedes, gauges swing green, a celebration burst, the relief sting. The fantasy payoff, every cycle.
- **Era advance:** the evolution wipe seeds the new era's signature; a fanfare; the map saturates a tier.
- **Cable cut:** continents on the far side of a severed undersea cable visibly desaturate. The global scale of the stakes, made visual.
- **Error 404:** the bleach-to-white loss lockup. The negative space that makes the vivid flow mean something.

---

## 11. Accessibility

| Need | Solution |
|---|---|
| **Colorblind-safe** (`[GDD § Accessibility]`, `[UX-DR4]`) | Color never sole: type = shape + icon; node state = ring pulse + icon. Ship **Deuteranopia / Protanopia / Tritanopia palette toggles** that remap the warm cluster for more lightness separation. Warm cluster is simulator-verified before lock (Section 5.2). Terrain is monochrome value texture only (Section 3), so the map's sense of place never adds colorblind load - the Mini Motorways caution, honored. |
| **Reduced motion** (`[UX-DR5]`) | Disable screen-edge flash and screen shake; ALL animation freezes to a static state (flow-pulse steadies, the AI morphing blob holds a fixed silhouette, era-advance confetti is suppressed); crises remain readable via gauges + icons + audio. |
| **Pause anytime** (`[GDD]`) | No real-time-pressure-only design; the player can always stop to think (core to the fair-crisis model). |
| **Scaling** (`[GDD § Accessibility]`) | UI/gauge scaling for small screens and low vision; readable at a glance on phone and monitor. |
| **Input parity** (`[FORGE #6]`) | Full touch / mouse / controller parity; no input-dependent mechanics. |
| **Captions** (`[UX-DR5]`) | All audio alerts captioned on screen; the forecast panel is readable without color. |
| **Contrast** | All text/chrome meets WCAG AA against the light canvas (`ink-bright` `#33414F` on `chrome-panel` is ~10:1, AAA). |

Filter/focus modes (Section 8.4) double as low-vision aids: isolate one type, highlight only strained nodes. **Palette toggles are global:** when a colorblind remap shifts a packet-category color, the matching brand tiles (Section 6.3), node glows, and SLA chips all follow, so the type-to-color mapping stays consistent everywhere.

---

## 12. Rendering notes (Godot 4.7 / `gl_compatibility`)

Implementation hints for the build minion, honoring `[Arch §9.1]` and `[project-context]` engine traps. Not prescriptive, just feasible within the renderer budget:

- **Pipes:** `Line2D` with per-segment width for tier; an additive-blend underlay sprite for the glow halo (cheap fake bloom that works in `gl_compatibility`). The flow pulse = an animated texture/sprite traveling the path, or a per-vertex color shimmer. Undersea cables = wider Line2D, cooler core, lower saturation.
- **Packet dots:** pooled `PacketDot` nodes (color = type; shape = a simple polygon/sprite per type; `[Arch §9.1]` pools them). Interpolate position between the last two 20 Hz snapshots for 60 fps smoothness.
- **Glow:** prefer additive sprites and radial-gradient textures over GPU particle systems; keep draw calls low for the phone budget.
- **Node glow/pulse:** an animated sprite or a shader-less ring (`draw_arc`) whose alpha/scale pulses on a timer; the pulse rate is data-driven from health state.
- **Map texture:** the layered land/ocean/topographic texture is a static (or slowly animated) background - a pre-rendered texture per seed, NOT per-frame procedural work, so it costs negligible GPU. City-tint speckle can be a noise texture modulated by population density.
- **FinLT traps honored:** themes handed explicitly to popups across CanvasLayers; deferred-frame sizing via `await resized`; `@onready`/`%UniqueName` refs; int re-cast after any JSON load.

---

## 13. Placeholder to target art path

| Phase | Art | Why |
|---|---|---|
| **Prototype (fun-test, MVP)** | Placeholder: colored rects for nodes, `Line2D` for pipes, emoji + simple polygons for packet shapes, system fonts. The map geography = a flat light texture with a drawn landmass/ocean mask (no custom art). Just enough juice (colored dots, leak spray, crisis alert) to prove the *concept*, not the polish `[GDD § Asset]`. | Single-polished-launch doctrine; prototype is reference, not shippable. |
| **Full game (post-playtest)** | Custom owned art via the Blender-MCP orthographic-render pipeline `[GDD § Asset]`: every asset shares one art bible (this palette, line weight, material treatment, lighting) so homogeneity comes from the bible, not the tool. The landmass/ocean/topographic map art is custom-rendered per the art bible. | Premium "save the internet" feel; no purchased/licensed art (matches the Suno ownership doctrine). |

The palette, shape/icon system, and map treatment in this spec are **identical for both phases**: the prototype proves them in placeholder form; the full game realizes them in custom art. The visual identity does not change between phases, only its fidelity.

---

## Resolved decisions (lavish review, 2026-08-07)

User verdict: **"go with your recommendations."** All open questions resolved as proposed:

| Ref | Decision | Rationale |
|---|---|---|
| **OQ-1 (vetoed; shades render-adopted per PR #9)** | **Streaming = blue `#1E4A98`, email = grey `#5A6270`** (the 3 committed design docs' consensus; the lone uncommitted catalog overridden; shades adopted from the look-book renders). | Warm must be reserved for the amber/red crisis alarm so it stays a signal, not wallpaper; ambient traffic stays cool. The earlier "catalog orange" rec is vetoed (Section 2). |
| **OQ-2** | **Multicast = warm tangerine `#FF9E3D` + star shape.** | Stays warm (the attention channel); with streaming now cool blue (Section 2), multicast is separated from streaming by hue family (warm vs cool) + the 1-to-many star silhouette. |
| **OQ-3** | **CRT scanlines (Era 1) + faint topology grid throughout.** | Era-1 personality without overdoing retro; the grid is the snap lattice. |
| **OQ-4** (reversed to buildings, Amendment 2026-08-08; router superseded to ROUND puck by A3) | **6 distinct literal buildings per terminal role** (peaked-roof house / server-broadcast block / indigo gaming block / warm-stone bank / big low data-center block / bay-door warehouse); **junction = ROUND capacity-scaled hub puck** (disc + LED ring + glowing core, not a building). | Maximum readability of "who generates / who receives"; the building silhouette carries terminal role (MM building aesthetic, §3.1); the round puck reads as through-infrastructure scaled by capacity — a different *shape family* so it's never mistaken for a destination. Reverses the earlier abstract-shape decision; supersedes "substation building" (A3). |
| **OQ-5** (adapted to light, light-cascade amendment) | **Error 404 bleach-to-white + mono lockup** (dark draft was flash-to-black). | The emotional inverse that makes the vivid flow mean something. |
| **OQ-6** (FINALIZED light, light-cascade amendment 2026-08-08) | **Canvas palette = LIGHT (daytime Mini Motorways)** per the A/B verdict; dark alt retained as reference (`01a-vista-dark.png`). | The A/B renders decided it from visuals: the light canvas reads as cheerful, clean, and keeps the vivid-flow-is-the-signal principle (warm/cool encoding + subtle glow) without bloom-on-black. The dark draft's analysis (glow/contrast, warm/cool, Error 404 inverse) carried over and adapted to light. |
| **MAP** | **Textured global map with landmasses vs oceans (undersea cables); monochrome value-texture terrain only.** | Borrows MM's sense of place and weighted-region spawning; differentiates via the internet's global geography and the cable-cut crisis; honors MM's colorblind caution by keeping terrain desaturated. |

| Decision | Rationale | Rejected alternative |
|---|---|---|
| Canvas palette: **LIGHT (daytime)** (light-cascade amendment 2026-08-08) | The A/B verdict (PR #9) chose light: vivid flow + subtle glow is the priority signal on a cheerful, readable daytime field; Error 404 = bleach-to-white is the emotional inverse. The dark "internet at night" alt is retained as reference, not rejected outright. | The user decided from the A/B renders; light is locked. (The earlier "dark drafted, light under evaluation" and the original "dark decided, light rejected" are both overturned.) |
| Nine distinct shapes + icons (color is fast-recognizer, not the key) | `[UX-DR4]` locked; colorblind safety cannot rest on hue alone, especially the warm cluster | Color-only encoding (fails colorblind safety; rejected by lock) |
| Pipe tier = material + width + luminosity (copper -> steel -> fiber -> backbone) | Modernization becomes visible (P4); the network brightens as you upgrade | Width-only tiers (loses the era-progression read) |
| Era evolution = rising saturation/density arc (light-canvas adapted) | The internet's growth is *felt* as the map getting richer and denser, not just content gating | Static look across eras (kills the differentiator) |
| Cool = ambient traffic, warm = attention (crisis + high-stakes) | Reserves warm for the alarm system so amber/red always means danger; keeps ubiquitous streaming off the crisis spectrum | Warm=load / cool=fill-gaps (made ambient streaming orange, colliding with crisis amber/red) |
| Global land/ocean map with undersea cables | The "save the internet" fantasy is global; the cable-cut crisis needs a spatial home; differentiates from MM's municipal map | Flat abstract grid (no sense of place, weaker fantasy) |

## Open follow-ups (not blocking this spec)

- **Streaming color (decided by designer's veto; shades render-adopted):** streaming = blue `#1E4A98`, email = grey `#5A6270`, matching the 3 committed design docs and reserving warm for the crisis alarm; exact shades adopted from the look-book (PR #9) to match the approved renders. The lone outlier is the local `game/data/packet_types.json`, which is currently **uncommitted** (not tracked in git; only `.gitkeep` is) and owned by the prototype/data job. **Handoff:** that job should set the catalog colors to match this spec. This PR does not commit the catalog (out of scope; owned elsewhere).
- **Blender-MCP reference render (recommended next artifact):** a single orthographic render of the proposed look (light textured world map, vivid pipes, packet shapes, an undersea cable, a mid-surge crisis) to anchor the direction before full-game asset production. The dark alt (`01a-vista-dark.png`, PR #9) already exists as the comparison reference. The Blender MCP is available; offered as an immediate follow-up to this spec, troubleshooting together if the pipeline needs it.
- **Doc-debt (minor after the veto):** the GDD roster and narrative capsule are already consistent with this spec (blue streaming); only the uncommitted catalog drifts (handoff above). The narrative notes the GDD uses 173 em-dashes with no CI guard; an em-dash CI lint is a separate hardening task.
- **Capsule/trailer art:** the narrative's capsule art direction (`§5.4`) locks the concept (top-down city map by day, vivid pipes, leak fountain, red-lit router, the coffee-carrying engineer hero, the YOU_TUNE DOWN alert tile). This art-direction spec is its visual foundation, and the capsule's blue-streaming is consistent with the locked palette. Full capsule art is cut from prototype footage later via the Blender pipeline.

## Out of scope (this spec)

- The V2 AI stress-test system's visuals (full-game, `[GDD § M5]`).
- Exact Suno track briefs (audio direction is `[GDD § Audio]`; this spec touches SFX only for juice mapping).
- Concrete phone perf/memory budgets (named at prototype time, `[GDD open Q3]`).

---

*Status: approved (lavish review 2026-08-07). The companion review surface lived at `.lavish/art-direction-v1.html` (gitignored, ephemeral). This file is committed and a PR opens targeting `main`; the human reviews and merges.*
