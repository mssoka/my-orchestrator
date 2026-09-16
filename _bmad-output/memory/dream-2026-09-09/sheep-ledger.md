# Sheep ledger — 2026-09-09

## Coverage

### Sources and counting

| 🔎 Source | Coverage |
|---|---|
| `/Users/moses/code/_bmad-output/memory/dream-2026-09-09/inputs/ledger-events-200.txt` | Read completely: 200 event rows, newest `2026-09-09T00:49:30Z`, oldest `2026-09-08T01:01:55Z`. |
| `/Users/moses/code/_bmad-output/orchestrator.db` | Queried read-only for `ts > 2026-09-07T00:39:44Z` through pass start `2026-09-09T00:50:25.251361+00:00`: 416 event rows across 26 jobs. This recovered the 216 rows omitted by the rolling latest-200 file. |
| `/Users/moses/code/bin/ledger show <id>` | Run for every one of the 26 jobs below; all job fields and complete event histories were inspected. |
| Older-tail screen | Read the 40 database events immediately at/before the marker (`2026-09-06T20:02:28Z` through `2026-09-07T00:39:11Z`). No late backfill with post-marker content was found. |
| Dedup stores | Target-searched cloned `store/AGENTS.md` and `store/minion-field-notes.md`; read the relevant model-policy, launch-envelope, Lavish, and pane-forensics passages. |

Counting unit below is a `job_events` database row, not a status change and not a sighting. Repeated watcher classifications, corrections, receipts, and cross-job notes about one incident were collapsed to one sighting during pattern analysis. The current `dream-2026-09-09` row's 2 events are covered but excluded from material counts, leaving **414 material event rows across 25 jobs**. All ledger events have exact timestamps; there is no same-day/timeless boundary uncertainty. The two `dream-2026-09-07` closure events are five seconds after the marker and were retained in coverage but yielded no candidate. No source gap remains after the read-only database census and all-job `ledger show` pass.

### Complete interval job census

| 🧾 Job id | Events |
|---|---:|
| `dream-2026-09-07` | 2 |
| `dream-2026-09-09` | 2 *(excluded from material analysis)* |
| `h3-local-production-queue` | 2 |
| `model-policy-gpt-2026-09-07` | 5 |
| `model-policy-vision-routing-followup-2026-09-07` | 6 |
| `my-orchestrator-blender-mcp-reliable-startup` | 19 |
| `my-orchestrator-bmad-build-config-unblock-pp3d` | 9 |
| `my-orchestrator-video-route-canon-2026-09-07` | 5 |
| `orchestrator-lens-layout-and-stuck-sensor` | 9 |
| `orchestrator-minion-sweeper` | 1 |
| `packet-plumber-3d-l1-refine-1` | 23 |
| `packet-plumber-3d-l1-refine-1-perkins-r3` | 6 |
| `packet-plumber-3d-l1-refine-1-perkins-r4` | 8 |
| `packet-plumber-3d-l1-refine-1-perkins-r5` | 8 |
| `packet-plumber-3d-l1-refine-1-perkins-r6` | 10 |
| `packet-plumber-3d-l1-refine-1-perkins-r7` | 4 |
| `packet-plumber-3d-planet-life-router-legibility` | 109 |
| `packet-plumber-3d-typography-video-study` | 13 |
| `righttenantry-agents-wif-durable` | 1 |
| `youtube-channel-kimodo-soma-exploration` | 12 |
| `youtube-channel-music-video-visual-review-policy` | 5 |
| `youtube-channel-selva-electrica-assets-rigs` | 124 |
| `youtube-channel-selva-full-song-storyboard` | 25 |
| `youtube-channel-video-lane-asset-doctrine` | 4 |
| `youtube-channel-video-route-canon-2026-09-07` | 2 |
| `youtube-channel-video-route-canon-delivery` | 2 |
| **Total** | **416** |

## Candidate patterns

### 1. Thinking level is a value-specific part of model provenance; retire blanket `max`

**Proposed lesson/target.** Every launch surface must derive both `--model` and the exact `--thinking` value from the current model policy, then verify the persisted session event. `max` and `xhigh` are distinct, not aliases. A live mismatch can be corrected in place with `/thinking <required-level>` and a recorded session event; it does not require kill/re-dispatch.

**Evidence (3 job rows, 2 independent dispatch incidents; the storyboard/SOMA pair was one correlated batch):**

- `/Users/moses/code/_bmad-output/orchestrator.db`, `job_events.id=4904`, entry `2026-09-08T00:31:32Z`, job `packet-plumber-3d-typography-video-study` — **verbatim:** “Initial session event recorded thinkingLevel=max at 00:21:57.945Z; sent /thinking xhigh to live pane w85:pNA (no respawn/model change), and session now records thinking_level_change xhigh at 00:31:07.336Z with pane footer xhigh.”
- `inputs/ledger-events-200.txt:49`, entry `2026-09-08T19:12:38Z`, job `youtube-channel-selva-full-song-storyboard` — **verbatim:** “Dispatch-envelope correction verified: session JSONL initially recorded max at 19:05:02.286Z; in-place /thinking xhigh produced thinking_level_change xhigh at 19:11:17.014Z in same session/model/pane, no restart/kill/redispatch.”
- `inputs/ledger-events-200.txt:48`, entry `2026-09-08T19:12:38Z`, job `youtube-channel-kimodo-soma-exploration` — **verbatim:** “Dispatch-envelope correction verified: session JSONL initially recorded max at 19:06:46.084Z; in-place /thinking xhigh produced thinking_level_change xhigh at 19:11:17.021Z in same session/model/pane, no restart/kill/redispatch.”

**Novelty/dedup.** This is a **correction/addendum**, not a new model policy. Cloned `store/AGENTS.md:349-355` already records the current value-specific GPT policy (Astra/Sol `xhigh`, Luna `max`), while stale historical text at `store/AGENTS.md:672-674` still says “`--thinking max` on EVERY agent launch.” The incidents show that contradiction is operational, not editorial.

**Counterevidence and limits.** Other new GPT launches were correct (`youtube-channel-selva-electrica-assets-rigs`, entry `2026-09-07T15:26:06Z`, and `packet-plumber-3d-planet-life-router-legibility`, entry `2026-09-07T17:52:18Z`, both persisted Astra/xhigh). Therefore this is not a provider-wide serialization bug; it is dispatch-surface/config drift. The evidence supports in-place correction for `/thinking`; it does not establish that every slash command has identical turn-resume semantics.

**Disposition.** **Promote.** Supersede the blanket-max sentence and harden launch templates/tests to assert the exact policy pair `(modelId, thinkingLevel)` from session JSONL.

### 2. Shared interactive Blender state must be re-probed at every destructive action boundary

**Proposed lesson/target.** Before restart, file load/restore, or first mutation against a shared interactive Blender, freshly verify exact file/scene identity, owner, dirty bit, frame, jobs/playback, and workers. A prior clean check, checkpoint, approval, or connectivity handshake is not transferable across an action boundary. If state drifted, stop before touching it and preserve/reconcile first.

**Evidence (3 independent state-drift episodes across 2 job rows):**

- `/Users/moses/code/_bmad-output/orchestrator.db`, entry `2026-09-07T20:34:34Z`, job `my-orchestrator-blender-mcp-reliable-startup` — **verbatim:** “Fresh Selva receipt is explicit restart_clearance=false: live GUI scene at frame 83 is dirty despite checkpoint copy; all supported jobs/playback and native workers are idle/empty. Hold install/restart; do not use the prior connectivity success or old hero_moth checkpoint.”
- `inputs/ledger-events-200.txt:145`, entry `2026-09-08T11:24:42Z`, job `youtube-channel-selva-electrica-assets-rigs` — **verbatim:** “NEW SAFETY BLOCK after delegated plan release: fresh direct MCP at required pre-mutation check found PID59538 on exact hero_showcase-v5 disk hash eefbeac976a5cc333f12ba013f2e28da03818cb71c00ace401e13061ebe00b93, SELVA_Hero_04/owner w85:pNE, no jobs/playback, but dirty=true at frame129 versus prior clean frame42.”
- `inputs/ledger-events-200.txt:133`, entry `2026-09-08T12:23:31Z`, same job but a later post-geometry boundary — **verbatim:** “Fresh reconciliation found PID59538 live v6 hero_showcase-v6.blend disk SHA8fe8bbfa2fad3eecf4a1615983df5404f1feade27a8eb56da9dbbf776d83d51d dirty=true/frame69 vs clean/frame42, owner pNG, no jobs/playback. Cause unknown; pNG and pNE stopped native writes/return.”

**Novelty/dedup.** **Novel** in the cloned curated memory: targeted searches found no shared-Blender dirty-state/action-boundary doctrine. Existing pane/process forensics are analogous but do not protect authored application state.

**Counterevidence and limits.** Dirty state does not ban all work. At `inputs/ledger-events-200.txt:63` (`2026-09-08T18:26:25Z`) the lane safely continued CPU-only analysis from isolated copies while the interactive scene remained dirty. The guard applies to actions that can overwrite, reload, restart, or mutate shared state—not read-only census or isolated-copy work. A dirty bit alone also does not establish authorship or harmful change; that uncertainty is precisely why the action must halt.

**Disposition.** **Promote** as a shared-Blender safety addendum, scoped to destructive/live mutation boundaries.

### 3. Keep durable scope authority separate from expiring operational readiness

**Proposed lesson/target.** Represent two gates independently: (1) the durable grant for an exact scope, owner, and attempt budget; (2) ephemeral readiness evidence such as process census, dirty-state clearance, or a short-TTL preflight. Failure/expiry of readiness blocks execution but does not silently revoke the unchanged scope grant or justify repeating a human A/E question. Resume only after repairing the missing condition and rerunning the immediate preflight. A later user hold, scope change, ownership change, or superseding ruling still invalidates the grant.

**Evidence (2 independent jobs/mechanisms):**

- `inputs/ledger-events-200.txt:145`, entry `2026-09-08T11:24:42Z`, job `youtube-channel-selva-electrica-assets-rigs` — **verbatim:** “Approval remains valid; explicit provenance/preservation direction required before implementation.”
- `inputs/ledger-events-200.txt:91`, entry `2026-09-08T16:32:04Z`, job `packet-plumber-3d-planet-life-router-legibility` — **verbatim:** “Once effective external watchdog/live-size-cap receipts and a repeated immediate safe preflight are verified, existing three-stage grant is sufficient; no additional A/E or repeated plan approval needed for unchanged scope.”
- Same PP3D incident, `inputs/ledger-events-200.txt:68`, entry `2026-09-08T18:07:00Z` — **verbatim:** “Existing grant is unchanged, but 60s preflight is expired and any later stage requires fresh immediate checks plus parent policy review.”

**Novelty/dedup.** **Possible addendum.** Existing memory has durable ledger routing and user-gate doctrines, but targeted searches found no explicit authority-versus-readiness distinction.

**Counterevidence and limits.** This must not become autonomous permission. In `youtube-channel-selva-electrica-assets-rigs` at `2026-09-08T19:50:03Z`, a later hard stop explicitly superseded the earlier topology approval; the row correctly performed no trial. Likewise PP3D's eventual stage failed closed and cancelled the remaining stages. The lesson only preserves an explicit unchanged grant; it cannot infer one or broaden it.

**Disposition.** **Promote cautiously** as an operational gate distinction, retaining the exact “unchanged scope/owner and no later hold” qualifier.

## Watch items

### User-ended Lavish can still contain unconsumed prompts

Single incident; do not promote yet. `inputs/ledger-events-200.txt:13`, entry `2026-09-08T23:59:03Z`, job `youtube-channel-selva-full-song-storyboard` — **verbatim:** “f576e37752952bdc is now actually status=ended, ended_by=user, pending_prompts=2, artifact_revision=17; no foreground poll exists.” The lane preserved the exact prompt texts read-only and did not claim consumption or reopen. This qualifies the existing field note that Send-&-End feedback arrives on the next poll: there may be no live poll. One case is insufficient to define the general recovery API; retain as a watch item.

### Blender save-copy may omit zero-user non-fake datablocks

Single mechanism within the second dirty-state episode; do not generalize yet. `inputs/ledger-events-200.txt:122`, entry `2026-09-08T12:58:43Z`, job `youtube-channel-selva-electrica-assets-rigs` — **verbatim:** “43 live zero-user non-fake datablocks omitted by save-copy (42 meshes + 1 armature), authorship/change history unknown; existing checkpoint SHA 0fbf71c5245bf877e77a7bfe0a68f6d9db4bd64ebbe182a4349ebe4774822172 incomplete for these IDs.” The successful preservation receipt at line 113 captured 43/43 before restore. Keep this as a Blender-specific completeness warning pending an independent recurrence.

### Whole-file mutation restoration can resurrect stale code

Single new incident. In `packet-plumber-3d-l1-refine-1`, entry `2026-09-07T02:43:50Z`, the fold reported — **verbatim:** “root cause: the r3 mutation-leg exercise restored a STALE props.gd backup predating three r3 edits; only the attitude edits were re-applied.” The corrective cull-parity mutation caught the regression. Candidate future guard: mutation legs should restore only their mutation or verify the complete target file/tree against the pre-leg snapshot after restoration. One occurrence is not enough to promote.

## Rejected/duplicate candidates

- **Stuck-working false positives — duplicate doctrine, no new promotion.** Three fresh false-positive episodes occurred: long PP3D verification (`inputs/ledger-events-200.txt:185`), long PP3D mutation generation (`:98`), and a foreground Lavish poll (`:25`). A true `terminated` error was also correctly classified and continued once in Selva at `2026-09-07T21:51:19Z`. This is useful validation of the new detection-only sensor, but cloned `store/AGENTS.md:1398-1404` already says session mtime/tool-use growth precedes any continue/revive reflex, and the sensor shipped as detection-only. Do not duplicate it.
- **Latest user ruling supersedes prior approval — existing reversal doctrine.** The Selva topology grant was superseded minutes later by the user's hard stop; this is another clean occurrence of the already-curated amend/relay and user-reversal rules, not a new rule.
- **Cache/claim falsification — existing bytes-not-claims family.** The L1 lane retracted its “live glTF dependency” claim after a fresh-checkout reproduction exposed stale `.godot` cache evidence. This is strong execution of existing verify-not-assume and claimed-but-did-not-land doctrine, not a separate promotion.
- **Current GPT model/vision route and direct-Blender video route — policy, not inferred memory.** These are current user rulings already present in cloned `AGENTS.md`; this pass must not reinterpret them as autonomous policy.
- **Watcher/status volume — rejected as counting noise.** The PP3D and Selva rows contain many repeated receipts, settle classifications, and same-incident corrections. Their 109/124 event totals are not sightings and were not used as recurrence evidence.
- **No-remote delivery and post-merge follow-up PR — single operational cases.** The youtube repo initially lacked a remote and PR #20 received a post-merge amendment requiring PR #21. Both were handled safely, but neither recurred independently in this interval.
