# Sheep shard — ledger (dream-2026-09-07)

Read: 321 events / 42 jobs (full sqlite event stream 2026-09-05T00:09:06Z →
2026-09-07T00:15Z) / ledger show on: packet-plumber-3d-alive-planet,
p-p-3d-alive-planet-perkins-r4, p-p-3d-alive-planet-perkins-r6,
p-p-3d-alive-planet-fold, p-p-3d-router-family, p-p-3d-l1-arpanet,
p-p-3d-l1-look-parity, p-p-3d-l1-refine-1,
righttenantry-agents-tf-in-ci, rta-wif-durable, rta-prod-scale-to-zero.

## Candidate patterns

### 1. Quota-flip sensor joins the stale-echo family; every echo gets a same-status ALREADY-ACTED note with the sha verbatim (7 sightings: tf-in-ci + router-family 09-05, alive-planet ×4 + its perkins-r6 09-06)
- Quote/evidence: righttenantry-agents-tf-in-ci 2026-09-05T18:18:28Z — "sensor
  'dispatch r4 on eaabda7' echo = STALE — r3 reviewed EXACTLY
  sha=eaabda76dda426723a1f94a64e10ac25aa4066b7 and posted APPROVED (5122422939);
  loop terminal on approval, no r4 owed". packet-plumber-3d-alive-planet
  2026-09-06T15:49:02Z — "Quota flip 15:47Z (k3 5h-cap DOWN) = ALREADY-ACTED
  echo: detected at ~15:10Z when r4 attempt-1 died on this exact 403; glm-5.3
  probed UP + r4 retried…". Also: tf-in-ci 15:50:31Z (tick raced the r2
  pre-add), router-family 02:02:51Z ('dispatch r2' = note-only), alive-planet
  14:37:34Z (sensor fired in the ~1min window between the minion's push and
  the row update), 16:47:32Z (k3-UP flip = confirmation of already-executed
  routing), alive-planet-perkins-r6 18:48:19Z (APPROVED-review + round-debris
  lines = ALREADY-ACTED).
- Proposed lesson: the quota-probe flip injector now re-fires events the round
  rows already acted on — classify quota flips exactly like review-sensor
  echoes: answer with a same-status note quoting the sha + the action already
  taken, never a second action.

### 2. HELD round row on a CONFLICTING/rebasing PR: declare the pre-rebase sha DEAD verbatim + a named release trigger; release re-resolves the fresh head (3 sightings: router-family-perkins-r1 + alive-planet-perkins-r1 09-05, wif-durable-perkins-r1 09-06)
- Quote/evidence: packet-plumber-3d-router-family-perkins-r1
  2026-09-05T01:33:48Z — "HELD - review target UNSTABLE (PR #7 CONFLICTING:
  branched pre-#5; rebase relayed to the open minion, force-push incoming).
  Sensor-dedup row. sha=43516f3… is DEAD (pre-rebase head - never review it).
  RELEASE TRIGGER: rebase lands (PR mergeable)…"; released 01:45:39Z at fresh
  859e2e1 → APPROVED. alive-planet-perkins-r1 2026-09-05T23:04:14Z — same
  shape (fa21cf3 DEAD → released d7edd8a). righttenantry-agents-wif-durable-
  perkins-r1 2026-09-06T11:53:18Z — "r1 PRE-ADD HELD… HOLD REASON: head MOVING
  + CI RED"; released 11:57:23Z when "head settled… remaining CI red =
  user-gated live-role update, diagnosed not instability".
- Proposed lesson: the unstable-target hold now has a rebase-conflict flavor —
  pre-create the round row HELD with the dead sha named verbatim ("never
  review it") + the release trigger; release = resolve the post-rebase head,
  update the note, launch.

### 3. Chained paneless holds release at the predecessor's merge close-out; amendments and Perkins-warning folds RIDE the held row and are re-read at release (3 sightings: model-single-source + tf-in-ci 09-05, l1-look-parity 09-06)
- Quote/evidence: righttenantry-agents-model-single-source 2026-09-05T09:32:41Z
  — "PANELESS HELD ROW. RELEASE GATE: dispatch only after
  righttenantry-agents-model-38-sweep MERGES (same files…)"; 10:19:22Z —
  "AMENDMENT (user ruling via Gru, 10:1xZ — BEFORE release): FOLD the CI path
  fix"; released 12:24:00Z "fresh develop head 6e82006 resolved". tf-in-ci
  13:33:30Z — "FOLD (Gru — Perkins W-headline on #181): README runbook scope
  +1… lands when this row releases". packet-plumber-3d-l1-look-parity
  2026-09-06T19:24:53Z — "briefing rewritten to v2 — LEAN SWAP… Held state +
  release trigger UNCHANGED… RE-READ the v2 briefing at release".
- Proposed lesson: held rows are the amendment surface while they wait — fold
  user rulings + Perkins-warning scope into the staged briefing during the
  hold, and make the release step re-read the amended briefing and re-resolve
  the fresh head (the 3-link RTA chain 38-sweep → single-source → tf-in-ci ran
  end-to-end on this in one day).

### 4. k3 has a THIRD cap flavor — mid-day 5-hour wall; mid-round cap death = same-row RETRY (attempt N, not rN+1) on glm-5.3, partials preserved, VISION CAVEAT (2 sightings: alive-planet-perkins-r4 + r6, same parent, 09-06 — trend candidate)
- Quote/evidence: packet-plumber-3d-alive-planet-perkins-r4 2026-09-06T15:10:49Z
  — "RETRY (same-row, attempt 2) on zai-coding-cn/glm-5.3: attempt 1 died
  mid-wave on the k3 5-HOUR USAGE CAP 403 (account wall, ~14:43Z-15:47Z — not
  a burst; k3 probe DOWN confirmed)… Partials preserved at r4-attempt1-k3-403/.
  … Same sha 2cf9ded, same row (not r5)". perkins-r6 18:03:51Z — same shape
  ("2nd mid-round cap today"). r5 dispatch 16:08:48Z — "k3 RETURNED (5h cap
  freed ~20min early — 3x strict-OK probes)".
- Proposed lesson: the k3 cap taxonomy is now weekly-7d (09-04) / 5h-wall /
  1302-burst — recover respectively by waiting days, same-row retry on
  glm-5.3 (attempt-N, partials at <round>-attempt1-k3-403/, VISION CAVEAT),
  one continue; the 5h window frees EARLY vs the stated reset — the probe,
  never the clock, gates the resume.

### 5. 1302 bursts under glm-only load strike AT WAVE-SPAWN: the main dies on timeouts while lenses survive; one continue per burst, pi auto-retry absorbs a share; budget ~1 burst per spawn (6 sightings: router-family-r1, l1-arpanet-r1, scene-refactor-r1, tf-in-ci-r1/r2, model-single-source-r1 09-05; alive-planet-r2 + r6 ×3 09-06)
- Quote/evidence: packet-plumber-3d-alive-planet-perkins-r6 2026-09-06T18:32:34Z
  — "SECOND 1302 burst killed the main mid-wave-B-spawn (3 lenses dispatched
  before death)… ONE continue -> main working… The 1302 cadence under glm-only
  load is ~every-spawn now (3 bursts absorbed this round)". alive-planet-
  perkins-r2 11:53:18Z — "1302-burst + connection wave killed the wave at
  spawn — main dead on timeouts post-spawn, 6 lenses dead mid-turn… Recovery:
  ONE continue per pane (6 lenses + main) = all 7 working". righttenantry-
  agents-model-single-source-perkins-r1 2026-09-05T13:22:23Z — "working->done
  blip = TRANSIENT… self-recovered via pi auto-retry before any continue was
  spent".
- Proposed lesson: during glm-only windows treat 1302 as a per-spawn tax on
  the round MAIN (lenses usually live): classify by transcript before spending
  a continue (auto-retry absorbs some), then exactly one continue per dead
  pane — never a hold, never a re-dispatch.

### 6. The 'claimed-but-didn't-land' class is a first-class fix-audit hunt: commit messages/docs claim pins that grep + mutation disprove; extraction refactors can silently invert a constant with the suite green (4 sightings: alive-planet 09-05/06, tf-in-ci 09-05, l1-refine-1 + wif-durable 09-06)
- Quote/evidence: packet-plumber-3d-alive-planet-perkins-r4 2026-09-06T15:42:54Z
  — "river-width pin STILL absent (4th round — commit claims a vertex-to-path
  measurement that grep shows doesn't exist; revert still passes GREEN)";
  the r4 briefing leg reads "hunt the 'claimed-but-didn't-land' class".
  righttenantry-agents-tf-in-ci-perkins-r2 2026-09-05T16:13:31Z — "header +
  tripwire pin both false — gcloud-verified". p-p-3d-l1-refine-1
  2026-09-06T23:47:50Z — "1 NEW delta blocker: ISLET_TOP_FRAC extraction
  INVERTED 0.38->0.62 (planet.gd:207)… No islet-geometry pin = suite stayed
  green". wif-durable shipped "mutation-hardened" pins up-front (4 mutations
  all RED).
- Proposed lesson: fix-audit briefings name the false-claims class as an
  explicit leg — every fix claim gets grep-verified against the tree AND
  mutation-proven (revert → RED); a constant extraction is a delta-blocker
  candidate until a value pin exists, because the suite cannot see an
  inversion.

### 7. The user play/look gate IS the aesthetic verdict; Perkins rounds carry VISION CAVEAT mechanical-only look checks, and a play-session-in-progress HOLDS the worktree + pane from sweeping (4 sightings: l1-arpanet + art-integration 09-05, l1-look-parity + alive-planet 09-06)
- Quote/evidence: packet-plumber-3d-l1-look-parity 2026-09-06T19:59:22Z —
  "USER PLAY SESSION IN PROGRESS (Gru FYI 20:0xZ)… HOLD: do NOT sweep this
  worktree or close pane pHD until the user reports done looking… Perkins r1
  (pHE) reviews the swap correctness in parallel — unaffected". l1-look-
  parity-perkins-r1 19:58:56Z — "VISION CAVEAT — mechanical-only look checks;
  the USER is the look verdict". packet-plumber-3d-alive-planet 19:03:42Z —
  "The user's look-gate verdict: merge = the aesthetic ruling satisfied".
  l1-arpanet 2026-09-05T18:12:59Z — row HELD blocked on "THE L1 PLAY GATE…
  the user's play session rules the level AND the E2 engine together".
- Proposed lesson: on look lanes write the play-session HOLD note onto the row
  the moment the user starts looking (no sweeps, no pane closes until they
  report), and let the Perkins round run mechanical-only in parallel — the
  merge/play click is the aesthetic verdict, never a lens.

### 8. Fresh-checkout reproduction is the arbiter of breakage claims — a stale .godot cache manufactured false 'deletion breaks imports' evidence; the double-reversal closed with an honest retraction (1 sighting — strong watch-item candidate)
- Quote/evidence: packet-plumber-3d-l1-refine-1 2026-09-06T22:12:22Z — "Rider
  2 (texture purge) BLOCKED-BY-EVIDENCE: the 11 orphans are LIVE glTF external
  texture deps (deleting broke 4 glb imports…)"; Perkins r1 22:42:49Z — "THE
  TEXTURE-PURGE REVERSAL DISPROVEN (all 7 glbs embed images, zero external
  URIs, fresh import w/ 11 deleted exits 0 — r6 was right; SHIP the purge)";
  minion 23:19:16Z — "PURGE SHIPPED — r1 reversal retracted: my breakage
  evidence was a stale .godot cache artifact; fresh-checkout reproduction
  confirms Perkins".
- Proposed lesson: never claim "deleting X breaks Y" from a dirty local tree —
  editor caches (.godot) fabricate breakage evidence; reproduce on a FRESH
  checkout before filing a blockage, and treat a verified retraction as a
  first-class deliverable, not a loss.

### 9. Review-anchor discipline held end-to-end: self-reports truncate the anchor, the close-out VERDICT capture fetches the full id (2 sightings: router-family-perkins-r1 + scene-refactor-perkins-r1, both 09-05)
- Quote/evidence: router-family-perkins-r1 self-report 2026-09-05T01:58:19Z —
  "review=…/pull/7#pullrequestreview" (anchor truncated); close-out capture
  02:02:51Z carries "Review: …/pull/7#pullrequestreview-5119304322".
  scene-refactor-perkins-r1 self-report 10:41:35Z truncated
  ("#pullrequestreview-"); close-out 10:44:01Z carries
  "#pullrequestreview-5120899982".
- Proposed lesson: the 09-02 fetch-the-anchor doctrine is operating as
  written — keep reading review URLs off the close-out capture note, never
  the round's self-report (which truncates the anchor).

## One-off / job-scoped lessons (watch-item candidates)

- **Priority inversion: park-by-sweep + un-park-by-fold** — alive-planet-fold
  2026-09-06T19:27:32Z "PARKED by USER RULING (priority inversion)… pHC was
  mid-work (no PR open) -> pane closed + worktree/branch swept (the fold is
  small + cheap to redo — nothing committed lost)"; 20:22:15Z "UN-PARKED by
  FOLDING… scope FOLDED into packet-plumber-3d-l1-refine-1 as riders ('one
  heist, one round')… Do NOT re-dispatch this job". Parking a mid-work job is
  safe when nothing is committed; the successor's dispatch carries the parked
  scope as named riders.
- **Missed close-out on a row held in-review pending a second PR's merge** —
  righttenantry-agents-prod-scale-to-zero 2026-09-06T10:17:21Z: #176 + #178
  merged 09-04, the row "held in-review pending the #178 merge and never got
  its close-out" — caught ~2 days late at a board sweep. Rows whose note says
  "HOLDS until X merges" need reconciliation at every board sweep; the PR
  watcher alone misses the dependent merge.
- **Early-turn abort at boot (stopReason=aborted)** — alive-planet-fold
  2026-09-06T19:04:59Z: "EARLY-TURN ABORT — mid-setup… a tool read aborted…
  ONE continue -> working. Not a stall, not a clarify halt." A boot-time
  working->idle with 'Operation aborted' = one continue, nothing more.
- **Self-proving acceptance for CI-mechanics fixes** — rta-ci-concurrency-fix
  2026-09-06T18:04:58Z: minion "discovered tf-plan has a deployment/** paths
  filter (would skip the fix PR)" and added a docs-only trigger; 20:02:28Z:
  "both workflows ran concurrently on the fix PR itself, both green, PR
  Checks NOT cancelled". A CI fix PR is its own acceptance test — but check
  path filters don't exempt the fix PR from the workflow it fixes.
- **Mislabeled fold commit subject** — alive-planet 2026-09-06T16:06:57Z:
  "commit subject says 'Perkins r3 warnings' + terminal says 'r4
  auto-triggers' = MISLABELED; this fold actually targets the r4 VERDICT" —
  the classify note caught + corrected the record. Fold commits should name
  the verdict round they target.
- **Full pane death with lane state on disk = zero-loss** — h3-local-
  production-queue 2026-09-06T10:16:24Z: "the pane DIED COMPLETELY (no herdr
  registration, zero node processes… not just a dead pi). Lane state fully
  preserved on disk: …/local/{LOG.md,watch.txt,graph_noaudio.json}". The
  marker-file lane contract (08-30/31) survives even a whole-pane death.
- **Bootstrap chicken-egg for read-only CI terraform plans** — rta-wif-durable
  2026-09-06 (11:28→12:04Z, 4 events): plan runs pre-apply, so the grant fix
  can't land itself — "the grants land via apply but the plan runs pre-apply
  (bootstrap chicken-egg class)"; resolved by user-hand `gcloud iam roles
  update` ×2 + layer-by-layer 403 triage, "minimal-only (a push = new sha =
  r1 sweep + fresh round per doctrine)". Expect N sequential 403 layers on a
  zero-write planner bootstrap; each push re-sweeps the in-flight round, so
  batch fixes per push.
- **Lavish-as-review for docs PRs is now routine** — gdd-amend-levels /
  -cumulative / -era-planets / -alive-planet (all 09-05): pr_review=0 with a
  multi-round lavish ruling gate ("lavish gate HELD (5 user rounds R1-R5…)")
  then docs-only direct PR per exemption. Confirmation, not new doctrine.

## Coverage note

Full 321-event stream read (sqlite, notes to 300 chars; two close-out notes
re-read at 900 for the anchor check). `ledger show` run on the 11 rows listed
in the header — the heaviest loop (alive-planet + its r4/r6), the RTA chain
(tf-in-ci, wif-durable), the hold/release pair (l1-look-parity,
alive-planet-fold), the unstable-target hold (router-family), the play-gate
row (l1-arpanet), the refine loop (l1-refine-1), and the missed close-out
(prod-scale-to-zero). Remaining 31 jobs (all perkins round rows r1-r3/r5,
gdd-amend ×4, model-38-sweep ± r1, model-single-source ± r1, ci-concurrency-
fix, h3-local-production-queue, e2-flow-qos, art-integration, scene-refactor
± r1, l1-topology-font ± r1, l1-arpanet-perkins-r1, l1-look-parity-perkins-r1,
l1-refine-1-perkins-r1/r2, tf-in-ci-perkins-r1/r2/r3, wif-durable-perkins-r1,
dream-2026-09-04/-07) were covered from the event stream alone — their events
were complete enough (self-report + close-out capture pairs) that no extra
row detail was needed. One sqlite lock retry needed mid-read (watcher write);
no data lost.
