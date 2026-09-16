---
name: blender-music-video
description: Create and finish native Blender kinetic-loop music videos from a supplied song and creative brief, editable scene, or approved loop. Use for artwork-led looping MVs with original music, matching thumbnails and local delivery; not narrative-film generation, AI video, remixing, general editing or publishing.
compatibility: Blender5.2; Python3.10+ with NumPy, SciPy and Pillow; FFmpeg/FFprobe for decoding/probing only. Local filesystem and native Blender rendering. No add-ons or paid services required.
metadata:
  version: 1.0.0
---

# Native Blender music video

Spend judgment on the song and art; let code repeat the plumbing. This is **one kinetic-loop workflow**, not an automatic arbitrary-song beauty generator.

## First run

Resolve this skill's directory to an absolute `SKILL_ROOT`. All paths below are relative to **this SKILL.md**, never the caller's working directory. Keep job outputs outside the installed skill. Do not install dependencies or change global Blender preferences silently.

1. Confirm song rights/scope, full-song authority and **one** creative direction. If already approved, reuse that decision—no six-way workshop or new routine approval gate.
2. Read [creative guidance](references/creative.md) when authoring, and [colour/native rules](references/colour-native.md) before native work. If tempo/structure evidence is needed, load the existing `song-structure` skill rather than adding DSP here. Preserve uncertainty.
3. Copy [the config template](examples/job.json) to the job. Fill actual source paths, authority, theme, palette rationale and output settings; see [config/commands](references/commands.md). The template is not ready-to-run approval.

```sh
python3 "$SKILL_ROOT/scripts/mv.py" inspect --config "/absolute/job.json" --blender "/path/to/Blender"
```

## Normal run

- **New native art:** use Blender MCP for live authoring/inspection when available. Preserve the live document first. `scripts/recipe.py` provides native material/light/periodic helpers and a radial-relief recipe; it adds a new scene, never clears the live document. A new concept enters as a versioned `.blend`/scene via `art.mode=scene`; it need not resemble this recipe.
- **Recipe or supplied scene:** run `preview`; inspect actual phase images and motion, then record an honest owner `review --stage preview --note ...`. Run `loop`; inspect motion/seam/endpoint evidence and record `review --stage loop`.
- **Approved picture-only loop:** `art.mode=loop` skips all3D authoring and loop rendering. Intake verifies its measured frame count/fps/colour and copies it byte-identically.
- Run `assemble` for the real native VSE project and sample-zero audio/colour diagnostic. Inspect its actual picture result; record `review --stage assemble` yourself. Do not ask the user to approve routine technical setup again.
- Run `export`, `thumbnail`, `verify`, then `package`. These are separate finite commands using the same `--config` and, for native work, `--blender` arguments. No external concat/mux/encode substitute; no full-song3D rerender.
- Run `serve --port 0` and use its printed loopback URL. Perform [actual playback/colour/audio/player QA](references/verification.md), record `review --stage package`, and deliver the movie, native kit and thumbnail directly. Do not equate metrics with subjective acceptance or listening.

```sh
python3 "$SKILL_ROOT/scripts/mv.py" preview --config "/absolute/job.json" --blender "/path/to/Blender"
python3 "$SKILL_ROOT/scripts/mv.py" review --config "/absolute/job.json" --stage preview --note "Actual observations and evidence paths"
# Continue the stages above, or skip preview/loop for approved-loop intake.
```

## Invariants and genuine exceptions

- Preserve original media, accepted outputs and source-bound receipts. Original song stays external/unpacked and appears once at unity volume/speed; no fades, trimming of its ending, retiming or claimed beat sync.
- Config/source/helper changes invalidate resume. Use a versioned output for changed work; `--retry` preserves failed attempts. A partial file is never completion. Inspect locks/PIDs before recovery; no ETA-based killing or foreign process control.
- Read compact JSON and targeted evidence, not frame-by-frame logs. One native worker per job output; the caller serializes resource use across jobs. CLI has no Herdr/pane/port assumptions; its JSON is the notification integration boundary.
- Colour mismatches, absent dependencies, unsupported fps/format/OCIO/version, failed seam/audio tests or changed input are real stops—not reasons to weaken assertions. See documented limits before extending the contract.
- Creative direction and actual output review remain human/agent work. Never fabricate feedback; `test_only` is exclusively synthetic CI and cannot count as user approval.

## Validate or extend

```sh
python3 -m unittest discover -s "$SKILL_ROOT/tests" -p 'test_*.py'
python3 "$SKILL_ROOT/scripts/selftest.py" --work "/absolute/new neutral test folder" --blender "/path/to/Blender"
```

Use [coverage/limits](references/verification.md). Do not rerender an accepted production MV to prove a helper change. Installation/discovery is a separate stable-library operation, not a symlink into a disposable job tree.
