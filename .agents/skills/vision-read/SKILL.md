---
name: vision-read
description: Read an image with the KYLE vision model (zai-coding-cn/glm-5.3-flash — the ops tier's native multimodal, headless pi with an @file attachment, no mega-minion needed) for quick-reads, or spawn a KYLE visual-verification mega-minion for evidence-grade checks. Use when you need to know what an image shows (screenshots of panes, UI states, game screens, diagrams) and the current model has no vision, or for any image the user asks you to look at.
---

# vision-read — KYLE vision (quick-read + visual-verification)

KYLE doctrine (2026-08-21 user ruling; the AGENTS.md 'Vision = KYLE' block is
canon): vision is EXPLICIT — never faked, never delegated to a blind text
model. Two modes:

- **quick-read** — THIS skill's headless tool (`bin/vision-read`): one
  command, stdout answer. No pane, no mega-minion.
- **visual-verification** — a full **KYLE mega-minion** spawned in the
  summoning repo/worktree cwd with tools (read/grep/bash); it reads the
  render code / goldens / tests and answers with evidence. Use when a
  visual claim is evidence-grade (golden diffs, render captures, layout or
  geometry truth) — a blind quick-read is not enough.

When the active reasoning model is k3, or the session model is
`zai-coding-cn/glm-5.3-flash` (natively multimodal, verified 2026-08-27
through pi with a registered `input: ["text","image"]` entry — the first
GLM-5-series flash with native vision, user ruling), vision is INLINE — no
spawn, read the image directly with the read tool / @file attachment.
Otherwise (glm-5.3 / deepseek are blind) route through this skill.

## When to use

- The user asks what an image shows (screenshots, pane states, UI, diagrams,
  game screens) and your model cannot see images (pi's read tool will say
  "Current model does not support images" — that note means the ACTIVE model
  lacks vision; use this skill instead).
- Any forensic image read where the content matters (verbatim text, layout,
  errors, unusual states).
- Evidence-grade visual verification (goldens, captures, geometry) → Mode 2.
- Do NOT use for: generating images, image editing, or vision the user
  explicitly wants on another model.

## Mode 1 — quick-read (headless tool)

```bash
# default (zai-coding-cn/glm-5.3-flash — KYLE, standing since the 2026-08-27
# native-multimodal ruling; 4.6v demoted to fallback)
/Users/moses/code/bin/vision-read "/absolute/path/to/image.png" "optional prompt"

# explicit model for one call
/Users/moses/code/bin/vision-read --model zai-coding-cn/glm-4.6v "/path.png"

# LOCAL last resort only (lmstudio/google/gemma-4-e2b — coarse, misreads verbatim text)
/Users/moses/code/bin/vision-read --fast "/absolute/path/to/image.png"

# swap the model for a whole session without touching any file
VISION_MODEL=zai-coding-cn/glm-5v-turbo /Users/moses/code/bin/vision-read "/path.png"
```

### Swapping the model

Resolution order (first match wins): **`VISION_MODEL` env var → `--model` flag → `--fast` → default glm-5.3-flash**. To make a model the permanent default, edit the `MODEL="..."` default line in `bin/vision-read` (or export `VISION_MODEL` in the shell profile). **Fallback when flash is down: `--model zai-coding-cn/glm-4.6v`** (the pre-08-27 standing pin). **Any swap target must declare image input** — add `"input": ["text", "image"]` to its entry in the models registry (`~/.pi/agent/models.json` overrides / `models-store.json` catalog) or pi bounces the attachment (see Troubleshooting).

The wrapper runs (env-cleared, so no PI_* overrides):

```bash
pi --print --no-session --no-tools \
  --model zai-coding-cn/glm-4.6v \
  "@/absolute/path/to/image.png" "<prompt>"
```

- The `@<path>` argument is pi's file-attachment mechanism; image files are
  attached as images (auto-resized to 2000x2000 max).
- `--no-tools` keeps it a pure read (no tool-call detours).
- The image path must be absolute or relative to the caller's cwd.

## Mode 2 — visual-verification (KYLE mega-minion)

Spawn KYLE as a full mega-minion when the visual claim needs evidence:

- **Spawn cwd = the summoning repo/worktree** (codebase access: read/grep/
  bash on the real render code, goldens, tests). Never a bare cwd.
- **Model pinned: `zai-coding-cn/glm-5.3-flash`** (the ops pin — probe first;
  fallback `--model zai-coding-cn/glm-4.6v` if flash is down).
- **Prompt carries summon-reason + pointers**: what to verify, which files
  render the artifact, where goldens/tests live, what evidence to produce
  (pixel scans, hashes, diff output) — never "look at this and tell me".
- **Image attached via @file** (absolute path).
- Pane naming: `<job-slug>-kyle` in a descriptive tab; close the pane when
  done.

Prompt skeleton:

```
You are KYLE, the vision mega-minion. Summon reason: <what must be proven>.
Image: @<absolute path to capture/png>
Verify against the codebase in this cwd: <render path>, <golden paths>, <test
paths>. Answer with EVIDENCE (pixel scans, byte/hash diffs, geometry checks),
not vibes. Never describe what the image "probably" shows — if the pixels
don't prove it, say so.
```

## Probe-first rule

Before ANY vision call on glm-4.6v (quick-read or KYLE spawn), probe the
model with an env-cleared pi one-liner:

```bash
env $(env | grep '^PI_' | sed 's/=.*//;s/^/-u /' | tr '\n' ' ') \
  pi --model zai-coding-cn/glm-4.6v -p --no-session -nt "Reply OK"
# expect: OK
```

If 4.6v is DOWN: **stop and escalate** — never proceed on a blind model.
A text model cannot substitute for vision; reporting a description you
cannot verify is fabrication. (Same for the `--fast` local fallback: if
both are down, report "vision unavailable".)

## Model + patience (doctrine 2026-08-21)

- **Default: `zai-coding-cn/glm-5.3-flash`** — KYLE, the standing vision model
  since the 2026-08-27 ruling (ops tier + native multimodal; fast, 1M
  context, and registered with `input: ["text","image"]`). The
  evidence-grade bar is the METHOD (pixel scans, hashes, geometry — never
  vibes), not the model.
- **`--fast`: `lmstudio/google/gemma-4-e2b`** — LOCAL last resort (~15s/
  image but coarse and MISREADS verbatim text: missed overlays,
  hallucinated percentages). Never default.
- glm-4.6v is a **reasoning model**: expect **up to a few minutes per
  image**. An empty or partial reply mid-reasoning is NOT a failure — the
  answer lands when the reasoning block closes. Callers MUST use a generous
  bash timeout (600s+).
- **Thinking effort:** `VISION_THINKING` env passthrough (default low) —
  routine forensic reads are perception, not reasoning.
- If the read must be async, run it with nohup into a log and poll the log.

## Troubleshooting

- **"Current model does not support images"** on the read tool — the ACTIVE
  model lacks vision; route through this skill's headless call instead.
- **Image bounces even on glm-4.6v** — check the models registry
  (`~/.pi/agent/models.json` override / `models-store.json` catalog): the
  model entry must declare `"input": ["text", "image"]` (pi gates image
  attachment on the model's declared input types).
- **Empty stdout for minutes** — glm-4.6v is reasoning; wait. If it never
  returns, re-probe (the model may have gone down mid-flight).
- **Vision must never be faked** — model down or probe failing → report
  "vision unavailable" / escalate rather than describing the image from
  assumptions.

## Ledger/ops notes

- This is the explicit-vision path replacing the old describe_image
  auto-delegation (removed 2026-08-18: it lied about its identity and
  silently delegated to text models). Vision is EXPLICIT — an agent asks
  for it when needed; it is never auto-injected.
- Perkins lens runs use quick-read (Mode 1) when a lens needs to verify a
  visual claim (T2 goldens, sprite bboxes) — the lens pane calls
  `vision-read` on the artifact and quotes the result as evidence.
  Evidence-grade verification (render geometry, golden diffs) goes to KYLE
  (Mode 2).
