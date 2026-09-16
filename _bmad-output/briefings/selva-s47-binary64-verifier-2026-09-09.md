# Selva S47 — correct numerical contact verifier, preserve physical threshold

## Delegated decision

**APPROVE by Gru under the full-film production/routine planning grant** the separately versioned binary64 contact-verifier correction below, host regression proof and ONE new source-bound S47 verification pass. No new user A/E, job/parent/fleet. Same pNE/session/worktree/Astra-xhigh.

This explicitly extends the preceding DIAGNOSTIC-ONLY grant to correcting the verifier. It does NOT retry/replay the failed Stage02 construction/control suite, change plant geometry, relax contact tolerance, reopen moth/proof02, or declare S47 accepted from three diagnostic queries.

## Evidence read / grounded conclusion

Gru read COMPLETE `production/full-film-v01/receipts/diagnostic-s47-ground-v01-20260909T102810Z/RESULT.md`. Diagnostic resultSHA5ec71324cbdbf0315bb89b94ab178b270a178ffac0c55df82e04345a3f8cd816; reconciliationSHAf705a12f76a0a590aec42a8ca31359e26af25297007f36280420f07d05ff7590. One native89594/supervisor89593 exited0/absent/1.4018095001s,3queries/no rendering; no GPU-usage telemetry collected.

At frame5471.5, exact second endpoint[1.0000000149011612,7.999999970197678,0] has native BVH distance2.6973982585332124um, with nearestpoint[1.0000019073486328,8.000001907348633,0]—in-plane positional error. Independent binary64 constrained-triangle computation on ALL188evaluated triangles gives0m, valid interiortriangle187/vertices50,73,85/barycentrics and1.986e-15m reconstruction residual; native-cast geometry also0. World/local agree. Firstendpointnative0.9536743164um vs independent0. +10umZ control is independent10um/native10.3574102468um; BOTHreject at2um. Ground is an evaluated beveled box, not an infinite plane.

Classification supported for THESE observations: NATIVE_QUERY_NUMERICAL_FALSE_CONTACT_FAILURE. The original detached-leaf in-memory pose was not saved/recreated; new measurements are not retroactively inserted into old logs. Ground/vine independence from leaf03 and exact reconstruction of logged endpoint are documented. Old Stage02 failure remains failed.

## Implementation boundary

- Immutable scene `selva-electrica-mv/production/full-film-v01/blender/leaf-vine-s47-v01.blend`, SHA2e2ffc1ddb1c7a9f9e2b531734e110fca03a7adba3b1d3775d95ed74326f224f, globalframes5422..5521 (100frames). Preserve old scripts/request/evidence, diagnostic geometry arrays, all source/library/asset/shot/camera/action/material hashes and protected user state.
- NEW verifier v2 + NEW tests/receipts/source binding only, in pNE's task tree. Correct the ground-contact decision to use binary64 closest distance to actual evaluated triangle domains, including constrained edges/vertices and object-to-world conversion. Keep the physical threshold exactly **2e-6m**. No tolerance increase, rounding to zero, axis-only/infinite-plane shortcut, authored-base-only mesh, guessed flat-ground shortcut, changed units or geometry edits.
- Avoid quietly falling back to the same float32 math in an allegedly binary64 implementation. Explicitly handle non-finite/empty/degenerate data conservatively. Native BVH may remain diagnostic/acceleration only if conservative candidate coverage is proven; do not assume its approximate selected face is the true binary64 global minimum. Actual188triangle data is small—prefer a straightforward correctness-first computation over new optimization machinery.
- Do not globally replace moth/other-job collision checks or alter existing failure gates. Scope is S47 vine-ground/contact verifier accuracy; preserve meaningful detached-leaf/attachment and off-surface controls and their original physical intent.

## Proof then one fresh validation, not old-suite retry

1. HOST-ONLY regression/tests first using recorded exact evaluated geometry/query fixtures: both original endpoints pass2um, +10umZ fails; include inside/outside face, edge/vertex, just-below/above2um, coordinate transforms and invalid/degenerate cases. Show original float32-based predicate rejects the recorded secondendpoint while the corrected triangle-domain computation accepts it. Off-surface and outside-domain fixtures must fail; no 'plane distance0' vacuous pass.
2. Mutation legs: substituting infinite-plane distance must fail outside-domain tests; removing/loosening2um enforcement must fail off-surface/boundary tests; dropping the required detached/contact control must be detected. Run affected real functions, not always-PASS mocks. Record executed RED/restoredGREEN and new source/test hashes. One retained Astra/xhigh read-only numerical/contact reviewer may check this narrow delta; no new fleet/Perkins/bootstrap marathon. Consolidate routine host fixes before native execution.
3. ONE NEW isolated listener-free source-bound validation worker on the SAME immutable asset, not its failed generator/request/script or old-suite entry point. Read/evaluate source without saving/editing it or touching live Blender. Native evaluation: full100integerframes and quarter-frame positions5422..5521 (397samples) plus at most8 bounded meaningful control fixtures. Controls may mutate explicitly isolated transient TEST copies and restore/discard them; they must never change the frozen saved scene or user/live scene. Keep complete actual sample/control counts and require every planned check to complete—abort/missing control is failure, not exit0 PASS. No new candidate construction, geometry family or source version inferred.
4. Maximum180seconds native wall/64MiB new output,1validationinvocation/no retry, counted in existing film24h/80GiB envelope. Fresh actual owner/process/safe slot through Silas, existing supervisor; no stalePID authority/userwindow interference/PP3D interaction. Capture source/driver/inputs/scene/frame-space/command/start/end/output/quiescence and meaningful failure numerics. Preserve originals and new failure on any ERROR/timeout/cap/unsafe state or real geometric failure; no automatic patch/retry/waiver after native failure.
5. Result must distinguish numerical correction proof, complete new S47 evaluated-motion/contact coverage and final visual acceptance. Prior Stage02 controls/take still failed/incomplete historically. Do not overwrite their receipts or silently promote source-only manifest into footage.

## After successful checks

If this new focused validation genuinely completes GREEN with required controls/source invariants, release only the independently verified S47 source/clearance evidence into the EXISTING approved full-film production workflow. Next actual production-frame visual/cost checks and any S47 render remain under the original full-film stages/budgets/quality checks and Silas scheduling—not another mandatory user6–8sproof/go. Numerical GREEN is not visual screening, footage, a completed shot or final film acceptance. pNS receives only complete correctly typed hashed exports with relevant evidence; source-only records are not footage.

Moth151/proof02 STOP remains immutable; no moth work in this pass. PP3D observer exploration remains BLOCKED with no further work under its latest ruling—this Selva grant does not affect it. Other independent Selva assets may progress; no whole-film freeze/remote/publication/paid/SOMA/H3/push/PR/merge.

## Skills / dispatch

Continue existing applicable production workflow and proportionate internal verification. `context7-docs`/installed Blender API descriptions for actual evaluated geometry behavior; use native Astra vision for subsequent EXISTINGLY authorized render checks. No bootstrap repetition solely because of this amendment, no uninvited new review fleet.

repo: youtube-channel
repo_root: /Users/moses/code/youtube-channel
job_id: youtube-channel-selva-electrica-assets-rigs
worktree: /Users/moses/.herdr/worktrees/youtube-channel/selva-electrica-assets-rigs
mode: same pNE/session; separatelyversioned numerical verifier +1newS47validation
base: main (retained branch/dirty work)
model: openai-codex/gpt-6-astra
thinking: xhigh
pr_review: 0
new_job: false
new_validation_native_invocations: 1max
validation_watchdog_seconds: 180
validation_output_cap_mib: 64
geometry_or_tolerance_change: forbidden
follow_on_render: existing full-film grant only, after actual clearance+visual/cost+scheduling gates

Silas: relay complete decision, verify same-parent processing, account resources and route actual corrected-verifier/validation result or precise new failure. Do not relay each preparation/byte-count receipt; final user visual gate remains unchanged.
