---
name: vision-read
description: Read an image with the local vision model (qwen3.8-27b-mlx@4bit via LM Studio) — headless pi with an @file attachment, no mega-minion needed. Use when you need to know what an image shows (screenshots of panes, UI states, game screens, diagrams) and the current model has no vision, or for any image the user asks you to look at.
---

# vision-read — local image reading (headless, no mega-minion)

Reads an image by calling pi directly with the local vision model. No pane,
no mega-minion — one command, stdout answer.

## When to use

- The user asks what an image shows (screenshots, pane states, UI, diagrams,
  game screens) and your model cannot see images (pi's read tool will say
  "Current model does not support images" — that note means the ACTIVE model
  lacks vision; use this skill instead).
- Any forensic image read where the content matters (verbatim text, layout,
  errors, unusual states).
- Do NOT use for: generating images, image editing, or vision the user
  explicitly wants on another model.

## How

```bash
# default (qwen3.8-27b-mlx@4bit — accurate, slow)
/Users/moses/code/bin/vision-read "/absolute/path/to/image.png" "optional prompt"

# fast but coarse (gemma-4-e2b — last-resort fallback only)
/Users/moses/code/bin/vision-read --fast "/absolute/path/to/image.png"

# explicit model for one call
/Users/moses/code/bin/vision-read --model lmstudio/qwen3.8-27b-mlx@4bit "/path.png"

# swap the model for a whole session without touching any file
VISION_MODEL=lmstudio/gemma-4-e2b /Users/moses/code/bin/vision-read "/path.png"
```

### Swapping the model

Resolution order (first match wins): **`VISION_MODEL` env var → `--model` flag → `--fast` → default qwen**. To make a model the permanent default, edit the `MODEL="..."` default line in `bin/vision-read` (or export `VISION_MODEL` in the shell profile). **Any swap target must declare image input** — add `"input": ["text", "image"]` to its entry in `~/.pi/agent/models.json` or pi bounces the attachment (see Troubleshooting).

The wrapper runs (env-cleared, so no PI_* overrides):

```bash
pi --print --no-session --no-tools \
  --model lmstudio/qwen3.8-27b-mlx@4bit \
  "@/absolute/path/to/image.png" "<prompt>"
```

- The `@<path>` argument is pi's file-attachment mechanism; image files are
  attached as images (auto-resized to 2000x2000 max).
- `--no-tools` keeps it a pure read (no tool-call detours).
- The image path must be absolute or relative to the caller's cwd.

## Model + patience (doctrine 2026-08-18)

- **Default: `lmstudio/qwen/qwen3.8-27b`** (full-precision) — user ruling
  2026-08-18: flipped from the 4-bit after the LOW-thinking timing test
  (full @ LOW = 3 min 28 s on a pane screenshot; 4-bit was the prior
  default). `lmstudio/qwen3.8-27b-mlx@4bit` remains the fast swap target.
- **`--fast`: `lmstudio/gemma-4-e2b`** — ~15s/image but coarse and MISREADS
  verbatim text (missed overlays, hallucinated percentages). Last resort only.
- qwen is a **reasoning model**: expect **2-4+ minutes per image** at
  LOW thinking. An empty or partial reply mid-reasoning is NOT a failure —
  the answer lands when the reasoning block closes. Callers MUST use a
  generous bash timeout (600s+).
- **Thinking effort — controlled ONLY by the LM Studio per-model UI toggle
  (verified 2026-08-18):** pi's `--thinking` flag is NOT transmitted to LM
  Studio (the request body carries no thinking param), and the API ignores
  `thinking: false` / `thinking: {type: disabled}` / `reasoning_effort`
  (reasoning tokens still fire — measured 12-20 on a trivial probe). So:
  keep the UI toggle at **LOW** for routine forensic reads (measured 5.5x
  faster than MAX with identical substance; residual glyph misreads on
  narrow/wrapped regions are caught by a verification pass); set it to
  **medium/xhigh only for deep-analysis tasks** (layout causality, golden
  diff judgment). `VISION_THINKING` env remains a passthrough for providers
  that accept per-request thinking.
- **max_completion_tokens:** pi sent 16384 for this provider (not the 60000
  the doctrine once assumed). Long reasoning can truncate — for deep
  analysis consider raising the model's maxTokens in models.json.
- If the read must be async, run it with nohup into a log and poll the log.

## Troubleshooting

- **"Current model does not support images"** on the read tool — the ACTIVE
  model lacks vision; route through this skill's headless call instead.
- **Image bounces even on qwen** — check `~/.pi/agent/models.json`: the
  model entry must declare `"input": ["text", "image"]` (pi gates image
  attachment on the model's declared input types; the 08-18 fix added it to
  both qwen entries). The `contextWindow` for qwen is 65000; `max_tokens`
  60000.
- **Empty stdout for minutes** — qwen is reasoning; wait. Check the LM Studio
  API is serving (`curl -s localhost:1234/v1/models`) if it never returns.
- **Vision must never be faked** — if qwen is down and gemma also fails,
  report "vision unavailable" rather than describing the image from
  assumptions. Local vision is always available in this setup (LM Studio).

## Ledger/ops notes

- This is the explicit-vision path replacing the old describe_image
  auto-delegation (removed 2026-08-18: it lied about its identity and
  silently delegated to text models). Vision is EXPLICIT — an agent asks for
  it when needed; it is never auto-injected.
- Perkins lens runs use this mechanism when a lens needs to verify a visual
  claim (T2 goldens, sprite bboxes) — the lens pane calls `vision-read` on
  the artifact and quotes the result as evidence.
