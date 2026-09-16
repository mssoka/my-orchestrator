# PP3D shutdown diagnostics — nonvisual GLM5.3 investigation

## User request and scope

User, verbatim:

> ok. let's explore that. use glm5.3 for that, we don't need to have vision, or create a 3D asset to explore that right?

Context: Gru just explained the retained full-suite allocator/dependency/ObjectDB/resource exit diagnostics and the editor's residual StringName warning, distinguishing them from the current feature supervisor's process-identity failure.

**Yes: this is a nonvisual source/log/lifecycle investigation.** User explicitly authorizes reopening READ-ONLY investigation of those shutdown diagnostics and chooses **`zai-coding-cn/glm-5.3`** for this lane. This is a lane-specific model exception, not a global model-policy change or a reason to switch the active feature/art owners. No image/asset creation or visual review is necessary.

The paired editor BEFORE/AFTER runs remain PARKED0/2; no native run, editor probe, containment investigation, cleanup-contract narrowing or waiver follows from “explore.” Findings may recommend a small future reproduction or fix; neither is executed here.

## Ownership / isolation / model

- New read-only job: `packet-plumber-3d-shutdown-investigation-glm`.
- Repository: `/Users/moses/code/packet-plumber-3d`, base main.
- One separate investigator pane in a DETACHED analysis worktree at `d2ffebbe05c603419516b85fe13e5f45295eca1f` (historical checkout for navigation ONLY, not a claim that it contains the dirty current feature changes). Use exact preserved per-run source snapshots for causal claims.
- Active pMY remains the SOLE feature/test-runtime writer in `/Users/moses/.herdr/worktrees/packet-plumber-3d/planet-life-router-legibility`. Read its sealed snapshots/logs; never modify that tree or its session, signal/control its process, touch pP4 or contact/reassign pN2/reviewers. The new investigator's output belongs only to its own case/report namespace.
- Pin exact model `zai-coding-cn/glm-5.3`, thinking `max`; verify actual model/thinking events. This lane contains no images and needs no vision fallback. No Astra/KYLE/helper substitution.
- Silas must probe this exact model through the existing env-cleared pi route before dispatch. A chatty successful answer is not a DOWN verdict; inspect actual error/result/provenance. If genuinely unavailable, report it and HOLD this lane rather than silently changing models, installing providers or modifying global routing. No secrets in probes/reports. Do not let a legacy-model probe overwrite global GPT routing policy.
- At most ONE same-model, explicitly pinned, read-only helper if the investigation skill's large-file/evidence-scan delegation rule requires it; return structured JSON citations. No general fleet or native/vision helper. Preserve output to disk; investigator owns the synthesis.

## Known facts and exact evidence roots

Sole-writer worktree `W=/Users/moses/.herdr/worktrees/packet-plumber-3d/planet-life-router-legibility`.

Evidence base `E=$W/.scratch/planet-life/companions-dolphins-20260908-115343`.

1. `$W/_bmad-output/implementation-artifacts/planet-life-shutdown-cleanup-retest.md` — read complete. Records the real orphaned HUD-label fix and narrow successful family/dolphin checks, plus the remaining editor StringName warning. Do NOT re-diagnose the already repaired label as though it remains unfixed.
2. Full-suite retained actual streams/source: `$E/feature-completion-resume-20260909/headless-current-02/full/output/native.stderr.log`, sibling stdout, `full/project/`, `full/execution.json`, `full/audit.json`, parent input/cache/summary manifests. This run had621 semantic checks; it predates subsequent feature-review corrections. It is NOT a final638-check/current-source verification claim.
3. Editor retained actual streams: `$E/native-smoke-cleanup-retest-20260909/stages/editor/output/native.stdout.log` and `native.stderr.log`; exact source/project, editor population receipt and execution/inspection records in that run. The report cites editor execution SHA `0df344702c6994801a93932a5816c5e98b3353c98c7f9d575fc2374acd7edbc4`.
4. `$E/cleanup-source-green-01/source.json` and `project/`, relevant frozen pre-HUD-fix/repaired source manifests and `$E/shutdown-cleanup-repair-20260909T011748Z/`. Use existing stored engine-source/API research if present before fetching anything anew. A77/78 manifest count is not evidence that the unexecuted paired comparisons produced results.
5. `/Users/moses/code/_bmad-output/implementation-artifacts/pp3d-editor-comparisons-user-park-2026-09-09.md` remains controlling for native comparisons/whole-owned-tree cleanup.
6. Current feature status only for separation: `$E/feature-completion-resume-20260909/feature-native-stop-disposition.md` and observation HANDOFF. Do not analyze or change the active process-identity adapter; pMY owns that separate new instrumented attempt.

Retained full-suite stderr includes:

- `ERROR: Pages in use exist at exit in PagedAllocator: N20RasterizerSceneDummy21GeometryInstanceDummyE`
- `WARNING: Leaked instance dependency: Bug - did not call instance_notify_deleted when freeing.`
- `WARNING: 73 ObjectDB instances were leaked at exit (run with --verbose for details).`
- `ERROR: 1 resources still in use at exit (run with --verbose for details).`

Retained editor stdout includes:

- `Orphan StringName: Node (static: 6, total: 7)`
- `StringName: 1 unclaimed string names at exit.`

Editor stderr also contained repeated `Image format RGB8 not supported by hardware, converting to RGBA8.` Keep that format fallback distinct from ownership/leak findings.

Exact installed engine in the reports: Godot4.7.2.stable.official.ed1daf0bf. Previously cited StringName source revision: `ed1daf0bf001b61586d9930840f2f1394092c079`. Source/version correspondence must be verified from receipts. If the exact revision cannot be obtained, disclose the gap rather than substituting HEAD/latest and claiming an exact match.

## Questions to answer — falsify the premise

1. For EACH diagnostic family, what exactly triggers the engine message? Which facts does it establish, and which stronger claims does it NOT establish? In particular, an orphan StringName called Node is not itself proof of one leaked scene Node, and an exit leak count does not by itself demonstrate growing gameplay memory use.
2. Trace allocations, adoption/ownership, signal/callable/static references, resource/mesh dependencies, test fixture teardown, deferred queue_free and SceneTree.quit ordering in the SOURCE THAT PRODUCED each log. Are there specific reachable cleanup omissions, or only plausible hypotheses? Show counterevidence and version differences.
3. Separate project lifecycle defects, test-runner/fixture teardown defects and possible engine/editor/headless-dummy behavior. Do NOT presume engine-only harmlessness, and do not presume every engine-named message is caused by game code. Correlation with a render mode is not causal proof.
4. What does the verified HUD fix already explain? Which diagnostics disappeared in the scoped family/dolphin/editor probes, and which residuals remain? Do not aggregate unrelated runs into a single purported current result.
5. Is the residual editor StringName issue causally connected to the broad full-suite ObjectDB/resource/allocator messages? Keep separate causal tracks unless evidence actually joins them.
6. What is the smallest next action with the highest information value? If existing evidence supports a specific source fix, name it precisely without implementing. If new evidence is necessary, specify one bounded reproduction/control, expected discriminating observations and cleanup requirements for Gru to disposition later. Do not rebuild the old observer/containment/terminal-control project.

## Working method / limits

Use `gds-investigate` and its Confirmed/Deduced/Hypothesized grading, stronghold-first approach, preserved hypotheses, source trace and refutation pass. This briefing pre-approves the bounded READ-ONLY scope of outcomes1–5; intermediate checkpoints go to the case file/Gru through Silas rather than requiring five new user approvals. A substantive scope/evidence obstacle still stops for disposition. No assumptions fabricated to satisfy an outcome.

Follow supported skill activation/customization. A task-local `_bmad` link to the existing canonical installation may be set up in the NEW analysis worktree if needed; shared configs/skills/renderer remain untouched. Use the skill's explicit unresolved-output-path fallback if applicable. On actual bootstrap failure, preserve the exact error and route it; no raw-workflow bypass, installed-skill/config repair or repeated bootstrap campaign.

Allow read-only source/log/git inspection and pure host-side text/data analysis. Existing diagnostic artifacts are read-only external inputs; hashes and version-specific paths are required. Do not execute copied application/test scripts, import engine/runtime modules with side effects, launch Godot/editor/renderers/native probes, query/control other workers or mutate source, tests, monitors, caches, dependency/engine settings or user applications.

Narrow official Godot source/docs/issue research is permitted where needed to interpret exact messages; cite URLs and matching version. Read-only internet research is not permission to download assets, binaries, dependencies or execute third-party code. Use `context7-docs` for relevant library API details; version-specific source is stronger evidence for implementation behavior. No images or 3D assets.

Timebox the initial investigation to60min of active analysis; write findings early. Stop with an honest evidence gap rather than extending into an infrastructure project. Missing evidence is an acceptable, precise result; a failed hypothesis with a better causal account is a useful deliverable.

## Deliverables / close-out

A concise case file plus a compact summary table covering each diagnostic: observed run/source, producing condition, ownership path, evidence grade, unresolved gap and recommended next action. Include path:line/commit/log citations, clearly identify externally referenced evidence roots, retain rejected hypotheses, and give a plain-English answer: what is actually broken, what is only suspected, and whether any current gameplay consequence is demonstrated.

No PR, implementation, automatic fix, native reproduction, visual review or batch follows this report. Do not label shutdown clean, feature accepted or play-ready. Preserve completed deliverables into `/Users/moses/code/_bmad-output/implementation-artifacts/pp3d-shutdown-investigation-glm-2026-09-09/` before any analysis-worktree cleanup.

Silas: record lane-specific user model override and native0 scope on the new row; coordinate_with the feature parent, not blocked_by it. Confirm investigator delivery/read/provenance and actual progress. On completion verify the report exists, relay the concrete conclusion/path to Gru immediately, and verify the no-PR notification result shown:true (do not rely on pane/PR watchers). Do not sweep pMY, the retained feature tree or user terminals. Report ends at diagnosis; Gru routes any future fix/reproduction.

## Dispatch parameters

- repo: packet-plumber-3d
- repo_root: /Users/moses/code/packet-plumber-3d
- job_id: packet-plumber-3d-shutdown-investigation-glm
- base: main; DETACHED historical navigation worktree at d2ffebbe05c603419516b85fe13e5f45295eca1f
- mode: read-only diagnosis, no PR/native/assets/vision
- model: zai-coding-cn/glm-5.3 (explicit user exception, probe-gated, no silent fallback)
- thinking: max
- pr_review: 0
- skills: gds-investigate; context7-docs as needed
- full-film and active feature owners: unchanged
