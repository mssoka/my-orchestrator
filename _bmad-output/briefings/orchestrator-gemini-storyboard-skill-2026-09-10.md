# Reusable Gemini storyboard-image skill — video-agnostic

**LIVE-GATE UPDATE:** user has now approved the initial 2–3-image pilot, US$5 TOTAL shared across both jobs. Read `/Users/moses/code/_bmad-output/briefings/gemini-storyboard-live-pilot-approval-2026-09-10.md`; it supersedes all pending-approval/zero-live-call clauses below. One real useful pilot run, not duplicate paid test campaigns. All generic-skill/style/model and unrelated scope boundaries remain.

## User authority and intent

User requested a reusable skill using https://ai.google.dev/gemini-api/docs/image-generation, said GOOGLE_AI_API_KEY is in ~/.zshrc, and requested integration into the channel's repeatable music-video workflow. Selva is a pilot for shots not yet started. Two explicit requirements:

> the prompt for the images, should reflect the style we want for the music video, not just random images....

> remember, this wont just be for Selva. so the skill should not be specific to Selva.

Latest user model ruling: `model="gemini-3.1-flash-image"`. Use that exact image-generation model, not a Pro/preview/older alias.

Create ONE generic `gemini-storyboard` skill, not a Selva helper later generalized. Film-specific direction is INPUT DATA. Do not hard-code Selva, its palette, cast, shot IDs/count, duration, FPS, source paths or craft references into runtime defaults. The separate channel workflow amendment carries the real Selva pilot.

Read the playbook's Minion standing orders. This is an orchestrator-root CODE job in a NEW isolated worktree from origin/main; never implement in Gru/Silas's live checkout.

## Deliverable and scope

Canonical package: `.agents/skills/gemini-storyboard/` with SKILL.md, a small runnable Python helper, input templates/reference notes, and offline tests. Follow existing skill packaging rather than building a service/framework. No duplicated implementation in youtube-channel.

The reusable contract must support:
- A named video/project and its own approved style bible: visual medium/shape language, palette, materials, lighting, composition/camera language, mood, continuity rules and exclusions. Missing direction is a useful validation error, not fallback to generic "cinematic" or to the last video's aesthetic.
- Per-video character/environment reference registry with stable IDs, role, provenance and permission for external API use. References actually condition the request, not merely appear as filenames in prose. Film-specific shared reference/style block plus per-shot story beat, subjects, action, location, framing and lighting form each prompt. Deliberate shot variation stays inside the chosen film direction.
- Shot IDs and supplied song/section/timing metadata; arbitrary film lengths/counts/aspects, optional start/end illustrations for transformations. Do not infer audio alignment or perform audio analysis in this skill. Timing may be unknown and must then be labelled, not invented.
- Explicit shot eligibility: existing shot-specific production is preserved; started/unknown statuses cannot silently enter an unstarted-only run. New projects supply their own plan/status manifest. No Selva-specific status exception in the core.
- Offline dry-run/validation that emits inspectable prompts, selected/excluded shots and planned configuration without credentials or network. Live execution is a separate explicit action.
- A small initial style/character-consistency sample, a real image review, then wider storyboard generation only after that look verdict. Generated images are storyboard/look targets, not native geometry/rigs, animation or completed film proof.
- Per-video/per-run outputs, prompt and reference hashes, model/config, usage metadata, image hashes, attempt/result status and review disposition. Preserve revisions; no silent overwrite or cross-film cache/reference bleed. Contact-sheet/shot-card output should pair exact images with IDs/timing/beat and clearly mark mocks/dry-run as NOT generated images.

## Gemini API and credential requirements

Use the official Google Gen AI Python SDK and current official docs. Explicitly map environment `GOOGLE_AI_API_KEY` into the client; the SDK's default variable names differ. Never read/print the contents of ~/.zshrc in a tool response, copy its key to a file, accept a key in argv, log auth headers, include it in exceptions/receipts, or put it in a browser artifact. Prefer inherited environment. Document safe launch from the user's existing configured shell; do not edit shell startup/config or dump the environment.

Research already completed by Gru:
- Official image guide: https://ai.google.dev/gemini-api/docs/image-generation
- Official SDK: https://github.com/googleapis/python-genai (Context7 ID `/googleapis/python-genai`). Current indexed README uses `client.models.generate_content(model='gemini-3.1-flash-image', config=types.GenerateContentConfig(response_modalities=['IMAGE'], image_config=types.ImageConfig(aspect_ratio='9:16')))`. Some image-guide snippets use newer/different `response_format` syntax: VERIFY against the exact installed SDK, do not splice incompatible snippets together.
- `types.Part.from_bytes(data=..., mime_type=...)` can carry image references; the helper must validate actual images/MIME itself.
- `HttpRetryOptions(attempts=1)` disables implicit SDK retries. Use bounded request timeouts and explicit recorded retries; do not silently resubmit after an ambiguous timeout and assume it was free.
- Skip `part.thought` intermediate images when identifying final boards. Handle text-only/safety-blocked/no-image/malformed responses honestly. Preserve relevant finish/safety/usage information without raw secrets or a giant raw-response dump. For multi-turn edits, the SDK must preserve required thought signatures; a simpler explicit single-turn reference-conditioned revision path is acceptable and preferable to a fragile custom chat implementation.
- Usage exposes prompt/candidate/total/thought and per-modality token counts. Preserve unknown usage/cost on interrupted requests; an estimate is not an actual bill.
- Pricing source: https://ai.google.dev/gemini-api/docs/pricing . Check actual selected model/size/current rates. Do not infer free generation from an API key or a free-tier heading.

Pin the implemented generation model to `gemini-3.1-flash-image` per the explicit user ruling; carry it in examples, request builder and receipts. Aspect/size remain per-video configuration with supported combinations validated. No alternative model selection or fallback without a later explicit user amendment. Gemini is the image-generation backend; this does NOT change pi agent model routing.

## Spending and data boundary

This implementation stage authorizes public documentation/SDK work and offline/mock verification, not billed image calls. Existing video production paid cap is $0; no Gemini live call, quota/auth probe, reference upload or paid batch under this brief. Implement explicit per-run attempt/spending controls and dry cost estimates, with date/source and uncertain-input caveats; execution must require a positive user-approved budget. Do not overengineer a new process-identity/scheduling subsystem.

Only explicitly selected, cloud-cleared reference images may be sent when live generation is later released. Local/external reference permissions do not automatically mean upload permission. Do not download/upload/copy CHARGE, BMS or other third-party assets for this job. No Blender/Godot/native render, game capture, paid service, publishing or legacy Higgsfield/Comfy/MLX pipeline changes.

## Acceptance / verification

1. Same helper runs completely offline for TWO synthetic video fixtures with contrasting styles, casts and timing. Changing only input data changes the complete planned prompts/references/output namespace; neither fixture needs Selva files. No Selva identifiers/style leakage in shared runtime/templates.
2. Required style and shot/story fields reach the actual request builder. Missing style, wrong/missing reference, unsupported config and started/unknown selection are exercised as failures. Mechanical tests prove prompt assembly, not aesthetic compliance.
3. Mock actual SDK call boundary: valid final image versus thought image; refusal/text-only/no-image; malformed bytes; transient/ambiguous timeout; usage known/unknown; resume/revision no-overwrite; attempt/budget limit; secret-redacted error. Test dry-run with no key and no transport call. Include representative mutation/negative legs for the key guards; never label mock bytes as live Gemini evidence.
4. Verify request serialization with the installed SDK offline, record its version and exact supported API shape. No live request hidden in a test/help path.
5. SKILL.md is discoverable/portable and all relative references resolve from its directory, including from a different cwd. Read Pi skill docs fully and relevant .md cross-references before authoring. Generic example invocation, workflow steps, input template and setup/cost caveats are usable by a fresh future-video agent.
6. Relay a compact interface/path/example command to Silas for the channel workflow owner as soon as stable. The channel owner may consume it read-only; each writer owns its own repository/files.
7. Open a normal focused code PR against mssoka/my-orchestrator main; pr_review=1. No merge or live-root sync/deployment claim. Report tested-offline status and outstanding live pilot explicitly.

## Skills policy

- Implementation: `bmad-build` at `/Users/moses/code/.agents/skills/bmad-build/SKILL.md`; invoke its render command exactly once from the actual worktree without changing cwd. Read the returned workflow on success; report output and HALT on failure. No source-workflow bypass, repair or rebootstrap campaign.
- API documentation: `context7-docs`; official image/pricing links above.
- Pi skill authoring: read installed Pi README + docs/skills.md completely and related .md references; Agent Skills format https://agentskills.io/specification.
- bmad's prescribed review layers are required; use the installed canonical review skills/templates rather than invented shorthand. `lavish` for any actual visual review. This package is a code deliverable with regular PR review; the separate channel documentation goes through lavish before its PR.

## Model policy

This is a visual/video-generation workflow: minion and any visual/review helpers `openai-codex/gpt-6-astra`, thinking `xhigh`. Explicitly pin and verify model/thinking on launch. No default-provider reliance, legacy detour or broader model-policy change. Do not dispatch a helper simply to read an image that native Astra can inspect itself.

## Dispatch parameters

- job_id: orchestrator-gemini-storyboard-skill
- repo: orchestrator
- repo_root: /Users/moses/code
- github_repo: mssoka/my-orchestrator
- slug: gemini-storyboard-skill
- base: main
- worktree: REQUIRED new worktree from origin/main; live root remains untouched
- model: openai-codex/gpt-6-astra
- thinking: xhigh
- pr_review: 1
- coordinate_with: youtube-channel-selva-full-song-storyboard (interface relay only, no shared edits)
- live_api_calls: 0 until separate explicit image budget/first-sample release

Silas: pin the exact job id in handover and real ledger columns; bootstrap only established environment prerequisites. Minion completion must report PR via `ledger pr` plus in-review, actual offline checks and remaining limitations. Fire the checklist-gated notification with pasted shown:true and relay to Silas. Preserve artifacts and do not close other owners' sessions.
