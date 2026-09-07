---
name: vision-read
description: Read an image with the native GPT vision route (Astra for 3D, Sol for non-3D helpers) through a headless pi with an @file attachment, or use KYLE as a visual-verification role for evidence-grade checks. Use when the current model cannot accept images, when a headless read is needed, or for any image the user asks you to inspect.
---

# vision-read — KYLE vision (quick-read + visual-verification)

KYLE doctrine (the 2026-09-07 GPT-chain ruling; the AGENTS.md vision block
is canon): vision is EXPLICIT — never faked, never delegated to a blind text
model. Current native-vision routing is:

- **3D/game/Blender work and 3D visual verification** →
  `openai-codex/gpt-6-astra` (Astra), `xhigh`.
- **Non-3D helper reads** → `openai-codex/gpt-5.6-sol` (Sol), `xhigh`.
- **Silas/COO** → `openai-codex/gpt-5.6-luna` (Luna), `max`.

Attach images inline on those GPT sessions; no vision spawn is needed. KYLE
remains a role for evidence-grade visual verification or a dedicated visual
specialist when useful. KYLE's provider follows the current role policy; it
is not a hard-coded legacy GLM route. Legacy visual models are explicit,
probe-verified fallbacks only.

Two modes:

- **quick-read** — THIS skill's headless tool (`bin/vision-read`): one
  command, stdout answer. No pane, no mega-minion.
- **visual-verification** — a full **KYLE mega-minion** spawned in the
  summoning repo/worktree cwd with tools (read/grep/bash); it reads the
  render code / goldens / tests and answers with evidence. Use when a
  visual claim is evidence-grade (golden diffs, render captures, layout or
  geometry truth) — a blind quick-read is not enough.

## When to use

- The user asks what an image shows (screenshots, pane states, UI, diagrams,
  game screens). If the active GPT-chain model supports images, attach the
  image inline; if it does not, use this skill (pi's read tool will say
  "Current model does not support images").
- Any forensic image read where the content matters (verbatim text, layout,
  errors, unusual states).
- Evidence-grade visual verification (goldens, captures, geometry) → Mode 2.
- Do NOT use for: generating images, image editing, or vision the user
  explicitly wants on another model.

## Mode 1 — quick-read (headless tool)

```bash
# default: native GPT vision, Astra/xhigh (3D-safe default)
/Users/moses/code/bin/vision-read "/absolute/path/to/image.png" "optional prompt"

# non-3D helper read: select Sol/xhigh explicitly
/Users/moses/code/bin/vision-read --model openai-codex/gpt-5.6-sol \
  "/absolute/path/to/image.png" "optional prompt"

# explicit 3D/KYLE-role read: select Astra/xhigh explicitly
/Users/moses/code/bin/vision-read --model openai-codex/gpt-6-astra \
  "/absolute/path/to/image.png" "optional prompt"

# LOCAL last resort only (coarse; never the policy default)
/Users/moses/code/bin/vision-read --fast "/absolute/path/to/image.png"

# swap the model for one call/session without touching any file
VISION_MODEL=openai-codex/gpt-6-astra /Users/moses/code/bin/vision-read "/path.png"
```

### Swapping the model

Resolution order (first match wins): **`VISION_MODEL` env var → `--model` flag → `--fast`/`--local` → default `openai-codex/gpt-6-astra`**. The default is Astra/xhigh for 3D-safe routing; select `openai-codex/gpt-5.6-sol` @ xhigh explicitly for non-3D helpers. To make a model the permanent default, edit the `MODEL="..."` line in `bin/vision-read`. Any swap target must declare image input — `input: ["text", "image"]` in the models registry — or pi bounces the attachment (see Troubleshooting). Legacy visual models may be selected only explicitly after authorization and a successful probe.

The wrapper runs (env-cleared, so no PI_* overrides):

```bash
# Select Astra for 3D, or Sol for a non-3D helper before invoking.
pi --print --no-session --no-tools \
  --thinking xhigh --model openai-codex/gpt-6-astra \
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
- **Model pin follows the current GPT policy:** Astra/xhigh for 3D
  verification, Sol/xhigh for non-3D verification. KYLE is the role, not a
  hard-coded provider. Use a legacy visual model only as an explicitly
  authorized, probe-verified fallback.
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
Model: <openai-codex/gpt-6-astra for 3D | openai-codex/gpt-5.6-sol for non-3D>
Verify against the codebase in this cwd: <render path>, <golden paths>, <test
paths>. Answer with EVIDENCE (pixel scans, byte/hash diffs, geometry checks),
not vibes. Never describe what the image "probably" shows — if the pixels
don't prove it, say so.
```

## Probe-first rule

Before a new headless vision route or KYLE spawn, probe the selected remote
model with an env-cleared pi one-liner (Astra for 3D, Sol for non-3D):

```bash
env $(env | grep '^PI_' | sed 's/=.*//;s/^/-u /' | tr '\n' ' ') \
  pi --model openai-codex/gpt-6-astra --thinking xhigh -p --no-session -nt "Reply OK"
# expect: OK
```

If the selected model is DOWN: **stop and escalate** — never silently route
to a legacy model. A text model cannot substitute for vision; reporting a
description you cannot verify is fabrication. Local fallbacks are explicit
and must be disclosed; if no authorized vision route is available, report
"vision unavailable".

## Model + patience (doctrine 2026-08-21)

- **Default: `openai-codex/gpt-6-astra` @ `xhigh`** — native multimodal
  GPT, chosen as the safe default for 3D/Blender evidence. Use
  `openai-codex/gpt-5.6-sol` @ `xhigh` explicitly for non-3D helpers. The
  evidence-grade bar is the METHOD (pixel scans, hashes, geometry — never
  vibes), not the model.
- **KYLE** is a visual-verification role that may use the policy-selected
  GPT model; it is not a legacy GLM default. Legacy visual models and
  `--fast`/`--local` fallbacks are explicit and disclosed only.
- Astra/Sol are native multimodal GPT models. An empty or partial reply
  mid-reasoning is NOT a failure — the final answer lands when the reasoning
  block closes. Callers MUST use a generous bash timeout (600s+).
- **Thinking effort:** `VISION_THINKING` env passthrough (default `xhigh`)
  — the GPT policy pins Astra and Sol to xhigh.
- If the read must be async, run it with nohup into a log and poll the log.

## Troubleshooting

- **"Current model does not support images"** on the read tool — the ACTIVE
  model lacks vision; route through this skill's headless call instead.
- **Image bounces even on a GPT model** — check the models registry
  (`~/.pi/agent/models.json` override / `models-store.json` catalog): the
  model entry must declare `"input": ["text", "image"]` (pi gates image
  attachment on the model's declared input types).
- **Empty stdout for minutes** — the selected model may still be reasoning;
  wait. If it never returns, re-probe the exact model (it may have gone
  down mid-flight).
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
