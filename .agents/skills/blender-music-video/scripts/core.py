"""Host-side contracts and immutable receipts; no rendering or external assembly."""

from pathlib import Path
import hashlib, json, math, os, shutil, subprocess, time


class ContractError(RuntimeError):
    pass


def require(ok, message):
    if not ok:
        raise ContractError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while b := f.read(1024 * 1024):
            h.update(b)
    return h.hexdigest()


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def read(path):
    return json.loads(Path(path).read_text())


def command(args):
    p = subprocess.run([str(x) for x in args], capture_output=True)
    require(p.returncode == 0, p.stderr.decode(errors="replace")[-3000:])
    return p.stdout


def executable(name):
    p = shutil.which(str(name))
    require(p is not None, f"Missing executable: {name}")
    return str(Path(p).resolve())


def probe(path):
    return json.loads(
        command(
            [
                "ffprobe",
                "-v",
                "error",
                "-count_frames",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                path,
            ]
        )
    )


def stream(info, kind):
    values = [s for s in info["streams"] if s["codec_type"] == kind]
    require(len(values) == 1, f"Expected one {kind} stream")
    return values[0]


def pcm(path):
    import numpy as np

    return np.frombuffer(
        command(
            [
                "ffmpeg",
                "-v",
                "error",
                "-xerror",
                "-i",
                path,
                "-map",
                "0:a:0",
                "-f",
                "f32le",
                "-acodec",
                "pcm_f32le",
                "-",
            ]
        ),
        dtype="<f4",
    ).reshape(-1, 2)


def resolve(base, value):
    p = Path(value).expanduser()
    return (base / p).resolve() if not p.is_absolute() else p.resolve()


def load_config(path):
    path = Path(path).resolve()
    c = read(path)
    require(
        type(c.get("version")) is int and c["version"] == 1,
        "Config version must be integer1",
    )
    require(
        type(c.get("test_only", False)) is bool,
        "test_only must be a boolean, never a string",
    )
    require(
        not (
            set(c)
            - {
                "version",
                "title",
                "output",
                "music",
                "art",
                "video",
                "loop",
                "thumbnail",
                "approval",
                "test_only",
                "reserve_gib",
            }
        ),
        "Unknown config key",
    )
    for key in [
        "title",
        "output",
        "music",
        "art",
        "video",
        "loop",
        "thumbnail",
        "approval",
    ]:
        require(key in c, f"Missing config field: {key}")
    allowed = {
        "art": {
            "mode",
            "recipe",
            "theme",
            "direction",
            "palette_rationale",
            "palette",
            "segments",
            "key_watts",
            "rim_watts",
            "scene_file",
            "scene_name",
            "loop_file",
        },
        "video": {"fps", "width", "height", "crf", "samples", "max_audio_seconds"},
        "loop": {"frames"},
        "thumbnail": {"frame_index", "width", "jpeg_width"},
        "approval": {"direction", "full_song", "loop"},
    }
    for key, keys in allowed.items():
        require(
            isinstance(c[key], dict) and not (set(c[key]) - keys),
            f"Unknown/malformed {key} config",
        )
    require(
        isinstance(c["title"], str) and 0 < len(c["title"]) <= 160, "Provide a title"
    )
    c["output"] = str(resolve(path.parent, c["output"]))
    c["music"] = str(resolve(path.parent, c["music"]))
    r = Path(c["output"])
    require(Path(c["music"]).is_file(), "Missing original music")
    require(
        not Path(c["music"]).is_relative_to(r),
        "Original music must remain outside output/package",
    )
    require(
        c["art"].get("mode") in {"recipe", "scene", "loop"},
        "art.mode must be recipe, scene or loop",
    )
    for key in ["theme", "direction", "palette_rationale"]:
        require(
            isinstance(c["art"].get(key), str) and bool(c["art"][key].strip()),
            f"Record art.{key}; no automatic song-to-art inference",
        )
    for key in ["scene_file", "loop_file"]:
        if key in c["art"]:
            c["art"][key] = str(resolve(path.parent, c["art"][key]))
            require(Path(c["art"][key]).is_file(), f"Missing {key}")
            require(
                not Path(c["art"][key]).is_relative_to(r),
                "Inputs must be outside the new owned output",
            )
    if c["art"]["mode"] == "scene":
        require(
            "scene_file" in c["art"] and c["art"].get("scene_name"),
            "Provide scene_file and scene_name",
        )
    if c["art"]["mode"] == "loop":
        require(
            "loop_file" in c["art"]
            and isinstance(c["approval"].get("loop"), str)
            and bool(c["approval"]["loop"].strip()),
            "Record actual approved-loop provenance",
        )
    if c["art"]["mode"] == "recipe":
        require(
            c["art"].get("recipe") == "radial-relief",
            "Supported recipe: radial-relief; use scene intake for a new concept",
        )
        palette = c["art"].get("palette", {})
        require(
            set(palette) == {"shell", "accent", "key", "rim"},
            "Provide shell/accent/key/rim palette",
        )
        import re

        require(
            all(re.fullmatch(r"#[0-9a-fA-F]{6}", x) for x in palette.values()),
            "Palette must use #RRGGBB references",
        )
        require(
            type(c["art"].get("segments", 12)) is int
            and 4 <= c["art"].get("segments", 12) <= 48,
            "segments must be an integer4–48",
        )
        for key in ["key_watts", "rim_watts"]:
            require(
                type(c["art"].get(key)) in {int, float} and 0 < c["art"][key] <= 20000,
                f"Provide numeric bounded {key}",
            )
    require(
        all(
            isinstance(c["approval"].get(k), str) and bool(c["approval"][k].strip())
            for k in ["direction", "full_song"]
        ),
        "Record creative direction and full-song authority; do not invent approval",
    )
    v = c["video"]
    require(
        type(v.get("fps")) is int and 1 <= v["fps"] <= 120, "Integer fps1–120 required"
    )
    require(
        1 <= v.get("max_audio_seconds", 1800) <= 1800,
        "Audio budget must be1–1800 seconds",
    )
    require(
        all(
            isinstance(v.get(k), int) and v[k] >= 64 and v[k] % 2 == 0
            for k in ["width", "height"]
        ),
        "Even video dimensions >=64 required",
    )
    require(
        v["width"] * 9 == v["height"] * 16 and v["width"] <= 3840,
        "Current video contract:16:9, up to3840 pixels wide",
    )
    require(
        type(v.get("crf", 16)) is int and 0 <= v.get("crf", 16) <= 30,
        "crf must be an integer0–30",
    )
    require(
        type(v.get("samples", 32)) is int and 1 <= v.get("samples", 32) <= 512,
        "samples must be an integer1–512",
    )
    require(
        isinstance(c["loop"].get("frames"), int) and 8 <= c["loop"]["frames"] <= 3600,
        "Provide measured/intended loop.frames8–3600",
    )
    t = c["thumbnail"]
    require(
        isinstance(t.get("frame_index"), int)
        and 0 <= t["frame_index"] < c["loop"]["frames"],
        "Thumbnail frame_index is zero-based within loop",
    )
    require(
        all(
            isinstance(t.get(k), int) and 64 <= t[k] <= 7680 and t[k] % 16 == 0
            for k in ["width", "jpeg_width"]
        ),
        "Thumbnail widths must be multiples of16, at most7680",
    )
    reserve = c.setdefault("reserve_gib", 36)
    require(
        isinstance(reserve, (int, float)) and reserve >= 36,
        "Launch reserve must be >=36GiB; runtime reserve is two GiB lower",
    )
    require(
        not os.environ.get("OCIO"), "Custom OCIO is outside this tested colour contract"
    )
    return c


def inspect(c):
    executable("ffmpeg")
    executable("ffprobe")
    import numpy, scipy, PIL  # Explicit dependency preflight; no automatic installation.

    a = stream(probe(c["music"]), "audio")
    require(a["channels"] == 2, "Current tested contract requires stereo input")
    rate = int(a["sample_rate"])
    require(rate in {44100, 48000}, "Current supported audio rates:44100 or48000")
    require(
        float(a.get("duration", 0)) <= c["video"].get("max_audio_seconds", 1800),
        "Audio exceeds declared duration budget",
    )
    decoded = pcm(c["music"])
    samples = len(decoded)
    frames = (samples * c["video"]["fps"] + rate - 1) // rate
    require(
        frames >= 2 and samples / rate <= c["video"].get("max_audio_seconds", 1800),
        "Empty/over-budget soundtrack",
    )
    active = numpy.flatnonzero(numpy.max(numpy.abs(decoded), axis=1) > 1e-4)
    require(len(active) > 0, "Silent soundtrack requires a different QA contract")
    probe_frames = min(
        frames,
        max(
            3 * c["video"]["fps"],
            int(active[0]) * c["video"]["fps"] // rate + c["video"]["fps"],
        ),
    )
    inputs = {"music": {"path": c["music"], "sha256": digest(c["music"])}}
    for key in ["scene_file", "loop_file"]:
        if key in c["art"]:
            inputs[key] = {"path": c["art"][key], "sha256": digest(c["art"][key])}
    if c["art"]["mode"] == "loop":
        p = probe(c["art"]["loop_file"])
        require(
            len(p["streams"]) == 1,
            "Approved loop must be picture-only, never bundle embedded original audio",
        )
        v = stream(p, "video")
        validate_picture(v, c)
    return {
        "inputs": inputs,
        "probe_frames": probe_frames,
        "audio_rate": rate,
        "audio_samples": samples,
        "audio_seconds": samples / rate,
        "frames": frames,
        "video_seconds": frames / c["video"]["fps"],
        "tail_seconds": frames / c["video"]["fps"] - samples / rate,
        "full_cycles": frames // c["loop"]["frames"],
        "partial_frames": frames % c["loop"]["frames"],
    }


def validate_picture(v, c):
    from fractions import Fraction

    require(
        Fraction(v["avg_frame_rate"]) == c["video"]["fps"],
        "Picture fps mismatch: never silently retime",
    )
    require(
        v.get("sample_aspect_ratio") == "1:1", "Square-pixel approved loop required"
    )
    require(
        [v["width"], v["height"]] == [c["video"]["width"], c["video"]["height"]],
        "Picture dimensions mismatch",
    )
    require(
        int(v["nb_read_frames"]) == c["loop"]["frames"], "Loop frame count mismatch"
    )
    require(
        (
            v.get("color_transfer"),
            v.get("color_primaries"),
            v.get("color_space"),
            v.get("color_range"),
        )
        == ("iec61966-2-1", "bt709", "bt709", "tv"),
        "Approved loop must have measured sRGB/Rec709-matrix/limited-range metadata; other targets need a validated transform",
    )


def script_identity():
    h = hashlib.sha256()
    for p in sorted(Path(__file__).parent.glob("*.py")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def open_job(c):
    facts = inspect(c)
    identity = hashlib.sha256(
        json.dumps(
            {"config": c, "inputs": facts["inputs"], "scripts": script_identity()},
            sort_keys=True,
        ).encode()
    ).hexdigest()
    r = Path(c["output"])
    mark = r / "job.json"
    if r.exists():
        require(
            mark.is_file(),
            "Existing output is not owned by this job; choose a fresh directory",
        )
        require(
            read(mark)["identity"] == identity,
            "Config, source or helper identity mismatch; preserve old job and use a versioned output",
        )
    else:
        parent = next(p for p in [r.parent, *r.parents] if p.exists())
        require(
            shutil.disk_usage(parent).free >= c["reserve_gib"] * 2**30,
            "Insufficient disk reserve",
        )
        r.mkdir(parents=True)
        save(
            mark,
            {
                "identity": identity,
                "config": c,
                "facts": facts,
                "test_only": bool(c.get("test_only")),
            },
        )
    return r, read(mark)


def check_inputs(job):
    for x in job["facts"]["inputs"].values():
        require(digest(x["path"]) == x["sha256"], "Read-only input changed")


def receipt(r, stage):
    p = r / f"{stage}.json"
    require(
        p.is_file(),
        f"No completed {stage} receipt (partial/failed output is not success)",
    )
    d = read(p)
    require(d["identity"] == read(r / "job.json")["identity"], "Stale stage receipt")
    for name, info in d["files"].items():
        require(
            (r / name).is_file() and digest(r / name) == info["sha256"],
            f"Missing/changed artifact: {name}",
        )
    return d


def complete(r, job, stage, folder, extra):
    files = {
        str(p.relative_to(r)): {"sha256": digest(p), "bytes": p.stat().st_size}
        for p in folder.rglob("*")
        if p.is_file() and p.name not in {"worker.log", "progress.json", "run.json"}
    }
    data = {
        "identity": job["identity"],
        "stage": stage,
        "state": "STAGE_COMPLETE_NEEDS_QA_OR_REVIEW",
        "files": files,
        **extra,
    }
    save(r / f"{stage}.json", data)
    return data


def resolve_loop(r, job):
    c = job["config"]
    asset = r / "assets/loop.mp4"
    if c["art"]["mode"] == "loop":
        source = Path(c["art"]["loop_file"])
    else:
        source = r / receipt(r, "loop")["movie"]
    if asset.exists():
        require(digest(asset) == digest(source), "Owned loop asset changed")
    else:
        asset.parent.mkdir(exist_ok=True)
        shutil.copy2(source, asset)
    return asset
