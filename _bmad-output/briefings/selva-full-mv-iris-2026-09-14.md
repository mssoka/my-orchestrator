# Selva Eléctrica — finish the full music video in Blender

> **Later user extraction request:** “can the minion make this into a skill , with scripts so we dont have to burn tokens to repeat this for future videos”; clarified “i mean the full music video.” SAME owner must deliver this MV first, then package the end-to-end native workflow as a reusable script-backed skill under `/Users/moses/code/_bmad-output/briefings/blender-music-video-skill-extraction-2026-09-14.md`. Do not stop/rebuild this finished export or hold its delivery for tooling. Skill availability is an additional owed deliverable, not a vague future task.

## User GO and ownership

User, after discussing Blender as the full video editor: **“the loop is done. now lets create the full MV with music.”**

This explicitly authorizes FULL-SONG ASSEMBLY from the completed selected loop. It supersedes prior “no full-song assembly” fences for THIS new finishing stage only. No extra approval/selection gate is owed before work. Native-only preference remains: user previously said “ack. thanks. native it is” and clarified using Blender “as full video editor.”

Continue SAME canonical row `youtube-channel-selva-electric-loom`, SAME owner/session/worktree (`w9Z:p1`, `/Users/moses/.herdr/worktrees/youtube-channel/selva-electric-loom`; Silas verifies). Astra/xhigh; pr_review=0. No new fleet, no Perkins, no default model boot. Read this entire amendment and take ownership through a usable finished MV, not merely a timeline or queued export. Ordinary documentation lookup, VSE setup, diagnostic exports and in-scope fixes are already authorized.

The antecedent is resolved from actual user feedback and delivered files: **Nocturnal Iris, A+B: Tropical Club Orbit + Prism Ribbons**, NOT original Electric Loom or a montage of the six. User kept all six for possible future use, selected Iris and then A+B lighting. The existing derivative finished before this GO. No fresh design election required.

## Exact immutable inputs

All paths below are relative to the existing worktree unless absolute.

- Picture: `selva-electrica-mv/kinetic-comparison-v01/iris-lighting-ab-v01/review/iris-lighting-ab-v01.mp4` — 1920×1080,30fps,576 frames,19.2s; SHA256 `987b9ae141c5d16d03645a20ef83614835180f1754dcdf511e5c415fa071d46b`. Use the SINGLE cycle, not the57.6s seam-review encode. Reverify before ingest.
- Native artwork: same derivative's `source/iris-lighting-ab-v01.blend`, SHA256 `88380c352d177a09c0eefcd59e100bd967f4be10480f5da664f082cd3c2c7dbf`.
- Original music, read-only: `/Users/moses/code/_local-refs/selva-electrica-audio-2026-09-08/Selva Eléctrica.mp3`. Recorded SHA256 `f3a4113c5d7237117aec15b70afc91ae0633a73862967701dec365861c616110`, duration277.320979s, stereo48kHz. Probe actual file/decoded timeline; don't blindly use a historical rounded duration.
- Standing colour/theme guide: `selva-electrica-mv/kinetic-comparison-v01/lighting-directions/colour-design.md` (read fully). Keep its technical/thematic guidance, superseding ONLY its old no-full-song authorization statements.
- Delivered media/source receipt: derivative `review/delivery-manifest.json`; delivered direct player http://127.0.0.1:8794/iris-lighting-ab-v01/review/index.html . All six originals and this completed lighting derivative remain frozen. Do not reopen ended Lavish sessions or alter the old media server in a way that breaks existing links.

## Build the actual edit

Create a NEW owned namespace `selva-electrica-mv/full-mv-iris-v01/` and an editable native **Blender Video Sequence Editor .blend** with real movie and sound strips. Direct Blender MCP remains the primary live integration; native background Blender export is fine. Inspect/preserve unexplained live dirty state before any scene change. Do not overwrite or clear the existing artwork/user document.

1. Reuse the finished19.2s picture cycle across the full original song. **Do not re-render the3D mechanism for the song's entire duration.** The final VSE composition still needs encoding; that is normal. No full-song PNG/AVI archive or unnecessary proxy duplicates.
2. Place the original song ONCE, starting at the start of the edit, original speed/pitch and unchanged editorial content. No looping/remixing/normalizing/time-stretching/fading/replacing the song or inserting SFX. Original source bytes stay unchanged; codec transcoding for delivery is not claimed to be bit-identical audio.
3. Use the existing30fps/1080p picture without retiming. Repeat cleanly: exactly576 picture frames per full cycle, no duplicated endpoint, frozen frames, black gaps, overlaps or dissolves concealing the seam. Trim only the last picture repeat to fit the entire song. Derive total frame budget from actual audio coverage, allowing the minimal (<one frame where feasible) video-tail rounding instead of truncating the song.
4. Keep it artwork-first: no switch to other concepts, invented story, artist credit, lyrics, logo, watermark or long intro/outro. No fresh lighting/camera treatment. Any minimal title must use the known song name only; a clean title-free movie is appropriate.
5. This is thematic moving art, NOT proven beat synchronization. Do not infer a precise100BPM grid, remap the song, change the accepted picture speed or advertise synchronization based on the old approximate tempo estimate.
6. Produce the final MP4 through native Blender VSE export with high-quality H.264 video and AAC stereo audio at a sensible supported setting. Consult current Blender5.2 documentation/runtime API (context7-docs) before implementation. The installed Blender API is authoritative. A .blend facade plus an undisclosed standalone concat/mux substitution does not satisfy the native-editor request. ffprobe/FFmpeg are fine for independent probing/decoding/QA; Blender's own bundled encoder is naturally fine. If a genuinely unresolved native-export blocker remains, report it rather than silently switching to Resolve or external assembly.

## Critical finishing trap: do not grade the finished loop twice

The delivered loop is already AgX-rendered, display-referred SDR, with Rec.709 primaries/matrix, limited range and **sRGB transfer metadata**. Read its colour guide. Do not blindly inherit the3D scene's AgX/exposure on this finished movie and apply another tone map. Inspect the VSE input, working and output colour settings on the actual runtime. Preserve the accepted appearance; if converting to a conventional Rec.709 delivery transfer, perform a real transform rather than merely retagging.

Use a short representative native VSE export FIRST to validate picture roundtrip and music presence. Compare matched source/output phases under the same viewing transform for unexpected luminance/saturation shifts, wrong range or clipping. Record coherent export colour metadata. No new creative grading pass, HDR promise or calibrated-display claim.

## Matching thumbnail (previously discussed companion output)

Create one matching16:9 thumbnail using the actual finished Iris art and native Blender framing/compositing, not AI generation or another concept. Choose a strong readable cyan/rose/amber phase; preserve the original source and version any thumbnail setup. Deliver a high-resolution still plus a practical JPEG thumbnail. A clean artwork version is sufficient; optional minimal “Selva Eléctrica” text must be readable at small size and must not obscure the hero. Do not invent channel/artist branding or start a separate design campaign. The full MV is the primary deliverable.

## Verify and deliver

- Reopen the native edit and verify its real media links; document external dependencies. Never copy the original MP3 into tracked repo files: it remains in `_local-refs`, referenced read-only. Final MV containing that user-supplied song IS explicitly authorized. If a portable private bundle is necessary, keep it outside Git and document paths; no external publication.
- Full-file decode and stream probes: actual duration/frame count/dimensions/fps, video AND audible-content audio streams, coherent colour tags, no missing strips or render errors. Check decoded output audio coverage/alignment against the original allowing codec delay/lossy differences, not an impossible byte-equality test. Catch silent output, late starts, early cut-offs or an accidentally repeated song.
- Inspect beginning, multiple repeat boundaries, middle, final partial cycle and end; verify actual finished-player playback with working sound controls. Compare source/finished colour on matched frames. Do not claim you listened if evidence is only waveform/correlation or muted browser playback; disclose the actual verification mode honestly.
- Produce a NEW local full-MV review/download page (new direct page or genuinely new Lavish session), with user-initiated Play, clear sound controls, full movie, thumbnail and editable-project links. Never autoplay loud music or reopen an ended session. No placeholder/partial MP4 delivery.
- Preserve a compact central snapshot of the final edit, required owned assets, final movie, thumbnail and concise reproduction/QA records before any later cleanup. Preserve old sources/movies/user-look resources and>=32GiB free. No AI weights/add-ons/download campaign.
- Deliver the concrete full-MV URL/path and thumbnail through verified owner→Silas→Gru callbacks; keep USER LOOK ACTIVE resources available until the user finishes. No need to relay repeated hashes/frame allocations. No worker left unmonitored; healthy export isn't killed for an early ETA.

## Fences and ops

Old55-shot Selva story/AI lanes remain HUMAN-STOP_PARKED and weights REMOVED. No H3/other-film changes, Resolve, uploads, publishing, remote commits, PR or merge is inferred. PP3D remains independent; no system-wide process cull or GPU serialization. One owned worker/live-editor within this lane, as before.

Silas: amend the SAME row's note/briefing pointer and deliver this to the existing idle owner; verify accepted handover and actual resumed work. Do not mistake the old “no full-song” receipts for current authority after this explicit user GO. No new user gate before native assembly. Report the final artifact, not preparation paperwork.
