# Art Direction v1 — Amendments (2026-08-08)

> **What this is.** A record of every user-directed change to the visual canon since
> `art-direction-v1.md` was lavish-approved (PR #7). The reference renders in
> `../art-renders/` (PR #9) implement these; this doc is the canon trail so a
> future editor (Gru) can fold them into `art-direction-v1.md` itself.
>
> **Status of v1:** approved sections stand EXCEPT where explicitly superseded below.
> Each amendment cites the v1 section it changes and the decision source.

| # | Amendment | Supersedes / refines in v1 | Source |
|---|---|---|---|
| **A1** | **Canvas = LIGHT (Mini-Motorways daytime).** Warm cream land + soft-blue water + green parks, flat cheerful colour, minimal/no bloom. | §1 "Dark (night) backdrop" lock; §4.1 `canvas-*` dark palette; the "internet at night, seen from above" thesis. Dark is retained as an *alternative* (`renders/01a-vista-dark.png`), not the default. | User verdict via in-render lavish A/B ("light"). |
| **A2** | **Terminals are LITERAL BUILDINGS, 6 types.** Residential (peaked-roof house), Content host (server/broadcast block), Gaming server (indigo + green sign), Financial hub (warm-stone bank + gold columns), Data center (big low block + rooftop units), CDN cache (bay-door warehouse). | §6.2 "terminals = abstract glowing shapes (rounded rect / diamond / hexagon…)" — reversed: shapes become literal building silhouettes. Shape+icon accessibility system (§5) is preserved via distinct silhouettes + facade accents. | User: "we need the buildings instead of boring shapes / beautiful art, not abstract shapes." + §6.2 roster. |
| **A3** | **Routers are ROUND capacity-scaled hub pucks**, a distinct *shape* family from the rectilinear buildings (disc + ring of indicator LEDs + glowing core; tier 1→3 scale ports/LEDs/core/rings). | §6.2 "junction (router) = an octagon" — replaced with a round infrastructure hub. Routers are infrastructure, never mistaken for a destination. | User: "the typical router icon is round" (round beats a colour-only distinction; colorblind-safe). |
| **A4** | **Pipes are smooth bezier conduits** with rounded caps + a glowing inner **core** on fiber/backbone tiers; refined thin weights. Tier = width + colour + luminosity + core. | §7.1 tier language (kept, refined): adds the elegant-curve + lit-core treatment. | User: pipes "minimalistic but elegant and beautiful"; Mini-Motorways road elegance. |
| **A5** | **Map background is canonical:** procedural landmasses (coastlines/bays) + ocean + green park blobs — MM-style, not a flat void. | §3 (the textured-map direction) — now implemented and locked in the light palette. | User: "a map background, just like in Mini Motorways." |
| **A6** | **Topology rule: terminals connect via ROUTERS only, never terminal-to-terminal.** Houses/buildings are leaves; routers are the interconnect (and route router-to-router). | New rule (refines §M3 node/pipe model): no house↔house links. | User: "houses shouldn't connect to each other — they should connect to routers." |
| **A7** | **Unchanged (rest of v1 stands):** blue streaming / grey email packet personalities (§2, §5); warm-reserved-for-alarms (§2); the 9-type colorblind-safe shape+icon system (§5); pipe tiers copper→backbone (§7.1); 6 eras + electrification arc (§9); the QoS-as-art flow readout (§5.3). | — | — |

---

## ⚠️ Cascade for Gru (reconciliation needed outside art-direction)

Amendment **A1 (light canvas)** ripples beyond art-direction into two other locked docs that assume darkness — Gru to reconcile:

- **`[FORGE #5]`** (the forge's sealed decision): "Mini Motorways clean-minimalist, 2D top-down, **dark backdrop**, glowing pipes, colored packet dots." The "dark backdrop" clause is now amended to light.
- **`narrative-v1.md`** (PR #5, merged): built on "the internet at night," the Dispatcher's 3am control room, and the **"Error 404 / the internet goes dark"** loss beat. If the canvas ships light, the narrative's mood language and the loss beat need re-voicing (a daytime network can still "go down," but the "goes dark" framing and night-shift voice no longer fit literally).

These are doc/narrative jobs, not render jobs. The renders (PR #9) implement the chosen light direction regardless.

---

## How the renders map to these amendments

| Render | Amendments demonstrated |
|---|---|
| `01b-vista-light.png` | A1 (light), A2 (buildings), A3 (round routers), A4 (elegant pipes), A5 (map), A6 (houses→routers) |
| `07-terminals.png` | A2 (full 6-building roster) |
| `06-router-variants.png` | A3 (round capacity tiers) |
| `04-pipes-tiers.png` | A4 (bezier + cores) |
| `02-packet-flow.png`, `03-node-identity.png`, `05-crisis.png` | A1, A7 (unchanged canon) |

Recipe + exact hexes for the 2D implementation: `../art-renders/look-book-v1.md`.
