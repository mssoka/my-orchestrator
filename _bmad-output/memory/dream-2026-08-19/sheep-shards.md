# sheep-shards — dream-2026-08-19 input

Read-only pass over 13 field-note shards newer than the dream marker
2026-08-17T17:47:09Z: dream-2026-08-17, packet-plumber-background-maps,
packet-plumber-terminal-assets-5.11, packet-plumber-v2-5.10-narrow-access,
packet-plumber-v2-5.11-terminal-types, packet-plumber-v2-5.12-aggregation-groups,
packet-plumber-v2-6.1-era-definition, packet-plumber-v2-6.2-advance-trigger,
packet-plumber-v2-7.1-visual-juice, packet-plumber-v2-7.3-accessibility-core,
packet-plumber-v2-qos-default-standard, righttenantry-security-audit,
wire-aesthetics.

Note for Bob: the adjacent-pane-id sheep kill (dream-2026-08-17, p1ZZ/p1Z0)
is already canonized in AGENTS.md (Watcher section, "CONFIRMED KILL 08-17
17:09Z") and is therefore NOT re-listed below.

---

### C1 - herdr 0.8.0 renamed `wait agent-status` — the dispatch-chain recipe in the gotchas is stale
target: AGENTS.md-gotchas
class: auto
evidence: dream-2026-08-17, 2026-08-17/18 — "`herdr wait agent-status` is GONE — it's `herdr agent wait <pane> --until idle --timeout MS` now, and it errors `agent_not_found` if the pi hasn't registered yet (sleep + retry before handing over)"
why: the chained dispatch recipe in the Dispatch & handover gotcha still names the dead command; every fresh dispatch/minion boot hits it, and the failure mode (agent_not_found at boot) needs the sleep+retry, not a re-dispatch.

### C2 - Backfilled source files defeat mtime/marker filters — read post-marker tails, never skip
target: docs/minion-field-notes.md
class: auto
evidence: dream-2026-08-17, 2026-08-17 — "files BACKFILLED after the marker ... backfilled journal files need tail reads, not skips" (recovered the undreamed 5.2 20h-minion arc)
why: marker/mtime-based incremental reads silently drop material written late into old-dated files; tail-read anything plausibly backfilled.

### C3 - Odin allocator/defer lifetime traps: never delete temp-arena slices, defer scopes to the enclosing block, never delete string literals
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-background-maps, 2026-08-18 — "the temp arena frees wholesale — never per-slice delete"; packet-plumber-v2-5.12-aggregation-groups, 2026-08-19 — "a `defer` inside an `if` runs at the if-block's end, not the proc's ... the unit test PASSED (freed memory not yet reused — silent luck)"; wire-aesthetics, 2026-08-19 — "`delete()` on a string LITERAL (not a clone) aborts — clone first"
why: three jobs in three days hit the same family — arena-interior deletes abort, block-scoped defers produce silent use-after-free that passes tests, literal deletes abort.

### C4 - Golden-image changes demand mechanical byte-level proof, never eyeball or assumption
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-7.1-visual-juice, ~2026-08-18 — "verify rlsw pixels programmatically (PIL/numpy), never eyeball" (same trap family as the R/B-swizzle; alpha and winding both diverge silently); packet-plumber-v2-5.10-narrow-access — "`cmp -l` every .log.bin vs HEAD — exactly 8 bytes @ 18..25"; packet-plumber-v2-qos-default-standard — "`harness fold-check <prev-catalog-hash> <prev-tick1>` mechanically proves a fold-only shift"; packet-plumber-v2-7.3-accessibility-core, 2026-08-19 — "proven by the full suite, never assumed"
why: four jobs this window; eyeballing misses culled triangles and 1-pixel drifts, and assumptions about byte-identity are exactly what the goldens exist to disprove.

### C5 - Rebuild the harness/binary before blessing — stale builds silently bless old code
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-7.1-visual-juice, ~2026-08-18 — "after ANY render edit, rebuild `bin/harness` BEFORE `harness save` or the bless lands on old code ... (CI caught it; a stale-bless costs a whole re-bless)"
why: a stale build cache invalidates the entire bless and only surfaces later as tiny color-only diffs in CI; rebuild-before-bless is the cheap insurance.

### C6 - Serialized state is a contract surface: append catalog entries at the END, load new cross-ref catalogs LAST, headers snapshot run-setup state
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-5.11-terminal-types, 2026-08-19 — "node_types.json array order is T1-VISIBLE ... ALWAYS append new catalog entries at the END"; packet-plumber-v2-6.1-era-definition — "catalog load-order is a test-contract surface, keep new cross-ref catalogs last"; packet-plumber-v2-6.1-era-definition — "the header MUST carry the RUN-SETUP (start) era" (else replay validates against the wrong era and latches replay_error)
why: serialized-as-index catalogs, catalog load order, and log headers all broke tests/proofs when mutated carelessly — layout changes are API changes.

### C7 - Changing a default or catalog value is never one-line: budget the ripple and grep for setups relying on the old default
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-5.10-narrow-access, ~2026-08-18 — "A catalog tier bump (narrow 5 → 10 u/s) is NOT a one-line change: it re-times every narrow-path test ... (scratch-instrument, print, re-pin — never guess)"; packet-plumber-v2-qos-default-standard — "grep lane-only setups when any default-allocation change lands" (stale lane-only tests silently sat at E7-floor rates)
why: two jobs hit default-dependent fixtures that stayed green while testing the wrong premise; the sweep of dependent setups is part of the change, not follow-up.

### C8 - A pin must structurally engage the mechanism or it is vacuous: credit-rich fixtures, real (not hand-appended) states, window-scoped counts
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-5.12-aggregation-groups, 2026-08-19 — "Concentration pins need a credit-RICH fixture ... or the pin is vacuous" (800/800 permille with AND without the weight); packet-plumber-v2-6.1-era-definition — "never hand-append Active_Crisis rows — the engine auto-resolves them" (deferral window silently collapsed); packet-plumber-v2-5.11-terminal-types — "count per-terminal spawns inside the SURGE WINDOW only (the bound formula's W is the window, the old count was whole-run)"
why: green-but-meaningless tests recurred across three jobs; before trusting a pin, verify the fixture actually exercises the code path (starved gates, auto-resolving states, and wrong-window counters all pass vacuously).

### C9 - Verify mega-minion handover delivery via the session jsonl, not pane status — three silent failure modes
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-7.1-visual-juice, ~2026-08-18 — "a kimi-quota 403 consumes the handover prompt as an EMPTY assistant turn — check the pane's session jsonl for assistant content before trusting `done`; use `herdr agent prompt` to deliver"; same shard — "`herdr pane run <pane> \"pi --model x\"` can type into a nested shell instead of the agent"; same shard — "A user-pasted image can also arrive as bare `[Image-#N]` text with no payload — grep the session jsonl"
why: nested-shell typing, quota-dead prompts, and payload-less image pastes all look like a working pane from the outside; assistant content in the jsonl is the only ground truth.

### C10 - Pane reclamation race: check pane state before re-dispatch, and weigh finishing small residual scopes in-pane
target: docs/minion-field-notes.md
class: auto
evidence: righttenantry-security-audit, 2026-08-18 — "TWO lens dispatches lost to external pane closure (mid-hunt, no file written); before a third re-dispatch, check `herdr pane get` + consider finishing small residual scopes in-pane (parent completed authn+ssr solo faster than another spawn+reclaim cycle)"
why: external pane closure can eat repeated re-dispatches; for small leftover scope the spawn+reclaim cycle costs more than finishing solo.

### C11 - Provider-cap pause protocol works when the pre-park write happens: preserve artifacts + resume-notes BEFORE parking
target: docs/minion-field-notes.md
class: auto
evidence: righttenantry-security-audit, 2026-08-18 — "preserve artifacts + write resume-notes.md BEFORE parking; the resume rode glm-5.3's return cleanly with the 5 finished lens files as head-start"
why: the pause/resume cycle is only lossless if the resume state is durable before the park; artifacts + notes are the resume.

### C12 - Briefing model lines can be 402-dead at dispatch — verify the actual model via PI_MODEL/session jsonl, never the briefing text
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-7.3-accessibility-core, 2026-08-19 — "the briefing's `deepseek/deepseek-v4-flash` model line was 402-DEAD at dispatch ... check `PI_MODEL` before trusting a briefing's model (Silas launched me on glm despite the ledger's flash field)"
why: orchestrator-side model swaps under provider outages make the briefing/ledger field stale; a minion that trusts it mis-attributes its own behavior and provenance.

### C13 - Lavish triage at scale: per-finding native controls + one batch question for the low-priority block
target: docs/minion-field-notes.md
class: auto
evidence: righttenantry-security-audit, 2026-08-18 — "per-finding native radio forms with `data-lavish-question=<id>` + one Queue button each + ONE batch question for the Low block; user triaged 47 findings in a single session, dom_snapshot verified the render, zero stranded prompts"
why: big finding lists are triaged in one session only when per-item prompts are cheap to answer and the low block is batched; verify the render before handing off.

### C14 - Structure variants for reversal from the start: legacy-inline branch + variant branch, flags-off path byte-identical and harness-proven
target: docs/minion-field-notes.md
class: auto
evidence: wire-aesthetics, 2026-08-19 — "the LAVISH GATE verdict ('ship pure straight, routing OFF, anchors OFF') turned the re-bless requirement into its opposite ... Structure every variant as a legacy-inline branch + a path-walk branch from the start (a shared path-walk that 'should be equivalent' drifted 1 pixel in estate_surge — found only because the flags-off harness run must be fully green)"
why: lavish-gate reversals are expected (canon: mid-flight reversals); a variant built as a shared "should be equivalent" path makes the reversal cost a full re-bless, while a legacy-inline branch keeps flags-off byte-identity provable.

### C15 - Deterministic render ≠ deterministic encoding: checkout unchanged regenerated artifacts so diffs stay additive
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-terminal-assets-5.11, shard undated (window 08-18/19) — "PIXEL-IDENTICAL but PNG-encoding NON-DETERMINISTIC run-to-run — after adding sprites, `git checkout` the existing PNGs so only new files + sprites.json land"
why: regen pipelines that re-encode unchanged outputs churn goldens/manifests randomly; restoring unchanged artifacts keeps every regen diff reviewable and additive.

### C16 - Odin compile-idiom traps recur: constants need a local copy to index, unused tuple destructures compile clean, #partial switch
target: docs/minion-field-notes.md
class: auto
evidence: wire-aesthetics, 2026-08-19 — "needs a LOCAL copy of the CIRCLE16 constant to index at runtime ('Cannot index a constant') — the same rule as PULSE16"; same shard — "multi-return `X, t, ok := seg_cross(...)` with `X` unused compiles clean ... don't chase it as an error"; same shard — "`#partial switch` for enums with unhandled cases, `inc[:]` to pass a dynamic as a slice"
why: the constant-indexing rule has now bitten twice (PULSE16, CIRCLE16) and the unused-destructure non-error wastes debug time if mistaken for one.

---

### ANECDOTE 1 - Structurally impossible golden → unit-pin it and say so in the PR body
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-6.2-advance-trigger, ~2026-08-19 — "an E15 crisis-block GOLDEN is impossible; unit-pin it with the test-table era 4 + the surge fixture, and say so in the PR body"
why: one-off; when the real catalog can't express a scenario, the honest move is a unit pin plus an explicit PR disclosure, not a silently skipped test.

### ANECDOTE 2 - Every view construction needs a loaded palette — palette-less view segfaults
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-7.3-accessibility-core, 2026-08-19 — "a view without a palette (the parity harness's) SEGFAULTS on the chip rect; every view construction needs a loaded palette"
why: one-off crash class from implicit view dependencies; constructors that read view fields must not assume optional members exist.

### ANECDOTE 3 - Run a brace-depth checker after multi-hunk edits
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-7.3-accessibility-core, 2026-08-19 — "a misplaced `{}` brace + a comment-merged `{` in palcheck took two full debug passes to find — run the brace-depth checker on any file after multi-hunk edits"
why: one-off; multi-hunk edit-tool changes can merge braces invisibly, and a mechanical depth check is cheaper than two debug passes.

### ANECDOTE 4 - Init/ensure must run before the early-return guard or initialization silently never happens
target: docs/minion-field-notes.md
class: auto
evidence: packet-plumber-v2-6.2-advance-trigger, ~2026-08-19 — "`era_gate_ensure` must run BEFORE the `window_ticks==0` guard or the ring never initializes (the 'fired nothing' silent bug)"
why: one-off silent-bug class: a guard placed before the ensure turns a loud misconfiguration into quiet no-op behavior.
