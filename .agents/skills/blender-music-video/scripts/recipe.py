"""Neutral native building helpers and ONE configurable radial-relief recipe.
New concepts can use these helpers or enter through an approved .blend scene.
"""

import bpy, math
from mathutils import Vector


def linear_hex(value):
    rgb = [int(value[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(
        x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb
    )


def material(name, colour, metal=0, roughness=0.35, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    rgb = linear_hex(colour)
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = roughness
    if emission:
        p.inputs["Emission Color"].default_value = (*rgb, 1)
        p.inputs["Emission Strength"].default_value = emission
    return m


def link(scene, obj):
    scene.collection.objects.link(obj)
    return obj


def box(scene, name, size, location, mat, bevel=0.04):
    x, y, z = [v / 2 for v in size]
    verts = [(a, b, c) for a in (-x, x) for b in (-y, y) for c in (-z, z)]
    faces = [
        (0, 4, 6, 2),
        (1, 3, 7, 5),
        (0, 1, 5, 4),
        (2, 6, 7, 3),
        (0, 2, 3, 1),
        (4, 5, 7, 6),
    ]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], [tuple(reversed(f)) for f in faces])
    mesh.update()
    o = link(scene, bpy.data.objects.new(name, mesh))
    o.location = location
    o.data.materials.append(mat)
    if bevel:
        b = o.modifiers.new("Crafted edges", "BEVEL")
        b.width = bevel
        b.segments = 3
    return o


def annulus(scene, name, inner, outer, z, depth, mat, segments=96):
    verts = []
    for h in [z, z + depth]:
        for radius in [inner, outer]:
            verts.extend(
                (
                    radius * math.cos(i * 2 * math.pi / segments),
                    radius * math.sin(i * 2 * math.pi / segments),
                    h,
                )
                for i in range(segments)
            )
    faces = []
    n = segments
    for i in range(n):
        j = (i + 1) % n
        faces.extend(
            [
                (i, j, n + j, n + i),
                (2 * n + i, 3 * n + i, 3 * n + j, 2 * n + j),
                (i, 2 * n + i, 2 * n + j, j),
                (n + i, n + j, 3 * n + j, 3 * n + i),
            ]
        )
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = link(scene, bpy.data.objects.new(name, mesh))
    o.data.materials.append(mat)
    b = o.modifiers.new("Rim bevel", "BEVEL")
    b.width = 0.025
    b.segments = 3
    return o


def periodic(obj, path, index, expression):
    if len(expression) > 240:
        raise ValueError("Native driver expression too long; use property targets")
    f = obj.driver_add(path, index)
    f.driver.type = "SCRIPTED"
    f.driver.expression = expression
    return f


def area(scene, name, colour, watts, location, size=4):
    data = bpy.data.lights.new(name, "AREA")
    data.color = linear_hex(colour)
    data.energy = watts
    data.shape = "DISK"
    data.size = size
    o = link(scene, bpy.data.objects.new(name, data))
    o.location = location
    o.rotation_euler = (
        (Vector((0, 0, 0.3)) - o.location).to_track_quat("-Z", "Y").to_euler()
    )
    return o


def build(c):
    name = "Kinetic artwork / " + c["title"]
    assert name not in bpy.data.scenes, "Never replace an existing scene"
    s = bpy.data.scenes.new(name)
    bpy.context.window.scene = s
    s.render.engine = "BLENDER_EEVEE"
    s.world = bpy.data.worlds.new(name + " / World")
    s.world.use_nodes = True
    s.world.node_tree.nodes["Background"].inputs[0].default_value = (
        0.025,
        0.025,
        0.025,
        1,
    )
    s.world.node_tree.nodes["Background"].inputs[1].default_value = 0.25
    p = c["art"]["palette"]
    shell = material("Shell", p["shell"], 0.72, 0.3)
    accent = material("Accent", p["accent"], 0.68, 0.27)
    dark = material("Neutral plinth", "#111214", 0.25, 0.46)
    core = material("Diffuser", p["accent"], 0, 0.6, 0.4)
    n = c["loop"]["frames"]
    phase = f"(2*pi*(frame-1)/{n})"
    count = c["art"].get("segments", 12)
    annulus(s, "Plinth", 0.01, 2.65, -0.4, 0.32, dark)
    annulus(s, "Fixed rim", 2.34, 2.53, -0.02, 0.12, shell)
    annulus(s, "Centre", 0.01, 0.72, -0.02, 0.07, core)
    rotor = link(s, bpy.data.objects.new("Periodic rotor", None))
    periodic(rotor, "rotation_euler", 2, phase)
    for i in range(count):
        angle = 2 * math.pi * i / count
        pivot = link(s, bpy.data.objects.new(f"Petal hinge {i:02}", None))
        pivot.parent = rotor
        pivot.location = (1.46 * math.cos(angle), 1.46 * math.sin(angle), 0.12)
        pivot.rotation_euler.z = angle
        petal = box(
            s,
            f"Relief petal {i:02}",
            (1.34, 0.42, 0.11),
            (0, 0, 0),
            accent if i == 0 else shell,
        )
        petal.parent = pivot
        periodic(pivot, "rotation_euler", 1, f".18+.23*sin({phase}+{angle:.6f})")
    box(s, "Ground", (200, 200, 0.1), (0, 0, -0.51), dark, 0)
    light = area(s, "Key", p["key"], c["art"]["key_watts"], (1, -3, 6), 5)
    orbit = link(s, bpy.data.objects.new("Light orbit", None))
    light.parent = orbit
    periodic(orbit, "rotation_euler", 2, "-" + phase)
    area(s, "Rim", p["rim"], c["art"]["rim_watts"], (-3, 2, 4), 3)
    area(s, "Fill", p["key"], c["art"]["key_watts"] * 0.2, (3, -4, 3), 5)
    camera = link(
        s,
        bpy.data.objects.new("Artwork camera", bpy.data.cameras.new("Artwork camera")),
    )
    camera.location = (4, -6, 7)
    camera.rotation_euler = (
        (Vector((0, 0, 0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    )
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 9
    s.camera = camera
    s.display_settings.display_device = "sRGB"
    s.view_settings.view_transform = "AgX"
    s.view_settings.look = "AgX - Medium High Contrast"
    s.view_settings.exposure = 0
    s.view_settings.gamma = 1
    s.frame_start = 1
    s.frame_end = n
    s["theme"] = c["art"]["theme"]
    s["direction"] = c["art"]["direction"]
    s["palette_rationale"] = c["art"]["palette_rationale"]
    s["recipe"] = "radial-relief"
    return s
