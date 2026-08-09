# sheep-shards findings — dream-2026-08-09

Shards read: 19 (2 orchestrator, 10 packet-plumber, 7 righttenantry; 2026-08-07..08-10).

## Candidate patterns

### `gh pr create`: always `--body-file`, never heredoc command-substitution
- Sightings: orchestrator-docs-ua1-ua2 (2026-08-07) — "backticks — bash command-substitution executes them (`node_modules: command not found`)"
- orchestrator-perkins-ops-codify (2026-08-07) — "with a trailing `| tail` breaks bash (unmatched paren / unexpected EOF)"
- righttenantry-refcheck-rc3-2 (2026-08-09) — "breaks on apostrophe-heavy bodies ('unexpected EOF')... had to `gh pr edit` a wrong test count"
- Why it matters: 3 independent sightings, 3 jobs, 2 repos, 3 days — the `--body "$(cat <<'EOF'...)"` idiom keeps biting in different ways (backticks, pipes, apostrophes). `--body-file <file>` is robust to all; also grep-verify any counts claimed in the body before pushing.
- Already in memory? no.

### "No worktree" briefings still dispatch a worktree — ground truth = pane cwd
- Sightings: orchestrator-docs-ua1-ua2 (2026-08-07) — "briefing said 'work directly in the orchestrator root (no worktree)' but the dispatch actually created a STANDARD worktree"
- orchestrator-perkins-ops-codify (2026-08-07) — "I first ran git against `/Users/moses/code` (main) and hit `fatal: branch already used by worktree`"
- Why it matters: 2 jobs same day hit the identical briefing-vs-dispatch mismatch; `pwd` + `git branch --show-current` first, run git/edits from actual cwd.
- Already in memory? partially: the 2026-08-07 "relative paths surprise in worktrees" entry + stale-briefing addendum cover adjacent ground but not the "briefing's worktree/no-worktree decision itself disagrees with dispatch" flavor — addendum candidate.

### Briefing ground-truth check extends to proper nouns, migrations, CI claims, PR citations, tool capabilities
- Sightings: righttenantry-refcheck-ad5-amend (2026-08-08) — "Gru's briefing gave the Alpha Sender ID as `RTenTRY`; the canon is `RTenantry`. I committed `RTenTRY` before Gru caught it"
- righttenantry-refcheck-rc2-3 (2026-08-08) — "the briefing's 'Migration: ALTER TYPE ... ADD VALUE skipped' was STALE — rc2-1 already added it"
- packet-plumber-narrative-messaging (2026-08-07) — "Briefing banned em-dashes 'CI-guarded', but disk shows NO em-dash CI guard"
- orchestrator-perkins-ops-codify (2026-08-07) — "it named 'RT-agent #169 N3'... disk check showed #169 has only r1"
- packet-plumber-prototype-build (2026-08-08) — "the GoPeak Godot MCP install has NO `capture_screenshot` tool (briefing said it did)"
- Why it matters: 5 new sightings across 5 jobs and both repos; the claim types keep diversifying (names, migration state, CI existence, PR/sha citations, MCP tool inventory). Grepping a briefing-supplied proper noun against canon BEFORE first commit is the new concrete move.
- Already in memory? partially: the 2026-08-07 ground-truth-first addendum ("extends to the BRIEFING itself") — these are reinforcement + new claim-type list; strengthen that entry.

### Atomic-multi-edit trap: new addenda (per-file targeting, post-bulk-rename grep, python-anchored replace)
- Sightings: packet-plumber-port-limits-canon (2026-08-08) — "one `oldText` aimed at the wrong file... rejected BOTH edits silently — check each oldText's target file"
- packet-plumber-odin-architecture (2026-08-08) — "a sed/python bulk path-rename afterwards will silently create NEW stale texts (`harness//`, misaligned ASCII diagrams)"
- packet-plumber-sprint-plan-v1 (2026-08-10) — "a 10-line Python script beats the edit tool... anchoring `.replace()` on unique substrings is robust and lets you verify with asserts"
- righttenantry-refcheck-rc3-2 (2026-08-09) — "`gleam format` reflowed split string literals... a stale oldText silently failed to match (second sighting after dream-2026-08-03)"
- Why it matters: 4 new sightings of the in-store atomicity lesson, each adding a distinct prevention (per-file batches, grep renamed tokens after bulk edits, python for fragile big blocks, re-grep after formatters).
- Already in memory? partially: core trap is the 2026-08-03 entry — fold these in as addendum bullets.

### Doc amendments: grep-bound the FULL blast radius, never infer from memory
- Sightings: packet-plumber-art-direction-amend (2026-08-08) — "'Reverse every abstract X statement' requires a grep sweep to bound ALL sites, then a scope-verify pass that nothing collateral moved"
- righttenantry-refcheck-ad5-amend (2026-08-08) — "must re-check HEADINGS/siblings of the named target... the AD-5 heading still said 'launch dependency' — a silent internal contradiction"
- righttenantry-refcheck-ad6-stoplink-amend (2026-08-08) — "my first list was non-exhaustive AND mis-attributed UX sections (I guessed '§7.4/§8.x'; the real labels were in §4.2/§6.6/§9)"
- packet-plumber-forge6-desktop-first-amend (2026-08-08) — "grep downstream docs for `FORGE #<n>` before writing ripple flags"
- Why it matters: 4 sightings, 2 repos, same day — amendments live or die on exhaustive grep of sites/headings/downstream citations; guessed section numbers are always wrong.
- Already in memory? no (edge-hunter skill is method, this is the recurring field failure).

### Match the doc's own house style / existing amendment pattern when amending
- Sightings: packet-plumber-art-direction-amend (2026-08-08) — "doc carries a 'no em-dashes' rule AND uses ` - `... MATCH it in additions - grepping for `—` first (0 hits) confirmed"
- packet-plumber-forge6-desktop-first-amend (2026-08-08) — "the forge doc already had an amendment pattern... matching the in-doc precedent keeps canon self-consistent; don't invent a new amendment format"
- Why it matters: 2 sightings same crew/day; canon docs stay self-consistent only if amendments clone the doc's own conventions (dash style, inline-tag format, log entry shape).
- Already in memory? no.

### Surface judgment calls and out-of-scope consequences explicitly — never silently decide
- Sightings: packet-plumber-art-direction (2026-08-07) — "a sibling canonical doc that flips a decision's evidence: SURFACE it and use veto power rather than silently deferring"
- packet-plumber-art-direction-amend (2026-08-08) — "Literalized it conservatively + flagged it in the PR's Decisions & rationale as a one-line-revert - better than silently dropping"
- righttenantry-refcheck-ad5-amend (2026-08-08) — "an in-scope change has a load-bearing out-of-scope consequence: flag + escalate, don't silently expand scope and don't silently leave the gap"
- Why it matters: 3 sightings, 2 repos — the conservative-resolve + prominent-flag move is becoming the house norm for ambiguity at a scope edge.
- Already in memory? no.

### Lavish verdict ground truth = `~/.lavish-axi/state.json` (sessions.<id>.chat) — confirmed twice more
- Sightings: packet-plumber-blender-art (2026-08-08) — "the poll's `prompts[]` usually delivers, but session-end can strand a queued message... state.json chat is ground truth"
- packet-plumber-narrative-messaging (2026-08-07) — "user verdict was a terse 'read good.' + Send&End... confirmed via ~/.lavish-axi/state.json `sessions/<id>/chat[].text` (no stranded prompts)"
- Why it matters: 2 new independent confirmations of the 2026-08-03 stranded-prompts entry; the exact lookup path (`sessions.<id>.chat`) is now attested.
- Already in memory? partially: 2026-08-03 entry — add the concrete state.json path + "verify BEFORE acting on a load-bearing decision" framing.

## Singletons (interesting but seen once)

- packet-plumber-blender-art (2026-08-08): NEVER `bpy.ops.wm.read_factory_settings()` via BlenderMCP — reloads the addon, kills the :9876 server thread, chicken-and-egg dead (user must toggle the addon). Delete default objects instead. High-value if Blender jobs recur.
- packet-plumber-blender-art (2026-08-08): Blender 5.2 compositor = node-GROUP API (`scene.compositing_node_group`, `NodeGroupOutput`, interface sockets; Glare settings are input-socket display-name strings `'Bloom'`/`'High'`); disable = set group to `None` (`use_nodes=False` doesn't stick — stale Glare group blew a render to white); Eevee has no bloom since 4.2 → compositor Glare; Standard view transform keeps canon hex (AgX desaturates); emissive >1 clips toward white.
- packet-plumber-blender-art (2026-08-08): gable-roof ridge along Y so the gable-END faces a -Y camera; in-scene text rotated X 90° or it foreshortens.
- packet-plumber-prototype-iterate-1 (2026-08-08): macOS offscreen windows freeze their compositor — in-game captures repeat the FIRST frame forever (diff frame hashes!); movie mode (`--write-movie --fixed-fps`) is the reliable capture path. REFINES the in-store 2026-07-31 windowed-offscreen lesson (see stale section).
- packet-plumber-prototype-build (2026-08-08): `--position -32000` is outside the renderable desktop (viewport never clears, ghosted text) — `-3000,-3000` stands; `describe_image` is the only eyes, flaky, ~1 image per call — retry.
- packet-plumber-prototype-iterate-1 (2026-08-08): snapshot/signal emit re-enters its handler synchronously — a hook that submits on `snap.tick==X` recurses to stack overflow; guard one-shot.
- packet-plumber-prototype-iterate-1 (2026-08-08): validate wiring against the REAL bootstrap path — headless harness passed balance explicitly, masking `PacketFlow.new()` without it (knobs silently defaulted in-game). Generalizes: harness-supplied config can mask production bootstrap gaps.
- packet-plumber-prototype-build/-iterate-1 (2026-08-08): game-feel cluster — SLA/loss must be a ROLLING window (~10s), not cumulative-from-tick-0; latency is an SLA metric, never a drop trigger; cosmetic vis_dist advances only when a packet is served (congestion piles visibly); weighted-random sink spread is lumpy on small sets (audit per-leg capacity vs the lump, not the mean); reservation heuristics must fall through to fallback candidates; map growth cascades balance constants (budget/surge/queue all retuned 4→9 houses).
- packet-plumber-sprint-plan-v1 (2026-08-10): terse/ambiguous lavish verdicts — paraphrase back ("reading you as X — confirm?") BEFORE a sweeping change; a misread one-liner cost a flip across 8 locations + full revert. Pairs with the 2026-08-03 provenance entry.
- packet-plumber-sprint-plan-v1 (2026-08-10): vanilla `marked --gfm` emits NO heading ids — inject slugged ids before building a TOC. Lavish-craft addendum. Also: bash tool cwd resets to repo root EVERY call — `cd` in the same command (bit ~5×).
- packet-plumber-art-direction (2026-08-07): worktree can be stale vs origin/main (sibling PR landed your source docs after branch cut) — `git log HEAD..origin/main` + rebase before opening the PR.
- packet-plumber-art-direction (2026-08-07): `game/data/*.json` uncommitted — uncommitted local files are not canonical, and never commit data owned by another job from your PR.
- packet-plumber-port-limits-canon (2026-08-08): packet-plumber decision-log requires provenance (dated entry + inline tag, house style `(*...*)` / `[RULING — user, DATE]`) — repo canon rule.
- righttenantry-per-applicant-remind (2026-08-08): gleeunit prints dots only — "N passed" doesn't prove a NEW test ran; break-and-revert probe (flip one assertion, confirm exactly 1 failure at your path, revert). Generalizes to any terse runner.
- righttenantry-per-applicant-remind (2026-08-08): RT em-dash CI scans only `copy.toast/page(code,ctx)` — new copy fns with other signatures escape the guard (coverage-gap flavor of the in-store Perkins N3/W1 entry); macOS grep has no `-P` — python `'\u2014' in line`.
- righttenantry-per-applicant-remind + rc2-2 (2026-08-08): Squirrel regen churn addendum — reflows BOTH `application/sql.gleam` AND `ai/sql.gleam`; `gleam format` is the canonical arbiter (reverted a pog.array hunk), revert all churn not yours. Extends the in-store Squirrel triple-trap.
- righttenantry-refcheck-rc2-2 (2026-08-08): adding an enum value touches 6+ compile-forced match sites across 3 packages — grep `case` on the type everywhere, then reason about each DEFAULT arm (`is_non_terminal` differs by context); two status pills had DRIFTED — the brand doc is the arbiter, not either component.
- righttenantry-refcheck-rc2-3 (2026-08-08): pgo rejects text→bool casts (`$n::boolean`) — inline boolean literals; `Ok(pog.Returned(_, [row]))`+`[]` not exhaustive — `Ok(_) ->` catch-all for INSERT...RETURNING.
- righttenantry-refcheck-rc3-1 (2026-08-09): gleam `uri.percent_encode` leaves `+` unencoded → means space in form bodies — re-encode `+`→`%2B` for E.164 numbers (latent same bug in stripe_client.form_encode); `request.get_header` returns `Result(String, Nil)` not Option.
- righttenantry-refcheck-rc3-1 (2026-08-09): test-DB port contention 3rd sighting (54321 held by sibling worktree; isolated :54324) — reinforces the in-store 2026-07-31 entry.
- righttenantry-refcheck-ad6-stoplink-amend (2026-08-08): link scanners/preview fetchers GET every URL — for non-recoverable terminal actions (objection), spec GET-renders-confirm + POST-mutates, never GET-mutates. Durable web-security pattern, one sighting.
- righttenantry-refcheck-ad6-stoplink-amend (2026-08-08): hunter false positive on `terminal_reason` — verify schema-slug findings against the mapping section before crediting (instance of in-store verify-mechanism lesson).
- righttenantry-refcheck-rc3-2 (2026-08-09): amendment registers supersede WITHOUT rewriting in place — UX §6.3/§6.4 and epics AC still say "Reply STOP"; read the register FIRST, resolve briefing compressions against the source sections.
- packet-plumber-odin-architecture (2026-08-08): lavish mid-form user QUESTION (freeform, not a radio) = answer in next --agent-reply AND rebuild the form with the new options. Extends the in-store question-forms craft entry. Also version-pin realism: "'PCG64-XSH-RR' doesn't exist... reviewers WILL check" — get version/API facts exactly right in canon docs.
- packet-plumber-narrative-messaging (2026-08-07): cross-check every copy sample against locked MECHANICS, not just tone — "DROPPING" violated the zero-drops banking SLA (caught by self-review).

## Stale/contradicted memory candidates (with where)

- `minion-field-notes.md` 2026-07-31 (finlit crew): "captures must run WINDOWED off-screen (`--position -3000,-3000`)" — REFINED, not wrong: prototype-build confirms `-3000,-3000` (and that `-32000` is outside the renderable desktop), but iterate-1 found macOS offscreen windows freeze the compositor so captures repeat the first frame forever; movie mode (`--write-movie --fixed-fps 60`, frames via ffmpeg) is the reliable path. Recommend amending the entry to: windowed offscreen for one-shots, movie mode for anything sequence/verification-grade, and diff frame hashes to detect freeze.
- No outright contradictions found. The ground-truth-first/briefing entry (2026-08-07 addendum), atomic-edit entry (2026-08-03), lavish stranded-prompts entry (2026-08-03), Squirrel triple-trap (2026-07-31), test-DB port entry (2026-07-31), and question-forms craft entry (2026-07-31) all gained reinforcing sightings — addendum material, not corrections.
