#!/usr/bin/env python3
"""Single entry point: staged native music-video workflow; see --help."""

import argparse, contextlib, html, json, os, shutil, subprocess, sys, time, zipfile
from pathlib import Path
from core import (
    check_inputs,
    command,
    complete,
    digest,
    executable,
    load_config,
    open_job,
    probe,
    read,
    receipt,
    require,
    resolve_loop,
    save,
    stream,
    validate_picture,
)

SCRIPTS = Path(__file__).resolve().parent
NATIVE = {"preview", "loop", "assemble", "export", "thumbnail"}
ACTIVE_ROOT = None


def blender_tool(value):
    path = executable(value or os.environ.get("BLENDER", "blender"))
    version = command([path, "--version"]).decode(errors="replace")
    require(
        version.startswith("Blender 5.2."), "Validated native API requires Blender5.2"
    )
    return path


def reviewed(r, stage):
    job = read(r / "job.json")
    if job["test_only"]:
        return
    p = r / f"review-{stage}.json"
    require(
        p.is_file(),
        f"Owner must inspect {stage} and record review; this is not a new user-approval gate",
    )
    require(read(p)["receipt_sha256"] == digest(r / f"{stage}.json"), "Review is stale")


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


@contextlib.contextmanager
def lock(r, clear=False):
    path = r / "worker.lock"
    if path.exists():
        d = read(path)
        require(
            clear, "An owned worker lock exists; inspect it, never launch a duplicate"
        )
        require(d["identity"] == read(r / "job.json")["identity"], "Foreign lock")
        require(
            not any(alive(p) for p in [d.get("pid"), d.get("worker_pid")] if p),
            "A recorded process is alive; refuse lock removal",
        )
        path.rename(r / f"stale-lock-{time.time_ns()}.json")
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.close(fd)
    state = {"identity": read(r / "job.json")["identity"], "pid": os.getpid()}
    save(path, state)
    try:
        yield path, state
    finally:
        if not state.get("worker_pid") or not alive(state["worker_pid"]):
            path.unlink(missing_ok=True)


def attempt(r, stage, retry):
    parent = r / "attempts"
    parent.mkdir(exist_ok=True)
    old = list(parent.glob(stage + "-*"))
    require(
        not old or retry,
        "Old attempt retained; inspect it then use --retry for a fresh attempt",
    )
    p = parent / f"{stage}-{len(old) + 1:03}"
    p.mkdir()
    return p


def relative(r, data):
    return {
        k: str(Path(v).relative_to(r))
        if isinstance(v, str) and v.startswith(str(r) + os.sep)
        else v
        for k, v in data.items()
    }


def native_stage(r, job, args):
    stage = args.command
    c = job["config"]
    if (r / f"{stage}.json").exists():
        return receipt(r, stage)
    with lock(r, args.clear_stale_lock) as (lockpath, state):
        run = {"config": c, "facts": job["facts"], "task": stage}
        source = None
        if stage == "preview":
            require(
                c["art"]["mode"] != "loop",
                "Approved loop intake skips artwork preview/rendering",
            )
            if c["art"]["mode"] == "scene":
                source = Path(c["art"]["scene_file"])
        elif stage == "loop":
            reviewed(r, "preview")
            d = receipt(r, "preview")
            source = r / d["artwork"]
            run.update(scene_name=d["scene_name"], start_frame=d["start_frame"])
        elif stage in {"assemble", "export"}:
            if c["art"]["mode"] != "loop":
                reviewed(r, "loop")
            run["loop"] = str(resolve_loop(r, job))
            if stage == "export":
                reviewed(r, "assemble")
                d = receipt(r, "assemble")
                source = r / d["edit"]
                run["scene_name"] = d["scene_name"]
        elif stage == "thumbnail":
            if c["art"]["mode"] == "loop":
                run["loop"] = str(resolve_loop(r, job))
            else:
                d = receipt(r, "preview")
                source = r / d["artwork"]
                run.update(
                    artwork=str(source),
                    scene_name=d["scene_name"],
                    start_frame=d["start_frame"],
                )
        blender = blender_tool(args.blender)
        folder = attempt(r, stage, args.retry)
        run["folder"] = str(folder)
        if source:
            run.update(source=str(source), source_sha256=digest(source))
        save(folder / "run.json", run)
        cmd = (
            [blender, "--factory-startup", "-b"]
            + ([str(source)] if source else [])
            + [
                "--python-exit-code",
                "1",
                "--python",
                str(SCRIPTS / "native.py"),
                "--",
                str(folder / "run.json"),
            ]
        )
        require(
            shutil.disk_usage(r).free >= c["reserve_gib"] * 2**30,
            "Insufficient launch reserve",
        )
        check_inputs(job)
        with (folder / "worker.log").open("wb") as log:
            p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
            state.update(worker_pid=p.pid, stage=stage, folder=str(folder))
            save(lockpath, state)
            save(
                folder / "terminal.json",
                {"state": "NATIVE_RUNNING", "pid": p.pid, "command": cmd},
            )
            code = p.wait()
        save(
            folder / "terminal.json",
            {
                "state": "NATIVE_EXITED_NEEDS_QA" if code == 0 else "FAILED",
                "returncode": code,
            },
        )
        require(code == 0, f"Native worker failed; retained {folder}/worker.log")
        d = relative(r, read(folder / "native-complete.json"))
        check_inputs(job)
        from checks import video_check, loop_check

        if stage == "loop":
            validate_picture(stream(probe(r / d["movie"]), "video"), c)
            loop_check(r / d["movie"], folder)
        if stage == "assemble":
            video_check(
                r / d["roundtrip"],
                Path(run["loop"]),
                c,
                job["facts"],
                d["roundtrip_frames"],
                folder,
                False,
            )
        if stage == "thumbnail":
            from PIL import Image

            for name, key in [("still.png", "width"), ("thumbnail.jpg", "jpeg_width")]:
                with Image.open(folder / name) as image:
                    require(
                        image.size
                        == (c["thumbnail"][key], c["thumbnail"][key] * 9 // 16),
                        "Thumbnail dimensions changed",
                    )
                    image.verify()
            require(
                (folder / "still.png").read_bytes()[24] == 16,
                "Expected16-bit PNG still",
            )
            save(
                folder / "thumbnail-check.json",
                {
                    "dimensions_and_decode": "passed",
                    "native_frame_index": c["thumbnail"]["frame_index"],
                    "upscaled_from_loop": d["upscaled_from_loop"],
                },
            )
        return complete(r, job, stage, folder, d)


def package(r, job):
    verified = receipt(r, "verify")
    thumb = receipt(r, "thumbnail")
    edit = receipt(r, "assemble")
    movie = receipt(r, "export")
    dest = r / "delivery"
    require(not dest.exists(), "Delivery exists: preserve it, do not overwrite")
    dest.mkdir()
    paths = set()
    for d in [verified, thumb, edit, movie]:
        paths.update(d["files"])
    if job["config"]["art"]["mode"] != "loop":
        paths.update(receipt(r, "preview")["files"])
        paths.update(receipt(r, "loop")["files"])
    paths.add("assets/loop.mp4")
    # Explicit allowlist; no original soundtrack, private live snapshots or rejected attempts.
    paths = {
        p
        for p in paths
        if Path(p).suffix in {".blend", ".mp4", ".jpg", ".png", ".json"}
    }
    for name in sorted(paths):
        src = r / name
        require(src.resolve().is_relative_to(r), "No escaping symlink in package")
        require(
            src.resolve() != Path(job["config"]["music"]), "Never bundle original music"
        )
        dst = dest / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        require(digest(src) == digest(dst), "Package copy mismatch")
    for name in [
        "job.json",
        "preview.json",
        "loop.json",
        "assemble.json",
        "export.json",
        "thumbnail.json",
        "verify.json",
    ]:
        if (r / name).exists():
            shutil.copy2(r / name, dest / name)
    notes = """# Native music-video handoff\n\nLocal review only; not published. Original music is external, unmodified and NOT bundled. Re-link that same original when moving machines. The encoded AAC soundtrack is of course part of the movie.\n\nThe native edit contains real contiguous picture strips and the original sound once, unity volume, native memory cache, no fades or retiming. Open the Native music video / Video Editing workspace; set workspace.sequencer_scene to the edit if the application retains another workspace. Do not use UI operators headlessly.\n\nArtwork output is baked sRGB. The VSE uses Standard/None/exposure0/gamma1, not another AgX pass. Use the skill CLI for final exports: ordinary UI rendering bypasses the metadata correction. Native H264 metadata was guardedly repaired to sRGB transfer while retaining Rec709 primaries/matrix and limited range. This is a metadata fix, NOT a colour conversion. Inspect measurements.json and native export metadata receipts.\n\nMeasured PCM correlation is not listening. Frame decoding/callbacks are not calibrated-display certification. No beat-sync or HDR claim. Check actual playback, seams, audio and thumbnail before calling this ready. Native AAC packet padding is reported separately from the frame-grid tail.\n\nRegeneration: load the blender-music-video skill; use the original config/source inputs with a NEW output root. Existing accepted outputs are never overwritten. Supplied scenes can have external texture/font/library dependencies; those are not automatically bundled.\n"""
    (dest / "README.md").write_text(notes)
    save(dest / "creative-record.json", job["config"]["art"])
    import copy

    reproduction = copy.deepcopy(job["config"])
    reproduction["output"] = "./new reproduction output"
    reproduction["art"] = {
        k: reproduction["art"][k] for k in ["theme", "direction", "palette_rationale"]
    }
    reproduction["art"].update(mode="loop", loop_file="./assets/loop.mp4")
    reproduction["approval"]["loop"] = (
        "Inherited completed/approved loop; consult source-bound job and owner review"
    )
    save(dest / "reproduce.json", reproduction)
    with zipfile.ZipFile(dest / "native-edit-kit.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(paths):
            if Path(name).suffix == ".blend" or name == "assets/loop.mp4":
                z.write(dest / name, name)
        z.write(dest / "README.md", "README.md")
        z.write(dest / "creative-record.json", "creative-record.json")
        z.write(dest / "reproduce.json", "reproduce.json")
    title = html.escape(job["config"]["title"])
    m = html.escape(movie["movie"], quote=True)
    t = next(p for p in thumb["files"] if p.endswith("/thumbnail.jpg"))
    t = html.escape(t, quote=True)
    (dest / "index.html").write_text(
        f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} / local review</title><style>body{{margin:0;background:#141719;color:#efebe3;font:18px Georgia,serif}}main{{max-width:1100px;margin:auto;padding:28px}}small,a,button{{font:14px monospace}}a{{color:#e6c48d}}video{{width:100%;aspect-ratio:16/9;background:#000}}button{{padding:12px;margin:8px 8px 8px 0}}nav{{display:flex;flex-wrap:wrap;gap:20px;margin:22px 0}}p{{max-width:72ch;line-height:1.5}}</style><main><small>NATIVE MUSIC VIDEO / LOCAL REVIEW</small><h1>{title}</h1><video id="movie" controls playsinline preload="metadata" poster="{t}" src="{m}"></video><button id="play">Play / pause</button><button id="restart">Restart</button><nav><a download href="{m}">Movie</a><a download href="native-edit-kit.zip">Native editing kit (no original music)</a><a download href="{t}">Thumbnail</a><a href="README.md">Native / colour notes</a><a href="verify.json">Measured QA</a></nav><p>Original song once. No fades, retiming or publication. Technical measurements do not replace actual viewing and listening; consult the owner-review receipt for what was personally checked.</p></main><script>const v=document.querySelector('video');v.volume=.65;document.querySelector('#play').onclick=()=>v.paused?v.play().catch(e=>alert(e.message)):v.pause();document.querySelector('#restart').onclick=()=>v.currentTime=0;</script></html>'''
    )
    manifest = {
        str(p.relative_to(dest)): {"sha256": digest(p), "bytes": p.stat().st_size}
        for p in dest.rglob("*")
        if p.is_file()
    }
    save(dest / "manifest.json", manifest)
    all_files = {
        str(p.relative_to(r)): {"sha256": digest(p), "bytes": p.stat().st_size}
        for p in dest.rglob("*")
        if p.is_file()
    }
    result = {
        "identity": job["identity"],
        "state": "TEST_ONLY" if job["test_only"] else "PACKAGED_NEEDS_ACTUAL_REVIEW",
        "directory": "delivery",
        "files": all_files,
    }
    save(r / "package.json", result)
    return result


def main():
    global ACTIVE_ROOT
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "command",
        choices=[
            "inspect",
            "preview",
            "loop",
            "assemble",
            "export",
            "thumbnail",
            "verify",
            "review",
            "package",
            "serve",
        ],
    )
    p.add_argument("--config")
    p.add_argument(
        "--delivery",
        help="Serve a relocated, manifest-verified delivery without its old job root",
    )
    p.add_argument("--blender")
    p.add_argument("--retry", action="store_true")
    p.add_argument("--clear-stale-lock", action="store_true")
    p.add_argument("--stage", choices=["preview", "loop", "assemble", "package"])
    p.add_argument("--note")
    p.add_argument("--port", type=int, default=0)
    args = p.parse_args()
    if args.command == "serve" and args.delivery:
        from serve import serve

        serve(Path(args.delivery), args.port)
        return
    require(args.config, "--config is required except for serve --delivery")
    c = load_config(args.config)
    if args.command == "inspect":
        blender_tool(args.blender)
    r, job = open_job(c)
    ACTIVE_ROOT = r
    result = {}
    if args.command == "inspect":
        result = job
    elif args.command in NATIVE:
        result = native_stage(r, job, args)
    elif args.command == "verify":
        d = receipt(r, "export")
        folder = attempt(r, "verify", args.retry)
        from checks import video_check

        result = video_check(
            r / d["movie"],
            resolve_loop(r, job),
            c,
            job["facts"],
            job["facts"]["frames"],
            folder,
            True,
        )
        result = complete(
            r, job, "verify", folder, {"state": "MEASURED_NEEDS_ACTUAL_REVIEW"}
        )
    elif args.command == "review":
        require(
            args.stage and args.note,
            "Supply --stage and a truthful --note with observed evidence",
        )
        receipt(r, args.stage)
        require(
            not (r / f"review-{args.stage}.json").exists(),
            "Review already exists; preserve it",
        )
        result = {
            "stage": args.stage,
            "note": args.note,
            "test_only": job["test_only"],
            "receipt_sha256": digest(r / f"{args.stage}.json"),
            "recorded_at": time.time(),
        }
        if args.stage == "package":
            result["state"] = (
                "TEST_ONLY" if job["test_only"] else "OWNER_REVIEW_RECORDED"
            )
            result["payload_manifest_sha256"] = digest(r / "delivery/manifest.json")
            require(
                not (r / "delivery/owner-review.json").exists(),
                "Preserve existing owner review",
            )
            save(
                r / "delivery/owner-review.json", result
            )  # Separate appended review; immutable payload manifest stays unchanged.
        save(r / f"review-{args.stage}.json", result)
    elif args.command == "package":
        result = package(r, job)
    elif args.command == "serve":
        receipt(r, "package")
        from serve import serve

        serve(r / "delivery", args.port)
        return
    check_inputs(job)
    receipt_name = (
        "job.json"
        if args.command == "inspect"
        else f"review-{args.stage}.json"
        if args.command == "review"
        else f"{args.command}.json"
    )
    summary = {
        "stage": args.command,
        "state": result.get("state", "STAGE_COMPLETE_NEEDS_REVIEW"),
        "test_only": job["test_only"],
        "receipt": str(r / receipt_name),
    }
    summary.update(
        {k: result[k] for k in ["movie", "artwork", "edit", "directory"] if k in result}
    )
    if args.command == "inspect":
        summary.update(
            {
                k: job["facts"][k]
                for k in [
                    "frames",
                    "audio_seconds",
                    "video_seconds",
                    "full_cycles",
                    "partial_frames",
                    "tail_seconds",
                ]
            }
        )
    print(json.dumps(summary))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback

        error = {"state": "FAILED", "error": str(e)}
        if ACTIVE_ROOT is not None:
            path = ACTIVE_ROOT / "errors" / f"{time.time_ns()}.json"
            save(path, {**error, "traceback": traceback.format_exc()})
            error["receipt"] = str(path)
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)
