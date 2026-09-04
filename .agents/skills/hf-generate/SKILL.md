---
name: hf-generate
description: Submit Higgsfield generations (video/image/3d/audio) via the RAW developer API with reference media, polling, and download — the proven path when the Blender plugin's own submission layer fails server-side. Use when generating Seedance/image/3D jobs from scripts, batch-generating video shots with blockout+character+style references, or when hf_fnf_video/plugin submissions fail.
---

# hf-generate — raw Higgsfield developer API submissions

Bundles `scripts/hf_gen.py` (curl-transport only — **Cloudflare 1010-bans
python urllib's TLS fingerprint, so every call shells out to the curl
binary**). **Why this exists:** the Blender plugin's own submission layer
(`hf_fnf_video`) failed server-side 4/4 on 2026-08-30 while the web UI
succeeded with identical media — the raw developer API works when the body
is the `{"params": {...}}` envelope. Sending fields flat gets
`422 extra_forbidden` on everything.

**Upload flow (proven 2026-08-30):** slot pattern, NOT multipart —
`POST /developer/v2alpha/media?type=K&extension=E` → presigned `upload_url`
→ PUT bytes → `POST /media/<id>/confirm?type=K` → media id. Multipart POST
to /medias gets Cloudflare 1010.

## Auth + workspace

- Token: the Blender plugin's session at
  `~/Library/Application Support/Higgsfield/Blender/auth.json`
  (`access_token` else `id_token`) — same file the bridge uses.
- Workspace header: `hf-workspace-id` (default
  `50d577d1-1f9f-407c-a0d7-3d786ca1f2db` — the plugin's pinned workspace).
  Without it: `400 Missing workspace id`.

## Run

```bash
python3 <skill-dir>/scripts/hf_gen.py video --job-type seedance_2_5 \
    --params-file shot_params.json \
    --image-ref <elias-media-id> --image-ref <barrio-media-id> \
    --video-ref <blockout-media-id> \
    --wait --timeout 1800 --download /abs/path/shot.mp4
```

- `--params-file` — JSON of job params (mode, prompt, duration, resolution,
  aspect_ratio, generate_audio...). Full param catalog per model:
  `bl_list_models({type, include_schema:true})` via the bridge.
- `--image-ref/--video-ref/--audio-ref` — media ids from prior uploads
  (uploaded media PERSISTS — reuse ids across shots; no re-upload).
- `--upload /path/file` — uploads new media first (multipart POST to
  `/developer/v2alpha/medias`) and wires the ids as references.
- `--wait` polls `/developer/v2alpha/jobs/<id>` every 15s; `--download`
  writes the result file locally.

## Proven reference stack (subo-a-sion, 2026-08-30)

- seedance_2_5 omni_reference: 10s/480p/16:9 = **25 credits** (job
  `381b55e3` completed, real footage).
- 30s/1080p/high-bitrate via web UI showed **270 credits** on the button.
- Failed jobs refund automatically (Manage Account → Usage).
- Keep upload files light (<2MB): the web UI tolerated 6-7MB refs; the API
  path was flaky until refs were compressed (unconfirmed cause, cheap rule).

## Prompt contract

Load the bridge's `higgsfield_read_seedance_prompts` BEFORE writing video
prompts: six-step formula, 60-100 word main block, one camera move,
positive phrasing only, end-state line, ratio from delivery.
