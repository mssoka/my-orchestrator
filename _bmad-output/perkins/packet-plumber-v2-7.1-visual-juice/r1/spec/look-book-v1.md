# Packet Plumber — Look-Book v1 (reference-render aesthetic recipe)

> **Status:** reference renders for the visual identity. **Canvas verdict (user, via lavish A/B 2026-08-08): LIGHT — Mini-Motorways daytime.** This amends art-direction #7's "dark internet at night" (Gru tracks the doc). The dark variant is retained in `renders/01a-vista-dark.png` as the considered alternative.
>
> **Two further canon refinements this look-book records (user-directed):**
> 1. **Literal buildings, not abstract shapes** — terminals are little MM-style buildings (house / content host / data center).
> 2. **Routers are capacity-scaled ROUND infrastructure** — a circular hub/patch **puck** (a distinct *shape* family from the rectilinear buildings; the canonical round router icon) that scales with tier.
>
> Everything else in the canon is unchanged: blue streaming / grey email packet personalities, pipes with a pulse, 6 eras, the identity thesis.

These renders are the visual **north star** for the 2D top-down Godot implementation. They establish the look (mood, materials, lighting, the flowing-packet aesthetic); the exact hexes below are the 2D target.

---

## 1. The reference renders (what each shows)

| File | Moment | What it anchors |
|---|---|---|
| `renders/01b-vista-light.png` | **The vista** (hero mood) | A living daytime network on a procedural **land/ocean map** (coastlines, parks): peaked-roof houses + a content host + a data center + **round disc routers**, joined by smooth tiered pipes. **Houses connect to routers, never house-to-house.** THE mood shot. |
| `renders/02-packet-flow.png` | **Packet flow** | Blue streaming triangles vs grey email circles, **visibly distinct** (the prototype's failure mode, done right). |
| `renders/03-node-identity.png` | **Node identity** | The 4 node families — Residential (house), Content host, Data center, Router — + the healthy/strained/critical state triad. |
| `renders/04-pipes-tiers.png` | **Pipes by tier** | Copper → steel → fiber → backbone: smooth bezier conduits, width + material + luminosity scale up; fiber/backbone carry a glowing inner **core** (the network brightens as you modernize). |
| `renders/05-crisis.png` | **Crisis moment** | A strained→critical node, a severed cable (the cut gap + scattering packets), the signature `! YOU_TUNE: DOWN. 2.3B users affected.` alarm. Warm colour reserved for danger. |
| `renders/06-router-variants.png` | **Router capacity tiers** | Round hub **pucks** scaling tier 1 basic hub (ring of lights) → tier 2 switch (+ glowing core) → tier 3 switch-fabric (double light ring, larger). A different SHAPE family from the buildings; capacity scales like the pipes. |
| `renders/07-terminals.png` | **Terminal roster** | The full **6 building types**: residential (house), content host, gaming server, financial hub, data center, CDN cache — each a distinct literal silhouette. |
| `renders/01a-vista-dark.png` | *(alternative — not chosen)* | The dark "internet at night" variant from the A/B. Retained for reference. |

---

## 2. The chosen palette — LIGHT (Mini-Motorways daytime)

A warm, cheerful, flat-colour map. Brightness is **not** the priority signal here (that was the dark-canvas argument); readability and approachability are. Crisp coloured lines on a cream map; minimal/no bloom.

| Token | Hex | Use |
|---|---|---|
| `canvas` | `#E8DDC2` | Warm cream play surface (the map). |
| `grid` | `#C2B694` | Subtle darker grid lines (the snap lattice). |
| `ink` (labels) | `#33414F` | Primary label/caption text. |
| `ink-faint` | `#6A7078` | Secondary text. |
| **house bodies** (varied, cheerful) | `#E85A4A` `#F2C94C` `#5ECB6B` `#4A9BE2` | Coral / gold / sage / sky — a neighbourhood of varied homes. |
| **house roofs** (darker complement) | `#7A2E26` `#7A5418` `#2C6A34` `#26507E` | Dark warm/cool roofs for silhouette contrast. |
| `host` (content-host body/roof) | `#3E78D0` / `#264C8E` | The "server/broadcast" building (brand-blue). |
| `dc` (data-center body/roof) | `#4E8AA0` / `#2E5E70` | The big low cloud building. |
| `router` (puck) | `#5E6E80` / `#3E4A5C` | Neutral hardware grey — a ROUND disc hub (infrastructure, not a place). |
| `router-tip` (LEDs) | `#2E8B57` | Ring of indicator LEDs (active/healthy). |
| `pipe_core` | LIGHT `#7AA8E6` / DARK `#AECBFF` | Lighter tint glowing inside fiber/backbone conduits. |
| **pipes** | copper `#8E5E2E` · steel `#78808C` · fiber `#2E5494` | Crisp coloured conduits; darker than the canvas so they read. |
| **packets** | streaming `#1E4A98` (blue) · email `#5A6270` (grey) | Distinct at a glance. |
| **state triad** | healthy `#37D67A` · strained `#F2B544` · critical `#E84545` | Reused for node health + alarms. **Warm (amber/red) is reserved for danger.** |

> **Packet-type roster (9, era-ordered):** email (grey, small circle) · web (clay, rounded square) · streaming (blue, large triangle) · gaming (green, diamond) · banking (gold, hexagon) · voice (lavender, pill) · multicast (tangerine, star) · IoT (cyan, tiny square) · AI (rose, blob). **Color is never the sole encoder** — each has a distinct shape + icon (colorblind-safe).

---

## 3. The 3D → 2D recipe (how the Godot build reproduces this)

The renders are **orthographic 3D** (Eevee) at a gentle ~35° tilt; the Godot game is **2D top-down**. The look transfers as follows:

- **Buildings** → 2D sprites/icons for the **6 terminal types**: peaked-roof house (residential), flat server block (content host), indigo + green-sign block (gaming server), warm-stone + gold-columns bank (financial hub), big low block (data center), bay-door warehouse (CDN cache). Each a distinct literal silhouette; varied cheerful body + dark roof.
- **Routers** → a **ROUND disc/hub sprite** (a puck with a ring of indicator LEDs + optional glowing center); a **3-tier sprite set** (bigger disc + more LEDs + glowing core + double ring at higher tier) so capacity reads at a glance. Round = a different *shape* family from the rectilinear buildings, so a router is never mistaken for a destination.
- **Pipes** → smooth curved `Line2D` (bezier, rounded joins/caps — Mini-Motorways road elegance); per-tier width + colour. Fiber/backbone carry a brighter inner **core** line (a lit conduit). Tier = width + colour + brightness (copper thin/dim → backbone wide/bright + core).
- **Packets** → pooled dot sprites; **shape per type** (triangle/circle/diamond/…), **colour per type**, size = bandwidth. Interpolate position between 20 Hz sim snapshots for 60 fps smoothness.
- **Node state** → ring/outline colour (green/amber/red) + **pulse rate** (slow strain, fast critical) + an icon — triple-redundant, colorblind-safe.
- **Canvas / map** → a procedural **land/ocean map** (noise-driven landmasses with coastlines + green park blobs over soft-blue water), MM-style — not a flat void. Diagram shots (pipe tiers, packet flow) keep a flat gridded canvas for label clarity.
- **Topology** → terminals are **leaves**: every house/building connects to a **router** (the round interconnect hub), never terminal-to-terminal. Routers route between terminals and between each other.

---

## 4. Render pipeline (Blender 5.2 LTS / Eevee) — for reproducibility

- **Engine:** Eevee, **Standard** color management (keeps chroma faithful; AgX desaturates bright hues to white).
- **Glow (dark variant only):** compositor **Bloom** via the 5.x node-group API (`CompositorNodeTree` + `NodeGroupOutput` + an interface `Image` socket). The light/daytime look uses **no compositor** (`compositing_node_group = None`) — flat vector colours, MM-style.
- **Materials:** pure emissive (no lights) — gives flat, controllable colour. Tuned source hexes slightly deeper than the 2D-target hexes where bloom would otherwise wash them.
- **Buildings:** low-poly primitives (cube body + bmesh **gable roof** with ridge along Y so the triangular peak faces the camera + emissive window quads).
- **Source:** `blend-sources/pp_lib.py` (parametric scene builder — palette-driven; rebuild any shot with `build_<shot>(LIGHT)` / `build_<shot>(DARK)`). `.blend` snapshot in `blend-sources/`.

---

## 5. Decisions & rationale (provenance — so a fresh minion/reviewer can take over cold)

| # | Decision | Rests on | Rejected alternative |
|---|---|---|---|
| D1 | **LIGHT (MM-daytime) canvas** | User verdict via lavish A/B 2026-08-08 ("copy what works") | Dark "internet at night" (art-direction #7's locked thesis — now amended; dark retained as alternative) |
| D2 | **Literal buildings** for terminals (house / content host / data center) | User: "beautiful art, not abstract shapes" | Abstract glowing geometric nodes (art-direction #7 §6 — reversed) |
| D3 | **Routers = ROUND capacity-scaled hub pucks** (disc + light ring + glowing core; tier 1→3), a distinct SHAPE family from buildings | User: "the typical router icon is round"; round beats a colour-only distinction (colorblind-safe) | Rectangular chassis; router-as-building; abstract octagon |
| D8 | **Pipes = smooth bezier conduits** with rounded caps + a glowing inner **core** on fiber/backbone | User: pipes "minimalistic but elegant and beautiful"; Mini-Motorways road elegance (smooth curves, seamless joins) | Flat chunky rectangular ribbons ("plain") |
| D9 | **Map background** (procedural land + ocean + parks), not a blank canvas | User: "a map background, just like Mini Motorways"; art-direction #7 §3 | Flat solid-colour void |
| D10 | **6 literal terminal building types** (residential / content host / gaming server / financial hub / data center / CDN cache) | User: "do we need more building types?" + canon §6.2 roster | Only 3 (residential/content/data-center) |
| D11 | **Terminals connect via routers; never house-to-house** (houses are leaves; routers are the interconnect) | User: "houses shouldn't connect to each other - they should connect to routers" | House-to-house links (Cu spurs) |
| D4 | **Blue streaming / grey email** packets, shape+colour distinct | art-direction #7 §2 (designer's veto); fixes the prototype's all-red failure | Catalog orange streaming |
| D5 | **Warm reserved for alarms** (amber strain, red critical) | art-direction #7 §2 signal-to-noise principle | Warm ambient traffic (collides with crisis alarm) |
| D6 | Packets stay as the **colorblind-safe shape system** (triangles/circles/…) | art-direction #7 §5 (`[UX-DR4]` — colour never sole) | — (gameplay readability, not "abstract nodes") |
| D7 | Gable roof **ridge along Y** (peak faces camera) | the triangular gable-end is the silhouette that reads as "house" | ridge along X (camera sees a slope, reads as a cube) |

### Open follow-ups (not blocking these renders)
- **Canon reconciliation (Gru):** the light canvas ripples beyond art-direction #7 — `[FORGE #5]` "dark backdrop" lock and `narrative-v1` ("internet at night," the Dispatcher's 3am control room, "Error 404 / the internet goes dark"). The narrative's loss beat and mood language assume darkness; those need amendment if light ships. Flagged to Gru; not a render job.
- **Era-evolution stretch render** (map "electrifying" across 6 eras) — not yet produced; offered as a follow-up.
- **Ocean/landmass geography + undersea-cable arena** — sketched in the crisis shot only; full global-map texture is a future asset.

---

## 6. Amendment (2026-08-17) — the production surface ruling + the building sprite pipeline (story 7.1)

**Provenance:** user rulings via the 7.1 lavish style gate + pane chat, 2026-08-17.
The gate verdict, verbatim: *"7.1 top-down direction (r4): APPROVE — ship the top-down sprite direction as shown."*
(Gate page: `_bmad-output/design-analysis/style-gate-7.1/index.html`.)

**1. Surface style.** The 8 reference renders are **composition + shape-language
anchors only** — never surface treatment. The shipping surface is **Mini
Motorways flat-2D minimalism**: flat solid colors, crisp clean pipes, simple
geometric silhouettes, generous whitespace, pastel-on-cream, zero texture
noise, zero 3D materials/bevels/bloom/gradients/drop shadows. One refinement
of that ruling (user, same day, from the Blender 3/4 viewport screenshot):
buildings DO carry depth, the flat-2D way — **painted shading** (walls are one
flat darker tone; the gable roof's two slopes are two flat tones) + a **flat
contact shadow** drawn under each node by the game (a translucent ink ellipse;
Blender's hashed alpha dithers at sprite size, so the shadow is NOT baked).

**2. Buildings are a SPRITE pipeline.** True top-down (the MM view — a steep
tilt where the ROOF carries the read), our own designs, generated by
`tools/gen_sprites.py` (Blender 5.2, headless; flat emissive materials;
canon hexes converted sRGB→linear so the rendered pixels land ON the §2 hexes)
into `assets/sprites/` (committed, with a `sprites.json` content-bbox sidecar
embedded into the build). The game draws sprites for terminals + router pucks
(`app/render/sprites.odin`). The family: **residential** = two-tone gable roof
+ chimney (canon body/roof pairs, 4 colorways); **content host** = flat roof +
the big white play-button roof marking + rooftop vent + antenna; **data
center** = long flat roof + cooling-unit grid; **router pucks** = the round
hub — dark rim, face, core, green LED ring(s), tier-scaled (basic/mid/high).
The 6-type roster follows this language. No MM or purchased assets — ours,
reproducible from the committed script.

**3. Pipes (the 3.3 canon re-styled, not replaced).** The tier color owns a
wide flat **band** (×2.2 the pre-7.1 wire width); the three QoS lanes ride
INSIDE it as saturated stripes separated by canvas gutters (the motorway
lane-marking read; lane width still = the WFQ share). Zoom-level LOD: at the
bird's-eye the stripes are a hint (pre-composited toward the tier color — the
calm read); zoomed in they draw full.

**4. Camera (new canon).** Focus-zoom: selecting a node/link eases the camera
into it (~2.3×/2.6×) where lanes + queues reveal at full read; deselecting
eases back to the bird's-eye fit. Alerts-as-nav: the crisis banner click
focus-zooms the named bottleneck. Filter/focus: an SLA gauge row click focuses
that class (other classes ghost). The camera is app-owned presentation state —
the sim never sees it; the harness captures at the fit, so goldens pin the
bird's-eye read. **Bridges** (from the MM comparison) are deferred — a
candidate for the era-6 SDN look, not this story.

**5. Queued packets** pile at the building's doorstep (a deterministic fan
keyed by packet id), never on the roof.

**6. Renderer findings recorded (affect how goldens read).** (a) The pre-7.1
primitive house's roof triangle was silently CULLED by the software rasterizer
(winding order) — it never rendered in any T2 golden; the sprite path
supersedes it. (b) rlsw's line primitives draw OPAQUE regardless of alpha —
translucent line draws diverge between the GPU app and the goldens; the 7.1
draws pre-composite instead of alpha-blending.

---

*End of look-book v1 + the 7.1 amendment. Source: `blend-sources/pp_lib.py` + `.blend` + `tools/gen_sprites.py`. On approval these renders + this doc + the sources commit and a PR opens targeting `main` (never merged by the minion).*
