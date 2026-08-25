# packet-plumber-v2-design-audit

## Task

Visual design audit of the CURRENT Packet-Plumber v2 build (Odin
renderer, post-look-polish PR #75) against the Mini Motorways (MM)
aesthetic bar. User feedback from a live play session (2026-08-21
~23:5xZ, the fun-test gate speaking):

1. Routers and terminals "need to look better like Mini Motorways".
2. "It's not clear which node is what" — node-type identifiability is
   failing at a glance.
3. Terminals "popping up too frequently" — spawn cadence FEELS frantic
   (audit the visual/feel side; the rate fix itself is a separate job).
4. Packets move too fast to follow — audit how the motion reads
   visually (the pace fix itself is a separate job).

Deliverable: a lavish report the user reads to decide (a) what
in-engine polish to order, and (b) whether a NEW Blender design pass
is needed — the user will launch the Blender session themselves if the
verdict says so. NO code changes in this job.

## Rules (hard)

1. Capture FIRST, from this worktree at the recorded sha (base v2
   @head): run the game and capture stills + short clips (or frame
   sequences) covering routers, terminals, each node type, packets in
   motion, and a terminal spawning. Reuse the capture approach the
   look-polish job used (see PR #75 artifacts / its session; MCP
   screenshot or the in-repo capture harness — whatever it used).
   Label every capture with the sha. Do not audit from memory.
2. KYLE (vision mega-minion) does the looking — the summoning minion
   may be blind. Spawn via the herdr mega-minion pattern on
   `zai-coding-cn/glm-4.6v` (standing vision model; probe first with
   the env-cleared pi probe — if DOWN, STOP and escalate via Silas,
   do not proceed on a blind model). Visual-verification mode: full
   agent with --cwd at the repo worktree, image files attached
   (@file), read/grep/bash access to the render code. Prompt carries
   the questions + pointers into the code. This is the 2026-08-21
   user ruling on Kyle, exercised by v2-look-polish — same recipe.
3. IP guardrail: NO fetching, downloading, or embedding actual Mini
   Motorways assets. MM reference = Kyle's trained knowledge of the
   game's aesthetic + the user's verbal target only. `_local-refs/mm/`
   on disk has NO frames (README only) — do not invent paths to it.
4. Ask Kyle, per capture set: (a) routers/terminals vs the MM bar —
   shape language, palette, shadow/AA, weight; (b) node identifiability
   — can each node type be told apart at a glance, what does MM do
   (shape+color coding, restraint) that we don't; (c) how does packet
   motion read (choppy? blur? trail-less?); (d) how does terminal
   spawn cadence feel in the captures.
5. Verdict section (mandatory, user decision input): IN-ENGINE vs
   BLENDER — for each problem area, does the fix live in code
   (palette, shapes drawn by the renderer, pacing) or does it need new
   art assets from a Blender pass? Be explicit; the user launches
   Blender only if this says so.
6. Preserve the report + captures to
   `_bmad-output/implementation-artifacts/` (no-PR job: the artifact IS
   the deliverable). Fire `herdr notification show "<job-id>"` with a
   one-line summary on finish (verify shown:true).

## Acceptance

- Lavish artifact: captures embedded, per-question Kyle verdicts with
  evidence pointers, the IN-ENGINE vs BLENDER table, recommended next
  jobs list. Reviewed by the user in-browser.
- Zero code changes (diff empty).
- Notification fired + shown:true; artifacts preserved.

## Skills policy

bmad-quick-dev (workflow shell only — this is an audit/report job);
lavish for the deliverable. Kyle mega-minion for all image reading.

## Model policy

Minion: deepseek-v4-flash, --thinking max. Kyle (vision mega-minion):
zai-coding-cn/glm-4.6v (probe-gated; escalate if DOWN).

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-design-audit
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 0 (no PR; report deliverable — notification +
  preserved artifact are the completion signals)
- parallel-safe with packet-plumber-v2-pace-tuning (audit pins its
  sha; the pace job's unmerged branch never reaches this worktree's
  runtime)
