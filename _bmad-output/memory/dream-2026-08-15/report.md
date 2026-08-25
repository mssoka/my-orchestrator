# Dream report — 2026-08-15

Material: 3 undreamed field-note shards, 4 journal files (gru 08-14; silas
08-13-post-marker tail, 08-14, 08-15), 60 ledger jobs with activity, since
2026-08-13T16:26:29Z. Sheep: shards / journals / ledger (3, all glm-5.3, all
closed). Verification pass (adversarial) applied to every candidate;
single-sighting items demoted to watch items; already-codified candidates
pruned to recurrence notes. Store diffs: `store/AGENTS.md.diff` (80 added
lines), `store/minion-field-notes.md.diff` (14 added lines) — diff-ready for
Silas to apply.

**08-13 user-ack ledger (all resolved):** U1 cap-override ✓ applied (playbook
'User cap override'); U2 FULL THROTTLE + disjointness ✓ applied (playbook);
U3 pr_review=0 quick-fix scope ✓ applied (Intake step 8 note); U4 follow-up
intake sweep ✓ applied (Intake step 9); U5 template stale lines ✓ fixed
(marker-writer + model line, refreshed again 08-15); U6 lens-loss tolerance —
target file `perkins-pr-review-plan.md` NOT FOUND at the named path (possibly
renamed) — **Silas: verify whether U6 ever landed.**

## Proposals

### P1 — Reasoning tier = glm-5.3 (08-14 user ruling) + model-flip verification traps + no-mid-round flips
- Target: AGENTS.md (provider-incidents gotcha, kimi-retirement block) · Class: auto (applied to store copy)
- Change: 2026-08-14 supersede appended — reasoning tier is
  `zai-coding-cn/glm-5.3` (Gru/Perkins/Bob), v4-pro = interim fallback, flash
  unchanged. Verification doctrine: a "glm-4.7" self-report was model
  hallucination and a "ZAI balance 0" probe was a wrong-endpoint curl —
  verify new models THROUGH pi (env-cleared probe + session jsonl modelId),
  never raw API curls or the reply's self-named id. Model flips apply to NEW
  dispatches only (in-flight rounds complete on their launched model).
- Evidence: gru 08-14 (MODEL POLICY RULING + MODEL VERIFICATION CLOSED); silas
  08-13-tail 13:55Z (wrong-endpoint curl correction); silas 08-15 16:35Z
  (template refreshed); ledger: 9 glm-5.3 rounds 08-14/15 all clean
  (611-r2 = first, 13:33Z 08-14).
- Reasoning: AGENTS.md still routed v4-pro in three places after the playbook
  was updated — an agent reading only the gotchas would misroute the reasoning
  tier; the verification traps nearly killed the flip (false "provider down").

### P2 — Serialize gate is PER-PROVIDER (deepseek parallel override; ZAI/glm-5.3 one-fan-out-at-a-time)
- Target: AGENTS.md (Serialize concurrent Perkins BURSTS gotcha) · Class: auto (applied)
- Change: 08-14 addendum — deepseek carries the user's 08-12 parallel-rounds
  override (two concurrent rounds clean; parallel across DIFFERENT providers
  fine); ZAI/glm-5.3 serializes one fan-out at a time — a 1302 burst hit the
  5th glm-5.3 round of the day (5.7-r2, 20:45Z 08-14; one continue revived);
  ~5 rounds/day cumulative is the observed burst ceiling.
- Evidence: gru 08-14 (parallel deepseek rounds); silas 08-14 14:45Z (queue
  serialize), 19:50Z (coexists-different-providers), 20:45Z (1302 burst).
- Reasoning: the gotcha read as unconditional serialize; with glm-5.3 back on
  reasoning duty the gate needs the per-provider split or Silas either
  over-holds (deepseek) or trips 429s (ZAI).

### P3 — GitHub Actions BILLING block = new incident sibling class (looks CI-red, runner never started)
- Target: AGENTS.md (provider-incidents gotcha, clause (d)) · Class: auto (applied)
- Change: runner-never-started ≠ CI-red: rerun useless, NOT a hold trigger —
  dispatch rounds anyway (Perkins verifies locally at the sha = ground
  truth), ONE escalation to the user, then note-only per PR; retire the
  briefing caveat line once fixed.
- Evidence: ×6 PRs 08-13/14 (#39/#40/#41/#42/#43/#44 — ledger notes
  23:51Z→07:35Z); silas 08-14 14:50Z (billing FIXED, caveat retired via #618
  green checks).
- Reasoning: six wrongful holds were avoided only by Silas re-deriving the
  doctrine per PR; the class will recur on any future billing hiccup and the
  unstable-target hold keys on exactly this confusion.

### P4 — No-PR lifecycle: both watcher-gap flavors now seen + preserve deliverables BEFORE the sweep
- Target: AGENTS.md (no-PR gotcha) · Class: auto (applied)
- Change: (a) bughunt2 08-15 was the SENSOR-gap flavor — the minion DID fire
  `cli:notification:show` ×2 at 00:22Z (verified in its session jsonl by
  Bob) yet the completion sat unseen 8.5h (surfaced via user/Gru relay);
  notification alone is NOT sufficient → reconcile no-PR non-done rows at
  every board sweep. (b) PRESERVE no-PR deliverables (reports, regression
  suites) to `_bmad-output/implementation-artifacts/` BEFORE the worktree
  sweep.
- Evidence: (a) silas 08-15 09:05Z + Bob's jsonl verification; (b) silas
  08-14 21:15Z (local-test lost untracked artifacts), 23:40Z + silas 08-15
  09:05Z (bughunt suite twice-swept, re-created 3rd time, now preserved) —
  ×4 sightings.
- Reasoning: closes the loop on the 08-07 gotcha with the missing flavor
  confirmed and a proven preservation standard; suites are durable assets,
  not scratch.

### P5 — Minions can SELF-CREATE ledger rows (wrong-id phantoms + missing fields)
- Target: AGENTS.md (Ledger section, new bullet) · Class: auto (applied)
- Change: when a watcher re-fires on a merged PR or a job seems untracked,
  check for a minion-created phantom row; reconcile to ONE canonical id.
- Evidence: `refcheck-followup-607` (prefix dropped) ran 19h as a duplicate
  of the canonical row feeding the PR watcher (08-14 13:27Z); 
  `bundle-reprice-pin` self-created with missing fields (08-13 23:09Z). ×2.
- Reasoning: codified id-hygiene covers the ORCHESTRATOR's hand-typing; this
  is a new ACTOR (the minion) creating rows Silas must reconcile.

### P6 — Durable routing lives on ledger rows (QUEUE / BATCHED / RESPAWN-TRIGGER)
- Target: AGENTS.md (Ledger section, new bullet) · Class: auto (applied)
- Change: routing/trigger decisions are written as notes on the OWNING row
  (even done rows) so they survive session restarts and context turnover.
- Evidence: #618-merge respawn trigger fired exactly as written across a
  Silas restart (verification-rerun dispatched 08-14 18:55Z); #621
  BATCHED-to-next-RT-batch ruling (08-15 08:59Z); 5.2 visibility QUEUE note
  (08-15 11:05Z). ×3 + one full trigger→fire cycle.
- Reasoning: release triggers are codified for held Perkins rounds only;
  this window generalized the practice to queued jobs, batched rulings on
  done rows, and respawn triggers — all executed correctly across turnover.

### P7 — Review-URL truncation in self-close events
- Target: AGENTS.md (anchor-ids gotcha) · Class: auto (applied)
- Change: self-close EVENT notes truncate the anchor (`#pullrequestreview-` /
  `-1`); the recovered-as-note verdict at close-out carries the real id —
  never read the URL off the self-close event.
- Evidence: qos-panel 5.8 (00:43:19Z vs recovered 00:43:58Z, id 4942164141);
  readability-assist (00:16:00Z vs 00:20:31Z, id 4932656755). ×2.
- Reasoning: same blast radius as a guessed anchor; one clause covers it.

### P8 — rsync --exclude='_bmad' for RT main-checkout worktree bootstrap
- Target: AGENTS.md (Dispatch & handover, new bullet) · Class: auto (applied)
- Change: `cp -r` cycles on the self-referencing `_bmad` symlink; rsync with
  the exclude is the standard copy.
- Evidence: silas 08-13-tail 18:40Z + 19:20Z ("the self-ref _bmad symlink
  cycle again — rsync --exclude is now the standard copy"). ×2 dispatches.
- Reasoning: recurs on every RT dispatch from the main checkout.

### P9 — Backticks in double-quoted `herdr pane run` payloads are eaten (sibling of the extension-template gotcha)
- Target: AGENTS.md (Extensions backtick gotcha) · Class: auto (applied, flagged borderline)
- Change: single-quote the whole payload or drop backticks — the relay
  arrives with blank code spans otherwise.
- Evidence: silas 08-13-tail 17:15Z (relay slip, blanks in delivered
  message). ⚠️ 1 direct sighting — promoted as a CLASS promotion (the 08-01
  extension-template-literal kill is the same hazard, second surface).
  Verification pass note: rejected for standalone promotion, accepted as a
  one-clause sibling append.
- Reasoning: silent corruption of fix recipes; deterministic bash mechanics.

### P10 — Plain tab moves do NOT mutate pane ids (only workspace moves do)
- Target: AGENTS.md (pane-id gotcha) · Class: auto (applied)
- Change: one-clause contrast clarification — don't over-correct ledger rows
  after a tab move.
- Evidence: silas 08-14-tail 09:30Z (tAX decongestion moved 10 mega-minions,
  zero ledger corrections). ×1 factual clarification of a codified gotcha.
- Reasoning: prevents needless ledger churn from mis-applying the
  workspace-move gotcha.

### P11 — PP visual verification: app-layer UI invisible to goldens; pixel-scan, never vision models
- Target: docs/minion-field-notes.md (rlsw/harness family addendum) · Class: auto (applied)
- Change: zero golden-shift does NOT verify an overlay change; scratch
  replica (ODIN_ROOT shadow + LoadImageFromScreen) + PIL pixel-scan for
  overlap truth.
- Evidence: 5.3-pause-ux shard (08-14) + silas 08-14 20:45Z (chip
  collision-verified via replica + PIL — "vision models misjudge
  coordinates"). ×2.
- Reasoning: generalizes the golden-invisibility trap + a new trust rule for
  visual verification.

### P12 — Canon-amendment craft: cite the ruling source (date + job id)
- Target: docs/minion-field-notes.md (canon-amendment entry, clause (h)) · Class: auto (applied)
- Change: a presentation-only ruling still earns a same-PR canon amendment,
  and the amendment STATES the ruling source so canon/code drift is
  detectable.
- Evidence: 5.3-pause-ux shard (08-14). ⚠️ 1 sighting — facet completion of
  the codified (a)-(g) canon-amendment craft entry.
- Reasoning: completes an existing promoted pattern; cheap.

## User-ack escalations (Silas → Gru → user)

### U1 — Playbook stale model line (~line 221-223, 'Durable state' intro)
"Gru / Perkins / Bob launches name `deepseek/deepseek-v4-pro` (flash as the
interim)" contradicts the 08-14 glm-5.3 ruling 35 lines above it — the
second location the flip missed (the rot pattern). One-line fix; trivial but
playbook edits are user-ack class. **Recommend Silas apply on ack.**

### U2 — Interactive-pane settle-echo firehose (watcher feature request, low priority)
refcheck-local-test fired ~15 note-only settle echoes 08-14 (every user turn
in an interactive pane wakes the watcher). Classification-per-echo is correct
but pure tax. Candidate: watcher-side suppression flag for
interactive-session panes. Needs user/Silas decision (tooling change) — not
urgent.

## Watch items (anecdotes — tracked, not proposed)

- **Merge-hunk audit round flavor (×1, #49 pause-ux 08-14):** same-file
  base-merge moved an APPROVED head → r2 briefed as a scoped hunk audit,
  then moot-swept on merge. Completes the head-move taxonomy (skip-row for
  no-op base-sync is codified; this is the changed-diff branch). Promote on
  2nd sighting.
- **Serialize-hold FALLBACK TIMERS (×1, 08-14 21:15Z):** hold keyed on an
  imminent event with a 45-min fallback deadline — prevents queue deadlock
  when the event slips. Promote on recurrence.
- **Restart-orphan staged rows (×1, 5.3-r1 08-14):** a `dispatched` row with
  no pane/briefing after a Silas restart mid-dispatch — serialize-hold
  absorbed it. Named failure shape; promote on recurrence.
- **ECMP two-pass min-cost collection invariant (×1, routing-bandwidth-cost
  shard):** relaxation value and membership test must use the SAME value,
  two-pass order. PP-specific; watch.
- **HUD state-dependent occupancy (×1, 5.3-pause-ux shard):** placement that
  fits idle collides in selection/crisis states. Watch.
- **Single-field fan-out mirror sync (×1, ctr-metadata-619 shard):** one SEO
  field feeds title/H1/JSON-LD/og — sync every mirror. RT-specific; watch.
- **glm-5.3 1308 5h-wall: untested on 5.3** (1302 burst seen; the 1308 wall
  from glm-5.2 history not yet) — first 1308 on 5.3 confirms the taxonomy
  carries over.
- **Silas id slips ×2 more (08-15: tC5→tC4, p1P0→p1P8)** — both self-caught
  via pane get; known gotcha, recurrence only. The FIX quote is already in
  the gotcha verbatim ("capture pane/tab to vars... never re-type").
- **PP design tenet** ("if players need a manual, the design failed") —
  ledger-noted on the 5.2 row + Gru journal for the next canon amendment
  window; no memory-store action needed.

## Pruned / rejected candidates (with why)

- **Full-throttle chain doctrine / disjointness gate / briefing-at-release**
  (journals C15) — already codified (08-13 U2, playbook 'FULL THROTTLE');
  this window's ~10 uses are clean recurrence, not new doctrine.
- **Cap-override + verify-don't-reopen** (journals C17) — codified (08-13
  U1); #36 r4 is recurrence.
- **pr_review=0 quick-fix scope** (journals C16) — codified (08-13 U3);
  ctr-619 is a clean instance.
- **Skip-row for no-op head moves** (journals C10 / ledger C7) — codified
  ('Round-budget ops'); 5.5-demolish-input is a clean instance.
- **Perkins self-close norm** — codified; 11/11 rounds self-closed this
  window, zero verdict losses (healthy).
- **pr_review column blindness class** — did NOT recur (all 23 code-review
  jobs carried the column = 1); sweep fallback unexercised.
- **sheep-journals C20 helper-tab decongestion practice** — folded into
  P10's evidence; the practice itself (split interactive fleets into helper
  tabs) left as watch-level convention, not doctrine.
- **sheep-shards C1 (ECMP) / C3 (HUD) / C5 (mirrors)** — single sightings,
  demoted to watch items above.
