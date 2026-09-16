# Colour and native API contract

## Artwork versus baked picture

- `#RRGGBB` references are sRGB design values. `recipe.linear_hex` converts them **once** to scene-linear RGB for native materials/lights, assuming the default Rec709/sRGB-primary Blender workspace. It is not a general gamut converter.
- The supplied recipe uses AgX/Medium High Contrast, exposure0, gamma1. Supplied scenes retain their existing view/camera/material look; only declared size/frame/quality settings change. Approve the look in actual pixels.
- Exported loop pixels are already display-referred sRGB. The VSE therefore uses **Standard / None / exposure0 / gamma1**, sequencer sRGB. Another AgX pass would grade the picture twice.
- Delivery is SDR H264 with Rec709 primaries/matrix, **sRGB transfer (`iec61966-2-1`)**, limited-range YUV. This is not “all BT709,” HDR mastering, spectral dispersion, or universal calibrated-display certification.

## Guarded native metadata correction

The tested native encoder can label those sRGB pixels with BT709 transfer1. `srgb_metadata.py` changes recognized generated SPS/`colr` transfer signalling to13 **inside the Blender export process**, without changing picture/audio packet payloads or file layout. Already-correct13 is idempotent. Unsupported signalling, missing colour atoms, in-band SPS, foreign output paths or structural size changes are refused.

This is a metadata repair, **not colour conversion**. Never apply it to an arbitrary third-party Rec709/gamma2.4 movie to make it “sRGB.” Approved-loop intake requires the already-measured target metadata. A different target needs a real validated transform and actual browser/native comparison. A Rec.1886 trial in the production work was rejected because actual browser appearance differed despite a normalized numerical comparison.

The current repair buffers the file and refuses exports larger than2GiB. Validate a bounded streaming implementation before expanding that limit; do not simply remove it. Ordinary UI rendering bypasses this helper, so use the CLI for accepted exports. Native projects include that warning.

## Blender5.2-specific lessons encoded in code

- Set `image_settings.media_type='VIDEO'` **before** `file_format='FFMPEG'`.
- VSE creation uses `sequence_editor.strips.new_movie/new_sound`. Real contiguous strips, not shell concatenation.
- `workspace.sequencer_scene` matters independently of the active window scene. The saved edit includes a bound native workspace. Fit the timeline manually in a live GUI if necessary; do not call context-sensitive view operators headlessly.
- Cache original audio using `Sound.use_memory_cache=True`; keep it external and unpacked. An uncached MP3 source-read skip in production was only exposed by sample-zero/full-song QA, not an eight-second seek test. Never compensate by shifting/trimming the edit.
- Frame budget is integer ceil(decoded samples × fps / sample rate). Picture repeats cover that range; original sound appears once, unity volume, no offsets/retiming. Report frame-grid tail and any native AAC packet padding separately. Decoder alignment/end tests remain mandatory.
- Compact driver expressions/property targets, correct mesh winding, fresh output guards and isolated background workers prevent previously observed failures. Factory-startup flags affect only the disposable worker, not global preferences or the live user document.

## Dependencies and limits

Native worker is version-bound to Blender5.2. Host Python3.10+ needs NumPy, SciPy and Pillow; FFmpeg/FFprobe decode/probe only. No automatic installs, add-ons, weights, external encoders or publishing.

Current input contract: stereo44.1/48kHz audio; integer fps1–120; opaque square-pixel16:9 pictures, at most4K video;8–3600 loop frames; audio budget at most30minutes; still widths up to7680. These are resource/config bounds, not claims that every permitted combination was tested. Custom OCIO, fractional-fps/VFR, HDR/P3, alpha compositing, multichannel/mono source handling, missing/UDIM dependencies, narrative montages and beat-synchronized retiming need separately validated work.

API references: [sound mixdown](https://docs.blender.org/api/current/bpy.ops.sound.html), [external dependency paths](https://docs.blender.org/api/current/bpy.utils.html), [Blender colour management](https://docs.blender.org/manual/en/latest/render/color_management.html). Installed RNA and real native tests remain authoritative for the pinned runtime.
