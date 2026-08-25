# Kyle — You OWN the lavish session now (handoff from minion, 2026-08-22)

## Your role now
You are the **lead design analyst** for the Packet Plumber v2 visual design audit. The user wants to chat with YOU directly through the lavish review session. From now on YOU poll the session, reply to feedback, apply changes to the report, and iterate. The minion (your orchestrator) is out of the feedback loop except for capture/measurement support.

## The report + session
- Report: `/Users/moses/.herdr/worktrees/packet-plumber/packet-plumber-v2-design-audit/_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/design-audit.html`
- Session: `http://127.0.0.1:4387/session/423cdcfbe00f9a41` (lavish server on 4387 is UP)
- MM refs server: `http://127.0.0.1:4388/mm/Mini-Motorways-images/…` (4388 is UP — you restarted it earlier today; files live in `/Users/moses/code/_local-refs/mm/Mini-Motorways-images/`)
- To work: `cd /Users/moses/.herdr/worktrees/packet-plumber/packet-plumber-v2-design-audit/_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit` then `npx -y lavish-axi poll design-audit.html`
- To reply/iterate: `npx -y lavish-axi poll design-audit.html --agent-reply "<message>"`
- NEVER kill a poll; if it times out (~600s), re-run it — feedback stays queued. One foreground poll at a time.

## Your design directions (already written)
`/Users/moses/.herdr/worktrees/packet-plumber/packet-plumber-v2-design-audit/_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/kyle-design-directions.md` — 6 sections (scale, palette/POP, identifiability, motion, spawn, shadows/depth) each with Current / MM Target / Proposed Direction / Evidence. This is your source of truth.

## All user feedback accumulated so far (the session's review history)
1. Routers/terminals "need to look better like MM" (job briefing, 08-21).
2. Node types not identifiable at a glance (job briefing).
3. Terminal spawn feels too frantic (job briefing).
4. Packets move too fast to follow (job briefing).
5. "I don't see the new folded-in suggestions in the screenshots/images" → minion added annotated evidence sheets (blur-hue-deltas, palette-harmony-share, depth-haze-mock) — done.
6. "I still don't see these colours popping… networking is boring so we need to make it pop… has to make good attention-grabbing thumbnails" → minion measured saturation ceiling (ours 0.51–0.57 vs MM 0.91–1.00), added POP test + pop-mock + thumbnail-test. Done.
7. "I still don't see the sample images showing the expected outcome" → minion embedded the actual MM press-kit frames in a new "expected outcome" section. Done — user then said "the saturation looks better".
8. **CURRENT (latest feedback, needs your response):** "the saturation looks better, but I also noticed that the houses are smaller in MM vs PP. We need that as well. They used shadows to create depth. Houses have smaller shadows and the buildings have larger shadows. Also while we're at it, compare the background maps as well. And also the art."

## What the latest feedback requires of you
The minion already measured (stats in your design-directions.md §1 and §6):
- Scale: our house = 36px (3.2× band), campus = 53px (4.7× band); MM house ≈ 0.5–1.0× road width. **The user is right.**
- Shadows: MM = soft drop shadows offset down-right, scaling with building size; ours = uniform 0.64w×0.36w ellipse at 16% ink under every node.
- Background map: MM image_01 = 51% plain paper / 26% water / 11% warm land tint; ours = 34% canvas / 49% water / 9% park.
- "And also the art": this is the router/terminal/puck sprite-art read vs MM's minimal flat buildings (your Q1 + silhouette directions).

Your job now: respond to the user in-session, and FOLD these into the report as a designer-facing spec (per area = current state vs MM target vs exact proposed direction — concrete hexes, sizes, ink %, offsets). The user makes the design changes THEMSELVES, so the report must read as an actionable spec, not findings.

## Hard guardrails (do not break)
- ZERO code changes to the game repo. The diff must stay empty. The ONLY writable area is `_bmad-output/implementation-artifacts/packet-plumber-v2-design-audit/` (report + captures + your md files). No `git add/commit`. Do NOT edit app/, core/, data/, tools/, harness/.
- MM assets must NEVER enter the repo. The report references them via `http://127.0.0.1:4388/mm/…` only. You may measure them with Python (stats), but never copy MM image bytes into the artifact dir.
- Keep captures at the pinned sha (8639d5f) — every capture is already sha-labeled; do not regenerate unless you re-verify at the same sha.
- The report is the deliverable. No PR, no commit.

## Design-direction format for the report (audience = the user, who will implement)
For each area (scale, shadows/depth, background map, art/silhouettes, plus your existing 6):
- **Current** (with measured numbers + which capture shows it)
- **MM Target** (with which MM image + measured numbers)
- **Proposed Direction** (EXACT: hex pairs with 70/30 weighting, pixel targets, ink %, offsets, durations) — write it so a designer can implement without asking.
- Keep the IN-ENGINE vs BLENDER decision table.

## First actions
1. Poll the session now (`npx -y lavish-axi poll design-audit.html`) — the user is waiting to chat with you.
2. When feedback arrives, reply in-session AND update the report HTML.
3. Keep the loop: poll → respond → edit → poll again with `--agent-reply`.
