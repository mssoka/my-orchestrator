"""Finite native Blender workers. Rendering/encoding happens HERE, never in FFmpeg CLI.
Do not run this worker entry point in a live user document. recipe.py helpers are live-safe.
"""

import bpy, json, sys, os, time, math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import digest, save, require
from srgb_metadata import repair
from recipe import build


def activate(s):
    bpy.context.window.scene = s
    if s.sequence_editor:
        for w in bpy.data.workspaces:
            if hasattr(w, "sequencer_scene"):
                w.sequencer_scene = s


def scene_file(s, path):
    require(bpy.app.background, "Never clear/reopen a live user document")
    require(not path.exists(), "Refuse native source overwrite")
    name = s.name
    bpy.data.libraries.write(
        str(path), {s}, fake_user=True, compress=True, path_remap="ABSOLUTE"
    )
    bpy.ops.wm.open_mainfile(filepath=str(path))
    s = bpy.data.scenes[name]
    activate(s)
    for other in list(bpy.data.scenes):
        if other != s and not other.objects and not other.sequence_editor:
            bpy.data.scenes.remove(other)
    if s.sequence_editor:
        for strip in s.sequence_editor.strips:
            if strip.type == "MOVIE":
                strip.filepath = "//" + os.path.relpath(
                    bpy.path.abspath(strip.filepath), path.parent
                )
        template = (
            Path(bpy.utils.resource_path("LOCAL"))
            / "scripts/startup/bl_app_templates_system/Video_Editing/startup.blend"
        )
        if template.exists():
            with bpy.data.libraries.load(str(template), link=False) as (data, loaded):
                loaded.workspaces = [n for n in data.workspaces if n == "Video Editing"]
            if loaded.workspaces:
                w = loaded.workspaces[0]
                w.name = "Native music video"
                w.sequencer_scene = s
                bpy.context.window.workspace = w
        activate(s)
        # Never use screen/view2d UI operators headlessly. Fit the view in the live GUI.
    bpy.ops.wm.save_as_mainfile(filepath=str(path), compress=True)
    return s


def dimensions(s, c, percent=100):
    s.render.resolution_x = c["video"]["width"]
    s.render.resolution_y = c["video"]["height"]
    s.render.resolution_percentage = percent
    s.render.fps = c["video"]["fps"]
    s.render.fps_base = 1


def video(s, c, audio=False):
    settings = s.render.image_settings
    settings.media_type = "VIDEO"
    settings.file_format = "FFMPEG"
    settings.color_mode = "RGB"
    settings.color_depth = "8"
    settings.color_management = "FOLLOW_SCENE"
    f = s.render.ffmpeg
    f.format = "MPEG4"
    f.codec = "H264"
    f.constant_rate_factor = "CUSTOM"
    f.custom_constant_rate_factor = c["video"].get("crf", 16)
    f.ffmpeg_preset = "GOOD"
    f.gopsize = c["video"]["fps"] * 2
    f.use_max_b_frames = True
    f.max_b_frames = 2
    f.audio_codec = "AAC" if audio else "NONE"
    if audio:
        f.audio_bitrate = 320
        f.audio_mixrate = FACTS["audio_rate"]
        f.audio_channels = "STEREO"
        f.audio_volume = 1


def still(s, path, fmt="PNG", depth="8"):
    require(not path.exists(), "Refuse still overwrite")
    s.render.image_settings.media_type = "IMAGE"
    s.render.image_settings.file_format = fmt
    s.render.image_settings.color_mode = "RGB"
    s.render.image_settings.color_depth = depth
    s.render.image_settings.quality = 92
    s.render.filepath = str(path)
    bpy.ops.render.render(write_still=True, scene=s.name)


def render_movie(s, path, start, end, c, audio=False):
    require(not path.exists(), "Refuse movie overwrite")
    require(
        s.display_settings.display_device == "sRGB",
        "Only measured sRGB display output is supported",
    )
    video(s, c, audio)
    s.frame_start = start
    s.frame_end = end
    s.render.filepath = str(path)
    activate(s)
    bpy.ops.render.render(animation=True, scene=s.name)
    require(path.is_file() and path.stat().st_size > 1000, "No native movie")
    metadata = repair(path, ROOT)
    save(path.with_suffix(".metadata.json"), metadata)


def art_scene(c):
    if c["art"]["mode"] == "recipe":
        s = build(c)
    else:
        s = bpy.data.scenes.get(c["art"]["scene_name"])
        require(s is not None, "Native scene name missing")
        activate(s)
        require(s.camera is not None, "Approved artwork needs its camera")
        require(
            s.sequence_editor is None
            and not any(o.type == "SPEAKER" for o in s.objects),
            "Artwork intake must be a3D scene without VSE/speaker audio; use loop intake for baked edits",
        )
        require(
            not s.render.film_transparent
            and s.render.pixel_aspect_x == s.render.pixel_aspect_y,
            "Opaque square-pixel artwork required; do not silently composite or squeeze",
        )
        require(
            s.render.resolution_x * 9 == s.render.resolution_y * 16,
            "Do not silently change an approved camera aspect",
        )
        for dependency in bpy.utils.blend_paths(
            absolute=True, packed=False, local=False
        ):
            require(
                Path(dependency).is_file(),
                f"Missing/special native dependency: {dependency}",
            )
    require(
        s.display_settings.display_device == "sRGB"
        and s.render.image_settings.color_management == "FOLLOW_SCENE",
        "Approved scene requires a validated sRGB/FOLLOW_SCENE output view",
    )
    s["native_mv_theme"] = c["art"]["theme"]
    s["native_mv_rationale"] = c["art"]["palette_rationale"]
    dimensions(s, c)
    if hasattr(s, "eevee"):
        s.eevee.taa_render_samples = c["video"].get("samples", 32)
    return s


def edit_scene(c, loop, frames, name):
    require(name not in bpy.data.scenes, "Refuse scene replacement")
    s = bpy.data.scenes.new(name)
    activate(s)
    dimensions(s, c)
    s.frame_start = 1
    s.frame_end = frames
    s.sync_mode = "AUDIO_SYNC"
    s.render.use_sequencer = True
    s.display_settings.display_device = "sRGB"
    s.view_settings.view_transform = "Standard"
    s.view_settings.look = "None"
    s.view_settings.exposure = 0
    s.view_settings.gamma = 1
    s.sequencer_colorspace_settings.name = "sRGB"
    ed = s.sequence_editor_create()
    n = c["loop"]["frames"]
    for i in range((frames + n - 1) // n):
        x = ed.strips.new_movie(
            f"Picture cycle {i + 1}", str(loop), channel=1, frame_start=1 + i * n
        )
        x.colorspace_settings.name = "sRGB"
        x.frame_final_end = min(1 + (i + 1) * n, frames + 1)
    return s


def inspect_edit(s, c, loop):
    xs = list(s.sequence_editor.strips)
    movies = sorted(
        (x for x in xs if x.type == "MOVIE"), key=lambda x: x.frame_final_start
    )
    sounds = [x for x in xs if x.type == "SOUND"]
    n = c["loop"]["frames"]
    frames = FACTS["frames"]
    require(
        len(xs) == len(movies) + 1 and len(sounds) == 1 and not s.objects,
        "Expected real picture strips and original sound once",
    )
    require(
        [(x.frame_final_start, x.frame_final_end) for x in movies]
        == [
            (1 + i * n, min(1 + (i + 1) * n, frames + 1))
            for i in range((frames + n - 1) // n)
        ],
        "Timeline gap/overlap/retiming",
    )
    for x in movies:
        require(
            digest(Path(bpy.path.abspath(x.filepath))) == digest(loop)
            and x.colorspace_settings.name == "sRGB"
            and not list(x.retiming_keys)
            and x.frame_offset_start == 0
            and x.animation_offset_start == 0,
            "Movie link/colour/retiming mismatch",
        )
    a = sounds[0]
    require(
        a.sound.filepath == c["music"]
        and not a.sound.packed_file
        and a.sound.use_memory_cache,
        "Original must be external, cached, unpacked",
    )
    require(
        a.volume == 1
        and a.sound_offset == 0
        and not list(a.retiming_keys)
        and a.frame_final_start == 1
        and a.frame_final_end == frames + 1,
        "Unexpected sound edit",
    )
    require(
        s.view_settings.view_transform == "Standard"
        and s.view_settings.exposure == 0
        and s.view_settings.gamma == 1,
        "Do not double grade",
    )
    return {
        "movie_strips": len(movies),
        "sound_strips": 1,
        "frames": frames,
        "audio_memory_cache": True,
        "audio_packed": False,
        "sound_offset": 0,
        "links": [bpy.path.abspath(x.filepath) for x in movies],
    }


def main(run):
    global ROOT, FACTS
    require(bpy.app.background, "Worker must run in isolated native Blender")
    require(
        bpy.app.version[:2] == (5, 2),
        "This tested worker supports Blender5.2; validate other versions before changing the guard",
    )
    c = run["config"]
    FACTS = run["facts"]
    ROOT = Path(c["output"])
    folder = Path(run["folder"])
    task = run["task"]
    begin = time.time()
    require(folder.is_relative_to(ROOT), "Output ownership failure")
    for x in FACTS["inputs"].values():
        require(digest(x["path"]) == x["sha256"], "Input changed before native work")
    if run.get("source"):
        require(
            digest(run["source"]) == run["source_sha256"],
            "Native source changed before worker started",
        )

    def progress(scene, *args):
        import shutil

        if shutil.disk_usage(ROOT).free < (c["reserve_gib"] - 2) * 2**30:
            save(
                folder / "reserve-failure.json", {"reason": "real disk reserve breach"}
            )
            os._exit(73)
        save(
            folder / "progress.json",
            {
                "stage": task,
                "frame": scene.frame_current,
                "elapsed": time.time() - begin,
                "pid": os.getpid(),
            },
        )

    bpy.app.handlers.render_post.append(progress)
    result = {}
    if task == "preview":
        s = art_scene(c)
        start = s.frame_start
        n = c["loop"]["frames"]
        s.frame_end = start + n - 1
        native = folder / "artwork.blend"
        s = scene_file(s, native)
        # File reopen resets handlers; register after it.
        bpy.app.handlers.render_post.append(progress)
        for k, index in enumerate([0, n // 4, n // 2, 3 * n // 4]):
            s.frame_set(start + index)
            s.render.resolution_percentage = 50
            still(s, folder / f"phase-{k}.png")
        render_movie(s, folder / "motion.mp4", start, start + n - 1, c)
        result = {
            "artwork": str(native),
            "scene_name": s.name,
            "start_frame": start,
            "view": s.view_settings.view_transform,
            "display": "sRGB",
            "external_dependencies": list(
                bpy.utils.blend_paths(absolute=True, packed=False, local=False)
            ),
        }
    elif task == "loop":
        s = bpy.data.scenes[run["scene_name"]]
        activate(s)
        dimensions(s, c)
        start = run["start_frame"]
        n = c["loop"]["frames"]
        for label, frame in [("start", start), ("endpoint", start + n)]:
            s.frame_set(frame)
            still(s, folder / f"{label}.png")
        render_movie(s, folder / "loop.mp4", start, start + n - 1, c)
        result = {"movie": str(folder / "loop.mp4"), "scene_name": s.name}
    elif task == "assemble":
        loop = Path(run["loop"])
        s = edit_scene(c, loop, FACTS["frames"], "Music video / " + c["title"])
        ed = s.sequence_editor
        a = ed.strips.new_sound(
            "Original music / ONCE", c["music"], channel=2, frame_start=1
        )
        a.volume = 1
        a.sound.use_memory_cache = True
        a.frame_final_end = FACTS["frames"] + 1
        a.show_waveform = True
        video(s, c, True)
        s.render.filepath = "//manual-export/movie.mp4"
        s["export_warning"] = (
            "Use blender-music-video CLI for accepted exports. Ordinary UI render bypasses the guarded sRGB metadata correction."
        )
        s["job_config_json"] = json.dumps(c)
        native = folder / "edit.blend"
        s = scene_file(s, native)
        bpy.app.handlers.render_post.append(progress)
        check = inspect_edit(s, c, loop)
        save(folder / "native-reopen.json", check)
        # Always include sample-zero; a middle-only test misses MP3 start-read defects.
        end = FACTS["probe_frames"]
        render_movie(s, folder / "roundtrip.mp4", 1, end, c, True)
        result = {
            "edit": str(native),
            "scene_name": s.name,
            "roundtrip": str(folder / "roundtrip.mp4"),
            "roundtrip_frames": end,
        }
    elif task == "export":
        s = bpy.data.scenes[run["scene_name"]]
        activate(s)
        save(folder / "native-reopen.json", inspect_edit(s, c, Path(run["loop"])))
        render_movie(s, folder / "movie.mp4", 1, FACTS["frames"], c, True)
        result = {"movie": str(folder / "movie.mp4")}
    elif task == "thumbnail":
        if run.get("artwork"):
            s = bpy.data.scenes[run["scene_name"]]
            activate(s)
            s.frame_set(run["start_frame"] + c["thumbnail"]["frame_index"])
            upscaled = False
        else:
            s = edit_scene(
                c, Path(run["loop"]), c["loop"]["frames"], "Thumbnail / " + c["title"]
            )
            s.frame_set(1 + c["thumbnail"]["frame_index"])
            upscaled = c["thumbnail"]["width"] > c["video"]["width"]
        for name, fmt, width, depth in [
            ("still.png", "PNG", c["thumbnail"]["width"], "16"),
            ("thumbnail.jpg", "JPEG", c["thumbnail"]["jpeg_width"], "8"),
        ]:
            s.render.resolution_x = width
            s.render.resolution_y = width * 9 // 16
            s.render.resolution_percentage = 100
            still(s, folder / name, fmt, depth)
        native = folder / "thumbnail.blend"
        scene_file(s, native)
        result = {
            "native": str(native),
            "upscaled_from_loop": upscaled,
            "frame_index": c["thumbnail"]["frame_index"],
        }
    else:
        raise ValueError("Unknown native task")
    for x in FACTS["inputs"].values():
        require(digest(x["path"]) == x["sha256"], "Read-only input changed")
    if run.get("source"):
        require(
            digest(run["source"]) == run["source_sha256"],
            "Native source changed during worker",
        )
    save(
        folder / "native-complete.json",
        {
            "task": task,
            "blender": bpy.app.version_string,
            "seconds": time.time() - begin,
            **result,
        },
    )


if __name__ == "__main__":
    main(json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text()))
