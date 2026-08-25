# KYLE Vision Audit: Packet-Plumber v2 vs Mini Motorways (MM-Referenced)

## Q1: Routers + Terminals vs MM Bar
**(a) What OUR frames show:**  
- Routers: 3D pucks with ports, soft 16% shadow blobs, extruded depth (juice-30000ms.png, router_tiers-02500ms.png)  
- Terminals: 3D blocks with subtle shading (tt_residential.png, tt_small_biz.png, tt_campus.png, tt_content_host.png)  
- Background: Beige land, blue water, grid overlay  

**(b) What MM REFS show:**  
- MM buildings: Flat 2D rectangles with thin outlines, distinct shapes (image_01, image_02, image_03, image_04, image_05, image_06, image_07, image_08, image_09)  
- MM shadows: Subtle long shadows, not soft blobs  
- MM palette: Warm cream paper background, flat color blocks  

**(c) Pass-1 verdict:** Confirmed - MM uses flat 2D aesthetic with minimal depth cues  

**(d) Ranked fixes:**  
- **needs-art:** Replace 3D pucks with flat two-tone router discs (MM's flat disc + thin outline)  
- **needs-art:** Replace 3D terminal blocks with flat rectangles (MM's tiny flat rects)  
- **in-engine:** Remove soft shadow blobs (MM has long shadows, not blobs)  
- **in-engine:** Flatten background to cream paper texture (MM's warm cream paper)  

**(e) Sprite-vs-ref:** Our sprites have 3D extrusion and shading that MM doesn't have - requires Blender re-render  

## Q2: Node Identifiability
**(a) What OUR frames show:**  
- Terminals: Similar 3D block shapes, only color differs (tt_residential.png, tt_small_biz.png, tt_campus.png, tt_content_host.png)  
- Router tiers: Size variation but same 3D puck shape  

**(b) What MM REFS show:**  
- MM buildings: Distinct shapes per type (image_02, image_04, image_06, image_08, image_09)  
- MM color coding: Complementary to shape differences  

**(c) Pass-1 verdict:** Confirmed - MM uses distinct shapes, we only use color  

**(d) Ranked fixes:**  
- **needs-art:** Give each terminal type unique flat shape (MM's distinct shapes)  
- **needs-art:** Enhance color contrast between terminal types  
- **in-engine:** Add subtle icons to terminals (MM's minimal icons)  
- **in-engine:** Ensure router tiers have distinct visual markers beyond size  

**(e) Sprite-vs-ref:** Our terminal sprites share the same basic 3D block shape - requires Blender re-render  

## Q3: Packet Motion
**(a) What OUR frames show:**  
- Packets: Small dots with glints, no visible trails, choppy motion (motion-29800ms.png through motion-30800ms.png)  

**(b) What MM REFS show:**  
- MM cars: Subtle trails, consistent spacing along roads (image_01, image_03, image_05, image_07)  

**(c) Pass-1 verdict:** Confirmed - MM has better motion readability  

**(d) Ranked fixes:**  
- **in-engine:** Add subtle packet trails (MM's trail effect)  
- **in-engine:** Increase packet size slightly for better visibility  
- **in-engine:** Add motion blur to packets in motion  
- **in-engine:** Ensure consistent packet spacing along pipes  

**(e) Sprite-vs-ref:** Our packet sprites lack trails that MM cars have - can be fixed in-engine  

## Q4: Terminal Spawn Cadence
**(a) What OUR frames show:**  
- Spawn: Instant pop (spawn-02000ms.png, spawn_pop_zoom.png) with no gradual reveal  

**(b) What MM REFS show:**  
- MM buildings: Subtle appearance animations (image_01, image_03, image_05, image_07)  

**(c) Pass-1 verdict:** Confirmed - MM has smoother spawn animations  

**(d) Ranked fixes:**  
- **in-engine:** Add spawn telegraph (MM's warning effect)  
- **in-engine:** Implement gradual terminal reveal (fade or slide)  
- **in-engine:** Add placement animation (MM's smooth transition)  
- **in-engine:** Ensure terminals don't pop fully formed  

**(e) Sprite-vs-ref:** Our terminal sprites lack smooth appearance - requires Blender re-render  

## Top 5 Gaps Summary
1. **3D vs 2D:** Entire asset suite needs flat 2D conversion (MM's aesthetic)  
2. **Shape Language:** Nodes lack distinct shapes (MM's unique shapes per type)  
3. **Motion Readability:** Packets need trails and better spacing  
4. **Spawn Polish:** Abrupt spawns need gradual reveal and telegraph  
5. **Visual Restraint:** Excessive 3D effects violate MM's minimalism