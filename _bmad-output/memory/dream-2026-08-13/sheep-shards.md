# Sheep findings — field-note shards (dream 2026-08-13)

## Candidate patterns

### C1 — Stale briefing claims: verify ground truth before trusting ACs/carry-forwards
- Suggested target: playbook (briefing hygiene / carry-forward rules)
- Evidence (×5 sightings, both repos):
  - righttenantry-refcheck-rc3-6 (2026-08-11): "ALWAYS grep the architecture amendments register + the deployed code (router.gleam) for the amended behaviour before trusting a briefing AC"
  - packet-plumber-v2-2.2-ecmp (2026-08-11): "A briefing carry-forward claimed "T2 pixel-unverified until the rlsw harness exists" — STALE (ground-truth first: the goldens/ pixel dirs + the shadow build disproved it)"
  - packet-plumber-v2-harness-ecmp-demo (2026-08-12): "Verify the actual repo state before rebuilding infrastructure; the briefing's deferral narrative was stale."
  - righttenantry-refcheck-rc4-1 (2026-08-12): "the briefing's em-dash "CI ban" was again false on disk (keep the §8.1 canon copy verbatim)"
  - righttenantry-refcheck-rc4-4 (2026-08-13): "Always grep the DB enum migrations, not the briefing, for the emitted set."
- Why it matters: briefing carry-forwards rot fast; every job here (both repos) lost time to a stale claim a 2-minute grep would have caught.

### C2 — Absolute-path edit trap: minions edit the MAIN checkout, not their worktree
- Suggested target: AGENTS.md gotchas
- Evidence:
  - packet-plumber-v2-2.2-ecmp (2026-08-11): "the absolute-path trap bit AGAIN … so all 3 edits landed in the main checkout, worktree clean. `odin test`/`lint`/`harness` all `cd`'d to the main checkout too, so they passed against the WRONG tree. FIX: resolve every edit to the WORKTREE path … after edits, `git status` from cwd BEFORE trusting a green test run."
- Why it matters: green gates on the wrong tree are the worst kind of false confidence; "bit AGAIN" = recurrence (reinforces the 2026-08-11 field note).

### C3 — Batch edit-tool silent rejection on indentation mismatch
- Suggested target: AGENTS.md gotchas
- Evidence:
  - packet-plumber-v2-2.3-demolish (2026-08-12): "the edit-tool nested-switch trap bit again — a 5-edit batch to `harness/demo.odin` was REJECTED SILENTLY (all 5 lost) because ONE oldText had shallow indentation for a 3-level-deep switch … the tool reports the failed edit index but applies NONE on a mismatch."
- Why it matters: one bad oldText silently discards the whole batch; "bit again" = recurrence.

### C4 — PP determinism spine: derived-not-serialized, absent-when-empty, prove-before-bless (×6 sightings)
- Suggested target: docs/minion-field-notes.md (PP canon)
- Evidence:
  - packet-plumber-v2-2.1-bundles (2026-08-11): "Zero serialized-state change → slice-1 T1 hashes + T2 pixels both byte-identical, no re-bless."
  - packet-plumber-v2-2.2-ecmp (2026-08-11): "the routing table is DERIVED (not serialized) … Net: purely additive, no re-bless."
  - packet-plumber-v2-3.5-node-placement (2026-08-12): "Catalog edits are GOLDEN-POISONED in PP v2 … Wire new rules as core consts … until a legitimate re-bless"
  - packet-plumber-v2-3.5-node-placement (2026-08-12): "LOG_VERSION bumps … force a golden-log re-bless — do it as `harness save` for ALL demos, then byte-verify every `.log.bin` differs ONLY in the version field"
  - packet-plumber-v2-3.2-lane-qos (2026-08-13): "Prove behavioral identity BEFORE blessing … Flag loudly in the PR; don't halt." + "T1-dump additions must be ABSENT-WHEN-EMPTY, not just sparse (a zero count still shifts every default-run hash)."
  - packet-plumber-v2-4.1-warning-forecast (2026-08-13): "Golden re-blesses: every `.t1`/`.log.bin` shifts on any balance.json content change (catalog_hash fold, the 3.2 precedent)"
  - packet-plumber-v2-1.4-win-lose-stub (2026-08-11): "it MUST thread through BOTH `run_demo` (live) + `replay_hashes` (replay) … miss any caller and ODN-11 replay diverges at the terminal tick."
- Why it matters: the single most-repeated PP lesson — this discipline (derived state, no re-bless, prove first) is what every story had to rediscover.

### C5 — Odin temp-allocator trap: `fmt.tprintf` strings die at the tick boundary
- Suggested target: docs/minion-field-notes.md
- Evidence (×2 sightings):
  - packet-plumber-v2-harness-ecmp-demo (2026-08-12): "Odin `fmt.tprintf` = temp allocator, `fmt.aprintf` = default — the harness tick loop's per-tick `free_all` silently frees ANY tprintf string that must outlive the iteration … In-loop failure strings must be `fmt.aprintf`."
  - packet-plumber-v2-3.2-lane-qos (2026-08-13): "`fmt.tprintf` has NO allocator param on the dev-2026-08 pin (use `fmt.aprintf(..., allocator = context.temp_allocator)` for per-frame HUD strings)"
- Why it matters: silent blank-garbage failures that only surface on never-run error paths (T2 failure strings were garbage the first time the path ran).

### C6 — Silent no-ops / silent rejections: verify by observable effect, never reported success (×5 sightings)
- Suggested target: docs/minion-field-notes.md
- Evidence:
  - packet-plumber-v2-3.4-sla (2026-08-12): "a `narrow` pipe draw is silently REJECTED (max_span 10) → no route → packets pile at their source with zero events; for narrow-tier tests, spawn nodes ≤10 tiles apart. Cost me a debug probe cycle."
  - packet-plumber-v2-4.2-surge-crisis (2026-08-13): "a "fix" that adds pipes to a full router silently rejects (Router_Ports_Full → replay_error latched) — swap (demolish-then-draw) or size the healthy fixture to 2 pipes/side"
  - packet-plumber-v2-4.1-warning-forecast (2026-08-13): "Odin `strings.replace` in a test can return "replaced=true" while the runtime doc still holds the old substring … pin multi-line replace1 rows via single-line anchors or byte-verify"
  - packet-plumber-v2-4.1-warning-forecast (2026-08-13): "test-catalog `Balance` fields MUST mirror data/balance.json (zeroed `warnings` thresholds made zero-load read as 🔴 — every node red at tick 1, silently shifting every dump)"
  - righttenantry-refcheck-rc1-1-grapheme-fix (2026-08-12): "grep the file after the revert; the UA path survived my first revert and silently kept the fix."
- Why it matters: cross-repo; sim, test fixtures, and tooling all have silent no-op paths — the fix is always an observable-effect check, not the success return value.

### C7 — Vacuous-green assertions and negative controls
- Suggested target: docs/minion-field-notes.md
- Evidence (×3 sightings):
  - righttenantry-refcheck-rc4-1 (2026-08-12): "a `string.contains(body, "\"referee_ip\"")` assertion is vacuously green while the IP is on the wire. Assert both forms; prove with a neutralize-the-strip → red negative control."
  - righttenantry-refcheck-rc4-2 (2026-08-12): "`list.all([])` is vacuously True — emptiness must be checked BEFORE the all-terminal branch (the pre-trigger sub-line bug)."
  - righttenantry-refcheck-rc3-7 (2026-08-12): "Unit tests pass because they check gleam's compact `json.to_string` output directly; integration tests read Postgres jsonb and need decode-based asserts."
- Why it matters: tests that pass vacuously are the most expensive false green; the standard fix (assert both forms + a red negative control) emerged twice independently.

### C8 — Cross-boundary string representation mismatch (DB stores strings differently than the app produced)
- Suggested target: docs/minion-field-notes.md
- Evidence (×3 sightings):
  - righttenantry-refcheck-rc1-1-grapheme-fix (2026-08-12): "Gleam `string.slice` counts GRAPHEMES while Postgres `length()` counts CODEPOINTS — codepoint-bounded slicing … is the only cut that guarantees a DB CHECK `length() <= N` holds"
  - righttenantry-refcheck-rc4-4 (2026-08-13): "PG `::text` uses a space separator, the sweep stamps RFC3339 `T` — space (0x20) < 'T' (0x54) sorts the evening before the morning. Server-built timeline must normalise space→T before sorting"
  - righttenantry-refcheck-rc3-7 (2026-08-12): "Postgres `jsonb::text` adds a space after `:` … substring-contains checks on STORED fraud_signals fail; parse + decode the field instead."
- Why it matters: three flavors of one trap — slice/sort/contains on DB-stored text must use the DB's representation, not the app's.

### C9 — Test-DB port contention across sibling worktrees; spin your own container
- Suggested target: docs/minion-field-notes.md
- Evidence (×2 sightings):
  - righttenantry-refcheck-rc1-1-grapheme-fix (2026-08-12): "Test-DB port 54321 is contended across sibling worktrees — spin your own `postgres:16-alpine` container on a free port"
  - righttenantry-refcheck-rc4-4 (2026-08-13): "Integration suite on own container (:54328) — the sibling worktrees own 54321/54326/54327/54332-34"
- Why it matters: hardcoded 54321 is a standing trap with parallel RTA worktrees alive; own-container is now the proven standard.

### C10 — Squirrel regen churn: revert ai/sql.gleam + application/sql.gleam, verify each hunk
- Suggested target: docs/minion-field-notes.md
- Evidence (×2 sightings):
  - righttenantry-refcheck-rc3-7 (2026-08-12): "Squirrel regen churns `ai/sql.gleam` + `application/sql.gleam` (blank-line + pog.array reflow) on EVERY run — revert both to HEAD after each regen when your SQL lives in `reference_checks/`"
  - righttenantry-refcheck-rc4-4 (2026-08-13): "Squirrel regen churns `application/sql.gleam` formatting hunks unrelated to new columns (reverted one) + `ai/sql.gleam` whitespace (revert whole file); verify each hunk before keeping."
- Why it matters: every RTA SQL change risks shipping unrelated churn; the revert-then-verify step should be boilerplate.

### C11 — Correction/retry loops: corrected_at boundary + attempt reset (×3 evidence pieces, 2 jobs)
- Suggested target: docs/minion-field-notes.md (generalizes beyond RTA: any retry/cadence loop)
- Evidence:
  - righttenantry-refcheck-rc4-3 (2026-08-12): "For retry/cadence loops, RESET the attempt counter (and capability token) on re-queue — a step-dispatched sweep reads attempt_count, and a corrected row at count 1 dead-ends in the co-nudge step forever."
  - righttenantry-refcheck-rc4-3 (2026-08-12): "gate post-loop failures on the CORRECTION instant (a `corrected_at` column …): stale/redelivered pre-correction events must stand down, never fabricate a fraud signal."
  - righttenantry-refcheck-rc4-4 (2026-08-13): "correct_reference_call resets attempt_count to 0, so batch index alone mislabels the re-invite as "Reminder N" — segment send batches by corrected_at boundary."
- Why it matters: three adjacent bugs from one missing invariant — the correction boundary must segment everything downstream (attempt counts, batch labels, failure gating).

### C12 — Sticky latches, admission-time truth, terminal rows (×3 sightings, both repos)
- Suggested target: docs/minion-field-notes.md
- Evidence:
  - packet-plumber-v2-3.4-sla (2026-08-12): "the Loss latch must be sticky-Enter by contract; "monotone" applies to the counter, never the ratio."
  - packet-plumber-v2-4.2-surge-crisis (2026-08-13): "make the drop event carry its shed bundle (admission-time truth) + add resolve hysteresis (bound−margin + no-drop + no-bound-lane) or the trigger/resolve pair fires every few ticks on any marginal network."
  - righttenantry-refcheck-rc3-7 (2026-08-12): "any "stamp on creation" that writes a denormalised column must respect terminal rows — submission is terminal, so the submitted snapshot is never recomputed."
- Why it matters: same architectural truth in sim + app: derived/triggered state must latch at admission and never recompute from later, diluted state.

### C13 — Harness build path: tools/harness.sh only (bare build = R/B-swapped frames)
- Suggested target: docs/minion-field-notes.md
- Evidence (×2 sightings):
  - packet-plumber-v2-4.2-surge-crisis (2026-08-13): "Build the harness ONLY via tools/harness.sh (ODN_ROOT=the rlsw shadow) — a bare `odin build harness` links the stock GPU raylib and produces R/B-swapped golden frames (921600/921600 pixel diffs) that look like a render bug."
  - packet-plumber-v2-2.2-ecmp (2026-08-11): "rlsw is gitignored, so it's ABSENT in a fresh worktree — point the harness build at the main checkout's shadow: `ODIN_ROOT=<main>/tools/raylib-sw/shadow odin build harness -out:bin/harness`"
- Why it matters: hours of chasing a phantom render bug that was just the wrong build script (gitignored dep absent in fresh worktrees).

### C14 — Vision model unreliable at sub-5px resolution; measure goldens programmatically
- Suggested target: docs/minion-field-notes.md (orchestrator tooling lesson)
- Evidence:
  - packet-plumber-v2-2.1-bundles (2026-08-11): "The vision model was UNRELIABLE at this resolution (hallucinated text + missed the 2px diff) — measure goldens programmatically (PIL pixel diff + thickness count), don't trust describe_image for sub-5px render differences."
- Why it matters: calibrates when to trust vision-based review vs pixel-diff tooling — a harness-level tool-choice lesson.

### C15 — Minion-run pre-PR self-review (edge-case hunter / 2-hunter swarm) catches real bugs — make standard
- Suggested target: playbook (review loop) or docs/minion-field-notes.md
- Evidence (×2 sightings, both repos):
  - righttenantry-refcheck-rc4-1 (2026-08-12): "an edge-case-hunter self-review before the PR paid off 4 real fixes (vacuous strip guard, hooks-vs-wire status divergence on unknown enum values, non-forward-tolerant decoder, corrupt-result read failure)"
  - packet-plumber-v2-3.3-contention (2026-08-13): "The 2-hunter review swarm caught it; verify bidirectional traffic visually in the blessed captures."
- Why it matters: both repos independently report the cheap pre-PR self-review catching real bugs before Perkins — cheap and proven.

### C16 — New route path families need their OWN registry arms; verify per family
- Suggested target: docs/minion-field-notes.md
- Evidence:
  - righttenantry-refcheck-rc3-6 (2026-08-11): "New POST routes at a NEW top-level path family (`/webhooks/*`, not `/api/v1/webhooks/*` …) need their OWN registry arms — the existing `["api","v1","webhooks",..]` CSRF prefix did NOT cover them (a missing arm 403s). Verify each registry (is_public_path / CSRF / redact_token_route) against disk per route family; don't assume the existing arm covers a new prefix."
- Why it matters: a 403 that masquerades as auth misconfig; the briefing's "register in all three registries" is per-arm but which arms apply is per-route-family.

### C17 — Signed-URL webhook contracts: reconstruct from consts, never from request Host
- Suggested target: docs/minion-field-notes.md
- Evidence:
  - righttenantry-refcheck-rc3-6 (2026-08-11): "Twilio status callback path is a LIVE CONTRACT fixed in `sms_client.gleam` … the X-Twilio-Signature signs that EXACT URL (base + path), so the verifier must reconstruct it from `TWILIO_STATUS_CALLBACK_BASE_URL` + the const, not from the request's own Host/URL (proxy host mismatch fails verification, never silently passes)."
- Why it matters: signature verification fails behind proxies in a way that looks like auth errors — the reconstruction source is the whole bug.

### C18 — Deferred multi-removal by index: sort ascending before descending splice
- Suggested target: docs/minion-field-notes.md
- Evidence:
  - packet-plumber-v2-3.3-contention (2026-08-13): "a deferred-splice (collect drop indices in a pass, splice after) needs an ASCENDING sort before the descending splice — the drops list is in APPEND order, and removing a lower index first shifts the higher ones (two same-tick sheds [11,9] silently spliced the WRONG packet … goldens already blessed with the bug had to be re-blessed). Any new deferred-multi-removal in core: sort-then-descending + a same-tick-double-shed regression test."
- Why it matters: the classic index-shift bug shipped into blessed goldens — the called-for regression test is a transferable recipe.

### C19 — Grep-based gates false-positive; strip comments and back with behavioral pins
- Suggested target: docs/minion-field-notes.md
- Evidence (×2 sightings):
  - packet-plumber-v2-2.1-bundles (2026-08-11): "The no-LB grep-gate (lint gate 5) must strip `//` comments BEFORE grepping, or the prohibition's own explanatory prose … false-positives. Strip with `sed 's://.*::'` per file, then grep code-only."
  - packet-plumber-v2-2.2-ecmp (2026-08-11): "a naive Perkins grep for `splitmix64` in routing would false-positive — the real guard is "no rng_next/rng_range/state.rng in the routing path", backed by a behavioral test"
- Why it matters: static grep gates are only as good as their comment-stripping + the behavioral test behind them — matters for lint gates AND Perkins review greps.

### C20 — Gleam/Lustre trap cluster (×4 evidence pieces, 3 jobs)
- Suggested target: docs/minion-field-notes.md (RTA language cheat-sheet)
- Evidence:
  - righttenantry-refcheck-rc4-2 (2026-08-12): "gleam 1.15.1 parser REJECTS `++ [list-literal]` ("operator has no value on its right side") — use `list.append`/spread; the repo never uses `++ [`."
  - righttenantry-refcheck-rc4-3 (2026-08-12): "an EMPTY-STRING attribute value is a PRESENT boolean attribute (`attribute("disabled", "")` ships permanently-disabled buttons)"
  - righttenantry-refcheck-rc4-3 (2026-08-12): "a case-clause body starting with `let` is a parse error unless braced; no function calls in clause guards; no list `..` spread in this Gleam version (use `list.append`)"
  - righttenantry-refcheck-rc4-4 (2026-08-13): "Gleam guards can't call functions — nested `case string.compare(...) { Gt if ... -> ... }` with `import gleam/order.{Gt}`."
- Why it matters: a growing list of non-obvious traps (esp. the silently-wrong empty-attribute case) that each cost a debugging cycle; worth one consolidated cheat-sheet entry.
