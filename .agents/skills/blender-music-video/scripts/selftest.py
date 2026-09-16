#!/usr/bin/env python3
"""Small neutral native integration fixture. Outputs never count as user approval."""

import argparse, copy, json, math, subprocess, sys, time, wave, zipfile
from pathlib import Path
import numpy as np
from core import save, read, digest, require

SCRIPT = Path(__file__).resolve().parent


def fixture(work, duration=4.237, rate=48000, name="synthetic stereo phrase.wav"):
    work = Path(work)
    music = work / name
    t = np.arange(round(duration * rate)) / rate
    rng = np.random.default_rng(417)
    signal = np.column_stack(
        [
            0.13 * np.sin(2 * np.pi * (173 * t + 11 * t * t))
            + 0.035 * np.sin(2 * np.pi * 487 * t),
            0.12 * np.sin(2 * np.pi * (227 * t + 7 * t * t))
            + 0.04 * np.sin(2 * np.pi * 619 * t),
        ]
    )
    signal += rng.normal(0, 0.001, signal.shape)
    signal *= 0.75 + 0.2 * np.sin(2 * np.pi * 0.37 * t)[:, None]
    with wave.open(str(music), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes((signal * 32767).astype("<i2").tobytes())
    music.chmod(0o444)
    return music


def config(work, music):
    return {
        "version": 1,
        "title": "Quiet relay / synthetic study",
        "output": str(work / "recipe output with spaces"),
        "music": str(music),
        "test_only": True,
        "reserve_gib": 36,
        "art": {
            "mode": "recipe",
            "recipe": "radial-relief",
            "theme": "Patience becoming playful movement; synthetic technical fixture, not a real song interpretation",
            "direction": "Tilting silver relief with a single warm marker",
            "palette_rationale": "Neutral silver retains form; a restrained warm marker makes the long cycle legible. Pale key and cool rim separate surfaces. These are fixture choices, not a channel default.",
            "palette": {
                "shell": "#87929B",
                "accent": "#C79A66",
                "key": "#F2EADC",
                "rim": "#C4D2E0",
            },
            "segments": 10,
            "key_watts": 1000,
            "rim_watts": 650,
        },
        "video": {"fps": 24, "width": 640, "height": 360, "crf": 16, "samples": 16},
        "loop": {"frames": 48},
        "thumbnail": {"frame_index": 17, "width": 1280, "jpeg_width": 640},
        "approval": {
            "direction": "SYNTHETIC TEST ONLY",
            "full_song": "SYNTHETIC TEST ONLY",
        },
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--work", required=True)
    p.add_argument("--blender", required=True)
    args = p.parse_args()
    work = Path(args.work).resolve()
    require(not work.exists(), "Use fresh test directory")
    work.mkdir(parents=True)
    logs = work / "logs"
    logs.mkdir()
    music = fixture(work)
    c = config(work, music)
    cp = work / "recipe config.json"
    save(cp, c)
    events = []

    def run(stage, path=cp, extra=(), expected=0):
        num = len(events)
        log = logs / f"{num:02}-{stage}.log"
        begin = time.time()
        with log.open("w") as f:
            r = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT / "mv.py"),
                    stage,
                    "--config",
                    str(path),
                    "--blender",
                    args.blender,
                    *extra,
                ],
                stdout=f,
                stderr=subprocess.STDOUT,
            )
        events.append(
            {
                "stage": stage,
                "config": path.name,
                "exit": r.returncode,
                "seconds": time.time() - begin,
                "log": str(log.relative_to(work)),
            }
        )
        save(work / "progress.json", events)
        require(
            (r.returncode == 0) == (expected == 0),
            f"Unexpected {stage} exit; inspect {log}",
        )

    for stage in [
        "inspect",
        "preview",
        "loop",
        "assemble",
        "export",
        "thumbnail",
        "verify",
        "package",
    ]:
        run(stage)
    root = Path(c["output"])
    facts = read(root / "job.json")["facts"]
    require(
        facts["partial_frames"] > 0 and c["video"]["fps"] != 30,
        "Must exercise changed timing/partial cycle",
    )
    run("export")  # completed/source-bound resume, not a rerender
    run("package", expected=1)  # immutable delivery must not be overwritten
    run(
        "review",
        extra=(
            "--stage",
            "package",
            "--note",
            "Synthetic review-record API exercise only; actual pixel/playback judgement is separate, not user feedback.",
        ),
    )
    require(
        read(root / "delivery/owner-review.json")["test_only"],
        "Synthetic review lost its label",
    )
    # Approved-loop intake: no preview/loop3D, different audio length and source sample rate.
    music2 = fixture(work, 5.117, 44100, "second synthetic phrase.wav")
    b = copy.deepcopy(c)
    b["music"] = str(music2)
    b["output"] = str(work / "approved loop output")
    b["title"] = "Second neutral fixture"
    b["art"]["mode"] = "loop"
    b["art"]["loop_file"] = str(root / "assets/loop.mp4")
    b["approval"]["loop"] = "SYNTHETIC FIXTURE, NOT USER FEEDBACK"
    bp = work / "approved loop config.json"
    save(bp, b)
    for stage in ["inspect", "assemble", "export", "thumbnail", "verify", "package"]:
        run(stage, bp)
    # Native source intake uses the same engine, with an existing editable scene.
    preview = read(root / "preview.json")
    s = copy.deepcopy(c)
    s["output"] = str(work / "approved scene output")
    s["art"]["mode"] = "scene"
    s["art"]["scene_file"] = str(root / preview["artwork"])
    s["art"]["scene_name"] = preview["scene_name"]
    sp = work / "approved scene config.json"
    save(sp, s)
    for stage in ["preview", "loop", "thumbnail"]:
        run(stage, sp)
    # Exercise the cached sample-zero MP3 path with native-generated synthetic audio.
    mp3 = work / "native synthetic phrase.mp3"
    request = work / "make audio request.json"
    save(request, {"source": str(music), "target": str(mp3)})
    with (logs / "make-audio.log").open("w") as f:
        generated = subprocess.run(
            [
                args.blender,
                "--factory-startup",
                "-b",
                "--python-exit-code",
                "1",
                "--python",
                str(SCRIPT.parent / "tests/make_audio.py"),
                "--",
                str(request),
            ],
            stdout=f,
            stderr=subprocess.STDOUT,
        )
    require(generated.returncode == 0, "Native synthetic MP3 generation failed")
    m = copy.deepcopy(b)
    m["output"] = str(work / "cached MP3 output")
    m["music"] = str(mp3)
    mp = work / "cached MP3 config.json"
    save(mp, m)
    for stage in ["inspect", "assemble", "export", "thumbnail", "verify", "package"]:
        run(stage, mp)
    # Cheap negatives through the public entry point, not just unit mocks.
    bad = copy.deepcopy(b)
    bad["music"] = str(work / "absent music.wav")
    bad["output"] = str(work / "missing-input output")
    badp = work / "missing-input config.json"
    save(badp, bad)
    run("inspect", badp, expected=1)
    bad = copy.deepcopy(b)
    bad["video"]["fps"] = 25
    bad["output"] = str(work / "mismatched-loop output")
    badp = work / "mismatched-loop config.json"
    save(badp, bad)
    run("inspect", badp, expected=1)
    bad = copy.deepcopy(b)
    bad["output"] = str(work / "unowned existing output")
    Path(bad["output"]).mkdir()
    badp = work / "existing-output config.json"
    save(badp, bad)
    run("inspect", badp, expected=1)
    bad = copy.deepcopy(c)
    bad["title"] = "Mismatched resume"
    badp = work / "changed-resume config.json"
    save(badp, bad)
    run("inspect", badp, expected=1)
    bad = copy.deepcopy(b)
    bad["output"] = str(work / "interrupted output")
    badp = work / "interrupted config.json"
    save(badp, bad)
    run("inspect", badp)
    partial = Path(bad["output"])
    (partial / "movie.mp4").write_bytes(b"partial")
    save(partial / "terminal.json", {"state": "FAILED", "returncode": 73})
    run("verify", badp, expected=1)
    bad = copy.deepcopy(s)
    bad["output"] = str(work / "failed-native output")
    bad["art"]["scene_name"] = "INTENTIONALLY ABSENT"
    badp = work / "failed-native config.json"
    save(badp, bad)
    run("preview", badp, expected=1)
    require(
        not (Path(bad["output"]) / "preview.json").exists(),
        "Failed worker reported completion",
    )
    # Reopen the relocated zipped edit and verify that its picture link stays inside the kit.
    relocate = work / "relocated native kit"
    relocate.mkdir()
    with zipfile.ZipFile(root / "delivery/native-edit-kit.zip") as z:
        require(
            not any(Path(n).suffix.lower() in {".mp3", ".wav"} for n in z.namelist()),
            "Original audio leaked into kit",
        )
        z.extractall(relocate)
    edit = read(root / "assemble.json")
    reopen = work / "reopen request.json"
    save(
        reopen,
        {
            "job": str(root / "job.json"),
            "loop": str(relocate / "assets/loop.mp4"),
            "scene": edit["scene_name"],
            "report": str(work / "relocated-reopen.json"),
        },
    )
    with (logs / "relocated-reopen.log").open("w") as f:
        r = subprocess.run(
            [
                args.blender,
                "-b",
                str(relocate / edit["edit"]),
                "--python-exit-code",
                "1",
                "--python",
                str(SCRIPT.parent / "tests/reopen.py"),
                "--",
                str(reopen),
            ],
            stdout=f,
            stderr=subprocess.STDOUT,
        )
    require(r.returncode == 0, "Relocated native reopen failed")
    require(
        digest(music) == facts["inputs"]["music"]["sha256"],
        "Synthetic original mutated",
    )
    save(
        work / "terminal.json",
        {
            "state": "NATIVE_SMOKE_PASSED_NEEDS_ACTUAL_PIXEL_PLAYBACK_REVIEW",
            "events": events,
            "facts": facts,
            "recipe_root": str(root),
            "loop_root": b["output"],
            "scene_root": s["output"],
            "mp3_root": m["output"],
            "real_user_feedback": False,
        },
    )
    print(
        json.dumps(
            {
                "state": "NATIVE_SMOKE_PASSED_NEEDS_ACTUAL_REVIEW",
                "receipt": str(work / "terminal.json"),
            }
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"state": "FAILED", "error": str(e)}), file=sys.stderr)
        sys.exit(1)
