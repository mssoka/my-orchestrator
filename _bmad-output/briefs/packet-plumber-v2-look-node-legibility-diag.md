# Briefing — packet-plumber-v2-look-node-legibility-diag (READ-ONLY evidence job)

Skill to execute: **bmad-quick-dev** (diagnosis mode — NO production-code
edits in this job). Briefing is self-contained if the skill is absent.

## USER REPORT (verbatim, 2026-08-26 01:12)

"i can barely see the nodes even when zoomed in."

Screenshot (READ-ONLY reference, do not copy into the tree):
`/Users/moses/Desktop/Screenshot 2026-08-26 at 01.12.14.png`
KYLE screening read: router pucks read dark with thin muted rings; the
saturated pipes dominate; nodes recede against both the pipes and the
board. Screening only — pixel-verify everything.

## Context (second complaint on this axis — take it seriously)

- This is the user's FIRST session on v2 @0b2aeb9 (both viscomm merges
  live). Diff archaeology PROVES #99/#100 did not touch node drawing
  (visibility.odin = HUD gauges; view.odin +7 lines, gauge-related).
- Prior art: commit 9bf9797 "camera zoom tiers + node-vs-puck legibility
  rebalance" — puck base 1.15→1.05, PUCK_GROWTH_MAX=1.30, Dublin blocks
  0.40/0.22→0.55/0.30 — the response to the 08-23 directive ("even zoomed
  in I can barely see the buildings, routers are big"). The class of
  complaint RECURRED: the balance is still wrong.
- Zoom ladder (canon): DEFAULT_ZOOM 2.0 resting home / focus 2.3–2.6 /
  wheel-out floor 1.0. Nodes must read at ALL tiers, 2.0 first.

## Task: evidence, not vibes (deliverable = a proposal the user can SEE)

1. **Captures.** Build the app (main checkout is CLEAN on v2 @0b2aeb9 —
   build there is fine, do NOT commit). Capture frames at each zoom tier
   (2.0 default, 2.6 focus, 1.0 out) on a fixture with routers + terminals
   + pipes. Craft (field notes): macOS offscreen windows freeze the
   compositor — use movie mode (`--write-movie --fixed-fps`); harness only
   via tools/harness.sh with ODN_ROOT=the rlsw shadow (bare `odin build
   harness` = R/B-swapped frames).
2. **Pixel measurements (KYLE mega-minion, evidence-grade).** Spawn KYLE
   (model zai-coding-cn/glm-4.6v, pinned, probe first) in this cwd with
   the captures attached: measure node ring/puck luminance + saturation vs
   (a) the board, (b) adjacent pipes, (c) the tier-band colors; ring
   stroke thickness in screen px at each tier; puck size in px vs pipe
   width. KYLE craft: prompt to a FILE, absolute OUT paths, verify session
   modelId, read findings from DISK.
3. **Number the suspects** with evidence: puck base scale (1.05) /
   PUCK_GROWTH_MAX cap, tier-band stroke + brightness, ring alpha, pipe
   saturation overpowering nodes, building contrast at 2.0. Git archaeology
   for when each knob took its current value.
4. **Propose 2–3 rebalance directions** (e.g. minimum screen-space ring
   stroke, brighter tier bands / darker rim halo, slight pipe de-emphasis
   near nodes) each with a mocked side-by-side strip (current vs proposed)
   and the measured deltas. NO production-code edits.
5. **Lavish artifact** (named in Skills policy): one HTML page — the
   captures, the measurement table, the side-by-side proposals — so the
   user rules a direction in the browser.

## Ledger / reporting

- Row: `packet-plumber-v2-look-node-legibility-diag`. No PR (no code
  changes). Report: `ledger note` + `herdr notification show
  "packet-plumber-v2-look-node-legibility-diag" --body "<lavish url>"` —
  the notification is the completion signal (no-PR job doctrine).
- Preserve all captures/measurements under
  `_bmad-output/implementation-artifacts/look-node-legibility/` BEFORE
  any sweep.

## Model policy

- Minion: `zai-coding-cn/glm-5.3` (sole live provider), `--thinking max`.
- KYLE mega-minion: `zai-coding-cn/glm-4.6v` pinned explicitly (probe
  first; if 4.6v is DOWN, report vision-unavailable and ship the numeric
  pixel measurements only — never fake a visual verdict).

## Dispatch parameters

- repo: Packet-Plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: look-node-legibility-diag
- base: v2 (head 0b2aeb9 — READ-ONLY, build + captures only)
- branch: NONE (read-only job — no worktree branch needed; use the main
  checkout, touch nothing)
- model: zai-coding-cn/glm-5.3
- pr_review: 0 (no code — CI/ops-exempt class; the FIX job that follows
  carries pr_review=1)
