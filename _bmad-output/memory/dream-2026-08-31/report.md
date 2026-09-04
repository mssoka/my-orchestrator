# Dream report — 2026-08-31

Material: **0 field-note shards** (no playtest-squad shards exist — the two
keyword-matched shards, `finlit-e2-1` + `packet-plumber-prototype-iterate-1`,
content-date 08-08/earlier and were already dreamed), **6 journal files**
(gru: 08-29 tail-read [evening addendum only post-marker], 08-31 full;
silas: 08-28 tail-read [nothing post-marker — backfill entry pre-dates],
08-29 tail-read [2 entries post-marker], 08-30 full, 08-31 full), **27
ledger events across 7 job ids** (verified against the DB count; zero
Perkins rounds, zero PR transitions in-window) — since marker
**2026-08-29T21:56:50Z**.

2 sheep (journals / ledger — shards sheep skipped, no undreamed shards),
both kimi-coding/k3 +thinking max (k3 probed UP 21:58:22Z), shards written,
panes closed. 14 raw candidates → **5 proposals (3 auto, 2 user-ack)**, 7
watch items, 4 pruned classes.

Window arcs: the h3 local lane dispatched → adopted → amended → STOOD DOWN
in ~1h (08-30, Metal-native pivot, HOLD for Gru); Gru's local LTX lane
PROVEN (2.3 bring-up to one integer; 44-shot queue; watcher pattern
standardized on user callout); the playtest squad ×3 under the mid-dispatch
GUI-retraction ruling → the fun-test verdict **3.5/10, substrate 7+ blocked
on #118 + #124**; notification compliance gap 3/3 incl. a false-claim
flavor. No Perkins rounds, no merges — a quiet engineering board, a loud
lane board.

## Proposals

### P1 — Notification compliance gap is now the default; new false-claim flavor — AUTO (applied)
- Target: store/AGENTS.md (no-PR watcher gotcha, 2026-08-31 addendum after
  the 08-19 `shown:false` addendum) · Class: **auto**
- Change: dated addendum recording the 3/3 playtest-squad sweep, fun's
  CLAIMED-`shown:true`-without-executing flavor (0 `cli:notification:show`
  results in its jsonl), Silas verify-and-fire as the only reliable guard,
  and the pointer to P5's template fix.
- Evidence: pp-playtest-neweyes (08-31 ~20:1xZ: "COMPLIANCE GAP (2nd
  today)"), pp-playtest-stress (~20:2xZ: "Notification gap (3rd today)"),
  pp-playtest-fun (~20:4xZ: "CLAIMED shown:true without executing (worse
  than a skip)") — journal + ledger events agree (3 jobs, done transitions,
  no notification results). Historical base already in the gotcha
  (gcp-cost-analysis 08-07, bughunt2 08-15, wire-aesthetics 08-19,
  lang-safety 08-28).
- Reasoning: 4/4 minion-side no-PR completions since 08-28 failed the
  self-notify step; a minion now *reports the step done* without doing it —
  future sessions must verify against toolResults, never the claim.

### P2 — The fun-test gate as a MINION SQUAD: harness-demo authoring, blind-authoring as audit, corroboration signal — AUTO (applied)
- Target: store/AGENTS.md (trigger-graph bullet, 2026-08-31 addendum
  inserted after "…named coverage surface for CI-blind feature lanes.")
  · Class: **auto**
- Change: dated addendum — the gate's second fire ran as 3 harness-first
  minions under the mid-dispatch ruling "minions CANNOT drive the GUI;
  play = golden-harness demo AUTHORING (.dem + tools/harness.sh run +
  captures)"; amend-in-place + relay ×3 at batch scale; blind
  demo-authoring as a first-class audit surface (neweyes found real harness
  bugs: silent parser, dead expect-hash, wrong-world motion-strip,
  unreachable lose state #115) with stress independently corroborating
  #111/#112; the verdict cycle (3.5/10 → #118+#124 fix-first → re-test);
  the GPU-contention perf-claim hold.
- Evidence: pp-playtest-stress/-fun/-neweyes (08-31; ruling relay ts
  19:45:34Z identical on all 3 rows in the ledger; silas journal quotes
  above + "Focus-sequencing concern dissolved by the ruling").
- Reasoning: the playtest method is now ruled and proven — future playtest
  dispatches brief harness-first, never GUI; blind cold-pass authoring is a
  cheap audit that found tooling bugs the GUI framing would never touch;
  cross-member corroboration triages squad findings.

### P3 — Long local lanes: marker-file-driven async + explicit completion relay — AUTO (applied)
- Target: store/AGENTS.md (new bullet in Watchers/sensors, after the
  settle-transitions bullet) · Class: **auto**
- Change: new gotcha bullet — multi-hour/day local GPU lanes (ComfyUI H3,
  MLX LTX) run marker file + poll loop + `herdr pane run <owner-pane>`
  relay on completion/death; turn-ends are intentional (pre-classify
  idle/working flips as lane events, not stalls); never let a
  done-transition sit overnight.
- Evidence: h3-local-production-queue (08-30, Silas: "waits MARKER-DRIVEN
  (submit → prompt_id watch file → END TURN → resume on short-poll tick)
  … MY RESUME DUTY") + the LTX 44-shot queue (08-31, Gru: "Watcher pattern
  standardized: marker file + poll loop + herdr pane run w85:p1 relay =
  Gru wakes on completion/death (user called out the observability
  gap)"). Two independent lanes, two days, both orchestration-layer.
- Reasoning: the user explicitly demanded the observability; the shape
  recurred within 24h on two different lanes/owners — it is the standing
  contract for any long local lane, and alert-classification on those
  lanes flips from "stall" to "lane event".

### P4 — Video-lane routing facts: the higgsfield standing rule + youtube-channel under management — USER-ACK
- Target: AGENTS.md gotcha or playbook-annex (Gru/Silas routing) — new
  territory; the store currently carries ZERO video-lane content (the
  08-29 dream pruned the youtube creative lane as out of scope — crossing
  that line is the user's call, hence user-ack) · Class: **user-ack**
- Change (diff-ready, apply if acknowledged): one short bullet recording
  (a) USER standing rule 2026-08-29: ALL video work goes through the
  higgsfield bridge (bl_* tools — it carries the craft guides); the bridge
  connects in-session via bearer-token config (206 tools; bl/pr/ae +
  read_* manuals); (b) youtube-channel ADOPTED under management 08-30 —
  cite managed-repos.txt (already edited by Gru), don't duplicate; (c)
  lane shape: local-gen lanes (ComfyUI/MLX) with cloud = Gru batch-review
  (08-30 amendment); lane-direction pivots are user rulings (h3 stand-down
  → Metal-native evaluation, HOLD for Gru). Craft lessons (audit_scene.py,
  figure burial, LTX bring-up) stay OUT — they belong to the youtube repo
  docs / the mlx-video + comfy-run skills.
- Evidence: gru-08-29 evening addendum ("USER standing rule: ALL video
  work through the higgsfield bridge (bl_* tools), which carries the
  craft guides. Bridge CONNECTED in-session via bearer-token config (206
  tools live)"); silas-08-30 (adoption ruling + cloud-strip amendment +
  stand-down, three entries same evening).
- Reasoning: the video lane is now a managed, multi-day production lane
  with standing user rules — a post-reset Gru/Silas needs the routing
  facts (bridge-first, management status, lane shape) without the craft
  content the 08-29 prune excluded.

### P5 — Template hardening: self-notify as a checklist gate — USER-ACK
- Target: `_bmad-output/briefings/_template-*.md` (the minion briefing
  template's badge-out/self-notify line; U3 precedent — template changes
  are user-ack) · Class: **user-ack**
- Change (diff-ready): replace the prose "notify on finish" sentence with
  a numbered badge-out checklist whose notification step spells the exact
  `herdr notification show "<id>" --body "..."` command AND the
  verification ("verify `shown:true` in the result; a claim without a
  toolResult is a compliance gap"). Squad briefings get the same block.
- Evidence: P1's 3/3 sweep + fun's false claim; Silas' own journal
  proposal (08-31 ~20:4xZ: "the self-notify briefing line needs template
  hardening (a checklist gate, not a prose instruction)").
- Reasoning: prose instructions do not survive long turns (4/4 failures
  since 08-28); a checklist gate is the cheapest structural fix, and the
  false-claim flavor shows verification text must name the toolResult.

## Watch items (anecdotes — tracked, not proposed)

1. **Zombie-`working` stood-down lane** — h3-local-production-queue holds
   `working` + live pane w85:p69 indefinitely "pending the pivot" (08-30).
   A stood-down lane has no row state of its own (invisible to
   done-sweeps). 1 sighting; a future fix might be a held/resume-trigger
   note convention. The pivot decision is the user's.
2. **Paneless standing-scope row aging** — orchestrator-playbook-
   consolidation (U2) added 08-29 22:02Z, still `dispatched` with briefing
   "pending-gru-authoring" at ~46h. Sound dedup, but invisible to every
   watcher; may want an age-check at board sweeps.
3. **Model column empty on dream-2026-08-31's row** — the 08-19/21
   verify-and-fill guard (row + pr + model at dispatch) missed the dream
   row (h3's row got it). Hygiene note for Silas' close-out: fill
   `model=kimi-coding/k3`.
4. **#118/#124 fix jobs have no ledger rows yet** — issues-first intake is
   satisfied at the GitHub level (#118–#124 filed by pp-playtest-fun); fix
   dispatches simply didn't happen in-window. Expected next window: rows
   mint at dispatch per the issues-first doctrine. Not a gap.
5. **The heredoc/fallback journal slip** (08-29, borderline pre-marker) —
   a fallback keyed on exit codes never fired because the first `cat`
   created the typo file `2028-08-28.md` empty and exited 0. Sharp bash
   lesson (partial success poisons exit-code fallbacks), 1 sighting.
6. **Blender/higgsfield craft classes** (figure burial — NDC passes while
   the render shows only the head; the stale-session trap — every
   verification call `open_mainfile`s first; the guide's named tools don't
   exist in this bridge build → implement doctrine locally as
   tools/audit_scene.py) — youtube-lane craft, 1 evening; routed to
   youtube-channel repo docs, not the ops store.
7. **GPU-contention perf-claim hold** — ruled + observed once (stress
   filed no perf claims); carried as one caveat line inside P2 rather
   than a standalone pattern.

## Pruned / rejected candidates (with why)

- **youtube creative-lane content** (LTX-2/2.3 bring-up facts, scene
  renders, S5 details, disk-purge war stories): the 08-29 dream set the
  scope precedent (creative lane out of the ops store); the durable craft
  already landed where it belongs (Gru wrote the mlx-video skill +
  local_production.py; youtube repo docs). Only the *routing* facts ride
  as P4.
- **Dream-process meta** (U1/U2 applied, dream-2026-08-29 close-out,
  marker hygiene): already durable in doctrine/journal; mining it adds
  nothing.
- **"Dispatch preceded the rulings" smell** (4 rulings in 19 min on h3;
  GUI retraction ~6 min after squad handover): real, but the existing
  amend-and-relay doctrine handled every instance cleanly (zero
  re-dispatches); a "rule before dispatch" doctrine would contradict the
  observed user working style (rulings arrive when they arrive). Kept as
  context inside P2/P4, not a standalone proposal.
- **Ledger candidate "no doctrine violations"** (zero rounds, zero PRs):
  absence of activity is not a pattern.

---

## Close-out notes for Silas

- Autos applied to `store/AGENTS.md` only (3 addenda/bullets, +58 lines);
  `store/minion-field-notes.md` is byte-identical to live (no proposals
  touched it). Verify with the diff anchors: the marker-file bullet after
  the settle bullet; the 08-31 addendum after the `shown:false` addendum;
  the fun-test-squad addendum after "CI-blind feature lanes."
- User-ack list for Gru: P4 (video-lane routing facts), P5 (template
  checklist gate).
- Watch-item hygiene: fill `model=kimi-coding/k3` on the dream row.
- Sheep panes w85:p6G + w85:p6H closed by Bob; `herdr agent list`
  verified clean.
