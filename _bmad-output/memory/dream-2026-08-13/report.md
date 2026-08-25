# Dream report — 2026-08-13

Material: 18 undreamed field-note shards, 4 journal files (gru 08-12; silas
08-11-post-marker, 08-12, 08-13), 58 ledger jobs with activity, since
2026-08-11T16:06:54Z. Sheep: shards / journals / ledger (3, all closed).
Verification pass (adversarial) applied to every candidate; single-sighting
items demoted to watch items; already-codified candidates pruned.

## Proposals

### P1 — Provider incidents: 08-13 addendum (firewall class + 429 taxonomy + dual-down toolkit)
- Target: AGENTS.md (provider-incidents gotcha) · Class: auto
- Change: append three clauses to the provider-incidents gotcha:
  (a) 429 error CODES matter — 1302 burst (one continue revives) vs 1308
  5-hour hard cap (account-wide wall, continue = waste, self-heals as
  panes idle); (b) dual-provider-down → HOLD regime (no new dispatches,
  minimum-effort watcher ops, light close-outs) + always-live spares
  (deepseek/openrouter) + the pi probe one-liner + auth.json field is
  `key`; (c) NEW CLASS: recurring "Connection error / Retry failed after
  3 attempts" on deepseek = CHECK NETWORK with the user before provider
  blame (2026-08-13: office firewall, user-confirmed root cause); one
  continue per pane clears each wave meanwhile.
- Evidence: pp-3.1 08-12 00:27Z (1308 "已达到 5 小时的使用上限" — HARD
  ACCOUNT-WIDE WALL — continue re-429s); rc3-6-r1 08-11 20:47Z (1302 burst,
  9+ concurrent glm calls); silas 08-13 13:05Z/13:20Z ("the office
  firewall blocking deepseek API calls, not a provider episode" — 2 waves,
  2 panes); gru 08-12 ("deepseek + openrouter are always-live spares").
- Reasoning: the active provider is deepseek now — the firewall class is
  the live recurring failure; 429-code triage generalizes to any provider.

### P2 — pr_review gotcha: manual dispatch MASKS a dead sensor + proactive sweep proven
- Target: AGENTS.md (pr_review gotcha) · Class: auto
- Change: append: manual/held dispatch is what MASKED the ~11h outage
  (everything ran manually, so the dead sensor was invisible); the
  ratified sweep rule executed cold on 08-13 (rc4-4 #609 r1 dispatched
  proactively at 13:50Z — head stable, no round row) — the fallback is
  proven, keep sweeping at every completion.
- Evidence: silas 08-12 23:5xZ ("Everything since was manual/held
  dispatch, which masked the outage"); silas 08-13 13:50Z ("PROACTIVE r1
  dispatch (sweep rule — head 1a3839c stable, no round row)").
- Reasoning: closes the loop on the 08-12 gotcha — the masking mechanism
  and the first proof the fallback works standalone.

### P3 — Serialize-hold gotcha: release-trigger taxonomy + held-row sha hygiene
- Target: AGENTS.md (serialize-hold gotcha) · Class: auto
- Change: 08-13 addendum: release triggers now span three kinds — (a)
  in-flight round's close-out; (b) close-out + CI green; (c) verdict-gate
  OPEN for a held JOB. Held-row hygiene at release: RE-VERIFY the head
  (refresh the row sha when the head moved during the hold — a980194 →
  abe578b after a rebase), fresh sha at release, and rebase a dirty base
  via parked-pane relaunch + relay.
- Evidence: 3.1-r2 08-12 09:22Z (sha refreshed a980194→abe578b, "release
  on #604 r1 close-out; re-verify head at release"); 3.2 08-12 11:40Z
  ("RELEASED (verdict gate OPEN — #30 r1 APPROVED)… fresh sha at
  release"); 3.1 08-12 09:15Z (#28 DIRTY base → parked-pane relaunch +
  rebase relay); rc4-4 08-13 10:52Z + A 13:35Z (fresh fetch/rebase at
  release). ×6 sightings.
- Reasoning: held rows went through three different release shapes this
  window; the re-verify-at-release step is what prevented stale-sha
  dispatches.

### P4 — pr-field NULL self-report gap: 3 fresh sightings (the RTA-crew pattern persists)
- Target: AGENTS.md (ledger `pr` gotcha) · Class: auto
- Change: extend the 08-11 addendum: 3 more sightings 08-12/13 (3.2
  lane-qos, rc1-1 grapheme-fix, rc4-4 #609 — Silas: "SELF-REPORT GAP
  again: pr field NULL on in-review (the RTA-crew pattern)"). Silas
  verify-and-set on every in-review transition remains the only reliable
  guard; crews still don't self-set.
- Evidence: silas 08-13 13:50Z; ledger 08-12 12:17Z ("pr field was NULL
  (self-report note only) — SET via ledger pr"); ledger 08-13 13:48Z.
- Reasoning: the recurring gap justifies keeping verification mandatory;
  the gotcha now shows the pattern is crew-level, not one-off.

### P5 — Pane-ids gotcha: moves RE-SCOPE ids; herdr parse keys
- Target: AGENTS.md (pane-ids gotcha) · Class: auto
- Change: append: a workspace move MUTATES the pane id (w4T:p1 →
  w1T:pXM — the pre-move id becomes a phantom the watcher chases) — the
  ledger pane_id must be re-captured post-move (×5 on 08-12/13: pXM, pZ8,
  pZD, p0V, p16W). herdr JSON parse keys: split result = `result.pane`,
  move's tab = `move_result.created_tab` (wrong keys leave orphan panes).
- Evidence: silas 08-12 10:25Z/13:55Z/14:45Z/18:50Z ("id re-scoped
  w4T:p1->w1T:pXM on move — ledger corrected" ×4); silas 08-12 08:2xZ
  ("pane-split parse key is result.pane (not split_result)").
- Reasoning: the id-capture habit gotcha (08-08) named typos; this window
  showed the MOVE mechanism behind fresh phantom ids.

### P6 — NEW gotcha: never guess review-URL anchor ids
- Target: AGENTS.md (new bullet, ledger section) · Class: auto
- Change: never construct a review URL by guessing the anchor id —
  `gh api repos/<owner>/<repo>/pulls/<n>/reviews --jq '.[-1].id'` first
  (the review-sensor alert gives the id, pane-done alerts don't).
- Evidence: silas 08-11 19:43Z ("SLIP: my first done-note guessed the
  review URL anchor id (4908829057) — corrected via gh api… LESSON: never
  construct a review URL by guessing the id"); silas 08-11 21:20Z
  ("review id 4910842259 — fetched via gh api, the 1.4 lesson held"). ×2.
- Reasoning: guessed ids write wrong URLs into the permanent ledger.

### P7 — Fix-audit-hold gotcha: CI pending ≠ red
- Target: AGENTS.md (fix-audit-hold gotcha) · Class: auto
- Change: append: the unstable-target hold gates on RED CI only — a fresh
  r1 dispatch is OK on 4/5 pass + 1 pending ("UNSTABLE=pending not red");
  treating pending as red needlessly blocks fresh rounds.
- Evidence: silas 08-13 08:48Z ("CI 4/5 pass + 1 pending (UNSTABLE-pending,
  not red — fresh-r1 dispatch OK)"); silas 08-12 09:2xZ ("CI pending
  (UNSTABLE=pending not red)"). ×2.
- Reasoning: the hold doctrine reads stricter than it is; the pending
  classification recurs at every dispatch window.

### P8 — Mid-flight reversals gotcha: amend-canon + relay; prototype main = ground truth
- Target: AGENTS.md (user mid-flight reversals gotcha) · Class: auto
- Change: append: the healthy mid-flight path is AMEND the canon docs +
  RELAY to the in-flight minion so the PR ships the ruling (spatial-lane
  canon 2e3acab/8ece056 relayed to 3.3 pZ8; the PR carried the canon); and
  when GDD/architecture/stories diverge, the prototype's main branch is
  the ground truth to diff against (router-placement miss audit).
- Evidence: gru 08-12 ("CANON: QoS lanes are SPATIAL… Amended all three
  docs… relayed to the in-flight 3.3 minion (pZ8)"; "the PROTOTYPE had
  Cmd_Place_Router… main branch = prototype-era code, placement intact").
- Reasoning: extends the 08-07/08 reversals gotcha with the standard
  recovery that worked twice in one day.

### P9 — Model dispatch gotcha: briefing model lines are load-bearing for mega-minions
- Target: AGENTS.md (model dispatch gotcha) · Class: auto
- Change: append: briefings must name the model for minion AND
  mega-minions EXPLICITLY every time — the code-review skill pins NO
  model on lens launches, and bare `pi` resolves to defaultProvider
  (kimi-coding — a RETIRED provider since 08-12, so an unset dispatch
  silently lands on kimi/k3); template model lines rot ("unset" in the
  dream template meant retired-kimi at 08-13 dispatch — override
  required).
- Evidence: gru 08-12 ("GRU BRIEFING RULE from here: Model policy names
  deepseek/deepseek-v4-flash for minion AND mega-minions, explicitly,
  every time"); silas 08-12 08:36Z ("The code-review skill pins NO model
  on mm launches — the guidance was load-bearing"); silas 08-13 16:12Z
  ("template's 'unset' is stale — pi default = retired kimi/k3").
- Reasoning: three independent confirmations in 24h that the model line
  is an operational control, not documentation.

### P10 — minion-field-notes: rlsw harness entry addendum (R/B-swap + gitignored rlsw + tprintf)
- Target: docs/minion-field-notes.md (rlsw entry) · Class: auto
- Change: extend the 08-11 rlsw entry: a bare `odin build harness` (no
  tools/harness.sh) links the stock GPU raylib and produces R/B-SWAPPED
  golden frames (921600/921600 pixel diffs — looks like a render bug,
  isn't); rlsw is gitignored → ABSENT in a fresh worktree → point
  ODIN_ROOT at the main checkout's shadow
  (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`); Odin `fmt.tprintf` uses the
  TEMP allocator — in-loop strings that outlive the tick iteration must
  be `fmt.aprintf` (T2 failure strings were blank garbage the first time
  that path ran), and JSON literals need `{{`/`}}`.
- Evidence: 4.2 08-13 ("Build the harness ONLY via tools/harness.sh — a
  bare odin build harness… R/B-swapped golden frames"); 2.2-ecmp 08-11
  ("rlsw is gitignored, so it's ABSENT in a fresh worktree — ODIN_ROOT=
  <main>/tools/raylib-sw/shadow"); harness 08-12 ("fmt.tprintf = temp
  allocator… the T2 failure path had never run before").
- Reasoning: extends the existing black-frame entry with the failure
  modes this window actually produced (×3 jobs).

### P11 — minion-field-notes: NEW PP golden-discipline entry
- Target: docs/minion-field-notes.md (Tooling traps) · Class: auto
- Change: new entry consolidating the ×7-sighting golden rules: (a)
  catalog edits are GOLDEN-POISONED — cat.hash folds every catalog byte
  (any balance.json/node_type change re-blesses ALL .t1/.log.bin — wire
  new rules as core consts until a legitimate re-bless); (b) T1-dump
  additions must be ABSENT-WHEN-EMPTY (a zero count still shifts every
  default-run hash); (c) a re-bless is deliberate + PROVEN or it's a
  finding — byte-verify `.log.bin` differs ONLY in the version field,
  splice the OLD catalog_hash into the new dump (fnv must equal the
  blessed tick-1 golden), cause-document every shift; (d) DERIVED state
  (bundles, routing tables) keeps goldens valid — prefer derived over
  serialized.
- Evidence: 3.5 08-12 ("Catalog edits are GOLDEN-POISONED… cat.hash folds
  every catalog byte"); 3.2 08-13 ("T1-dump additions must be
  ABSENT-WHEN-EMPTY… prove behavioral identity BEFORE blessing"); 2.1/2.2
  08-11 ("Zero serialized-state change → byte-identical, no re-bless");
  1.4/3.4/4.1 (re-bless cause-documented every time).
- Reasoning: the single most-repeated PP lesson of the window — each
  story rediscovered it; one entry stops the rediscovery.

### P12 — minion-field-notes: ground-truth-first addendum (new claim-types)
- Target: docs/minion-field-notes.md (ground-truth-first entry) · Class: auto
- Change: 08-13 addendum, new claim-types: grep the ARCHITECTURE
  AMENDMENTS REGISTER for amended behavior before trusting a briefing AC
  (rc3-6's "inbound STOP→objected" was dead); grep DB ENUM MIGRATIONS,
  not the briefing, for emitted sets (rc4-4: FIVE codec variants, not
  four); carry-forward claims about repo state rot within a day ("T2
  unverified until the rlsw harness exists" was stale — the harness
  existed and worked).
- Evidence: rc3-6 08-11, rc4-4 08-13, 2.2 08-11, harness 08-12, rc4-1
  08-12 (×5 sightings).
- Reasoning: the addendum pattern of this entry (claim-types diversify);
  this window added three new types.

### P13 — minion-field-notes: negative-control addendum (escaped wire form + revert-grep)
- Target: docs/minion-field-notes.md (negative-control entry) · Class: auto
- Change: append: assert BOTH forms of a JSON-string-embedded payload —
  the ESCAPED wire form (`\"referee_ip\"`) is what ships; a
  `string.contains(body, "\"referee_ip\"")` assertion is vacuously green
  while the IP is on the wire. And grep the file AFTER a python-replace
  negative-control revert — an inline-arg call survived the first revert
  and silently kept the fix.
- Evidence: rc4-1 08-12 ("a string.contains(body, "\"referee_ip\"")
  assertion is vacuously green while the IP is on the wire"); rc1-1 08-12
  ("the UA path survived my first revert and silently kept the fix").
- Reasoning: two new failure modes of the prove-it-bites discipline.

### P14 — minion-field-notes: NEW recurring finding — timestamp format-mix
- Target: docs/minion-field-notes.md (Recurring review findings) · Class: auto
- Change: new entry: PG `::text` renders timestamps with a SPACE
  separator, app code stamps RFC3339 `T` — space (0x20) < 'T' (0x54), so
  string compares/sorts invert same-day events (evening before morning).
  Normalize space→T before comparing/sorting, and pin with a fixture the
  server ACTUALLY sends (the rc4-2 pin fed a never-sent format — Perkins
  r2 W4 caught the wrong fix).
- Evidence: rc4-2 r2 08-12 (W4 "fix wrong for production — ' ' < 'T'
  inverts same-day form-open vs invitation"); rc4-3 r2 08-12 (W3
  "headline format-mix… 'T' > ' '"); rc4-4 08-13 ("the old client-side
  timeline sort silently mis-ordered same-day events"). ×3.
- Reasoning: three rounds across three jobs found the same inversion —
  the canonical RT review finding of the window.

### P15 — minion-field-notes: NEW — correction-boundary invariants
- Target: docs/minion-field-notes.md (Tooling traps) · Class: auto
- Change: new entry: when a one-cycle correction/retry loop exists, the
  CORRECTION INSTANT segments everything downstream — reset the attempt
  counter + capability token on re-queue (a corrected row at count 1
  dead-ends the co-nudge step forever), gate post-loop failures on
  `corrected_at` (stale/redelivered pre-correction events must stand
  down, never fabricate a fraud signal), and segment send batches by the
  corrected_at boundary (batch index alone mislabels the re-invite as
  "Reminder N").
- Evidence: rc4-3 08-12 (×2 clauses), rc4-4 08-13 ("segment send batches
  by corrected_at boundary") + the rc4-3 r1-r5 B1 saga (cadence-restart
  re-fire = fold accumulator).
- Reasoning: three adjacent bugs from one missing invariant — the
  boundary must segment everything downstream.

### P16 — minion-field-notes: NEW — DB-stored text ≠ app text
- Target: docs/minion-field-notes.md (Tooling traps) · Class: auto
- Change: new entry: three flavors of one trap — (a) Gleam
  `string.slice` counts GRAPHEMES, Postgres `length()` counts CODEPOINTS
  → codepoint-bounded slicing is the only cut that satisfies a DB CHECK
  for multi-codepoint headers (ZWJ emoji: 1 grapheme = 7 codepoints);
  (b) `jsonb::text` adds a space after `:` → substring-contains on
  STORED fraud_signals fails — parse + decode the field (unit tests pass
  because they check gleam's compact json.to_string output, integration
  reads Postgres); (c) the timestamp space-vs-T mix (P14 — pin with
  server-real fixtures).
- Evidence: rc1-1 08-12, rc3-7 08-12, rc4-4 08-13 (×3 flavors).
- Reasoning: slice/sort/contains on DB-stored text must use the DB's
  representation — three independent losses to it this window.

### P17 — minion-field-notes: NEW — Gleam/Lustre trap cluster
- Target: docs/minion-field-notes.md (Tooling traps) · Class: auto
- Change: new entry: (a) an EMPTY-STRING attribute value is a PRESENT
  boolean attribute — `attribute("disabled","")` ships
  permanently-disabled buttons (omit when enabled: `list.append(attrs,
  case busy {True -> [attribute("disabled","true")] False -> []})`);
  (b) gleam 1.15.1 REJECTS `++ [list-literal]` ("operator has no value
  on its right side") — use `list.append`/spread; (c) `list.all([])` is
  vacuously True — check emptiness BEFORE the all-terminal branch; (d) a
  case-clause body starting with `let` is a parse error unless braced;
  no function calls in clause guards; no `..` spread in this Gleam
  version; (e) `decode.optional_field` is the `use`-callback 4-arg form
  (Decoder(t) of the default's type).
- Evidence: rc4-2 08-12, rc4-3 08-12 (×2), rc4-4 08-13 (×3 jobs).
- Reasoning: each cost a debugging cycle; one consolidated cheat-sheet
  entry beats per-job rediscovery.

### P18 — minion-field-notes: Squirrel addendum (verify each hunk)
- Target: docs/minion-field-notes.md (Squirrel entry) · Class: auto
- Change: append: regen churns `application/sql.gleam` formatting hunks
  unrelated to new columns — VERIFY EACH HUNK before keeping (rc4-4
  reverted one); `ai/sql.gleam` whitespace → revert the whole file.
- Evidence: rc3-7 08-12 + rc4-4 08-13 (×2).
- Reasoning: extends the revert-churn convention with the per-hunk
  verification step.

### P19 — minion-field-notes: Test-DB port register addendum
- Target: docs/minion-field-notes.md (test-DB entry) · Class: auto
- Change: append: the Makefile HARDCODES 54321; as of 08-13 sibling
  worktrees owned 54321/54326/54327/54332-34 — grab a free port and pass
  `TEST_DATABASE_URL=postgresql://test:test@localhost:<port>/
  righttenantry_test` to `gleam test -- --tag integration`.
- Evidence: rc1-1 08-12 + rc4-4 08-13 ("the sibling worktrees own
  54321/54326/54327/54332-34"). ×2.
- Reasoning: the hardcode is the standing trap; the port list tells the
  next minion what's taken.

### P20 — minion-field-notes: edit-atomicity addendum (tab-depth facet)
- Target: docs/minion-field-notes.md (edit-atomicity entry) · Class: auto
- Change: append: nested-code batches need EXACT tab depth — a 5-edit
  batch to a 3-level-deep switch was rejected silently (all 5 lost)
  because one oldText was indented 3 tabs, not 4. Re-read the exact depth
  of nested code before authoring batch oldText.
- Evidence: 2.3-demolish 08-12 ("a 5-edit batch… REJECTED SILENTLY…
  because ONE oldText had shallow indentation").
- Reasoning: a new failure facet of the existing atomicity entry.

### P21 — minion-field-notes: absolute-path addendum (wrong-tree green gates)
- Target: docs/minion-field-notes.md (worktree-paths entry) · Class: auto
- Change: append: 3rd sighting — the gates THEMSELVES cd'd to the main
  checkout, so odin test/lint/harness passed against the WRONG tree
  (edits + tests both misdirected). After edits, `git status` from cwd
  BEFORE trusting a green test run.
- Evidence: 2.2-ecmp 08-11 ("the absolute-path trap bit AGAIN… they
  passed against the WRONG tree").
- Reasoning: green-on-wrong-tree is the worst false confidence; closes
  the loop with the check order.

### P22 — minion-field-notes: 2-hunter swarm addendum (code PRs too)
- Target: docs/minion-field-notes.md (swarm entry) · Class: auto
- Change: append: the pre-PR self-review earns its cost on CODE PRs too
  — an edge-case-hunter self-review before the PR paid off 4 real fixes
  on rc4-1; the 2-hunter swarm caught the spatial-lane mirroring bug on
  3.3 — both before Perkins saw the PR.
- Evidence: rc4-1 08-12 ("an edge-case-hunter self-review before the PR
  paid off 4 real fixes"); 3.3 08-13 ("The 2-hunter review swarm caught
  it"). ×2, both repos.
- Reasoning: extends the 08-07 docs-swarm entry to the code-PR case.

### P23 — minion-field-notes: NEW — verify by observable effect
- Target: docs/minion-field-notes.md (Conventions) · Class: auto
- Change: new entry: reported success lies — verify by OBSERVABLE
  effect, not return values: a narrow pipe draw is silently REJECTED
  (max_span 10) → zero events (spawn nodes ≤10 apart for narrow-tier
  tests); adding pipes to a full router silently rejects
  (Router_Ports_Full → replay_error latched); Odin `strings.replace`
  returns replaced=true while the doc holds the old substring (raw-string
  newline mismatch — pin single-line anchors or byte-verify); test-catalog
  `Balance` fields must mirror data/balance.json (zeroed thresholds =
  every node red at tick 1, silently shifting every dump).
- Evidence: 3.4 08-12, 4.2 08-13, 4.1 08-13 (×2). ×4 sightings, both
  repos.
- Reasoning: four silent no-op paths cost four debug cycles this window.

### P24 — minion-field-notes: registry entry addendum (per-route-family arms)
- Target: docs/minion-field-notes.md (registry-omission entry) · Class: auto
- Change: append: which arms apply is PER-ROUTE-FAMILY — a NEW top-level
  path family (`/webhooks/*` vs `/api/v1/webhooks/*`) needs its OWN
  registry arms; the existing `["api","v1","webhooks",..]` CSRF prefix
  did NOT cover it (a missing arm 403s). Verify each registry
  (is_public_path / CSRF / redact_token_route) against disk per route
  family.
- Evidence: rc3-6 08-11 ("the existing CSRF prefix did NOT cover them…
  Verify each registry against disk per route family").
- Reasoning: extends the rc3-3 lesson with the family-granularity
  clarification.

### P25 — minion-field-notes: NEW — vacuous-test blocker class (Perkins)
- Target: docs/minion-field-notes.md (Recurring review findings) · Class: auto
- Change: new entry: a fix whose regression test is VACUOUS or ABSENT is
  still a blocker even when the mechanism is real by inspection —
  fix-audit rounds must verify the test pins the ORIGINAL failure mode
  and drives the REAL route (rc4-3 r4: the backstop test called the dead
  SQL directly, never the POST route; #36 r2: the demolish-and-renumber
  test was absent — every resolve fixture preserved slot order). The
  r5-style fix: drive the POST route + pin the SQL mechanism + neutralize
  → red.
- Evidence: silas 08-13 08:48Z + 15:00Z (×2 blockers, both repos).
- Reasoning: mechanism-inspection alone passed a broken fix twice; the
  test-verification mandate is what the final rounds enforced.

### P26 — minion-field-notes: Lustre entry addendum (source-side empty attr)
- Target: docs/minion-field-notes.md (Lustre serialized-render entry) · Class: auto
- Change: append: the SOURCE side mirrors it — an empty-string attribute
  value serializes as a PRESENT attribute (see P17a): writing
  `attribute("disabled", "")` ships a permanently-disabled button; omit
  the attribute instead.
- Evidence: rc4-2 r1 B2 08-12 ("Lustre empty-string attribute →
  confirm/save buttons always disabled in-browser") + rc4-3 08-12.
- Reasoning: pairs the assert-side entry with the write-side trap.

### P27 — minion-field-notes: NEW — PP sim-truth traps
- Target: docs/minion-field-notes.md (PP section) · Class: auto
- Change: new entry: (a) `record_run` clears `state.events` every tick
  (ODN-14 drain) — any end-of-run event scan is vacuous; collect the
  stream while stepping; (b) breach ratios are NOT monotone — later
  deliveries dilute the ratio below tolerance, so transition-style exits
  fire falsely: latches must be sticky-Enter by contract ("monotone"
  applies to the counter, never the ratio); (c) carry ADMISSION-TIME
  truth in events (the shed bundle) + resolve hysteresis or the
  trigger/resolve pair chatters every few ticks on marginal networks.
- Evidence: 3.4 08-12 (×2), 4.2 08-13 + 4.2 r1 N13 (ODN-14
  event-buffer-as-sim-input coupling). ×3.
- Reasoning: sim-truth lessons that generalize beyond the single story
  each came from.

## Watch items (anecdotes — tracked, not proposed)

- W1: no-args `herdr worktree create` made a JUNK worktree in the
  ORCHESTRATOR ROOT (08-13, silas 10:52Z) — never invoke without
  --cwd/--branch/--base/--label. STRONG flag; one sighting so far.
- W2: minions over-halt at internal "approval" checkpoints (08-12 pVT,
  parked "awaiting approval" pre-push) — standing orders pre-approve
  internal checkpoints; fix is one relayed nudge, never a relaunch.
- W3: a round pane can stall ~5h with no artifacts + session file gone
  (08-13 rc4-3 r4) — the signature says RELAUNCH (re-does setup), not
  continue; an overnight-stall watch at morning reconciliation.
- W4: Twilio X-Twilio-Signature signs the EXACT callback URL — the
  verifier must reconstruct it from TWILIO_STATUS_CALLBACK_BASE_URL +
  the const, never the request's Host (proxy mismatch fails
  verification) — rc3-6.
- W5: vision models are UNRELIABLE at sub-5px differences (2.1: missed a
  2px diff + hallucinated text) — measure goldens programmatically (PIL
  pixel diff + thickness count), don't trust describe_image for render
  verification.
- W6: deferred multi-removal by index needs an ascending sort BEFORE the
  descending splice (3.3: two same-tick sheds spliced the WRONG packet,
  blessed into goldens) — sort-then-descending + same-tick regression.
- W7: blocked-on-external-data jobs get a dated re-check + pre-planned
  dispatch action (08-12 dublin-rents: re-check ~08-19, then bump
  priority + dispatch) — a routine worth standardizing.
- W8: mid-round 403 with SETUP-ONLY artifacts (zero lens JSONs) = light
  doctrine (no regenerate, no re-dispatch, same row, mid-pane model
  switch) — harness r1 08-12; one sighting.
- W9: Odin `strings.replace` reports replaced=true while the doc holds
  the old substring when fixture raw-string newlines don't match the
  file's (4.1) — pin single-line anchors or byte-verify.
- W10: test-catalog `Balance` fields must mirror data/balance.json
  (4.1: zeroed warnings thresholds = every node red at tick 1).

## Pruned / rejected candidates

- Echo discipline (ledger C2: ×12 note-only echoes) — already codified;
  reinforcement only, no new content.
- bmad canonical-checkout quirk live confirmation (journals C23) — the
  08-11 entry + cmp-verified recovery already cover it; the cold
  execution validates, adds nothing.
- Fix-audit round contract (prior_findings / verify-each / chunking) —
  playbook lines 930-975 codify it; nothing new.
- Kimi probe false-dawn discipline (ledger C4) — MOOT: kimi k3 retired
  entirely (08-12-late ruling); the false-dawn premise is already in the
  provider gotcha's supersede chain.
- Model flip-flop event chain (08-12 08:37-08:39Z) — same retirement;
  superseded by the final ruling already in the gotcha.
- Router_Ports_Full / narrow-span / strings.replace / Balance-mirror as
  standalone entries — promoted into P23's cluster (silent no-ops).
- Grapheme/codepoint as standalone — promoted into P16's cluster
  (DB-stored text).
- Lens-loss tolerance (ledger C8) — promoted to user-ack U6 (the
  perkins-pr-review-plan only has the degraded guard, not the 6/7
  sufficient-not-degraded judgment).

## User-ack proposals (no store edit — Silas escalates to Gru)

### U1 — Playbook: cap-override doctrine
The 3-round cap is doctrine, not law: the user can order r4/r5 (rc4-3
saga: r4 + r5 both user-approved fix-audits, r5 APPROVED). Mechanics to
codify: override rounds run fix-audit + prior_findings +
verify-don't-reopen (same as normal rounds); the MINION is unaware of
overrides (believes cap-hit, parks) — Silas/Gru track the budget and
escalate at push time ("next sha = r5 — beyond the user-approved r4 →
escalate"); cap alerts superseded by user overrides = note-only.

### U2 — Playbook: FULL THROTTLE + file-disjointness hold gate
User ruling 08-12 15:50Z: the serialize doctrine is SUSPENDED for
Perkins rounds while on deepseek API ("full throttle… glm-429/1308 cap
history does not apply"). New hold-vs-parallel gate: file-level
DISJOINTNESS — hold when goldens/ or shared modules overlap (08-13
routing-bandwidth-cost held on goldens/ overlap with #36; B+C verified
disjoint by file → parallel). The pane-capacity serialize rule only
binds on capped providers.

### U3 — Playbook: pr_review=0 quick-fix scope (user-ruled 08-12)
The quick-fix shortcut applies to CI/ops-tooling fixes ONLY — not
gameplay/canon-surface code (new command kinds, serialization,
LOG_VERSION, payload contracts) — those keep pr_review 1. (#30 3.5
node-placement was wrongly briefed 0; the user caught it.)

### U4 — Playbook: follow-up intake + deferred-work sweep routine
User-ruled 08-12: advisory findings batch into ONE issue per repo (#34
PP, #607 RT); parse bmad deferred-work docs at dispatch windows — run
unblocked items parallel-safe, gate or fold the rest into future
briefings (RC2.1 codec folded into RC4.4).

### U5 — Template fix: _template-dream.md carries two known-stale lines
(a) the marker writer line says Gru; the playbook says SILAS writes the
marker (known stale since 08-11, flagged again 08-13 16:12Z); (b) the
model line says "unset" — unset resolves to defaultProvider = retired
kimi/k3; make the template name deepseek/deepseek-v4-pro explicitly
(Bob + every sheep). Two one-line edits.

### U6 — perkins-pr-review-plan.md: lens-loss tolerance
Add the 6/7-lens judgment: a round completes at 6/7 lenses when the
stuck one's concerns are covered elsewhere ("sufficient not degraded" —
×3 sightings 08-11/12); recovery for a 429'd/stuck lens = 2-concurrent
re-wave, not a full round re-run.
