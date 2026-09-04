---
name: mlx-video
description: Generate video locally on Apple Silicon with LTX-2 (Metal-native, MLX) — text-to-video and image-to-video at production spec. Use when the task is local video generation, the LTX lane, rerolls/iterations of local clips, or batch local production. Covers the one-time setup (convert flow + loader patches), prompt guards learned from artifacts, and the production envelope.
---

# mlx-video — the local LTX-2 lane

Metal-native video generation via the `mlx-video` library (LTX-2 19B distilled, audio+video DiT). Proven 2026-08-30: 4s @ 1920×1088 ≈ 10 min, 0 credits, unlimited rerolls.

## Layout & one-time setup

- Clone: `/tmp/mlx-video` (it's a LIBRARY — run from the clone dir, `uv run ...`).
- Model: convert the HF monolith to the modular layout ONCE, then generate from it:
  ```
  uv run python -m mlx_video.models.ltx_2.convert \
    --source <hf-snapshot-dir|monolith.safetensors> \
    --output /tmp/mlx-video/LTX-2-distilled --variant distilled
  ```
  Convert symlinks text_encoder/tokenizer (no extra disk). Output = transformer/, vae/{encoder,decoder}, audio_vae/, vocoder/, latent_upsampler/, connectors/.
- **Loader patches (LOCAL to the clone, needed for the HF checkpoint dialect):**
  1. `ltx_2.py from_pretrained`: filter config_dict to declared `LTXModelConfig` annotations (HF config carries `_class_name`/`_diffusers_version`).
  2. `ltx_2.py sanitize()`: the stock version early-returns unless keys have `model.diffusion_model.` — the HF layout then gets ZERO renames (1,680 "extra" params). Patch = unconditional normalization: `.norm_q.→.q_norm.`, `.norm_k.→.k_norm.`, `.to_out.0.→.to_out.`, `.ff.net.0.proj.→.ff.proj_in.`, `.ff.net.2.→.ff.proj_out.`, `.audio_ff.*` same, `.linear_1/2.→.linear1/2`, `.*_a2v_cross_attn_scale_shift_table→.scale_shift_table_a2v_ca_*`, plus 8 ANCHORED (startswith) top-level renames: `time_embed.→adaln_single.`, `audio_time_embed.→audio_adaln_single.`, `av_cross_attn_{video,audio}_scale_shift.→av_ca_{video,audio}_scale_shift_adaln_single.`, `av_cross_attn_{video_a2v,audio_v2a}_gate.→av_ca_{a2v,v2a}_gate_adaln_single.`, `proj_in.→patchify_proj.`, `audio_proj_in.→audio_patchify_proj.`.
  3. A fresh re-clone needs both patches re-applied (check upstream first — may be fixed).
- **Verify BEFORE burning GPU** (header-only, no weight loads): read safetensors headers (8-byte len + JSON), `tree_flatten(model.parameters())` vs `sanitize(ckpt keys)` → must be extra:0 / missing:0.

## Generate (production template)

```
uv run mlx_video.ltx_2.generate \
  --model-repo /tmp/mlx-video/LTX-2-distilled \
  --prompt "<shot prompt> , steady exposure, consistent lighting throughout, cinematic, full frame, no border, no film strip, no text" \
  [--image <anchor.png>]            # I2V: anchor IS the first frame; aspect MUST match target dims
  --pipeline distilled -n 97 --width 1920 --height 1088 \
  -o <vault>/<name>.mp4             # ALWAYS -o to the vault — default output.mp4 gets overwritten
```

## The rules (each cost an artifact to learn)

- **Dims ÷64** (VAE blocks): 1920×1088 is the 16:9 pick (1080 not divisible) — crop 4px top/bottom in the edit → exact 1920×1080.
- **Prompt guards — MANDATORY:**
  - `steady exposure, consistent lighting throughout` — kills the reproducible tail-darkening drift.
  - `full frame, no border, no film strip` + NEVER write "35mm film/grain" at T2V — the model renders literal sprocket-hole film-strip borders. (I2V anchors suppress it; guard anyway.)
- **Frames**: 24fps → 49f=2s, 97f=4s, 145f=6s, 193f=8s. Retention doctrine: 97–145f.
- **Two-stage distilled pipeline**: stage-1 diffuses at HALF res (8 steps), stage-2 latent-upsamples — that's the speed. `--spatial-upscaler` path (x2 file in repo) = alternative: generate 960×544, upscale after.
- **I2V anchors**: the image is the literal first frame. Character-sheet turnarounds confuse it — crop ONE view. MCU anchors for character tests. Anchoring an in-scene still (mflux/img2img) beats a studio sheet; a studio anchor transitions to the prompted scene in ~20 frames (cuttable).
- **Identity in prompt**: name the canon traits every time (locs tied back, grey-flecked beard, olive field jacket, chevron patch...). Proven: face holds through a 90° gaze turn at MCU.

## Production envelope (M-series, measured)

| Setting | s/frame | 97f wall | peak mem |
|---|---|---|---|
| 768×512 smoke | ~1.2 | ~1 min | 37.5GB |
| 1024×1024 | ~2.7 | ~4.5 min | 39.3GB |
| 1920×1088 production | ~6.1–6.5 | ~10 min | 43.4GB |

Batch math: 20 production clips ≈ 3.5–7h sequential GPU. Run batches with `tools/local_production.py` (state file, one-at-a-time GPU discipline, vault outputs).

## Disk & download hygiene

- HF cache hoards every variant: keep ONLY distilled monolith + distilled-lora + spatial/temporal upscalers; purge dev/fp4/fp8 blobs (freed 117.5G when disk hit 99%!). `df -h /` before any big pull.
- Killed downloads leave corrupt `.incomplete` blobs → `rm -rf ~/.cache/huggingface/hub/models--Lightricks--LTX-2` and retry cleanly. `HF_HUB_ENABLE_HF_TRANSFER=1` helps; free tier still throttles ~60–250s/file.
- ComfyUI/H3 lesson (why this lane exists): 20–30B models crawl on Metal through emulated quantized kernels (1000s/step) — MLX-native is the only viable local path on this Mac.

Field notes: `/Users/moses/code/youtube-channel/tools/mlx-lane-notes.md` — log every new quirk here.
