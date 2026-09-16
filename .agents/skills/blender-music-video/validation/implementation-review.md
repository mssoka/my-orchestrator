# Same-owner implementation review

Scope: isolated native-workflow extraction; existing production media/source remained frozen. BMad routing/trace was used proportionately. Under the explicit same-owner/no-extra-fleet/pr_review=0 amendment, review was inline with focused tests—not an independent blind review or a new agent/PR gate.

## Patched boundaries

1. Reject nested config typos, boolean frame rates and string-valued `test_only`; retain actual authority strings.
2. Keep original music outside the output/package and preserve hashes across work.
3. Refuse ambiguous supplied-scene colour overrides, non-square/transparent output, artwork VSE/speaker audio and missing/special dependencies.
4. Bind native source hashes before/after workers as well as source-bound completed receipts; incomplete files never count as completion.
5. Bound metadata correction to the recognized native sRGB contract, one colour atom/track, limited range, unchanged layout/payloads and a2GiB memory ceiling.
6. Derive frame budget from decoded samples and distinguish native AAC packet padding from frame-grid rounding.
7. Cache original sound and include sample-zero/measurable audio plus full-program ending checks; never offset an edit to conceal decoder delay.
8. Normalize audio alignment energy and choose a signal-bearing channel; handle anti-phase stereo and silent channels explicitly.
9. Correct primitive box winding; inspect actual bevels, material separation, framing and periodic poses.
10. Give native source a relative manual-export location and explicit warning that ordinary UI exports bypass metadata correction.
11. Preserve relative picture links through the ZIP, exclude original music and supply a fresh-output reproduction config.
12. Verify relocated delivery manifests; reject range errors, escaping symlinks and upload methods.
13. Append honest source-bound owner review separately from the immutable delivery payload; synthetic tests stay labelled.
14. Retain host failure traces and native logs, refuse live-lock stealing, and emit compact CLI receipt pointers rather than flooding output.

No pre-existing code changes deferred. The pre-existing live comparison-server log was intentionally excluded from this source commit.

## Retained RED evidence

- Optional native `sound.mixdown` fixture experiments returned without a usable complete MP3; those files/logs were rejected, not promoted. The fixture now uses Blender's native Audaspace writer and the resulting MP3 passes the generic cached VSE path. This does not establish a universal diagnosis of `mixdown`.
- Cold browser playback recorded two drops. After exercising actual controls/loading, the same1280px viewport completed a warm uninterrupted replay with zero drops/seeks/errors. Both results are retained; no universal-player smoothness claim.
- Six public-CLI negatives include a real failed native worker, missing input, wrong fps, occupied output, changed resume and an interrupted-looking file without a completion receipt.

## Evidence

32 contract/metadata/HTTP tests;33 public-CLI smoke events; recipe and provided-scene native renders; approved-loop skip; stereo44.1/48kHz and synthetic MP3; full native VSE/audio export; fractional repeats; native thumbnails; relocated ZIP reopen; actual browser phase/seam/ending images, colour pair, native controls, five download links, range request and390px layout. See `results.json` and centrally preserved detailed logs.

The prior full-length native delivery supplies the long-program leg without another production render. No listening, beat-grid, HDR, calibrated-display or automatic original-art claim was made. Stable installation/default discovery is an installer-owned handoff check, separate from this source validation.
