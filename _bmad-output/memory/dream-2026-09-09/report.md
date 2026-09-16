# Dream report — 2026-09-09

Material: **2 shards (9 entries), 115 journal source blocks (113 post-marker, 2 boundary-uncertain), 25 ledger jobs (414 events)** since **2026-09-07T00:39:44Z**, through the pass cutoff **2026-09-09T00:50:25.251361Z**.

| 🧠 Result | Count / disposition |
|---|---|
| Source readers | 3 sheep; all output shards delivered; all 3 panes explicitly closed |
| Candidate patterns | 10 raw headings → 9 distinct patterns |
| Accepted proposals | **7: 6 auto + 1 user-ack** |
| Watch items | **10**, not promoted |
| Standalone candidates rejected after consolidation | 2; additional already-curated recurrences listed below |
| Live state | Memory files and last-dream untouched by Bob; no PR, repo task work or application mutation |

## Coverage and dating

- **Shards:** 2 newer-mtime files read completely; 211 older files tail-screened. Three typography bullets are dated 09-08. Six Selva bullets have only a 09-07 date; Bob resolved their marker-boundary uncertainty against the canonical job's `started_at=2026-09-07T15:25:06Z` and the post-dispatch journal history. These are nine new job entries, not nine independent incidents.
- **Journals:** 8 newer-mtime files read completely across Gru and Silas; 58 older files tail-screened. Units are `##` sections or, for unheaded Silas logs, blank-line-separated event groups. Cross-writer accounts count toward coverage but never double-count an incident. Two late-written old-filename journals (`gru-journal/2026-09-06.md`, `silas-journal/2026-09-03.md`) supplied 12 content-date intake blocks; two remain boundary-uncertain and are not needed for a proposal. Thus neither filenames nor mtimes were used as event dates.
- **Ledger:** latest 200 covered only back to 09-08T01:01:55Z. A read-only interval census recovered **216 older omitted rows**: 416 total interval rows, less this dream's 2 rows = **414 material events / 25 jobs**. Every interval job was read with `ledger show`. Prior-dream close-out five seconds after the marker is counted but yields no pattern. Forty pre-marker DB events were also screened.
- **Total file intake:** 10 full newer-mtime files plus **269 older file tails**. Older corroborators are cited as history, not counted again as new material. No optional production-pane transcript reader was needed.
- Detailed censuses and caveats: [shards](sheep-shards.md), [journals](sheep-journals.md), [ledger](sheep-ledger.md). Primary cited journal/shard snapshots are under `inputs/cited-sources/`; the read-only event snapshot is `inputs/ledger-interval.json`.

## Proposals

All paths below are relative to `/Users/moses/code` unless stated otherwise. Exact edits are already applied to the **cloned** `store/` files. Evidence denotes recorded observations/receipts, not tests rerun by Bob.

### P1 — Retire the locally fixed BMad ambiguity waiver, without conflating missing renderers

- **Target:** `docs/minion-field-notes.md`, historical BMad tooling entry · **Class: auto** (stale wording correction).
- **Change:** mark the 6.11 failure/workaround historical and append the already-codified 09-07 local retirement: installed 6.12.0 repair accepts duplicate keys only when all resolve identically; conflicts/missing config still halt. Point to the current annex and hash-gated patch documentation. Keep a missing renderer in another checkout a separate diagnosis; do not inherit a waiver from old notes.
- **Evidence:** `youtube-channel-selva-electrica-assets-rigs`, 09-07, `field-notes/youtube-channel-selva-electrica-assets-rigs.md:3`: “bmad-build render_skill.py succeeded in this worktree”. Independently, `my-orchestrator-bmad-build-config-unblock-pp3d` / PP3D parent, 09-07, `silas-journal/2026-09-07.md:283–285`: “manifest and 14/14 output hashes verified”; parent independently reran and resumed. Current `docs/playbook-annex.md:556–565` explicitly says the former ambiguity waiver “is retired locally”.
- **Reasoning:** the curated file still said the waiver remained standing until a real fix landed; that fix is now recorded and delivered. This synchronizes memory to existing canon, not a new workflow permission.

### P2 — Certify the final evaluated representation

- **Target:** `docs/minion-field-notes.md`, independent-anchor convention · **Class: auto** (shard promotion).
- **Change:** capture evidence carries decoded dimensions and source SHA before cropping/normalization; geometry checks observe evaluated world-space support, exact part/side and active modifiers; saved/reopened or appended timeline behavior is checked separately from manual sliders. Intermediate views remain diagnostic, not final-contract substitutes.
- **Evidence:** `packet-plumber-3d-typography-video-study`, 09-08, its field-note shard: “captures at 0818afc2 decode as1600×450 despite base1600×900”. `youtube-channel-selva-electrica-assets-rigs`, 09-07, its shard: “Contact tests must observe evaluated world-space support, not a copied formula”. Independent historical asset-scout bbox measurements corroborate the same final-transform principle without adding new material counts.
- **Reasoning:** viewport normalization and evaluated modifiers can invalidate otherwise plausible source-level or crop-level assertions. This adds the final-stage transform boundary to the existing independent-anchor rule.

### P3 — Artifact existence after timeout is not completion

- **Target:** `docs/minion-field-notes.md`, tool/bridge-timeout entry · **Class: auto** (shard promotion/addendum).
- **Change:** inspect producer liveness before retrying; publication requires attempt/source identity, fresh and complete outputs, producer result and the job's semantic gates. Partial attempts stay diagnostic; do not splice them into one claimed complete proof.
- **Evidence:** `youtube-channel-selva-electrica-assets-rigs`, 09-07, shard line 6: “require complete exit-zero evidence before atomic gate publication; never splice a timed-out partial attempt”. Independent historical `packet-plumber-v2-blender-sculpt`, 08-23, shard lines 3–8: failed piped Blender runs left stale files that `cmp` compared as alleged determinism proof.
- **Reasoning:** hardens the existing advice to check artifacts after transport timeouts without creating its unsafe inverse, “a file exists, therefore the job passed”. The 08-23 corroborator was read directly, not counted as new.

### P4 — Verify thinking provenance as well as model identity

- **Target:** `AGENTS.md`, append to Model dispatch & correction ops gotcha · **Class: auto** (gotcha append, existing policy unchanged).
- **Change:** explicitly supersede the historical blanket-max recipe with a reminder to verify persisted model and thinking events. Astra/Sol xhigh and Luna max are distinct policy values. Correct `/thinking` in place and verify continued progress; do not import `/model` turn behavior by assumption.
- **Evidence:** `packet-plumber-3d-typography-video-study`, 09-08, ledger event **4904**: “Initial session event recorded thinkingLevel=max”; `/thinking xhigh` corrected the same session. Separate storyboard/SOMA dispatch batch, 09-08, ledger **5058/5059**: “initially recorded max” and same-session xhigh corrections. The two sibling jobs count as **one batch incident**, giving two independent incidents total.
- **Reasoning:** all these sessions had the correct model while the thinking setting was wrong. Session modelId alone did not prove the launch envelope. No launcher/code fix is claimed here.

### P5 — Recheck shared Blender state at the live action boundary

- **Target:** `AGENTS.md`, gotcha append under Pane forensics · **Class: auto** (gotcha promotion).
- **Change:** reservation/handshake/old checkpoint is not live-state clearance. Before restart, load/restore or first mutation after handoff, freshly check owner, exact file/scene, dirty state/frame, jobs/playback and workers. Unexplained drift stops the live action and requires preservation/reconciliation under existing authority. Isolated-copy/read-only work stays distinct; newest observation time, not latest relay arrival, determines which clearance is current.
- **Evidence:** `my-orchestrator-blender-mcp-reliable-startup`, 09-07, `gru-journal/2026-09-07.md:49–63`: “LIVE CHECK CAUGHT UNSAVED WORK” at frame83 despite idle workers; a later verified clean receipt superseded the older dirty relay. Independent next-day `youtube-channel-selva-electrica-assets-rigs`, 09-08, `gru-journal/2026-09-08.md:69–77` and ledger 11:24:42Z: same PID/hash/owner/no jobs, but dirty frame129 rather than clean frame42.
- **Reasoning:** avoids losing unsaved application state while also avoiding an indefinite hold based on stale clearance evidence. The later 43-orphan save-copy problem is deliberately **not** generalized into this proposal.

### P6 — Make the visual viewing handoff explicit and usable

- **Target:** `docs/minion-field-notes.md`, Lavish/artifact-delivery tooling entry · **Class: auto** (cross-job lesson promotion).
- **Change:** for requested visual delivery, verify the exact artifact and agreed viewing/review path, then give a conspicuous READY TO WATCH/REVIEW message. A browser-open action is not feedback monitoring; confirm the owner poll/supported wake path. Opening a player requires authorization; otherwise provide a clear usable path. Opened, watched and approved remain separate claims.
- **Evidence:** `youtube-channel-selva-electrica-assets-rigs`, 09-08, `gru-journal/2026-09-08.md:227–233`: user “how was I supposed to know?”; “a local file link did not constitute a clear viewing handoff”. Separate `youtube-channel-selva-full-song-storyboard`, 09-08, journal line 310: “owner opened browser before finishing mechanical preflight and never started poll”.
- **Reasoning:** a finished file and an opened page each failed to deliver the intended user experience. This is a delivery lesson, not permission to steal focus or claim aesthetic approval.

### U1 — Distinguish durable authority from expiring readiness

- **Target:** `AGENTS.md`, proposed gotcha append under Dispatch & handover · **Class: user-ack** (operational workflow clarification).
- **Change:** separately record the explicit grant's scope, owner, attempt budget and superseding holds versus immediate resource/dirty-state/watchdog/preflight readiness. If only readiness is missing or expired, reconcile and freshly recheck before executing the still-unconsumed unchanged scope; do not require a redundant A/E or end the turn until the short-lived preflight expires. A later stop, changed scope/ownership, consumed attempt or terminal cancellation still controls; **no retry or revival is implied**.
- **Evidence:** `youtube-channel-selva-electrica-assets-rigs`, 09-08, ledger 11:24:42Z: “Approval remains valid; explicit provenance/preservation direction required before implementation.” Independent `packet-plumber-3d-planet-life-router-legibility`, 09-08, ledger 16:32:04Z: “existing three-stage grant is sufficient; no additional A/E”; 18:07:00Z: the unchanged grant's 60-second preflight had expired. `gru-journal/2026-09-09.md:20` records the owner ending its turn instead of executing.
- **Counterevidence/limit:** Selva's later hard stop superseded the topology grant; PP3D FAMILY's terminal diagnostic failure cancelled the two remaining stages. Neither can resume through this proposed clarification.
- **Reasoning:** prevents both repeated approval loops and accidental autonomous restart. Although supported by two jobs, generalizing the gate-handling process deserves explicit user acknowledgment. **Do not apply U1 with the autos.**

## Watch items (anecdotes — tracked, not proposed)

| 👀 ID | Observation / source | Why it stays a watch |
|---|---|---|
| W1 | Selva 09-07: process-local Metal-only completed the 156-frame source in 537.52s; asset/rig shard line 6 | One controlled scene result, not general hardware policy |
| W2 | Selva 09-08: normal save-copy omitted **43 zero-user non-fake datablocks**; ledger 12:58:43Z, later preserved 43/43 | One completeness mechanism; do not certify ordinary copies as lossless |
| W3 | L1-refine 09-07: mutation exercise restored a stale whole `props.gd`, resurrecting old code; ledger 02:43:50Z | One newly recorded restoration mechanism |
| W4 | Selva 09-08: 42-mesh wing/leg collision inventory omitted eyes; previous GREEN did not cover the new defect; Gru journal :238 | One repair arc; explicit animated contact-inventory rule needs independent recurrence |
| W5 | Storyboard caption setup 09-08: venv-local copies misclassified as global mutation, then absent metadata misclassified as a license verdict; Gru journal :338/:345 | Two assertions in one setup sequence, not independent sightings |
| W6 | Storyboard 09-08: identified-actor same-session API messages released the existing foreground poll; Gru journal :334/:345 | Repeated UIDs within one job/session/day; not a general recovery protocol yet |
| W7 | PP3D FAMILY 09-09: exit0 and decodable media, but shutdown ERROR diagnostics caused fail-closed cancellation; Gru journal :29–35 | One native cleanup-error episode; cause/harmlessness not established |
| W8 | PP3D preview 09-08: initial wrong scene/startup error despite a launched window; corrected exact-SHA archive used explicit main scene; Gru journal :47 | One preview-launch episode; not a new runtime-wide defect claim |
| W9 | SOMA research 09-08: official Python ARM failure did not establish a failure of the separately supported C++ SOMA30 route; Gru journal :301–305 | One premise correction; user parked research, no runtime/adoption inference |
| W10 | This dream: legacy `bmad-review-adversarial-general/SKILL.md` aliases resolve to a missing canonical directory | One current workflow-reference gap; successor rubric used and disclosed, no skill/config repair performed |

## Pruned / rejected candidates (with why)

- **Immediate successor receipt as a separate new doctrine:** two real gaps (Selva helper handback idle ~92 minutes; PP3D passed preflight expired). Existing W3/async completion-relay doctrine already covers missed continuation. Retain the expiring-preflight facet in U1, not another standalone entry.
- **Newest terminal state as a separate new rule:** the sheep's novelty claim does not survive comparison with the existing user-reversal, hold and amend/relay rules. Its evidence supplies U1's essential no-revival boundary instead.
- **Ended Lavish with pending prompts:** current storyboard recurrence is already covered by the 08-03/08-09 state.json/final-feedback entries; no extra watch/proposal.
- **GPT routing/native vision, direct Blender route, music-video no-Perkins, asset doctrine/private remote:** current user policy or already-delivered project canon, not new evidence-derived policy. Do not duplicate the complete studio doctrine into global memory or generalize it to game/tooling work.
- **Stale pane IDs, stuck-working/settle noise, direct in-pane user provenance, no-PR notification requirements, claim falsification:** fresh recurrence without enough new mechanism to earn more text.
- **401 route hold + 403 source frames as a combined access doctrine:** different authority/evidence boundaries; rejected as over-abstract.
- **Watcher volume, duplicate journal accounts, sibling batch members and repeated caption attempts:** never counted as independent sightings.

## Verification and application contract

[verification.md](verification.md) records the adversarial challenges, candidate mapping and limits. The named legacy review skill was unavailable; its installed successor adversarial lens was used as a rubric, not represented as execution of the missing skill. Read-only sensor/config grep found no stale BMad ambiguity-waiver string and current GPT role comments; no tooling changes were made.

| 📦 Artifact | Application rule |
|---|---|
| [auto.patch](auto.patch) | Six auto proposals only; review/apply against current live files |
| [user-ack-U1.patch](user-ack-U1.patch) | Separate U1 patch; **hold for user acknowledgment** |
| [all-proposals.patch](all-proposals.patch), `store/` | Include BOTH classes; **never copy the entire store over live memory blindly** |
| [patch-manifest.json](patch-manifest.json) | Baseline/proposed hashes and class split |
| `spawn-provenance.json`, `sheep-*-closed.json` | Explicit Sol/xhigh/cwd/handover receipts and owned-pane cleanup |
| `completion-validation.json` | Final hash, patch-composition and cleanup checks |

Bob does not apply live proposals or write last-dream. Silas owns application, U1 routing, marker update and final close-out. No follow-up task, policy switch, user-media reopening, merge or production restart is authorized by this report.
