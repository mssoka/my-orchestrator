# Configuration and commands

`python3 "$SKILL_ROOT/scripts/mv.py" <stage> --config "/absolute/job.json" [--blender "/path/to/Blender"]`

Only `serve --delivery /absolute/copied/delivery --port 0` works without a job config. The CLI prints compact result/receipt pointers; complete facts, manifests and native logs remain on disk. No Herdr, fixed pane or fixed port dependency.

## Config

Paths resolve relative to the **config file**, not cwd. `output` must be a fresh/versioned owned directory; inputs must exist outside it. Never place outputs inside the installed skill. Original music is external/read-only, never copied or packed.

- `version`: integer1. `title`: display title, not a file-name template.
- `music`: original stereo44.1/48kHz source. Actual decoded samples—not container duration—drive the frame budget.
- `art.mode`: `recipe`, `scene`, or `loop`. Every mode records `theme`, `direction`, `palette_rationale`.
  - `recipe`: `recipe=radial-relief`, `segments`4–48, `palette` with sRGB hex `shell/accent/key/rim`, numeric `key_watts/rim_watts`.
  - `scene`: `scene_file` plus exact `scene_name`. Opaque square-pixel16:9, sRGB/FOLLOW_SCENE, intended camera, no VSE/speaker audio. Original native input is preserved.
  - `loop`: picture-only H264/sRGB movie in `loop_file`, measured matching fps/size/frame count, with `approval.loop` provenance. All3D work is skipped.
- `video`: integer `fps`, even16:9 `width/height`, integer `crf`0–30 (default16), `samples`1–512 (default32), optional `max_audio_seconds`1–1800. Video width at most3840. Source Cycles settings remain native; the samples helper configures EEVEE.
- `loop.frames`:8–3600. Native-scene start frame is retained; exactly this many frames encode, next endpoint is diagnostic only. No implicit retiming to fit an input movie.
- `thumbnail`: zero-based `frame_index` within the loop; `width` for16-bit PNG and `jpeg_width` for JPEG. Widths are multiples of16,64–7680; height follows16:9. Loop-only intake can upscale, explicitly reported as no new detail.
- `approval.direction`, `approval.full_song`: actual authority/provenance strings, not empty defaults or synthetic feedback. `test_only` is a boolean reserved for synthetic validation; it skips owner checks but labels results TEST_ONLY.
- `reserve_gib`: at least36; native runtime stops on a real free-space breach two GiB lower. No arbitrary ETA kill. Buffered metadata correction separately refuses files above2GiB.

## Stages

1. `inspect`: validate config/tools/Blender version, decode/probe inputs, measure duration/fps/colour, establish the owned source/config/helper fingerprint and frame budget.
2. `preview`: recipe/supplied-scene native artwork, four small still phases, low-resolution complete motion cycle, editable `.blend`.
3. `review --stage preview --note "..."`: record actual observations/evidence. The agent can do this under existing creative authority; no routine user gate.
4. `loop`: one finite native loop export plus native endpoint test/full decode/unique-frame/seam checks. Then actual review with `review --stage loop`.
5. `assemble`: hash-identical owned picture, real native VSE project, one original cached sound, contiguous full/fractional picture strips. Reopen and native diagnostic from sample-zero through measurable audio. Inspect its picture, then `review --stage assemble`.
6. `export`: reopen the exact source, validate links/cut/cache/colour, native H264/AAC full-song export. No3D full-song rendering or shell assembly.
7. `thumbnail`: native PNG/JPEG and editable still setup; dimension/decode checks. Artwork look is retained, not recoloured for branding.
8. `verify`: full decode/frame-phase/join/audio alignment/end/gain/clipping checks. Measurements do not mean visual acceptance or listening.
9. `package`: copied byte-checked delivery, local player, native editing ZIP, thumbnail, notes, `reproduce.json`, manifests. Original song and rejected attempts/private snapshots are excluded. The native ZIP preserves relative picture links; external music/assets require their originals.
10. `serve --port 0`: loopback URL printed after binding. After actual playback/player/colour/audio review, use `review --stage package`; its separately appended `delivery/owner-review.json` binds the unchanged payload manifest. Deliver locally; never publish automatically.

For a moved package use `serve --delivery /absolute/copied/delivery --port 0`; it verifies payload hashes without relying on the old job path. `reproduce.json` uses the bundled loop and a **new** output root; re-link the same original song before reuse. To redesign art, use native scene intake instead.

## Recovery

Completed native stages are reused only after source/config/helper and artifact hashes match. Existing unowned output and changed resume inputs are refused. Failed attempts remain under `attempts/`; `--retry` creates a new attempt rather than overwriting one. Missing completion receipts—even with a movie-looking file—are not success.

`worker.lock` records supervisor/worker PIDs. Inspect those processes and terminal/progress logs first. `--clear-stale-lock` refuses to clear any lock whose recorded process is alive. Do not kill healthy renders for an early ETA, and do not run parallel jobs against the same output. Serialize host resources across separate jobs externally; there is no global scheduler/database.

The CLI does not grant asset rights, invent reviews, install software, mutate global preferences, pack original audio, contact paid services, publish, or manage identity panes.
