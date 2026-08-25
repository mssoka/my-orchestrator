# Dream report — 2026-08-11

Material: **14 field-note shards**, **4 journal files** (gru 2026-08-09
tail + 2026-08-11; silas 2026-08-09 ~920 lines + 2026-08-11), **200 ledger
events** (+ `show` on ~10 active jobs), since **2026-08-09T13:54:22Z**.
3 sheep (shards / journals / ledger) read their sources and wrote
candidate shards; this report is Bob's consolidation after a
`bmad-review-adversarial-general` verification pass (each candidate
challenged against its quoted evidence; ≥2 independent sightings to
promote, else watch).

Window character: the **kimi-quota-403 saga** (glm-5.2 became the
sanctioned Perkins fallback), the **packet-plumber v2 from-scratch
sprint start** (Odin/Raylib, 3 vertical-slice stories), a dense **RT
refcheck rc3-4 → rc3-5** Perkins rework chain, and the **RTA #172
boundary-gate family** (ADK state-marshalling). Dense window → dense
dream.

**All 17 proposals are `auto`** (field-notes promotions/amendments +
AGENTS.md gotcha appends/amends to *existing* subsections — no new
sections, no playbook/policy/persona changes). Applied to the store
copies in `store/`; Silas copies store → live at close-out.

---

## Proposals

### minion-field-notes.md

### F1 — bmad tooling resolves repo-root to the CANONICAL checkout, bypassing a worktree minion's writes  ★
- Target: minion-field-notes.md (Tooling traps) · Class: **auto** (AMEND the 2026-08-07 "relative paths surprise in worktrees" entry)
- Change: append a 2026-08-11 addendum naming the bmad-tooling root-resolution cause + the source-file escalation + the verify-where-edits-land rule.
- Evidence:
  - righttenantry-refcheck-rc3-5 (2026-08-11): "the bmad tooling (create-story/dev-story) resolves the repo root to the CANONICAL checkout (/Users/moses/code/RightTenantry) instead of the worktree cwd — sweep.gleam + 5 sweep_*.sql landed entirely in the main checkout; the worktree was completely clean."
  - righttenantry-refcheck-rc3-3/-rc3-4 (2026-08-10): tracker/spec artifacts written to the MAIN checkout by the bmad tooling (path quirk); close-out stash→pull→pop to recover.
  - Gru journal 2026-08-11: "bmad tooling-quirk (writes tracker/spec to main checkout, not worktree) — 3+ sightings; field-note candidate."
- Reasoning: 4+ sightings, escalating severity (tracker → spec → LIVE source); the existing relative-paths entry doesn't name the tooling root-resolution cause. Gru explicitly named it as the field-note candidate.

### F2 — ADK `ctx.state` is a per-node SNAPSHOT, not live; cross-node gate state via `ctx.session.state` (+ the divergent-fake-ctx test harness)
- Target: minion-field-notes.md (Tooling traps — new ADK cluster) · Class: **auto**
- Change: add a new Tooling-traps entry covering (a) `ctx.state` snapshot vs `ctx.session.state` live; (b) the InMemory `_Recorder` harness can't reproduce it — build a divergent fake ctx; (c) `output_key` write is conditional but `after_agent_callback` always fires → stale-slot; per-attempt pop is hygiene.
- Evidence:
  - righttenantryagents-boundary-gate-state-fix (2026-08-10): "ADK `ctx.state` is a per-node SNAPSHOT, not live … `ctx.state.get(child_key)` returns `None` right after `run_node`. The RT convention (agent.py:263/:396) is raw `ctx.session.state` for ALL cross-node gate state."
  - righttenantryagents-boundary-gate-state-fix (2026-08-10): "the InMemory recorder harness CAN'T reproduce this — `_Recorder` stubs share the live dict; build a divergent fake ctx (stale snapshot + live session.state)."
  - righttenantryagents-boundary-gate-slot-clear (2026-08-11): "ADK skips the `output_key` write on empty/schema-fail/tool-call-only … while `after_agent_callback` ALWAYS fires → a clean attempt can leave the PRIOR dirty review … the per-attempt `pop` is necessary hygiene."
- Reasoning: spans 2 RTA jobs, Perkins-verified, silent failure (looks right, fails silently). RT-Agents is an active project.

### F3 — Squirrel emits its OWN per-module enum types (shadowing shared) + shared-constructor enums can't be emitted (NULLIF-string-cast)
- Target: minion-field-notes.md (Tooling traps) · Class: **auto** (AMEND the 2026-07-31 Squirrel triple-trap entry)
- Change: append a 2026-08-10 addendum: (a) status args must be the trigger module's `sql.<Variant>`, not the shared variants (type mismatch); (b) when two PG enums share constructor names, use STRING + `NULLIF($n,'')::<enum>` cast, never a bare `$n::<enum>`.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10): "Squirrel generates its OWN `ReferenceCallStatus` inside `reference_checks/sql.gleam` SEPARATE from `shared.*` — status args must be `sql.Refused`/etc., not the shared variants."
  - righttenantry-refcheck-rc3-5 (2026-08-10): "the `reference_call_*` status + outcome enums SHARE constructor names → Gleam forbids duplicate constructors → outcomes are passed as STRING + `NULLIF($n,'')::reference_call_outcome` cast."
- Reasoning: 2 independent Squirrel type traps across 2 jobs; each costs a compile cycle.

### F4 — T2 pixel goldens need the rlsw SOFTWARE renderer (stock GPU raylib renders solid black headless)
- Target: minion-field-notes.md (Tooling traps) · Class: **auto** (NEW — the Raylib analog of the 2026-07-31 Godot headless entry)
- Change: add a new entry: `odin run harness` links stock GPU `vendor:raylib` → solid black headless (no GPU context); use `tools/harness.sh` (rlsw software renderer); port the prototype's `goldens.odin` (flip + BGRA→RGBA swizzle) verbatim; kick the ~40s `tools/build_raylib_sw.sh` off in the BACKGROUND before coding.
- Evidence:
  - packet-plumber-v2-1.2-window-draw-pipe (2026-08-11): "rlsw T2 capture path works headless via `rl.InitWindow` + `LoadImageFromScreen` … the SW raylib build takes ~40s + a github clone; kick it off in the background before coding."
  - packet-plumber-v2-1.3-packet-flow (2026-08-11): "T2 pixel goldens need the rlsw software renderer — `odin run harness` links the stock GPU `vendor:raylib` and renders a SOLID BLACK frame headless."
- Reasoning: 2 sightings across 2 PP-v2 stories; the GPU-black-frame failure is the raylib analog of the Godot headless trap; load-bearing for every PP-v2 story that adds a golden.

### F5 — verify-briefing-premises: 2026-08-11 addendum (4 new stale/wrong claim-types)
- Target: minion-field-notes.md (Conventions — ground-truth-first) · Class: **auto** (AMEND the 2026-08-07 verify-premises entry, which lists claim-types)
- Change: append a 2026-08-11 addendum listing 4 new claim-types seen this window: (a) **stale-stack planning doc** — a recent DATE doesn't mean current stack (v1 sprint-plan dated post-Odin-pivot but drafted in Godot/GDScript citing the superseded arch); (b) **wrong identifier/state-key** — briefing named `STATE_FINAL_OUTPUT` (the scrubber payload) not `STATE_FINAL_COMPLIANCE_REVIEW` (the gate's review slot); (c) **wrong mechanism model** — "register each route in ALL three registries" rests on a per-arm model; the registries are prefix-matched (one arm covers any depth); (d) **namespace collision + superseded-vs-live doc** — two "E" namespaces (arch edge-cases E1–E32 vs GDD epics E1–E11); `architecture-v1.md` (superseded Godot) vs `odin-architecture-v1.md` (live canon). Grep the symbol/citation against disk before acting on a briefing's named identifier/mechanism/stack.
- Evidence: packet-plumber-sprint-replan-v2 (a), righttenantryagents-boundary-gate-slot-clear (b), righttenantry-refcheck-rc3-4 (c), packet-plumber-routing-canon-amend (d) — all 2026-08-10/11, one per claim-type.
- Reasoning: folds 4 single-sighting items into one amendment to an already-≥5-sighting pattern; each is a concrete new claim-type.

### F6 — canon-doc amendment craft: 2026-08-11 addendum (width-preserving ASCII, no-overlap placement, dual-append merge, namespace disambiguation)
- Target: minion-field-notes.md (Conventions — canon-doc amendment craft) · Class: **auto** (AMEND the 2026-08-09 entry)
- Change: append a 2026-08-11 addendum: (a) ASCII-box edits MUST be **width-preserving** (`span, LB)`→`span,bndl)` kept 13 chars — a width-shift breaks diagram alignment); (b) **pre-emptive no-overlap placement** under an open sibling PR — grep the sibling's hunks, place inserts outside them → clean auto-merge; (c) for an append-only decision-log, a mid-job sibling-merge conflict resolves as **DUAL-APPEND (keep both)**, not pick-a-side; (d) **disambiguate same-letter namespaces + superseded-vs-live docs** before editing (folds the doc-pair half of F5(d) into the craft rule too).
- Evidence: packet-plumber-routing-canon-amend (a,d), packet-plumber-gdd-mechanics-amend (b,c) — 2026-08-10.
- Reasoning: folds 4 single-sighting craft refinements into one amendment; each is a concrete new craft rule.

### F7 — A client-populated hidden field is INERT without page-specific JS wiring; `simulate.form_body` MASKS it
- Target: minion-field-notes.md (Conventions / Recurring review findings) · Class: **auto** (AMEND the 2026-08-03 "Node tests blind to browser semantics" + 2026-08-09 "prove a test BITES" entries)
- Change: append a 2026-08-10/11 addendum: a hidden field ships in HTML but is never populated unless page-specific JS wires a submit listener; a `simulate.form_body` integration test PASSES while prod stays broken. Fix = wire a page-specific submit seam + drive the BROWSER path in a node test (not the simulator) + prove it bites (neutralize → red). This is now a standing Perkins lens-guard ("NOT a simulate.form_body mask — the #599 r2 lesson") carried into #21/#174/#22 briefings.
- Evidence:
  - righttenantry-refcheck-rc3-4 Perkins r2 (2026-08-10): "W1's fix is INERT — `_focus_seconds` ships in HTML but `reference_form.js` never populates it → always 0 in prod; the new flow test MASKS it (`simulate.form_body` bypasses the browser)."
  - righttenantry-refcheck-rc3-4 r3 (2026-08-10): fix = `initReviewSubmit` seam + 4 node browser-path tests.
  - righttenantryagents-boundary-gate-slot-clear Perkins r1 (2026-08-11): same masking-test class caught again ("the clean stamp derives from the SAME slot whose write the test claims lost").
- Reasoning: recurred within one review arc (r1→r2→r3) AND propagated as a named lens-guard to 3 later rounds; the most-reinforced minion lesson this window.

### F8 — The "registry-omission" blocker class: every new POST route must be registered in ALL access-control/observability registries
- Target: minion-field-notes.md (Recurring review findings) · Class: **auto** (NEW)
- Change: add a new Recurring-review-finding entry: adding a POST route means registering it in EVERY registry the codebase maintains (RT: `is_public_path`, CSRF allowlist, `redact_token_route`). Missing one is a recurring Perkins blocker (csrf arm absent → 403; redact arm absent → token leak). Enumerate every registry and arm each; the lesson is now baked into RT briefings by name ("the rc3-3 csrf-registry lesson").
- Evidence:
  - righttenantry-refcheck-rc3-3 Perkins r1 (2026-08-09): "B1 csrf.should_skip missing `["reference",..]` arm — same registry-omission class as the rc3-2 redact gap; 3-lens agreement."
  - righttenantry-refcheck-rc3-4 briefing (2026-08-10): "MUST register every new POST route in ALL 3 registries — the rc3-3 csrf-registry lesson."
- Reasoning: ≥3 sightings (rc3-2 redact, rc3-3 csrf, rc3-4 carry-forward); a recurring Perkins-blocker class now propagated into briefings.

### F9 — PP-v2 determinism spine: thread every run-setup through BOTH live + replay (else ODN-11 diverges at tick 1)
- Target: minion-field-notes.md (Tooling traps) · Class: **auto** (NEW — PP-v2 determinism)
- Change: add a new entry: the replay gate re-creates run-setup (fixture) but NOT flow demand by default — flow demand is run-setup (not in the action log), so a new run-setup added to the sim (spawn intents, director plans) must be threaded through `replay_hashes` in BOTH live (`lower_spawns`) and replay paths, or ODN-11 replay diverges at tick 1.
- Evidence:
  - packet-plumber-v2-1.3-packet-flow (2026-08-11): "the replay gate re-creates run-setup but NOT flow demand … ODN-11 replay diverged at tick 1 until I threaded the demo's `spawn` intents through `replay_hashes`."
  - packet-plumber-v2-1.1-walking-skeleton (2026-08-11): "the spine's `step` is a heartbeat (one owned-RNG draw/tick folded into a `tick_nonce` state field) — ties the RNG into the step path so replay-equality is non-vacuous."
- Reasoning: 2 sightings across 2 PP-v2 stories; load-bearing for every later PP-v2 story that adds run-setup.

---

### AGENTS.md gotchas (appends/amends to existing subsections)

### G1 — Serialize concurrent glm-5.2 BURSTS (model-capacity, sibling to pane-capacity serialize-hold)
- Target: AGENTS.md gotchas (Provider incidents) · Class: **auto** (NEW append)
- Change: add a bullet: a Perkins round = ~8 concurrent glm-5.2 panes; two rounds (or a round + a fanned-out mega-minion wave) concurrently trip an account rate-limit 429. SERIALIZE the bursts (one fan-out at a time); defer/stagger a job's mega-minions entirely until an in-flight Perkins round closes (trigger = the round's close-out). Distinct from the pane-capacity serialize-hold — same dedup, different gate (model-quota vs pane-count).
- Evidence:
  - Silas journal 2026-08-09T21:40Z: "ZAI-CODING-CN/GLM-5.2 429 rate-limit: 13 panes ALL glm-5.2 + rate-limited — likely a burst from 13 concurrent calls."
  - Silas journal 2026-08-09T23:48Z (Gru ruling): "serialize bursts; pQ4 fully-defers mega-minions until Perkins r2 closes … a 429 mid-round is the failure mode that killed it once."
- Reasoning: names the avoidable mid-round 429 that forced the rc3-3 r2 retry; the serialize trigger is cheap.

### G2 — kimi-quota-403 saga: glm-5.2 is the sanctioned Perkins fallback; first-turn 403 = `/model`+continue (not sweep)
- Target: AGENTS.md gotchas (Provider incidents) · Class: **auto** (AMEND the 3-classes gotcha — also updates the now-stale "redirect glm-5.2 → deepseek" bit)
- Change: append a 2026-08-11 addendum: with kimi quota-down all billing cycle, **glm-5.2 is the sanctioned Perkins fallback** (the 08-07 "redirect glm-5.2 → deepseek" doctrine is superseded when kimi is the down provider). A **first-turn 403** (no lenses/artifacts) recovers via mid-pane `/model zai-coding-cn/glm-5.2` + `continue` — pane recovers to working, NO re-dispatch, NO regenerate (lighter than the mid-work-403 sweep+regenerate doctrine, which still applies when partial lens JSONs exist). The "kimi is back up" premise (another job's activity / a Gru nod) is UNRELIABLE mid-cycle — 403 recurred within ~12 min of an apparent recovery. A 403-killed round is a RETRY on the SAME row (not rN+1); sweep ALL dead panes, fresh worktree @ same sha, regenerate ALL lens JSONs (discard 3-byte empties — they contaminate the verdict), carry prior findings forward. A pane-watcher `gone->done` echo right after a 403 is the transient pre-recovery flicker — note-only.
- Evidence:
  - righttenantry-refcheck-rc3-5-perkins-r2 (2026-08-11T13:55Z): "kimi-coding/k3 403'd at launch (quota exhausted this billing cycle) → switched to glm-5.2 via /model + continue; pane recovered. No work lost (first-turn 403)."
  - righttenantry-refcheck-rc3-3-perkins-r2 (2026-08-09T23:16/23:23Z): "kimi quota 403 AGAIN mid-review … RETRY #1 on glm-5.2 on the SAME r2 row (not r3); swept 8 dead panes; fresh worktree; regenerated all lens JSONs."
  - righttenantry-refcheck-rc3-5-perkins-r2 (2026-08-11T14:00Z): "pane-watcher echo `gone->done` was the transient post-403 flicker before /model+continue — stale, no action."
- Reasoning: folds 3 candidates (first-turn recovery, same-row retry, model-recovery echo); corrects a stale bit (glm-5.2 is now a recovery TARGET, not just redirect-away-from).

### G3 — A Perkins fix-audit round is HELD on an UNSTABLE review target (moving head / red CI), not just pane capacity
- Target: AGENTS.md gotchas (Watchers, sensors & Perkins rounds) · Class: **auto** (NEW append — sibling to serialize-hold)
- Change: add a bullet: a fix-audit round is deferred when the PR head is still MOVING (minion iterating CI fixes / active A/B) AND/OR CI is RED — the harness verification can't run on a red/unstable CI. Hold for the STABLE sha (CI green + r1 blockers addressed + minion done iterating). The review sensor RE-FIRES on every new commit while the head moves — those are echoes (note-only), not new work.
- Evidence:
  - packet-plumber-odin-prototype Perkins r2 (2026-08-09T18:43Z): "HELD — head fc3ca42 unstable: CI RED (ubuntu segfault + macOS catalog drift), minion still pushing fixes; r1 blockers unaddressed. Dispatch r2 on the STABLE sha."
  - packet-plumber-odin-prototype Perkins r2 (2026-08-09T19:13Z): "STILL HELD — head 0b92fa4 is a FEATURE commit (A/B verdict pending); r2 runs on the stable sha."
- Reasoning: distinct hold reason from pane-capacity serialize-hold; codifies the "sensor re-fires per-commit while head moves = echoes" class.

### G4 — Perkins-branch anomaly: `perkins-*` BRANCHES appear where only a DETACHED worktree should exist (audit-flagged, root cause inferred)
- Target: AGENTS.md gotchas (Watchers, sensors & Perkins rounds) · Class: **auto** (NEW append — audit flag)
- Change: add a bullet: Perkins rounds use DETACHED worktrees (`git worktree add --detach <sha>`, no branch — dedup is ledger-ROW-based). Yet `perkins-*` branches have appeared as merged debris (3 branches / 2 repos: perkins-odin-prototype-r1/r2 + perkins-refcheck-rc3-3-r1) — a dispatch is using `herdr worktree create --branch` (the regular-minion path) where `--detach` is correct, OR a Perkins minion created the branch. Harmless when caught (merged + recoverable from main; `branch -D`), but a dispatch-mechanics inconsistency worth auditing. **Root cause inferred, not confirmed** — flag for a dispatch-history audit (`--branch` where `--detach` was correct).
- Evidence:
  - Silas journal 2026-08-10T00:58Z: "Torch perkins-odin-prototype-r1/r2 branch debris; ANOMALY noted — Perkins rounds use detached worktrees, yet these existed as branches."
  - Silas journal 2026-08-10T01:02Z: "Perkins-branch ANOMALY = 2nd sighting: perkins-refcheck-rc3-3-r1 branch existed as merged debris — now 3 branches across 2 repos."
- Reasoning: ≥2 sightings, Silas dream-flagged; honest framing (anomaly + inferred root cause) — the value is the audit target, not a confirmed fix.

### G5 — `ledger pr` convention: the briefing template now carries the explicit instruction (propagating) — but STILL verify (not universal)
- Target: AGENTS.md gotchas (Ledger) · Class: **auto** (AMEND the "`set in-review` does NOT populate `pr`" gotcha)
- Change: append a 2026-08-11 addendum: the durable fix is in flight — the briefing template now carries an explicit `ledger pr <id> <url>` instruction, and the RT + PP crews are starting to run it themselves (rc3-4 #599, v2-1.1 #21 "minion set the pr field — 2nd job in a row"). BUT it is NOT universal — the RTA crew still produced a NULL `pr` on self-report (#173, #597) this window. Silas still VERIFYs `pr` on every in-review transition (`ledger show`, not the lossy table); don't relax verification just because most crews now self-set it.
- Evidence:
  - righttenantry-refcheck-rc3-4 (2026-08-10T19:05Z): "THE MINION RAN `ledger pr` ITSELF this time (convention propagated; only took 4 jobs)."
  - righttenantryagents-boundary-gate-state-fix (2026-08-10T18:23Z) + righttenantry-apply-form-scrub-fix (2026-08-10T12:54Z): "pr field was NULL (minion set in-review w/o ledger pr) — set" (the RTA miss).
- Reasoning: 5+ sightings + the durable fix, but the RTA miss proves propagation is leaky → keep the verify step.

### G6 — Serialize-hold is now standard CROSS-REPO; the briefing names the in-flight round + the release trigger
- Target: AGENTS.md gotchas (Watchers, sensors & Perkins rounds) · Class: **auto** (AMEND the serialize-hold gotcha)
- Change: append a 2026-08-11 addendum: serialize-hold is now standard ops across repos (RT ↔ PP), not just same-repo pane capacity (≥4 fresh sightings). The held round's briefing NAMES the in-flight round it's behind ("SERIALIZE-HELD behind perkins-v2-1.2-window-draw-pipe-r1") and the RELEASE trigger (the in-flight round's close-out); the held pane stays dispatched (sensor dedup'd) until release.
- Evidence: rc3-4 (behind #173), boundary-gate-state-fix r2 (behind rc3-4), rc3-5 r1 (behind #22), rc3-5-perkins-r1 briefing ("behind perkins-v2-1.2 … RELEASE when pRS's round closes") — 2026-08-10/11.
- Reasoning: the existing gotcha says "standard but undocumented" — this documents the cross-repo scope + the named-behind/named-trigger briefing shape (the durable practice).

### G7 — "settle (working->done after clean completion)" pre-emptive note is now the STANDARD close-out step
- Target: AGENTS.md gotchas (Watchers, sensors & Perkins rounds) · Class: **auto** (AMEND the settle-transition gotcha)
- Change: append a 2026-08-11 addendum: Silas now pre-emptively writes a "settle (working->done after clean completion): <summary>" note at close-out to classify the inevitable watcher settle-transition echo BEFORE it fires — the note IS the classification, so the echo that follows is note-only. The note doubles as the human-readable completion summary (PR + suite counts + what was proven). Standard, not optional (5 sightings this window: rc3-4, boundary-gate-state-fix, scrub-fix, find-stuck-terminal, sprint-replan-v2).
- Evidence: 5 "settle (working->done after clean completion)" notes 2026-08-10/11 (one per close-out).
- Reasoning: codifies the pre-emptive settle-note as the standard dedup + summary step.

### G8 — Verify merge/deploy state by commit-containment (`git merge-base --is-ancestor`), never by grepping a single file
- Target: AGENTS.md gotchas (Ledger — close-out verification) · Class: **auto** (NEW append)
- Change: add a bullet: two false-negative traps when verifying a PR/fix is in a branch — (a) grepping a single file gives a FALSE NEGATIVE if you grep the wrong file (or the change lives elsewhere); (b) checking `--merged`/ancestry BEFORE pulling lies (a stale local base predates the merge). Use `git merge-base --is-ancestor <commit> <branch>` AFTER `pull --ff-only` (or `git fetch origin <base>:<base>` when the tree is held). Commit-containment is immune to both traps.
- Evidence:
  - Gru journal 2026-08-11 (RTA #172): "verified via commit-containment, not file-grep — grepping the wrong file gave a false negative."
  - Silas journal 2026-08-10T01:02Z (rc3-3): "local develop was STALE (predated the merge) → 'NOT in --merged develop' pre-pull; post-pull it advanced. Check --merged AFTER the pull."
- Reasoning: 2 sightings, one an explicit Gru LESSON; one command, unambiguous, prevents a re-deploy/re-fix loop.

---

## Watch items (anecdotes — tracked, not proposed)

Single-sighting or below-threshold patterns with forward-relevance; not promoted (honor the ≥2 rule) but logged so a 2nd sighting promotes them next dream.

- **PP-v2 Odin toolchain traps (single-story each):** `core:testing` API form (`testing.expect(t,…)`, not `tfail`/`t.expect`); `delete(arr)` no-`&` + `new(T)` not deletable; `package core` collides with runtime core (ODN-1 gate = import-grep + `nm`, not `-build-mode:obj`); nested procs non-capturing; `make([dynamic]u8,..)` then `dyn[:]` over `make([]u8,..)`; per-tick `free_all(temp_allocator)` nukes fields read during the tick (use persistent allocator); `.odin-version` resolves to the same nightly already installed (a T2 mismatch is a real diff, not version drift). Forward-relevant to every PP-v2 story — promote on 2nd sighting. (shards C17–C22, C24)
- **Gleam/RT single-sighting traps:** `decode.null` doesn't exist (use `decode.dict`/`decode.optional(string)`); `unitest.tag` needs a STRING LITERAL (const doesn't skip under `gleam test`); Postgres JSONB re-serialises with space-after-colon + may reorder keys (use `->>'field'`, not `::text` substring); testing inline-Gleam-emitted JS under `node --test` (extract + unescape + eval the shipped literal); `instanceof Node` blind under node → `Object.prototype.toString.call`; double-scheme CTA trap (`origin_from_domain` is scheme-full; pass raw `origin_domain` to `build_entity_url`). (shards C9–C15)
- **grep tooling traps:** ERE `\|` is literal not alternation (`grep -cE "a\|b"` false-0s); macOS BSD grep has no `-P` → `perl -CSD -ne` for multibyte/codepoint search. (shards C1, C2)
- **lavish craft (single-sighting):** multi-question Decide answers arrive as compact codes (`1A,2B,3A`); empty freeform still arrives as a prompt tag (parse, don't re-prompt); lavish SVG parallel edges overlap unless fanned perpendicular; proximity-check direction oscillates (track explicit from/to); `insertBefore` on a non-child throws NotFoundError mid-`draw()` (looks "working" — verify node count). (shards C5, C42, C6; ledger C9)
- **AGENTS.md-candidate ops (single-sighting, some Silas-flagged):** briefing boilerplate "After user approval" = MERGE gate not pre-PR approval (Silas flagged for AGENTS.md — scrub-fix stalled a prod fix); `herdr tab create` lands in the wrong (focused) workspace (verify + move — Silas auto-handles inline now); `herdr pane move --label` labels the TAB not the PANE (follow with `pane rename`); temp-worktree for branch merges when main checkout dirty; re-read CURRENT transcript before any destructive kill (transient 429s self-recover); double-provider outage + Gru himself on the failing provider → `herdr notification show` is the only pane-independent channel to the user (CEO-down escalation break); latent bug → P0 when an unrelated change raises the trigger rate; `pr_review=0` ops-helper job class (PR opened, Perkins OFF, USER reviews the diff); user can pause a Perkins round by chatting its pane directly (stays `working`, route advice via Gru). (journals C2,C3,C4,C6,C9,C13; ledger C2,C4,C5,C8)
- **drive-by rename breaks a CONTRACT token (telemetry event/test id):** single incident (#173 r1 B1, codespell sed `unparseable`→`unparsable`); remedy = add the frozen word to `[codespell] ignore-words`, don't restore "standard" spelling in the token. High-leverage Perkins-blocker class — promote on 2nd sighting. (ledger C6; journals C14)
- **Bob's own dreaming-process notes** (dream-2026-08-09 shard, not yet in the consolidated store): a sheep can hit the quota wall mid-turn (check the shard FILE, not just pane status, before closing); diff the cloned store vs LIVE at pass start (store==live check). Single-source + Bob-specific — could seed a future "Dreaming (Bob)" subsection if a 2nd dream confirms them. (shards C39, C40)

---

## Pruned / rejected candidates (with why)

- **Descriptive tab labels** (journals C1): ALREADY in the playbook (lines 444–446, 544–546, 801) — user ruling, applied. No AGENTS.md action; re-proposing would duplicate canon.
- **CONTINUOUS EXECUTION policy** (journals C18): ALREADY in the playbook (line 504) as a standing user ruling. Awareness-only; the journals sheep itself flagged "no dream action needed."
- **Conflict-sensor rebase is the MINION's job** (shards C38): ALREADY in the playbook (line 655 — the conflict sensor relays "rebase onto <base>, force-push" to the minion pane). The shard author didn't realize the playbook covers it.
- **CONTINUOUS EXECUTION / lavish-loop-sequential as a proposal:** the lavish-loop-is-sequential point folds into G1 (serialize bursts) as context, not a standalone proposal.
- **Per-role model policy (3 roles)** (ledger C4): demoted to context within G2 — the existing "Model dispatch & correction ops" gotcha already covers `/model` mid-session; the per-ROLE distinction is real but thin as a standalone, and folds into the kimi-saga recovery doctrine.
- **"BFS mandate is precise not absolute" + "derived data must not be hashed"** (shards C35, C36; journals C15a): single-sighting PP canon-interpretation notes → watch. The derived-data-not-hashed rule is sound but one sighting.
- **Various single-sighting Odin/Gleam/lavish traps:** kept as watch items (above), not proposals — the ≥2 rule.
