# Channel workflow amendment — reusable AI storyboards, Selva pilot only

**LIVE-GATE UPDATE:** user has now approved the initial 2–3-image pilot, US$5 TOTAL shared across both jobs. Read `/Users/moses/code/_bmad-output/briefings/gemini-storyboard-live-pilot-approval-2026-09-10.md`; it supersedes all pending-approval/zero-live-call clauses below. Deliver actual generated images for review, not another setup-only gate. Generic-skill/style/model and unrelated scope boundaries remain.

## User ruling

The user requested a Gemini image-generation skill and a documented repeatable music-video workflow for future channel projects, applied now only to Selva scenes not yet started. Explicit reminders:

> the prompt for the images, should reflect the style we want for the music video, not just random images....

> remember, this wont just be for Selva. so the skill should not be specific to Selva.

Latest explicit user model ruling: `model="gemini-3.1-flash-image"`. Pin that exact image-generation model in the channel workflow, template and pilot; do not select another model or alias.

The generic package is a SEPARATE orchestrator job `orchestrator-gemini-storyboard-skill`, canonical `.agents/skills/gemini-storyboard/`. You own the CHANNEL workflow and Selva pilot data, not its core implementation. No duplicated skill or Selva-only generator. Coordinate interface through Silas.

## Dispatch / ownership

Amend the existing `youtube-channel-selva-full-song-storyboard` row/pane w85:pNS and retained session/worktree. This expressly releases useful channel workflow/pilot-preparation work from its old editorial idle-await, not a new native/audio campaign. Preserve existing storyboards, caption attempts, completed manifests, review history and all unrelated work. Do not relaunch or clear the session merely for this amendment. No competing editor in this worktree.

pP5 remains sole native Selva producer, and current S47 pass04/CHECK06 is out of scope. Do not change its source, scenes, timings, guards, access or queue. PP3D play/publication may coexist with its authorized queue; not a blocker for this host/docs job.

## Deliverables

1. Update the CHANNEL `README.md` pipeline and create a reusable `docs/music-video-workflow.md` (or equivalent clear linked name):
   - song/lyrics analysis and evidence-bound timing;
   - treatment + shot list;
   - each video's own approved style bible and character/environment references;
   - reference-conditioned AI storyboard images: first a small representative consistency sample, human look verdict, then the wider board;
   - timed shot cards/contact sheet and, where useful, start/end illustrations for a transformation;
   - approved boards handed to native Blender blockout, assets/rigs, animation, lighting/rendering and assembly with actual motion/contact and look review gates.
   AI images are not geometry/rigs, final frames or animation proof. Gemini storyboard preparation does NOT revive the retired Higgsfield plugin/blockout-to-AI-video pipeline. Keep direct Blender MCP primary for native production. Existing other-video pipelines remain untouched.
2. A PORTABLE blank per-video input template matching the shared skill: project, own style/continuity canon, own cast/locations/references, shot/timing data, eligibility, output namespace, model/size and budget/review settings. All style values belong to each film; no Selva palette/moth/city/count/duration as the channel default. Clearly separate a Selva example from the reusable instructions. Demonstrate how another video changes only data, not code.
3. A separate Selva pilot package under `selva-electrica-mv/storyboard/` in a NEW versioned directory: compiled prompts, eligibility list with reasons/evidence, selected reference provenance/role/cloud-clearance status, and a proposal for 2–3 representative UNSTARTED shots for the initial style check. These are dry-run plans, not generated image claims.
4. Reviewable lavish channel-workflow + pilot-plan artifact before a documentation PR. It must distinguish generic process, per-video inputs and the one pilot. Show actual planned prompts and why they follow Selva direction; no decorative unrelated AI images. Poll only the new review session for this deliverable; do not reopen ended prior sessions or infer approval from silence. After explicit disposition, publish a focused docs/template PR against mssoka/youtube-channel main, preserving all existing untracked/native/editorial artifacts. Do not blanket-stage old work. No merge.

## Prompt/style contract

Every request combines a shared, versioned FILM style/reference block with the exact shot's causal story beat, character/object identities, environment, action, composition/lens/framing, lighting and continuity requirements. No "make a cinematic image" prompts, arbitrary moodboards, random changed cast, or unrelated styles. Reference files must actually be attached when live use is later authorized, not merely mentioned by path.

For Selva, read the LATEST ruled treatment/timing/production overlays and coordinate source-of-truth with pP5 through Silas. Earlier headers that say draft/proposal/no-audio are historical, not authority to undo later full-song approval. Existing sources include:
- Your `selva-electrica-mv/storyboard/{treatment.md,shotlist.csv,timing-revision.json,review-record.md,assets.json}` and `versions/timing-v03-20260909/`.
- Your full-film production/conform/manifest and final verdict overlay.
- pP5's read-only `selva-electrica-mv/spec/{SPEC.md,premium-hero.md}`, `production/full-film-v01/` and latest art/user-ruling receipts.
- Gru's `briefings/selva-full-film-production-2026-09-09.md`, `selva-charge-quality-ruling-2026-09-09.md`, `selva-check05-user-ruling-pass04-2026-09-10.md`.

Finished CHARGE is Selva's craft floor, NOT an aesthetic inherited by all future videos. Extract relevant approved craft language; do not copy/upload CHARGE screenshots or BMS assets under this brief. Held/rejected Selva frames are not silently promoted to final look canon. A retained city-layout approval can support geography continuity without claiming the plant finish was approved.

## Unstarted-only eligibility

Use actual shot-specific production evidence, not '0 final shots admitted' as a synonym for 'nothing started'. S47 is explicitly excluded. Preserve any other shot with native staging/animation/render work already begun, even if failed or unfinished. Shared assets or a textual plan alone do not necessarily establish every shot as started; distinguish them. Unknown status stays excluded pending ordinary owner reconciliation. No changing the existing 55-shot story, approved timing, cast, ongoing repairs or current production queue.

For future new videos, the board precedes scene production. The partial-retrofit/unstarted-only rule is the Selva pilot application, not a hard-coded list in the skill.

## Current financial / execution boundary

Google image guide: https://ai.google.dev/gemini-api/docs/image-generation ; pricing: https://ai.google.dev/gemini-api/docs/pricing . User says GOOGLE_AI_API_KEY is in ~/.zshrc. DO NOT read/print/copy the key or startup file, dump environment, change credential setup, or send any API call/reference upload now. Existing paid limit is $0; a separate explicit first-sample budget remains to be obtained. Draft the selected size for pinned `gemini-3.1-flash-image`, 2–3-shot selection, input/ref requirements and estimate with the core-skill owner, ready for one concise release decision. Do not park the documentation/parameter work on that future live-generation gate.

No Blender/Godot/native render/capture, new audio inference/alignment, asset acquisition, paid generation, model policy change or film publication in this amendment. No giant new process monitor or attempt-ticket infrastructure. Keep technical receipts proportional to a docs/dry-run task.

## Acceptance

- Generic workflow and blank template work for an unrelated music video with a different style/cast/timeline; Selva is visibly just the pilot appendix/data.
- Read-only eligibility and authority reconciliation preserves active/started scenes; actual status reasons provided.
- Pilot planned prompts demonstrably carry approved shared style + shot-specific beat/framing/reference IDs. Rendered-image/aesthetic success is NOT claimed before generation and visual inspection.
- Exact shared-skill commands/input shape are verified against its stable interface, not invented. Docs work proceeds in parallel; final integration can await interface handoff.
- Relative links resolve; template validates through the generic helper offline when available; no reference/secret/native artifact copied into the PR.
- User reviews workflow/pilot plan in lavish before the focused docs PR. `pr_review=0` for this documentation-only amendment; if implementation becomes necessary beyond small input/template data, route scope to Silas rather than silently expanding.

## Skills policy

Use the retained project's existing BMAD context, `bmad-spec` for a short durable workflow/input contract if needed, and `lavish` for the required docs review. Read the new `gemini-storyboard` skill when its owner supplies the stable path. Use `context7-docs` for exact API/interface documentation questions, not remembered SDK syntax. If meaningful implementation is genuinely required, invoke `bmad-build` once exactly as installed, with no framework repair/rebootstrap or workflow-source bypass; report a failure rather than manufacturing progress.

## Model policy

Retain the existing pNS `openai-codex/gpt-6-astra` / xhigh session. Visual/video helpers, if genuinely required, same Astra/xhigh with explicit provenance. No switch to unapproved general GLM routing; Gemini as the image backend is separate from agent-provider policy.

## Dispatch parameters

- job_id: youtube-channel-selva-full-song-storyboard (EXISTING row; do not create a short-id phantom)
- repo: youtube-channel
- repo_root: /Users/moses/code/youtube-channel
- github_repo: mssoka/youtube-channel
- worktree: /Users/moses/.herdr/worktrees/youtube-channel/selva-full-song-storyboard
- pane: w85:pNS (reverify live owner/session, preserve)
- slug: selva-full-song-storyboard (existing branch, no rebase/reset)
- base: main
- model: openai-codex/gpt-6-astra
- thinking: xhigh
- pr_review: 0
- coordinate_with: orchestrator-gemini-storyboard-skill; youtube-channel-selva-electrica-assets-rigs (read-only source/eligibility handoff)
- live_api_calls: 0 pending first-sample budget release

Silas executes/relays and verifies delivery; preserve pending editorial history. At completion or true review halt, use checklist-gated notification with actual pasted shown:true, report the exact new lavish URL/PR and state, and update the existing canonical row (including `ledger pr` when applicable). No native film-complete claim from this amendment.
