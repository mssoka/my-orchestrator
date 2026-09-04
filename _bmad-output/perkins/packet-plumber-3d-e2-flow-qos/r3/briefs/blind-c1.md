You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
diff --git a/scenes/main.tscn b/scenes/main.tscn
index 5aad5da..c2b0d7c 100644
--- a/scenes/main.tscn
+++ b/scenes/main.tscn
@@ -1,4 +1,4 @@
-[gd_scene load_steps=9 format=3]
+[gd_scene load_steps=11 format=3]
 
 [ext_resource type="Script" path="res://scripts/main.gd" id="1"]
 [ext_resource type="Script" path="res://scripts/planet.gd" id="2"]
@@ -7,6 +7,8 @@
 [ext_resource type="Script" path="res://scripts/connect_controller.gd" id="5"]
 [ext_resource type="Script" path="res://scripts/hud.gd" id="6"]
 [ext_resource type="Script" path="res://scripts/capture_runner.gd" id="7"]
+[ext_resource type="Script" path="res://scripts/flow_view.gd" id="8"]
+[ext_resource type="Script" path="res://scripts/qos_panel.gd" id="9"]
 
 [sub_resource type="Environment" id="env"]
 background_mode = 1
@@ -55,8 +57,14 @@ script = ExtResource("4")
 [node name="ConnectController" type="Node" parent="."]
 script = ExtResource("5")
 
+[node name="FlowView" type="Node" parent="."]
+script = ExtResource("8")
+
 [node name="CaptureRunner" type="Node" parent="."]
 script = ExtResource("7")
 
+[node name="QosPanel" type="CanvasLayer" parent="."]
+script = ExtResource("9")
+
 [node name="HUD" type="CanvasLayer" parent="."]
 script = ExtResource("6")
diff --git a/scripts/capture_runner.gd b/scripts/capture_runner.gd
index 8d17b8e..5acb372 100644
--- a/scripts/capture_runner.gd
+++ b/scripts/capture_runner.gd
@@ -72,10 +72,54 @@ func _run() -> void:
 	_rig.snap()
 	await _settle()
 	await _shot("04-parallel-bundle.png")
+	await _e2_shots(sites)
 	print("capture: done -> %s" % ProjectSettings.globalize_path(OUT_DIR))
 	get_tree().quit(0)
 
 
+## E2 shots: a connected network with live packet flow, then the QoS panel
+## mid-interaction (ladder applied — strands visibly re-thicken).
+func _e2_shots(sites: Array) -> void:
+	var main := get_parent()
+	var by_idx: Array = sites
+	# A 3-wedge network through the REAL verb path: houses -> routers, an
+	# inter-wedge spine, enough reachable destinations for live demand.
+	var spine: Array = [by_idx[0], by_idx[9]]
+	for pair in [
+		[1, 0], [2, 0], [3, 0], [4, 0],
+		[0, 9], [10, 9], [12, 9], [13, 9],
+		[9, 11], [13, 11], [15, 11], [17, 11],
+		[11, 22], [23, 22], [25, 22], [27, 22],
+	]:
+		_controller.connect_programmatic(by_idx[pair[0]], by_idx[pair[1]])
+	# Give the spine the 3-lane ladder BEFORE the flow shot so class-dependent
+	# strand speeds are real in the capture (express dots visibly outrun).
+	var spine_sim = main.get("sim")
+	var spine_bundle = spine_sim.bundle_for_pair(spine[0].node_index, spine[1].node_index)
+	var panel = main.get_node("QosPanel")
+	panel.open(int(spine_bundle.id), spine_sim) # public surface: open + the apply signal
+	panel.apply_requested.emit(int(spine_bundle.id), [50, 30, 20], {"email": 2, "streaming": 0})
+	# Let the sim run (main steps it per physics frame) until arcs carry traffic.
+	for i in 540:
+		await get_tree().process_frame
+	# 5 — packets streaming along the spine at class-dependent speeds.
+	_rig.frame_point(_arc_mid(spine[0], spine[1]), 1)
+	_rig.snap()
+	await _settle()
+	await _shot("06-packets-flowing.png")
+	# 6 — the QoS panel on pipe select: re-open on the ALREADY-3-lane spine
+	# and apply again (idempotent command) so the panel reads the live state.
+	var sim = main.get("sim")
+	var bundle = sim.bundle_for_pair(spine[0].node_index, spine[1].node_index)
+	var pipe_id := int(bundle.id)
+	panel.open(pipe_id, sim)
+	await _settle(6)
+	panel.apply_requested.emit(pipe_id, [50, 30, 20], {"email": 2, "streaming": 0})
+	await _settle(6)
+	await _shot("07-qos-panel.png")
+	qos_close(main)
+
+
 func _settle(frames := 24) -> void:
 	for i in frames:
 		await get_tree().process_frame
@@ -124,3 +168,9 @@ func _readable_pair(sites: Array) -> Array:
 func _arc_mid(a: NodeSite, b: NodeSite) -> Vector3:
 	var mid := Geodesic.geodesic_points(a.global_position, b.global_position, 2)[1]
 	return mid * WorldSeed.PLANET_RADIUS
+
+
+## Close the QoS panel through its own control (the capture ends the interaction).
+func qos_close(main: Node) -> void:
+	var panel = main.get_node("QosPanel")
+	panel.close_panel()
diff --git a/scripts/connect_controller.gd b/scripts/connect_controller.gd
index 2e8bb7a..283c9c5 100644
--- a/scripts/connect_controller.gd
+++ b/scripts/connect_controller.gd
@@ -1,13 +1,15 @@
 class_name ConnectController
 extends Node
 
-## E1.3 + E1.4 — the connect verb. While drawing, the pointer ray-casts the
-## planet (physics layer 1) and the preview arc follows the surface
-## projection; a generous snap radius (measured in surface ARC, so the feel
-## is zoom-independent) lifts the target to the nearest qualifying node.
-## Release on a snapped node connects; release elsewhere cancels — no
-## accidental pipes. Committed pipes are registered so parallel same-pair
-## pipes merge into one fatter bundle.
+## E1.3 + E2 — the connect verb's gesture half. While drawing, the pointer
+## ray-casts the planet (physics layer 1) and the preview arc follows the
+## surface projection; a generous snap radius (measured in surface ARC, so
+## the feel is zoom-independent) lifts the target to the nearest qualifying
+## node. Release on a snapped node connects; release elsewhere cancels.
+##
+## E2: committing is a SIM COMMAND — the controller asks main to apply
+## add_pipe; FlowView builds the arc (bundle merge included) from sim state.
+## No pipe state lives here anymore.
 
 const SNAP_ARC_RAD := 0.24 # ~14° of surface arc — generous
 const PREVIEW_COLOR := Color(1.0, 0.85, 0.6, 0.65)
@@ -19,9 +21,7 @@ var _preview: PipeArc
 @onready var rig: OrbitCamera = get_node("../OrbitRig")
 @onready var nodes_container: Node3D = get_node("../Nodes")
 @onready var pipes_container: Node3D = get_node("../Pipes")
-
-## pair key -> {count: int, arc: PipeArc}
-var _registry := {}
+@onready var _main: Node3D = get_parent()
 
 
 func _ready() -> void:
@@ -92,32 +92,20 @@ func draw_cancel() -> void:
 	_last_preview_end = Vector3.INF
 
 
-## Programmatic commit — used by the release path AND the capture harness so
-## the renders tested in captures are exactly the renders gameplay produces.
+## Programmatic commit — routes through the REAL command path (sim add_pipe
+## + FlowView binding), so the renders tested in captures are exactly the
+## renders gameplay produces.
 func connect_programmatic(a: NodeSite, b: NodeSite) -> PipeArc:
-	var key := _pair_key(a, b)
-	if _registry.has(key):
-		var entry: Dictionary = _registry[key]
-		entry.count += 1
-		var params: Array = entry.arc.merged_params(entry.count)
-		entry.arc.build(a.global_position, b.global_position, params[0], params[1])
-		_pop(entry.arc)
-		return entry.arc
-	var arc := PipeArc.new()
-	arc.name = "Pipe_%s_%s" % [a.name, b.name]
-	pipes_container.add_child(arc)
-	arc.build(a.global_position, b.global_position, 1.0, 3)
-	_registry[key] = {"count": 1, "arc": arc}
-	return arc
+	return _main.request_connect(a, b)
 
 
 func pipe_count(a: NodeSite, b: NodeSite) -> int:
-	var key := _pair_key(a, b)
-	return _registry[key].count if _registry.has(key) else 0
+	var sim: SimCore = _main.sim
+	return sim.pipe_count(a.node_index, b.node_index)
 
 
 func _show_preview(a: Vector3, b: Vector3) -> void:
-	_preview.build(a, b, 1.0, 3)
+	_preview.build(a, b, 1.0)
 	_preview.visible = true
 
 
@@ -133,17 +121,3 @@ func _project_pointer(screen_pos: Vector2) -> Vector3:
 	if hit.is_empty():
 		return Vector3.INF
 	return hit.position
-
-
-## Pair key — unordered, so A→B and B→A share the bundle.
-func _pair_key(a: NodeSite, b: NodeSite) -> String:
-	var an := str(a.name)
-	var bn := str(b.name)
-	return an + "|" + bn if an < bn else bn + "|" + an
-
-
-func _pop(arc: PipeArc) -> void:
-	var tween := create_tween()
-	arc.scale = Vector3.ONE * 1.18
-	tween.tween_property(arc, "scale", Vector3.ONE, 0.18)\
-		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
diff --git a/scripts/flow_view.gd b/scripts/flow_view.gd
new file mode 100644
index 0000000..af52408
--- /dev/null
+++ b/scripts/flow_view.gd
@@ -0,0 +1,177 @@
+class_name FlowView
+extends Node
+
+## E2 — the sim-to-view bridge. Renders SimCore state: one PipeArc per
+## bundle (rebuilt on parallel-count or allocation changes), packet dots
+## riding their lane's strand, and node egress pulses. READS the sim every
+## frame; NEVER writes it (the view-purity contract pins that).
+
+const DOT_RADIUS := 0.11
+const MAX_DOTS_PER_PIPE := 48 # beyond this the density speaks; lowest ids win
+
+var sim: SimCore
+var nodes_container: Node3D
+var pipes_container: Node3D
+
+var _pipe_views := {} # pipe_id -> PipeArc
+var _pipe_meta := {} # pipe_id -> {parallel, alloc} — change detection
+var _dots := {} # pipe_id -> Array[MeshInstance3D]
+var _dot_mats := {} # class -> StandardMaterial3D
+
+
+func setup(sim_: SimCore, nodes_container_: Node3D, pipes_container_: Node3D) -> void:
+	sim = sim_
+	nodes_container = nodes_container_
+	pipes_container = pipes_container_
+	for cls in SimBalance.CLASS_IDS:
+		var m := StandardMaterial3D.new()
+		m.albedo_color = SimBalance.CLASSES[cls].color
+		m.roughness = 0.5
+		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
+		_dot_mats[cls] = m
+
+
+func arc_for(pipe_id: int) -> PipeArc:
+	return _pipe_views.get(pipe_id)
+
+
+## One sync pass: create/rebuild changed pipe views, then position dots.
+func sync() -> void:
+	if sim == null:
+		return
+	for pid in sim.pipes.keys():
+		var p: Dictionary = sim.pipes[pid]
+		var id := int(pid)
+		var meta: Dictionary = _pipe_meta.get(id, {})
+		if not _pipe_views.has(id):
+			_create_view(id, p)
+		elif int(meta.get("parallel", 0)) != int(p.parallel):
+			_rebuild_view(id, p)
+			_pop(_pipe_views[id]) # E1 'grow bigger' feedback on the bundle merge
+		elif meta.get("alloc", []) != p.alloc:
+			_rebuild_view(id, p)
+		_sync_dots(id, p)
+	# E2 has no demolish; stale views would be freed here.
+
+
+## Pipe pick for the select verb: closest approach of the screen ray to each
+## arc's path samples. Generous, zoom-scaled threshold. View-layer only.
+func pick_pipe(screen_pos: Vector2, camera: Camera3D) -> int:
+	if sim == null or sim.pipes.is_empty():
+		return -1
+	var from := camera.project_ray_origin(screen_pos)
+	var dir := camera.project_ray_normal(screen_pos)
+	# Occlusion guard: a far-side pipe near the ray's EXIT point must never
+	# win a click aimed at the visible hemisphere — reject samples beyond
+	# the planet's near-surface hit.
+	var entry := Geodesic.ray_sphere(from, dir, Vector3.ZERO, WorldSeed.PLANET_RADIUS)
+	var max_t := INF
+	if entry != Vector3.INF:
+		max_t = (entry - from).length()
+	var best_id := -1
+	var best_dist := 1e12
+	for pid in _pipe_views: # the view's own registry — geometry, not sim state
+		var arc: PipeArc = _pipe_views[pid]
+		if arc == null:
+			continue
+		var planet_dist := from.length() - WorldSeed.PLANET_RADIUS
+		var thr := clampf(absf(planet_dist) * 0.05, 0.25, 1.5)
+		var path: PackedVector3Array = arc.get_path_samples()
+		for i in range(0, path.size(), 2): # every 2nd sample — plenty at 49 pts
+			var to_p := path[i] - from
+			var t := to_p.dot(dir)
+			if t < 0.0 or t > max_t:
+				continue
+			var d := (to_p - dir * t).length()
+			if d < thr and d < best_dist:
+				best_dist = d
+				best_id = int(pid)
+	return best_id
+
+
+func _create_view(id: int, p: Dictionary) -> void:
+	var arc := PipeArc.new()
+	arc.name = "Pipe_%d" % id
+	pipes_container.add_child(arc)
+	_pipe_views[id] = arc
+	_dots[id] = []
+	_apply_build(arc, p)
+	_pop(arc)
+	_pipe_meta[id] = {"parallel": int(p.parallel), "alloc": p.alloc.duplicate()}
+
+
+func _rebuild_view(id: int, p: Dictionary) -> void:
+	var arc: PipeArc = _pipe_views[id]
+	_apply_build(arc, p)
+	_pipe_meta[id] = {"parallel": int(p.parallel), "alloc": p.alloc.duplicate()}
+
+
+func _apply_build(arc: PipeArc, p: Dictionary) -> void:
+	var a: Vector3 = sim.node_pos[p.a]
+	var b: Vector3 = sim.node_pos[p.b]
+	# merged-bundle growth: fatter cable per parallel pipe (E1 ladder, capped)
+	var scale := minf(1.0 + 0.45 * float(int(p.parallel) - 1), 2.2)
+	arc.build(a, b, scale, p.alloc)
+
+
+func _pop(arc: PipeArc) -> void:
+	var tween := create_tween()
+	arc.scale = Vector3.ONE * 1.18
+	tween.tween_property(arc, "scale", Vector3.ONE, 0.18)\
+		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
+
+
+func _sync_dots(id: int, p: Dictionary) -> void:
+	var pool: Array = _dots[id]
+	var arc: PipeArc = _pipe_views[id]
+	var length := maxf(1.0, float(p.length_milli))
+	var used := 0
+	var capped := false
+	for endpoint in 2:
+		var inflight: Array = p.inflight_a if endpoint == 0 else p.inflight_b
+		for k in inflight.size():
+			if used >= MAX_DOTS_PER_PIPE:
+				capped = true # density speaks; hide the rest — never ghost
+				break
+			var pkt: Dictionary = sim.packets.get(inflight[k])
+			if pkt == null:
+				continue
+			# Slot reuse must REBIND the class material — a slot that once
+			# held streaming would otherwise render email packets blue.
+			var t := float(int(pkt.progress_milli)) / length
+			if endpoint == 1:
+				t = 1.0 - t # b -> a traversal renders reversed
+			var lane := int(pkt.lane)
+			var pos := arc.strand_point(lane, t)
+			var dot: MeshInstance3D
+			if used < pool.size():
+				dot = pool[used]
+				dot.visible = true
+				dot.material_override = _dot_mats[pkt.cls]
+			else:
+				dot = MeshInstance3D.new()
+				var sphere := SphereMesh.new()
+				sphere.radius = DOT_RADIUS
+				sphere.height = DOT_RADIUS * 2.0
+				sphere.radial_segments = 10
+				sphere.rings = 6
+				dot.mesh = sphere
+				dot.material_override = _dot_mats[pkt.cls]
+				dot.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
+				pipes_container.add_child(dot)
+				pool.append(dot)
+			dot.global_position = pos
+			used += 1
+		if capped:
+			break
+	for i in range(used, pool.size()):
+		pool[i].visible = false
+
+
+## Node egress pulses — the visible serialization beat (E2.4).
+func pulse_egress() -> void:
+	for i in sim.node_admissions.size():
+		if sim.node_admissions[i] > 0 and i < nodes_container.get_child_count():
+			var site := nodes_container.get_child(i)
+			if site is NodeSite:
+				(site as NodeSite).pulse_egress()
diff --git a/scripts/flow_view.gd.uid b/scripts/flow_view.gd.uid
new file mode 100644
index 0000000..2fa9081
--- /dev/null
+++ b/scripts/flow_view.gd.uid
@@ -0,0 +1 @@
+uid://dh0o5x5bk6cve
diff --git a/scripts/hud.gd b/scripts/hud.gd
index 0e12e10..feedade 100644
--- a/scripts/hud.gd
+++ b/scripts/hud.gd
@@ -1,9 +1,14 @@
+class_name Hud
 extends CanvasLayer
 
-## Quiet-when-healthy HUD: one hint chip, no meters, no health, no sim UI.
-## The map is the UI (canon) — slice 1 carries only the verb cheat-sheet.
+## Quiet-when-healthy HUD (canon): the verb cheat-sheet chip plus a breach
+## chip that appears ONLY when a class's SLA latch is on. No meters, no
+## always-on sim UI — the map is the UI.
 
-const HINT := "drag space — orbit   ·   scroll — zoom   ·   drag a node — connect"
+const HINT := "drag space — orbit   ·   scroll — zoom   ·   drag a node — connect   ·   click a pipe — QoS"
+
+var _breach := Label.new()
+var _breach_panel := PanelContainer.new()
 
 
 func _ready() -> void:
@@ -31,3 +36,27 @@ func _ready() -> void:
 	add_child(panel)
 	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
 	panel.position.y -= 28.0
+
+	# breach chip — hidden until an SLA latch fires (quiet-when-healthy)
+	var bstyle := style.duplicate()
+	bstyle.bg_color = Color(WorldSeed.COL_ROOF, 0.85)
+	_breach_panel.add_theme_stylebox_override("panel", bstyle)
+	_breach_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
+	_breach.add_theme_font_size_override("font_size", 14)
+	_breach.add_theme_color_override("font_color", Color(0.98, 0.9, 0.86))
+	_breach.mouse_filter = Control.MOUSE_FILTER_IGNORE
+	_breach_panel.add_child(_breach)
+	add_child(_breach_panel)
+	_breach_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER_TOP)
+	_breach_panel.position.y = 18.0
+	_breach_panel.visible = false
+
+
+## Empty string hides the chip (the latches cleared -> quiet again).
+func set_breaches(lines: String) -> void:
+	if lines.is_empty():
+		_breach_panel.visible = false
+		return
+	if _breach.text != lines:
+		_breach.text = lines
+	_breach_panel.visible = true
diff --git a/scripts/input_router.gd b/scripts/input_router.gd
index 19f6d7e..83a3ad2 100644
--- a/scripts/input_router.gd
+++ b/scripts/input_router.gd
@@ -1,10 +1,12 @@
 class_name InputRouter
 extends Node
 
-## E1.3 — positional input disambiguation (the load-bearing grammar):
-## press on a node = begin DRAW; press anywhere else (surface, sky) = begin
-## ORBIT. One rule, no modes. The decision is factored into the static
-## classify() so the headless suite can pin the contract.
+## E1.3 + E2.3 — positional input disambiguation (the load-bearing grammar):
+## press on a node = begin DRAW; press on a pipe = begin SELECT (a clean
+## click opens the QoS panel; dragging past the click threshold becomes an
+## orbit); press anywhere else = ORBIT. One positional rule, no modes. The
+## decision is factored into the static classify() so the headless suite can
+## pin the contract.
 
 signal draw_requested(site: NodeSite)
 signal draw_moved(screen_pos: Vector2, rel: Vector2)
@@ -12,19 +14,27 @@ signal orbit_moved(rel: Vector2)
 signal gesture_ended(screen_pos: Vector2)
 signal zoom_requested(step: int)
 signal gesture_cancelled
+signal pipe_selected(pipe_id: int)
 
 const PINCH_STEP_FACTOR := 1.25 # accumulated pinch growth per ladder step
+const CLICK_SLOP_PX := 6.0 # press-release movement still counted as a click
 
 var _pinch_accum := 1.0
 
-enum Mode { NONE, DRAW, ORBIT }
+enum Mode { NONE, DRAW, ORBIT, SELECT }
 
 var _mode: Mode = Mode.NONE
+var _press_pos := Vector2.ZERO
+var _picked_pipe := -1
 
 @onready var camera: Camera3D = get_node("../OrbitRig/Camera3D")
+@onready var flow_view: FlowView = get_node("../FlowView")
 
 
-## THE rule: a node hit draws, anything else orbits.
+## THE positional rule for PHYSICS hits: a node draws, anything else orbits.
+## The pipe branch is geometric (not physics) — it lives in _begin, which
+## consults FlowView.pick_pipe after the physics classify, and is pinned by
+## tests/test_view_interaction.gd's real-gesture legs.
 static func classify(collider: Object) -> Mode:
 	if collider is NodeSite:
 		return Mode.DRAW
@@ -52,6 +62,11 @@ func _unhandled_input(event: InputEvent) -> void:
 	elif event is InputEventMouseMotion and _mode != Mode.NONE:
 		if _mode == Mode.DRAW:
 			draw_moved.emit(event.position, event.relative)
+		elif _mode == Mode.SELECT:
+			if event.position.distance_to(_press_pos) > CLICK_SLOP_PX:
+				_mode = Mode.ORBIT # a dragged select becomes an orbit
+			else:
+				return # still within click slop — no motion yet
 		else:
 			orbit_moved.emit(event.relative)
 
@@ -67,16 +82,28 @@ func _notification(what: int) -> void:
 
 
 func _begin(screen_pos: Vector2) -> void:
+	_press_pos = screen_pos
+	_picked_pipe = -1
 	var hit := _pick(screen_pos)
 	_mode = classify(hit.get("collider") if hit else null)
 	if _mode == Mode.DRAW:
 		draw_requested.emit(hit.collider)
+		return
+	# Not a node: pipes ride ABOVE the planet body, so try the geometric pipe
+	# pick before falling back to orbit (a planet-body physics hit must not
+	# shadow a pipe press).
+	_picked_pipe = flow_view.pick_pipe(screen_pos, camera)
+	_mode = Mode.SELECT if _picked_pipe >= 0 else Mode.ORBIT
 
 
 func _end(screen_pos: Vector2) -> void:
 	var was := _mode
 	_mode = Mode.NONE
-	if was != Mode.NONE:
+	if was == Mode.SELECT and _picked_pipe >= 0 \
+			and screen_pos.distance_to(_press_pos) <= CLICK_SLOP_PX:
+		pipe_selected.emit(_picked_pipe)
+	_picked_pipe = -1
+	if was != Mode.NONE and was != Mode.SELECT:
 		gesture_ended.emit(screen_pos)
 
 
diff --git a/scripts/main.gd b/scripts/main.gd
index b59947e..9ed547d 100644
--- a/scripts/main.gd
+++ b/scripts/main.gd
@@ -1,29 +1,169 @@
+@tool
 extends Node3D
 
-## Slice-1 composition root: builds the seeded world, stages the nodes, and
-## wires the input grammar (router -> camera / connect controller).
-## NO sim state is created anywhere in this slice (E1 canon).
+## Slice-1 + E2 composition root: builds the seeded world, stages the nodes,
+## wires the input grammar (router -> camera / connect controller), owns the
+## deterministic SimCore (stepped once per physics tick), and binds FlowView.
+##
+## @tool + "Regenerate Preview" (folded QoL): in the EDITOR the inspector
+## button runs the SAME seeded generation into the viewport; _ready returns
+## early under the editor hint so the runtime boot path is byte-identical to
+## E1. Generated nodes carry no owner, so they never serialize into the
+## saved scene.
 
 const SEED := 20260904 # slice-1 world seed — deterministic from here
 
+@export_tool_button("Regenerate Preview", "Reload") var regenerate_preview: Callable = _regenerate_preview
+
 @onready var planet: Planet = $Planet
 @onready var nodes_container: Node3D = $Nodes
+@onready var pipes_container: Node3D = $Pipes
 @onready var router: InputRouter = $InputRouter
 @onready var controller: ConnectController = $ConnectController
 @onready var rig: OrbitCamera = $OrbitRig
+@onready var flow_view: FlowView = $FlowView
+@onready var qos_panel: QosPanel = $QosPanel
+@onready var hud: Hud = $HUD
+
+var sim: SimCore
 
 
 func _ready() -> void:
-	_aim_lights()
-	var layout := WorldSeed.wedge_layout(SEED)
-	planet.generate(SEED, layout)
-	_stage_nodes(SEED, layout)
+	if Engine.is_editor_hint():
+		# Folded-QoL evidence affordance: one-shot editor capture for the
+		# capture harness (see PR notes). The button path is the same code.
+		if OS.get_cmdline_user_args().has("--editor-preview-shot"):
+			_editor_preview_shot()
+		return # the editor builds via the inspector button — runtime path untouched
+	var layout := WorldSeed.wedge_layout(SEED) # computed ONCE, threaded everywhere
+	_generate_world(layout)
+	sim = SimCore.new()
+	sim.setup(SEED, WorldSeed.node_placements(SEED, layout))
+	if Engine.physics_ticks_per_second != SimBalance.TICK_HZ:
+		# Silent default-drift guard: every wall-clock constant (SLA tolerances,
+		# demand intervals) anchors on the 60 Hz tick.
+		push_warning("physics_ticks_per_second=%d != SimBalance.TICK_HZ=%d — wall-clock sim semantics drift"
+			% [Engine.physics_ticks_per_second, SimBalance.TICK_HZ])
+	flow_view.setup(sim, nodes_container, pipes_container)
 	router.draw_requested.connect(_on_draw_requested)
 	router.orbit_moved.connect(rig.orbit)
 	router.draw_moved.connect(controller.draw_move)
 	router.gesture_ended.connect(controller.draw_end)
 	router.gesture_cancelled.connect(controller.draw_cancel)
 	router.zoom_requested.connect(rig.zoom)
+	router.pipe_selected.connect(_on_pipe_selected)
+	qos_panel.apply_requested.connect(_on_qos_apply)
+
+
+## Fixed tick: one sim step per physics frame (60 Hz) — the ONLY place the
+## sim advances during play.
+func _physics_process(_delta: float) -> void:
+	if Engine.is_editor_hint() or sim == null:
+		return
+	sim.step_tick()
+
+
+## View sync + egress pulses + SLA breach chip — reads only.
+func _process(_delta: float) -> void:
+	if Engine.is_editor_hint() or sim == null:
+		return
+	flow_view.sync()
+	flow_view.pulse_egress()
+	hud.set_breaches(_breach_lines())
+
+
+## The connect verb's commit path AND the programmatic path (captures,
+## tests): one sim command, one FlowView sync, return the bound arc.
+func request_connect(a: NodeSite, b: NodeSite) -> PipeArc:
+	if sim == null:
+		return null
+	sim.apply_command({"cmd": "add_pipe", "a": a.node_index, "b": b.node_index})
+	flow_view.sync()
+	var bundle = sim.bundle_for_pair(a.node_index, b.node_index)
+	if bundle == null:
+		return null
+	return flow_view.arc_for(int(bundle.id))
+
+
+func _on_pipe_selected(pipe_id: int) -> void:
+	qos_panel.open(pipe_id, sim)
+
+
+func _on_qos_apply(pipe_id: int, alloc: Array, cls_lane: Dictionary) -> void:
+	sim.apply_command({"cmd": "set_lanes", "pipe": pipe_id, "alloc": alloc, "cls_lane": cls_lane})
+	qos_panel.open(pipe_id, sim) # re-read the applied state
+
+
+## One-shot editor capture: regenerate via the REAL button path, then save
+## the editor viewport (world visible without pressing play) and quit.
+func _editor_preview_shot() -> void:
+	# The editor boots slowly — wait until the edited scene is actually open
+	# and the viewport has drawn real frames before capturing.
+	for i in 120:
+		await get_tree().process_frame
+		if get_tree().edited_scene_root == self and i > 60:
+			break
+	_regenerate_preview()
+	var vp3d: Viewport = _editor_vp3d()
+	# The editor's default 3D camera sits INSIDE the radius-8 planet (its
+	# front faces cull) — move it outside for the shot: a globe view of origin.
+	if vp3d != null:
+		var cam: Camera3D = vp3d.get_camera_3d()
+		if cam != null:
+			cam.global_transform = Transform3D(Basis.IDENTITY, Vector3(0, 9, 20))
+			cam.look_at(Vector3.ZERO)
+	for i in 60:
+		await get_tree().process_frame
+		RenderingServer.force_draw()
+	var img := Image.new()
+	if vp3d != null:
+		img = vp3d.get_texture().get_image()
+		print("editor-preview-shot: 3d viewport %dx%d" % [img.get_width(), img.get_height()])
+	else:
+		img = get_viewport().get_texture().get_image()
+		print("editor-preview-shot: window viewport %dx%d" % [img.get_width(), img.get_height()])
+	var err := img.save_png(ProjectSettings.globalize_path("res://captures/08-editor-preview.png"))
+	print("editor-preview-shot: saved (err %d)" % err)
+	get_tree().quit(0 if err == OK else 1)
+
+
+## EditorInterface resolves through the Engine singleton registry so this
+## @tool script still PARSES in export templates (the class does not exist
+## there — a direct identifier reference would kill the composition root).
+func _editor_vp3d() -> Viewport:
+	if not Engine.has_singleton("EditorInterface"):
+		return null
+	var ei: Variant = Engine.get_singleton("EditorInterface")
+	return ei.get_editor_viewport_3d(0)
+
+
+## The ONE seeded generation body — the runtime boot AND the editor's
+## "Regenerate Preview" both run exactly this. The layout is computed ONCE
+## by the caller and threaded through, so staged nodes and sim placements
+## can never drift onto different layouts.
+func _generate_world(layout: Dictionary) -> void:
+	_aim_lights()
+	planet.generate(SEED, layout)
+	_stage_nodes(SEED, layout)
+
+
+## EDITOR ONLY (guarded): clear + re-run the SAME seeded generation the
+## runtime boot uses, so the viewport shows the real world without play.
+func _regenerate_preview() -> void:
+	if not Engine.is_editor_hint():
+		return
+	_clear_generated()
+	_generate_world(WorldSeed.wedge_layout(SEED))
+
+
+func _clear_generated() -> void:
+	for c in planet.get_children():
+		planet.remove_child(c)
+		c.free()
+	for container: Node3D in [nodes_container, pipes_container]:
+		for c in container.get_children():
+			container.remove_child(c)
+			c.free()
 
 
 ## Warm key + cool fill, aimed by hand — code keeps the basis honest.
@@ -35,12 +175,27 @@ func _aim_lights() -> void:
 
 
 func _stage_nodes(seed_value: int, layout: Dictionary) -> void:
-	for info in WorldSeed.node_placements(seed_value, layout):
+	var placements := WorldSeed.node_placements(seed_value, layout)
+	for i in placements.size():
 		var site := NodeSite.new()
 		nodes_container.add_child(site)
-		site.setup(info)
+		site.setup(placements[i])
+		site.node_index = i
 
 
 ## A draw gesture may only begin on a node (router guarantees classification).
 func _on_draw_requested(site: NodeSite) -> void:
 	controller.draw_begin(site)
+
+
+func _breach_lines() -> String:
+	var parts := PackedStringArray()
+	for cls in SimBalance.CLASS_IDS:
+		var s: Dictionary = sim.sla[cls]
+		# Independent ifs: a latency latch must never hide a co-occurring loss
+		# breach (sticky latches would silence it forever).
+		if bool(s.lat_breach):
+			parts.append("%s latency SLA breached" % cls)
+		if bool(s.loss_breach):
+			parts.append("%s loss SLA breached" % cls)
+	return "  ·  ".join(parts)
diff --git a/scripts/node_site.gd b/scripts/node_site.gd
index a0f0c2c..7c9f083 100644
--- a/scripts/node_site.gd
+++ b/scripts/node_site.gd
@@ -8,10 +8,35 @@ extends Area3D
 
 const HOUSE_SCALE := Vector3(0.8, 0.55, 0.7)
 const ROUTER_SCALE := Vector3(0.45, 0.8, 0.45)
+const PULSE_COOLDOWN := 0.22 # seconds between egress pulses
 
 var site_name := ""
 var kind := "house" # "house" | "router"
 var surface_pos := Vector3.ZERO # world-space surface point (length R)
+var node_index := -1 # sim node id (staging order = WorldSeed order)
+
+var _pulse_cd := 0.0
+
+
+func _process(delta: float) -> void:
+	if _pulse_cd > 0.0:
+		_pulse_cd -= delta
+
+
+## E2.4 — one visible egress beat: the building visibly bumps as packets
+## serialize out of it. Cooldown keeps a saturated node readable (a beat,
+## not a blur). View-layer only — the sim never calls into here.
+func pulse_egress() -> void:
+	if _pulse_cd > 0.0:
+		return
+	_pulse_cd = PULSE_COOLDOWN
+	var visual := get_node_or_null("Visual")
+	if visual == null:
+		return
+	var tween := create_tween()
+	visual.scale = Vector3.ONE * 1.14
+	tween.tween_property(visual, "scale", Vector3.ONE, PULSE_COOLDOWN)\
+		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
 
 
 func setup(info: Dictionary) -> void:
diff --git a/scripts/pipe_arc.gd b/scripts/pipe_arc.gd
index 2a5a73a..7ae4da5 100644
--- a/scripts/pipe_arc.gd
+++ b/scripts/pipe_arc.gd
@@ -1,12 +1,14 @@
 class_name PipeArc
 extends MeshInstance3D
 
-## E1.4 — a pipe rendered as a bundled cable riding the surface on trestles:
-## the path is a valid geodesic (great circle) lifted by a slight sine
-## elevation — it never tunnels through the planet. Three strands render the
-## cable identity (class-queue strands arrive with E2; here they are
-## presentation-only). Parallel pipes between the same node pair merge into
-## one fatter bundle via rebuild().
+## E1.4 + E2.3/E2.4 — a pipe rendered as a bundled cable riding the surface
+## on trestles: the path is a valid geodesic (great circle) lifted by a
+## slight sine elevation — it never tunnels through the planet. The three
+## strands ARE the three class lanes (Express / Standard / Best-effort):
+## strand thickness = the lane's allocation share, and in-flight packet dots
+## ride their lane's strand at lane speed (the sim drives positions; this
+## node only renders). Parallel pipes between the same node pair merge into
+## one fatter bundle via the shared `radius_scale`.
 ##
 ## Frame construction (the load-bearing trick): every arc is a great circle,
 ## so the {outward-radial, path-plane-normal} pair is an exact orthonormal
@@ -19,39 +21,81 @@ const BASE_RADIUS := 0.09
 const BASE_ELEVATION_FRAC := 0.064 # peak lift as a fraction of the planet radius
 const TRESTLE_EVERY := 6 # a post every Nth path sample
 const STRAND_RING := 0.38 # strand-circle radius as a fraction of cable radius — tight, reads as one cable
+const HAIRLINE_FRAC := 0.3 # an unallocated lane renders as a hairline strand
 
 var _a := Vector3.ZERO
 var _b := Vector3.ZERO
 var _radius_scale := 1.0
-var _strand_count := 3
+var _shares := [100, 0, 0] # lane allocation shares (view mirror of the sim)
+var _path := PackedVector3Array()
 
 
 ## Build/rebuild the arc. `radius_scale` > 1 renders the merged parallel
-## bundle; `strands` grows with the pipe count (3 per pipe, capped).
-func build(a: Vector3, b: Vector3, radius_scale := 1.0, strands := 3) -> void:
+## bundle; `shares` are the three lane allocations (0-100 each). Empty
+## `shares` = SimBalance.DEFAULT_ALLOC (Standard 100%) — the legacy E1 call
+## sites (the draw preview) render the default allocation.
+func build(a: Vector3, b: Vector3, radius_scale := 1.0, shares: Array = []) -> void:
 	_a = a
 	_b = b
 	_radius_scale = radius_scale
-	_strand_count = clampi(strands, 3, 9)
+	if shares.is_empty():
+		shares = SimBalance.DEFAULT_ALLOC
+	_shares = [int(shares[0]), int(shares[1]), int(shares[2])]
 	_rebuild_mesh()
 	_rebuild_trestles()
 
 
-## Merged-bundle growth ("pop bigger"): fatter cable, visibly more strands.
-## Radius and strand count are capped so extreme pipe counts stay sane.
-func merged_params(count: int) -> Array:
-	return [minf(1.0 + 0.45 * float(count - 1), 2.2), mini(3 * count, 9)]
+## Path samples for the view's pick math (read-only).
+func get_path_samples() -> PackedVector3Array:
+	return _path
+
+
+## Path sample at normalized t in [0, 1] (a -> b), interpolated.
+func sample_at(t: float) -> Vector3:
+	var n := _path.size()
+	if n == 0:
+		return _a
+	var f := clampf(t, 0.0, 1.0) * float(n - 1)
+	var i := int(f)
+	if i >= n - 1:
+		return _path[n - 1]
+	return _path[i].lerp(_path[i + 1], f - float(i))
+
+
+## The world-space point on lane `lane`'s strand at normalized t — packet
+## dots ride exactly here (offset outward onto the strand surface).
+func strand_point(lane: int, t: float) -> Vector3:
+	var center := sample_at(t)
+	if center == _a and _path.is_empty():
+		return center
+	var axis := Geodesic.geodesic_axis(_path[0], _path[_path.size() - 1])
+	var u := center.normalized()
+	var ang := _lane_angle(lane)
+	var cable_r := BASE_RADIUS * _radius_scale
+	var ring := STRAND_RING * cable_r
+	var tube := _strand_thickness(lane) * cable_r * 0.46
+	return center + (u * cos(ang) + axis * sin(ang)) * (ring + tube)
+
+
+## Strand angular placement around the cable: lane order around the ring.
+func _lane_angle(lane: int) -> float:
+	return TAU * (float(lane) + 0.5) / 3.0
+
+
+func _strand_thickness(lane: int) -> float:
+	# share 100% -> 1.0; share 0% -> a hairline strand (the cable still reads
+	# as three strands even when a lane is unallocated)
+	var share := float(_shares[lane]) / 100.0
+	return share if share > 0.0 else HAIRLINE_FRAC
 
 
 func _rebuild_mesh() -> void:
-	var path := Geodesic.elevated_path(_a, _b, WorldSeed.PLANET_RADIUS, BASE_ELEVATION_FRAC * WorldSeed.PLANET_RADIUS * _radius_scale, SEGMENTS)
+	_path = Geodesic.elevated_path(_a, _b, WorldSeed.PLANET_RADIUS, BASE_ELEVATION_FRAC * WorldSeed.PLANET_RADIUS * _radius_scale, SEGMENTS)
 	var st := SurfaceTool.new()
 	st.begin(Mesh.PRIMITIVE_TRIANGLES)
 	var cable_r := BASE_RADIUS * _radius_scale
-	var strand_r := cable_r * 0.46
-	for i in _strand_count:
-		var ang := TAU * float(i) / float(_strand_count)
-		_append_strand(st, path, ang, STRAND_RING * cable_r, strand_r)
+	for lane in 3:
+		_append_strand(st, _lane_angle(lane), STRAND_RING * cable_r, _strand_thickness(lane) * cable_r * 0.46)
 	st.generate_normals()
 	var cable_mesh := ArrayMesh.new()
 	st.commit(cable_mesh) # ONE surface, ONE cable material
@@ -59,24 +103,24 @@ func _rebuild_mesh() -> void:
 	self.mesh = cable_mesh
 
 
-## One strand tube: `center_dir` places the strand axis around the cable
+## One strand tube: `center_ang` places the strand axis around the cable
 ## (angle on the {radial, plane-normal} circle), `ring` offsets the strand
 ## center, `tube_r` is the strand thickness.
-func _append_strand(st: SurfaceTool, path: PackedVector3Array, center_ang: float, ring: float, tube_r: float) -> void:
-	var axis := _path_plane_normal(path)
+func _append_strand(st: SurfaceTool, center_ang: float, ring: float, tube_r: float) -> void:
+	var axis := _path_plane_normal()
 	var cu := cos(center_ang)
 	var su := sin(center_ang)
-	var count := path.size()
+	var count := _path.size()
 	var centers := PackedVector3Array()
 	centers.resize(count)
 	for i in count:
-		var u := path[i].normalized()
-		centers[i] = path[i] + (u * cu + axis * su) * ring
+		var u := _path[i].normalized()
+		centers[i] = _path[i] + (u * cu + axis * su) * ring
 	# ring direction for angle a: du(a) = u*cos(a) + axis*sin(a) — smooth along
 	# the path by construction (u and axis are both exact great-circle vectors).
 	for i in count - 1:
-		var u0 := path[i].normalized()
-		var u1 := path[i + 1].normalized()
+		var u0 := _path[i].normalized()
+		var u1 := _path[i + 1].normalized()
 		for s in RADIAL:
 			var a0 := TAU * float(s) / float(RADIAL)
 			var a1 := TAU * float(s + 1) / float(RADIAL)
@@ -96,16 +140,15 @@ func _append_strand(st: SurfaceTool, path: PackedVector3Array, center_ang: float
 ## exactly the rotation axis `geodesic_points` rotates around (same function,
 ## same deterministic antipodal fallback), so the mesh frame can never twist
 ## against the path plane — even for near-antipodal arcs.
-func _path_plane_normal(path: PackedVector3Array) -> Vector3:
-	return Geodesic.geodesic_axis(path[0], path[path.size() - 1])
+func _path_plane_normal() -> Vector3:
+	return Geodesic.geodesic_axis(_path[0], _path[_path.size() - 1])
 
 
 func _rebuild_trestles() -> void:
 	for c in get_children():
 		c.queue_free()
-	var path := Geodesic.elevated_path(_a, _b, WorldSeed.PLANET_RADIUS, BASE_ELEVATION_FRAC * WorldSeed.PLANET_RADIUS * _radius_scale, SEGMENTS)
-	for i in range(TRESTLE_EVERY, path.size() - TRESTLE_EVERY, TRESTLE_EVERY):
-		var top := path[i]
+	for i in range(TRESTLE_EVERY, _path.size() - TRESTLE_EVERY, TRESTLE_EVERY):
+		var top := _path[i]
 		var base := top.normalized() * WorldSeed.PLANET_RADIUS
 		var post := MeshInstance3D.new()
 		var cyl := CylinderMesh.new()
diff --git a/scripts/planet.gd b/scripts/planet.gd
index 182cb66..f0ef74d 100644
--- a/scripts/planet.gd
+++ b/scripts/planet.gd
@@ -1,3 +1,4 @@
+@tool
 class_name Planet
 extends Node3D
 
diff --git a/scripts/qos_panel.gd b/scripts/qos_panel.gd
new file mode 100644
index 0000000..698df3e
--- /dev/null
+++ b/scripts/qos_panel.gd
@@ -0,0 +1,187 @@
+class_name QosPanel
+extends CanvasLayer
+
+## E2.3 — the QoS panel on pipe select. Shows the selected bundle's lanes
+## and lets the player allocate: the assignment ladder rungs (1 = 100%,
+## 2 = 70/30, 3 = 50/30/20 — data-driven from SimBalance) and per-class lane
+## assignment (email / streaming -> Express / Standard / Best-effort).
+## NOTHING auto-allocates: every change reaches the sim as one set_lanes
+## COMMAND applied by main — this panel never writes sim state itself.
+
+signal apply_requested(pipe_id: int, alloc: Array, cls_lane: Dictionary)
+
+var _pipe_id := -1
+var _alloc: Array = [0, 100, 0]
+var _cls_lane := {"email": 1, "streaming": 1}
+
+var _title := Label.new()
+var _sub := Label.new()
+var _rung_buttons: Array[Button] = []
+var _shares_label := Label.new()
+var _class_buttons := {}
+var _apply_btn := Button.new()
+
+
+func _ready() -> void:
+	visible = false
+	var panel := PanelContainer.new()
+	var style := StyleBoxFlat.new()
+	style.bg_color = Color(WorldSeed.COL_SPACE, 0.88)
+	style.corner_radius_top_left = 10
+	style.corner_radius_top_right = 10
+	style.corner_radius_bottom_left = 10
+	style.corner_radius_bottom_right = 10
+	style.content_margin_left = 16.0
+	style.content_margin_right = 16.0
+	style.content_margin_top = 12.0
+	style.content_margin_bottom = 12.0
+	panel.add_theme_stylebox_override("panel", style)
+	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER_RIGHT)
+	panel.position.x -= 340.0
+	panel.position.y = 90.0
+	add_child(panel)
+
+	var vbox := VBoxContainer.new()
+	vbox.custom_minimum_size = Vector2(300, 0)
+	vbox.add_theme_constant_override("separation", 10)
+	panel.add_child(vbox)
+
+	_title.add_theme_font_size_override("font_size", 18)
+	_title.add_theme_color_override("font_color", Color(0.92, 0.95, 0.98))
+	vbox.add_child(_title)
+	_sub.add_theme_font_size_override("font_size", 13)
+	_sub.add_theme_color_override("font_color", Color(0.75, 0.8, 0.86))
+	vbox.add_child(_sub)
+
+	vbox.add_child(_make_rule("LANES — assignment ladder"))
+	var rungs := HBoxContainer.new()
+	rungs.add_theme_constant_override("separation", 8)
+	vbox.add_child(rungs)
+	for rung in 3:
+		var b := Button.new()
+		b.text = "%d lane%s" % [rung + 1, "" if rung == 0 else "s"]
+		b.focus_mode = Control.FOCUS_NONE
+		b.pressed.connect(_on_rung.bind(rung + 1))
+		_rung_buttons.append(b)
+		rungs.add_child(b)
+	_shares_label.add_theme_font_size_override("font_size", 13)
+	_shares_label.add_theme_color_override("font_color", Color(0.75, 0.8, 0.86))
+	vbox.add_child(_shares_label)
+
+	for cls in SimBalance.CLASS_IDS:
+		vbox.add_child(_make_rule(_class_title(cls)))
+		var row := HBoxContainer.new()
+		row.add_theme_constant_override("separation", 8)
+		var dot := ColorRect.new()
+		dot.color = SimBalance.CLASSES[cls].color
+		dot.custom_minimum_size = Vector2(14, 14)
+		row.add_child(dot)
+		var b := Button.new()
+		b.focus_mode = Control.FOCUS_NONE
+		b.pressed.connect(_on_class_cycle.bind(cls))
+		_class_buttons[cls] = b
+		row.add_child(b)
+		vbox.add_child(row)
+
+	var buttons := HBoxContainer.new()
+	buttons.add_theme_constant_override("separation", 8)
+	buttons.alignment = BoxContainer.ALIGNMENT_END
+	_apply_btn.text = "Apply"
+	_apply_btn.focus_mode = Control.FOCUS_NONE
+	_apply_btn.pressed.connect(_on_apply)
+	buttons.add_child(_apply_btn)
+	var close := Button.new()
+	close.text = "Close"
+	close.focus_mode = Control.FOCUS_NONE
+	close.pressed.connect(close_panel)
+	buttons.add_child(close)
+	vbox.add_child(buttons)
+
+
+func _make_rule(text: String) -> Label:
+	var l := Label.new()
+	l.text = text
+	l.add_theme_font_size_override("font_size", 12)
+	l.add_theme_color_override("font_color", Color(0.55, 0.62, 0.7))
+	return l
+
+
+func _class_title(cls: String) -> String:
+	return cls.capitalize() + " rides"
+
+
+func open(pipe_id: int, sim: SimCore) -> void:
+	_pipe_id = pipe_id
+	var p: Dictionary = sim.pipes.get(pipe_id)
+	if p == null:
+		close_panel()
+		return
+	_alloc = (p.alloc as Array).duplicate()
+	_cls_lane = (p.cls_lane as Dictionary).duplicate()
+	var an: String = _node_name(p.a)
+	var bn: String = _node_name(p.b)
+	_title.text = "%s  <->  %s" % [an, bn]
+	_sub.text = "%s pipe x%d — %d u/s pooled" % [
+		p.tier.capitalize(), int(p.parallel),
+		int(SimBalance.TIERS[p.tier].capacity_u_s) * int(p.parallel),
+	]
+	_refresh()
+	visible = true
+
+
+func close_panel() -> void:
+	visible = false
+	_pipe_id = -1
+
+
+func _node_name(idx: int) -> String:
+	return "n%02d" % (idx + 1)
+
+
+func _on_rung(count: int) -> void:
+	_alloc = SimBalance.LADDER[count].duplicate()
+	# classes on newly-inactive lanes fall back to the highest active lane
+	for cls in _cls_lane:
+		if _alloc[int(_cls_lane[cls])] <= 0:
+			var lane := SimBalance.LANE_STANDARD
+			if _alloc[lane] <= 0:
+				lane = 0
+			_cls_lane[cls] = lane
+	_refresh()
+
+
+func _on_class_cycle(cls: String) -> void:
+	var order: Array[int] = []
+	for lane in 3:
+		if int(_alloc[lane]) > 0:
+			order.append(lane)
+	if order.is_empty():
+		return
+	var cur: int = order.find(int(_cls_lane[cls]))
+	_cls_lane[cls] = order[(cur + 1) % order.size()]
+	_refresh()
+
+
+func _on_apply() -> void:
+	if _pipe_id < 0:
+		return
+	apply_requested.emit(_pipe_id, _alloc.duplicate(), _cls_lane.duplicate())
+
+
+func _refresh() -> void:
+	for rung in 3:
+		_rung_buttons[rung].disabled = false
+	var active := 0
+	for lane in 3:
+		if int(_alloc[lane]) > 0:
+			active += 1
+	_rung_buttons[active - 1].disabled = true # pressed rung reads as disabled
+	var parts := PackedStringArray()
+	for lane in 3:
+		parts.append("%s %d%%" % [SimBalance.LANE_NAMES[lane], int(_alloc[lane])])
+	_shares_label.text = "  ·  ".join(parts)
+	for cls in _class_buttons:
+		var lane: int = int(_cls_lane[cls])
+		var btn: Button = _class_buttons[cls]
+		btn.text = SimBalance.LANE_NAMES[lane]
+		btn.disabled = int(_alloc[lane]) <= 0
diff --git a/scripts/qos_panel.gd.uid b/scripts/qos_panel.gd.uid
new file mode 100644
index 0000000..5334b0f
--- /dev/null
+++ b/scripts/qos_panel.gd.uid
@@ -0,0 +1 @@
+uid://b26m41jcklx8o
diff --git a/scripts/sim/sim_balance.gd b/scripts/sim/sim_balance.gd
new file mode 100644
index 0000000..7e41571
--- /dev/null
+++ b/scripts/sim/sim_balance.gd
@@ -0,0 +1,68 @@
+class_name SimBalance
+extends RefCounted
+
+## E2 balance data — the single data source for every sim tunable (the
+## "balance.json pattern": one diffable table, nothing scattered).
+##
+## Inherited canon (PP-Odin data/packet_types.json, the inheritance list):
+## email 2000 ms / 30 % loss, streaming 1200 ms / 10 % loss, both default to
+## the Standard lane; streaming costs double bandwidth (bandwidth_demand 2).
+## The capacity ladder is THIS GDD's Numerical Design (10/25/50/120 u/s).
+## `[ASSUMPTION: prototype tuning — rates, speeds, queue depth]`
+
+const TICK_HZ := 60 # fixed sim tick (stepped from the physics loop)
+const TICK_MS := 1000.0 / float(TICK_HZ)
+
+const MILLI := 1000 # 1 packet unit = 1000 milli-units (integer sim math)
+const PACKET_MILLI := {"email": 1000, "streaming": 2000} # bandwidth_demand canon
+
+# Pipe tiers (GDD M1 ladder). cost = routing cost per hop — fat is cheap
+# ("packets take the fattest route"), the capacity-cost spirit of the
+# PP-Odin 2026-08-13 ruling. Only `standard` is drawable in E2.
+const TIERS := {
+	"narrow": {"capacity_u_s": 10, "cost": 4, "drawable": false},
+	"standard": {"capacity_u_s": 25, "cost": 3, "drawable": true},
+	"wide": {"capacity_u_s": 50, "cost": 2, "drawable": false},
+	"backbone": {"capacity_u_s": 120, "cost": 1, "drawable": false},
+}
+const DRAW_TIER := "standard"
+
+# Packet classes. latency_tol_ms / max_loss_pct inherited from PP-Odin
+# packet_types.json; drop_priority = contention drop order (lowest drops
+# first — email tolerates loss, streaming does not); demand_mean_s = mean
+# spawn interval per terminal house (prototype rates — slice-1 scale).
+const CLASSES := {
+	"email": {
+		"latency_tol_ms": 2000, "max_loss_pct": 30,
+		"drop_priority": 0, "demand_mean_s": 6.0,
+		"color": Color("ffd166"),
+	},
+	"streaming": {
+		"latency_tol_ms": 1200, "max_loss_pct": 10,
+		"drop_priority": 1, "demand_mean_s": 2.0,
+		"color": Color("4aa3e8"),
+	},
+}
+const CLASS_IDS := ["email", "streaming"]
+
+# Class lanes (E2.3). Lane index order IS priority order: egress serializes
+# Express -> Standard -> Best-effort; strand speed follows the lane.
+const LANE_EXPRESS := 0
+const LANE_STANDARD := 1
+const LANE_BEST_EFFORT := 2
+const LANE_NAMES := ["Express", "Standard", "Best-effort"]
+const LANE_SPEED_MILLI := [200, 100, 60] # travel milli-units per tick, by lane (speed = priority)
+
+# The assignment ladder — 1 lane used = 100%, 2 = 70/30, 3 = 50/30/20
+# (Express/Standard/Best-effort shares, data-driven per canon).
+const LADDER := {
+	1: [0, 100, 0],
+	2: [70, 30, 0],
+	3: [50, 30, 20],
+}
+# Nothing auto-allocates: every fresh pipe carries Standard at 100% and
+# every class rides Standard until the player says otherwise.
+const DEFAULT_ALLOC := [0, 100, 0]
+const DEFAULT_CLASS_LANE := {"email": 1, "streaming": 1}
+
+const QUEUE_DEPTH := 6 # waiting packets per (pipe endpoint, lane)
diff --git a/scripts/sim/sim_balance.gd.uid b/scripts/sim/sim_balance.gd.uid
new file mode 100644
index 0000000..e840b35
--- /dev/null
+++ b/scripts/sim/sim_balance.gd.uid
@@ -0,0 +1 @@
+uid://bare270wmmhjl
diff --git a/scripts/sim/sim_core.gd b/scripts/sim/sim_core.gd
new file mode 100644
index 0000000..e529eea
--- /dev/null
+++ b/scripts/sim/sim_core.gd
@@ -0,0 +1,609 @@
+class_name SimCore
+extends RefCounted
+
+## E2.1/E2.2 — the deterministic flow simulation core (scene-free, view-free).
+##
+## Doctrine (carried from PP-Odin, mapped to Godot):
+## - Fixed tick, owned seed-derived streams (WorldSeed's splitmix family —
+##   stateless position-based draws, so there is no RNG cursor to serialize).
+## - Integer milli-unit state everywhere: byte-identity is exact, not
+##   float-fragile. Floats appear only ONCE per pipe (arc length from the
+##   seed-deterministic node geometry) and are frozen to int milli-units.
+## - Sim state mutates ONLY through apply_command() (the command bus) and
+##   step_tick(). The view layer reads; it never writes (pinned by
+##   tests/test_view_purity.gd).
+## - Junctions forward per-packet: path cost = static pipe-tier cost (fat is
+##   cheap); equal-cost next-hop sets split by the owned hash over
+##   (src, dst, class, pkt_id) — flow-pinned ECMP (GDD M3).
+## - Parallel pipes between the same pair merge into ONE pooled-capacity
+##   bundle (one sim link; the view renders it fatter). Link capacity is
+##   FULL-DUPLEX: each endpoint admits against the full pooled budget, so a
+##   bidirectionally saturated link carries ~2x — pinned by test_sim_flow's
+##   duplex test; a half-duplex change would be a deliberate re-decision.
+## - E2.3 class lanes: per-bundle 3-lane allocation + per-class lane
+##   assignment; admission serializes Express -> Standard -> Best-effort,
+##   work-conserving (unused higher-lane allowance flows down), reserves hold
+##   under saturation, contention drops lowest drop-precedence first.
+## - E2.5 SLA: per-class latency/loss counters; breach latches are
+##   STICKY-ENTER (inherited PP-Odin lesson: ratios dilute, latches must not
+##   chatter) and every drop is attributable (tick/pipe/node/class record).
+
+const INF_DIST := 0x7FFFFFFF
+const DROPS_CAP := 512
+const CMDS_CAP := 512
+
+var seed_value := 0
+var tick := 0
+
+var node_kind: Array[String] = []
+var node_pos: Array[Vector3] = []
+var node_is_house: Array[bool] = []
+
+var pipes := {} # id -> {id,a,b,tier,parallel,length_milli,alloc,cls_lane,accum,inflight_a,inflight_b}
+var next_pipe_id := 1
+var packets := {} # id -> {id,src,dst,cls,spawn_tick,state,pipe,end,lane,progress_milli}
+var next_packet_id := 1
+var spawn_count: Array[int] = []
+var queues := {} # pipe_id -> [endpoint][lane] -> Array[int] of packet ids
+
+var routes := {} # dst -> {dist: Array[int], hops: Dictionary node -> Array[int]}
+var _adj := {} # node -> Array[{pipe, other, cost}] (rebuilt on topology change)
+
+var sla := {} # class -> aggregate counters + sticky breach latches
+var drops: Array = [] # {tick,packet,cls,pipe,node,reason} — attributable
+var dropped_total := 0
+var node_admissions: Array[int] = [] # admitted this tick, per node (view: egress pulse)
+var command_log: Array = [] # {tick, cmd} — the replay spine (newest CMDS_CAP kept)
+var commands_total := 0 # every command ever applied (the log is a capped window)
+
+
+## `placements` = WorldSeed.node_placements() output ({name, pos, kind}).
+func setup(seed_value_: int, placements: Array) -> void:
+	seed_value = seed_value_
+	tick = 0
+	pipes.clear()
+	packets.clear()
+	queues.clear()
+	routes.clear()
+	_adj.clear()
+	sla.clear()
+	drops.clear()
+	dropped_total = 0
+	command_log.clear()
+	next_pipe_id = 1
+	next_packet_id = 1
+	node_kind.clear()
+	node_pos.clear()
+	node_is_house.clear()
+	spawn_count.clear()
+	node_admissions.clear()
+	for p in placements:
+		node_kind.append(p.kind)
+		node_pos.append(p.pos)
+		node_is_house.append(p.kind == "house")
+		spawn_count.append(0)
+		node_admissions.append(0)
+	for cls in SimBalance.CLASS_IDS:
+		sla[cls] = {
+			"delivered": 0, "dropped": 0, "latency_sum": 0,
+			"lat_breach": false, "lat_tick": -1,
+			"loss_breach": false, "loss_tick": -1, "events": [],
+		}
+
+
+# --- command bus -------------------------------------------------------------
+
+## The only way game code changes sim state. Topology: {"cmd":"add_pipe",
+## "a":i,"b":i}. QoS: {"cmd":"set_lanes","pipe":id,"alloc":[e,s,b],
+## "cls_lane":{"email":l,"streaming":l}}. Invalid commands are recorded and
+## ignored (deterministic no-ops) — the panel never sends one.
+func apply_command(cmd: Dictionary) -> void:
+	commands_total += 1
+	command_log.append({"tick": tick, "cmd": cmd.duplicate(true)})
+	if command_log.size() > CMDS_CAP:
+		command_log.pop_front() # newest window kept; total stays in the dump
+	match cmd.get("cmd", ""):
+		"add_pipe":
+			_cmd_add_pipe(cmd)
+		"set_lanes":
+			_cmd_set_lanes(cmd)
+
+
+func _cmd_add_pipe(cmd: Dictionary) -> void:
+	if not (cmd.has("a") and cmd.has("b")):
+		return
+	var a := int(cmd.a)
+	var b := int(cmd.b)
+	if a < 0 or b < 0 or a >= node_kind.size() or b >= node_kind.size() or a == b:
+		return
+	var existing = bundle_for_pair(a, b)
+	if existing != null:
+		existing.parallel += 1 # bundle: pooled capacity, same link
+		return
+	var id := next_pipe_id
+	next_pipe_id += 1
+	var tier: String = SimBalance.DRAW_TIER
+	var length_units := Geodesic.arc_length(node_pos[a], node_pos[b], WorldSeed.PLANET_RADIUS)
+	pipes[id] = {
+		"id": id, "a": a, "b": b, "tier": tier, "parallel": 1,
+		"length_milli": int(round(length_units * float(SimBalance.MILLI))),
+		"alloc": SimBalance.DEFAULT_ALLOC.duplicate(),
+		"cls_lane": SimBalance.DEFAULT_CLASS_LANE.duplicate(),
+		"accum": 0, "inflight_a": [], "inflight_b": [],
+		"credit": [[0, 0, 0], [0, 0, 0]],
+	}
+	queues[id] = [[[], [], []], [[], [], []]] # [endpoint][lane] -> packet ids
+	_rebuild_adj()
+	_rebuild_routes()
+
+
+func _cmd_set_lanes(cmd: Dictionary) -> void:
+	if not (cmd.has("pipe") and cmd.has("alloc") and cmd.has("cls_lane")):
+		return
+	var p = pipes.get(int(cmd.pipe))
+	if p == null:
+		return
+	var alloc: Array = cmd.alloc
+	if alloc.size() != 3:
+		return
+	var total := 0
+	for v in alloc:
+		var s := int(v)
+		if s < 0 or s > 100:
+			return
+		total += s
+	if total > 100:
+		return
+	var cls_lane: Dictionary = cmd.cls_lane
+	for cls in SimBalance.CLASS_IDS:
+		if not cls_lane.has(cls):
+			return
+		var lane := int(cls_lane[cls])
+		if lane < 0 or lane > 2 or alloc[lane] <= 0:
+			return # a class may only ride an ACTIVE (allocated) lane
+	p.alloc = [int(alloc[0]), int(alloc[1]), int(alloc[2])]
+	var mapped := {}
+	for cls2 in SimBalance.CLASS_IDS:
+		mapped[cls2] = int(cls_lane[cls2])
+	p.cls_lane = mapped
+	# A lane that just went inactive may still hold QUEUED packets — without
+	# this guard they would strand forever (an inactive lane's allowance
+	# decays to zero: never admitted, never dropped, invisible to SLA).
+	# Re-enqueue them in FIFO order; they re-route and re-lane onto ACTIVE
+	# lanes (overflow drops are recorded and attributable as usual).
+	# In-flight packets finish traversal on their admitted lane.
+	for endpoint in 2:
+		for lane in 3:
+			if int(p.alloc[lane]) > 0:
+				continue
+			var stranded: Array = queues[p.id][endpoint][lane]
+			while not stranded.is_empty():
+				var sid: int = stranded.pop_front()
+				var node: int = p.a if endpoint == 0 else p.b
+				_enqueue_at_node(sid, node)
+
+
+func bundle_for_pair(a: int, b: int):
+	for p in pipes.values():
+		if (p.a == a and p.b == b) or (p.a == b and p.b == a):
+			return p
+	return null
+
+
+func pipe_count(a: int, b: int) -> int:
+	var p = bundle_for_pair(a, b)
+	return int(p.parallel) if p != null else 0
+
+
+# --- the tick ----------------------------------------------------------------
+
+func step_tick() -> void:
+	tick += 1
+	for i in node_admissions.size():
+		node_admissions[i] = 0
+	_spawn_demand()
+	_admit_all()
+	_traverse_all()
+
+
+# Deterministic per-(node, class) demand: interval schedule + seeded phase +
+# seeded thinning + seeded destination. Stateless draws — no RNG cursor.
+# Demand only spawns when the destination is REACHABLE (unreachable demand
+# is not congestion — it must never poison the SLA counters).
+func _spawn_demand() -> void:
+	var houses: Array[int] = []
+	for i in node_is_house.size():
+		if node_is_house[i]:
+			houses.append(i)
+	if houses.size() < 2:
+		return
+	for n in node_is_house.size():
+		if not node_is_house[n]:
+			continue
+		for ci in SimBalance.CLASS_IDS.size():
+			var cls: String = SimBalance.CLASS_IDS[ci]
+			var interval := maxi(1, int(round(float(SimBalance.TICK_HZ) * float(SimBalance.CLASSES[cls].demand_mean_s))))
+			var phase := int(WorldSeed.unit_f(seed_value, 5_000_000 + n * 97 + ci * 7919) * float(interval))
+			if (tick + phase) % interval != 0:
+				continue
+			@warning_ignore("integer_division")
+			if WorldSeed.unit_f(seed_value, 6_000_000 + n * 97 + ci * 7919 + tick / interval) < 0.25:
+				continue # deterministic thinning — natural cadence, still seeded
+			var dst := _pick_destination(n, houses, spawn_count[n])
+			spawn_count[n] += 1
+			if dst < 0 or not _reachable(n, dst):
+				continue
+			_spawn_packet(n, dst, cls)
+
+
+func _pick_destination(n: int, houses: Array[int], counter: int) -> int:
+	var ci := 0 # destination salt is class-independent — one stream per node
+	var base := int(WorldSeed.unit_f(seed_value, 7_000_000 + n * 97 + ci * 7919 + counter * 31337) * float(houses.size()))
+	var dst: int = houses[base % houses.size()]
+	if dst == n:
+		dst = houses[(base + 1) % houses.size()]
+	return dst
+
+
+func _reachable(src: int, dst: int) -> bool:
+	var r = routes.get(dst)
+	return r != null and r.hops.has(src)
+
+
+## Test/harness staging door: the headless suite floods through here for
+## deterministic scenarios. Game code never calls it — demand comes from
+## _spawn_demand, mutations from apply_command.
+func _spawn_packet(src: int, dst: int, cls: String) -> void:
+	var id := next_packet_id
+	next_packet_id += 1
+	packets[id] = {
+		"id": id, "src": src, "dst": dst, "cls": cls, "spawn_tick": tick,
+		"state": 0, "pipe": -1, "end": 0, "lane": SimBalance.LANE_STANDARD,
+		"progress_milli": 0,
+	}
+	_enqueue_at_node(id, src)
+
+
+## Route + queue a packet currently waiting at `node`.
+func _enqueue_at_node(id: int, node: int) -> void:
+	var pkt: Dictionary = packets[id]
+	var pipe_id := _pick_next_pipe(pkt.src, pkt.dst, pkt.cls, id, node)
+	if pipe_id < 0:
+		_drop(id, node, "no_route")
+		return
+	var p: Dictionary = pipes[pipe_id]
+	var endpoint: int = 0 if p.a == node else 1
+	var lane := _lane_for(p, pkt.cls)
+	pkt.pipe = pipe_id
+	pkt.end = endpoint
+	pkt.lane = lane
+	pkt.state = 0
+	var q: Array = queues[pipe_id][endpoint][lane]
+	if q.size() >= SimBalance.QUEUE_DEPTH:
+		_drop_overflow(pipe_id, endpoint, lane, id)
+		return
+	q.append(id)
+
+
+## The lane this bundle carries `cls` on right now.
+func _lane_for(p: Dictionary, cls: String) -> int:
+	return int(p.cls_lane.get(cls, SimBalance.LANE_STANDARD))
+
+## ECMP: among the equal-cost next-hop bundles at `node`, the owned hash over
+## (src, dst, class, pkt_id) picks per packet — flow-pinned (GDD M3).
+func _pick_next_pipe(src: int, dst: int, cls: String, pkt_id: int, node: int) -> int:
+	# UNTYPED on purpose: routes.get(missing) yields null, and a typed
+	# Dictionary local throws a SCRIPT ERROR on the assignment itself —
+	# which silently aborted callers and left the null guard below dead.
+	var r = routes.get(dst)
+	if r == null:
+		return -1
+	var options: Array = r.hops.get(node, [])
+	if options.is_empty():
+		return -1
+	if options.size() == 1:
+		return options[0]
+	var ci := SimBalance.CLASS_IDS.find(cls)
+	var h := WorldSeed.hash_i32(WorldSeed.hash_i32(WorldSeed.hash_i32(WorldSeed.hash_i32(0x9E3779B9 ^ src) ^ dst) ^ ci) ^ pkt_id)
+	return options[(h & 0x7FFFFFFF) % options.size()]
+
+
+## E2.4 — serialization: per bundle endpoint, lanes drain Express ->
+## Standard -> Best-effort. Each lane banks its reserved share into a
+## persistent credit (deficit-style — otherwise a 1000-milli packet could
+## never cross a 416-milli/tick reserve); an EMPTY lane flushes its whole
+## credit downward (work-conserving gap-filling), so under saturation every
+## lane is held to ≈ its reserve (E2.3 reservation) while IDLE lanes donate
+## their whole reserve downward. Unspendable allowance stays BANKED in its
+## own lane's credit — it never skips the ladder; only idle lanes flush.
+func _admit_all() -> void:
+	var ids := pipes.keys()
+	ids.sort()
+	for pid in ids:
+		var p: Dictionary = pipes[pid]
+		# integer per-tick budget with a persistent remainder accumulator:
+		# pooled_units*1000 milli per second, distributed over TICK_HZ ticks.
+		var pooled_units := int(SimBalance.TIERS[p.tier].capacity_u_s) * int(p.parallel)
+		@warning_ignore("integer_division")
+		var budget := pooled_units * SimBalance.MILLI / SimBalance.TICK_HZ
+		p.accum = int(p.accum) + pooled_units * SimBalance.MILLI % SimBalance.TICK_HZ
+		if int(p.accum) >= SimBalance.TICK_HZ:
+			p.accum = int(p.accum) - SimBalance.TICK_HZ
+			budget += 1
+		for endpoint in 2:
+			var carry_down := 0
+			for lane in 3:
+				@warning_ignore("integer_division")
+				var reserve := budget * int(p.alloc[lane]) / 100
+				var q: Array = queues[pid][endpoint][lane]
+				if q.is_empty():
+					# idle lane: flush the whole credit down the ladder
+					carry_down += int(p.credit[endpoint][lane]) + reserve
+					p.credit[endpoint][lane] = 0
+					continue
+				# The bank IS the allowance: banked credit from earlier ticks
+				# spends in bursts (deficit scheduling) — capping it at the
+				# per-tick budget would strand any packet larger than one
+				# tick's reserve forever. Long-run rates stay = reserves
+				# because the bank only fills from per-tick reserves.
+				var allowance := int(p.credit[endpoint][lane]) + reserve + carry_down
+				carry_down = 0
+				var used := 0
+				while not q.is_empty():
+					var milli := int(SimBalance.PACKET_MILLI[packets[q[0]].cls])
+					if used + milli > allowance:
+						break
+					var id: int = q.pop_front()
+					_admit(p, endpoint, id)
+					used += milli
+				p.credit[endpoint][lane] = allowance - used
+				# surplus a lane could not spend stays banked in its credit —
+				# it never skips the ladder (no flow UP)
+
+
+func _admit(p: Dictionary, endpoint: int, id: int) -> void:
+	var pkt: Dictionary = packets[id]
+	pkt.state = 1
+	pkt.progress_milli = 0
+	var inflight: Array = p.inflight_a if endpoint == 0 else p.inflight_b
+	inflight.append(id)
+	var node: int = p.a if endpoint == 0 else p.b
+	node_admissions[node] += 1
+
+
+## In-flight traversal: progress advances by lane speed (strand speed =
+## priority); arrival delivers (SLA) or hands the packet to the far node.
+func _traverse_all() -> void:
+	var ids := pipes.keys()
+	ids.sort()
+	var arrivals: Array = [] # [pipe_id, endpoint, packet_id]
+	for pid in ids:
+		var p: Dictionary = pipes[pid]
+		for endpoint in 2:
+			var inflight: Array = p.inflight_a if endpoint == 0 else p.inflight_b
+			var keep: Array = []
+			for id in inflight:
+				var pkt: Dictionary = packets[id]
+				pkt.progress_milli = int(pkt.progress_milli) + SimBalance.LANE_SPEED_MILLI[int(pkt.lane)]
+				if int(pkt.progress_milli) >= int(p.length_milli):
+					arrivals.append([pid, endpoint, id])
+				else:
+					keep.append(id)
+			if endpoint == 0:
+				p.inflight_a = keep
+			else:
+				p.inflight_b = keep
+	for arr in arrivals:
+		_arrive(arr[0], arr[1], arr[2])
+
+
+func _arrive(pipe_id: int, endpoint: int, id: int) -> void:
+	var p: Dictionary = pipes[pipe_id]
+	var node: int = p.b if endpoint == 0 else p.a
+	var pkt: Dictionary = packets[id]
+	if pkt.dst == node:
+		packets.erase(id)
+		_delivered(pkt, pipe_id, node)
+	else:
+		_enqueue_at_node(id, node)
+
+
+func _delivered(pkt: Dictionary, pipe_id: int, node: int) -> void:
+	var s: Dictionary = sla[pkt.cls]
+	s.delivered = int(s.delivered) + 1
+	var latency := tick - int(pkt.spawn_tick)
+	s.latency_sum = int(s.latency_sum) + latency
+	if latency > _latency_tol_ticks(pkt.cls) and not bool(s.lat_breach):
+		# Attributable like every drop: the breach latches at the delivery
+		# through a specific pipe at a specific node (the A1 contract).
+		s.lat_breach = true
+		s.lat_tick = tick
+		s.events.append({"tick": tick, "kind": "latency", "pipe": pipe_id, "node": node})
+
+
+func _drop(id: int, node: int, reason: String) -> void:
+	var pkt: Dictionary = packets.get(id)
+	if pkt == null:
+		return
+	packets.erase(id)
+	_record_drop(pkt, -1, node, reason)
+
+
+## Queue overflow: contention drops by drop precedence — lowest drops first;
+## ties break to the lowest packet id (oldest of its class). The newcomer
+## competes with the queued packets and may be the victim.
+func _drop_overflow(pipe_id: int, endpoint: int, lane: int, newcomer: int) -> void:
+	var p: Dictionary = pipes[pipe_id]
+	var q: Array = queues[pipe_id][endpoint][lane]
+	var victim := newcomer
+	for id in q:
+		if _is_lower_rank(id, victim):
+			victim = id
+	var node: int = p.a if endpoint == 0 else p.b
+	if victim == newcomer:
+		var npkt: Dictionary = packets[newcomer]
+		packets.erase(newcomer)
+		_record_drop(npkt, pipe_id, node, "queue_overflow")
+		return
+	q.erase(victim)
+	var vpkt: Dictionary = packets[victim]
+	packets.erase(victim)
+	_record_drop(vpkt, pipe_id, node, "queue_overflow")
+	q.append(newcomer)
+
+
+## True when packet `a` ranks lower (drops earlier) than `b`: drop priority
+## first, then packet id (oldest of its class). Tuple compare — a packed
+## int would overflow the priority band once ids exceed 2^30.
+func _is_lower_rank(a: int, b: int) -> bool:
+	var pa := int(SimBalance.CLASSES[packets[a].cls].drop_priority)
+	var pb := int(SimBalance.CLASSES[packets[b].cls].drop_priority)
+	if pa != pb:
+		return pa < pb
+	return a < b
+
+
+func _record_drop(pkt: Dictionary, pipe_id: int, node: int, reason: String) -> void:
+	dropped_total += 1
+	if drops.size() >= DROPS_CAP:
+		drops.pop_front()
+	drops.append({
+		"tick": tick, "packet": int(pkt.id), "cls": pkt.cls,
+		"pipe": pipe_id, "node": node, "reason": reason,
+	})
+	var s: Dictionary = sla[pkt.cls]
+	s.dropped = int(s.dropped) + 1
+	var denom := int(s.dropped) + int(s.delivered)
+	if denom > 0:
+		@warning_ignore("integer_division")
+		var pct := int(s.dropped) * 100 / denom
+		if pct > int(SimBalance.CLASSES[pkt.cls].max_loss_pct) and not bool(s.loss_breach):
+			s.loss_breach = true
+			s.loss_tick = tick
+			s.events.append({"tick": tick, "kind": "loss", "pipe": pipe_id, "node": node})
+
+
+# --- routing (derived state — rebuilt on topology change only) ---------------
+
+func _rebuild_adj() -> void:
+	_adj.clear()
+	for i in node_kind.size():
+		_adj[i] = []
+	var ids := pipes.keys()
+	ids.sort()
+	for pid in ids:
+		var p: Dictionary = pipes[pid]
+		var cost := int(SimBalance.TIERS[p.tier].cost)
+		_adj[p.a].append({"pipe": pid, "other": p.b, "cost": cost})
+		_adj[p.b].append({"pipe": pid, "other": p.a, "cost": cost})
+
+
+## Destination-rooted Dijkstra with integer hop costs; equal-cost next-hop
+## sets stored per node (options iterated in ascending pipe id — sorted _adj).
+func _rebuild_routes() -> void:
+	routes.clear()
+	var n := node_kind.size()
+	for dst in n:
+		var dist: Array[int] = []
+		dist.resize(n)
+		dist.fill(INF_DIST)
+		dist[dst] = 0
+		var visited: Array[bool] = []
+		visited.resize(n)
+		visited.fill(false)
+		for _i in n:
+			var u := -1
+			var best := INF_DIST
+			for v in n:
+				if not visited[v] and dist[v] < best:
+					best = dist[v]
+					u = v
+			if u < 0:
+				break
+			visited[u] = true
+			for edge in _adj[u]:
+				var nd: int = dist[u] + int(edge.cost)
+				if nd < dist[edge.other]:
+					dist[edge.other] = nd
+		var hops := {}
+		for v in n:
+			if v == dst or dist[v] >= INF_DIST:
+				continue
+			var options: Array[int] = []
+			for edge in _adj[v]:
+				if dist[v] == dist[edge.other] + int(edge.cost):
+					options.append(edge.pipe)
+			if not options.is_empty():
+				hops[v] = options
+		routes[dst] = {"dist": dist, "hops": hops}
+
+
+# --- SLA helpers --------------------------------------------------------------
+
+func _latency_tol_ticks(cls: String) -> int:
+	return int(ceil(float(SimBalance.CLASSES[cls].latency_tol_ms) / SimBalance.TICK_MS))
+
+
+# --- canonical state / replay hash --------------------------------------------
+
+## Deterministic canonical serialization: sorted ids, fixed field order,
+## integers only. Two sims with the same seed + command stream produce
+## byte-identical dumps at every tick (the E2 replay contract).
+func dump_state() -> String:
+	var out := PackedStringArray()
+	out.append("pp3d-e2|v1|%d|%d|%d|%d" % [seed_value, tick, next_pipe_id, next_packet_id])
+	var ids := pipes.keys()
+	ids.sort()
+	for pid in ids:
+		var p: Dictionary = pipes[pid]
+		out.append("P|%d|%d|%d|%s|%d|%d|%d,%d,%d|%d,%d|%d|%s|%s|%s|%s" % [
+			p.id, p.a, p.b, p.tier, p.parallel, p.length_milli,
+			p.alloc[0], p.alloc[1], p.alloc[2],
+			p.cls_lane["email"], p.cls_lane["streaming"], p.accum,
+			_join_ids(p.inflight_a), _join_ids(p.inflight_b),
+			_join_ids(p.credit[0]), _join_ids(p.credit[1]),
+		])
+		for endpoint in 2:
+			for lane in 3:
+				out.append("Q|%d|%d|%d|%s" % [pid, endpoint, lane, _join_ids(queues[pid][endpoint][lane])])
+	var pids := packets.keys()
+	pids.sort()
+	for id in pids:
+		var k: Dictionary = packets[id]
+		out.append("K|%d|%d|%d|%s|%d|%d|%d|%d|%d|%d" % [
+			id, k.src, k.dst, k.cls, k.spawn_tick, k.state, k.pipe, k.end, k.lane, k.progress_milli,
+		])
+	for i in spawn_count.size():
+		out.append("S|%d|%d" % [i, spawn_count[i]])
+	for cls in SimBalance.CLASS_IDS:
+		var s: Dictionary = sla[cls]
+		out.append("L|%s|%d|%d|%d|%s|%d|%s|%d" % [
+			cls, s.delivered, s.dropped, s.latency_sum,
+			"1" if s.lat_breach else "0", s.lat_tick,
+			"1" if s.loss_breach else "0", s.loss_tick,
+		])
+	out.append("D|%d|%d" % [dropped_total, drops.size()])
+	for d in drops:
+		out.append("d|%d|%d|%s|%d|%d|%s" % [d.tick, d.packet, d.cls, d.pipe, d.node, d.reason])
+	out.append("C|%d|%d" % [commands_total, command_log.size()])
+	for c in command_log:
+		out.append("c|%d|%s" % [c.tick, var_to_str(c.cmd)])
+	return "|".join(out)
+
+
+func state_hash() -> int:
+	var dump := dump_state()
+	var h := 0x811C9DC5
+	for b in dump.to_utf8_buffer():
+		h = h ^ int(b)
+		h = (h * 0x01000193) & 0xFFFFFFFF
+	return h
+
+
+static func _join_ids(arr: Array) -> String:
+	if arr.is_empty():
+		return "-"
+	var parts := PackedStringArray()
+	for v in arr:
+		parts.append(str(int(v)))
+	return ".".join(parts)
diff --git a/scripts/sim/sim_core.gd.uid b/scripts/sim/sim_core.gd.uid
new file mode 100644
index 0000000..4cbd65c
--- /dev/null
+++ b/scripts/sim/sim_core.gd.uid
@@ -0,0 +1 @@
+uid://bfr2hcgk65t1g
diff --git a/tools/determinism_log.gd b/tools/determinism_log.gd
new file mode 100644
index 0000000..2b66e5c
--- /dev/null
+++ b/tools/determinism_log.gd
@@ -0,0 +1,56 @@
+extends SceneTree
+
+## E2 capture (A2): the replay-determinism log. Two fresh SimCore instances,
+## same seed, identical command streams (topology + a set_lanes override),
+## stepped in lockstep — per-tick hash samples + a MATCH verdict, written to
+## captures/05-replay-determinism.txt. Run headless:
+##   godot --headless -s res://tools/determinism_log.gd
+## (Command stream + tick count: REPLAY_CMDS / REPLAY_TICKS in
+## tests/test_sim_base.gd — ONE definition shared with the replay test.)
+
+func _initialize() -> void:
+	process_frame.connect(_go, CONNECT_ONE_SHOT)
+
+
+func _go() -> void:
+	var base = load("res://tests/test_sim_base.gd")
+	var cmds = base.REPLAY_CMDS
+	var ticks = base.REPLAY_TICKS
+	var inject_tick = base.REPLAY_INJECT_TICK
+	var a := SimCore.new()
+	var b := SimCore.new()
+	a.setup(20260904, WorldSeed.node_placements(20260904, WorldSeed.wedge_layout(20260904)))
+	b.setup(20260904, WorldSeed.node_placements(20260904, WorldSeed.wedge_layout(20260904)))
+	var lines := PackedStringArray()
+	lines.append("Packet Plumber 3D — E2 replay determinism (the A1 contract)")
+	lines.append("seed=%d ticks=%d commands=%d (three-wedge network + a 50/30/20 set_lanes)" % [20260904, ticks, cmds.size()])
+	lines.append("run A / run B: two fresh SimCore instances, identical command streams,")
+	lines.append("stepped in lockstep; hash = fnv1a over the canonical integer state dump.")
+	lines.append("")
+	var identical := true
+	for t in ticks:
+		if t == inject_tick:
+			for c in cmds:
+				a.apply_command(c)
+				b.apply_command(c)
+		a.step_tick()
+		b.step_tick()
+		var ha := a.state_hash()
+		var hb := b.state_hash()
+		if t % 60 == 0 or ha != hb:
+			lines.append("tick %3d   hashA %08x   hashB %08x   %s" % [t, ha, hb, "MATCH" if ha == hb else "DIFFER"])
+		if ha != hb:
+			identical = false
+	lines.append("")
+	lines.append("final state dumps byte-identical: %s" % ("YES" if a.dump_state() == b.dump_state() else "NO"))
+	lines.append("traffic carried: %d packets delivered across the run" % (int(a.sla["email"].delivered) + int(a.sla["streaming"].delivered)))
+	lines.append("VERDICT: %s" % ("PASS — replay byte-identity holds on the fixed seed" if identical else "FAIL — sims diverged"))
+	var f := FileAccess.open("res://captures/05-replay-determinism.txt", FileAccess.WRITE)
+	if f == null:
+		printerr("determinism log: cannot open captures/05-replay-determinism.txt (err %d)" % FileAccess.get_open_error())
+		quit(1)
+		return
+	f.store_string("\n".join(lines) + "\n")
+	f.close()
+	print("determinism log written (%s)" % ("PASS" if identical else "FAIL"))
+	quit(0 if identical else 1)
diff --git a/tools/determinism_log.gd.uid b/tools/determinism_log.gd.uid
new file mode 100644
index 0000000..45106e3
--- /dev/null
+++ b/tools/determinism_log.gd.uid
@@ -0,0 +1 @@
+uid://dxoj2sjq2lcfo

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

--- ISOLATION (binding) ---
You are the BLIND lens: reading anything beyond the diff above (repo files, specs, other docs) INVALIDATES your review. Work from the diff text only.


--- CHUNKING DISCLOSURE ---
This PR's diff (4240 lines) was split into 2 file-group chunks per the big-diff policy; you are reviewing chunk 1 of 2 — the RUNTIME CODE: scripts/, scenes/, tools/ (19 files, 1938 lines). The other chunk is reviewed by a sibling wave. Do NOT report the other chunk's content as missing — its absence from your DIFF section is an artifact of chunking, not a PR defect.


--- FILE-OUTPUT CONTRACT (headless round) ---
Write ONLY your JSON array to this exact absolute path (do not derive it, do not write anywhere else):
/Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e2-flow-qos/r3/blind-c1.json
The file must contain the JSON array and nothing else. Then stop.
