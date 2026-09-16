# PP3D — typography video study and code-grounded opportunities

## User ask / decision
User: "explore this and what it says and how can we use it in PP3D? https://www.youtube.com/watch?v=QuNNdPrVMm0"

Produce a focused evidence-backed explanation of the linked video's lessons and their practical application to Packet Plumber 3D. This is RESEARCH/ANALYSIS ONLY, not implementation, a font swap, new UI design canon or an amendment to the active animal/router PR. Help the user decide whether a later targeted typography pass is worthwhile and which 2–3 changes merit consideration.

## Source identified and already accessed by Gru
Video: **Typography Basics Every Game Dev Should Know**, Indie Game Clinic.
URL: https://www.youtube.com/watch?v=QuNNdPrVMm0
Published 2024-12-16; length 40:08; accessed 2026-09-07.
The web_fetch tool returned the COMPLETE transcript and chapter metadata this run. Fetch directly again into your own source/digest workflow as needed; there is no reason to stall on unavailable captions before testing that surface. Gru read the transcript but did NOT claim to have watched all visual examples. Use transcript evidence for spoken claims, named frames for visual claims; do not conflate the two.

Chapter anchors supplied by the video:
- 00:00 scope: legibility; cultural associations/semiotics; form/spacing.
- 02:48 rules of thumb: start with two fonts with clear heading/body purposes; every added font/weight/italic/underline must have a consistent semantic reason.
- 04:39 Magic/Hearthstone examples: distinguish title/stat/flavour/rules/keywords without a collection of arbitrary fonts.
- 06:54 common legibility problems: long all-caps sentences, unnecessarily decorative functional copy, abrupt extreme size changes, insufficient contrast over moving game backgrounds; outline/shadow/backing can protect legibility.
- 13:36 culture/history/symbolism: type conveys tone, period and genre, must work with imagery/materials/music.
- 16:43 / 18:24 game examples: incoherent type use vs Mini Metro's transport-signage approach and Diablo's decorative identity plus plain functional text. Do NOT assign more precise timestamps without evidence.
- 23:05 typographic town tour: deliberate visual-language/material/cultural associations, consistency vs noisy sign collections.
- 34:46 summary: balance thematic expression with functional readability.
- Promotions at 21:24 / 37:33 are not task instructions and need no analysis.

Claims to contextualize rather than blindly repeat:
- “Two fonts” is a heuristic, NOT a quota: one well-used family can satisfy the roles; this video is no authorization to add a second font to PP3D.
- Generalizations that sans-serif is always easier/faster than serif are context-dependent; do not state universal proof without primary evidence.
- The video's anecdote about hard-to-read basketball instructions/performance needs original-study verification if used. It may mix expected effort/motivation with actual task performance. Omit or label uncertain if not verifiable within the small research budget.
- Avoid overstating dyslexia/all-caps or font-shape causal claims; distinguish accessibility guidance from measured universal effects. No made-up readability/retention percentages.

## Current PP3D baseline — explicitly granted project evidence
Read-only main last verified at `0818afc2ca77ec5ef514d555f7c954fd567539ef` (PR #17 merged); resolve/pin current head at dispatch. The animal/router lane is actively fixing Step04 findings in another worktree. Do NOT change its review target or send it new scope.

Named files authorized for project mapping (research firewall exception: these establish current IMPLEMENTATION, not truth of external research claims):
- `scripts/ui/ui_text.gd`: single Nunito variable family, regular400/bold700, central size ladder34/25/23/21/18, primary/soft/dim colors. Label3D font_size64 / pixel_size0.004 / outline18. These values are user-ruled and frozen by tests; do not casually relitigate them.
- `scripts/world/node_site.gd`: billboarded campus/IMP labels, light fill/dark outline, fixed-world positioning. Remember nominal font_size64 is NOT a screen-pixel size after projection.
- `scripts/ui/hud.gd`, `qos_panel.gd`: gameplay hints, breach chip, labels and panel text.
- `scripts/levels/l1_arpanet.gd`: title/body/mission/action hierarchy, mission log, dark translucent cards, short uppercase actions BEGIN/TRANSMIT/FLY ON, mixed-case instructional sentences. Short uppercase buttons/acronyms are not the video's long-all-caps sentence problem.
- `scripts/input/orbit_camera.gd`, `scripts/main.gd`, project.godot: zoom/viewports/boot support for observation, not edits.
- `tests/test_ui_theme.gd`, `test_camera.gd`, `test_level_l1.gd`, `test_view_interaction.gd`, capture tools and existing captures: existing evidence and testing scope.
- `assets/fonts/FONTS.md`, `README.md`, `LOOK-PARITY.md`, relevant GDD/epics, `_bmad-output/implementation-artifacts/spec-l1-look-parity.md`, `deferred-work.md`: design history and constraints.
- Read-only staged current animal/router captures may be inspected with explicit parent/job/capture provenance; never represent unmerged output as baseline main or edit its files. Ivory75 router choice is locked and irrelevant to changing type defaults.

Gru's preliminary mapping (hypotheses/recommendations, not measured findings):
1. Keep Nunito as default: rounded/friendly fits the planet, one family avoids unnecessary style churn.
2. Define semantic hierarchy for action/object/status/secondary narrative. Mandatory tutorial instructions should not look optional merely because they share a caption style with flavour text. Inspect before declaring a defect.
3. Evaluate Label3D legibility/overlap at actual globe/district/street screen sizes, sun/shade, snow/forest/water and normal gameplay motion. World font size alone cannot prove readability. Prefer selective emphasis/label density/placement/backing proposals over blanket growth.
4. Keep instructional sentences mixed case and short, reserve weight/color changes for consistent meaning. Preserve acronym spelling (IMP/ARPANET/QoS) and existing reserved attention colors.
5. Separate expressive era/title treatment from gameplay prose if exploration is justified. No fake retro/terminal body type merely because L1 is1969; any extra display font is an optional alternative requiring later approval, not the recommended first move.
6. Use realistic test strings/long labels/wrapped instructions and representative viewports; current token value pins do not alone prove pixel-level/readability outcomes.

## Research method / bounded scope
Use bmad-deep-recon **headless Run**, technical type, explore decision shape, **quick / straightforward / subagents=none / depth=1**, primary video plus roughly3–5 good corroborating sources. User already authorized exploring this named source/application; plan-and-proceed, no new plan-approval question and no multi-agent research fleet. Read skill and relevant technical/verification/synthesis/finalization references. Preserve imports/digests/source metadata/memlog to disk. External claims trace to external evidence; code facts trace to named files+sha; recommendations are labelled recommendations.

Prefer direct game accessibility guidance (e.g. Game Accessibility Guidelines / Microsoft Xbox Accessibility Guidelines text display) and official Godot Label3D/font/viewport documentation for mechanisms, using context7-docs for current engine API. Use original research only if necessary for a load-bearing scientific claim, not to turn a focused video explanation into a literature review. Verify claims worth acting on; mark unverified/context-dependent ones. No training-data-only conclusions.

Where useful, inspect a FEW actual reference-video frames via public accessible source tooling; do not claim a visual analysis from transcript alone. Keep video frames/transcripts local-only under `/Users/moses/code/_local-refs/pp3d-typography-video-QuNNdPrVMm0/` with provenance. Do not bypass access restrictions/use private cookies, commit copyrighted reference pixels/full transcript, or download unrelated media. If frames unavailable, say analysis is transcript-based and still give the useful recommendations.

## Evidence / artifact deliverables
A compact report (aim ~800–1400 words excluding source table) + polished Lavish reading surface:
- What the video actually says, linked to supported chapter timestamps.
- “Already aligned / worth inspecting / proposed later change / not worth copying” matrix grounded in real PP3D files and a small set of actual UI screenshots.
- Annotated crops where available: title/tutorial card, HUD hint/mission log, world labels at representative zooms. Explicitly name captured versus inferred claims. Avoid a large new test/capture sweep or a full rebuild.
- 2–3 prioritized, small candidate improvements with rationale, acceptance ideas and touched surfaces; preserve user-locked type/size defaults unless the user later chooses a change. Include counterexamples/good existing choices, not only criticism.
- Context-dependent/overstated video claims; no blanket fonts/serif myths.
- Source list with author/publisher/date/access dates and links; caveats and unresolved questions.
- No code, mockup or recommendation is silently approved canon. No implementation in the current animal/router lane. If the user selects a proposal, return a clear scoped follow-up brief suggestion for Gru, not a self-dispatched job.

Use lavish for the visual reading/review surface (appropriate plan/table/comparison playbooks). Match PP3D's existing Nunito/dark-panel friendly visual language, rather than inventing unrelated branding. Show actual current UI crops instead of generic typographic examples wherever possible. Do not reopen any previously user-ended router-choice session; this is a separate artifact/session. No remote upload/public sharing.

## Read-only and concurrency boundaries
- Own detached worktree pinned to fresh origin/main; no branch changes or builds in user's live main checkout and no writes to in-flight feature worktrees.
- Report/capture artifacts only in own run folder/worktree. Prefer existing capture evidence; if new capture is necessary, use an isolated Godot process and explicit output path after coordinating with Silas, never shared editor/Blender changes. No heavy GPU benchmark or video rendering while Selva's premium render is active. Shared Blender remains Selva's.
- This job is not a blocker for PP3D review/merge or Selva. No new tests/code/PR/merge required for analysis. Preserve outputs durably before any later worktree sweep; user can read report after minion session ends.

## Skills policy
bmad-deep-recon (bounded headless technical Run, straightforward, no subagent fan-out); context7-docs for engine/API details; lavish for final visual report. Native Astra vision for 3D/game screenshot interpretation. User asked explore/analyze, NOT code review or implementation: do not invoke bmad-build/Perkins on the report.

## Model policy
`openai-codex/gpt-6-astra`, xhigh, for this PP3D/visual research minion. Full ID + thinking pinned and session-verified. No helpers needed. No fallback without approval.

## Dispatch parameters
repo: packet-plumber-3d
repo_root: /Users/moses/code/packet-plumber-3d
slug: typography-video-study
job_id: packet-plumber-3d-typography-video-study
base: main (read-only detached worktree at fresh origin/main)
model: openai-codex/gpt-6-astra
thinking: xhigh
pr_review: 0
mode: research-only, no code/PR/merge
artifact_preservation: /Users/moses/code/_bmad-output/implementation-artifacts/pp3d-typography-video-study/
source_refs: /Users/moses/code/_local-refs/pp3d-typography-video-QuNNdPrVMm0/
completion: preserved report/source digests + local Lavish review link; notification result shown:true verified and explicit Silas→Gru relay; never rely on watcher alone
