# User-approved SELVA diagnostic — actual mesh versus conservative framing box

## Authority / project distinction

User, 2026-09-12, answered **"yes"** to Gru's explicit proposal: **ONE <=5-minute actual-mesh framing check across the full shot, keeping the same margin, before changing artwork or camera.** This is SELVA/Blender work, NOT PP3D. The successful build was Selva A; Selva B then failed. PP3D's separate import diagnostic grant is unaffected.

This authorizes ONE new framing-only native diagnostic, not A/B retry, CHECK06, camera/art change, validation waiver, or shot acceptance. Stop after reporting the diagnostic regardless of outcome. Preserve A passed/B failed and every prior STOP.

Same existing row `youtube-channel-selva-electrica-assets-rigs`, live pYR/session01a0954f-f26c-7150-a89a-182fdde98f85, retained dirty worktree `/Users/moses/.herdr/worktrees/youtube-channel/selva-electrica-assets-rigs`, Astra/xhigh. Deliver IN PLACE; no relaunch if alive, helper/fleet/new row/tree, reset/rebase/pull/cleanup/commit/PR.

## Exact evidence / source

Read `/Users/moses/code/_bmad-output/implementation-artifacts/selva-manifest-rebind-20260912/STOP.md`, STOP.json and FINAL-ACCOUNTING.json. Latest STOP SHA851402434f640b666f622d915ae197bf3036a19419239eed0cf4c60d7350e8b9.

D04=`<worktree>/selva-electrica-mv/production/full-film-v01/receipts/charge-look-pass04-20260910`.

Use unchanged `D04/A-art-build-rebind-v05/charge-look-pass04-cap01.blend` —51388040bytes/SHA256 **799a8fa546ce136f06920e9b1e7eb5fc8a6ac93e3ccda47fdf65c2076a85e84a** (freshly verified by Gru12:33Z). Its actual scene, verified by B's load path, is **SELVA_S47_ChargeLookPass04**. The retained request's old source_scene text saysPass03; do not trust that stale metadata over the actual consumed scene contract. Bind a NEW truthful diagnostic request without modifying old records.

B worker `D04/B-validation-rebind-v05/validate_pass04.py` lines169–186 computes snapshots, then projects all eight corners of each occupied world-axis-aligned bounding box; Roadbed is excluded from framing. At5511.5 minY0.014756826683878899 failed required0.015. Last complete sample5511.25:358/397quarters,90/100integer frames,3222/3573 fidelity comparisons,7controls. About0.262627 nominal pixels short of a16.2px safety margin at1080p, not demonstrated clipping. The remainder of B is unverified.

## Diagnostic question / unchanged criteria

Distinguish:
1. Conservative AABB corners violate1.5% margin while the actual evaluated mesh meets it.
2. Actual mesh itself violates the SAME margin at some sample.
3. Evidence incomplete/ambiguous; no conclusion.

Keep positive depth and normalized x/y bounds[0.015,0.985] EXACTLY. No epsilon-as-waiver, reduced margin, selected-frame subset, hidden/offscreen-point discard, camera move/zoom/lens/shift/animation change, render-border/resolution alteration, geometry/control/material change or source save. AABB-only breach is diagnostic evidence for a future validator decision, NOT permission to change B or mark it green.

## Bounded preparation

NEW <=30min/8MiB host authoring/check window for a minimal framing-only driver and truthful entry packet; record actual start/deadline and preserve accounting. Add at most1800s to prior6900 declared host ceiling (8700); carry actual6544.269076824188s and old193.636218/0.065973s overruns unchanged. Include host proof/receipt/central copies. Do not replay B's whole preparation, seven collision controls, expensive full geometry/fidelity campaign, BMad bootstrap or process-classifier proof.

Reuse safe projection/data/frame helpers and already-proven observation/supervision contracts where byte/semantic-identical. Allowed edits are NEW diagnostic driver/request/receipt and minimal versioned recognition of its explicit diagnostic mode/bounds/no-render completion markers. Do not weaken old A/B/C contracts or generalize an observer framework. Inert file/math/mocked-I/O checks allowed within the preparation window; ZERO actual Blender/probe/native rehearsals before the one entry.

## ONE native diagnostic entry — <=300s /128MiB outputs

- New namespace `framing-diagnostic01-20260912` and a clearly named framing-only stage; one isolated owned Blender worker launched through the established direct-MCP production route. Same installed binary, threads and strict owned supervision; no scene mutation in shared live Blender. No hidden warmup/version/control process or extra entry. Record start/deadline before launch; enforce absolute<=300s including bounded owned cleanup. Retain exact ownership handles, stdout/stderr/exit/EOF and final result/diagnostic limits.
- Open the unchanged saved source in isolation with scripts disabled, using the actual single scenePass04. Do NOT import the top-level B validation script (it executes controls/the full campaign). Do NOT run collision, containment or source–TEST mutation/fidelity checks; this entry measures framing only.
- Sample the EXACT397 quarter-frame times from5422 through5521 inclusive (same frame/subframe semantics as retained B), including5511.5 and all39 previously uncompleted quarter samples. Count and pin endpoints/uniqueness/order/completion. Same frozen camera animation is evaluated at each time; do not change it.
- Use the same evaluated source geometry snapshots/object domain as B: seven bound leaf meshes plus FF02_Arch_Vine; Roadbed remains excluded ONLY from framing, exactly as in B. Verify expected objects, finite evaluated world geometry, active modifiers and render/viewport parity; no selective visibility sample. No new TEST scene or geometry mutation. Preserve and hash-bind the saved source and relevant camera/action/settings before/after; evaluating frames in the isolated disposable process is allowed, writing the blend is not.
- At each sample, compute BOTH (a) identical per-object world-AABB corner projections and (b) actual evaluated mesh vertex projections, with the same camera/depth/screen convention. Preserve object/vertex indices and world/projected coordinates for extremal and offending witnesses; keep per-object extrema, depth flags, counts and all violating sample times. Do not substitute leaf origins, silhouettes guessed from a picture, or sampled vertices for complete mesh coverage.
- Vertex extrema establish the finite evaluated triangular mesh's projection only under verified positive-depth perspective assumptions; report nonpositive/ambiguous depth explicitly, never silently discard it. Do not claim rendered-pixel coverage, displacement/motion blur or continuous-between-samples safety from these finite evaluated vertices.
- Efficient vectorized projection is allowed to fit the bound, but must be cross-checked IN THIS same native entry against Blender's existing world_to_camera_view convention for representative/extremal actual points, with enough precision to resolve a0.000243 normalized shortfall. Account for sensor fit/aspect/lens/shift/camera transforms. Record discrepancies and precision; if a near-margin verdict is numerically ambiguous, label it inconclusive, not green. No second native projection calibration.
- Reproduce the old AABB result at5511.5 with a source/convention comparison and retained full float precision; if inconsistent, report the cause/uncertainty before drawing an AABB-vs-mesh conclusion. Do not tune constants to match it.
- Framing-margin violations are the expected diagnostic observation: retain/latch them and continue collecting the other frames within this ONE bounded pass, rather than first-failure-aborting as B did. This does not waive any violation or make B pass. Unexpected source/identity/finite-data/projection/worker/renderer/log/deadline/byte failure stops with bounded exact-owned cleanup, partial counts and honest inconclusive result; no retry.

Output per-frame/per-object summaries and compact extremal witnesses, not huge redundant copies of every vertex at every time. Preserve enough data to inspect every violation. Complete raw log/receipt and all count/completion flags required. Do not loosen framing or other contracts to achieve an exit0.

## Counters / live gates / exclusions

This is a NEW diagnostic native entry (<=300s), NOT another A or B and not a render slot. Charge actual seconds/artifacts to existing pass/global budgets; last global988.7974491952921s, pass native242.23082170899988s conservatively including preservation, slots5/stills4/shots0. Original pass4200s/2GiB, global24h/80GiB/free32GiB/paid0 stay. CHECK06slot6 remains unused/CLOSED; A and B remain consumed. Reconcile latest actual totals before entry.

Fresh ordinary owned/source/live/process/budget gates are required and authorized; do not repeat the completed classifier-proof campaign or use old7199/PID proof as current cleanliness. Standing Blender access permits routine preserved-live checks, not overwriting/restarting user work. Stable archived manifest binding remains unchanged with exact378b6c76…hash and consumed references intact; no new old-worktree dependency. Silas coordinates actual native start boundaries with other eligible workers, no user-game interference or blanket GPU hold. No Higgsfield, asset intake/research, GUI driving, source/camera/tolerance fix, render/CHECK06, B retry or paid work.

## Result / stopping rule

After the single diagnostic, STOP regardless of result. Write `/Users/moses/code/_bmad-output/implementation-artifacts/selva-fixed-camera-framing-diagnostic-2026-09-12.md` with concise evidence-graded conclusions:
- 397 coverage/accounting and source/camera identity.
- Known5511.5 AABB versus actual-mesh extrema and responsible objects/witnesses.
- Full-shot worst AABB AND mesh margins, all violating times, any incomplete/ambiguous regions.
- Confirmed conservative-only margin miss versus actual-mesh margin miss versus inconclusive; no unproved pixel-clipping/visual acceptance claim.
- Smallest future decision, PROPOSAL ONLY. No automatic validator amendment, geometry/camera change, new B or CHECK06 release.

Preserve raw evidence/driver/receipt centrally under the same job. Row WORKING during this bounded diagnostic, BLOCKED at result. Report to Silas; notification checklist with actual shown:true (one retry iffalse), owner marker/completion/death wake if async, <=3 useful own-field-note lessons. Routine hashes stay backstage; report the meaningful result.

## Skills / model / dispatch parameters

Retained valid `bmad-build` focused diagnostic implementation/check context; `gds-investigate` evidence-grading principles for result, no new interactive/bootstrap/helper campaign. Parent `openai-codex/gpt-6-astra` / `xhigh`, actual session verified. No native aesthetic verdict or new Lavish gate from a no-image diagnostic.

- job_id: youtube-channel-selva-electrica-assets-rigs — same existing row
- repo: youtube-channel
- repo_root: /Users/moses/code/youtube-channel
- github_repo: mssoka/youtube-channel
- base: main
- slug: selva-electrica-assets-rigs
- worktree: /Users/moses/.herdr/worktrees/youtube-channel/selva-electrica-assets-rigs — retain dirty
- pane: existing w85:pYR, verify live and deliver IN PLACE
- model: openai-codex/gpt-6-astra
- thinking: xhigh
- pr_review: 0 — local diagnostic, no commit/PR

Silas records exact new grant separately, verifies full briefing accepted and actual preparation; no relaunch/duplicate and no PP3D authority implied.
