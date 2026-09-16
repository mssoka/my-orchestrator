# Official Kimodo-SOMA — bounded humanoid-motion exploration

## Research-return correction (2026-09-08)

The earlier SMPL-X-only C++ support premise below was DISPROVEN. Current `localai-org/kimodo.cpp` at568b0253f346fbe369587c7dae73d58594a14c90 supports SOMA RP/SEED v1.1 as30-joint motion, CPU/Vulkan and skeleton-only GLB; no general constraints,77-joint expansion or skinned-mesh export. Gru independently fetched this pinned README after the research return. Port execution/Mac compatibility remain untested and unadopted. Do NOT transfer official Python's x86 MotionCorrection build blocker to the C++ port without evidence. Reported official pipeline findings: commercially permitted SOMA motion-model terms with separately licensed/gated Llama, missing local runtime/assets, stock x86 correction build versus arm64 and unmerged MPS PR; NO model generation/retarget/render run. Full durable result: `/Users/moses/code/_bmad-output/implementation-artifacts/kimodo-soma-exploration/research.md`. This paragraph corrects the evidence, not authorization for install/download/acceptance or a new execution lane.

## User authorization / decision

User accepted shortlisting official Kimodo-SOMA and now says: “ok, explore soma.” Explore whether it is a practical, rights-compatible source of human walking/turning/reaction/groove motion for Selva Eléctrica and later published/monetized YouTube animation. It is NOT the moth collision solution, a requirement for the parallel full-song storyboard, or a committed studio pipeline.

Deliver a short source-backed recommendation plus a concrete smallest proof path. Prefer actual evidence over speculative compatibility claims. Research first; run a tiny local demonstration only if every already-authorized prerequisite below is present. Do not turn this into weeks of installation/porting/tool infrastructure. No unrelated platform comparison or full character kit.

## Ground truth / claims to verify this run

- Earlier research found `localai-org/kimodo.cpp` supports SMPL-X22, not SOMA. The code Apache license does NOT license all weights/body assets/outputs. Research/non-production SMPL-X checkpoint is NOT an acceptable default for published channel footage, even unmonetized.
- Official upstream: https://github.com/nv-tlabs/kimodo . Distinguish the Kimodo motion model, its SOMA checkpoint(s), SOMA body/rig assets, export tool and resulting output rights. Determine exactly what each license permits/requires rather than flattening them into “open source/commercial.” No legal certainty beyond cited terms; do not promise all user downstream uses are cleared.
- NVIDIA model licenses to retrieve and cite as applicable:
  - https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
  - https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-internal-scientific-research-and-development-model-license/
- Refresh current release/model cards/docs and actual source paths. Upstream capabilities must never be attributed to the C++ port. Dates and repo commit revisions belong in the report.

## Scope and useful questions

1. **Rights / access:** exact eligible SOMA model+body asset combination for monetized YouTube; notices/attribution/distribution conditions; gated download/account/terms requirements; whether generated motion may be retargeted to a separately licensed character without distributing the research body. Explicitly rule out SMPL-X/G1/checkpoint substitutions unless separately authorized and licensed.
2. **Local feasibility:** inspect this Mac hardware, installed relevant runtime versions and available disk/memory READ-ONLY, without secrets or blanket filesystem crawling. What upstream actually supports versus Apple Silicon CPU/MPS/Metal hypotheses. Identify unconditional CUDA kernels and device assumptions in source; memory/checkpoint sizes, dependencies and portable/unsupported parts. CUDA-only means a real constraint, not “should work.” No silently substituting the Vulkan C++ port.
3. **Motion -> Blender:** supported motion duration, text/trajectory/keyframe/contact constraints, actual export format, skeleton/joint hierarchy, axes/units/fps/root motion, foot contact/sliding and retargeting into a humanoid auto-rig. No hand-rig-from-scratch project. Hands/face/lip-sync/object interaction limits matter; don't promise them just because body locomotion works. Animation curves/retargeting code remain distinct from a visually accepted character.
4. **Production-fit test:** smallest test that answers useful questions: a short walk -> stop -> head/body turn, and optionally a short relaxed rhythmic groove for a sonidero. Judge foot planting, root drift, temporal consistency, controllability and whether it saves effort over ordinary licensed mocap/auto-rigging. Quantitative runtime/memory/quality claims require an actual run receipt; upstream/demo claims labelled separately.
5. **Recommendation:** GO for tiny local proof / conditional on access or a small compatibility change / NO local path without a separate project. State exact missing prerequisites and propose ONE next step, not a menu of20 products. Storyboard continues regardless; send practical motion constraints to its parent through Silas.

## Execution envelope

- Own isolated `youtube-channel` worktree from `origin/main`, outputs `research/kimodo-soma/` plus ignored job-owned scratch. Read studio `docs/video-lane-asset-doctrine.md` completely.
- Web docs/public metadata and small source inspection allowed. Use source-backed research, not memory. No credentials/auth-file access, signup, accepting terms/licenses, gated downloads, purchases/cloud GPU/paid generation, upload/publishing, or silent large model downloads. A new dependency/runtime/model install is a proposed next step, not assumed approved.
- May read existing installed runtime/version information and specifically identified model cache metadata without changing it. Don't scan or delete unrelated caches. No GPU during research; keep CPU probes light and bounded.
- A **single tiny proof**, max8seconds of motion, max120seconds wall-time and512MiB new output, no auto-retry, is allowed ONLY if supported execution code/dependencies AND explicitly permitted weights/body assets are ALREADY locally installed with documented authorization, AND Silas grants a fresh safe native/compute slot. Unknown provenance/access fails this gate. Real watchdog and output-cap control required; don't invent a timeout receipt. If dependencies are absent, deliver the exploration now rather than build a controller or wait indefinitely.
- Do not touch the live Blender MCP session: Selva pNE owns it and its dirty state. The current eye repair and any already-started PP3D smoke/render stage take precedence. No process kills, reload/discard, port takeover or concurrent native stage. Optional export/preview uses a new isolated listener-free job-owned worker ONLY after Silas confirms ownership and scheduling, preserving all user scenes/players. Native studio production remains direct Blender MCP primary; this is an isolated optional import test, not a replacement/Higgsfield bridge.
- If a complete demo movie is produced, verify full decode and open in QuickTime through Silas; report READY TO WATCH and label it a motion/retarget test, not finished Selva character art. If no executable proof ran, say **not run** plainly—no fabricated screenshot or latency.

## Deliverables / review

- Source digest(s), concise `research.md`, component/license/access matrix, local evidence/compatibility notes and a minimal reproducible proposed proof recipe with exact known versions/commands/limits. Redact private identifiers; no secret values in artifacts.
- One compact NEW Lavish page: recommendation up front; what is verified/not tested; optional genuine demo; approval choices only if access/install is needed. Substantial DOCS output needs Lavish review BEFORE any PR; no Perkins (`pr_review=0`). No sprawling report or review fleet. Foreground-poll and preserve user decisions verbatim.
- Durable handoff to `/Users/moses/code/_bmad-output/implementation-artifacts/kimodo-soma-exploration/` before any worktree removal. No PR necessary merely to prove research completion; any later docs PR targets main and is user-merged only.
- Coordinate with `youtube-channel-selva-full-song-storyboard` through Silas: useful motion limits/risks, never edit the storyboard's files or make its delivery wait.
- No-PR completion checklist: files preserved/verified; actual notification executed with saved `shown:true` receipt (not a prose claim); explicit result/URL/demo or blocker delivered to Silas for Gru. A minion printing a result to itself is not a delivered task.

## Skills policy / model

- Primary `bmad-deep-recon`, headless **run**, type **technical**, decision shape **explore**, lean effort. Context/decision/target supplied, so plan-and-proceed; source-backed digests and calibrated claims, no repeated intake questions. Public web evidence is required; if web tooling is unconfigured, report blocker rather than fabricate.
- `context7-docs` for library-specific syntax/runtime APIs if needed; official repository/source/model cards for exact Kimodo claims.
- `lavish` for compact comparison/table/input review surface before PR.
- No code-review fleet/Perkins or generalized installation/retargeting product. Any meaningful implementation beyond the tiny already-installed proof is a separately scoped follow-up, not folded silently into this exploration.
- Parent and any3D visual helper: `openai-codex/gpt-6-astra`, thinking `xhigh`; default single researcher. Native inline vision, no legacy model detour.

## Dispatch parameters

- job: `youtube-channel-kimodo-soma-exploration` (self-report EXACT ID)
- repo: `youtube-channel`
- repo_root: `/Users/moses/code/youtube-channel`
- slug: `kimodo-soma-exploration`
- base: `main` (fresh origin/main)
- worktree: new isolated standard worktree; create same-repo worktrees sequentially
- model: `openai-codex/gpt-6-astra`
- thinking: `xhigh`
- pr_review: 0
- blocking_dependency: none for research
- coordinate_with: `youtube-channel-selva-full-song-storyboard`, existing Selva and PP3D parents for any optional compute slot
- outputs: research/review artifacts; optional bounded proof only if all existing-prerequisite gates pass
