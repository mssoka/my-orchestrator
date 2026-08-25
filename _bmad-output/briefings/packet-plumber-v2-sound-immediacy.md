# packet-plumber-v2-sound-immediacy

## Task

AUDIO job, user-directed, OUT of the visual audit's scope (listed for
completeness; DIRECTION.md §3 — Brush's two audio rules: immediacy +
frequency stack). Every interaction should fire immediate feedback:

- wire placed (pipe placed → instant click/confirm)
- node spawn (telegraph + reveal → soft chime, matches the visual
  telegraph the spawn-feel job adds)
- crisis (surge → alert sting)
- packet delivery (subtle tick per delivery — frequency stack: sound
  density scales with traffic, so busy boards hum)

## Rules (hard)

1. The audio consumer already exists (7.2 event→sound map) — extend the
   map; do not build a new audio system.
2. Sounds are short, non-fatiguing, low-latency (immediacy).
3. Visual wave (jobs 1–6) is NOT a dependency — but time the node-spawn
   chime to the telegraph the spawn-feel job adds (coordinate after
   both land).
4. No visual/palette changes.

## Acceptance

- Event→sound map extended: wire, spawn, crisis, delivery all fire.
- Latency/immediacy verified (sound within ~50 ms of event).
- Local suite green.
- pr_review: 1 (Perkins before merge).

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-sound-immediacy
- base: v2
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe with everything (audio layer; coordinates spawn chime
  with v2-spawn-feel after merge)
- source of truth: DIRECTION.md §3 + design-audit.html sound note
