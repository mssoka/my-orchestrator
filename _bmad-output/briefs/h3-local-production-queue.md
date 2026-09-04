# Briefing: h3-local-production-queue

**Job:** own the LOCAL MiniMax H3 production queue for the Subo a Sion music
video — drive, watch, repair, and verify ~24 clip generations in ComfyUI,
scene by scene, until every scene has usable local footage. This is a
long-running background lane (~27 GPU-hours over days). The user has
explicitly chosen the local lane for cost (cloud covers ~13% of their
publishing cadence).

## Gate (do this first)

The mechanical proof job `ae7efe3a-2635-4101-9b78-4248774abb1b` is landing
NOW (5s, 832×480, turbo LoRA, mp4/h264). Verify BEFORE starting the queue:
1. `curl -s http://127.0.0.1:8188/history/ae7efe3a-2635-4101-9b78-4248774abb1b`
   → status success with an output mp4.
2. The mp4 exists under `/Users/moses/ComfyUI-Shared/output/` (SaveVideo
   default prefix `video/MiniMax_H3`; find the newest). Extract 3 frames
   (ffmpeg), LOOK at them: must show the pre-dawn barrio + the climber
   figure — NOT black, NOT garbage.
3. If black/failed: apply the playbook's black-output branch, then re-gate.

## The lane (proven mechanics)

- ComfyUI on `http://127.0.0.1:8188` (Comfy Desktop — must stay open).
- Skill: `comfy-run` (`~/.agents/skills/comfy-run/SKILL.md`) — its
  `scripts/comfy_submit.py` submits + patches + waits.
- Proven graph: `tools/h3_queue/s1_graph_proven.json` (the S1 R2V graph:
  Elias + barrio refs + blockout-video chain + duel prompt, 832×480).
- Per-shot settings: `--set 132.value=<seconds> --set 146.value=true
  --set 92.format=mp4 --set 92.codec=h264`
  (turbo Lightning LoRA 4-step ALWAYS on; format+codec ALWAYS explicit —
  never let them default).
- Expect ~17 min/step → ~68 min per 10s clip, ~35 min per 5s clip. That's
  normal on this machine (emulated quantized kernels). Do NOT "fix" the
  speed by changing models — H3 class is the user's ruling.

## Shot plan (B+ doctrine — 24 clips)

Per scene, cut 10s excerpts from that scene's blockout video
(`subo-a-sion-mv/renders/blockouts/scene_XX_blockout.mp4`) with ffmpeg
(overlap ok), upload each excerpt into ComfyUI's input dir
(`/Users/moses/ComfyUI-Shared/input/`), then submit a variant of the S1
graph with: the scene's prompt (from `subo-a-sion-mv/prompts/scene_XX.txt`),
the new ref video, Elias + barrio image refs UNCHANGED.

| Scene | Clips | Segments (from blockout) |
|---|---|---|
| S2 verse1 | 3 | 0-10 / 7-17 / 15-25 |
| S3 chorus1 | 3 | 0-10 / 11-21 / 22-32 |
| S4 verse2 | 4 | 0-10 / 10-20 / 20-30 / 30-40 |
| S5 chorus2 | 3 | 0-10 / 9-19 / 18-28 |
| S6 ridge | 3 | 0-10 / 9-19 / 17-27 |
| S7 bridge | 2 | 0-10 / 10-20 |
| S8 drop | 2 | 0-10 / 5-15 |
| S9 final | 4 | 0-10 / 10-20 / 20-30 / 30-40 |
| S10 outro | 2 | 0-10 / 7-17 |

Per scene's clip N: duplicate the proven graph, replace the
`LoadVideo.file` path, replace the prompt text (node
PrimitiveStringMultiline `value`), and set a distinct SaveVideo
`filename_prefix` like `subo_s04_c2`. Submit ONE AT A TIME (the machine
runs one job). Poll via the watcher pattern (see comfy-run docs; do NOT
block on long sleeps inside the agent session — use short polls between
other work).

## Failure playbook (all seen live 2026-08-30)

| Symptom | Cause | Fix |
|---|---|---|
| MPS OOM in text encoder (~29.8 GiB alloc) | 32B CLIP spike | shorten length (124f), close GPU-heavy apps, retry; if persistent, 832×480 confirmed-safe |
| `SaveVideo missing 'format'` | converter dropped dynamic-combo | `--set 92.format=mp4 --set 92.codec=h264` always |
| `avcodec_send_frame() returned 22` | bad container/codec pair | the explicit mp4+h264 pair fixes it |
| Pure black output (mean 0.0) | stale cache / degenerate latents | resubmit (RandomNoise randomizes); if black AGAIN, drop the turbo LoRA for that clip and accept 20 steps |
| SaveVideo keeps failing | PyAV quirks | SaveImage bypass (swap node to SaveImage, ffmpeg-assemble the PNGs at 24fps) |
| Job stuck >2x expected time | wedged | POST /interrupt, resubmit fresh |

## Verification standard (per clip)

After each clip lands: copy it to
`subo-a-sion-mv/renders/local/scene_XX_cN.mp4`, extract 3 frames
(start/mid/end), LOOK at them (you have native vision on flash):
composition follows the scene's blockout? the Climber reads (olive
jacket/backpack figure)? not black/garbage? Log verdict per clip in
`renders/local/LOG.md` (one line: clip, verdict, notes). Failed clips get
ONE playbook repair + resubmit; second failure = mark `LOCAL-FAIL` in the
log and move on (do not loop).

## Additional duty: cloud-lane verification

A SEPARATE cloud production driver (Gru-launched) is downloading Seedance
1080p clips into `subo-a-sion-mv/renders/cloud/` (22 clips, LOG.md there).
As clips land, verify each with the same frame-check standard (3 frames,
composition/Climber/not-black) and append verdicts to
`renders/cloud/VERIFY.md`. Cloud failures/repairs stay with Gru — you only
WATCH and VERDICT, never resubmit cloud jobs.

## Reporting

- After EVERY scene completes: one line in `renders/local/LOG.md` +
  `herdr notification show "h3-queue" --body "scene XX done (N/M clips)"`.
- Final: `herdr notification show "h3-queue" --body "LOCAL QUEUE COMPLETE:
  X/24 clips usable, Y failed"` and stop.
- Never touch: the Seedance/cloud lane, the .blend files, git commits
  (leave the tree dirty for Gru to review), other scenes' graphs.

## Skills policy

`comfy-run` (submissions), `vision-read` (inline on your model for frame
checks). No dispatches, no mega-minions without asking Gru first.

## Model policy

You run `zai-coding-cn/glm-5.3-flash --thinking max` (ops tier, natively
multimodal — vision checks are inline, no vision skill needed).

## Dispatch parameters

- repo: youtube-channel
- repo_root: /Users/moses/code/youtube-channel
- slug: h3-local-production-queue
- base: main
- model: zai-coding-cn/glm-5.3-flash
- worktree: NO (in-repo; writes only under subo-a-sion-mv/renders/local/)
- note: youtube-channel is a studio repo created this session, not yet in
  managed-repos.txt — this dispatch is by explicit user instruction
  ("assign to a minion", 2026-08-30).
