# KYLE Vision Audit: Packet-Plumber v2 vs Mini Motorways Bar

## Q1: Routers + Terminals vs MM Bar (Stills + Crops)
**(a) What I see:**  
- Routers: Circular 3D pucks with ports, soft 16% shadow blobs, extruded depth (juice-30000ms.png, router_tiers-02500ms.png, tt_router_mid.png, router_mid.png, router_high.png)  
- Terminals: 3D blocks with subtle shading and soft shadows (tt_residential.png, tt_small_biz.png, tt_campus.png, tt_content_host.png)  
- Background: Beige land, blue water, grid overlay (consistent across all stills)  
- Visual weight: Outlines are thin but 3D extrusion creates "game asset" look; shadows read as blobby rather than flat

**(b) MM contrast:**  
- MM uses flat 2D assets: Two-tone node discs (routers) with thin white outlines on cream paper background  
- MM terminals: Tiny flat rectangles with dark outlines, no extrusion  
- MM shadows: None (flat aesthetic) or minimal hard shadows  
- MM restraint: Subtle color coding, minimal visual noise

**(c) Ranked fixes:**  
1. **needs-art:** Replace 3D pucks with flat two-tone router discs (MM's flat disc + thin outline)  
2. **needs-art:** Replace 3D terminal blocks with flat rectangles (MM's tiny flat rects)  
3. **in-engine:** Remove soft shadow blobs (MM has no shadows)  
4. **in-engine:** Flatten background to cream paper texture (MM's warm cream paper)  

## Q2: Node Identifiability (Terminal_Types + Crops)
**(a) What I see:**  
- Residential: Brown 3D block (tt_residential.png)  
- Small_biz: Brown 3D block (tt_small_biz.png)  
- Campus: Brown 3D block (tt_campus.png)  
- Content_host: Blue 3D block (tt_content_host.png)  
- Router tiers: Size variation (basic smallest, high largest) but same 3D puck shape (router_tiers-02500ms.png, rt_basic_fixture, rt_mid, rt_high)  
- Identifiability: Only color differs; shape is identical across terminal types

**(b) MM contrast:**  
- MM: Distinct shape + color coding (rectangles vs circles vs triangles)  
- MM restraint: Minimal node types, clear visual hierarchy  
- MM: No two node types share the same base shape

**(c) Ranked fixes:**  
1. **needs-art:** Give each terminal type unique flat shape (MM's distinct shapes)  
2. **needs-art:** Enhance color contrast between terminal types  
3. **in-engine:** Add subtle icons to terminals (MM's minimal icons)  
4. **in-engine:** Ensure router tiers have distinct visual markers beyond size  

## Q3: Packet Motion (Motion Frames + Strips)
**(a) What I see:**  
- Packets: Small dots with glints, no visible trails (motion-29800ms.png through motion-30800ms.png, motion_strip_29800-30800.png)  
- Motion: Choppy, hard to track individual packets across 100ms frames  
- Spacing: Packets cluster, no clear separation  
- Readability: Lack of motion blur or trail makes tracking difficult

**(b) MM contrast:**  
- MM: Tiny flat packets with subtle trails  
- MM: Consistent spacing and speed  
- MM: Clear visual flow along roads

**(c) Ranked fixes:**  
1. **in-engine:** Add subtle packet trails (MM's trail effect)  
2. **in-engine:** Increase packet size slightly for better visibility  
3. **in-engine:** Add motion blur to packets in motion  
4. **in-engine:** Ensure consistent packet spacing along pipes  

## Q4: Terminal Spawn Cadence (Spawn Frames + Crops)
**(a) What I see:**  
- Spawn: Instant pop (spawn-02000ms.png, spawn_pop_zoom.png) with no gradual reveal  
- No telegraph or placement animation (spawn_pre_zoom.png shows empty space, then instant terminal)  
- Settling: Terminals appear fully formed immediately (spawn-02050ms.png, spawn-02100ms.png)  
- Visual feel: Abrupt, not gradual

**(b) MM contrast:**  
- MM: Gradual reveal with telegraph effect  
- MM: Placement animation (slide-in or fade)  
- MM: Smooth transition from empty space to terminal

**(c) Ranked fixes:**  
1. **in-engine:** Add spawn telegraph (MM's warning effect)  
2. **in-engine:** Implement gradual terminal reveal (fade or slide)  
3. **in-engine:** Add placement animation (MM's smooth transition)  
4. **in-engine:** Ensure terminals don't pop fully formed  

## Top 5 Gaps Summary
1. **3D vs 2D:** Entire asset suite needs flat 2D conversion (MM's aesthetic)  
2. **Shape Language:** Nodes lack distinct shapes (MM's unique shapes per type)  
3. **Motion Readability:** Packets need trails and better spacing  
4. **Spawn Polish:** Abrupt spawns need gradual reveal and telegraph  
5. **Visual Restraint:** Excessive 3D effects (shadows, extrusion) violate MM's minimalism  

DONE — findings at /Users/moses/.herdr/worktrees/packet-plumber/packet-plumber-v2-design-audit/_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/kyle-findings.md