# Selva S47 — one bounded read-only ground-contact diagnostic

## Decision

**APPROVE by Gru under the existing full-film production/routine planning authority** ONE new source-bound read-only geometry/query diagnostic. This is not a retry of the failed stage, no geometry revision, no old-script/receipt patch and no render/shot admission. Same pNE/session/worktree/Astra-xhigh; no new parent/fleet/userA-E.

Gru read COMPLETE stage-02 `failure-reconciliation.json`, reported SHAb86b58145b51dd3016f55bb6d5b1aef012d4b76937ae0c1f2654762d506b8ec6. The failed attempt remains terminal. Original leaf/vine/S47 source saved/reopened, then first detached-leaf negative control stopped at SECOND vine-ground assertion. Nearest-point result/distance were not logged: actual gap vs query precision remains UNRESOLVED, neither geometry failure nor clearance PASS established.

## Immutable inputs / question

- Worktree `/Users/moses/.herdr/worktrees/youtube-channel/selva-electrica-assets-rigs`.
- Source `selva-electrica-mv/production/full-film-v01/blender/leaf-vine-s47-v01.blend`, SHA2562e2ffc1ddb1c7a9f9e2b531734e110fca03a7adba3b1d3775d95ed74326f224f.
- Failed evidence directory `selva-electrica-mv/production/full-film-v01/receipts/stage-02-leaf-vine-20260909T095548Z/`, native84662/supervisor84661 already exited1/absent;1.529389875s. Do not rerun their request/script/control suite or reset failure.
- Recorded query `[1.0000000149011612,7.999999970197678,0.0]`; existing threshold **2e-6m**.
- Question: what geometry/transform/triangle does the exact nearest query use, what result/distance does it actually return, and does an independent double-precision point-to-evaluated-triangle computation agree? Do not lead with a 'harmless precision' assumption.

## Bounded execution

1. CPU/host preparation first: inspect failed request/script/trace/source to identify exact scene/frame, ground/vine objects, evaluated-versus-base geometry, spaces/transforms/units, BVH construction/query parameters and whether the first detached-leaf control changed any relevant ground/query input. Record source/script/input hashes, including immutable linked libraries. Do not edit the old script or recreate its geometry mutations as a 'read-only' rerun.
2. New versioned diagnostic script/receipts only, same owner; ONE isolated listener-free background Blender invocation on the frozen saved source, no user's live scene reuse/open/reload/save. A read-only source copy is permitted only if byte-identical/hash verified; no save of .blend, object/property/geometry mutation, rig replay, construction, old negative-control execution, GPU render or export. Frame/evaluated-depsgraph reads may reproduce the logged relevant frame, with transient evaluation documented; don't call that a source edit. If failed in-memory state was not saved, explicitly label what can/cannot be reconstructed from the saved source.
3. Log raw full-precision query point/result tuple, nearest point/distance/normal/triangle index (or None), exact coordinate spaces, transforms, ground triangle vertices and float precision. Include the FIRST and SECOND original ground-contact endpoints, plus at most6 bounded reference/roundoff queries if genuinely necessary. No full100-frame take, sweep/grid, adaptive candidate family or geometry optimization. Maximum8queries, no broad diagnostic expansion.
4. Independently calculate nearest point/distance to the actual relevant evaluated ground triangles in double precision using a separate computation, including triangle-domain/barycentric containment (an infinite-plane distance alone is NOT ground contact). Check world/local conversion, scale and flat-ground assumption against actual mesh. Report absolute/relative error versus the native query and the unchanged2um threshold. Preserve divergent/None results; no rounding to zero or fabricated precision. Independent means not another call to the same BVH routine dressed up as confirmation.
5. Bound this NEW diagnostic to **90seconds owned native wall time,64MiB combined output/log/data**,1invocation, no native retry. Silas obtains fresh actual ownership/process availability before launch, no stalePIDs, no interruption of userBlender/audio/services/PP3D. Use existing supervision; native PID/UTC/source/command/exit/output/quiescence receipt required. Label CPU geometry evaluation accurately; do not infer zeroGPU activity from configured renderer name alone. Account usage/outputs against existing24h/80GiB full-film aggregate; no counter reset.
6. On completion, return compact result: real geometric gap vs query/transform/precision defect vs unresolved, measured numbers, exact evidence paths/hashes and the smallest suggested correction. A suggested verifier correction, if justified, must preserve the intended geometric threshold and meaningful negative controls; it is NOT authorized to execute under this diagnostic-only grant. Genuine geometry changes or visual compromises also route to Gru first. On missing data/crash/timeout/cap/unsafe drift, preserve failure and stop—no retry/waiver.

## Preservation / downstream

Keep all failed source/scripts/request/markers/raw receipts and protected159/inputs344/frozen325/audio/moth151/proof02 unchanged. Current stage has0completedcontrols/takesamples/renders/exports/shots. Diagnostic success is NOT S47 motion clearance or render readiness and must not become a shot export; pNS receives no footage release. Moth/proof02 STOP unchanged. Independent leaf/prop/humanoid film work may continue separately under existing ownership/budget; no whole-film or PP3D pause from this investigation.

Silas: relay complete decision to existing pNE, verify processing, schedule only the bounded read-only diagnostic, and return MEASUREDRESULT/precisefailure (not repeated staging updates). Final visual acceptance stays user-owned; no publication/paid/PR/push/merge/SOMA/H3.

## Skills / model / dispatch

Continue existing already-active production workflow and targeted technical checks; `context7-docs`/installed Blender API descriptors for actual BVH/depsgraph behavior. No skill/bootstrap replay merely for this amendment, no new review fleet. Native Astra vision only if existing evidence needs reading; no new render here.

repo: youtube-channel
repo_root: /Users/moses/code/youtube-channel
job_id: youtube-channel-selva-electrica-assets-rigs
worktree: /Users/moses/.herdr/worktrees/youtube-channel/selva-electrica-assets-rigs
mode: same pNE/session; one new read-only contact diagnostic
base: main (retained branch/dirty work)
model: openai-codex/gpt-6-astra
thinking: xhigh
pr_review: 0
new_job: false
native_readonly_invocations: 1max
native_watchdog_seconds: 90
new_output_cap_mib: 64
render_or_geometry_repair_authorized: false
