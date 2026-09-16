# Dream report — 2026-09-15
Material: 3 field-note shards read (1 post-marker: dream-2026-09-13's own 3
one-liners; whole-store grep proved zero other post-marker shards), 4 journal
files (gru+silas 09-13 post-marker halves, gru+silas 09-14 full = ~330 lines),
12 ledger jobs (full job_events census, pre-dumped for the sheep), since
2026-09-13T03:03:31Z. Sheep: sheep-shards (p14E), sheep-journals (p14C),
sheep-ledger (p14D), all glm-5.3@max session-verified, all closed.

## Proposals

### P1 — PI_MODEL/PI_PROVIDER inheritance defeats launch pins on DIRECT LENS spawns
- Target: AGENTS.md (Model dispatch & correction ops, appended to the 09-07
  PI_MODEL addendum) · Class: **auto** (APPLIED to store copy)
- Change: dated 2026-09-13 addendum: lens panes inherit the round main's env —
  5 r3 lens panes came up glm-5.3/high despite an explicit Astra/xhigh pin
  (root cause: inherited PI_MODEL/PI_PROVIDER + `~/.pi/agent/settings.json`
  global glm defaults); clear the env on every spawn surface, verify each
  lens session's modelId (filename timestamps ≠ header ids); caught
  pre-output = in-place /model correction (perkins-r2 precedent), caught
  post-output = corrected relaunch, no blind revert.
- Evidence: ledger 17:51:49Z 09-13 "MODEL PROVENANCE INCIDENT 2026-09-13:
  actual r3 lenses p112/p00/p111/p114/p115 recorded zai-coding-cn/glm-5.3 at
  high despite pYQ launch command explicitly pinning openai-codex/gpt-6-astra
  xhigh." + "Live p0Z shell probe proved inherited PI_MODEL=glm-5.3 and
  PI_PROVIDER=zai-coding-cn"; gru-journal 09-13 "Primary forensics
  verified5active non-blind sessions actuallyGLM/high despite parent17:06
  launchtool explicitlypinningAstra/xhigh" (USER-CAUGHT); perkins-r2 02:33Z
  09-13 in-place correction as the pre-output variant.
- Reasoning: the 09-07 gotcha covered the relaunch flavor; the 09-13 incident
  is the lens-fleet flavor (user-spotted) — under hold regimes this silently
  invalidates whole review waves for their intended tier.

### P2 — Close-out sweeps race tree-rooted daemons and user-facing paths
- Target: AGENTS.md (Pane forensics section, new bullet) · Class: **auto**
  (APPLIED to store copy)
- Change: new gotcha bullet: before `worktree remove`, enumerate non-pane
  daemons (`lsof +D <worktree>` / listening ports), order preserve-first
  dependencies BEFORE the sweep (re-root servers, preserve untracked user
  deliverables), re-anchor every user-facing path handed out earlier
  (playables/links/aliases — hand over from stable roots), and include
  `git worktree list` in censuses (husk worktrees escape ledger+pane sweeps;
  failing `branch -D` = a worktree still pins the branch).
- Evidence: gru-journal 09-14 "GRU CAUGHT A SWEEP-RACE: Silas swept the
  worktree BEFORE re-rooting the gallery servers — both (8794/8795) orphaned
  on the deleted cwd, serving 404s"; silas-journal 09-14 "close-outs should
  check `lsof +D <worktree>` / listening-port daemons rooted in a worktree
  before `worktree remove --force` (pane sweep alone is insufficient — the
  08-27 orphan-process class, media-server flavor)"; ledger 09-14 "32 mp4s"
  LINK-RESTORATION + l1-spawn "PRESERVE-FIRST: user playable b40 ... the
  worktree-relative playable path in the ACK is DEAD"; silas-journal 09-14
  "ACK handover paths pointing INTO a worktree die at close-out — either
  preserve-first + relay the new path, or hand over from a stable root".
- Reasoning: 2 independent close-outs same day + the codified 08-27 orphan
  class = a recurring loss shape with a cheap pre-sweep check; central
  preserves made both recoveries lossless, but the check prevents the race.

### P3 — HOLD #2 (2026-09-14) dated record in the AGENTS.md interlude block
- Target: AGENTS.md (HOLD INTERLUDE block, after the LIFTED-09-12 paragraph)
  · Class: **user-ack** (applied to STORE COPY ONLY — needs sign-off)
- Change: a duration-limited HOLD #2 paragraph: verbatim user quotes, same
  GLM-interim recovery shape (glm-5.3@max code/Perkins, flash@high Silas),
  in-place event-verified flips, Silas mid-relay death revived same
  pane/session, watchman pins invalid, resume ONLY on explicit user token
  confirmation, visual legs deferred-not-waived, durable doc carries the
  second-hold section.
- Evidence: gru-journal 09-14 "we are out of tokens with astra. openai." /
  "so we are back to glm fully." / "Silas DIED on the cap mid-relay (Codex
  usage-limit error in pane); Gru revived same pane/session"; ledger
  "OPENAI QUOTA HOLD #2 (user ruling 2026-09-14, GPT chain suspended not
  retired)".
- Reasoning: the store's interlude currently ends at LIFTED-09-12/GPT-chain
  resumed — stale under hold #2 and a misroute risk for any session reading
  AGENTS.md as current policy; this dream itself was dispatched under the
  hold (glm-5.3 sheep). Flagged user-ack because it amends model-policy
  status text, not a pure gotcha append.

### P4 — Provenance test cuts both ways (genuine role:user; unbranded ACKs)
- Target: AGENTS.md (appended to the 09-13 `role:user` TRANSPORT-label gotcha)
  · Class: **auto** (APPLIED to store copy)
- Change: one addendum: a direct typed `retry` (16:54:15Z 09-13) WAS genuine
  human input and overrode a stale BLOCKED disposition; an unbranded ACK had
  its claim gh-verified before any ledger action — origin-session forensics +
  independent ground truth decide in both directions; the label (present or
  absent) never does.
- Evidence: ledger "session forensics then showed a new direct role=user
  input `retry` at 16:54:15Z"; silas-journal 09-14 "ACK arrived in my pane
  unbranded (no [GRU]/[MINION] prefix) — treated as the round main's closing
  report and verified against gh before ANY ledger action".
- Reasoning: the 09-13 gotcha's guard direction (distrust role:user) needs
  its inverse explicitly, or the doctrine over-rotates into ignoring genuine
  user input; two same-window sightings, one each direction.

### P5 — Dream-template model lines rot
- Target: AGENTS.md (appended to the 09-02 briefing-model-line-rot addendum)
  · Class: **auto** (APPLIED to store copy)
- Change: one addendum: the DREAM template's kimi line was stale at BOTH
  dream-2026-09-13 and dream-2026-09-15 dispatches (hold-era glm correction
  each time) — re-pin Bob/sheep model lines from the current regime at every
  dream dispatch; session-verify after launch.
- Evidence: silas-journal 09-14 "briefing filled from template with the model
  line CORRECTED (template said stale kimi; hold #2 → glm)"; silas-journal
  09-13 "Template was filled and corrected for the current dated OpenAI
  quota-hold".
- Reasoning: ×2 consecutive dreams; extends the known briefing-rot class to
  its last uncovered surface (templates, not just hand-authored briefs).

### P6 — Same-ROW extension shape for creative-lane follow-ons
- Target: AGENTS.md (appended to the mid-flight-reversal gotcha's amendment
  doctrine) · Class: **auto** (APPLIED to store copy)
- Change: one addendum: same-ROW extension = top-linked supersede amendment
  on the controlling brief + SAME row/owner/tree (done→dispatched re-open);
  "deferred" = a NAMED owed deliverable ON the row (the blender-music-video
  skill rode the MV row), never an orphan "later" task; contradicting
  exceptions get written at the TOP of the controlling brief so a stale
  blanket prohibition cannot quiet-park the new mandate.
- Evidence: gru-journal 09-13 "The skill is an explicit owed deliverable on
  SAME row, not an orphan 'later' task." (09-14); "Current comparison brief
  has a top supersede pointer so old no-full-song text cannot quiet-park the
  owner." (09-14); ledger 09-13T22:26:05Z "done -> dispatched SAME-OWNER
  AMENDMENT ACCEPTED: existing row/worktree/pane will resume for the
  five-option comparison"; gru-journal 09-13 six-loop "SAME row /w9Z:p1
  owner/tree" — 3 same-owner extensions + ~6 pivots, zero re-dispatches.
- Reasoning: the healthy follow-on shape at full speed on the Selva lane;
  extends the 09-04 deferred-means-a-row ruling with the same-ROW (not
  new-row) variant and the top-supersede pointer.

### P7 — Tool CALL ≠ RESULT; prepared brief ≠ received mandate
- Target: AGENTS.md (appended to the CLAIMED-BUT-DIDN'T-LAND / bytes-not-
  claims addendum in the Perkins section) · Class: **auto** (APPLIED to store
  copy)
- Change: one addendum stating the forensic rule with both 09-13 examples:
  claims about what an agent DID rest on results (diffs, session-jsonl
  results, gh state) — never on tool-call text, prepared prompts, or
  receipt-constructing pane output.
- Evidence: gru-journal 09-13 "EarlierGru'confirmedmutations'mistooktool
  CALLforRESULT; correctedincidentmemory/briefandpublicwording" and "Gru
  public correction: earlier readPREPARED briefs andmistookthemforreceived
  mandates; user'ssuspicionwasjustified."
- Reasoning: two same-day forensic misreads by Gru (the reader, not the
  agent) in the constellation lane; distinct from the agent-side
  claimed-but-didn't-land class already codified.

### P8 — youtube-channel drops worktrees (standing ruling record)
- Target: AGENTS.md (Dispatch & handover section, new bullet beside the PP
  `--base v2` rule) · Class: **auto** (APPLIED to store copy — ruling record,
  Silas may prefer the playbook)
- Change: one bullet: youtube-channel dispatches default to the main
  checkout `/Users/moses/code/youtube-channel`; worktrees only on genuine
  lane collision; cross-references the close-out sweep-race gotcha as
  rationale.
- Evidence: ledger 2026-09-14T14:50:11Z "STANDING RULING (user, 2026-09-14):
  youtube-channel drops worktrees — future dispatches default to main
  checkout /Users/moses/code/youtube-channel unless two lanes genuinely
  collide." (recorded at PR #4).
- Reasoning: repo-specific dispatch default, user-ruled, mirrors the
  PP-`--base v2` precedent of a one-line gotcha carrying a verbatim ruling.

## Watch items (anecdotes — tracked, not proposed)

1. **Perkins round brief that FORBIDS formal posting + overnight close-out
   gap** (PP3D #42 r2, 09-14): brief banned "PR comments, formal reviews,
   approval" contradicting the playbook; verdict finished 01:17Z, row done
   09:46Z, no URL, result NULL; recovery = same sha + saved artifacts, no
   new fleet. Single sighting — if a round brief ever strips posting duty
   again, promote to a gotcha.
2. **Stuck main inside a long synchronous `wave.py wait` is ALIVE** (r3,
   09-14, ×2 alerts same round): zero jsonl growth by design; check what the
   main is waiting on before nudging. Same class as the codified async-lane
   pre-classification, Perkins flavor.
3. **1302 kills the round MAIN while the wave survives** (#45 r1 ×2 +
   hold-doc stats): already codified; new nuance = alerts queue while Silas
   is between turns (2h dead time caught at wake-up census).
4. **Shard-writing compliance gap**: ZERO field-note shards for the entire
   09-13..15 window across ≥4 badge-outs (l1-spawn-awareness-37,
   selva-electric-loom, thumbnail-ctr-research, davinci probes) — briefings
   reference reading field-notes but the standing badge-out write step
   didn't survive long turns. Same class as the notification checklist-gap;
   candidate for the same template-gate hardening (Silas).
5. **`pr` column self-set 3/3 this window** (loom, #42, #45) — verify-and-set
   guard holding; retire only if the trend persists another window. Delayed
   flavor (pr set after done) still needs the done→in-review transition to
   arm the watcher.
6. **Split per-PR model override by work type** (#42 warning fixes):
   mechanical on glm-5.3@max, narrow vision stays Astra@xhigh, "unless they
   don't fit the criteria" suitability clause; vision leg parked
   deferred-not-waived. One sighting; extends the 09-12 per-PR override
   doctrine.
7. **Scope fences written INTO backlog issue bodies** (#43 stats-chip fence)
   — the fence must travel with the backlog item. One sighting.
8. **In-chat lavish waiver** (plan-before-heist's first application): user
   may waive the lavish page when forks are settled live in chat; the plan
   doc then carries the review. One sighting.
9. **%-completion dual metric** (Selva 30% estimate vs 0/55 hard counter,
   "report both, never inflate from checks/receipts/restarts") — one arc;
   cadence gotcha already covers the spirit; fold at next recurrence.
10. **Healthy-render no-arbitrary-timeout ruling** (Selva-scoped): internal
    8h allocations are not human walls; watchdog ETA projections must not
    kill healthy local renders. Durable in the Selva briefs; one arc.
11. **Premature RUNNING claims** (VSE pack-edit): a shell continuing past a
    Python assertion relayed false RUNNING — claim worker starts only from
    durable START/terminal receipts. One sighting.
12. **Skill-extraction pipeline template** (owner stages/tests → central
    HANDOFF → Silas byte-verified install with collision + discovery check;
    artifact FIRST, no project paths baked in): worked end-to-end once —
    template for future harvests, not yet a pattern.
13. **VSE craft traps** (sRGB wrongly tagged BT709 → metadata-only 2-byte
    fix; uncached MP3 ~23ms start skip → Sound.use_memory_cache=True;
    comparison galleries must be PLAY-verified before a user look): all
    encoded in the installed blender-music-video skill; single-lane.
14. **Locale-drift process-identity guards** (LANG mismatch + trailing-
    whitespace parser rejections): pin LC_ALL=C on producer AND consumer;
    a guard refusal is a comparator bug, not host drift. Two flavors, one
    lane — promote if it recurs outside Selva.
15. **Husk worktrees / branch -D pin** — folded into P2's enumeration clause
    (single direct sighting, selva-pr-media-clean).
16. **Mothball→resume, EXPIRED-CLOSEOUT, frozen allocations, stop-on-
    surprise, USER LOOK ACTIVE, backlog fences, watcher classification
    density, same-status notes** — all confirmations of already-codified
    doctrine; no changes needed.

## Pruned / rejected candidates (with why)

- **"Ledger WORKING is not execution evidence" as a new proposal** — 3 new
  sightings 09-13 but dream-2026-09-13 already consolidated it (store has the
  2026-09-12 ×3 bullet). Confirmation, not new doctrine.
- **Plan-before-heist + grid-at-creation P3 as proposals** — hot-applied to
  live AGENTS.md on 09-14 by Gru/Silas outside the dream (store already
  carries both); re-folding would duplicate. Only their single-sighting
  nuances (lavish waiver, resize semantics/husk-verification) remain watch
  items.
- **Hold #2 as an AUTO edit** — rejected: it amends model-policy status text
  beyond a gotcha append → reclassified user-ack (P3).
- **"Session filenames ≠ header ids" as its own gotcha** — folded into P1
  (single sighting, inseparable from the incident).
- **Sweep-race as Silas-only hygiene** (he already filed the root cause
  locally) — rejected: the failure shape spans any closer-out and pairs with
  the 08-27 class; a store bullet is the durable home (P2).
- **Row re-opening (done→working/dispatched) as standalone** — folded into
  P6's same-ROW extension sentence (it is the mechanic, not a separate
  pattern).
- **sheep-shards' three dream-process one-liners as proposals** — they are
  dream-procedure lessons already applied by this pass directly (grep-verify,
  merged-base census, events-ts intake); no store surface needs them.

## Store-diff summary (diff-ready)

`store/AGENTS.md` vs live `/Users/moses/code/AGENTS.md`: +82 lines, 7 edits —
P1 PI_MODEL lens addendum (Model dispatch ops), P3 HOLD #2 paragraph
(interlude block; USER-ACK), P5 template-rot addendum (briefing rot), P6
same-ROW extension addendum (reversal gotcha), P7 CALL≠RESULT addendum
(Perkins bytes-not-claims), P4 both-ways provenance addendum (role:user
gotcha), P2 close-out sweep-race bullet (Pane forensics), P8 youtube-channel
worktree-ruling bullet (Dispatch & handover). `store/minion-field-notes.md`:
UNCHANGED — the window produced no new field-note shards to promote (see
watch item 4).
