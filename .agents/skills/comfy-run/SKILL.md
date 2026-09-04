---
name: comfy-run
description: Submit ComfyUI workflows (frontend or API format) to a running ComfyUI server with surgical input overrides, video-reference chains, polling, and output download — repeatable local generation (MiniMax H3, Wan, LTXV, etc.). Use when the user wants to generate video/images in ComfyUI, queue a workflow by API, compare local-model output against cloud models, or asks about driving ComfyUI headlessly.
---

# comfy-run — drive ComfyUI via its HTTP API

Bundles `scripts/comfy_submit.py` (stdlib only). ComfyUI's built-in HTTP API
(default `http://127.0.0.1:8188`) is the driver — no MCP needed; MCP wrappers
just proxy the same endpoints.

## Prerequisites

- ComfyUI Desktop/server RUNNING (`curl -s http://127.0.0.1:8188/system_stats`).
- Input assets in the shared input dir (default
  `/Users/moses/ComfyUI-Shared/input`) — `LoadImage`/`LoadVideo` combo lists
  only see files there. Copy or symlink first.
- Outputs land in `/Users/moses/ComfyUI-Shared/output` (or `--download DIR`
  to fetch via the `/view` endpoint instead).

## Run

```bash
python3 <skill-dir>/scripts/comfy_submit.py WORKFLOW.json \
    --set 137.image=subo_elias_sheet.png \
    --set 139.image=subo_barrio_style.png \
    --set-file 138.value=@/abs/path/prompt.txt \
    --set 132.value=10 \
    --add-video 136.ref_videos.ref_video_0=/abs/path/blockout.mp4 \
    --wait --timeout 1800 --download /abs/path/outdir
```

- `WORKFLOW.json` — a template/frontend-format workflow (nodes+links) OR an
  API-format graph. Frontend format is converted automatically.
- `--set NODE.FIELD=VALUE` — applied AFTER conversion by API input name;
  values coerced to bool/int/float/string. This is the surgical patch layer.
- `--set-file NODE.FIELD=@path` — same but reads the value from a file
  (prompts live in files, never inline).
- `--add-video NODE.FIELD=path` — inserts `LoadVideo → GetVideoComponents`
  and wires the IMAGE-frames output into a `ref_videos.*` slot (MiniMax H3
  R2V pattern: the slot takes video FRAMES (IMAGE), not a VIDEO type).
- `--wait` polls `/history/<prompt_id>` until success/error and prints the
  output file list; `--download DIR` also fetches each output via `/view`.

## Hard-won format lessons (do not relearn)

1. **Templates are FRONTEND format** (nodes + links); `POST /prompt` needs
   API format (`{id: {class_type, inputs}}`). The converter handles:
   - widget defs shaped `[[options...],{meta}]` (COMBO) and `[[type,{meta}]]`
   - `input_order` (not dict merge) = authoritative widget order
   - linked params keep stale widgets → consume-and-discard by position
2. **MarkdownNote nodes are frontend-only** — always stripped.
3. **`ref_videos.*` slots take IMAGE frames** — never link a VIDEO output
   directly; always through `GetVideoComponents`.
4. **Autogrow input names** are dotted: `ref_images.ref_image_0`,
   `ref_videos.ref_video_0` — link by exact name.
5. Validation errors come back per-node with exact input names — read them,
   fix `--set`, resubmit. Two failures on the same defect = change approach.

## MiniMax H3 R2V reference setup (subo-a-sion proven)

- Template: `video_minimax_h3_r2v.json` (shipped in
  `comfyui_workflow_templates_json/templates/`).
- Core node `MiniMaxH3ReferenceToVideo` (id 136): prompt via
  PrimitiveStringMultiline (its field is `value`), width/height via
  ResolutionSelector, frame count `length` (124 ≈ 5s @24fps; 240 ≈ 10s;
  trained range ~124-362), `ref_image_size: match`.
- Local models (user's install): `minimax_h3_ref2va_pruned_int8_convrot`
  + `qwen3vl_32b_minimax_h3_nvfp4_awq` CLIP + video/audio VAEs.
- Lightning turbo 4-step LoRA exists in the template but is DISABLED by
  default (Boolean False) — full 20 steps. Enable only for fast drafts.
