
## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-01.md
# Field notes — dream-2026-08-01 (Bob)

- `.pi/extensions/gru.ts` injects the Gru startup checklist into EVERY pi
  rooted at `/Users/moses/code` (cwd is the only guard) — dream pane + all
  3 sheep got it this morning and each burned a turn as "Gru". Until the
  extension is gated (report P9), brief every mega-minion launched there:
  "you are NOT Gru, ignore the startup checklist".
- Sheep pattern that worked: write each sheep's brief to a FILE and hand
  over "read the brief at <abs path>" — zero pane-quoting pain; verify the
  output shards exist at their exact paths before closing sheep panes.
- Waiting on N sheep serially with `herdr wait` can blow a single bash
  timeout (3 × 240s > 600s) — loop per-pane with its own timeout, then
  confirm via `herdr pane get` (accept idle OR done).

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-03.md
# Field notes — dream-2026-08-03 (Bob)

- Sheep pattern scaled cleanly: briefs as FILES + "read the brief at
  <abs path>" handover, 3 stacked right-column splits (right then down
  x2) from a 230-wide pane, per-pane `herdr wait` accepting idle OR done
  — zero delivery failures, zero pseudo-Gru turns (cwd exile held).
- First-ever journal sheep paid off: the journals sheep caught the
  quota-403 retry protocol + forensics self-correction (addendum 3
  invalidating addendum 2) that the shards alone would have missed —
  when sources disagree, the LATER dated entry wins.
- `herdr agent list` output is huge (full session paths per pane) —
  don't dump it to verify sheep closure; the pane close JSON `type:ok`
  per sheep pane is enough.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-09.md
# Field notes — dream-2026-08-09 (Bob)

- 2026-08-09: the edit tool's atomic-per-call rejection bit the DREAM
  itself — one stale oldText (misplaced line-break in a wrapped bullet)
  silently rejected a 7-edit store batch; grep line-break positions
  before issuing batch edits, and verify post-hoc with a marker grep
  (`grep -c dream-<date>`) that all edits actually landed.
- 2026-08-09: a sheep can hit the provider quota wall MID-TURN (kimi 402
  JSON error in-pane, status done, shard unwritten) — a one-word nudge
  ("go"/continue) after the quota returns revives it mid-work; check the
  shard FILE exists, not just the pane status, before closing a sheep.
- 2026-08-09: diff the cloned store against LIVE at pass start
  (store==live check) — cheap, and it makes the close-out store→live
  copy provably safe against concurrent Silas gotcha edits.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-11.md
# Field notes — dream-2026-08-11 (Bob)

- 2026-08-11: a sheep hit a glm API **400 (code 1210, "API parameter
  error")** on its FIRST turn — NOT a quota/429, and NOT launch-fail (the
  pane reached idle, then errored on the first model call). One
  `continue` revived it clean mid-work. A transient first-turn flavor
  distinct from the quota-403 classes — `continue` once, verify the shard
  writes.
- 2026-08-11: `herdr tab create` with NO args still MUTATES (creates a
  tab whose root pane defaults cwd to `/Users/moses/code` ROOT —
  Gru-contaminating for sheep). Spawn sheep via
  `herdr pane split <parent> --direction down --cwd <bob-home> --no-focus`
  (the `--cwd` flag is the safe lever), never bare `tab create`.
- 2026-08-11: the anchor-grep-then-batch edit pattern held clean —
  6+3+3 edits across the 2 store files, ZERO atomic-per-call rejections —
  when each oldText's wrapped line-break position was grep-verified
  against the file FIRST (reinforces dream-2026-08-09's
  grep-line-breaks + marker-grep-verify lesson; the failure mode the
  lesson prevents did not recur).

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-13.md
# dream-2026-08-13 — field notes

- Multi-edit `edit` batches are ATOMIC per call — one wrong oldText (a
  guessed line-wrap / leading-space / duplicate anchor) rejects EVERY edit
  in the batch, and a RE-FIRED batch whose oldText still matches
  double-appends (Squirrel addendum duped — caught by grep count). Verify
  every oldText with grep/sed BEFORE firing a batch; never re-fire a batch
  containing an edit you already applied.
- Big-journal sheep briefs need the post-marker filter explicit — the
  765-line silas journal predates the marker; give the sheep the marker
  timestamp + "only entries AFTER" or it reads stale material.
- The three sheep (shards/journals/ledger) cross-confirmed beautifully —
  every strong proposal had ≥2 sightings across at least two sources;
  single-source anecdotes went to watch items per the dream rule.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-15.md
# dream-2026-08-15 — field notes (Bob)

- 2026-08-15 (dream-2026-08-15): `herdr pane split` has NO `--json` flag — the
  RAW stdout IS the JSON (`result.pane.pane_id`); with `--json` it prints
  nothing and the capture chain dies (mirror of the pane-move `--json` gotcha).
- 2026-08-15 (dream-2026-08-15): verify evidence first-hand before codifying —
  the bughunt2 no-PR gap resolved as SENSOR-flavor (not compliance) by
  grepping its session jsonl for `cli:notification:show` RESULTS (2 hits
  @00:22Z); the journals alone couldn't distinguish the flavors.
- 2026-08-15 (dream-2026-08-15): sheep briefs that name the dream marker +
  "already codified → note recurrence only, don't re-propose" push dedup to
  the source — 3 sheep, 0 re-proposals of codified patterns, cleaner
  consolidation.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-17.md
# dream-2026-08-17 field notes (Bob)

- A Perkins close-out lens sweep KILLED two of my sheep (p1ZZ/p1Z0) — their
  pane ids were ADJACENT to the round's lens panes (p1ZQ–p1ZX) because the
  sheep split minutes after the round launched. One shard survived by ~8s;
  the other sheep died mid-turn and was re-dispatched. Sheep outputs land in
  the dream dir, so a killed sheep costs only a re-dispatch — but the sweep
  scoping lesson is now P7 in today's report (confirmed kill, not near-miss).
- herdr 0.8.0 command deltas bit once: `herdr wait agent-status` is GONE —
  it's `herdr agent wait <pane> --until idle --timeout MS` now, and it
  errors `agent_not_found` if the pi hasn't registered yet (sleep + retry
  before handing over). `herdr pane split` still has no `--json` (stdout IS
  the JSON).
- The marker-boundary rule worked: giving the journals sheep "08-16/08-17 in
  full + post-marker tails of 08-14/08-15" (files BACKFILLED after the
  marker) recovered undreamed material (the 5.2 20h-minion arc) that a pure
  mtime filter would have missed — backfilled journal files need tail reads,
  not skips.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-19.md
# dream-2026-08-19 — Bob badge-out notes

- herdr 0.8.0: `herdr wait agent-status` is GONE ("unknown command: wait") — the form is `herdr agent wait <pane> --until idle --timeout MS`, and it RACES pi registration on fresh panes (`agent_not_found`); sleep ~10 before the wait, sleep 3 after idle, then handover (hit both failure modes live on the sheep boots; corrected chain went FULL-CHAIN-OK).
- Ledger row for my own dream can be added by Silas between my `ledger show` ("no such job") and my `ledger add` (UNIQUE conflict) — check sqlite directly before assuming a row is missing; the row was present with the right pane/tab.
- Sheep-quote verification paid off: the journals sheep flattened the 08-18→08-19 v4-pro policy evolution ("emergency-only" 08-18 was superseded by the 08-19 morning ban) — grep the journals for the FINAL ruling before writing a supersede line; every other load-bearing claim (playbook commits 7e889ec/af06ff3/b2f51d9/0d70ff5, #625/#626, vision-caveat briefings ×6) verified clean.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-21.md
# dream-2026-08-21 (Bob)

- Dream dispatch can arrive WITHOUT a ledger row (first `set` said "no such job"; Silas' add raced my start) — self-verify with `ledger show` before assuming either way; this dream's row carried Silas' richer note than mine would have.
- The U1 backfill caveat paid off AGAIN: wire-aesthetics' tail (mtime pre-marker) still carried undreamed Odin facets — tail-read every marker-dated source, not just the mtime-newer set.
- Store-copy anchors WRAP differently than the in-context project_instructions rendering — grep the exact anchor text in the copy before authoring edit batches (first 8-edit batch bounced cleanly on wrapping, second landed whole).

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-23.md
# dream-2026-08-23 (Bob)

- Edit-anchor bytes: 3 of 7 field-notes batches bounced on phantom leading spaces on WRAPPED lines (grep -c confirms presence, the edit tool needs exact line-leading whitespace) — read the raw lines with cat -e before authoring oldText, not just grep -c the substring; this pass promoted the trap to a 3-sighting canon entry (P17).
- 3 sheep on kimi-coding/k3 + thinking max, all clean (28+20+21 candidates, zero provider incidents, ~25 min wall) — the corrected dispatch chain + session-modelId provenance check scaled to dream mega-minions without a single continue.
- Backfill tail-reads cost 2 reads and were both clean pre-marker this time — keep the caveat (wire-aesthetics 08-21 proved it pays), but expect most per-job shards to be single-write.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-27.md
# dream-2026-08-27 — Bob's shard

- herdr pane resize --amount is a FLOAT fraction (0-1): integer amounts
  clamp the split to extremes (0.1 / 0.6 ratios observed) — 0.27 moved the
  boundary cleanly; verify with `herdr pane layout` after each call
  (semantics stay empirical).
- A marker that jumps WITHOUT a dream row (the 08-25 DSH-interlude advance)
  flags a coverage-gap window — date sources by CONTENT (git log per file,
  shard headers), never mtimes: a git checkout/restore normalizes every
  mtime to the same minute (08-25 16:49 local across ~200 files).
- Sheep handovers via brief-FILES + one-line pointers: 3/3 delivered clean,
  first try, zero quoting-class incidents (the KYLE spawn-craft law applied
  to sheep dispatch).

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-29.md
# dream-2026-08-29 — Bob's shard

- `stat -f %Sm` prints LOCAL time — comparing mtimes against a UTC marker
  without converting flips borderline files (the dream-2026-08-27 shard
  was −86s BEFORE the marker, not after); content-dating (the U1
  proposal) makes the whole class moot.
- Store-edit integrity check for close-out: `diff live store-copy | grep
  '^<'` isolates exactly the MODIFIED-live-line set (4 this pass — every
  mid-line addendum anchor), everything else is pure insertion; Silas can
  spot-check the 4 instead of the whole diff.
- 3-sheep wave on k3 brief-FILES: boot chain (sleep 12 → un-piped
  `agent wait --until idle` → sleep 3 → handover → verify working) held
  3/3; the session-jsonl modelId grep RACED the boot (files appeared
  seconds after agent registration — grep again, don't conclude).

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-08-31.md
# Field notes — dream-2026-08-31 (Bob)

- Small windows still earn sheep: 2 sheep (journals/ledger) cross-verified the fun-test squad window in ~5 min; the ledger sheep's independent DB count (27 events / 7 jobs) caught that #118/#124 fix rows don't exist yet — context, not a gap (issues-first intake, rows mint at dispatch).
- Content-dating (U1) earned its keep: silas-08-28.md's post-marker mtime (22:29) held ZERO post-marker content — the backfill entry pre-dated the marker; tail-read confirmed and skipped without re-mining.
- The 3/3 notification-gap sweep had a two-source proof (journal quotes + ledger transitions + 0 cli:notification:show results) — the false-claim flavor (fun CLAIMED shown:true without executing) is the new worst case; verify toolResults, never the minion's report.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-09-02.md
# Field notes — dream-2026-09-02 (Bob)

- `herdr pane split <pane>` REQUIRES `--direction right|down` — a bare split prints usage with RC masked by the parse pipe (the pipe-masked-failure gotcha's dream flavor); 3 "failed" splits created ZERO panes — verify with agent list before assuming debris. Split JSON key = `result.pane.pane_id` (unchanged on 0.8.0).
- The ledger sheep earned its pane again: independent DB reads caught the EMPTY review anchor in a close-out note AND that a minion's "dispatch add was missing" self-create claim was FALSE (the row existed under the long id) — journal-only reading would have missed both. Small windows still earn sheep (2nd dream).
- Adversarial pass caught a numeric-contract trap BEFORE it shipped: the shards' "max_span 10 vs 14/16/18" conflict resolved against `data/pipe_tiers.json` — both true (10 = the DISABLED narrow tier); the proposal became a stale-guard parenthetical, not a correction. Verify contract numbers against the repo, never pick a winner from two quotes.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-09-04.md
# Field notes — dream-2026-09-04 (Bob)

- The dispatch can delegate Silas' close-out steps to Bob ("apply autos, stage user-acks; write the marker ON COMPLETION") — when it does, mirror the store-copy diffs to the LIVE files byte-identical (diff-verified) and leave the COMMIT to Silas; the briefing's Never-list yields to the explicit dispatch, never to interpretation.
- Sheep briefs: glob-resolve every shard path against the filesystem before writing the brief (mine listed tie-`deconflect`, the file is tie-`deconflict` — the sheep caught it, the brief didn't); sheep on glm-5.3 with briefs-to-files ran 3/3 clean, ~2-4min each, zero continues.
- Dream window 09-02T22:38Z→09-04T23:58Z was PP3D-belt-shaped: journal+ledger sheep converged on every major pattern (k3 weekly cap, phantom checks, FYI live-red, deferred-row miss) — the 2-source convergence bar is easy to clear when one repo dominates the window; the adversarial pass then spends its time on the marginal singletons.

## SOURCE /Users/moses/code/_bmad-output/field-notes/dream-2026-09-07.md
# Field notes — dream-2026-09-07

- 2026-09-07: the pi edit tool's atomic-across-edits[] rollback bit me ×3 this pass — one wrong line-wrap in an oldText rolls back the WHOLE 11-edit call with only "could not find edits[N]"; re-read the exact wrap from the file (grep the fragment, sed the region) before re-issuing, and prefer short unique tail-line anchors over multi-line ones.
- 2026-09-07: sheep briefs to FILES + short file-pointer handovers worked clean (3/3 boots chained, modelId verified, zero stuck buffers); the 2×2 split layout (me + 3 sheep, one tab) is the comfortable dream shape.
- 2026-09-07: the dream row did not exist at first `ledger set` (dispatch add raced my start); the add UNIQUE-failed on retry revealing the row was there — check the DB before assuming either direction.

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-architecture-v1.md
# Field notes — finlit-architecture-v1 (2026-08-03)

- Mega-minion review swarms EARN their panes on big docs: the R1 swarm caught a schema that silently violated a locked pillar (KID-persists) and a sync-over-HTTP seam that wasn't buildable; R2 caught a defective rounding formula I'd written to fix R1 (the GDD's own $24→$2 tax example was the disproof) — budget an R2 pass, R1 fixes introduce their own bugs.
- HERDR_* env vars go STALE across Herdr restarts (mine pointed at a dead workspace) — always re-resolve with `herdr pane current --current` before splitting; layout JSON gives the real ids.
- Lavish end-session: poll returns queued rulings but the VERDICT may be absent even when the user is done — check `~/.lavish-axi/state.json` session (prompts/pending_prompts) as ground truth before deciding whether to ask for the verdict in-pane (it was absent → asked → approved).

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-bugfix-event-messages.md
# Field notes — finlit-bugfix-event-messages (2026-07-31)

- GDScript type trap that caused the whole bug: `var x := 60` (int) then `x -= delta` silently TRUNCATES each frame (−1/frame) — no error, no warning; any var receiving frame deltas must be explicitly float-typed (`var x: float = ...`). Int var = float literal also truncates silently.
- Godot capture rig on macOS: `--headless` = dummy renderer (`viewport.get_texture().get_image()` returns NULL) — captures must run WINDOWED; `await process_frame` inside `SceneTree._initialize()` deadlocks — drive frames from `_process`; `_ready` is DEFERRED to the first iteration when add_child happens in `_initialize` (freeze test state in the first `_process` frame, and a failed edit in a multi-edit `edit` call fails the WHOLE call atomically — re-check the file).
- Rebasing onto a theme/palette restyle: `.tres`/`.tscn` colors store 6-decimal truncations vs exact /255 from `Color("#hex")` — assert with `is_equal_approx`, never `==`; theme propagation is tree-scoped, so scene-instantiating color tests must add dynamically built cards INTO the tree (or hand the node the theme like `_open_popup` does) before asserting.

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-e2-1.md
# Field notes — finlit-e2-1 (playtest protocol)

- Godot disabled Buttons swallow clicks AND emit no `gui_input` (windowed probe: enabled=2 hits, disabled=0); headless `Input.parse_input_event` never routes GUI at all — tap capture needs a transparent `MOUSE_FILTER_STOP` overlay child (anchors FULL_RECT), verified windowed; headless tests pin wiring via direct `gui_input.emit`.
- Godot `FileAccess` WRITE buffers: `get_file_as_string` right after `store_line` is empty until `flush()` (probe it — same trap as pipe truncation); `DirAccess.make_dir_recursive_absolute` handles `user://` paths fine.
- GDScript 4.7 gotchas: no `Array.find_last` (use `rfind`); `:=` on a String/Array ternary trips INFERENCE_ON_VARIANT warnings-as-errors (annotate `: Array` explicitly); `Time.get_datetime_string_from_system(false, true)` puts a SPACE in filenames (use UTC + replace ":").

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-e2-7.md
# Field notes — finlit-e2-7 (touch-target rules, A29)

- Relative-path edit/write tools resolved to the MAIN checkout, not the worktree — one `git commit` ran with `cd /Users/moses/code/kids-finlit-game` and landed on local main (recovered via stash + branch move; ALWAYS use absolute worktree paths for file tools and git).
- Headless `push_input` routing: the root window is 64×64 while content space is 1280×1280 (stretch) — resize the window to the content size or routed taps never land; delivery is deferred one frame (assert a frame later).
- The leaderboard card's first layout pass sizes it ~8x tall from unwrapped labels — measure popup targets only after a bounded settle loop (rect stable across frames), never `await resized` alone.

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-game-brief.md
# Field notes — finlit-game-brief (2026-07-31)

- `herdr wait agent-status --status done` can time out even when the mega-minion finished — panes in a watched tab complete as `idle`, not `done`; poll `herdr pane get` and accept either.
- Mega-minions re-reviewing a file the parent just edited can report STALE findings from session context (2 this run) — verify every finding against disk before applying.
- gds-create-game-brief's `.decision-log.md` is a dotfile inside the run folder — `git add` the folder path normally picks it up, but confirm with `git status` before committing (the verify bar is "only the new artifact").

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-gdd-amendments.md
# Field notes — finlit-gdd-amendments (2026-08-05)

- Docs amendments that renegotiate LOCKED content need an explicit renegotiation section + inline [AMENDED — A#] tags + register-row updates — silent edits get caught by the review swarm every time (both lenses flagged provenance/citation issues; the adversarial lens web-verified the Disney Research citation).
- "12+"-style open caps invite implementers to invent numbers: pin the unlock ladder (per-gate assignments, definitions like "first $500 = lifetime total_earned", offline fallbacks) in the amendment itself — the edge-case hunter flagged it, and pinning took one table.
- Docs-vs-code honesty: when a doc amendment supersedes a code-side pin (Mrs. K persona in llm_tutor.gd, test_economy.gd:457), say "supersedes — code-side change, out of scope" instead of "replaced" — the reviewer checked disk and caught the overclaim.

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-prototype.md
# finlit-prototype — field notes (badge-out shard)

- Godot 4.7 gotchas that bit: `trait` is a RESERVED word in GDScript; `theme_override_constants/separation` is tscn-serialization syntax only — at runtime use `add_theme_constant_override()`; JSON.parse turns ALL ints into floats, so save-load needs an explicit re-cast pass before array indexing.
- DeepSeek `deepseek-v4-flash` has THINKING ON BY DEFAULT and it silently eats max_tokens (kid answers truncate mid-sentence) — send `"thinking": {"type": "disabled"}` for short-form output; docs 302-redirect, use web_search snippets instead of web_fetch.
- `godot --headless --check-only <project>` is NOT a valid invocation and hangs for 120s+; the working headless gate is `godot --headless --path <dir> --import` then `--quit-after 600`, tests via `--script res://tests/x.gd` with `extends SceneTree` + `_initialize()`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-tutor-economy-fix.md
# finlit-tutor-economy-fix — field notes (badge-out shard)

- DeepSeek truncation bugs: check `user://tutor_llm_log.jsonl` FIRST — this one was `finish_reason: stop` on every call; the CLIENT-side word-cap was the guillotine, not max_tokens/thinking. And "trim at sentence boundary" must be abbreviation-aware — the persona is literally named Mrs. K (the guard once returned "Mrs." as the whole answer).
- "Theoretical max wage" thinking must include the parents allowance (+$1/drop): couch-only math left a $0 doctrine margin ($1,800 = exactly the duplex price at day 15). Edge hunter caught it; price went $1,800→$2,000.
- Repricing an economy silently REVALUES old saves (book value derives from current tables) — bump the save schema version and let the corrupt-recovery path (identity kept) absorb them, or you fabricate wealth-climb.

## SOURCE /Users/moses/code/_bmad-output/field-notes/finlit-visual-mock.md
# finlit-visual-mock — field notes

- Godot: theme does NOT propagate across a CanvasLayer — popups under
  `PopupLayer` render default-white text unless you hand them the theme
  (`card.theme = theme` in `_open_popup`). Found via blank-looking captures.
- Container layout is deferred: styling/animating a node the same frame it's
  `add_child`ed gives `size == (0,0)` — juice pivots must await `resized`;
  and `get_child(i)` right after a rebuild hits queue_free'd nodes (new
  children are appended AFTER the dying ones until frame end).
- Screenshot rig: `--headless` has no renderer (blank PNGs); run windowed
  with `--position -3000,-3000` to stay off the user's screen — rendering
  still works. `set_process(false)` freezes game timers for deterministic
  stills; seed states via the pure economy API, never clicks.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-dashboard-perkins-bridge.md
- Out-of-tree host plugins CAN expose browser-callable remotes via SRC/source-mode Typert discovery (typertRemote binding + Remote marker, applied programmatically without decorator syntax); the browser rides ctx.connection.rpc.call("/api", "ns/method") because ctx.remote.* namespaces are a build-time-fixed set.
- A rejected cordis loader entry is FATAL to dsh-app-boot (exit 1) — host halves must guard every import/registration path and degrade to a log line.
- sqlite3 CLI cannot open this ledger DB read-only on this machine (rc=14); node:sqlite DatabaseSync {readOnly:true} works and is the sanctioned read path.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-docs-p4-p5.md
# Field notes — orchestrator-docs-p4-p5 (2026-08-31)

- 2026-08-31 (orchestrator-docs-p4-p5): "already in managed-repos.txt" in a briefing can mean the ORCHESTRATOR ROOT'S LIVE TREE (uncommitted) — youtube-channel's adoption line was in /Users/moses/code/managed-repos.txt, NOT in the worktree's committed copy; verify the live checkout before treating it as a missing record, and phrase doc references as "recorded in managed-repos.txt" (not "committed").
- 2026-08-31 (orchestrator-docs-p4-p5): `herdr notification show` returns `{"id":"cli:notification:show","result":{"reason":"shown","shown":true,"type":"notification_show"}}` — the exact paste-shape for the new P5 self-notify checklist gate (playbook Minion standing orders); `shown:false` = relay busy → retry once, then escalate.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-docs-ua1-ua2.md
# orchestrator-docs-ua1-ua2 — field notes

- 2026-08-07 (orchestrator-docs-ua1-ua2): briefing said "work directly in
  the orchestrator root (no worktree)" but the dispatch actually created a
  STANDARD worktree — pane cwd was `~/.herdr/worktrees/code/orchestrator-docs-ua1-ua2`
  with the `<slug>` branch already checked out. Ground truth = pane cwd; work
  there on the slug branch (the PR→main outcome is identical either way). Adds
  a "worktree/no-worktree decision in the briefing disagrees with the actual
  dispatch" flavor to the existing stale-briefing lesson.
- 2026-08-07 (orchestrator-docs-ua1-ua2): for a pure structural doc reorg
  (zero-content-loss constraint), the reliable PROOF is a sorted multiset of
  non-header lines old-vs-new (`grep -vE '^(##|###|\s*$)' | sort | diff`) →
  byte-identical = nothing changed/lost. Don't eyeball `git diff` — reordering
  shows as noisy add+remove pairs that look like content change.
- 2026-08-07 (orchestrator-docs-ua1-ua2): `gh pr create --body "$(cat <<'EOF'
  ... EOF)"` BREAKS when the body contains backticks — bash command-
  substitution executes them (got `node_modules: command not found`). Use
  `--body-file <file>` for any PR body with backticks/code spans.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-nefario-conflict-sensor.md
# orchestrator-nefario-conflict-sensor — field-note shard

- 2026-08-05 (orchestrator-nefario-conflict-sensor): Node 22
  `--experimental-strip-types` REJECTS constructor parameter properties
  (`private x: T` in a constructor signature) — "TypeScript parameter
  property is not supported in strip-only mode". Declare the field
  explicitly and assign in the body. (Same flag also can't run a file
  with non-erasable runtime enums/`const enum` — stick to plain const
  Sets like the extension already does.)
- 2026-08-05 (orchestrator-nefario-conflict-sensor): testing a pi
  extension that self-registers `setInterval` callbacks — each `start()`
  (a fresh `nefarioWatch(pi)` instance) pushes TWO callbacks (pane tick +
  PR tick). A per-scenario tick handle MUST be captured at start time;
  a fixed `callbacks[1]` index silently runs SCENARIO 1's closure against
  every other scenario's data (ticks stay silent, assertions pass by luck
  until a re-arm/re-fire case exposes it).
- 2026-08-05 (orchestrator-nefario-conflict-sensor): ESM relative imports
  resolve against the SCRIPT's directory, not `cwd` — a /tmp scratch
  importing a worktree `.ts` needs the absolute path; keep scratch files
  inside the worktree instead.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-night-watchman-hardening.md
# orchestrator-night-watchman-hardening (2026-08-22)

- launchd PATH class: quota-probe + night-watchman resolve pi/herdr/jq absolutely (PI_BIN env → ~/.local/share/fnm/aliases/default/bin → node-versions newest-first → command -v); a PATH error is NEVER a provider verdict — probe exits 2 with NO regime write, watchman startup FATALs on unresolvable herdr/jq, and a broken probe is logged+notified as TOOL-BROKEN (the 23:38Z misread class).
- Sandbox isolation hooks (NIGHT_WATCHMAN_LOG/STATE_DIR/LOCK_DIR/NOTIFY=0) keep test runs out of the live service's files — the live watchman never skipped a tick during the whole verification (isolated lock matters: --once shares the lock dir).
- Self-test assertions that grep $0 must not contain the literal word they assert (the no-create regex's `kill` flagged itself) — break the literal with a bracket class (kil[l]).

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-night-watchman.md
# orchestrator-night-watchman — field notes

- **bmad-build render HALT on this install (upstream 6.11.0, not repo
  drift):** `ambiguous config value implementation_artifacts` (bmm + gds
  both define it; the fresh skill uses the `{{.implementation_artifacts}}`
  short-token). No in-repo fix exists (config.toml installer-managed;
  overrides still leave 2 matches). Waived by Silas ruling — briefings
  should avoid bmad-build until upstream fixes the template; carry the
  canon note in PR bodies.
- **launchd StartInterval jobs self-heal across a merge:** bootstrapping
  a plist whose ProgramArguments path doesn't exist yet just logs exit-78
  failures per tick and starts succeeding once the merge materializes the
  file — no plist edit, no re-bootstrap, no untracked-file hazard in the
  live tree (the git-overwrite refusal makes copying the script there a
  trap).
- **Agent liveness = herdr detection AND session-file existence; env
  correctness = extension marker grep:** herdr can report a stale idle
  agent with the session file gone (dead pi class 07-30) — only the file
  check catches it. And the silas/gru extensions only inject their
  "Silas/Gru startup checklist" text when the right PI_* env is set, so
  grepping the fresh session jsonl proves `PI_SILAS=1`/`PI_GRU=1`
  end-to-end without trusting any pane-side report.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-perkins-ops-codify.md
# Field notes — orchestrator-perkins-ops-codify (2026-08-07)

What bit me / what future minions must know.

- 2026-08-07 (orchestrator-perkins-ops-codify): the briefing said "work
  directly in the orchestrator root (no worktree)" but the dispatch STILL
  created a worktree — my real cwd was
  `/Users/moses/.herdr/worktrees/code/orchestrator-perkins-ops-codify`,
  and the branch was checked out THERE. I first ran git against
  `/Users/moses/code` (main) and hit `fatal: branch already used by
  worktree`. The worktree-path gotcha applies even on "no worktree"
  orchestrator-root jobs: run git + file edits from your actual cwd, not
  the main checkout. (`pwd`/`git branch --show-current` first.)
- 2026-08-07 (orchestrator-perkins-ops-codify): the briefing's evidence
  citation was inaccurate — it named "RT-agent #169 N3" as a fold-in
  example, but disk check showed `RightTenantryAgents#169` has only r1
  (N3 was advisory, PR merged as-is, no fold-in/r2). Ground-truth-first
  (fresh instance): verify briefing-cited PR numbers + shas against disk
  (`gh pr view`, the perkins `<job>/rN/consolidated.json`) BEFORE writing
  them into a high-stakes doc — don't propagate a briefing's claim into
  the playbook unverified. Dropped #169; kept the verified #585.
- 2026-08-07 (orchestrator-perkins-ops-codify): `gh pr create --body
  "$(cat <<'EOF' … EOF)"` with a trailing `| tail` breaks bash
  (unmatched paren / unexpected EOF) — write the body to a file and use
  `--body-file <file>` instead. Robust for any multi-paragraph PR body.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-playbook-diet.md
# orchestrator-playbook-diet — field notes

- 2026-08-21: bmad-quick-dev → bmad-build render HALTs on this install
  (`ambiguous config value implementation_artifacts`) — waiver carried as
  a canon note in the PR body; the briefing was self-contained.
- 2026-08-21: full-file rewrites from memory re-inflate to ~950+ lines —
  the reliable diet is SEGMENTED line surgery (measure per section →
  exact-string replace → re-measure), not whole-file rewrites.
- 2026-08-21: heredoc + triple-quote Python strings with embedded quotes
  self-terminate (SyntaxError) — write replacement scripts to files or use
  the edit tool for exact-match replacements instead.
- 2026-08-21: the 650-line core target has a doctrine floor ~700: the
  keep-list sections (Model policy vision block, Minion standing orders
  paste-block, Dispatch commands, six-sensor table) are irreducible without
  cutting doctrine — report the honest number (713) and flag it in the PR.
- 2026-08-21: a `tr '\n' ' '` command inside a rewritten heredoc got
  corrupted into a literal newline — byte-check commands after any
  scripted rewrite (grep for the exact token).
- 2026-08-21: lavish session "ended by user" with the verdict in the
  session chat (`~/.lavish-axi/state.json` → sessions.<id>.chat) even when
  prompts shows 0 — check chat when the poll returns a dom_snapshot.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-role-skills.md
# orchestrator-role-skills (2026-08-22)

- pi extensions load via jiti (`jiti/static` → `createJiti`): the strongest load
  test is importing the real extension files through it; a `pi -e <ext> -p
  --no-session -nt "Reply OK"` boot from a NEUTRAL cwd exercises the full pi load
  path with zero side effects (the extensions' hardcoded-cwd guards short-circuit;
  verify via the session jsonl: only "Reply OK" present).
- The extension discovery glob is `.pi/extensions/*.ts` + `*/index.ts` (no deeper
  recursion, loader.js) — generated helper modules importable from extensions
  belong in a subdir WITHOUT index.ts (e.g. generated/role-blocks.ts).
- jiti/static is ESM-only (its package.json exports map has no "require" arm) —
  from CJS use dynamic import of the absolute lib path, never createRequire.
- Generator emission trick: JSON.stringify/json.dumps double-quoted strings
  (ensure_ascii=False) — backticks/${}/quotes/backslashes become inert; no
  template literal, so the 2026-08-01 ParseError class is impossible. Worst-case
  fixture round-trip test pins it.

## SOURCE /Users/moses/code/_bmad-output/field-notes/orchestrator-vision-tooling.md
# orchestrator-vision-tooling — field notes

- 2026-08-22: glm-4.6v needs NO ~/.pi/agent/models.json entry — the
  auto-fetched models-store.json catalog already declares
  `input: ["text","image"]` and the E2E proved the attachment passes
  (model_change modelId=glm-4.6v + image/png part + stopReason stop);
  only add a user-level override when a target model genuinely lacks the
  declaration.
- 2026-08-22: a `--no-session` run writes NO session jsonl — for a
  provenance check run without it; pin the session by its exact prompt or
  file-attachment TEXT PART, never by grepping the model name (the
  AGENTS.md canon puts "glm-4.6v" into EVERY session's context).
- 2026-08-22: ~/.pi/agent/skills/vision-read symlink is MISSING
  (pre-existing — every other skill is symlinked there); the skill ships
  repo-only at .agents/skills/vision-read and agents in other cwds may
  not resolve it. Flagged in PR; the role-skills job owns skill wiring.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-asset-scout.md
# field notes — packet-plumber-3d-asset-scout (2026-09-04)

- Poly Pizza (CC0-rich) has NO usable API without a key, but search pages embed full JSON in `window.__SERVER_APP_STATE__` (title/author/license/previewUrl) and the GLBs sit at `static.poly.pizza/<preview-uuid>.glb` — search-page JSON + curl = a complete free scouting API; tri counts via HTTP-range fetch of just the GLB JSON chunk (sum accessors).
- "Imports lie" quantified: authoring scales ranged 0.08x–25x across sources (power plant 1.33 m, farm house 25.3 m) — normalize by MEASURED world bbox (glTF accessor min/max × node-transform walk; ~80 lines of python, no Blender needed for GLB→GLB) and carry the factor in a `PP3D_NormalizedScale` root node; Sketchfab-sourced items go through the blender MCP `download_sketchfab_model` which accepts `target_size` and self-scales (still verify by measurement).
- Sketchfab thumbnails-as-files: `GET https://api.sketchfab.com/v3/models/<uid>` (public, no auth) → `thumbnails.images[].url` (NOT `.urls`); the blender MCP preview tool returns inline images only, unusable for HTML surfaces.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-e1-tiny-planet.md
# Field notes — packet-plumber-3d-e1-tiny-planet

- 2026-09-04: Godot camera gotchas that renders catch and unit tests miss: `look_at_from_position`
  takes GLOBAL coords (pinned our camera to world +Z — rig spanned, camera didn't); and
  `frame_point`-style "aim at X" must place the camera on X's SIDE, not the antipode (we
  photographed the wrong hemisphere). Always verify pose changes with a SCREENSHOT, not just
  transform asserts.
- 2026-09-04: Icosphere face winding: the classic Kahler table is CW = back-facing in Godot
  (CCW = front). Symptom: land invisible from outside, visible from inside. Swap two leaf verts
  and rely on SurfaceTool.generate_normals following winding.
- 2026-09-04: `-s` SceneTree scripts: nodes added during `_initialize` aren't inside the tree yet
  (global_transform errors) — run the suite on the first `process_frame`, and never `.free()`
  RefCounted test instances (drop the ref). Any pre-quit crash = engine hangs forever: null-guard
  every `load()` in the runner. Also GDScript has no `%e` format and INFERENCE_ON_VARIANT
  (`var x := get_setting()`) is an ERROR by default.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-e2-flow-qos.md
# field notes — packet-plumber-3d-e2-flow-qos

- 2026-09-04: Per-tick admission allowances can NEVER admit a packet larger
  than one tick's reserve — lanes need persistent deficit CREDIT (banked
  reserve, spendable in bursts) or a 1000-milli packet starves forever on a
  416-milli/tick budget. Caught by white-box probe before first suite run.
- 2026-09-04: Godot 4.7.1 runtime reload honors @warning_ignore at
  STATEMENT level only — func-level annotations pass the LSP but still warn
  in editor-run debug output. Also: non-tool scripts attached to scene nodes
  are PLACEHOLDER instances in the editor (@tool callers can't invoke their
  methods — Planet needed @tool for the editor-preview button path).
- 2026-09-04: Godot EDITOR windows at macOS off-screen positions (-3000)
  freeze to a 2x2 viewport texture (game windows render fine there) —
  capture EditorInterface.get_editor_viewport_3d(0) instead, and reposition
  the editor camera: its default pose sits INSIDE a radius-8 planet
  (front faces culled = "world missing" in the shot).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-gdd-amend-alive-planet.md
# Field notes — packet-plumber-3d-gdd-amend-alive-planet (2026-09-05)

- The core-loop ASCII box in gdd.md is visual-width-69 (emoji count 2): after editing box lines, re-measure ALL box lines with a python east-asian-width script — my first pad math used inner=65 (real: 64) and every replaced line came out 70; a one-line assert script caught and fixed it.
- The `gh pr create --body "$(cat <<'EOF'…)"` trap is real even for carefully quoted heredocs (×3 now) — went straight to `--body-file /tmp/…` on the second attempt; should have been the FIRST attempt.
- Canon-amendment pattern that worked: grep the OLD phrasings before editing ("building→building", "connect two houses", "no junctions", "L1 has no routers") — caught two non-obvious stragglers (tutorial seed line, L1 remediation "direct pipe") that the section-level plan missed.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-gdd-amend-cumulative.md
# packet-plumber-3d-gdd-amend-cumulative — field notes

- 2026-09-05: GDD amendment — supersede chains must be DATE-STAMPED at every amended canon site (M2/M3/OQ9/E10.7), not just in the decision log, or readers meet the old claim first and trust it (D5's retirement clause had propagated to 4 sites).
- 2026-09-05: `gh pr create --body "$(cat <<'EOF' ...)"` with apostrophe-rich markdown dies on quoting — write the body to a temp file and use `--body-file` instead.
- 2026-09-05: scope guard pays off twice — stale canon found ADJACENT to the named sections (Risks row 2 "constellation... re-scope an open question") gets flagged in the decision log + PR body, never silently fixed; keeps the diff reviewable and the ruling trail honest.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-gdd-amend-era-planets.md
# Field notes — packet-plumber-3d-gdd-amend-era-planets

- 2026-09-05: The GDD's own text is the best anchor source — two edit-batch rejections came from mis-transcribing the `]`` ` `—` inline-code close in the read output; python `repr()` of the exact line beat re-reading the rendered view every time.
- 2026-09-05: PP3D lavish gate pages: the repo's little-planet palette tokens (GDD Art §) make a coherent dark review page with zero CDN deps; SVG viewBox + short labels survived the DOM audit with zero layout warnings on first serve.
- 2026-09-05: Cross-lane courtesy pattern that worked: touch ONLY the files the briefing names (3 GDD files), put the adjacent-surface find (README stale comment) behind an in-page decision form — the user ruled it in, and the README edit rode this PR with zero l1-arpanet conflict risk.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-gdd-amend-levels.md
# Field notes — packet-plumber-3d-gdd-amend-levels

- 2026-09-04: lavish decision forms work — per-row radios + one Queue button got clean machine-parseable rulings (D1–D5 all arrived as tagged prompts); pair every form with a pros/cons explainer block when the options aren't self-evident (the user asked "explain this, pros and cons" on the two forms that lacked one).
- 2026-09-04: a user annotation can RESCUE a briefing's scope guard without breaking it — "look at the odin version" was satisfied from THIS repo's own verbatim inheritance records (M4/E10.2 carried the post-streaming era content); check what the repo's canon already records before reading across the guard.
- 2026-09-04: box-art/ASCII blocks in markdown need exact column-count replacements — build replacement lines in python and assert interior width (64) BEFORE issuing the edit; and after table edits, re-render the region to catch rows orphaned by an inserted clarifier paragraph (my M5 table split silently on first attempt).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-gdd-v1.md
# Field notes — packet-plumber-3d-gdd-v1 (2026-09-04)

- The pi `edit` tool is **atomic across the whole edits[] array** — one failed
  oldText rolls back ALL edits in the call (my 4-edit lavish-round-1 apply
  silently lost 3 of 4 edits; caught by re-grep). Always re-grep after a
  multi-edit apply, and keep oldText minimal so a miss is diagnosable.
- `bin/ledger set <id> in-review` is guarded: it REFUSES unless the `pr`
  field is already set — run `bin/ledger pr <id> <url>` FIRST, then `set
  in-review` (or pass the URL in the note). Wrong order = refused, not warned.
- Lavish craft: the FIRST `poll --agent-reply` returns only the dom_snapshot
  (no feedback) — that's normal; re-poll to actually wait. The
  `_local-refs` loopback pattern (`python3 -m http.server 4388 --bind
  127.0.0.1 --dir <refs>` + `http://127.0.0.1:4388/...` img URLs) serves
  IP-sensitive frames in the review page with zero copying — verify a 200
  with curl before opening the session.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-l1-topology-font.md
# packet-plumber-3d-l1-topology-font — field notes

- 2026-09-05: Godot 4.7 `FontVariation.variation_opentype` SILENTLY IGNORES
  string axis keys (`{"wght": 700}` renders regular) — only integer fourcc
  tags work (`{("w"<<"24")|...: 700}`); a bold-vs-regular advance-width pin
  is the cheap guard. Also: `#` comment lines poison project.godot sections
  (keys read back empty) — use `;`.
- 2026-09-05: macOS occlusion throttling freezes windowed captures (the
  freshness gate caught identical frames); fullscreen puts the window on an
  active Space and `CONTENT_SCALE_MODE_CANVAS_ITEMS`+`EXPAND` keeps UI at
  true game proportions on the big canvas (downscale to 1600 wide after).
- 2026-09-05: the godot MCP LSP serves the MAIN checkout root — worktree
  files analyze as outsiders (phantom "hides a global script class" +
  "not declared" for NEW global classes). Prove health via on-disk
  `.godot/global_script_class_cache.cfg` + `--check-only --script` per file.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-3d-scene-refactor.md
# packet-plumber-3d-scene-refactor — field notes

- 2026-09-05: Godot placeholder-instance trap bites @tool generation:
  `PackedScene.instantiate()` of a scene whose root script is NOT @tool
  yields a placeholder under the editor — script methods (setup()) are
  uncallable and staging silently aborts at child 1. Editor-hint paths must
  construct via .new(); runtime can instantiate. Caught ONLY by pixel
  forensics (suite is runtime-only).
- 2026-09-05: editor-viewport PNG md5 is NOT a valid determinism gate:
  same-code re-renders gave 3 different md5s pre-refactor; the audit pinned
  the mechanism (editor viewport height drifts ±1 px with window/dock
  layout). Gate instead on structural pixel diff (12× downscale + blur,
  grayscale): noise floor max≈1; real composition change reads max 110+.
- 2026-09-05: the godot MCP's LSP is a long-lived `godot --headless --editor
  --lsp --path .` process that holds the PRE-MOVE class cache after refactors
  (140 phantom diagnostics citing old paths; res:// resource-existence checks
  also lag new files). `pkill -f "godot.*--lsp"` → MCP respawns fresh → 0
  real diagnostics. Check disk `.godot/global_script_class_cache.cfg` first
  to prove the cache is fine.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-architecture-v1.md
# Field notes — packet-plumber-architecture-v1 (architecture minion)

- The `gds-game-architecture` skill's per-step A/P/C "Ready to begin? [Y/N]"
  checkpoints are **pre-approved** per the orchestration standing orders; the
  briefing's detailed scope overrides the skill's generic GDD discovery — proceed
  headless (read ALL source in full first), halt only on genuine blockers. None
  arose; the lavish review was the human gate.
- A **2-hunter review swarm** (adversarial-general + edge-case-hunter mega-minions)
  caught real contradictions the author was blind to on a high-stakes doc every
  downstream agent reads (CrisisEngine↔Director data-flow *direction*, `Vector3`
  vs `Vector3i` on the determinism spine, sim-tick SLA/QoS ownership, GDScript-has-
  no-interfaces). Worth the ~2-pane cost; verify every finding against disk
  (ground-truth-first) before applying — all 40 findings here were legit.
- lavish markdown→HTML via `marked --gfm -o` (file write, **no pipe**) handled a
  78KB doc cleanly (98KB HTML, verified tail); one `poll` return can deliver a
  **batch** of 7 feedback items at once — handle them together, re-render, reply
  once. Batch the doc edits in one `edit` call (disjoint oldTexts), re-render,
  reply — faster than per-item round-trips.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-art-direction-amend.md
# Field notes: packet-plumber-art-direction-amend (2026-08-08)

- (canon amendment) When a doc carries a "no em-dashes" rule AND uses ` - `
  hyphen-spaced dashes throughout, MATCH it in additions - grepping the doc for
  `—` first (0 hits) confirmed the convention; introduced zero, stayed surgical.
- (amendment scope) "Reverse every abstract X statement" requires a grep sweep
  to bound ALL sites, then a scope-verify pass that nothing collateral moved.
  Here: node-shape terms lived in §6.2 + OQ-4 only; §5 packet shapes (circle/
  triangle/diamond) are a DIFFERENT system and must be left locked - explicitly
  called out in the amendment note so a future agent doesn't "fix" them too.
- (judgment-call surfacing) A briefing that enumerates terminals but says "nodes
  = literal buildings / reverse every abstract shape" leaves the junction
  ambiguous. Literalized it conservatively + flagged it in the PR's Decisions &
  rationale as a one-line-revert - better than silently dropping or silently
  leaving the last bare shape.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-art-direction.md
# Field-notes shard: packet-plumber-art-direction

- 2026-08-07: the worktree was STALE (2 commits behind origin/main) — the narrative spec landed via PR #5 after my branch was cut, so `narrative-v1.md` was missing from my working tree though present on main. Always `git log HEAD..origin/main` for sibling merges that touch your deliverable's sources, and rebase onto origin/main before opening the PR.
- 2026-08-07: `game/data/*.json` catalogs are UNCOMMITTED (only `game/data/.gitkeep` is tracked) — reading them as "the runtime source of truth" misleads; the committed design docs (GDD + narrative) are the real authority. Don't treat uncommitted local working files as canonical, and don't commit data owned by another job (the prototype) from an art-direction PR.
- 2026-08-07: a "go with your recommendations" approval can be given before a sibling doc that changes a decision's basis is seen (I hadn't read the narrative when OQ-1 approved orange). When you later discover a sibling canonical doc that flips a decision's evidence, SURFACE it and use veto power rather than silently deferring — the user explicitly reminded me "you have the veto power on theme, looks."

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-background-maps.md
# packet-plumber-background-maps — field-notes shard

- 2026-08-18 (packet-plumber-background-maps): rlsw/harness process ABORT traps — deleting TEMP-allocator slices (`make(..., context.temp_allocator)` + `delete`) frees an arena interior pointer with the heap allocator ("pointer being freed was not allocated"); the temp arena frees wholesale — never per-slice delete (map.odin note).
- 2026-08-18 (packet-plumber-background-maps): a map/generator cache reused across demos in ONE harness process must be TOTAL (write every cell per generation) — `else if cell==0` keeps a prior seed's values (park/coast leaked across the juice re-bless); fresh processes hid the bug, the palcheck same-seed pin caught it.
- 2026-08-18 (packet-plumber-background-maps): pixel-per-pixel value noise (integer hash + smoothstep, no libm) renders MM-organic coastlines at 1 world-px; a wide coast band (radius 2) read as blocky banding — radius 1 + ~50% land reads organic; LAND_LEVEL 0.46 measured only ~40-49% land (value noise skews low) — 0.38 → ~46-52%.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-blender-art.md
# Field notes: packet-plumber-blender-art

- 2026-08-08: **NEVER call `bpy.ops.wm.read_factory_settings()` via BlenderMCP.** It reloads the
  BlenderMCP addon, which KILLS the :9876 socket server thread and does NOT restart it — Blender
  (PID) keeps running, but port 9876 has no listener and every MCP call then fails "Not connected to
  Blender" / "Connection closed". Chicken-and-egg: you can't run Blender code to restart the thread
  because the connection is dead, so it's a user-blocking halt. To clear the default scene, DELETE
  the default objects instead (`bpy.data.objects.remove` loop over Cube/Light/Camera + purge orphan
  data), never a factory-settings reload. Recovery = user toggles the BlenderMCP addon off→on in
  Blender Preferences → Add-ons (or its N-panel Start Server) to respawn the listener.
- 2026-08-08: Blender 5.2 LTS / Eevee Next has NO built-in bloom (`eevee.use_bloom` removed in 4.2).
  The "glowing flows on dark canvas" glow must come from a **Compositor Glare node** (Bloom) on the
  render output, with Standard view transform so the canon's exact hex values read faithfully (AgX
  / Filmic desaturate bright emissives).
- 2026-08-08: **Blender 5.2 compositor API (big refactor).** `scene.node_tree` is GONE (PR #143619).
  The compositor is a node-GROUP now: `nt = bpy.data.node_groups.new(name, 'CompositorNodeTree')`;
  `scene.compositing_node_group = nt`; output via a `NodeGroupOutput` node + `nt.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')`; assign Render Layers → Glare → GroupOutput. The Glare node's settings are **input sockets** with DISPLAY-NAME enum strings (`'Bloom'`/`'Fog Glow'`/`'Streaks'`, `'High'`/`'Medium'`), NOT node properties and NOT `'FOG_GLOW'`/`'HIGH'`. `CompositorNodeComposite` is undefined in 5.x.
- 2026-08-08: **To DISABLE the compositor in 5.x you must null the group:** `scene.compositing_node_group = None`. Setting `scene.use_nodes = False` alone does NOT stick (it stays True while a group is assigned) — a stale Glare group from a prior build silently re-applied and BLEW a light/daytime render to pure white. Symptom: PNG bg samples (1,1,1) instead of the set cream.
- 2026-08-08: Eevee BLEND transparency renders an Emission-through-Transparent mix as NOTHING (the glow disc vanishes). Opaque fade-to-canvas halos read as visible dark discs (they occlude the grid). Net: for glow, use compositor Bloom (dark palette) or just flat emissive (light palette) — don't fight Eevee's blend pipeline. Standard view transform keeps chroma (AgX desaturates bright hues to white); emissive strength ~1.0 = faithful hex, >1 clips channels toward white/cyan.
- 2026-08-08: **Verify a lavish verdict in `~/.lavish-axi/state.json` (sessions.<id>.chat) before acting** on a load-bearing decision — the poll's `prompts[]` usually delivers, but session-end can strand a queued message and the printed `prompts[]` line is ambiguous to parse; state.json chat is ground truth. (Confirmed the user's canvas verdict "light" there before rendering the rest.)
- 2026-08-08: For a "house" silhouette in a 3/4 ortho render, build a **gable (ridge) roof and run the ridge along Y** so the triangular gable-END faces the camera (-Y); ridge along X makes the camera see a roof slope and the building reads as a flat cube. In-scene TEXT labels must be rotated vertical (X 90°) to face the camera — flat-on-ground text foreshortens and overlaps geometry.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-bundle-reprice-pin.md
# Field notes — packet-plumber-bundle-reprice-pin (2026-08-13, W1 pin)

- W1 pin job: the mixed-tier bundle re-pricing branch (`else if c < min_cost[ns]`, routing_rebuild pass 1) is now pinned by test_cost_mixed_tier_bundle_min_member_pricing. Bite-toggled: disabling re-pricing makes the (res,host) route VANISH (count 0) — dist is relaxed per-pipe in the Dijkstra but pass-1 min_cost feeds the pass-2 equality, so a broken pass 1 erases the hop entirely. Useful failure signature for future toggles.
- Recurring main-checkout trap (3rd sighting): an `edit` with the MAIN checkout's absolute path lands in the canonical checkout even when cwd is the worktree — after any edit, `git status` in cwd + grep the target file's test count before trusting a green run. Worktree-absolute paths only.
- Fresh worktrees lack `tools/raylib-sw` (gitignored): symlink it from the main checkout for harness runs (`ln -s /Users/moses/code/packet-plumber/tools/raylib-sw tools/raylib-sw`), and DELETE the symlink before commit — the ignore pattern `tools/raylib-sw/` (trailing slash) does NOT match a symlink, so it shows up untracked.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-forge6-desktop-first-amend.md
# Field notes: packet-plumber-forge6-desktop-first-amend

- 2026-08-08: briefings say "FORGE #6" but forged-idea.md numbers decisions as bare `### 6.` under "Locked decisions" — `grep FORGE` finds nothing; read the doc's own structure before hunting.
- 2026-08-08: the forge doc already had an amendment pattern (2026-08-08 canvas amendment: inline `> **X (amended …)**` note + Amendment log entry) — matching the in-doc precedent keeps canon self-consistent; don't invent a new amendment format.
- 2026-08-08: briefing ripple claims are verifiable — odin-architecture-v1.md already cited the un-amended FORGE #6 ("FORGE #6 amended accordingly"); grep downstream docs for `FORGE #<n>` before writing ripple flags.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-full-game-doctrine.md
# Field notes — packet-plumber-full-game-doctrine (2026-08-17)

- `ledger set <job> <same-status> "note"` is a silent no-op that DROPS the note ("already working") — use `bin/ledger note <job> "..."` for any status-preserving update; the playbook's warning is buried in the review-sensor section, not the self-report bullet.
- GH Actions account-billing failure masquerades as a CI failure: jobs "fail" in ~4s with NO logs (`--log-failed` → "log not found", zero failed steps) — the truth is in `gh run view`'s ANNOTATIONS ("recent account payments have failed"). It kills GH-ACTIONS RUNNERS ONLY: Perkins runs locally via pi panes and is UNAFFECTED (Silas correction 2026-08-17 — I misdiagnosed a slow r1 as billing-blocked from a timing coincidence; a missing Perkins review is NOT billing evidence, verify the mechanism or ask Silas before escalating).
- The surgical-hunk rebase relay works exactly as designed: placed stories-v2.md hunks clear of sibling 5.5/7.2 status lines → rebased onto v2@#59 with ZERO conflicts; verified the sibling card byte-identical (`git show origin/v2:<path> | sed` vs worktree) before `--force-with-lease`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-gdd-mechanics-amend.md
# packet-plumber-gdd-mechanics-amend (2026-08-10)

- **Conflict-sensor rebase is the MINION's job, not Silas's.** A briefing may say "Silas rebases your branch at PR time" (narrative), but the playbook's conflict-sensor section relays "rebase onto <base>, force-push" to the MINION pane — the minion owns the rebase + conflict resolution. Don't wait for Silas; when #18-merged-mid-job hit, I was already mid-rebase when his relay arrived. (`git rebase origin/<base>` → resolve → `git push --force-with-lease`.)
- **Pre-emptive no-overlap placement pays off under an open sibling PR.** I placed my single §M5 insert at the END of §M5 (after the V2 paragraph), deliberately clear of #18's archetype-table hunk → `gdd.md` auto-merged CLEAN; the only conflict was a dual tail-append on `decision-log.md` (both PRs appended at EOF), trivial to resolve (keep both). When amending a doc an open sibling PR also touches, grep the sibling's diff hunks first and place inserts outside them.
- **A lavish loop that invites the user to probe realism beats a self-review for authenticity.** My "overdrive ages the pipes" cost was unfaithful — real cables (copper/fiber) don't fatigue from traffic volume; the user's "drops reduces scoring" instinct WAS the faithful mechanism (oversubscription → tail-drop). For a game whose secondary audience is the technically-curious, surface the design for a realism probe, don't just self-check tenets. (Also: `grep -cE "a\|b"` is WRONG in ERE — backslash-pipe is literal; use bare `|`. It gave false 0s in my verify pass.)

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-gdd-v1.md
# packet-plumber-gdd-v1 — field notes

- **gds-gdd workspace path ≠ briefing path.** The skill's canonical workspace is `_bmad-output/planning-artifacts/gdds/gdd-<project>-<date>/` (gdd.md + epics.md + decision-log.md); Gru's briefing named `_bmad-output/planning-artifacts/gdd/gdd-v1.md`. Used the skill's path (downstream `gds-game-architecture` / `gds-create-epics-and-stories` consume `{doc_workspace}/gdd.md` + `epics.md`) and flagged the deviation in the decision-log + lavish callout — a one-command move if the user prefers the other path.
- **D-1 (no engine-implementation leakage) is the recurring trap for a Godot-game GDD.** Godot terms crept in mid-review and were caught by grep after each edit: `signal` (→ "indicator"/"event"), `per-frame` (→ "discrete ticks"), `expand` stretch (Godot stretch mode → "viewport scales"), `Node2D`/`_process`/`gl_compatibility`. Re-scrub mechanics/systems sections on EVERY change; keep engine specifics in Technical Specifications only (D-3).
- **A lavish design-doc review can drive 15+ substantive user-driven changes** (here: open-ended-run restructure + Network Health loss, link-level QoS + node serialization, global leaderboards + backend, monetization, UI/navigation, asset pipeline, epic staging + E11 rebuild, etc.). Keep `decision-log.md` current PER change (provenance + pillar-fit + "why it earned its place") so the PR's Decisions & rationale stays traceable and a fresh minion/reviewer can take over cold.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-hud-warning-overlap-fix.md
# Field notes — packet-plumber-hud-warning-overlap-fix (2026-08-14)

- `_pr_body.md` in the worktree root is a STALE leftover from a previous job
  (Job C) — write your own PR body file; never reuse it.
- The drag-rejection/cost cursor anchor (`i32(cur.x)+12, i32(cur.y)-14`) is
  now the single source of truth at the top of the drag block — hoist
  `to_screen` once, don't duplicate the anchor per branch.
- Full local suite = lint.sh + `odin test core` + `odin build app` +
  `harness.sh run|drift-check|preview-check` (CI is billing-blocked); 18/18
  harness demos green = T2 goldens byte-identical = the no-shift proof.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-lang-safety-research.md
# packet-plumber-lang-safety-research — field notes (2026-08-28)

- Odin crash forensics: macOS libmalloc aborts lose the stack above
  `_heap_free` in the .ips — a -debug build + `breakpoint set -n
  malloc_error_break` under lldb recovers the full Odin stack in one run.
- READ-ONLY repro recipe that works: rsync the repo to /tmp (exclude
  _bmad), env-gate a frame-script driver in app/main.odin copying the
  PP_NOC_E2E injection pattern (append Device_Events after polls, before
  dispatch_frame) — drove real drag-connects and caught the box crash
  RED, then proved the 2-line fix GREEN (8 connects) same evening.
- Odin dynamic arrays carry their allocator in the header (lldb frame:
  mem_free_with_size reads it) — a missed field in shadow_clone alias-frees
  the LIVE buffers silently; the class is caught deterministically by
  core:mem Tracking_Allocator (bad_free_callback carries file:line), not
  by waiting for the abort.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-local-ci-suite.md
# packet-plumber-local-ci-suite — field notes

- 2026-08-16 (packet-plumber-local-ci-suite): pinned odin dev-2026-08 EXITS 0 on a failed windows cross-link (prints "Linking for cross compilation for this platform is not yet supported" to stderr, emits NO binary) — a gate must check the produced artifact, never just the rc. Also `odin test` needs `clang` for the test-runner link (GH ubuntu runners ship it preinstalled, slim images don't — a parity gap the replica had to close).
- 2026-08-16 (packet-plumber-local-ci-suite): Dockerfile RUN steps default to /bin/sh (dash) — `set -o pipefail` fails hard; add `SHELL ["/bin/bash","-o","pipefail","-c"]` to mirror CI's `shell: bash`. And under `set -u`, an empty array expansion (`"${arr[@]}"`) is an unbound-variable error on bash 3.2 — use `${arr[@]+"${arr[@]}"}`.
- 2026-08-16 (packet-plumber-local-ci-suite): Dockerfile layer order (COPY tools/ → RUN build_raylib_sw.sh → COPY .) bakes the rlsw shadow so warm runs skip the 40s clone+compile — the bake survives the final COPY because .dockerignore excludes the shadow from the build context; measured: 33s warm vs 1m06s cold container runs, and a `docker build` with fully-cached layers is ~0s.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-narrative-messaging.md
# Field notes: packet-plumber-narrative-messaging (2026-08-07)

- Briefing banned em-dashes "CI-guarded", but disk shows NO em-dash CI guard in
  packet-plumber (no .github/workflows, no markdownlint/textlint/pre-commit) and
  the lavish-approved GDD uses 173 em-dashes; the brief's own locked alert
  `YOU_TUNE: DOWN — 2.3B` contains one. Verified against disk, surfaced to user
  as an open decision; kept all NEW copy em-dash-free, locked string verbatim.
  Generalizes (field-notes rule): briefing "constraints/current-state" can be
  stale; grep disk before honoring a CI claim.
- lavish on a ~49KB creative doc: `npx -y marked --gfm -o body.html doc.md`
  (file write, no pipe) + a node-assembled themed HTML shell rendered cleanly;
  user verdict was a terse "read good." + Send&End = approval; confirmed via
  ~/.lavish-axi/state.json `sessions/<id>/chat[].text` (no stranded prompts).
- Self-review (edge-case-hunter) caught a real constraint violation: banking
  copy said "DROPPING" but banking SLA is zero-drops `[GDD § M2]`; fixed to
  STALLING (transactions hang, packets never drop). Cross-check every copy
  sample against locked MECHANICS, not just tone.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-odin-architecture.md
# Field notes — packet-plumber-odin-architecture (2026-08-08)

- Lavish question-forms pay off: all 4 rulings came back as queued prompts in
  ONE poll cycle (one Queue button per question + "which rulings I need most"
  in the first --agent-reply). A user QUESTION mid-form (not a radio) means:
  answer in the next --agent-reply AND rebuild the form with the new options —
  they answered from the rebuilt form immediately.
- Multi-edit `edit` batches reject ATOMICALLY (one bad oldText kills all) —
  and a sed/python bulk path-rename afterwards will silently create NEW stale
  texts (`harness//`, misaligned ASCII diagrams, renumbered lists); always
  grep the renamed tokens + re-read touched regions before committing.
- raylib 6.0 (2026-04) ships rlsw software renderer + PLATFORM_MEMORY headless
  backend — bit-exact pixel goldens with no GPU/Xvfb; Odin dev-2026-07a fixed
  vendor:raylib 6.0 bindings; Odin mobile = `-subtarget:android`, emerging
  (odin-lang/Odin#6759); "PCG64-XSH-RR" doesn't exist (PCG32 XSH-RR = 64-bit
  state; PCG64 = 128-bit, XSL-RR/DXSM) — reviewers WILL check.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-odin-prototype.md
# packet-plumber-odin-prototype — field notes (badge-out shard)

- **Custom raylib builds for Odin:** an ODIN_ROOT shadow (symlink everything except a REAL copy of `vendor/raylib/raylib.odin` + the swapped platform `.a`) cleanly swaps the linked raylib — foreign-import lib paths resolve relative to the binding file's REAL dir, so symlinked bindings defeat the swap. raylib 6.0 rlsw+PLATFORM_MEMORY builds with 5 .c files + clang (no cmake); headless readback = `LoadImageFromScreen` + `ImageFlipVertical` + R/B swizzle (its framebuffer is bottom-up BGRA; RenderTexture readback returns zeros — draw direct).
- **`context.temp_allocator` is a trap in any long-lived loop** (harness ticks): anything that must outlive the iteration (hash arrays, map KEYS, tprintf'd failure messages) needs a permanent allocator — a per-tick `free_all` turns them into silent garbage that stays *self-consistently* wrong (blessed corrupt goldens before I caught it via the replay gate). Put the replay-vs-live comparison in the default `run` path, not a side command nobody invokes.
- **Odin r1 gotchas:** no C ternary (`x if c else y`), `DrawTriangle` backface-culls by winding (flip vertex order if a triangle vanishes), `json.parse` needs `parse_integers=true` or every int is a Float, `os.read_dir` takes an open `^File`, `odin test` has no `t.Fatalf` (use `testing.expectf` + `fail_now`), and `for x in [2]T{a,b}` composite-literal iteration is a syntax error — bind the literal first.

## Session 2 (2026-08-09): inventory pivot + cross-platform CI green
- **Economy ruling landed**: budget → Mini-Motorways tray (per-tier link/router counts; demolish returns items; upgrades exchange; routers player-placed via tray chips; growth residential-only; tick-scheduled grants). All in PR #17.
- **Cross-platform pixel determinism**: rlsw's rasterizer diverges arm64↔amd64 because clang fuses FMA on ARM but baseline x86-64 lacks the instruction. `-ffp-contract=off` on the raylib-sw build makes both bit-identical (verified 0-diff vs the ubuntu CI actual). Odin's own codegen didn't need a flag.
- **Ubuntu "segfault" root cause was mine**: `save_diff_bundle` wrapped an Odin temp-arena slice in an rl.Image and called `rl.UnloadImage` on it → freeing non-raylib memory → SIGABRT, but ONLY on the mismatch path (which is why green runs never crashed). Rule: raylib owns raylib allocations; never hand it foreign pointers to free.
- **`git add -A` on a CI-fix commit swept half-done feature edits onto the branch** → catalog-hash drift (T1 correctly howling). The hash did its job; my hygiene didn't. Commit CI fixes with explicit paths.
- **Odin json with parse_integers=true**: numbers come back `json.Integer`, not `json.Float` — a `. (json.Float)` type assertion silently skips them. Mirror the `jint` both-forms pattern for counts.
- **balance.json vs demand.json both have growth_roles** — the director reads BALANCE's. Editing demand's was a no-op.
- **Autopilot needed real algorithms**: port-reserve wiring (fill-to-2-free so meshes always have somewhere to land), biggest-in-stock router placement, reachable-BFS hub selection (islands must chain TOWARD the mesh; island-to-island chaining wanders forever), midpoint relay chains for over-span gaps. Without these the run dies at ~150s.
- **Trap for harness/demo authors**: `flood_plan`-style plans are temp-allocated — a per-tick `free_all(context.temp_allocator)` in a test loop frees the plan after tick 1. Only tick 1 spawns.
- **fmt_bprintf is numerals-only by design** (deterministic HUD) — `%s` renders literally; compose name+count with two draws.

## Model policy update (2026-08-09, GRU ruling)
My spawned workers (mega-minions) go `--model zai-coding-cn/glm-5.2` from now on — NOT deepseek-v4-flash. I stay on kimi-coding/k3 (frontier reasoning/design); kimi quota is reserved for me + Perkins review. In-flight deepseek workers finish their current sub-task; new spawns use glm-5.2. Already reflected in docs/orchestration-playbook.md 'Model policy'.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-opening-five-min-story.md
- 2026-08-14 (packet-plumber-opening-five-min-story): a 12-edit batch was rejected because one oldText was a markdown blockquote continuation ("design requires..." on a line prefixed "> ") and I omitted the prefix; verify continuation-line prefixes with sed before batch edits. Also: after resolving numbered open questions (Q3), grep the doc for stale "see Open Questions Q<n>" references (beat 2 still called Q3 "optional" after it was resolved).
- 2026-08-14 (packet-plumber-opening-five-min-story): canon-doc amendment craft paid off again — narrative-v1's established amendment-log format ("What changed / What does NOT change" entry) made the Dispatcher re-grounding clean; matching the doc's em-dash-free house policy for new prose avoided a style fight.
- 2026-08-14 (packet-plumber-opening-five-min-story): briefings can carry stale framing about the project phase — I wrote "MVP build" options until the user corrected that the prototype fun gate already passed (prototype-fun-gate tag) and the full game is in build; grep project-context for the current phase before framing MVP-vs-full-game decisions.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-port-limits-canon.md
# Field notes: packet-plumber-port-limits-canon (2026-08-08)

- The atomic-multi-edit trap bit me live: one `oldText` aimed at the wrong
  file (decision-log text fired at gdd.md) rejected BOTH edits silently —
  check each oldText's target file before batching, re-issue survivors
  per-file.
- Packet-Plumber GDD canon amendments: provenance is MANDATORY in
  `decision-log.md` (the doc's own rule) — dated entry + inline tag in
  gdd.md matching house style `(*...addition...*)` / `[RULING — user, DATE]`.
- Ground-truth-first paid off: `game/data/node_types.json` +
  `topology_graph.gd` confirmed basic 4 / mid 8 / high 16, "parallel pipes
  each count", and BOTH-ENDS port consumption before canonizing — the
  per-end ambiguity was the only edge-hunter finding (fixed pre-commit).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-prototype-build.md
# Field notes: packet-plumber-prototype-build

- 2026-08-08: the GoPeak Godot MCP install has NO `capture_screenshot` tool
  (briefing said it did — verify against disk). Visual verification path =
  in-game viewport capture: `get_viewport().get_texture().get_image()` run
  WINDOWED offscreen `--position -3000,-3000` (NOT -32000 — outside the
  renderable desktop → the viewport never clears → ghosted/overlapping text).
  The agent can't view images; `describe_image` (vision) is the only "eyes" and
  is flaky (returns empty / aborts) — retry, and it often only parses 1 image per
  call even when you pass several.
- 2026-08-08: SLA/loss uptime must be a ROLLING recent window (~last 10s), NOT
  cumulative-from-tick-0. Cumulative permanently tanks the average during the
  build phase (player reading onboarding + drawing first pipes) → pre-surge loss
  even with good pipes. Rolling forgives setup; the meter recharges once built.
- 2026-08-08: latency is an SLA METRIC, not a drop trigger (real packets don't
  drop when late). Drops = contention/queue-overflow/unreachable only. Also:
  decouple a cosmetic `vis_dist` (flows along the route) from bandwidth progress,
  and advance it ONLY when a packet is served — congestion then piles ALONG a
  clogged pipe (the readable panic) instead of vanishing. Cosmetic, excluded from
  the replay fingerprint; determinism holds.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-prototype-iterate-1.md
# Field notes — packet-plumber-prototype-iterate-1 (2026-08-08)

- **macOS offscreen windows freeze their compositor — in-game captures repeat the FIRST frame forever** (same image bytes while ticks advance; a "missing panel" burned an hour of debugging before I diffed frame hashes). Windowed-on-screen works until occluded; **movie mode is the reliable path**: `godot --path game --write-movie /tmp/out.avi --fixed-fps 60 -- demo` (renders via the engine, compositor-independent; the in-game capture log also updates in movie mode). Screenshots for verification: extract AVI frames with ffmpeg, or use the in-game /tmp/pp_captures which update in movie mode.
- **`submit_command` (or any snapshot emit) re-enters `_on_snapshot` synchronously** — a capture-automation hook that submits a command on `snap.tick == X` recurses infinitely (stack overflow at tick 800). Guard with a one-shot flag.
- **GDScript `Array` literals in ternaries don't infer `Array[StringName]`** — `var t: Array[StringName] = [&"a"] if cond else [&"b"]` errors at runtime; build the typed array with appends.
- **The weighted-random sink spread is LUMPY on small sink sets** — a 15u standard leg overflows (queue_overflow, email collateral!) whenever its house draws an unlucky streak during the surge; wide legs absorb the variance. Any balance change to sink counts must re-audit per-leg capacity vs the lump, not the mean.
- **A "reservation" heuristic must fall through rejected candidates to its fallback list** — a house wiring loop that only tried the reserved set left a house stranded for 500+ ticks (the reachable last-port router was never tried because an out-of-span reserved candidate blocked it).
- **Validate `submit_command`-adjacent wiring against the REAL bootstrap path**: `RunState.bootstrap` created `PacketFlow.new(p_catalogs)` WITHOUT balance → ms_per_tick + queue depth silently fell back to defaults; balance-tuned knobs did nothing in the game (the headless harness passed balance explicitly, masking it).
- **Balance cascade from map growth**: 4→9 houses broke three tuned constants at once — budget (3000→5200), surge volume (3→2: 60u chokes the 3-router mesh the port limits allow), queue depth (20→40). Retunes are documented in the data files; expect more during playtest.
- **Router mesh is a chain unless ports are planned**: growth routers link to the nearest junction → the mid router (8 ports) becomes the spine and its link saturates under aggregate satellite traffic. Star meshes (direct-to-mid links) need port reservation from the start. The demo's port squeeze IS the feature, but the autopilot had to play it smart to survive.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-routing-bandwidth-cost.md
# packet-plumber-routing-bandwidth-cost — field notes

- 2026-08-13 (routing-bandwidth-cost): a catalog FIELD addition re-blesses
  EVERY .t1 + .log.bin via the cat.hash fold — but it is PROVABLE fold-only:
  splice the OLD catalog_hash over new state-dump bytes 33..40, FNV must equal
  the old golden tick-1 (all 16 demos did); .log.bin diffs were exactly the 8
  header bytes; T2s never moved. Re-bless WITH that proof, not on assertion.
- 2026-08-13 (routing-bandwidth-cost): mixed-tier bundles price at the FATTEST
  member (min tier cost) — per-pipe min relaxation must match the ECMP
  equality test (`dist[v] + min_cost == dist[u]`), or a later cheaper member
  breaks the condition (unroutable). Two-pass collection (min cost first,
  then equality) is the deterministic shape.
- 2026-08-13 (routing-bandwidth-cost): narrow-tier test geometry needs spans
  <= 10 (max_span!) — the 2.2 diamond's 13-spans reject at draw; compact
  diamond (8,15)/(16,11)/(16,19)/(24,15) is narrow-legal. And Odin fmt strings
  need `{{`/`}}` for literal braces in expectf messages.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-routing-canon-amend.md
# packet-plumber-routing-canon-amend — field notes

- 2026-08-10: a lavish-gated docs deliverable dispatched into an **absent-user window** = long idle polls. The poll blocked ~6.5h overnight (user away, state.json frozen at open-time); re-running on each bash timeout is correct (queued feedback is never lost) — just hold the gate, don't escalate as blocked, and verify the verdict via `~/.lavish-axi/state.json` `sessions.<id>.chat[].text` (the compact poll `prompts[]` repr is ambiguous; "good" + `ended_by:user` = unambiguous approval through the gate channel — no Gru provenance check needed).
- 2026-08-10: canon-amendment blast radius always exceeds the briefing's named sections — grep-bound it. Here the briefing named GDD §M3/§M5 + arch §6.2/§6.3/ODN-9/10/E1/E29, but the radius ALSO caught: epics.md (E1.4/E1.5/E2.3/test-contracts said "load-balance"), §4 ASCII diagrams (box edit MUST be width-preserving: `span, LB)`→`span,bndl)` kept 13 chars), §5.1 ODN-9/10 summary rows, §8.1 catalog + §8.2 data model + §15.1 coverage, and decision-log.md (history-preserving supersession APPEND, not a rewrite — matches the project's amendment pattern).
- 2026-08-10: disambiguate the two "E" namespaces before editing — the briefing's "E1/E29" were the **arch edge-case behaviors** (E1–E32 table at §11.7 + §6.2), NOT the GDD epics (E1–E11 in epics.md). And `architecture-v1.md` is the SUPERSEDED GL5.2/Godot arch (ADRs); the live canon with the ODN-* decisions + E1–E32 edge cases is `odin-architecture-v1.md` — only the latter was amended; the former stays historical (flagged in the PR).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-routing-explorer.md
# Field-note shard — packet-plumber-routing-explorer (2026-08-10)

Minion: packet-plumber-routing-explorer · Model: zai-coding-cn/glm-5.2 · No-PR lavish exploration job.

- **2026-08-10 (packet-plumber-routing-explorer):** lavish interactive SVG sims — parallel pipes between the same node pair overlap into ONE visible line unless you fan them perpendicular (compute each pipe's arc offset from sibling count: `(idx-(n-1)/2)*spacing`); and a proximity-check (`Math.abs(p.x-n.x)<8`) for packet-travel direction OSCILLATES (flips the from/to every other tick → packet jitters in place, looks "no animation") — track explicit `fromNode`/`toNode` per edge instead (mirror the real `current_node` walk).
- **2026-08-10 (packet-plumber-routing-explorer):** the lavish poll's `dom_snapshot` is a first-class self-check — it caught a DOM-throw render bug (`insertBefore(ring, svg.firstChild.nextSibling)` where nextSibling wasn't a child of the path → NotFoundError aborted `draw()` mid-loop, leaving only the first node) AND confirmed every fix without a browser. Read the dom_snapshot every poll; it shows exactly what rendered (text content = node glyphs, missing symbols = a throw).
- **2026-08-10 (packet-plumber-routing-explorer):** glm-5.2 single-pane built a ~100KB faithful JS sim (BFS `compute_route`, `pick_pipe`/`rr_next`, `qos_allocate` WFQ, severance reroute) fine end-to-end; a human-in-the-loop lavish iteration loop is sequential by nature (annotate→apply→react), so mega-minions DON'T speed it up — correctly deferred entirely during a concurrent Perkins glm-5.2 round per Silas's ruling (429-avoidance), then lifted; never needed. Build the artifact as ONE file via the `write` tool (file write, not a pipe → no 85KB pipe-buffer truncation); `node --check` the extracted `<script>` before serving.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-routing-forecast-shift.md
# Field notes — packet-plumber-routing-forecast-shift (Job C, R4)

- The 3.3 lane queues are STRICTLY FIFO at full pipe capacity per packet
  (serve_bundle_lane walks the array; windows repeat until capacity consumed)
  — a packet behind N queued packets waits N x edge-transit, so demo transit
  comments must count queue position, not lone-packet transit; verify capture
  narratives with a packet-state dump test, not arithmetic.
- The app's step passes `{}` (edits land via fast-path + are logged for
  replay) — tests exercising "the real edit path" should use the harness
  flavor (log-only + step_n) to stay aligned with the replay gate; the pixel
  capture narrative (which leg carries packets) is verifiable headlessly with
  a PIL blob-scan of email-color pixels vs screen-space segments (camera:
  scale min(1280/1040, 720/780), off_x 160).
- draw_forecast_panel's nil-preview default keeps harness T2 byte-identical,
  but a preview-non-nil + empty-forecast path still must NOT draw the weather
  card (the zero-pixels-when-empty contract is per-card, not per-call) — a
  self-review catch.
- r2 addendum: Odin `defer` is BLOCK-scoped — a `defer delete(sh)` inside a
  loop's if-block frees the buffer before the code after the block reads it
  (the preview golden rendered magnet=0 from freed-but-intact memory), and a
  block-local struct whose address escapes dangles past the block; hoist both
  to the loop body. Also: `var x T` is NOT Odin (use `x: T`), and a
  `odin build | head && echo OK` pipeline lies about the rc — check rc
  explicitly or the STALE binary silently re-blesses goldens (hit twice in
  one round).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-setup-brief.md
# Field notes: packet-plumber-setup-brief

- 2026-08-05: the briefing listed source-material paths under the
  orchestrator-root `_bmad-output/planning-artifacts/`, but the concept +
  forge files actually lived in the REPO's own
  `_bmad-output/planning-artifacts/` (same relative path, different root).
  For a repo-local job (cwd = the repo), `find` the planning artifacts
  *inside the repo* before declaring ENOENT against the orchestrator root.
- 2026-08-05: Godot `aspect=expand` + "both orientations" needs a SQUARE base
  (720×720) per the multiple-resolutions doc's explicit tip — a rectangular
  base yields a different scale factor per orientation. The user then ruled
  landscape-only, so 1280×720 + `orientation=0` (SCREEN_LANDSCAPE) won.
  Verify viewport/orientation semantics against the Godot
  multiple-resolutions doc before committing display settings; the
  `--headless --check-only` gate is invalid (hangs) — use `--import` then
  `--quit-after 600`.
- 2026-08-05: `gh pr create --body "$(cat <<'EOF' … EOF)"` choked on the
  body's embedded quotes/backticks even with a single-quoted heredoc — use
  `--body-file <file>` for any non-trivial PR body. (General shell lesson,
  reusable across jobs.)

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-sprint-plan-v1.md
# Field notes — packet-plumber-sprint-plan-v1 (2026-08-10)

- **Ambiguous terse verdicts — paraphrase before applying the change.** A one-line freeform lavish reply ("no mvp same as in the full game") got read as "flip to best-effort game-wide"; it actually meant "keep Standard, MVP=full-game for the default lane only." I over-rotated, committed the flip across 8 locations, then had to revert everything. Cost: a full extra render/reply cycle + user friction. Lesson: when a verdict/steering reply is terse or could cut two ways, paraphrase it back ("reading you as X — confirm?") BEFORE applying a sweeping change. Cheaper than a revert.
- **marked (vanilla `npx -y marked --gfm -o`) emits NO heading `id`s** — a TOC built from `<h2 id="...">` finds nothing. Inject slugged ids yourself (regex `<h2>(text)</h2>` → `<h2 id="slug">`) before building nav. Also: the lavish doc-review pattern that works is `marked --gfm -o <body.html>` (file, no pipe) → node script wraps in a DaisyUI shell + sticky TOC → `lavish-axi <html>`; the HTML auto-reloads in-browser when you re-run it after edits.
- **For fragile big-block markdown edits, a 10-line Python script beats the edit tool.** The `edit` tool is atomic-per-call (one bad oldText rejects the WHOLE batch) and exact-matching multi-line blocks with em-dashes/curly-quotes/indentation breaks often. Reading the file in Python and anchoring `.replace()`/`.find()` on unique substrings is robust and lets you verify with asserts. (Also: the bash tool's cwd resets to the repo root EVERY call — `cd` must be in the same command; bit me ~5× this job.)

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-sprint-replan-v2.md
# Field notes — packet-plumber-sprint-replan-v2 (2026-08-11)

- **Grep the architecture citation before trusting a sprint plan's engine/routing.** v1 sprint-plan/stories were dated *after* the Odin pivot (2026-08-08) but drafted in Godot/GDScript (`RefCounted`, `AC-FinLT`, `scripts/core/`) and cited `architecture-v1.md` (the GL5.2 Godot arch), NOT `odin-architecture-v1.md` — and on the reversed BFS+RR/LB routing. A "recent date" on a planning doc does NOT mean it's on the current stack; check which architecture file it cites + grep its code samples.
- **"No BFS legacy" is precise, not absolute.** The mandate bans the prototype's spawn-time BFS route cached per packet + the RR/weighted LB at parallel pipes. It does NOT ban a deterministic SPF computing the forwarding table internally — arch ODN-10 rule 1 explicitly permits `(junction,dst)→next hop` via deterministic BFS/SPF (insertion-order tie-breaks). State this precisely in any routing plan or a reviewer flags a phantom contradiction with the "no BFS" mandate.
- **Lavish multi-question Decide answers can arrive as a compact code ("1A,2B,3A"), not prose.** Parse question-number + option-letter. Also: an empty freeform-text field still arrives as a `"Freeform message"` prompt tag with empty `text` — the verdict was in the prior `message` prompt, not the empty one. (User ended the session immediately after — `session_ended: true, ended_by: user`.)

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-surge-explainer.md
# field notes — packet-plumber-surge-explainer (2026-08-15)

- v2's `bandwidth_demand` is loaded into the catalog (catalog.odin:455) but NOT consumed by the flow service pass (flow.odin:405 serves flat `packet_bandwidth` 30 for every packet) — verify per-class transit claims against serve_bundle_lane, not the catalog comment.
- The drop "ladder" (BE → Standard → Express) is lane-ordered, not class-ordered, and BOTH MVP classes default to the Standard lane — "email pays first" is only true after 5.8 categorization; the 99-vs-95 screenshot gap is run arithmetic, not a priority rule.
- Multi-edit `edit` batches reject atomically: a duplicate oldText (accidentally included twice) fails the WHOLE batch silently — dedupe targets; lavish session-end can arrive with the verdict in the final prompt (check state.json chat if the poll seems to miss one).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-terminal-assets-5.11.md
# packet-plumber-terminal-assets-5.11 — field notes

- The 7.1 sprite pipeline regen (Blender headless) is PIXEL-IDENTICAL but PNG-encoding NON-DETERMINISTIC run-to-run — after adding sprites, `git checkout` the existing PNGs so only new files + sprites.json land; bboxes are stable so the manifest diff stays additive.
- Extending the sprite sheet REQUIRES mirroring `SPRITE_COUNT` + the `files` list in app/render/sprites.odin (sprites_parse_boxes rejects len(order)!=SPRITE_COUNT and the whole sheet falls back to primitives = golden shift) — that's sheet/manifest data, distinct from role→index draw wiring (5.11's).
- The canon blend (`art-renders/blend-sources/pp-scene-light-vista.blend`) opens + re-saves cleanly via headless Blender (`bpy.ops.wm.open_mainfile` + `exec(open("pp_lib.py").read())` then save_as_mainfile) — the provenance path for "the blend gains new models".

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-traffic-model-design.md
# Field notes — packet-plumber-traffic-model-design (2026-08-15/16)

- Source material can live as UNTRACKED files in the MAIN checkout (surge-explainer/ was untracked in /Users/moses/code/packet-plumber, absent from the worktree) — find untracked briefing sources there, not in the worktree.
- The GDD M1 tier table (narrow 10/standard 25/wide 50/backbone 120) is STALE vs the shipped catalogs (5/15/40) — design specs must cite the shipped data/*.json as ground truth and flag the drift (the terminology audit owns the GDD-table refresh).
- Design tension surfaced late: per-terminal caps + era-3 demand/×10 surge → the MVP surge can silently stop landing on 4–6-node maps; the fix is per-type caps (content_host caps vs its own throughput, not the residential cap) + re-validating era-3 demand with 5.1 growth pacing — put such consequences in the artifact's Risks, never hidden in the spec.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-ue-bootstrap.md
# Field notes — packet-plumber-ue-bootstrap (2026-08-20)

- No UE on the machine → the dual-runner spine design (UE-header-free
  headers + standalone `tests/spine_check.cpp`) proved the ODN-9/11 port
  byte-exact against the Odin vectors BEFORE any engine install; engine-
  gated CI gates SKIP-with-reason, never false-green.
- `npx -y ue-mcp <uproject>` boots engine-free (27 tools + the Epic 5.8
  registry snapshot) — repo-root `.mcp.json` (stdio) is the wiring that
  works with pi today; the official Unreal MCP server needs the editor
  running (loopback HTTP :8000).
- UE module API surface (BuildSettingsVersion, EAutomationTestFlags names,
  commandlet run-name == class minus U) is unverifiable without the
  installed engine — flagged in AGENTS.md; re-verify before trusting a
  green engine build.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-ue-slice-1.md
# Field notes — packet-plumber-ue-slice-1

- UE-MCP bridge: `ue-mcp init` is pty-only; deploy via the package's
  `dist/deploy-cli.js` directly, then REBUILD (a stale editor instance shows
  "Incompatible or missing module"). The bridge port.json goes STALE on
  editor restarts — rewrite it from `Saved/UE_MCP_Bridge/instances/<pid>.json`;
  pkill misses old editors (kill by pid — multiple instances share the
  project and confuse everything). Stale `Binaries/Mac/*.dylib` pile up (43!)
  and the editor loads the HIGHEST — a full wipe+relink can produce an
  INCOMPATIBLE module stamp; keep at least one old dylib.
- C++-only UUserWidget (no designer asset) must build its tree in
  `RebuildWidget()` — NativeConstruct runs after the Slate widget exists and
  setting RootWidget there silently renders nothing. Same for
  `GetCachedGeometry` at construct time: fall back to the design size and
  re-fit on tick.
- UE UMG canvas is DPI-SCALED: the widget geometry (e.g. 1896x1081) is the
  layout truth, NOT the game viewport (1280x730) — the fit must use the
  widget's local size or everything renders shifted. Runtime
  AddChildToCanvas in NativeTick never paints — pre-create the pool in a
  layout pass (RebuildWorld) and only reposition in tick; every ClearWorld
  must be paired with a pool rebuild; FSlateRoundedBoxBrush ImageSize
  defaults to ZERO (explicit it or the widget is invisible).
- VERIFY SCREENSHOTS WITH PIXEL SCANS, not vision alone: the r1
  "mid-traversal" frame had zero dot pixels (the vision model hallucinated
  it — I trusted a single vision read). The dot was ALSO genuinely broken
  (the cascade above). After fixing, pixel-scan (4 positions across 12
  frames) + vision agreed. Never re-bless evidence on a vision claim.
- UE global `FIntPoint` (TIntPoint<int>) collides with `PP::FIntPoint` in
  engine-side files — qualify `PP::FIntPoint` everywhere outside the sim
  headers. The editor re-writes the AndroidFileServer section into
  DefaultEngine.ini on EVERY boot — disabling the plugin fixes it.
- Enhanced Input runtime actions must be created in the CONTROLLER
  CONSTRUCTOR — SetupInputComponent runs BEFORE BeginPlay, so BeginPlay-
  created actions are null at bind time (dead mouse, masked by MCP-bridge
  drawing). The module test binds + Execute()s the returned binding to
  synthesize the trigger headlessly.
- Test-module headers: the game module's headers must live in
  `Source/PacketPlumber/Public/` for the tests module to include them; the
  API macro (PACKETPLUMBER_API) is auto-defined by UBT — mark cross-module
  classes with it.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-1.1-walking-skeleton.md
# field notes — packet-plumber-v2-1.1-walking-skeleton (story 1.1: headless determinism spine + harness)

Lessons for future PP-v2 minions (the determinism spine is load-bearing for every later story):

- **Current Odin `core:testing` API** = `testing.expect(t, ok, "msg")` / `testing.expectf(t, cond, fmt, args)` / `testing.expect_value(t, got, want)`. NOT `tfail`/`tfailf` (old/prototype), NOT method-call `t.expect(...)` (fails — use the qualified `testing.expect(t, ...)` form). `expect_value` takes NO message string (its 4th param is a `Source_Code_Location`).
- **`delete` on a `[dynamic]` field is `delete(arr)` with NO `&`** in current Odin; `new(T)` heap pointers can't be `delete`d at all — prefer stack locals (`x: T; defer run_destroy(&x)`) for test state and `defer delete(returned_dynamic)` for returned `[dynamic]`s (the test mem-tracker flags leaks as warnings).
- **`package core` COLLIDES with Odin's runtime `core`** for `-build-mode:obj`/`-lib` output naming — those builds emit ONLY runtime objects, not the user package's code (vacuous but exit-0). The definitive ODN-1 purity gate is the import grep (`tools/lint.sh` gate 1: zero forbidden imports) + `nm` of a binary that LINKS core (e.g. `odin build harness -out:bin/harness` → `_core::*` symbols present, ZERO raylib). Reconcile the §16.3 `-build-mode:obj` artifact gate in a later CI-gate story; do NOT rename `package core` (architecture + prototype both pin it, and `odin test core` + `import pp "../core"` work fine).
- **`odin build <pkg> -out:bin/x` fails with a clang linker error if `bin/` doesn't exist** — `mkdir -p bin` first. Bless goldens with `odin run harness -- save boot` (compiles to a temp, no bin/ needed).
- The spine's `step` is a heartbeat (one owned-RNG draw/tick folded into a `tick_nonce` state field) — it ties the RNG into the step path so replay-equality is non-vacuous. Story 1.2 replaces `tick_nonce`/`applied` with real Topology state; the serialize/step/hash/log plumbing is unchanged.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-1.2-window-draw-pipe.md
# packet-plumber-v2-1.2-window-draw-pipe — field notes

- **bmad-tooling worktree quirk confirmed live:** every edit landed in my worktree (`/Users/moses/.herdr/worktrees/packet-plumber/v2-1-2-window-draw-pipe`) — verified via `git status` from my cwd after each phase; the main checkout (`/Users/moses/code/packet-plumber`) stayed untouched. Always `pwd` + `git rev-parse --show-toplevel` first; never assume the tooling's resolved root.
- **`free_all(context.temp_allocator)` per tick nukes demo.captures** if they're temp-allocated — the 1.1 spine's per-tick free_all was safe because 1.1 demos had no dynamic fields; the moment a demo carries `captures`/`draws` read DURING the tick loop, allocate them with `context.allocator` (persistent), not temp. Symptom: "captures=1" logged but no PNG written (the capture loop iterated freed memory).
- **rlsw T2 capture path works headless via `rl.InitWindow` + `LoadImageFromScreen`** (no GPU/display) — port the prototype's `goldens.odin` (flip + BGRA→RGBA swizzle) verbatim; `CIRCLE16`-style constant arrays can't be indexed by a runtime index in Odin (assign to a local first). The SW raylib build (`tools/build_raylib_sw.sh`) takes ~40s + a github clone; kick it off in the background before coding.
- **Odin nested procs are non-capturing** — a `clone` proc defined inside `make_drift_mutations` couldn't see `src`; lift helpers to module scope or pass params explicitly.
- **`make([]u8, len, allocator)` for a slice** is finicky in this Odin build; prefer `make([dynamic]u8, len, allocator)` then pass `dyn[:]` (matches the core pattern that compiles cleanly).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-1.3-packet-flow.md
# packet-plumber-v2-1.3-packet-flow — field notes (minion shard)

- **id-0 sentinel trap (bit me, then the tests caught it):** PP node/pipe ids are 0-based (first spawned node = id 0, first pipe = id 0), so `edge==0` / `at_node==0` CANNOT be the on-edge/at-node sentinel — a packet forwarded onto pipe id 0 looked "at a node" and never moved. Use an explicit `on_edge: bool` flag (or a +1 id scheme like the routing table's `next/pipe` arrays). The flow tests went red → green on this fix; the red was the negative-control proof the tests bite.
- **The replay gate re-creates run-setup (fixture) but NOT flow demand by default.** The flow demand is run-setup (like the fixture), NOT in the action log — so the ODN-11 replay diverged at tick 1 until I threaded the demo's `spawn` intents through `replay_hashes` (live lowers them via `lower_spawns`, replay re-creates them identically). Any future run-setup added to the sim (director plans, etc.) needs the same treatment in BOTH the live + replay paths.
- **T2 pixel goldens need the rlsw software renderer via `tools/harness.sh`** — `odin run harness` links the stock GPU `vendor:raylib` and renders a SOLID BLACK frame headless (no GPU context). And: the pinned `.odin-version` `dev-2026-08` downloads as the SAME `nightly+2026-08-06` / `902106f` that's already on the machine — so the local toolchain IS the pinned release; a T2 mismatch is a real diff, not a version drift.
- **Per-hop forwarding confirmed structurally** (grep, not just prose): `core/routing.odin` + `core/flow.odin` have NO `route[]` field on Packet, NO `compute_route` BFS-on-packet, NO rng draw in routing/flow (ECMP hash is slice 2). The forwarding table is DERIVED from the topology → not hashed (hashing it would bind replay to the build algorithm). 4-rule spine rule 1 trigger = `Topology.gen` (increments on spawn/draw), checked in `step` before `flow_step`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-1.4-win-lose-stub.md
# packet-plumber-v2-1.4-win-lose-stub — field notes

- Adding fields to Run_State's serialized form (`state_writer` in serialize.odin) re-blesses EVERY `.t1` manifest (the FNV input changes even for zero-valued new fields) — boot/draw/flow all re-blessed for 1.4. The `.log.bin` files stay UNCHANGED iff `LOG_VERSION` is unchanged (1.4 added no Command variant → LOG_VERSION stays 2). Precedent: 1.2 re-blessed 1.1 the same way.
- Win/lose run-setup (goal/tick_cap) is run-setup, NOT in the action log — it MUST thread through BOTH `run_demo` (live) + `replay_hashes` (replay), same spine rule as flow demand (the determinism field-note). 1.4 threads it as a `Session_Cfg` param through `replay_hashes`/`verify_replay`/`run_replay`/`drift_check`; miss any caller and ODN-11 replay diverges at the terminal tick.
- The terminal-event barrier is a `step` early-return when `state.terminal` that does NOT advance `state.tick` (the run freezes at the terminal tick) — this makes post-terminal manifest hashes byte-identical, so the barrier is SELF-DOCUMENTING in the `.t1` (win.t1: ticks 47-60 identical; lose.t1: tick 60 distinct, 61-64 frozen). The "exactly one terminal event per run" (E17) is visible there.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-2.1-bundles.md
# field notes — packet-plumber-v2-2.1-bundles (Story 2.1)

- The determinism-spine-preserving bundle design: `Packet.edge` stays a PIPE id (the representative/first member of its bundle); bundles are a DERIVED struct rebuilt on topology change (rule 1), NOT serialized (same as routing). Zero serialized-state change → slice-1 T1 hashes + T2 pixels both byte-identical, no re-bless. A bundle-id approach would have changed `p.edge`'s meaning + forced re-blessing all slice-1 goldens (false signal of behavior change).
- T2 merge-pop golden = the SETTLED bundled frame, not a mid-animation frame. The harness captures single frames per tick (no cosmetic-clock dimension); the pop juice is live-app cosmetic (ODN-15). Don't try to capture a transient pop in the harness — it's not how the single-frame capture path works (consistent with slice-1 settled goldens).
- The no-LB grep-gate (lint gate 5) must strip `//` comments BEFORE grepping, or the prohibition's own explanatory prose ("round-robin/weighted LB are deleted") false-positives. Strip with `sed 's://.*::'` per file, then grep code-only. Behavioral pin (transit time) complements it.
- Bundle render width that preserves slice-1 pixels EXACTLY: width = tier_width(highest_tier) + (count-1)*EXTRA. Single-member (count=1) = bare tier width → pixel-identical. Measured: bundle 8px vs single 6px (33% fatter) + pipe_fiber inner core. The vision model was UNRELIABLE at this resolution (hallucinated text + missed the 2px diff) — measure goldens programmatically (PIL pixel diff + thickness count), don't trust describe_image for sub-5px render differences.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-2.2-ecmp.md
# packet-plumber-v2-2.2-ecmp — field-note shard

- 2026-08-11 (self): the absolute-path trap bit AGAIN (reinforces the
  2026-08-11 field note). cwd was the worktree, but my `write`/`edit` calls
  used absolute paths to `/Users/moses/code/packet-plumber/...` (the MAIN
  checkout) — picked up from reading source material — so all 3 edits landed
  in the main checkout, worktree clean. `odin test`/`lint`/`harness` all
  `cd`'d to the main checkout too, so they passed against the WRONG tree.
  FIX: resolve every edit to the WORKTREE path (cwd-relative or
  `~/.herdr/worktrees/<repo>/<slug>/...`); after edits, `git status` from
  cwd BEFORE trusting a green test run. Recovery: cp the files into the
  worktree, cmp-verify, revert the main checkout, re-run gates in the
  worktree.
- 2026-08-11 (self): the rlsw software-renderer harness ALREADY EXISTS and
  works (2.1 blessed pixel goldens; `tools/build_raylib_sw.sh` clones raylib
  6.0 + builds `libraylib_sw.a` ~40s). A briefing carry-forward claimed "T2
  pixel-unverified until the rlsw harness exists" — STALE (ground-truth
  first: the goldens/ pixel dirs + the shadow build disproved it). rlsw is
  gitignored, so it's ABSENT in a fresh worktree — point the harness build
  at the main checkout's shadow: `ODIN_ROOT=<main>/tools/raylib-sw/shadow
  odin build harness -out:bin/harness` (compiles the worktree's core/harness
  against the main's pre-built rlsw).
- 2026-08-11 (self): ECMP determinism design that kept ALL goldens valid —
  (a) the routing table is DERIVED (not serialized), so restructuring its
  internal layout (flat single-hop -> packed equal-cost sets) has ZERO T1
  impact; (b) `ecmp_pick % 1 == 0`, so single-path scenarios (count==1)
  produce byte-identical per-packet paths; (c) ECMP only engages at count>=2
  junctions no existing scenario has. Net: purely additive, no re-bless. The
  pure hash reuses `splitmix64` (the same primitive rng.odin uses for seed
  expansion — sanctioned by ODN-9 as the "deterministic finalizer, NOT a
  sim-rng draw"); a naive Perkins grep for `splitmix64` in routing would
  false-positive — the real guard is "no rng_next/rng_range/state.rng in the
  routing path", backed by a behavioral test (flow-run vs no-flow-run rng
  state bit-identical).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-2.3-demolish.md
# packet-plumber-v2-2.3-demolish — field-note shard

- 2026-08-12 (pp v2-2.3): a demo with ZERO `capture at <ms>` lines validates via T1 hashes + the replay gate ONLY (no PNG golden needed) — the clean "pixel-deferred" golden path. Adding a new demo VERB (e.g. demolish) = extend `parse_demo`'s nested `at`-switch + `lower_intents`; the verb lowers into the action log, and replay handles it via the blessed log (NO replay-path change — `replay_hashes` re-applies logged commands generically).
- 2026-08-12 (pp v2-2.3): the edit-tool nested-switch trap bit again — a 5-edit batch to `harness/demo.odin` was REJECTED SILENTLY (all 5 lost) because ONE oldText had shallow indentation for a 3-level-deep switch (content is 4 tabs, not 3). Re-read the EXACT tab depth of nested code before authoring batch oldText; the tool reports the failed edit index but applies NONE on a mismatch.
- 2026-08-12 (pp v2-2.3): the E29 fix was a ONE-LINER by design — `Packet.at_node` is never cleared when a packet forwards onto an edge, so it already holds the departure junction while on-edge; the pre-2.3 "pipe vanished" path wrongly reset `at_node = p.src` (correct only for the first hop). Dropping that line makes multi-hop re-forward-at-departure live. The junction-demolish-strands-packet edge case needed an explicit dead-node CULL (E1's "drop" half) — add it whenever a topology edit can tombstone a node a packet is resident at.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-3.2-lane-qos.md
# Field notes — packet-plumber-v2-3.2-lane-qos

- 2026-08-13 (packet-plumber-v2-3.2-lane-qos): the acceptance's "existing goldens must not shift — STOP and flag, do not re-bless" tripwire fires on ANY balance.json content addition: ODN-11 folds catalog bytes into the state hash, so the T1 manifests + log headers reject with "catalog drift". Prove behavioral identity BEFORE blessing (T2 pixels pass against old PNGs + a reconstruction proof: splice the OLD catalog_hash into the new state dump at byte 33 → fnv must equal the blessed tick-1 golden; the harness's own save message says "re-bless deliberately" — the 3.1 story did the same). Flag loudly in the PR; don't halt.
- 2026-08-13 (packet-plumber-v2-3.2-lane-qos): T1-dump additions must be ABSENT-WHEN-EMPTY, not just sparse (a zero count still shifts every default-run hash). Also: `fmt.tprintf` has NO allocator param on the dev-2026-08 pin (use `fmt.aprintf(..., allocator = context.temp_allocator)` for per-frame HUD strings); `_ = ps` leftovers trip lint gate 4; a zero-value i64 selection sentinel (0 = live pipe id!) must be explicitly -1 at init AND restart.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-3.3-contention.md
# Field notes — packet-plumber-v2-3.3-contention

- 2026-08-13 (packet-plumber-v2-3.3-contention): a deferred-splice (collect drop indices in a pass, splice after) needs an ASCENDING sort before the descending splice — the drops list is in APPEND order, and removing a lower index first shifts the higher ones (two same-tick sheds [11,9] silently spliced the WRONG packet; caught by a white-box pin + the review swarm's F-verification, but the goldens already blessed with the bug had to be re-blessed). Any new deferred-multi-removal in core: sort-then-descending + a same-tick-double-shed regression test.
- 2026-08-13 (packet-plumber-v2-3.3-contention): spatial-lane rendering must derive the lateral axis from the BUNDLE's canonical lo→hi direction and its max-member tier — using the packet's own depart→arrive direction mirrors the normal on the reverse traversal (packets render in the WRONG band for half the traffic; the story's own demo showed it) and the packet's own tier mis-centers mixed-tier bundles. The 2-hunter review swarm caught it; verify bidirectional traffic visually in the blessed captures.
- 2026-08-13 (packet-plumber-v2-3.3-contention): the E9/E22 shed rule "the arrival drops when it is the shed target" is correct at admission (the arrival's lane is full ⇒ non-empty ⇒ the target can't be higher priority) but INVERTS at the pool guard (the arrival's lane may be absent from the pool — an all-Express pool would shed Express for a Standard arrival). Priority rule that holds everywhere: admit only when the target is STRICTLY lower priority than the arrival's lane (`shed_lane > arrive_lane`).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-3.4-sla.md
# packet-plumber-v2-3.4-sla — field notes

- Span trap: test-seed fixture nodes sit 12 tiles apart — a `narrow` pipe draw is silently REJECTED (max_span 10) → no route → packets pile at their source with zero events; for narrow-tier tests, spawn nodes ≤10 tiles apart. Cost me a debug probe cycle.
- `record_run` clears `state.events` every tick (ODN-14 drain) — any end-of-run event scan is vacuous; collect the stream while stepping (the `sla_record_run` pattern returning hashes + events).
- Cumulative-loss breach is NOT monotone: later deliveries dilute the ratio below tolerance, so a transition-style Exit would fire falsely — the Loss latch must be sticky-Enter by contract; "monotone" applies to the counter, never the ratio.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-3.5-node-placement.md
# packet-plumber-v2-3.5-node-placement — field notes

- Catalog edits are GOLDEN-POISONED in PP v2: `cat.hash` folds every catalog byte and `replay_hashes` rejects on drift — any node_type/balance.json change invalidates ALL blessed goldens. Wire new rules as core consts (ported values + comment) until a legitimate re-bless; port counts read from the existing `port_capacity` field.
- LOG_VERSION bumps (serialize.odin) force a golden-log re-bless — do it as `harness save` for ALL demos, then byte-verify every `.log.bin` differs ONLY in the version field (python diff vs `git show HEAD:`) and every `.t1`/`.png` is untouched; that diff IS the "don't re-bless without checking" proof.
- The harness's `capture_frame` passes a ZERO `Drag_State` — any new ghost gated on a plain `>= 0` int field (e.g. `placing`) draws in every T2 golden; gate on `drag.active && placing >= 0` and reset `placing = -1` in `start_run` (a `{}` struct reads as type 0).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-4.1-warning-forecast.md
# packet-plumber-v2-4.1-warning-forecast

- 2026-08-13: Odin `strings.replace` in a test can return "replaced=true" while the runtime doc still holds the old substring when the fixture's raw-string newlines don't match the file's — pin multi-line replace1 rows via single-line anchors or byte-verify; and test-catalog `Balance` fields MUST mirror data/balance.json (zeroed `warnings` thresholds made zero-load read as 🔴 — every node red at tick 1, silently shifting every dump).
- 2026-08-13: PP-v2 sim truth — the routing table gives COMPLETE paths only: a packet with a missing leg waits at its SPAWN node (not "at the router"), and the E9 ladder means at-node backlogs only form from unroutable piles; the honest node-strain measure is a failed-forward counter (`Packet.waiting_ticks`), and pipe pressure must be measured vs the lane bound (occupancy÷cap reads 200% for one packet on a standard pipe — busy-flicker). Golden re-blesses: every `.t1`/`.log.bin` shifts on any balance.json content change (catalog_hash fold, the 3.2 precedent); zero-traffic demos' T2s stay byte-identical — the negative proof.
- 2026-08-13: the harness T2 capture can draw HUD (the forecast panel) via the render package — `rl.DrawText` works in the rlsw software renderer (verified: text renders; framebuffer is BGRA — swizzle before comparing); the pulse animation must be tick-derived (pinned table, no transcendentals) or T2 goldens drift.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-4.2-surge-crisis.md
# field notes — packet-plumber-v2-4.2-surge-crisis

- The E9 lane queue at admission is the flow's ONLY saturation evidence — the SETTLED queue oscillates ±1-2 around the bound on the service/completion phase, so an engine that scans eval-time state alone chatters or misses saturation; make the drop event carry its shed bundle (admission-time truth) + add resolve hysteresis (bound−margin + no-drop + no-bound-lane) or the trigger/resolve pair fires every few ticks on any marginal network.
- The basic router's 4-port cap is a fixture-design constraint, not a detail: a "fix" that adds pipes to a full router silently rejects (Router_Ports_Full → replay_error latched) — swap (demolish-then-draw) or size the healthy fixture to 2 pipes/side; a single path can never carry the 20/tick surge (6-pack lane bound) — "within capacity" REQUIRES multi-route ECMP or lane-splitting.
- Build the harness ONLY via tools/harness.sh (ODN_ROOT=the rlsw shadow) — a bare `odin build harness` links the stock GPU raylib and produces R/B-swapped golden frames (921600/921600 pixel diffs) that look like a render bug.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-4.3-network-health.md
# packet-plumber-v2-4.3-network-health — field notes

- The E9 lane bound (not the pool) dominates saturation timing: a narrow path
  breaches the WINDOWED SLA at ~tick 5 (2 arrivals/tick vs 0.083 service), so
  grace+death land at ~405/~455 — measure with a probe, don't model the pool.
- The windowed-exit latency: the E30 exit needs a FULL window slide after the
  drops stop (~200 ticks) — the grace must exceed window+drain or the recovery
  is unwinnable; the prototype's grace 200 @10Hz = 20 s (400 @ 20 Hz), not 10 s.
- The 4-port router cap + the real base demand (120 u/tick) force 2+-router
  recovery/win fixtures (ECMP); a single router physically cannot serve it.
- A demolish-only "fix" clears the windowed breach (no pipes = no drops = 0%
  loss) — re-saturate by re-drawing, and remember Cmd_Place_Router enforces
  PLACEMENT_MIN_SEP_TILES (7): a 6-tile-away spot silently rejects the fan.
- The `.log.bin` re-bless for a catalog-hash fold is EXACTLY the 8 header
  bytes (cmp-proven); zero old T2 PNGs change when the new HUD draws
  zero-pixels-when-disabled — that is the negative proof.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.1-map-growth.md
# Field notes — packet-plumber-v2-5.1-map-growth

- The write/edit TOOLS resolved relative paths against the MAIN checkout (`/Users/moses/code/packet-plumber`, branch `v2`), NOT my worktree — ALL my growth code + goldens landed there; recovered by cmp-verified copy into the worktree + `git checkout --` restore of the main tree. Absolute worktree paths for every file tool, ALWAYS — the 2026-08-07 relative-path trap, re-bit on PP.
- Odin cannot index a file-scope `::` const array at runtime ("Cannot index a constant") — and core keeps ZERO file-scope vars (lint gate 2): use a proc-local value array for small tables (the growth direction LUT).
- Growth is the one branch where a same-tick re-step (the step_once test convention) is NOT idempotent — the rng hasn't advanced, so a re-plan can find a second valid spot and double-spawn. Any future tick-gated, rng-drawing branch in step needs the same non-serialized last-tick guard (`growth_last_tick`). rng_range draws NOTHING when hi <= lo — per-attempt draw counts vary with deterministic state; keep draw order + count pure functions of state or re-bless goldens.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.10-narrow-access.md
# packet-plumber-v2-5.10-narrow-access

- A catalog tier bump (narrow 5 → 10 u/s) is NOT a one-line change: it re-times every narrow-path test — the health/crisis fixtures' "saturated at base demand" premise died (queue on-edge ~4 < bound 6 at base; streaming now breaches via LATENCY ~7 instead), and ~6 tests' exact ticks had to be re-read from the sim (scratch-instrument, print, re-pin — never guess). Budget for the ripple; the golden re-bless partition (fold-only vs behavioral) is the sanity check: T2 pixels moved ONLY in the 6 narrow-pipe demos.
- Fold-only re-bless proof that works: (a) `cmp -l` every .log.bin vs HEAD — exactly 8 bytes @ 18..25 (the LOG header's catalog_hash, 0-indexed 17..24 — NOT the state dump's 33..40); (b) for era-0/no-narrow demos, a scratch core test replicating the demo (watch `use_fixture = true` DEFAULT — boot seeds the 3-node fixture!) that splices the old hash into the tick-1 state dump at 33..40: FNV must equal the old golden tick-1 (both directions verified byte-exact).
- The honest-signal fixture craft: an aggregation pin needs the SOURCE-side zero-drop assertion (drops at narrow access bundles == 0, resolved via bundle_of_pipe AFTER the run — the bundle view settles only once draws apply) AND a fat host drop (wide) or the host's own leg becomes the choke ahead of the shared uplink (295/317 drops landed there first try); 12 homes spread thin enough that even sink-side bursts stay under the access capacity (6 homes leaked 4/117).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.11-terminal-types.md
# field-notes shard — packet-plumber-v2-5.11-terminal-types

- **`node_types.json` array order is T1-VISIBLE**: the topology serializes `node_type` as a u16 index, so inserting a new type MID-array shifts existing indices and breaks the fold-only re-bless proof (the state dump differs beyond the 8-byte catalog_hash field). ALWAYS append new catalog entries at the END; the splice proof (old hash at bytes 33..40 of the tick-1 dump == old golden tick-1) catches an accidental shift before you bless.
- **Era-3 demand entries whose role has no live terminal are rng-SILENT** (empty eligible source set → the whole entry skips, zero draws) — so adding campus/small_biz demand specs leaves every existing era-3 demo fold-only; only growth+era-3 demos (node_health) shift behaviorally. Predict the T2 partition from the roster before running the harness.
- **The 5.9 W9 surge-lands pin is roster-coupled**: a new streaming-source role dilutes growth's content_host spawns and shifts the per-terminal credit envelope — re-pin to the streaming-capable crowd (content_hosts + campuses) with per-type ceilings, and count per-terminal spawns inside the SURGE WINDOW only (the bound formula's W is the window, the old count was whole-run).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.12-aggregation-groups.md
# Field notes — packet-plumber-v2-5.12-aggregation-groups (2026-08-19)

- Odin `defer` scopes to the ENCLOSING BLOCK: a `defer` inside an `if` runs at the if-block's end, not the proc's — a temp view "freed with defer" inside an `if len(...) > 0` was use-after-freed before the consumer loop read it, and the unit test PASSED (freed memory not yet reused — silent luck). Proc-scope defers or guard with a bool (`defer if built`).
- The 5.9 per-terminal credit gate structurally neutralizes any source-pick weight under CREDIT-STARVATION (each terminal is picked at exactly its credit rate, so no weight moves the shares — a 5-home email fixture gave 800/800 permille with and without the group weight). Concentration pins need a credit-RICH fixture (hosts 1333 milli/tick >> the ask) or the pin is vacuous.
- Permille weight multipliers must MULTIPLY, never `/1000`-divide: `demand_weight × scale` (scale in permille units) is the integer-exact ratio form; `1 × 1750 / 1000 = 1` truncates a weight-1 terminal to no-op and silently kills the concentration.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.2-node-health.md
# packet-plumber-v2-5.2-node-health

- The only game-correct per-node strain is the UN-FORWARDABLE pile (waiting_ticks>=1) vs throughput_units — a transit-inclusive "utilization" measure makes the HEALTHY map scream (measured: the health_win fan's routers hold 75-225% mid-surge with meter 100). Don't re-open this; the shared `warnings` 70/90 thresholds keep 5.2 coherent with 4.1 by construction.
- Derive-don't-record on a Crisis_State array is structural (the serializer writes only node_strain/pipe_strain/forecast/active) — pin it with BOTH replay identity AND a byte-dump negative control (mutate node_health → dump must not change); replay identity alone can't prove absence from the save format.
- Catalog edits are golden-poisoned — 5.2 reuses the balance `warnings` block instead of a dedicated `node_health` block precisely to avoid a catalog_hash re-bless; a future threshold re-tune must go through a DELIBERATE re-bless.
- The PR-event GitHub Action checks out the MERGE of the branch into origin/v2 — NOT the branch alone. A T2 blessing on a stale base (branched pre-#52's Open Sans font swap) passes locally + on the push-event run, then fails ONLY on the PR-event run with small HUD-text-region diffs. Before blessing T2s, `git fetch origin <base>` + merge the base (or check `git merge-base` vs origin/<base> is current); a presentation fold like a font swap re-blesses EVERY text-bearing demo's T2s, so a new demo blessed on the old font is stale the moment the base moves.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.3-pause-anywhere.md
# Field notes — packet-plumber-v2-5.3-pause-anywhere

- Pause is DRIVER-level, never core: the harness's wall-tick virtual clock
  (one T1 hash per wall tick; sim steps only unpaused; mid-pause commands
  lower to apply_tick = next EXECUTED sim tick) is the pattern; the app shows
  fast-path edits instantly while the harness defers to the step boundary —
  two models, converging at boundaries; the T1 pins the SIM freeze, the log
  pins the edits (don't bless "state stable" claims that include the
  fast-path channel).
- The first paused wall-tick hash legitimately differs from the last stepped
  tick's hash (the stepped hash includes that tick's event stream, drained
  right after) — the stable-window check must baseline on the FIRST paused
  hash, never the previous wall tick.
- App trap: the render reads DERIVED bundles (rebuilt only inside step) — a
  fast-path edit while paused was invisible until resume; needs a
  gen-checked bundles rebuild in the paused render path (derived only).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.3-pause-ux.md
# packet-plumber-v2-5.3-pause-ux

- The app pause overlay (app/main.odin) is APP-LAYER ONLY — the harness T2 captures
  (world+forecast+health+banner) NEVER include it, so an overlay change shifts zero
  goldens; the app's own frame is verifiable only via a scratch replica using the rlsw
  shadow (`ODIN_ROOT=<main>/tools/raylib-sw/shadow`) + `LoadImageFromScreen`, with
  pixel-scan (PIL) for overlap truth — vision models misjudge absolute coordinates.
- The top HUD band's only always-free slot is the gap between the Network Health card
  (right edge `win_w/2 + 230`) and the forecast panel (left edge `win_w - 250`) — the
  top-left column carries the QoS readout when a pipe is selected and top-right hosts
  the forecast during a crisis pause, so "top-left or top-right" chips collide in the
  exact pause-and-plan states; anchor the chip at `win_w/2 + 240` (tracks resize).
- A presentation-only ruling still earns a canon amendment in the SAME PR (GDD + art-
  direction + story-card status line): grep the pause canon first ("Pause-to-plan;
  color + icon + glow coding" is the indicator line), match house style, and state the
  ruling source (user ruling date + job id) so canon and code can never drift again.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.4-input-parity.md
# field notes — packet-plumber-v2-5.4-input-parity

- 2026-08-16: WORKTREE TRAP (again, 3rd+ sighting): I edited the MAIN checkout (`/Users/moses/code/packet-plumber`) via absolute paths while dispatched to the worktree — recovered by syncing byte-identical into the worktree + restoring main. Ground truth check: `pwd` + `git branch --show-current` FIRST, then use the worktree path in EVERY file tool + git.
- 2026-08-16: Odin slice literals `[]T{...}` (and `[][dynamic]T{...}`) get backing on the CALLER's stack/temp — a scenario-table built in one proc and used after `free_all` (or after the builder returns) dangles. Heap-build test data (`make` per element) when it must outlive a tick loop's free_all.
- 2026-08-16: review-swarm paid off (blind hunter caught 2 real same-frame divergences from the old handle_input: press+X emitted a Demolish the old code never could; ESC+release re-selected). Rule: when transcribing a sequential per-frame input handler into an event pipeline, state-dependent gates (demolish, selection, class keys) must be re-checked at EXECUTION time — the mapping sees pre-branch state.
- 2026-08-17: MUTATION-RESTORE TRAP: `git checkout <file>` restores from the INDEX (last commit), silently wiping uncommitted fixes — I killed my r3 mouse.odin fix that way and had to restore from /tmp backup. Rule: `cp file /tmp/backup` BEFORE mutating for a mutation test; never `git checkout` a file with uncommitted work.
- 2026-08-17: re-shaped pins must be mutation-proven: the r2 esc_release_place released >6px from the anchor, so the moved-check (not drag_eff) kept it quiet — deleting `&& !esc_cancelled` passed 20/20. Anchor == release point at a NON-UI spot is the shape that bites.
- 2026-08-17: gate loops must derive their count from the list length (${#GATES[@]}), never a literal: the 9th local-CI gate (input parity) was unreachable for a full review round while run_gates capped at 8.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.5-demolish-input.md
# Field notes — packet-plumber-v2-5.5-demolish-input

- 5.5 redispatch on the intent layer: the demolish surface (click-select + popover + X/DEL) already rode the 5.4 executor — the REAL work was the controller leg (pad X = RIGHT_FACE_LEFT, the keyboard X twin; Node_Select mirrors the cursor onto the selection junction->select/terminal->clear), the W1-r4 positive pins (the ui hook was ONLY wired to the negative esc_ui scenario — wire it for positive button scenarios too), and the r3-N7 gate leg (bad-arg -> exit 2, `[ -x ]` guard against the 127->`!`->0 false-green).
- Parity scenarios can drive the demolish BUTTON press on mouse AND touch through the SAME parity_ui_press_effect hook, and the pad leg rides the Demolish intent — one 3-device scenario asserts Cmd_Demolish_Node with mouse == touch == pad.
- Mutation discipline paid twice: my first negative-control mutation (`if false`) was vacuous — a pin that can't fail isn't a pin; the second (`if true`) proved both button scenarios bite. Always verify a mutation actually flips the scenario red.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.6-router-tiers.md
# Field notes — packet-plumber-v2-5.6-router-tiers

- `tools/harness.sh` builds the rlsw shadow in the worktree (~40s + github clone); a fresh worktree can instead `ln -s` the main checkout's `tools/raylib-sw/shadow` (gitignored) and `ODIN_ROOT=$PWD/tools/raylib-sw/shadow odin build harness -out:bin/harness` — 2nd sighting of the shadow-absent trap.
- Golden re-bless for a catalog change is MECHANICAL + PROVABLE: T2 PNGs must stay byte-identical (git status on goldens/*.png), every .log.bin diff must be EXACTLY the 8 catalog_hash bytes at 17..24, and .t1 shifts only in the catalog_hash header + per-tick hashes (state serialization embeds catalog_hash). Script the byte-check; don't eyeball it.
- The 5.6 placement values moved from the old PLACEMENT_MIN_SEP_TILES const into balance.json (its own comment promised that home on the "next legitimate re-bless") — the const's comment is the roadmap; when a data value is golden-poisoned, the const comment tells you when it can move.
- New demo goldens: identical frame bytes across captures is NORMAL for settled static topologies (place.dem does the same) — don't mistake it for a capture bug; the T1 manifest + replay gate are the real pins.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.7-runtime-telemetry.md
# Field notes — packet-plumber-v2-5.7-runtime-telemetry

- 2026-08-14: Odin `-define:PP_DEBUG=true` flips `when #config(PP_DEBUG, false)` — verified
  with a compile probe before building the gate; the harness/app overlay gate rests on it, and
  the plain harness build carries ZERO overlay bytes (goldens can't shift by construction).
- 2026-08-14: temp-allocator trap in a stats-pin verb — `fmt.tprintf` paths passed as a deferred
  write target get recycled by the harness's per-tick `free_all(temp)` → garbage paths. Deferred
  write paths must be `fmt.aprintf` (default allocator) + deleted.
- 2026-08-14: per-tick stats derivation must read the per-tick drop-site scratch (drop_sites)
  right after step — it's cleared at the TOP of the next flow_step, so a paused-wall-tick record
  would be a lie; the stream emits per STEPPED sim tick, which is also what keeps live == replay
  (pause schedule is run setup).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.8-qos-panel.md
# packet-plumber-v2-5.8-qos-panel — field notes

- 2026-08-15 (packet-plumber-v2-5.8-qos-panel): a gitignore trailing-slash
  pattern (`tools/raylib-sw/`) does NOT ignore a SYMLINK FILE at that path —
  my local rlsw shadow symlink got `git add -A`'d and committed (machine-
  absolute, broken elsewhere). Ignore the bare path (`tools/raylib-sw`), and
  after any `ln -s` in a worktree, `git status` + `git ls-files` to confirm
  it stayed untracked.
- 2026-08-15 (packet-plumber-v2-5.8-qos-panel): Odin `strconv.parse_int`
  returns `(int, bool)` — NOT `(i64, bool)` — so an i64 range-check against
  `i64(min(i32))` mismatches types in a `package main`/harness context (the
  catalog's identical-looking line compiles because it casts from
  `json.Integer` first). Compare as `int` or cast the parse result first.
- 2026-08-15 (packet-plumber-v2-5.8-qos-panel): review swarms earn their cost
  on canon-surface gameplay code — the 2-hunter pass caught a committed
  build-artifact symlink (BLOCKER), a silent manual-tune clobber on the
  panel's primary affordance, and a future-era never-drop default-lane hole in
  auto-reservation's E6-safety claim, all before Perkins sees the PR.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-5.9-demand-caps.md
# packet-plumber-v2-5.9-demand-caps — field notes

- The multi-edit atomic trap hit again (crisis_test batch): ONE ambiguous oldText rejected all 5 edits — the cap-1000 scenario overrides never landed, and I debugged phantom behavior for a round before noticing. Re-verify each edit's file AND uniqueness before batching; re-grep after.
- A draw to a NONEXISTENT node id is silently rejected (replay_error latched, no test checks it) — my first W10 fixture drew (1,3) where the sink was id 2, and the W5 transit pin passed VACUOUSLY (delivered 0 → the latency assert skipped). New fixture tests now carry `!replay_error` guards; verify every draw's ids from the spawn returns.
- The era-3 director volumes + growth pacing are load-bearing across MANY test files (crisis/health/node_health/stats all feed on them) — a demand re-tune re-pins far beyond demand_test; the crisis-engine tests can isolate the cap at `cap_fraction_permille = 1000` (full-rate arrival) with the cap's own pins in W9/W10. Also: the harness `save` does NOT delete stale capture PNGs (growth/05500ms.png lingered).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-6.1-era-definition.md
# Field notes — packet-plumber-v2-6.1-era-definition

- The action-log header stores the run's ERA at write time; a mid-run era advance means the header MUST carry the RUN-SETUP (start) era — `log_write` gained a `header_era` param (harness passes demo.era) — or the replay's advance command validates `to_era <= era` (already 3 from the header) and latches replay_error.
- eras.json's parse sits AFTER the PROTO required-content guards: a pkt doc that drops email/streaming must surface the packet_types rejection, NOT an eras-row "unknown packet type" — catalog load-order is a test-contract surface, keep new cross-ref catalogs last.
- E14 deferral tests: never hand-append Active_Crisis rows — the engine auto-resolves them (Saturated_Bundle needs a live saturated bundle; Pool_Exhaustion clears when the pool is below cap). Build a REAL crisis (narrow fixture + era-3 surge on schedule) or the deferral window silently collapses.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-6.2-advance-trigger.md
# Field notes — packet-plumber-v2-6.2-advance-trigger (r1 rework)

- The drift-check flip classes' temp-arena clobber (B2): a temp-allocated `lpath` held across `replay_hashes`' per-tick `free_all(context.temp_allocator)` reads garbage → `accepted=false` → a VACUOUS "rejected (OK)". Any future flip/divergence class must re-call `log_path(name)` at its site.
- `harness save <demo>` does NOT cover the input-parity T1s — `harness input-parity save` is a separate verb; a catalog_hash fold re-bless must include it or gate 10 fails on "catalog drift".
- GH CI has been billing-blocked ("recent account payments have failed... spending limit") since the 7.3 rounds — v2 merged the a11y T2 goldens (blessed with the WRONG palette state — remap not applied) and a stale QoS-era parity expectation, both never CI-verified; reproduced on pristine v2. The local container leg (`tools/ci-local.sh`) is the only working CI ground truth right now.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-6.3-upgrade-lifecycle.md
# packet-plumber-v2-6.3-upgrade-lifecycle — field notes

- 6.3 era-3 decay re-stages EVERY rate-sensitive era-3 test: the crisis/health fixtures
  were tuned on narrow@10 u/s pre-6.3; decayed narrows (5) + standards (7) push them into
  the marginal regime (attribution chatter — the resolve-margin dips cross). Re-stage the
  ENGINE-mechanic tests on the tier that keeps their staging (crisis: legacy narrows with
  per-test tier knobs; W10/W11 access contracts: WIDE — the era-3 modern tier; at era 3
  STANDARD is legacy too, "modern" means wide only).
- `test_catalog`'s `make_era_row` (determinism_test) builds era rows WITHOUT the decay
  factor → defaults to 0 → `pipe_effective_capacity` silently zeroes EVERY era-1+ pipe's
  capacity (the whole suite collapses). Any new Era_Row field MUST mirror in BOTH the
  catalog_test fixtures AND determinism_test's make_era_row (the load contract's mirror).
- The 6.2 gate's "era-3 standard pipes are legacy" is real: era-3 test fixtures drawn
  standard now decay 15→7 u/s — grep `s.era = 3` + standard/narrow draws when touching
  era-3 scenarios; the stats surface (cap_units) pins the decay in the stats test.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-7.1-visual-juice.md
# packet-plumber-v2-7.1-visual-juice — field notes (badge-out)

- **rlsw draws OPAQUE lines regardless of alpha** (verified with a pixel probe): any translucent DrawLineEx/DrawCircleV diverges between the GPU app and T2 goldens — pre-composite colors instead. Also: the canon house roof's DrawTriangle winding `(r1, r3, r2)` was culled by rlsw (never rendered in ANY pre-7.1 golden); `(r1, r2, r3)` draws. Same trap family as the R/B-swizzle: verify rlsw pixels programmatically (PIL/numpy), never eyeball.
- **The harness binary goes stale silently** — after ANY render edit, rebuild `bin/harness` BEFORE `harness save` or the bless lands on old code and the next fresh build fails with tiny color-only T2 diffs (CI caught it; a stale-bless costs a whole re-bless).
- **Mega-minion pane spawns in Herdr**: `herdr pane run <pane> "pi --model x"` can type into a nested shell instead of the agent, and a kimi-quota 403 consumes the handover prompt as an EMPTY assistant turn — check the pane's session jsonl for assistant content before trusting `done`; use `herdr agent prompt` to deliver. (A user-pasted image can also arrive as bare `[Image-#N]` text with no payload — grep the session jsonl before asking.)

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-7.2-audio-juice.md
# Field notes — packet-plumber-v2-7.2-audio-juice (2026-08-17)

- Worktree-trap, THE expensive one: I did the whole job with file-tool paths +
  bash `cd`s at the MAIN checkout (`/Users/moses/code/packet-plumber`) despite
  starting with `pwd` in the worktree — the briefing's `repo_root` param reads
  like a work path. Recovery: `cp` the changed/new files byte-identical into
  the worktree (`cmp`-verified), rebuild + full CI there, `git checkout --` +
  `rm` in main. Pin the worktree path ONCE and use it for every cd AND every
  file-tool path.
- The harness CAN import `app/audio` (a raylib-importing app package): Odin
  DCEs the unused raudio procs, so the rlsw shadow (which builds NO raudio.o)
  links clean — no `build_raylib_sw.sh` change needed. Verified on macOS +
  the CI container (gate 4).
- Odin specifics that bit: relative imports resolve from the PACKAGE ROOT
  (app/audio needs `../../core`, not `../core`); constant arrays can't be
  indexed with a variable index (copy to a local first); `fmt.bprintf` returns
  a string VIEW (ideal for fixed-buffer captions); a constant f32→int cast
  that truncates is a compile error (precompute an int constant like
  `SYNTH_RAMP_SAMPLES = 110`).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-7.3-accessibility-core.md
# Field notes — packet-plumber-v2-7.3-accessibility-core (2026-08-19)

- The briefing's `deepseek/deepseek-v4-flash` model line was 402-DEAD at dispatch (playbook 08-19 ruling): the job + the epic-context mega-minion ran on `zai-coding-cn/glm-5.3`; check `PI_MODEL` before trusting a briefing's model (Silas launched me on glm despite the ledger's flash field).
- The `hud()` scaled-int helper is the byte-identity hinge: at ×1.00 `i32(f32(k)*1.0+0.5) == k`, so scaling the capture-visible HUD (health/forecast/banner) through it kept every pre-existing T2 byte-identical — proven by the full suite, never assumed.
- Parity/zero-View traps: `settings_chip_rect` reads `v.palette.mode` — a view without a palette (the parity harness's) SEGFAULTS on the chip rect; every view construction needs a loaded palette. Also: a misplaced `{}` brace + a comment-merged `{` in palcheck took two full debug passes to find — run the brace-depth checker on any file after multi-hunk edits.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-arch-egress-migration.md
# packet-plumber-v2-arch-egress-migration — field notes (2026-08-26)

- shadow_clone is a per-story trap, not a one-off: EVERY new step()-touched dynamic array must be added to spawn_fx.odin's clone list AND its flow_init mirror (capacity-1) — the shadow silently aliases the LIVE run's pointers and the abort surfaces far away at run_destroy (malloc_error_break backtrace finds it; the tx-ring comment in the same proc is the prior incident).
- Diffing against a MOVING remote tip fakes deletions: the spine landed on v2 via #103 after the branch point, so "this branch deletes the spine" was a merge-base artifact — always diff at the merge-base before believing a hunter blocker about missing files.
- Same-count bundle renumber (demolish+draw in one batch) silently inherits the dead pair's history unless derived-ring layouts reset on Topology.gen — the B1 slot-renumbering class generalizes to every ring keyed by a regenerated index (hunter-probed at 120 phantom ticks).
- r1 fold addendum: test step_once helpers hardcode tick 1 — past that tick the backward-tick guard silently no-ops (use step_n); Odin for-in over array literals is still a syntax error; a clamp-at-100 util read needs an ASYMMETRIC fixture (60/30) — a saturated both-directions fixture cannot discriminate max from sum.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-arch-latency-egress-queue-model.md
# packet-plumber-v2-arch-latency-egress-queue-model — field notes (2026-08-26)

- Reality-check lens caught a spine assertion the code contradicts: `bandwidth_demand` is catalog-loaded but UNWIRED (zero consumers) — never cite a catalog knob in a formula without grepping consumers; "documented in the loader comment" ≠ consumed.
- Serialization-conflict blockers (adversarial AV-2) often dissolve against EXISTING tag-conditional payload slots + derived scratch (the Event.direction reuse kept LOG_VERSION at 6) — enumerate existing payload slots before declaring a bump unavoidable.
- Edit-tool trap: mermaid label strings contain LITERAL `\n` two-char sequences — in edit oldText they must be `\\n`-escaped (a raw `\n` in the JSON silently becomes a newline, the match fails, and the whole multi-edit call atomically no-ops).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-arch-latency-spine-docs.md
- BSD diff has no -R for recursive dir compare — use lowercase -r (cost one round-trip on the verbatim check).
- Commit message discipline: paste the EXACT ratified message; first commit attempt drifted to a shorthand form, caught by re-reading the ruling — amend before push, never after.
- Verbatim-copy jobs: cp -R then `diff -r` against source is cheap insurance that the PR carries exactly what was ratified.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-blender-sculpt.md
# Field-notes shard: packet-plumber-v2-blender-sculpt

- (2026-08-23) **Never trust a piped Blender run**: `blender -b -P … | grep`
  masks the exit code AND the traceback — two "determinism-proof" runs had
  crashed on a bad API call (`RenderSettings.use_metadata` is GONE in 5.2)
  while `cmp` compared stale files. Capture `rc` first, then sanity-check
  output FRESHNESS (mtimes / expected new values) before believing a
  byte-compare. PNG byte-determinism fix that works on 5.2: strip
  tEXt/iTXt/zTXt chunks post-render (the wall-clock `Date` tEXt is the only
  mover; IDAT is stable run-to-run).
- (2026-08-23) Blender-MCP exec chunks run in a FRESH globals namespace per
  call — imports don't persist; park helpers in `bpy.app.driver_namespace`
  and re-import `bpy/os/Vector` at the top of every chunk (and if a helper
  needs a module, inject it into `helper.__globals__`). Keep chunks small
  (~<100 lines — a big one died mid-write with a broken pipe, and a partial
  exec leaves partial scene state; clear and rebuild, don't patch).
- (2026-08-23) Look-gate lesson: at the MM top-down tilt (~60° elevation),
  sub-mass stacking (setback blocks) reads as MUDDY STRIPES, and wall-band
  shading alone stays subtle — the depth that actually reads is (a) the
  two-tone ROOF (gable barns / hip caps, per the user's top-down refs) and
  (b) the engine-drawn CAST SHADOW (12-18% ink @ fixed 2px offset is an
  invisible sliver; 25-33% ink @ proportional offset 0.08w/0.10h down-right
  reads). Coplanar plate overlaps z-fight — butt-joint instead.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-blender-silhouettes.md
# Field-notes shard: packet-plumber-v2-blender-silhouettes

- (2026-08-22) gen_sprites.py re-render on Blender 5.2 is PIXEL-DETERMINISTIC
  (decoded RGBA identical; md5 diffs are PNG-encoder metadata only) — a no-op
  re-render is golden-safe, so pipeline validation = render + pixel-compare,
  no re-bless. T2 compares decoded pixels, never file bytes.
- (2026-08-22) the pipeline's camera tilt VARIES with the per-sprite pad
  (direction vector includes the camera Y position: `(0, 0.35, 0.10) -
  (0, -4.5*pad, 10.0)`), so bbox aspects differ from world aspects — the
  renderer consumes the bbox aspect, so the READ is the bbox; don't "fix"
  the tilt without re-blessing (it's a pre-existing quirk, spec-documented).
- (2026-08-22) port-ring dots need an explicit cx/cy in add_flat_disc — the
  first cut stacked all dots at the disc center (PUCK_PORT_R was defined but
  never used in placement); KYLE caught nothing at contact-sheet scale — the
  bbox geometry table + a zoomed per-sprite check caught it.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-box-crash-third-spawn.md
# field notes — packet-plumber-v2-box-crash-third-spawn (2026-08-28)

- `shadow_clone` (app/render/spawn_fx.odin) hand-copies Run_State's dynamic arrays; EVERY new Run_State dynamic array must add a clone line AND a pin line in test_spawn_fx_shadow_clone_box_owns_every_array — the box-ON fixture + raw_data pointer pins are what make a missed field CI-visible (box-OFF fixtures hide it: nil headers delete harmlessly; skip only raw_data==nil in the pin, len==0 hides allocated backings).
- Reducing a "pointer being freed was not allocated" SIGABRT with lost app frames: grep the repro surface for by-value dynamic-array/struct copies feeding a destroy — `clone := src^` + `run_destroy(&shadow)` was the whole bug; Odin's test allocator prints `bad free @ file:line` call sites, so `odin test` beats libmalloc for localizing invalid frees.
- `odin test` bad frees are REPORTED not fatal, and temp_allocator frees are no-ops the leak report cannot see — a mutation gate must pin ownership directly (pointer compares), never depend on allocator abort/leak behavior.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-camera-zoom.md
- 2026-08-23 (packet-plumber-v2-camera-zoom): the 7.1 camera model (eased cam_zoom/cam_wx/cam_wy targets on App, camera_update deriving view scale/off) is the WHOLE camera — zoom/pan = set the targets, zero render-layer changes; the harness never runs camera_update so T2 stays byte-identical by construction. Empty-ground left-drag pan is conflict-free: Begin_Draw only ever starts on a node press.
- (same job) The wheel-ownership trap: the OLD NOC scroll read GetMouseWheelMove in the render block — keep ONE wheel consumer (the effect), or the same notch double-fires as a scroll AND a zoom.
- (same job) PP_CAM_E2E (PP_DEBUG + env) is the mechanical-evidence pattern for view-layer features: real Device_Events injected in handle_input, TakeScreenshot after EndDrawing, pixel-scan the before/after (paper-fraction + diff-frac) — never eyeball zoom claims; vision (KYLE quick-read) is the secondary check on the committed captures.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-congestion-read-a1.md
# field notes — packet-plumber-v2-congestion-read-a1

- 2026-08-28: palcheck render-only fixtures — `crisis.pipe_congestion` has len 0 until warnings_update runs; `resize()` + explicitly zero the grown slots to `.None`, and remember E26 rejects terminal→terminal pipes in fixtures (mirror §7: terminal→router).
- 2026-08-28: when a band-measure palcheck leg returns exactly your scan half-window count (2·half+1), the scanner is measuring ALONG the feature, not across it — assert a predicted pixel count from the draw's own math first (dump the column) before trusting the leg.
- 2026-08-28: stride the evidence harness FIRST (bin/harness_before from HEAD + view-only extension), then mutate — the corpus-freshness + mutation-leg ordering (before-strips → change → re-bless → after-strips) made every A1 claim mechanically checkable without a second worktree.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-design-audit.md
# packet-plumber-v2-design-audit — field notes

- **Kyle (glm-4.6v) full-agent spawn works like the one-shot recipe** — herdr pane split, `pi --model zai-coding-cn/glm-4.6v --thinking max`, hand over via `herdr agent prompt` with `@file` absolute paths; verify the session modelId in the pane title. He reads images with the read tool himself (batch 3-6). Long turns hit provider 500/timeouts — nudge with "write NOW compactly, do not re-read" when the file is overdue; his findings land on disk even when the final DONE message errors.
- **Kyle's vision verdicts need pixel verification before they drive decisions** — pass-1 "3D shading on sprites" was wrong (sprites measured 90-93% flat canon hexes, residual = AA only); "shapes identical" was wrong (aspects 1.01 vs 1.45-1.48). What's true survives: shadow blobs read heavy, small_biz/campus share warm-brown + aspect, packets render at 20Hz quantized (no sub-tick lerp — code-verified in draw_packets/packet_progress_frac), spawn is an instant pop (no animation exists). Measure sprites with PIL (interior-pixel color coverage) before believing a "needs Blender" verdict.
- **MM reference serving for lavish reports**: MM images must stay in _local-refs (never in repo). A symlink into the artifact dir gets 403'd by lavish's static root; serve the refs from a tiny `python3 -m http.server 4388 --bind 127.0.0.1` pane rooted at _local-refs and reference `http://127.0.0.1:4388/mm/...` in the HTML — browser-safe, repo-clean.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-dublin-board.md
# packet-plumber-v2-dublin-board (2026-08-23)

- The dublin.json OSM rings are SELF-INTERSECTING (pinch/retrace — all 358
  rings fail the simple-polygon test): ear clipping silently drops them;
  the even-odd point-in-polygon cell raster (1 cell/world px, span-filled
  like map_draw) is the ONLY fill that matches PIL's blessed gallery.
- `make([dynamic]T, n, cap)` makes LENGTH n (zeros) — the index-ring bug
  that silently zeroed an entire triangulation; 0-length+cap is the append
  pattern. The temp-arena free_all also ate a test board mid-run (default
  allocator for anything a record_run outlives).
- Board geometry reality: 719 snapped street tiles at 1-in-6 (sub-tile
  raw dots kept for the render); district Voronoi cells are smaller than
  the estate radius — 63% of tiles have zero SAME-DISTRICT attach-ring
  neighbors, so district-scoped attaches stall; the global street ring +
  ring-has-room eligibility is the working interplay (documented in
  growth.odin).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-dublin-map-beautify.md
  with the bbox boundary, polygonize, take the face containing a pinned sea
  seed. NAMING TRAP: a module-level `def polygonize()` SHADOWS the shapely
  import of the same name — build_sea silently called the ring helper and
  returned nothing for a full round (the bake's --verify PASSED because it
  compared the same buggy output twice!). Also: a seed ON the bbox edge is
  `touches`, never `contains` — keep the seed inside the bbox.
- The user's red speckle was NOT landuse=residential — it was the 224k
  building-centroid spawn candidates rendered as house_bodies[0] (red) dots.
  The fix (mock-gate amendments): street-aligned BLOCKS baked per candidate
  (nearest street segment via shapely STRtree — deterministic, ties break by
  input order; the asset's --verify proves byte-identical re-bakes).
- PIL does NOT alpha-blend on draw — RGBA pixels are stored raw; composite
  manually before pixel-scanning mock renders (a scan that skips this reads
  raw-alpha garbage and lies).
- KYLE mock-gate iterations: (1) saturated 4-color blocks + the residential
  street web + the 18% grid = "GIS export"; (2) muted 2-tone blocks + locals
  faded to alpha 40 + no grid + arterials up = crop PASS "game map", overview
  near-pass ("more abstraction"). The overview/crop LOD (block alpha 40 vs
  120) was needed — same data, zoom-aware wash.
- Lavish asset paths: the HTML at .lavish/<name>.html must reference images
  as <dir>/img/... — the session serves /artifact/<id>/<rel>; a bare img/…
  path fails as 8 fatal artifact-asset-unavailable failures (the poll returns
  them, not user feedback — repair + re-poll).
- Blender (5.2) flat-color render trap: Principled BSDF "Emission" still
  receives the WORLD's ambient light on its diffuse term — a flat paper color
  renders blown-out white. Use a pure ShaderNodeEmission node (no diffuse
  term at all) for unlit map layers; convert palette hex sRGB->linear
  explicitly and keep view_transform='Standard' for hex-exact PNGs. Also:
  bpy materials assigned sRGB values directly render +50% brighter — the
  double conversion bites silently.
- Odin nested procs do NOT capture the enclosing scope — pass the struct
  pointer as an explicit parameter (the seg-grid builder bit once).
- The mock gate evolved the design 7 rounds in one lavish session (fabric
  blocks -> Blender low-poly base -> topology-on-the-map -> zoom LOD model);
  the user APPROVED from the gallery with three final rulings (sea ~15%, no
  grid, roads must connect). The committed look = the Blender-baked underlay
  texture (assets/maps/dublin_underlay.png, 4160x3120, timestamp chunks
  stripped for byte-stability) + the game's own nodes as street-aligned
  blocks (dublin_node_block_draw). The LOD zoom bands + cluster spawn
  director are flagged follow-ups.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-dublin-spawn-director.md
- 2026-08-24 (packet-plumber-v2-dublin-spawn-director): Odin fmt has NO `%-3d` left-justify flags — `%-3d` renders value×100 garbage silently; plain `%d` only. Also: Odin has NO `var x T` declaration (compile error — use `x: T`), and `for p in [4][2]i32{...}` literals need a named var first.
- 2026-08-24 (same job): the stage-1 "district-scoped attach starves 63%" warning is load-bearing — weight the CLUSTER PICK (ring stays global); a zero-weight band must be excluded from the ELIGIBILITY list, not just the weighted draw (the single-eligible shortcut would pick it); every new director pin needs its mutation leg (uniform-pick mutation caught the vacuous ratio test — caps bound the sample at step level, so pin the exclusion not the ratio).
- 2026-08-24 (same job): the dublin board's growth is E31-bounded by the STATIC demo mesh (2 routers → ~15 terminals/90s) — the estate lens (derived cluster view) is the honest audit (per-district counts read 1-2 because estates straddle Voronoi boundaries by design).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-font-overhaul.md
# packet-plumber-v2-font-overhaul — field notes (badge-out)

- **rlsw SW-app traps (the gallery capture path):** (a) macOS PLATFORM_MEMORY GetTime() returns 0 → SetTargetFPS(60)'s busy wait `while (GetTime()<target)` spins FOREVER in EndDrawing (the harness never sets a target FPS, so it never hit this) — skip the limiter in SW builds; (b) the raylib-sw shadow has NO raudio — the app's audio package needs `when #config(PP_SW_AUDIO,false)` gating to link; (c) the GPU path lies twice: the compositor freezes the GL front buffer for occluded windows (TakeScreenshot repeats frames) AND RenderTexture readbacks carry glyph-coverage in the alpha with atlas-RGB leaking (gray boxes + white glyphs) — the SW framebuffer (LoadImageFromScreen + flip + r/b swizzle) is the ONLY reliable capture.
- **raylib LoadFontData COMPACTS the glyph array** (missing codepoints are SKIPPED — lookup is by glyph.value, never index) — a fallback merge must APPEND fallback glyphs into a MemAlloc'd array (raylib's UnloadFont frees it; never mix allocators). And a font-load failure must FAIL LOUDLY: the ibmplex gallery frames were silently Open Sans because a curl'd TTF was actually a 404 HTML page and LoadFontEx fell back quietly.
- **google/fonts raw URLs for IBM Plex static TTFs 404** (the repo is variable-only now: `IBMPlexSans[wdth,wght].ttf`) — use the IBM/plex GitHub release zips (`fonts/complete/ttf/`) and ALWAYS verify TTF magic bytes (00 01 00 00) after any font download.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-harness-ecmp-demo.md
# packet-plumber-v2-harness-ecmp-demo — field notes (badge-out shard)

- **Odin `fmt.tprintf` = temp allocator, `fmt.aprintf` = default** — the harness tick loop's per-tick `free_all` silently frees ANY tprintf string that must outlive the iteration (T2 failure messages + diff-dir paths came back as blank garbage; the T2 failure path had never run before because goldens were deferred). In-loop failure strings must be `fmt.aprintf`. Same trap for strings sliced out of temp-allocated demo text: `spawn_node` type names needed `strings.clone` at parse (the ODN-11 replay gate caught the dangling pointer live — the gate is the trap detector, trust it).
- **The rlsw harness was ALREADY working** — bundle/flow/draw/win/lose T2 goldens were blessed in slice-1/2.1 and pass bit-exact; the "deferred T2" debt was only ecmp (no demo) + demolish (no captures). Verify the actual repo state before rebuilding infrastructure; the briefing's deferral narrative was stale.
- **`fmt.tprintf` on a JSON literal needs `{{`/`}}`** — unescaped braces emit `%!(MISSING CLOSE BRACE)` into diff.json (the agent's §10.5 entry point was corrupted on every mismatch).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-look-node-legibility-diag.md
- 2026-08-26 (look-node-legibility-diag): SCRATCH rlsw capture traps beyond the harness doctrine — a scratch binary linking the same `app/render` package on the same raylib-sw shadow needed: TWO warmup content frames (first content EndDrawing = black), TWO presents per capture (LoadImageFromScreen reads the LAST PRESENTED buffer — one-frame lag; the harness never sees it because its view is static per demo), and NO flip/NO swizzle (its readback is top-down RGBA while the harness binary's needs flip+swizzle — same shadow, unexplained; verify per-binary against palette tokens + geometry anchors, never assume the harness recipe).
- 2026-08-26 (look-node-legibility-diag): Odin fmt JSON traps — literal `{`/`}` in format strings need `{{`/`}}` (a stray single `}` renders literally and breaks the JSON silently); `geom += str` is illegal (use an appendf helper with fmt.aprintf("%s%s", ...)); `import` keyword mandatory per import line.
- 2026-08-26 (look-node-legibility-diag): evidence craft that worked — emit geometry.json anchors (node screen pos, puck_w, band_px) FROM the renderer, then PIL-measure against them (radial ring scans + token classification + WCAG contrast); vision (KYLE) corroborates but ranks colors perceptually (called dark-ring variant "wrong" where WCAG said best contrast — both true: contrast vs board ≠ separation from the dark puck rim).
- 2026-08-26 (look-node-legibility-diag): node-legibility evidence verdict for the fix job: ring stroke 1-3px (0.055 factor, 4900d25) + C(ring,adjacent-pipe)≈1.0-1.3 at the doorstep (rings 4900d25 vs vivid pipes = the 08-22 user ruling) is the driver; puck scale (9bf9797) and dublin blocks are CLEARED; zoom never improves the ratio (bands scale with rings). Adjacent finding: at focus 2.6 the weather panel can sit ON a router (top-right) — worth a ticket.
- 2026-08-26 (look-node-legibility-diag, RULING): after a 7-round lavish loop the user ruled MM-STYLE — thin solid laneless links (8/11/14.5 world-px, ~30-40% of node Ø at every tier), nodes on top (magnet snap), real building sprites at router scale (home 1.00/biz 1.10/campus 1.22/DC 1.35 tiles, wash ~55% lighter), queues move to the router ingress/egress. Full spec: implementation-artifacts/look-node-legibility/direction-ruling.md. Lesson: the user iterates on MOCKS fast (7 rounds, ~10 min) — keep the mock tool parameterized per-direction, regenerate strips in one command, and let KYLE verify each round before replying.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-look-polish.md
# packet-plumber-v2-look-polish — field notes

- **The vision mega-minion doctrine (08-21): Kyle on `zai-coding-cn/glm-4.6v`** — 5v-turbo is subscription-blocked (429/1311); 4.6v works. Spawn recipe: env-cleared pi (`env $(env | grep '^PI_' | sed ...) pi --print --no-session --no-tools --model <full-path> @<abs-img> "<prompt>"`), prompts written to FILES (shell quoting eats multi-line prompts), absolute OUT paths (the spawn cds into the worktree — relative outputs land there). lmstudio/qwen via `bin/vision-read` is the always-up fallback.
- **rlsw alpha truth (golden-divergence law):** FILLED shapes (circles/ellipses/rects) alpha-blend in the software renderer; LINE primitives render alpha as OPAQUE — a translucent line draw diverges between the GPU app and the rlsw goldens. Translucent visual effects must be fill-based or pre-composited opaque.
- **The per-commit re-bless loop pays:** 5 deliberate re-blesses, each verified by (a) `cmp -l` every `.log.bin`/`.t1` vs HEAD (byte-identical — `harness save` rewrites T1 too), (b) diff-bbox pixel scans matching PREDICTED blend colors ±0 (casing blends, glint color, shadow footprints), (c) palcheck re-pins with measured floors — CI stayed 10/10 at every commit.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-look-zoom-language.md
# Field notes — packet-plumber-v2-look-zoom-language

- 2026-08-27: the harness demo-directive zero-value trap — a new numeric Demo field with "1.0 = default" semantics still zero-inits to 0.0; `zoom 0` drove `scale = fit*0` and the map grid loop drew ~forever (2.5h silent "suite run"). Normalize absent-directive numerics AT PARSE TAIL + belt the run site; a hung `harness run` with an empty log = sample the process, look for an unbounded render loop.
- 2026-08-27: unit-test Views that call sprite_puck_target (or anything reading sprites.json bboxes) MUST hand-set `v.sprites.bboxes[6..8][2]` — zero bboxes make every ROUTER endpoint's drawn size 0, which zeroes the covenant cap and VACUATES the whole sweep (it passed crushed at cap 0; the adversarial hunter probed it). sprite_house_target doesn't read bboxes — the house leg stayed honest while the router leg lied.
- 2026-08-27: under-sprite "glow dots" are invisible in our trimmed-blit pipeline — DrawTexturePro blits the CONTENT bbox tight, so any dot smaller than the footprint hides completely (the mock's under-dot only peeked because its paste carried transparent canvas padding). The read is a HALO: radius > 0.5× footprint. Also: predicted blend scans need the actual UNDERLAY color — probe map-preview with the correct fit offset (OX=(win−world×fit)/2), the seed-7 land tint is (239,228,186), not canvas.
- 2026-08-27: clearing `app.pullback` does NOT stop autonomous camera motion — camera_update's ease runs unconditionally (the flag only sets the rate). Any "stop the breath" site must freeze cam_zoom_to/cam_wx_to/cam_wy_to at the live values (set_reduced_motion does; the pre-existing N11 toggle still has the latent behavior — deferred).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-mechanics-the-box.md
# field notes — packet-plumber-v2-mechanics-the-box

- 2026-08-28: Odin `case:` in a `#partial switch` swallows EVERYTHING after it — a case inserted
  below the default silently never runs (a demolish refund priced zero and the tests still mostly
  passed). Keep special cases ABOVE the default; a grep for `case:` adjacency belongs in review.
- 2026-08-28: any charge/refund priced from POST-apply topology is a hazard class: pipe_slot/
  node_slot SKIP DEAD entities and fall back to slot 0 — tombstone-then-price refunds the wrong
  tier/span (or nothing). Pattern that works: validate snapshots the pre-edit facts into a small
  struct, charge prices from the snapshot. A test demolishing pipe id 0 MASKS the bug (slot 0 is
  the accidental right answer) — always demolish a non-zero id in refund tests.
- 2026-08-28: T2 pixel goldens + palcheck are ENVIRONMENT-BOUND on this machine: the pristine base
  (03dd6f8) re-blessed locally reproduces palcheck 61-fail exactly (committed base goldens: 32) and
  `save juice` on base ≠ committed juice. T1 (sim hashes) is stable. Before chasing a palcheck/T2
  regression, re-bless the BASE in a scratch worktree and compare — if base reproduces, it's the
  render environment, not your diff; disclose and let the human/CI decide the golden source of truth.
- 2026-08-28: `.gitignore`'s `_bmad/` does NOT match the worktree bootstrap SYMLINK (trailing slash
  matches directories only) — `git add -A` stages the symlink; the repo .gitignore now carries a
  bare `_bmad` line too.
- 2026-08-28: harness `stats-check <demo>` writes its streams under `bin/` — a fresh worktree has
  no `bin/` dir and fails "cannot read live stream: Not_Exist"; `mkdir -p bin` first.
- 2026-08-28: a fail-fast TEST TABLE can be entirely VACUOUS while green: a per-file reject helper that omits ONE catalog source makes the loader die in an EARLIER file, and the helper's "wrong file" branch returns without ever checking the rule — every row passes forever. Audit rejection helpers by MUTATING one expectation to nonsense: if the suite stays green, the table is dead. Fixing the helper then exposed ~40 stale expectations (rows written against the key NAME, the loader rejects with the MESSAGE substring) — fix each against the REAL rule and re-run.
- 2026-08-28: rejection-rule needles are brittle in three ways: (1) `replace1`'s 4th arg is a COUNT, not an occurrence index; (2) after retuning a fixture value, old needles stop matching and their rows silently no-op (verify each row still fails-for-the-right-reason); (3) loader messages carry EM-DASHES — a hyphen in the want substring fails the contains() check. Copy want-strings from the loader source, never from memory.
- 2026-08-28: `Catalog_Sources` field alignment differs per helper (eras needs fewer padding spaces) — a python needle with copied alignment silently no-ops across helpers. When a patch "applies" but grep finds no trace, the needle matched a DIFFERENT helper's block; verify by grepping for the inserted comment.
- 2026-08-28: NEVER edit data/*.json comments (or any catalog byte) after a golden re-bless — catalog_hash folds and every .t1 manifest + parity manifest goes stale (a full save + input-parity save needed AGAIN). Settle all data edits FIRST, then bless once, then freeze.
- 2026-08-28: two machines blessing the same corpus with different R/B raster conventions splits the corpus (Perkins census: 116/117 swapped vs 1 warm) — after ANY cross-machine merge, re-bless the ENTIRE corpus from ONE machine and run the full T2 loop twice consecutively before trusting it.
- 2026-08-28 (THE BIG ONE): **NEVER bless T2 goldens with `odin run harness` directly.** The direct build links the standard vendor:raylib (GPU/Metal headless) whose readback is R/B-SWAPPED (BGRA) — the frames render, the T2 compare is self-consistent, the suite goes green, and NOTHING looks wrong until a blob-level census finds every frame carrying the swapped convention. The sanctioned pipeline is `tools/harness.sh` (builds the rlsw software-raylib shadow via ODIN_ROOT swap — warm-correct RGBA, bit-exact per ODN-17). Symptoms of the wrong-backend trap: palcheck raster legs fail with 0 px of EVERY canon hex; "stale" goldens that re-bless to byte-identical wrong frames; a black frame where #106's is warm. The fold-check/T1 gates stay valid (sim hashes are render-independent) — which is exactly why the trap is invisible to the T1-only sweep. ALWAYS bless + verify T2 via tools/harness.sh.
- 2026-08-28: PNG pixel-diffs in a pinched shell: hand-rolling a PNG de-filter in python works (Paeth etc.) but the channel-stride must match the actual color type (ch=4 RGBA vs 3 RGB) — a step-3 walk over an RGBA buffer misaligns channels and fabricates phantom diffs. Use PIL when available; pin the tool.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-network-units.md
- 2026-08-23 (packet-plumber-v2-network-units): **New core state must be deep-cloned in app/render/spawn_fx.odin's shadow_clone** — a missed clone of the new Bundles tx ring made the capture-path shadow free the LIVE state's pointers (harness aborts only in the FULL demo loop at the first T2 capture; single demos pass — order-dependent heap corruption is the signature). Any future Run_State/Bundles field addition: grep shadow_clone.
- The briefing's "10/100/1000 Mbps" ladder is arithmetically impossible with "standard 1500B = 8 ticks" + "T1/T2 hash-equal": SIM_TIME_SCALE is pinned by standard (3333), rates derive from the sim's own transits (67/100/267 Mbps). If a nominal ladder is ever wanted it needs its own transit rebalance + full re-bless job.
- HONEST util = served-units-window / (cap × window) — physically bounded at 100, exact at saturation, ~16% for a single residential stream. The OLD backlog/cap formula read 800%-clamped-100 — queue depth is a separate signal.
- harness overlay-check needs the rlsw shadow build (harness-debug-sw) AND the "ms" suffix on the capture arg; overlay_check's own build links real raylib → black frames.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-noc-player-toggle.md
# packet-plumber-v2-noc-player-toggle (2026-08-23)

- bmad-build is UNUSABLE on packet-plumber: `_bmad/scripts/` has NO render_skill.py (only memlog.py/resolve_*.py) — skill waived per Silas ruling 08-21; the briefing was self-contained; carry the waiver as a canon note in the PR body.
- Edit-tool batches: an em-dash in oldText can silently fail the WHOLE batch (atomic reject, "edits[N] not found" while the block is verifiably present) — use minimal ASCII-only anchors, or a python replace for em-dash-heavy regions.
- The harness `overlay-check` verb's ms arg needs the `ms` suffix (`parse_ms` requires it): `harness-debug overlay-check surge 3000ms`, not `3000` — a bare number falls to usage().

- Rebase fold (post-r2): when a sibling PR (camera) adds a settings row at the SAME index you did, the merge keeps BOTH — your row moves up (PULLBACK=4, NOC=5, SETTINGS_ROW_COUNT 6) and the W2 nav pin must be re-pointed to the new depth. Also: a sibling's PP_DEBUG compile gate around a runtime feature (effect_overlay / wheel scroll) is OBSOLETE once you ungate the feature — ungate their gate too (a PP_DEBUG-only scroll body dead-zones the wheel in every normal build) and update THEIR test that pinned the old two-build behavior (the B2 release-leg premise "release can't have the overlay" dies with the runtime gate).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-noc-readability-2.md
# packet-plumber-v2-noc-readability-2 — field notes

- The DOCK-RIGHT ruling's geometry is IMPOSSIBLE to satisfy by re-anchoring
  the top band into the shrunken playfield (title 180 + health 460 + forecast
  250 = ~890px > play_w 756 at 1280) — the sanctioned resolution is: fit-to-
  rail camera (View.play_w, one derivation) + top band cards KEEP win_w
  anchors and draw OVER the rail (world -> rail -> HUD order); the rail
  content starts below the top band (NOC_CONTENT_Y 116). Document in the PR.
- Odin const arithmetic: `NOC_PANEL_W :: i32(360 * 1.4)` TRUNCATES to 503
  (float const 503.999...) — use int math `360 * 14 / 10` for the 504 rail.
- The PP_DEBUG harness verbs need the rlsw software build (bin/harness-debug
  is GPU and renders a SOLID BLACK frame headless — the 08-11 trap, still
  live); the overlay-check verb takes the `12000ms` suffix form; both
  overlay verbs must view_set_rail(true) so the capture matches the app.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-node-clarity.md
# packet-plumber-v2-node-clarity — field notes (minion shard)

- **Odin #load embeds data files at COMPILE time** — after any palette.json
  token edit, REBUILD the harness before re-rendering (a stale embed silently
  renders old colors and wastes a re-bless cycle).
- **The blur-gate sampler must be calibrated before trusting it**: build the
  σ6 sampler first, confirm it reproduces the audit's baseline deltas (res↔
  sbiz ~3-4°, res↔campus ~13°, router↔host ~9.7°) on the OLD golden, then
  iterate. Offline PIL sprite-composition sims under-predict the real
  render's saturation (real board surroundings darken/mix) — screen with the
  sim, settle with real renders. Wash alphas encoded in the token's alpha
  byte keeps everything in data (palcheck-pinnable).
- **Warm-family clustering is the trap**: terracotta↔brick↔warm-stone all
  blur toward the cream canvas (~44°) — the ≥15° bar forces a genuinely cool
  stone (green-gray ~110°) and a desaturated brick. Palette-anchor "families"
  survive, literal anchor hexes don't. Keep token edits ADDITIONS-ONLY when a
  sibling job owns shared tokens (POP owns the network) — and re-emit
  palette.json in its original aligned format (json.dump reformat churns 700
  lines).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-pace-tuning.md
# packet-plumber-v2-pace-tuning (2026-08-21/22)

- The 5.9 spawn-credit clamp makes the effective per-terminal pick rate
  `1 / ceil(1000/accrue)` per tick (campus 625 milli → 0.5/tick; host 333 →
  0.25/tick) — the raw accrue/1000 formula OVERSTATES the rate whenever
  accrue > 500 milli; demand tests must derive from the clamp, and W9-class
  "ask lands" contracts re-derive units-anchored at any pace scale (the ×10
  surge multiplicativity dims to ~2.6× at 4× — the packet ask can't express
  above the units-anchored pool; the saturation trigger still fires).
- The crisis (b)-drop-fallback regime is phase-dependent at the 4× pace:
  the director's bursty credit arrivals make the post-flow eval lane land on
  the bound every other tick (a) — the deterministic construction is ODD
  arrivals/tick (5/tick: 5→6→shed→5, post-flow below the bound) or a
  pre-window backlog at the bound at the window's first tick.
- A 4× pace re-tune ripples into EVERY exact-tick/unit test pin (17 files,
  46 pins) AND the health stagings: the post-fix breach exit lands ~fix+179
  (the latency window slides faster with sparser deliveries) vs the grace
  expiry ~428 — the "exit just after the expiry" staging needs the fix ≥300
  (at 241 the exit beats the expiry and the meter never drains).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-qos-default-standard.md
# packet-plumber-v2-qos-default-standard

- The 5.8 lane-only demos/tests (sla, qos_contention, audio_throttle, lane_pipe_setup, test_congested_run) were stale relative to the app's auto-follow — with the 08-19 100%-Standard default they MUST write the ladder weights (Cmd_Set_Weights) or their scenarios silently sit at E7-floor rates; grep lane-only setups when any default-allocation change lands.
- E6 guard check (validate_set_lane) must judge the pipe's SETTLED weights (auto-follow result for auto pipes), not its current default — otherwise the first never-drop assignment can never engage the ladder.
- Golden re-bless proof: `harness fold-check <prev-catalog-hash> <prev-tick1>` mechanically proves a fold-only shift (boot); `cmp -l` on .log.bin old-vs-new (8 differing bytes at 17-24 = catalog_hash only) classifies fold-only vs behavioral per demo.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-sound-immediacy.md
# packet-plumber-v2-sound-immediacy — field notes

- **Event-stream re-bless = the 4.2-class cost, cause-documented:** adding two
  zero-payload append-only event tags (PIPE_DRAWN/NODE_SPAWNED) moved 44 T1
  manifests; ZERO pixels/logs changed (verify with `git status` before claiming
  the re-bless is pure). Divergence ticks line up exactly with first-draw/
  first-spawn ticks — that's the cause check.
- **The live fast-path emits the SAME wire event as replay, at the SAME
  apply_tick** (`inp.tick + 1` — the logged apply_tick): emit from BOTH
  step's command loop and commit_draw or the app's stream silently diverges
  from a log replay (audio on == audio off holds only if the events match).
- **Input struct field name collision:** `Input.events` is already the
  Device_Event scratch buffer — name the app-side event ref `sim_events`
  (the `ictx.events[:]` dispatch call shadows any field named `events`).
- Parity (drive_parity) dispatches ALL frames BEFORE its step loop — a
  dispatch-time event lands before the hash mark and never rides the pinned
  stream; keep `sim_events` nil there (input-parity is not the audio golden).
- Brush's frequency-stack rule (DIRECTION §3) maps to synth recipes directly:
  wire = falling low-mid "tock" (opposite direction of the arrival's rising
  sweep so they're distinguishable), spawn = low thump + mid body + high tick.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-spawn-feel.md
# packet-plumber-v2-spawn-feel — field notes

- Odin render work: rlgl ENABLES backface culling with front = CCW — any
  hand-built triangle fan/quad (annulus rings, highlight bands) must wind CCW
  in screen space or it renders NOTHING in both the rlsw captures AND the GPU
  app; and the rlsw software renderer ignores LINE alpha (fills only) — a
  fading ring must be filled geometry, never DrawCircleLines/DrawLineEx.
- NEVER build the harness with a bare `odin build harness` — the rlsw shadow
  link requires `tools/harness.sh` (ODIN_ROOT=.../raylib-sw/shadow); a stock
  build links GPU raylib, the BGRA swizzle then corrupts EVERY capture (R/B
  swap + black first frame) and the suite "fails" with misleading full-frame
  diffs.
- Predicting the next growth-window spawn is a SHADOW CLONE + ≤10-step
  replay (deterministic sim — bit-exact); the clone must deep-copy every
  Run_State array (routing/bundles/flow/crisis/health/era_gate) — pinned by a
  hash round-trip test. Pending commands (apply_tick in (tick, window]) must
  be replayed by the shadow or demo draws mid-window diverge the telegraph.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-ux-font-resize.md
# field-notes — packet-plumber-v2-ux-font-resize (2026-08-15)

- macOS compositor FREEZES the GL front buffer for occluded windows — `rl.TakeScreenshot`/`LoadImageFromScreen` repeat frame 1 forever; the reliable capture is a RenderTexture pass + `LoadImageFromTexture` readback AFTER `EndTextureMode` (the GL flush — a read inside texture mode returns the stale FBO).
- Bundled-font determinism works: LoadFontEx on a committed static TTF (fonttools-instanced Open Sans) renders the same atlas in rlsw + GPU; a font swap folds T2 text goldens but leaves T1 untouched — verify `.t1`/`.log.bin` show zero diffs.
- Pre-existing v2 HUD overlap: the top-left title/hint ran UNDER the centered health card at 1280×720 (the card is drawn after, alpha 240) — pixel-scan ink extents to prove overlaps before/after; resize anchors must use `view.win_w/h`, never the WIN_W/WIN_H constants.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-viscomm-crisis-duck.md
# field notes — packet-plumber-v2-viscomm-crisis-duck

- The masked-rc trap bit THREE times in one job: `odin build ... | head` and `2>/dev/null` both hide build failures and re-run a STALE bin/harness (once "confirming" a mutation leg that hadn't compiled, once "passing" palcheck); after ANY suppressed-output command, echo $??-style rc capture must bind odin's rc, not the pipe's — and rebuild before trusting any binary run.
- An "involved" visual element can be pixel-UNTESTABLE by design: the crisis bottleneck outline overdraws the named bundle's whole band (+ riders), so the zone's non-recede was pinned one layer out (the type-chip glyph above the sprite + at-node doorstep riders, both clear of the outline's end-caps) — when the highlight owns the surface, pin the neighbor surface.
- Empirical golden-set prediction vs reality: the briefing predicted surge/estate_surge crisis re-blesses, but a temp capture-time crisis dump showed NO active crisis at any of their captures on the current head (stale 4.2-era captions post the 08-24 re-pin) — and dublin@90s unexpectedly carries a Pool_Exhaustion crisis (which the design correctly recedes nothing for); enumerate crisis state AT THE CAPTURE TICK, never from demo comments.

# Perkins r1 addendum (2026-08-26)

- rlsw renders DrawTriangle FILLS opaque too (not just lines) — an alpha-only "recede" on a hand-built triangle surface is a goldens-path no-op; use the RGB mix (crisis_recede) and pin with a live-render leg. Worse: dublin_node_block_draw's street-oriented quads are BACKFACE-CULLED for some windings (pre-existing; deferred) — a mutation that changes only the fill can stay pixel-inert because THE FILL NEVER RENDERS there; probe with distinct-color dumps before trusting any block-surface gate.
- Test-fixture pin craft: (a) `pop()` removes the LAST row — resolving a specific crisis in a fixture needs swap-remove; (b) never re-derive the "before" value inside an assertion AFTER mutating the fixture — capture it before; (c) an `|| true` inside an expect is a vacuous pin wearing a seatbelt (shipped one AGAIN, caught again — grep every new expect for it).

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-viscomm-gauge-telegraph.md
# packet-plumber-v2-viscomm-gauge-telegraph (2026-08-25)

- bmad-build WITHOUT render_skill.py: the pre-rendered snapshot at `_bmad/render/bmad-build/packet-plumber-*/` (hash dir) is complete + project-resolved — follow its step files directly (worktree needs `cp -R <repo_root>/_bmad .` first, per the annex bootstrap); carried the waiver canon note in the PR body per the standing Silas ruling.
- Odin proc literals do NOT capture enclosing locals — bitten twice in one job (palcheck render/count closures): write file-level helper procs with explicit params, never inline `proc` values over loop/config locals.
- The health meter's bar FILL + pct draw the darkened `state_*_text` variants (not the raw state colors — the 08-15 contrast audit's ripple); pixel-scan pins must match the text variant or they read 0 px and look like a geometry bug.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-viscomm-regression-audit.md
# packet-plumber-v2-viscomm-regression-audit — field notes

- 2026-08-27: "did effect X die" audits on PP resolve mechanically with `harness motion-strip` + a fixed-pixel time-series (link centerline color per frame) — a static-vs-animated effect and its phase are provable in one strip; golden PNGs in per-era worktrees are free BEFORE/AFTER evidence (each worktree's `goldens/` is its own era's blessed render — compare those before building anything).
- 2026-08-27: a "pulsating" user memory may be a PERCEPTION of static code — the 4.1 congestion halo never pulsed; the read came from level-flicker (amber↔red re-tint) + ribbon mass. Trace the MECHANISM and the CANVAS separately or you audit the wrong thing (severed-code hunt found nothing; the salience collapse was the L1 width ruling).
- 2026-08-27: lavish input playbook per-row radio forms + one Queue button each collected a clean per-row ruling (R1 restore-via-A1 arrived as a single tagged keep-leave prompt); a Send-&-End session delivers the final feedback once on the next poll — no extra polling rounds needed after it.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-viscomm-tie-deconflict.md
- `odin test app` runs only the app package's tests (46); the render pins live under `odin test app/render` (83) — a deliberate-fail probe is the cheap way to confirm a test binary actually executes your new test before trusting a green run.
- tools/derive_a11y_palettes.py cannot parse palette.json's inline `//` comments (json.load) — run it on a comment-stripped copy; pre-existing breakage worth an issue.
- The old CVD mode tables remapped route_tie to pale amber RGB-identical to state_congested's remap — a11y overrides can silently reintroduce a base-palette collision you just fixed; always diff the mode tables too.

# r2 fixes (2026-08-25, Perkins r1 NEEDS CHANGES)

- The r1 "mutation leg" passed because the pin covered the PREDICATE, not the draw path — a pure-proc pin is bypassable at the call site no matter how good it is; the closure was a palcheck pixel scan of the REAL render (ECMP diamond topology + preview_compute + draw_route_glow, mid-angle sampling against tie_dash_on) — render tests alone still pass under the bypass, palcheck is the gate that fails.
- Odin has no #error directive — the compile-time assert idiom is `when <bad> { BROKEN :: 1 / 0 }` (constant division by zero = compile error, proven by mutation leg 3).
- palcheck sections can do full live-render checks (ClearBackground + draw_route_glow + LoadImageFromScreen) without touching goldens — the "harness capture path never invokes assists" doctrine applies to golden CAPTURES, not to analysis renders.

## SOURCE /Users/moses/code/_bmad-output/field-notes/packet-plumber-v2-visibility.md
# packet-plumber-v2-visibility

- App-layer HUD surfaces (draw_hud) are T2-INVISIBLE by construction — the harness capture path never calls draw_hud; zero golden shift needs no fold. Verify app-layer overlays with a scratch replica (rlsw shadow + LoadImageFromScreen) + PIL pixel-scan, never eyeball — the 5.3 addendum recipe, and it caught the pool bar fill at the exact right rect.
- Bundle SLOTS renumber on every topology change (bundles_rebuild in pipe-slot order) — any cross-tick bundle reference (drop-marker rings, etc.) must store + verify the canonical (lo,hi) node pair, never the slot.
- The 2.3 silent severance cull counts an SLA drop with NO event + NO Drop_Site — a why-dropped split fed only from drop_sites UNDERCOUNTS after demolitions; derive the residual (dropped - pool - queue) as "severed".
- Review swarms earn their cost: both hunters independently caught the severed undercount; the edge hunter caught the bundle-slot misanchor. `make([dynamic]T, 0, N)` has LENGTH 0 — a `counts[p.class]` guard `p.class < len(counts)` silently writes nothing (test passed only because it used a fixed [8]u32).

## SOURCE /Users/moses/code/_bmad-output/field-notes/pp-funfix-118-124.md
# pp-funfix-118-124 — field notes

- 2026-09-01 (pp-funfix-118-124): PP worktree bootstrap missed `_bmad` (fully git-ignored) — `ln -s <repo_root>/_bmad _bmad` from the worktree before any bmad-build step; the render_skill.py lives at `/Users/moses/code/_bmad/scripts/` (the MAIN repo's `_bmad/scripts/` does NOT carry it).
- 2026-09-01 (pp-funfix-118-124): PP PRs ALWAYS `gh pr create --base v2` (Silas ops ruling after #125 was opened vs main and retargeted) — the dispatch briefing names no base; don't assume the remote HEAD default.
- 2026-09-01 (pp-funfix-118-124): replay_error latches with NO reason named (#123) — bisect rejections by (a) counting router ports FIRST (4/router; spine links count), (b) computing spans (`span_between` = integer Euclidean; standard 14 / mid 16 / wide 18), (c) `sed`-renumbering spawn ids leaves dangling draw endpoints — rewrite the whole demo instead.

## SOURCE /Users/moses/code/_bmad-output/field-notes/pp-playtest-fun.md
# pp-playtest-fun — field notes (shard)

- 2026-09-01 (r2): Unblessed strategy demos FAIL `harness run` (no-manifest T1) — but `harness save` in a sandbox copy blesses AND still writes the `--stats-out` stream even for failing runs; save-then-run is the only path that also replay-verifies your evidence. Sandbox copy = `rsync -a --exclude .git --exclude _bmad` (~300 MB, carries the gitignored rlsw shadow).
- 2026-09-01 (r2): The 4-port router cap IS the topology floor — a 3-router spine for 13 nodes needs 14 ports and every short draw fails validation as a replay_error latch (ODN-11) with no message naming the cause; count endpoints before authoring minimal meshes. Span metric is integer-Euclidean-rounded (isqrt + half-up), max 14 standard / 18 wide.
- 2026-09-01 (r2): The v3 stats CSV has NO lifecycle events — breach latches, grace chips, Run_Won are invisible in it (G-row meter + C-row flags only). Ground truth for "did the breach latch / did the grace re-arm" = blessed HUD capture PNGs read directly (glm-5.3-flash native vision); stats math alone misleads (a win with 1801/1801 SLA-flagged window ticks looks like a breach that should have drained).

## SOURCE /Users/moses/code/_bmad-output/field-notes/refcheck-followup-607.md
# Field notes — refcheck-followup-607

- macOS grep has no -P/\x{2014}; for em-dash archaeology use `rg -l '"[^"]*—'` (ripgrep handles UTF-8) then a python comment-stripping pass to separate real string-literal em-dashes from comments — the raw grep flags ~70 files that are comment-only.
- The em-dash ban lint must skip dev-facing `wisp.log_*` arguments (they legitimately carry em-dashes) and `client/src/copy.gleam` (spec-verbatim home); scope = user-facing view/composition modules. A YAML step NAME with an unquoted colon (`AR-RC13: ...`) breaks the workflow parser — quote it.
- Item 3 (timeline format-mix sort) was already fixed+pinned server-side by RC4.4 (`attempt_log_appends_lifecycle_events_test` + `normalize_at` before sort); verify-and-strengthen is the honest delivery — add the inverted-mix fixture (space-form attempt `at`) rather than duplicating the canonical one.
- `git checkout -- <file>` to restore a lint negative-control is fine, but it wipes your OTHER edits in that file — re-apply them in one python replace pass, then `grep -c '" — "'` to prove the composition sites are gone.

## SOURCE /Users/moses/code/_bmad-output/field-notes/refcheck-privacy-draft.md
# Field notes — righttenantry-refcheck-privacy-draft (2026-08-02)

- `element.unsafe_raw_html` CANNOT emit a standalone HTML comment (lustre 5.6 wraps inner_html in `<tag>…</tag>`; a `!--` tag renders `<!-->TEXT</!-->` and LEAKS visible text) — for a rendered comment, post-render `string.replace` on the exact serialized open tag + a presence/uniqueness test pin.
- `functions.edit` batches are ATOMIC — one bad `oldText` rejects every edit in the call, and `gleam format` reflows split strings between runs; re-read the formatted file before re-issuing a failed batch.
- Privacy-page copy tests must assert the RENDERED form: apostrophes come back as `&#39;` (houdini escape) — "landlord's" in an h2 pin fails against raw text.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-agent-model-flash.md
# Field-notes shard: righttenantry-agent-model-flash

Date: 2026-08-06 · Status: done (badge-out, NO PR in RT — re-dispatched to RightTenantryAgents)

## What bit me / high-value for the RT-Agents minion

- **The model does NOT live in RightTenantry.** Gru's briefing said "AI agent code lives in `server/src/ai/`" — that is the *orchestration* layer. RT is a **pure ADK client**: `server/src/ai/ai_client.gleam` builds a ScoringRequest to `AI_SERVICE_URL` with NO model field; `model_version` (lines 1373, 1784) is *decoded from the ADK response and logged*, never set by RT. The only `gemini` strings in RT are redaction regexes (`typst_sanitize.gleam`, `dsar/sql`) + test fixtures. **All model selection is in `RightTenantryAgents/tenant_scorer/config.py`** (`get_agent_model`: `{AGENT}_MODEL` env → `DEFAULT_MODEL` env → `_DEFAULT_HARDCODED="gemini-3.5-flash"`; every agent calls `get_agent_llm(agent_name)`). A future "change the model" job targets RT-Agents, never RT.
- **Prod models are Terraform-managed, not code-managed.** `RightTenantryAgents/deployment/terraform/variables.tf` defaults are NOT overridden by `production.tfvars`/`staging.tfvars`, so they ARE prod. A code-only PR (bumping `config.py` `_DEFAULT_HARDCODED`) changes only the **fallback** — production runs on the env-overridden Terraform values. Moving prod = change `variables.tf` (or `vars/*.tfvars`) too. Two surfaces, both must change. Current prod map (verified by reading `variables.tf` directly — note: `rg` output through the harness MASKS `gemini-*` tokens as `n.*`; `cat`/`read` shows real strings):
  - Flash tier (`default_model`): document_extractor, anonymizer, pii_reviewer, income_verifier, reference_validator, rental_history_verifier, inline judges → `gemini-3.5-flash`
  - Pro tier (pinned individually): risk_scorer, verification_compliance_judge, final_compliance_reviewer, consistency_checker, personal_statement_analyzer → `gemini-3.1-pro-preview`
- **Resolved rulings for this cost-optimization (carry into the RT-Agents PR):** target = `gemini-3.6-flash` for **ALL** agents (both tiers). It is an **UPGRADE not a downgrade** — Gru verified via Artificial Analysis: 3.6 Flash beats 3.1 Pro Preview on intelligence (50 vs 46: GPQA Diamond + Humanity's Last Exam + AA-Omniscience), cost ($1.16 vs $1.74/M tok, ~33% cheaper), AND speed (220 vs 122 tok/s). So `default_model` 3.5→3.6-flash AND all 5 Pro vars `gemini-3.1-pro-preview`→`gemini-3.6-flash`. Model ID `gemini-3.6-flash` confirmed GA 21 Jul 2026 (Google blog + DeepMind card + Cloud docs + Vertex pricing); do one live smoke-test inference before merge. Judge sanity-check stays as a LIGHT safety net (risk bar low). Leave retry/fail-fast logic untouched.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-agents-model-single-source.md
# Field notes — righttenantry-agents-model-single-source

- 2026-09-05: BSD (macOS) sed has no `0,/re/` address — a "mutation test" silently mutates NOTHING; worse, `git checkout -- <file>` afterwards nuked my real unstaged edits. Mutation tests: python replace + cp backup + diff-verify restore, never sed+checkout.
- 2026-09-05: bmad-quick-dev is GONE from the canonical home (successor bmad-build can't render — no `_bmad/scripts/render_skill.py`); standing waiver path worked: self-contained briefing + waiver note in PR body + run bmad-build's review-prompts (`review-prompts/*.md`) directly as herdr mega-minions — step-04 discipline without the renderer.
- 2026-09-05: `herdr agent wait <pane> --until idle` is the working syntax (skill doc's `herdr wait agent-status --status` is a newer/other CLI); `--until done` fires only in background panes, `idle` when seen.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-agents-prod-scale-to-zero.md
# field-notes: righttenantry-agents-prod-scale-to-zero

- 2026-09-04: `ledger set <id> in-review` is REFUSED until the PR URL is on the row (`!! in-review requires a PR URL`) — the natural order is backwards: run `ledger pr <id> <url>` BEFORE `set in-review` (error is loud, no harm, but it's a guaranteed re-run otherwise).
- 2026-09-04: RT `.github/workflows/deploy-to-prod.yml` path filter EXCLUDES `deployment/terraform/**` and NO CI runs terraform (prod workflow = `gcloud run deploy --source .`, inherits Terraform-managed flags) — tfvars PRs are merge-inert; "merge ≠ prod change" is a workflow-read fact, state it in the PR body every time.
- 2026-09-04: RT pre-commit hooks build a `.venv` via uv (149 packages, ~1 min) even on a tfvars-only commit in a fresh worktree — slow first commit is the hook bootstrap, not a hang.
- 2026-09-04: RT pins terraform values in tests/unit/test_concurrency.py — grep that file BEFORE flipping any prod tfvars value (a value flip without the pin flip = red suite on the NEXT unrelated PR, since pr-checks skips deployment/ paths; it detonated on the #177 promote).
- 2026-09-04: comment-mentions of `attr = value` in tfvars false-match unanchored `re.search` extractors (comment precedes assignment in file order) — anchor value-parsing regexes to line starts (re.MULTILINE) and prove with a negative control (revert the value → suite must FAIL).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-agents-tf-in-ci.md
# Field notes — righttenantry-agents-tf-in-ci

- 2026-09-05: bmad-build's render_skill.py doesn't exist in RTA's older `_bmad` install — the skill's step files carry everything; read them directly from the skill dir (template placeholders like `{workflow.review_layers}` stay unresolved; improvise the named layer from the playbook's lens list).
- 2026-09-05: RTA WIF trap: `roles/iam.serviceAccountTokenCreator` on a repo-wide principalSet lets ANY PR-ref token mint write-SA tokens WITHOUT workloadIdentityUser — ref-scoping only the workloadIdentityUser binding is NOT enough; scope every WIF-granted role on the write SA.
- 2026-09-05: GCS backend has NO state locking below Terraform 1.10 (CI pins ~1.7) — never grant a planner objectCreator "for the lock": at 1.10 a creator-without-delete strands the lock. GitHub concurrency groups per env are the real plan/apply mutex. Also: legacy `roles/storage.viewer` = buckets.list ONLY (no buckets.get/objects.get — verify role contents against cloud.google.com/iam/docs/roles-permissions, don't trust memory).
- 2026-09-05: Perkins r1: predefined-role memory CANNOT be trusted — bigquery.viewer and resourcemanager.projectIamViewer don't exist (real: bigquery.metadataViewer; no predefined project-IAM read role). gcloud-verify every roles/* string against cloud.google.com/iam/docs/roles-permissions before it reaches tfvars; the tripwire test (test_terraform_ci_invariants.py) now pins the inventories.
- 2026-09-05: Perkins r2: "viewer" != read-only — roles/aiplatform.viewer carries aiplatform.specialistPools.update (WRITE). ANY predefined role on a PR-reachable SA needs its full permission list gcloud-verified, not just its name; zero-write claims need per-permission pinned custom roles.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-agents-wif-durable.md
# Field notes — righttenantry-agents-wif-durable

- 2026-09-06: `herdr wait agent-status` doesn't exist in this CLI build — use `herdr agent wait <pane> --until idle --timeout N` (and `pane run` for prompts).
- 2026-09-06: invariant tests asserting on `_resource_block` output must strip WHOLE-LINE comments (`^\s*#` + MULTILINE) — comment prose inside a tf resource block can satisfy substring asserts (masked a real condition regression in my first draft); unanchored `#[^\n]*` corrupts HCL strings containing '#'.
- 2026-09-06: PR-branch lint (ruff F541) runs in pre-commit AFTER your message-drafting — run `uv run ruff check` on touched test files before committing; f-strings without placeholders (even with `{{}}` escapes) fail the hook and force an amend dance.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-analytics-568-617.md
# Field notes — righttenantry-analytics-568-617 (PR #624)

- OAuth first-touch: `wisp.get_query` percent-decodes (round-trip clean), and a Signed wisp cookie value is base64url-wrapped by `sign_message` — ANY payload string is header-safe, so `uri.query_to_string` output is a valid cookie value; tests can craft valid signed cookies with `simulate.cookie(req, name, raw, wisp.Signed)` on a `simulate.request` (same canned secret key base).
- The `rt_consent` cookie for tests must be set as a RAW header (`simulate.header("cookie", "rt_consent=" <> percent_encode(json))`) — `simulate.cookie(..., wisp.PlainText)` base64s it and `read_raw_consent_cookie` reads verbatim (mirror payment_verify_integration_test's helper).
- "Plan §5" (Meta consent gating: Lead + CompleteRegistration consent-gated, Purchase carve-out) has NO plan doc on disk — cite the code call sites (meta/dispatch.gleam:18-22) instead; and the em-dash lint exempts `wisp.log_*` string args, so decision logs can carry em-dashes.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-apply-form-scrub-fix.md
# righttenantry-apply-form-scrub-fix (2026-08-10)

- The PostHog `sanitize_properties` scrub is the ONLY inline-JS-in-Gleam scrub
  on `/apply`; grep `sanitize_properties` to find it — bare `scrub` has 20+
  unrelated hits (model-version scrub, Stripe/GoTrue PII scrub, etc.). The SPA
  shell's PostHog init (Makefile + Dockerfile `RT_ANALYTICS` perl) has NO scrub.
- Testing inline-Gleam-emitted JS under `node --test`: extract the `<> "..."`
  string-literal block from the .gleam source (anchor on stable tokens like
  `sanitize_properties:function(p){` … `return scrub(p);`, span from the opening
  `<>` to the last literal's closing `"`), unescape Gleam escapes, eval it.
  Tests the EXACT shipped bytes with no module refactor and zero leak risk on
  the defended token-redaction invariant (redaction stays always-on inline).
- `instanceof Node` guards are BLIND under `node --test` (no `Node` global
  there — the exact "Node tests blind to browser semantics" trap). For a
  DOM/host-object guard that must be runtime-tested in Node, use
  `Object.prototype.toString.call(o)` (plain-object check): skips ALL host
  objects, not just Nodes, and needs no browser shim. Prove the guard bites by
  neutering it in the shipped source and confirming the test goes red.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-csp-enforce-allowlist.md
- 2026-08-05 (righttenantry-csp-enforce-allowlist): Sentry `sentry-cli` (classic, /opt/homebrew/bin) with `help@righttenantry.ie` token has event:read — but the NEW `sentry` CLI's own token 403s; use `curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" https://sentry.io/api/0/organizations/right-tenantry/events/?query=issue.id:N...` (org-scoped, NOT /api/0/issues/) to read event payloads; `/api/0/issues/{id}/events/` 404s.
- 2026-08-05 (righttenantry-csp-enforce-allowlist): CSP `blocked-uri` values like bare `properties` or same-origin script blocks under `'self'` are physically impossible from real browsers — the public unauthenticated /api/v1/csp-report endpoint forwards any parseable body (1-in-4 sample); junk reports land in Sentry as csp_violation issues. Verify impossible payloads before allowlisting; Sentry short-ID groups can mix multiple blocked_uris under one title (RT-PROD-5 was 90% Meta subpaths + 2 junk self-origin events).
- 2026-08-05 (righttenantry-csp-enforce-allowlist): worktree bootstrap does NOT copy node_modules — `ln -s /Users/moses/code/RightTenantry/node_modules` before `make build` (tailwindcss). Test reviewers (mm-* panes) finished as `idle`; poll `pane get` not `wait agent-status`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-csp-posthog-allowlist.md
# righttenantry-csp-posthog-allowlist — field notes

- 2026-08-06: Security-control briefings can ship a WRONG mechanism — ground-truth the stated reason against disk + vendor docs before crediting. Here both the briefing's reasons ("array_loader fetches from eu.posthog.com" + "ingestion goes there") were FALSE: every PostHog load is same-origin proxied (`api_host:'/_ph'` + `/_ph_assets/static/array.js`); `ui_host` is links-only per PostHog's PostHogConfig reference. Resulted in a no-op doc comment, not the proposed CSP widening.
- 2026-08-06: PostHog reverse-proxy architecture = no CSP allowlist needed for the enforce flip. `api_host` carries all data AND the derived asset host (recorder/surveys/toolbar.js); `ui_host` is link/navigation surface only; the toolbar (sole ui_host fetcher) is unused in prod. eu.posthog.com is absent from the Sentry Report-Only list. Documented in `server/src/csp.gleam` "deliberately NOT allowlisted" section so it isn't re-litigated.
- 2026-08-06: `make build` fails in fresh RT worktrees on `tailwindcss: command not found` (dev-dep CLI not bootstrapped) — unrelated to server changes. Use `make build-server` + `make test-server` for server-only verification (1220 passed / 0 fail there).
- 2026-08-06: An invariant TEST only proves value if it BITES — a passing assertion alone is weak evidence. For a "X must stay absent" lock, run a negative control: inject X into the source, confirm the test goes red (full `make test-server` — unitest ignores gleeunit's `-n` filter, so don't bother targeting one test), then `git checkout` the file to revert to HEAD. Here injecting eu.posthog.com into connect-src flipped `policy_never_allowlists_posthog_cloud_host_test` red (1220p/1f) — proof the lock catches any directive addition, not a tautology.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-ctr-metadata-619.md
# righttenantry-ctr-metadata-619

- 2026-08-14: SEO metadata lives in `layout.page(title:, description:)` at the top of each SSR content view — the `| RightTenantry` suffix is auto-appended by `layout.gleam` (`html.title([], title <> " | RightTenantry")`), so views carry the string minus the suffix; description flows to both meta + og:description from one field. Pin the RENDERED html, not source strings.
- 2026-08-14: Lustre (houdini, erlang target) escapes apostrophes to `&#39;` in BOTH text nodes and attributes, and renders attributes sorted by name (content precedes name/property) — metadata test pins must use `escape_for_html` + exact tag terminators (`</title>`, `content="…" name="description"`) or they silently no-op.
- 2026-08-14: `rent_post.title` is a single field feeding `<title>`, H1, JSON-LD headline and og:title — changing the SEO title changes the visible H1 by design (field doc: "Full SEO title and H1"); rpz's `WebApplication` JSON-LD description mirrored the old meta description and needed the same-string sync (mirror rule generalizes beyond OG).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-demo-pdf-watermark.md
- 2026-08-24 (righttenantry-demo-pdf-watermark): typst PDFs embed CreationDate/ModDate (info dict + XMP) AND a random xmpMM:InstanceID + trailer /ID pair — byte-identity tests must normalize all six patterns (re:replace chain in the FFI); Erlang REBINDS a var in one scope = badmatch, and a fun closing over `Bin` for every step is NOT a chain (B1..B5 were independent replaces).
- 2026-08-24 (righttenantry-demo-pdf-watermark): `place` alignment semantics — `alignment` aligns within the CONTAINER then dx/dy OFFSET it (dx:50%,dy:50%+center lands bottom-right); centering = `place(dx: 0%, dy: 0%, center + horizon, body)`. And a page `background:` is painted UNDER content: a full-bleed cover block hides it — add an explicit `place` at the end of the cover block.
- 2026-08-24 (righttenantry-demo-pdf-watermark): demo PDFs in RT are pre-baked STATIC assets (build-time typst, `demo/pdf_prebake`) — the runtime server has NO demo mode; the client demo intercepts downloads (`model.demo_mode` is the only canonical demo check). Watermark seam = the shared template + a `watermark` flag on `generate`; prebake passes True, handler False.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-demo-polish-2.md
# righttenantry-demo-polish-2 field notes

- Toast mismatch root cause = PRODUCTION STALENESS, not demo code: prod
  bundle ships pre-#615 `fixed bottom-4 right-4 z-50` (main last merged
  Aug-10, 36 commits behind staging); demo/staging/develop all render
  `fixed top-20 right-4 z-[2147483001]` through the ONE shared toast
  component. Grep the deployed client.js for the position class — that IS
  the runtime truth; component-level parity checks (polish-1's) can't see
  a stale deploy. Matching prod would regress the #615 banner guarantee.
- polish-1's "real twin" verdicts failed the same way twice: verify the
  DATA feeding a render gate, not the gate's existence. Compare-top-3 hid
  because demo_store set `score_based_rank` = overall SCORE (86, 78...)
  instead of competition rank (1..8) — `top_three_ids` needs rank in
  {1,2,3} so the button never rendered. Port the server's competition_ranks
  + score-DESC-NULLS-LAST ordering (application_list_handler.gleam) into
  the demo store.
- Real demo PDF depth came from data, not the template: the typst template
  already renders Analyst's Brief/Category Notes/Recommendations/Scoring
  priority — they were absent because pdf_prebake's extras lacked
  detailed_insight/category_notes/recommendations/category_weights.
  Evidence items carry a `structured` BOOL — don't decode them as
  string-dicts in tests (gleam_json 3.x Json is opaque; parse with
  decode.field chains). Keep screen↔PDF consistent: same flags arrays in
  demo_store analysis_for AND pdf_prebake payloads; co-applicant income
  must not double-list as an additional income source.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-draft-grace-period.md
# righttenantry-draft-grace-period — field notes

- `git checkout -- <file>` after a sed-tamper test-run wiped ALL uncommitted
  work in that file (lost the whole new test file's edits; had to re-apply).
  Revert tamper lines with sed on the exact line, never checkout.
- RightTenantry vacancy has NO closed_at: manual-close moment =
  `closed_notified_at` (stamped in the same UPDATE by close_vacancy.sql);
  `vacancy.updated_at` never bumps on close (editable-fields-only trigger) —
  do not anchor time-based logic to it.
- Worktree bootstrap gap: `make build` fails on `tailwindcss: command not
  found` — `ln -s /Users/moses/code/RightTenantry/node_modules node_modules`
  fixes it (gitignored, never committed).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-dublin-rents-q2-2026.md
# righttenantry-dublin-rents-q2-2026 (2026-08-24)

- OG-card orphan test (`content_pages_point_at_their_own_og_cards_test`) fails on ANY committed `priv/static/og/*.png` not pinned in its pairs list — every new series post needs its card pinned there (plus the `let assert Ok(post)` lookup).
- Worktree bootstrap missed `server/.env -> ../.env` (main checkout has it) — without it `make run` panics "DATABASE_URL not set"; add the symlink before smoke-testing.
- og cards: `rsvg-convert -w 1200 -h 630 card.svg -o card.png` is the pipeline (PNG 1200x630 RGB); verify the render via `bin/vision-read` — and never sed a `</` inside an SVG text tag (it ate `</text>`).
- Data note for next quarter: verify figures against the live reports (Daft PDF/press + rtb.ie "latest" page — Q1 2026 RTB index still unpublished as of this PR; Q4 2025 rows stay dated explicitly).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-find-stuck-terminal.md
# righttenantry-find-stuck-terminal — field notes

- 2026-08-11: the backtick command-substitution trap hits `psql -c "..."` SQL **comments** too, not just `gh --body` heredocs — a `-- \`kind\` is...` comment inside the double-quoted `-c` arg got bash-substituted (`line N: kind: command not found` to stderr, query still ran). No backticks anywhere inside a `-c "..."` string, comments included.
- 2026-08-11: `gh pr create --body-file <path>` errors `open ...: no such file or directory` if you drop the extension by reflex — the file exists, you just named it wrong. Pass the real filename.
- 2026-08-11: macOS `grep` has no `-P` (perl-regex) — to find non-ASCII / specific codepoints use `perl -CSD -ne '... \x{2014} ...'`; the plain-byte form silently misses multibyte chars (first check wrongly said "0 em-dashes", `-CSD` found the U+2014 I'd added).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-completion-ps.md
# righttenantry-form-completion-ps — badge-out shard (2026-07-31)

- The worktree `.env` points at the STAGING Supabase; production is a different project — use `./deployment/db.sh prod -c "..."` (pulls the URL from GCP Secret Manager; psql `-v` var passing doesn't survive the wrapper, inline literals instead).
- Read-only prod funnel queries are fast and safe at aggregate level (counts/lags/dates) — do them EARLY; they reframed the whole session (email channel exonerated, on-page abandonment indicted before any lavish round-trip).
- Moses answers lavish question pages well when each question has its own Queue button + a "which rulings I need most" summary in the poll `--agent-reply`; he ended both sessions cleanly with Send & End after ~2 exchanges.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-copy-revision.md
# righttenantry-form-copy-revision — field notes

- User-ruled verbatim copy + GLOBAL em-dash ban: the acceptance grep must be run over non-comment code lines (indented comments defeat a naive `rg -v '^\s*//'`) — and "user-facing" excludes logs/SQL comments, which is what the 85 surviving server literal `—` hits all are.
- The client copy_test sentence-count pins (≤2 by terminal punctuation) silently constrain dash replacements — sentence breaks can trip them; colon/comma substitutions keep the budget. Case-sensitive `string.contains` also breaks on sentence-initial capitals.
- `edit` tool batches are atomic per call AND per file — a cross-file batch fails wholesale on the first mismatch, and dropping a trailing `,` from oldText leaves `",,"` doubles; perl `s/",,",/"` rescued all five.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-e2e-pass.md
# Field notes — righttenantry-form-e2e-pass

- agent-browser on this form: `click` silently no-ops on below-fold elements (emulated viewport + smooth scroll) — eval `scrollIntoView({behavior:'instant'})` first; `fill` can't set `input[type=date]` (set value + dispatch input/change); click the `label[for=field-X]` not the visually-hidden radio. 4/5 mega-minions hit the same three traps independently.
- posthog-js `_is_bot()` drops ALL capture for HeadlessChrome UAs — local analytics E2E sees zero network events; wrap `window.posthog.capture` in-page and assert the call stream instead. Also: `rt_consent_test=1` auto-accepts with analytics:false — for analytics legs, click the real banner's Accept-all.
- form-bug-hunt's documented `test+{SCENARIO}-{RUN_ID}@example.com` template produces `/` in email local parts (slug contains `/`) which shared/email.is_valid rejects — fixed in SKILL.md (sanitise `/`→`-`, ≤64 chars); Resend 422s example.com recipients locally, use `delivered+tag@resend.dev` when the send itself must succeed.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-funnel-w0.md
# Field notes — righttenantry-form-funnel-w0 (2026-07-31)

- `server/priv/static/*` is gitignored with a per-file exception list — any new
  static asset MUST get a `!path` exception in `.gitignore` or it silently
  never deploys (caught only by the review swarm).
- Squirrel: `run_squirrel.sh` sources `.env` and clobbers your override —
  run `cd server && DATABASE_URL=postgres://test:test@localhost:54321/righttenantry_test gleam run -m squirrel`
  directly after `make test-db-up` (never let it point at staging), and
  revert the formatter churn it leaves in unrelated generated files.
- gleam `decode.subfield` + `decode.optional` does NOT tolerate missing keys
  (the whole decode fails) — for back-compat payloads use
  `decode.optional_field(..., default, ...)` at the parent level.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-nojs-submit-fix.md
# righttenantry-form-nojs-submit-fix — field notes

- 2026-08-04: agent-browser's DEFAULT session is shared machine-wide — a sibling minion's drive hijacked my browser mid-scenario (I landed on THEIR page on THEIR port). Always `--session <job-id>`; also its clicks race `scroll-behavior: smooth` — `eval scrollIntoView` → sleep ~1.2s → `find first '<css>' click` is the reliable pattern.
- 2026-08-04: Playwright `javaScriptEnabled:false` kills in-page rAF, so actionability-gated actions (click/check) time out as "not stable"/"detached" — but fill/select/boundingBox work, and CDP evaluate still runs (probe with it to PROVE page scripts are off: stepper never activates). Drive clicks via `page.mouse.click` at boundingBox center, with a click→isChecked→retry helper for radios.
- 2026-08-04: RightTenantry local E2E recipe: `cp .env server/.env` + perl-edit `DATABASE_URL` to the docker test DB AND `PORT` to a free port (dot_env overrides process env at runtime; port 4000 was held by a sibling's BEAM — never `make kill` blindly). Seed landlord+vacancy straight from test_db.gleam's SQL via psql; AI-trigger 401-retry noise in the server log is expected locally, submissions still persist.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-resume-progress-fix.md
# Field notes — righttenantry-form-resume-progress-fix

- agent-browser `click` silently no-ops on the stepper's Back/Continue
  buttons under an emulated mobile viewport (sticky progress bar overlap) —
  drive stepper nav via `eval` clicks on `[data-testid=step-continue-<id>]`;
  `fill` can't set input[type=date] either (set value + dispatch input/change).
- Reseeding a resume leg without the UI: INSERT into application_draft with a
  url-safe-base64 `continue_token` and the draft `fields` JSON — the token
  seam works for any hand-minted row, no Resend round-trip needed.
- Review-swarm note: `make build` in a fresh worktree fails at tailwind
  until `npm ci` (worktrees ship no node_modules; `make test` never notices
  because js-tests use bare node).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-save-resume-f3.md
# Field notes — righttenantry-form-save-resume-f3

- gleam `edit`-tool batches are atomic per call — when one oldText in a
  multi-edit call fails, NONE of the edits land; re-apply the survivors
  individually (lost two email_client edits + a decoder edit this way,
  caught only by compile).
- Lustre sorts HTML attributes alphabetically when rendering
  (`name="_form_loaded_at" type=... value=...`) — never write HTML string
  splits that assume source attribute order.
- form.js's `_form_loaded_at` IIFE overwrites the SSR stamp on EVERY load —
  any deliberate server-side backdating (like the resume page's) needs a
  marker guard in form.js, not just the SSR change. And: `.gitignore`
  whitelists every `server/priv/static/*.js` individually — a new static JS
  file is invisible to git until whitelisted (blocker caught in review).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-form-stepper-f1.md
# righttenantry-form-stepper-f1 — field notes

- `server/priv/static/*` is git-ignored with a per-file whitelist — every new static asset needs its `!` line in `.gitignore` or it deploys as a dead script tag while SSR pins (which only assert the tag) stay green (review swarm caught it).
- Error-summary hrefs are already full anchors (`#field-<key>`) and upload-slot `.field-error` spans need inline `display:flex` (they never get `.has-error`) — same display bug also exists in form.js's preflight `showInlineError` (deferred).
- `dot_env.load_default()` overrides the process env — to repoint a local dev server, replace the `server/.env` symlink with an edited copy (gitignored); staging DB lags develop migrations (submissions 500 on `submitted_ip_text`), so E2E against a local Docker DB + seeded vacancy; timing trap rejects <2s fills as spam — sleep before scripted submits.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-gcp-cost-analysis.md
# Field notes — righttenantry-gcp-cost-analysis

- 2026-08-06 (lavish mid-review): after overwriting the dashboard HTML mid-review
  (Gru's "Gemini API is triple-blended, not personal" correction), the browser kept
  serving the CACHED old version — the user said "nice" to the stale "personal"
  framing. The poll's `dom_snapshot` was the only ground truth that the old content
  was still on screen. Lesson: after a mid-review file rewrite, either
  `lavish-axi <file> --reopen` or explicitly tell the reviewer to reload AND verify
  via the NEXT poll's dom_snapshot that the new content actually rendered before
  trusting any "looks good" verdict.
- 2026-08-06 (GCP cost attribution): a single GCP project can serve MULTIPLE
  use-cases — `iginsider` blended RT Facebook-ad creative + RT agents + personal
  YouTube. Never assume one project = one use-case; group by project but FLAG
  use-case blending and require app-side resource/call LABELS to attribute.
  The project boundary is the only clean line billing data gives you.
- 2026-08-06 (GCP billing export): `gcloud` has NO billing-export command and the
  public Cloud Billing v1 API does not expose the BigQuery export config — enabling
  it is CONSOLE-ONLY. From a minion shell you can create the target dataset (`bq mk`)
  and write the attribution queries, but flipping the export is the user's 4 console
  clicks. Required role: billing admin (`billing.accounts.update`). The Detailed
  (resource-level) export's `resource.name` splits Cloud Run by service with NO app
  change; use-case attribution inside a project still needs app labels.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-guarantor-autofill-fix.md
# righttenantry-guarantor-autofill-fix — field notes

- 2026-08-05: The reported bug has TWO layers. (1) `autocomplete_for`'s `_ -> "off"` fallback stamped an explicit autofill opt-out on every non-whitelisted field (guarantor + siblings) — fixed with per-field WHATWG tokens. (2) THE REAL BLOCKER, found via real-browser (Chrome 150) verification: Chromium's `kTypeValueFormFillingLimit = 9` (per type, per fill, counted across the whole form in DOM order) — the apply form has 10 NAME_FULL / 11 PHONE / 11 EMAIL fields (About You + 3 reference trios + 3 co-applicant cards × employer/guarantor blocks), so the primary guarantor block (10th/11th instances) is suppressed on every fill action. This reproduces the user's symptom exactly ("other sections fill; guarantor suggests but doesn't populate") and the `off` fallback was never the full story.
- 2026-08-05: The ONE honest token lever vs the cap: `tel` vs `tel-national` are separate Chrome type buckets — mapping co-applicant phones to `tel-national` keeps every phone fillable (primary at 5 `tel`, co-applicants at 6 `tel-national`; verified guarantor_phone fills). NAME/EMAIL have NO alternative standard tokens — they stay capped unless the co-applicant duplication is reduced (product decision). Don't chase the cap with non-standard tokens.
- 2026-08-05: Real-browser autofill verification technique that works: launch system Chrome with a fresh `--user-data-dir` + `--remote-debugging-port`, drive via raw CDP (Node 22 has a built-in WebSocket): `Autofill.enable` + `Autofill.setAddresses` (fields: NAME_FIRST/NAME_LAST/NAME_FULL/EMAIL_ADDRESS/PHONE_HOME_WHOLE_NUMBER/COMPANY_NAME) then `Autofill.trigger` with `fieldId` = `DOM.describeNode`'s backendNodeId + the address inline. `chrome://autofill-internals` (own tab, all scope checkboxes) logs fill decisions + field types — the only ground truth for why fields skip. Seeding Chrome's Web Data DB directly (addresses/address_type_tokens, FieldType enum: NAME_FULL=7, EMAIL_ADDRESS=9, PHONE_HOME_WHOLE_NUMBER=14, COMPANY_NAME=60) also works but CDP setAddresses is cleaner. DOM mutation tests (deleting fields) invalidate Chrome's cached form structure — results are garbage; use fresh page loads per experiment.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-mobile-form-hunt.md
# righttenantry-mobile-form-hunt — field notes

- The status-stepper "escapes card" bug needed BOTH `min-w-0` on the rail AND `w-full` on its `flex flex-wrap` wrapper — the wrapper is a flex item of a `flex-col items-center` column where align-items:center sizes items by CONTENT (cross-axis), so flex-shrink/min-width never apply; verify flex geometry by walking the ancestor chain in the DOM, not by reading classes.
- `dot_env.load_default()` overrides process env — to point the dev server at a local Docker DB, copy `server/.env` (rm symlink + cp) and patch it; a fresh `server/.env` symlink must be created in new worktrees (only root `.env` is bootstrapped) or the server panics "DATABASE_URL not set".
- agent-browser `eval` returns `["<json-string>"]` (array-wrapped double-encoded) — parse with a loop, not a single json.loads; the default session is shared machine-wide, always `--session <job-id>`; `set viewport W H 3` gives DPR3.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-mobile-layout-1.md
# righttenantry-mobile-layout-1 (PR #631)

- Briefing premise "vacancy_detail already handles the compare-bar bottom padding" was FALSE — grep showed NEITHER page had it (only comparison.gleam `pb-40`); both fixed with conditional `pb-28`. Always grep disk, not the briefing's current-state claim.
- Application notifications carry only the application id (`entity_type=="application"`, `entity_id`=aid); real server emits NO such notifications today (all are `vacancy`/`reference_call`) — the demo fixtures are the only writer. Client-side resolution (demo store authoritative; live resolves from loaded leaderboard, else None) was the contract-safe, no-schema-change fix.
- `shrink-0` on filter pills/stepper stops is the root-cause fix for mid-word truncation in an `overflow-x-auto` rail (not `text-overflow: ellipsis`, which permanently clips). Lustre `list.find_map` returns `Result`, not `Option` — hand-rolled the recursion.

r2 (PR #631): resolving an application notification client-side to a vacancy requires the loaded-data source be TAGGED with the vacancy it was fetched for — `model.leaderboard` survives navigation into VacancyEdit/Comparison/ApplicationDetail (only VacancyDetail/Handoff reset it), so `get_vacancy_id(route)` could fabricate a wrong vid from a stale Success. Grep `/server/src/ai/` (not just `notification/`) when the briefing claims "no real producer" — `ai_notifications.gleam` emits `entity_type: application` (AI-failure) with only the app id today. Extract the routing decision into a pure helper (`notification_target_path`) so BOTH entity types get a click→route pin; the modem.push effect is opaque. Reviewers pinged TWO real blockers — verify before trusting the reviewer's "all green" but they were both genuine here.

r3: REVIEWERS CATCH RESIDUAL RACES and arm-drift a reviewer round later — (1) any response message that fills cached route data must carry the id it was dispatched for and apply on a match-guard (a late `ApiReturnedLeaderboard` from prior vacancy after A→B nav re-fabricates; `LeaderboardResponse` messages needed the vacancy id + guard, mirroring the existing refresh-handler request-id guard). (2) When a helper is meant to be shared across real+demo update arms, a circular import (client↔demo_update) is not an excuse to leave one arm inline — move the helper to a NEUTRAL `helpers/` module both import, and call it from BOTH arms (the demo arm was still no-opping vacancy-typed clicks because it re-implemented only the application branch).

r4: EVERY guard must tag its OWN fetch's model-update set-site — a shared helper/guard is only as complete as its set-sites. Adding a guard that compares against a cached tag, then failing to set that tag in the COLD-BOOT fetch paths (session-restore + enter_demo, where `modem.init` doesn't dispatch BrowserChangedUrl so handle_browser_change isn't reachable) DROPS the legitimate first response and strands the UI at NotAsked forever — a live-product regression introduced by the guard itself. Also: guard the Error arm, not just Ok (W1). When a reviewer says "the guard misses the cold-boot paths", enumerate EVERY fetch dispatch site (including boot/entry effects) and pair each with its model tag.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-oauth-posthog-fix.md
# righttenantry-oauth-posthog-fix

- The inline analytics bridge snippets live in BOTH `Makefile` (build-client) and `Dockerfile` perl chains, each with their own substring-pin guard list — any snippet change must hit 4 places (2 chains + 2 guards), and the guard pin must be a substring UNIQUE to the changed arm (e.g. reset-arm adjacency), or the guard can't detect the regression.
- Squirrel regen: `gleam run -m squirrel` with `DATABASE_URL` pointed at your own test container — then revert the known whitespace churn in `ai/sql.gleam` + `application/sql.gleam` + `inbound_email/sql.gleam`. `(xmax = 0) AS is_new` in an upsert RETURNING codegens cleanly as `Bool` (atomic insert-vs-update flag — reviewers prefer it over a pre-check SELECT).
- The analytics bridge cookie lifetimes are a cross-cutting contract: `rt_landlord_id` (identify, 60s) vs `rt_landlord_external_id`/`rt_ph_reset` (sentinels, 10s) — pinned in 3 test assertions, 2 build guard lists, and multiple doc comments; changing one without the others is a silent contract drift.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-per-applicant-remind.md
# righttenantry-per-applicant-remind — field notes

- 2026-08-08: Squirrel codegen in a fresh RT worktree — `SQUIRREL_DIRECT_DATABASE_URL` in the symlinked `.env` points at the Supabase CLOUD pooler (prod read). Spin up a dedicated local Postgres (`docker run -d --name rt-<job>-test-db -p 5432X:5432 postgres:16-alpine`), `TEST_DB_PORT=5432X bash scripts/reset-test-db.sh`, then `cd server && DATABASE_URL+SQUIRREL_DIRECT_DATABASE_URL=postgresql://test:test@localhost:5432X/righttenantry_test gleam run -m squirrel`. This run reflowed BOTH `server/src/ai/sql.gleam` AND `server/src/application/sql.gleam` (not just `ai/` — revert all churn not yours).
- 2026-08-08: gleeunit prints passing tests as dots only — never the test name — so "N passed" does NOT prove a NEW test ran vs. was silently skipped/tag-gated. Verify by a break-and-revert probe: flip one `should.be_true`→`should.be_false`, re-run, confirm exactly 1 failure with your test's path, then revert.
- 2026-08-08: em-dash ban (U+2014) is enforced by `client/test/copy_test.gleam`'s `no_em_dash_test`, which scans ONLY `copy.toast(code,ctx)`/`copy.page(code,ctx)` — a NEW copy fn with non-(code,ctx) args (e.g. `remind_applicant_toast_copy(reminded,followup)`) is NOT covered by it; verify its strings by inspection. macOS `grep` has no `-P` flag — scan for the codepoint with python (`'\u2014' in line`).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-611-panel-persist.md
# Field notes — righttenantry-refcheck-611-panel-persist

- The issue's root-cause theory (Lustre `decode2` → `DispatchedEvent` swallow) was WRONG — instrument the compiled bundle in a live browser repro (add console.log to `decode2`/`dispatch2` in `server/priv/static/client.js`, restart server) before trusting a runtime-layer diagnosis; the real bug was a view-level dict-key mismatch (`text_input(slot, …)` vs `dict.get(edit, call.reference_call_id)`), a 3-line app fix.
- `lustre/dev/simulate` (with the REAL `client.update` + page view) is the runtime-faithful pin harness — `simulate.input` drives `cache.handle` → decode2 → update → view with zero DOM; negative-control it (revert fix → red) before trusting it.
- Rebasing onto origin/develop after the sibling merged was clean (disjoint areas), but re-ran the FULL suite + lint gates afterwards — em-dash lint now scans 125 files post-#612; test files aren't in its scope.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-612-emdash-prose.md
# Field notes — righttenantry-refcheck-612-emdash-prose

Job: #612 — em-dash exemptions removed; 15 spec-verbatim strings re-composed dash-free; lint boundary hardened.

- Issue title said "16 exemptions" but the lint set and the issue's own table both had 15 — count from the CODE (`SPEC_VERBATIM_OWNERS`), not the title, and say so in the PR.
- The lint only scanned raw U+2014 bytes — a Gleam literal `"\u{2014}"` (escape form) compiled to the same char and PASSED. Escape-form detection must be escape-aware (even backslash run = real escape; `\\u{2014}` literal text is not a dash). Prove with positive AND escaped-backslash negative controls.
- Widening `SERVER_INCLUDE` surfaces latent violations in files that were never scanned (log-only helper strings in `document_upload.gleam`); re-word the log strings dash-free rather than leave a scope claim that's false — and watch the Python docstring: writing `\u{2014}` inside it is a SyntaxError, use a raw string.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-613-615.md
# righttenantry-refcheck-613-615

- 2026-08-14: toast.gleam's header comment ("fixed top-right") was stale since birth — the code was always `bottom-4 right-4`. Trust the class string, not the module comment, when reasoning about toast position.
- 2026-08-14: Lustre houdini-escapes apostrophes in serialized attributes (`&#39;`) — pin `title=`/`aria-*` assertions with the escaped form; a bare `'` assertion fails while the DOM is correct.
- 2026-08-14: evidence screenshots must be captured INSIDE the element's lifetime window and pixel-verified before shipping — the first corner-case shot was taken after the 0.8–5.8s toast window and depicted nothing (caught by a reviewer, recaptured).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-621-reminder-hint.md
# righttenantry-refcheck-621-reminder-hint

- The reference_checks bug-hunt scenario suite lives on `origin/rt-refcheck-bughunt2`, NOT develop — copy it in from there for verification runs (untracked, don't commit; matches #616/#618 precedent). The verification-rerun sandbox is still alive: server `rt-refcheck-verification-rerun` on :4100, fixture DB container `rt-refcheck-verification-rerun-dev-db` on 54335 — but :4101 is a stale bug-hunt2 sandbox server (old code); run your own build on a free port.
- The fixture DB has TWO seed generations (a dead one stuck at `submitted` with zero reference_calls) — the dead generation sorts FIRST in the leaderboard (all scores NULL → `created_at ASC`) and silently breaks every scenario; delete it before running.
- agent-browser evals share one global scope: `const row` in a second eval throws "already declared" — wrap every eval in an IIFE `(() => { ... })()`, and `return` at the top level is a SyntaxError (use an expression or IIFE).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-ad5-amend.md
# Field notes — righttenantry-refcheck-ad5-amend (2026-08-08)

- **A briefing can carry a typo in a load-bearing proper noun.** Gru's briefing
  gave the Alpha Sender ID as `RTenTRY`; the canon (ComReg gate doc) is `RTenantry`.
  I committed `RTenTRY` before Gru caught it — a name/identifier supplied by the
  briefing should be grepped against the canon doc BEFORE the first commit (the
  same "briefing's stated value can be wrong" trap as the model-tier / mechanism
  gotchas, now extending to proper nouns). Fix cost a force-push amend; cheap here
  only because no PR was open yet.
- **Edge-case-hunter on a doc amendment must re-check HEADINGS/siblings of the
  named target, not just the named lines.** The briefing named AD-5 body + the
  deps row; the AD-5 *heading* still said "launch dependency" while the corrected
  body said "central dependency, not just launch polish" — a silent internal
  contradiction. The heading was part of AD-5 and the escalation was mandated,
  so fixing it was in-scope precision, not re-litigation.
- **Amending a sender type can break a sibling channel that the briefing fenced
  as out-of-scope.** Making the IE SMS sender a (non-replyable) Alpha Sender ID
  means the inbound STOP-by-SMS-reply webhook (AD-6/Q3) can't receive replies.
  Briefing said webhooks/objection-flow "unchanged" — so I did NOT redesign it,
  but surfaced it as a flagged consequence in the PR + escalation rather than
  leave the doc silently inconsistent. The right move when an in-scope change
  has a load-bearing out-of-scope consequence: flag + escalate, don't silently
  expand scope and don't silently leave the gap.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-ad6-stoplink-amend.md
# Field notes — righttenantry-refcheck-ad6-stoplink-amend

- Architecture-doc amendment only (single .md). "Note downstream implications, don't rewrite the stories" meant: leave epics/UX/privacy STOP-reply text in place + flag EVERY superseded location grep-confirmed in an Amendments-register "downstream implications" list. A hunter caught my first list was non-exhaustive AND mis-attributed UX sections (I guessed "§7.4/§8.x"; the real SMS-STOP labels were in §4.2/§6.6/§9). Lesson: when indexing downstream supersession, grep the actual docs for line+section, don't infer from memory.
- State-mutating GET links are a real bug for capability-token routes reached via SMS/email: link scanners + preview fetchers (iMessage, Android Messages, anti-malware) GET every URL. For a sticky/non-recoverable terminal (objected), spec GET-renders-confirm + POST-objects, never GET-mutates. One-tap unsubscribe lore does NOT apply when the consequence is non-recoverable.
- terminal_reason is the `failed`-row field ONLY (§4.6: only the `failed` mapping row carries it); objected/unreachable/etc. never have one. A hunter "you dropped the objected terminal_reason slug" finding was a false positive — verify the mechanism/column-scope against the §4.6 mapping before crediting schema-slug findings.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-bughunt2.md
# Field notes shard — righttenantry-refcheck-bughunt2 (2026-08-15)

- The reference-form `data-current` marker NEVER advances on desktop (the reference_form.js `showOnly` stepper is mobile-only) — id-scope continues to `[data-question="<id>"]` and verify via the autosave toast/draft; also `a_tenancy_from` (YYYY-MM) is required even when the ongoing checkbox is set.
- Toasts render `role="status"` + `data-testid="toast-message"`, NOT `[role=alert]` (the bug-hunt skill doc is stale on this) — poll the data-testid; and the panel's `has_next_reminder` cadence hint ignores `taken_over` (filed #621) — gate any "next step" copy on the taken-over flag.
- The RC3.5 reference-check sweep never runs in the sandbox (Cloud Scheduler in prod) — fire `POST /api/v1/internal/reference-checks` with INTERNAL_SECRET to tick it; the take-over/start actions re-arm rows (`next_attempt_at=now()`) so one manual tick sends everything due.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-local-test.md
# Field notes shard — righttenantry-refcheck-local-test (2026-08-14)

- Referee form renders ALL question forms stacked in the DOM (one visible): unscoped `[data-testid=reference-continue]` clicks silently re-submit the FIRST (identity) form forever — scope every click/fill to `[data-question][data-current="true"]`, and treat "page didn't advance" as a selector bug before a server bug.
- Refcheck + apply POSTs are timing-gated (floor 500ms/2s, stale-cap): sleep ≥2-3s AFTER the page renders BEFORE submitting; a rejected submission leaves the page's `_form_loaded_at` stale, so reload fresh instead of retrying.
- Local RT sandbox: :4000 may be sibling-owned (run :4100 via a gitignored `server/.env` copy, blanking Resend/Twilio/AI); `seed-refcheck-fixture.py` must resolve applications by the submit's own unique email — "latest application" queries race parallel jobs; the global sweep claims ALL due rows, so `--no-sweep` fixtures get swept mid-test by sibling runs.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc1-1-grapheme-fix.md
# Field notes — righttenantry-refcheck-rc1-1-grapheme-fix

- Gleam `string.slice` counts GRAPHEMES while Postgres `length()` counts CODEPOINTS — codepoint-bounded slicing (`to_utf_codepoints |> list.take |> from_utf_codepoints`) is the only cut that guarantees a DB CHECK `length() <= N` holds for adversarial multi-codepoint headers (ZWJ emoji: 1 grapheme = 7 codepoints).
- Test-DB port 54321 is contended across sibling worktrees — spin your own `postgres:16-alpine` container on a free port and pass `TEST_DATABASE_URL=postgresql://test:test@localhost:<port>/righttenantry_test` to `gleam test -- --tag integration` (Makefile hardcodes 54321).
- Reverting a fix for a negative control via python replace is easy to get wrong when the call has an inline arg (`slice_codepoint_bounded(value, 512)` vs piped `|> slice_codepoint_bounded(64)`) — grep the file after the revert; the UA path survived my first revert and silently kept the fix.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc1-1.md
# Field notes: righttenantry-refcheck-rc1-1

- Squirrel regen needs the LOCAL test DB (`DATABASE_URL=postgresql://test:test@localhost:<port>/righttenantry_test gleam run -m squirrel` from `server/`) — `run_squirrel.sh` points at staging, which doesn't have unmerged migrations; and every regen re-emits a whitespace-only change to `server/src/ai/sql.gleam` (`}///` doc-comment join) — revert that file after each run.
- Test-DB port 54321 is contended across worktrees: run your own container (`docker run -d --name rt-<job>-test-db -p 5432X:5432 postgres:16-alpine`) and pass `TEST_DB_PORT` to `scripts/reset-test-db.sh` + `TEST_DATABASE_URL` to `gleam test -- --tag integration` (sibling rc2-1 used 54322, I used 54323).
- Extending `shared/application.Application` ripples into full-literal fixtures in `shared/test/shared_test.gleam`, `client/test/client_test.gleam`, `client/test/components/`, and two server row fixtures (`application_detail_handler_test`, `ai/audit_report_test`) — grep `application.Application(` and `GetApplicationDetailRow(` before claiming done.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc1-2.md
# Field notes — righttenantry-refcheck-rc1-2 (2026-08-01)

- Lustre SSR renders attributes SORTED BY NAME with empty-valued ones bare (`checked`, `required`) — never assert attribute order from the view source, and beware verbatim copy colliding with assertion substrings (the §5.3 footer's "references are checked" ate my `checked` no-default assertion; assert `checked data-testid="..."` instead).
- The SSR apply form carries `novalidate` on BOTH the GET (form_view.gleam) and error re-render (form_pages.gleam) — native browser validation NEVER fires there; server-side re-render is the only validation path. Reviewers (both hunters, independently) hallucinated native-blocking findings from the `required` attributes; verify mechanism claims against the form element before crediting them.
- Making a form field mandatory server-side breaks every bug-hunt scenario that submits the form — including the label-invariants classification sets (they grep `[required]` in the DOM). When your story adds the UI for a mandatory field, update all 5 scenario files (landing/apply-form, landing/apply-form-label-invariants, workflows/apply-form-soak [browser fill AND fetch paths], workflows/seed-archetype-applicants [16 form_data blocks], workflows/seed-applicants [prep-protocol comment]) in the same PR.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc2-1.md
# Field notes: righttenantry-refcheck-rc2-1

- Squirrel types ALL cast expressions non-`Option` (even `CASE WHEN x IS NULL THEN NULL ...`) and can't codegen `timestamptz` results at all — nullable non-text columns must be `COALESCE(x::text, '')` with `NULLIF($n,'')` on writes, or you ship decode-failures/''-in-index bugs (house `ai/sql.gleam` has the latent instance).
- `make test-db-up` port 54321 can be occupied by a sibling minion's container — run your own `postgres:16-alpine` on 54322 + `TEST_DB_PORT=54322 scripts/reset-test-db.sh`, and point `DATABASE_URL` there for squirrel (never staging).
- Integration `truncate_all` in `server/test/integration/test_db.gleam` is a fixed table list — any new table without a FK to a truncated parent must be added or tests leak rows across runs.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc2-2.md
# righttenantry-refcheck-rc2-2 — field notes

- 2026-08-08 (refcheck-rc2-2): adding an `application_status` value touches a WIDE exhaustive-match surface — 6+ compile-forced cases across shared/server/client (encode/from_string/decoder, parse_status, both pills, stepper.rank, leaderboard status_rank, comparison CTAs) PLUS default-armed matches needing per-component judgment (is_non_terminal differs by context: viewed is non-terminal for comparison-selection but deliberately terminal-for-sweep; next_step_strip; sweep_nudge). Grep `case` on the type in all 3 packages, then reason about each default arm.
- 2026-08-08 (refcheck-rc2-2): there are TWO application-status pills that had DRIFTED — shared `status_pill.gleam` (leaderboard/comparison) vs `application_detail.view_status_pill` (detail header). The detail pill + stepper already followed the brand-doc "Application Status Pills" table; the shared one didn't (used `score-strong` which == teal #2D8A7E). The brand doc is the canonical house-semantic-set source — verify against it, not either component. `tailwind.config.js` confirmed score-strong===teal.
- 2026-08-08 (refcheck-rc2-2): Squirrel regen on a pure enum `ADD VALUE` produced the legit new variant in `application/sql.gleam` PLUS unrelated churn: a `pog.array` reformatting in the same file AND the usual whitespace churn in `ai/sql.gleam`. `gleam format` reverted the pog.array hunk to canonical (formatter is the arbiter, not squirrel's output); `git checkout` reverted `ai/sql.gleam`. Final `application/sql.gleam` diff was exactly the one variant + encoder arm.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc2-3.md
# righttenantry-refcheck-rc2-3 — field notes

- 2026-08-08 (rc2-3): pgo rejects a text param bound to a boolean column via
  `$n::boolean` (`UnexpectedArgumentType("bool", "<<\"false\">>")`) — inline the
  boolean literal into the test-seed SQL string instead (or pass a real bool);
  text→enum casts (`$n::application_status`) work fine, text→bool does not.
- 2026-08-08 (rc2-3): Gleam case-exhaustiveness bites on `pog.Returned` list
  patterns — `Ok(pog.Returned(_, [row]))` + `Ok(pog.Returned(_, []))` is NOT
  exhaustive (compiler wants the theoretical 2+-row case); use an `Ok(_) ->`
  catch-all for the "0 rows / conflict / unexpected multi-row" arm on INSERT...
  RETURNING and single-row guarded UPDATE guards. Same trap in three places.
- 2026-08-08 (rc2-3): the briefing's "Migration: ALTER TYPE reference_call_status
  ADD VALUE 'skipped'" was STALE — rc2-1 already added it; `audit_log.event_type`
  is TEXT so new event wire-strings need no migration either. Net migration count
  for the story: zero. (Another instance of "verify the briefing's stated current
  state on disk before acting" — the epics A-register + rc2-1 spec were the truth.)

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-1.md
# Field-note shard — righttenantry-refcheck-rc3-1 (RC3.1 SMS client + Twilio Lookup)

- gleam `uri.percent_encode` leaves `+` UNENCODED (it's a valid URI sub-delimiter) — but `+` means space in an `application/x-www-form-urlencoded` body, so an E.164 `To=+353...` would arrive at Twilio as ` 353...` with a leading space. Re-encode `+`→`%2B` after `percent_encode` for ANY phone-number-bearing form body or URL path segment (also needed for the Twilio Lookup path, whose curl docs use `%2B`). `payment/stripe_client.form_encode` has the same latent gap (its values rarely carry a leading `+`).
- `request.get_header(req, key)` returns `Result(String, Nil)` in gleam_http 4.x, NOT `Option(String)` — easy to misremember when writing test assertions (compiler catches it, but it costs a round-trip if you assume Option).
- Test-DB port 54321 was held by a sibling worktree (`draft-grace-period-test-db-1`); ran integration on an isolated container at :54324 — `scripts/reset-test-db.sh` honors `TEST_DB_PORT=<port>` and the integration run takes `TEST_DATABASE_URL=postgresql://test:test@localhost:<port>/righttenantry_test gleam test -- --tag integration`. Clean teardown with `docker stop`/`rm`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-2.md
# Field notes — righttenantry-refcheck-rc3-2 (2026-08-09)

- The 2026-08-08 stop-link amendment does NOT rewrite the docs in place everywhere: UX §6.3/§6.4 still read "Reply STOP" and the epics AC still says it too — the architecture amendments register (top of file) is the authoritative supersedure list. Always read the register FIRST on refcheck stories; briefing compressions of it ("the Art 14 notice + the opt-out both point to the stop-link") need resolving against §9.1, which keeps TWO distinct links (notice URL + stop-link).
- gleam format + the atomic-multi-edit trap compound: `gleam format` reflowed split string literals between my write and a follow-up edit, so a stale oldText silently failed to match — grep the CURRENT line-break positions before re-issuing edits to formatted Gleam files (second sighting after dream-2026-08-03).
- `gh pr create --body "$(cat <<'EOF' ...)"` breaks on apostrophe-heavy bodies ("unexpected EOF") — write the body to a file and use `--body-file` (and verify any claimed counts in it with grep before pushing: I had to `gh pr edit` a wrong test count).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-3.md
# Field notes — righttenantry-refcheck-rc3-3

- `make format` between edit batches REFLOWS long string constants — an `edit` oldText captured pre-format silently mismatches post-format (bit me twice; grep the current shape before re-firing, the dream-2026-08-03 atomicity note's sibling).
- Lustre SSR: `attribute.for` (not `for_`), bare `attribute("k","v")` needs `import lustre/attribute.{attribute}` (module+value namespaces share the name), and local type constructors shadow same-named imports in case patterns (my `TokenState.Completed` shadowed `reference_call.Completed` — qualify in patterns).
- jsonb `||` merge never deletes keys — conditional answers (x only when y) must be explicitly nulled on the non-y branch or stale values survive re-saves; and a remint-then-send flow needs a rollback path when every send fails, or the success page lies while the old link is already dead.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-4.md
# righttenantry-refcheck-rc3-4 (field-note shard)

- **2026-08-10 (refcheck-rc3-4 Perkins r2 B2):** a progressive-enhancement
  field rendered in the HTML is INERT unless the JS that populates it
  actually runs on that page. reference_form.js `initBrowser` bailed on the
  review page (different testid), and `onSubmit` bound only `.ref-question`
  forms — so the review submit's `_focus_seconds` shipped dead (always 0).
  The integration test MASKED it via `simulate.form_body` (which bypasses the
  browser). Lesson: any client-populated hidden field needs (a) the JS wiring
  on the SPECIFIC page that renders it, AND (b) a Node/browser-path test that
  drives the wiring seam — never rely on a server-side `simulate.form_body`
  test alone to prove a client-side population. The fix was a narrow
  page-specific seam (`initReviewSubmit`), not relaxing the form-page gate.
- **2026-08-10 (refcheck-rc3-4 Perkins r1):** the canonical double-scheme
  CTA trap — `origin_from_domain` returns scheme-full (`https://domain`),
  but `email_client.build_entity_url` prepends `https://` itself. Passing
  the scheme-full origin to ANY notification CTA builder yields
  `https://https://domain/...` — a dead link in every email. Pass the RAW
  `origin_domain` to `build_entity_url`; reserve `origin_from_domain` for
  message-body links (the invite base_url). The `notify_application_scored`
  precedent (ai_client.gleam) does it right; mirror it.
- **2026-08-10 (refcheck-rc3-4 Perkins r1):** a hidden field rendered on ONE
  form (per-question `_focus_seconds`) but NOT the form that actually POSTs
  the terminal action (the review submit) silently zeroes a downstream
  signal. The integration test masked it by injecting the field manually.
  When a field flows submit→result, render it on EVERY form that POSTs that
  action + assert the end-to-end flow (don't just inject in the test).
- **2026-08-10 (refcheck-rc3-4):** the briefing's "register EACH route in ALL three registries" rests on a per-arm mental model; the registries are **prefix-matched** `"reference", ..` (one arm covers any depth). The router is the only per-arm registry. Verify the briefing's mechanism claims against disk before acting — the work was router arms + coverage tests, NOT registry edits (which would be dead code). Same lesson as the canonical "verify briefing premises" note, now with a concrete routing instance.
- **2026-08-10 (refcheck-rc3-4):** Postgres JSONB re-serialises stored JSON with a **space after colons** (`"key": value`) and may reorder keys — substring assertions on `result::text` (e.g. `"schema_version":"refcall-v1"`) FAIL. Use `result->>'field'` extraction (`test_db.query_text`) for JSONB field assertions; reserve raw-text substring matches for non-JSONB columns.
- **2026-08-10 (refcheck-rc3-4):** Squirrel generates its OWN `ReferenceCallStatus` type inside `reference_checks/sql.gleam` (mirroring the PG enum), SEPARATE from `shared.reference_call.ReferenceCallStatus`. Status args to the sql functions must be `sql.Refused`/`sql.Objected`/etc. (the trigger module is the precedent — `sql.Skipped`). Don't pass the shared variants; it's a type mismatch that compiles to "Expected sql.ReferenceCallStatus".
- **2026-08-10 (refcheck-rc3-4):** `decode.null` does NOT exist in gleam/dynamic/decode (this Gleam version). To detect a JSON null in a Dynamic, use `decode.dict(...)` (succeeds on an object, fails on null) or the `decode.optional(string)` trick. `has_draft_key` for completeness must count object-valued answers (tenancy_period, rent_amount) as answered, not just strings.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-5.md
# righttenantry-refcheck-rc3-5 — field notes

- **Worktree-path gotcha (4th sighting):** I used the briefing's `repo_root` (`/Users/moses/code/RightTenantry`, the MAIN checkout) as my edit root + `cd`'d there in every bash call, so ALL my early edits landed in the main checkout, not my worktree. Silas synced it. FIX: your edit root is your WORKTREE cwd (`pwd` = `~/.herdr/worktrees/RightTenantry/<slug>`); never `cd /Users/moses/code/<repo>`; use worktree-relative paths for read/write/edit. The briefing's `repo_root` is for reference/bootstrap, NOT edits.
- **Squirrel + `reference_call_outcome`:** the `reference_call_*` status + outcome PG enums SHARE constructor names (ManualRecorded/Unreachable/FormCompleted/...). Gleam forbids duplicate constructors across types in one module, so HEAD never had a `ReferenceCallOutcome` Gleam type — outcomes are passed as STRING + `NULLIF($n,'')::reference_call_outcome` cast in SQL. A bare `$n::reference_call_outcome` in a NEW query makes Squirrel emit the conflicting type → "Duplicate definition". Always use the NULLIF-string-cast convention for outcome params.
- **`unitest.tag` needs a STRING LITERAL:** the integration-test skip is STATIC ANALYSIS, not runtime — `use <- unitest.tag(tag)` (a const) does NOT skip under `gleam test` (runs + fails on no DB); `use <- unitest.tag("integration")` (literal) does. My 12 sweep tests ran+failed until I swapped the const for the literal.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-6.md
# righttenantry-refcheck-rc3-6 (RC3.6 verified webhooks) — field notes

- The briefing's headline AC can be STALE on mechanism: briefing said "inbound STOP→objected" on the Twilio webhook, but the 2026-08-08 architecture amendment (in the amendments register) + rc3-4's shipped stop-link route + Twilio's one-way alphanumeric sender proved it dead. ALWAYS grep the architecture amendments register + the deployed code (router.gleam) for the amended behaviour before trusting a briefing AC; surfaced + reconciled via a lavish clarify (Q1).
- New POST routes at a NEW top-level path family (`/webhooks/*`, not `/api/v1/webhooks/*` per arch §7.2 + sms_client's fixed status_callback_path) need their OWN registry arms — the existing `["api","v1","webhooks",..]` CSRF prefix did NOT cover them (a missing arm 403s). Verify each registry (is_public_path / CSRF / redact_token_route) against disk per route family; don't assume the existing arm covers a new prefix. The "register in all three registries" briefing line is per-arm, but which arms apply is per-route-family.
- Twilio status callback path is a LIVE CONTRACT fixed in `sms_client.gleam` (`status_callback_path = "/webhooks/twilio-sms"`) — the X-Twilio-Signature signs that EXACT URL (base + path), so the verifier must reconstruct it from `TWILIO_STATUS_CALLBACK_BASE_URL` + the const, not from the request's own Host/URL (proxy host mismatch fails verification, never silently passes).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc3-7.md
# Field-note shard — righttenantry-refcheck-rc3-7 (RC3.7 Fraud-Signals)

- **Postgres `jsonb::text` adds a space after `:`** (`"line_type": "unknown"`) — substring-contains checks on STORED fraud_signals fail; parse + decode the field instead. (Unit tests pass because they check gleam's compact `json.to_string` output directly; integration tests read Postgres jsonb and need decode-based asserts.)
- **Squirrel types a `$n::jsonb` cast PARAM as `Json`** (auto-serializes via `pog.text(json.to_string(arg))`) — pass the `json.Json` directly, NOT `json.to_string(signals)`. Counterintuitive vs a SQL docstring that says "pass the JSON text"; complete_reference_call/stamp_creation both take Json.
- **Squirrel regen churns `ai/sql.gleam` + `application/sql.gleam`** (blank-line + pog.array reflow) on EVERY run — revert both to HEAD after each regen when your SQL lives in `reference_checks/` (not your change).
- **A creation-time stamp must be scoped to the rows THIS call created, never the whole application (Perkins r1 B1).** `handle_start` / the viewed trigger RE-FIRE on demand (idempotent ON CONFLICT inserts), so a wholesale re-stamp wipes a submitted sibling's `form_session`. Thread the created row ids out of the tx; stamp only those; skip when the list is empty. Generalises: any "stamp on creation" that writes a denormalised column must respect terminal rows — submission is terminal, so the submitted snapshot is never recomputed.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc4-1.md
- 2026-08-12 (righttenantry-refcheck-rc4-1): gleam_json 3.1.0 / stdlib 0.70 has NO decode.any / json.from_dynamic — JSONB payload fields can't be rebuilt as objects in shared codecs; the honest pattern is carry-as-text (ai_analysis.category_scores precedent) and strip at the SQL read boundary with jsonb `#-` + jsonb_typeof guards. #- THROWS on scalar/array intermediates — always guard the shape or one corrupt row 500s the whole read.
- 2026-08-12 (righttenantry-refcheck-rc4-1): §4.2 strip-assertions must check the ESCAPED wire form — a result document riding as a JSON string field ships its inner keys backslash-escaped (`\"referee_ip\"`), so a `string.contains(body, "\"referee_ip\"")` assertion is vacuously green while the IP is on the wire. Assert both forms; prove with a neutralize-the-strip → red negative control.
- 2026-08-12 (righttenantry-refcheck-rc4-1): an edge-case-hunter self-review before the PR paid off 4 real fixes (vacuous strip guard, hooks-vs-wire status divergence on unknown enum values, non-forward-tolerant decoder, corrupt-result read failure) — the briefing's em-dash "CI ban" was again false on disk (keep the §8.1 canon copy verbatim). Also: gleam's decode.optional_field expects Decoder(t) where t = the DEFAULT's type — Option fields need decode.optional(inner) as the field decoder.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc4-2.md
# righttenantry-refcheck-rc4-2 — field notes

- gleam 1.15.1 parser REJECTS `++ [list-literal]` ("operator has no value on its right side") — use `list.append`/spread; the repo never uses `++ [`.
- `decode.dict` fails on JSON arrays (they're `List(Dynamic)`); `list.last` returns Result; `list.filter_map` wants Result; the `type X` import prefix is per-item (bare name = constructor value only).
- `list.all([])` is vacuously True — emptiness must be checked BEFORE the all-terminal branch (the pre-trigger sub-line bug).
- The RC4.1 §8.1 payload had no form-open marker or completion timestamp — RC4.2's "Form opened"/"Reference received" states needed additive `form_opened_at`/`submitted_at` keys (expand-only, optional_field back-compat).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc4-3.md
# Field notes — righttenantry-refcheck-rc4-3

- Lustre/Gleam traps: an EMPTY-STRING attribute value is a PRESENT boolean attribute (`attribute("disabled", "")` ships permanently-disabled buttons — omit via `list.append(attrs, case busy {True -> [attribute("disabled","true")] False -> []})`); a case-clause body starting with `let` is a parse error unless braced; no function calls in clause guards; no list `..` spread in this Gleam version (use `list.append`); `decode.optional_field` is the `use`-callback 4-arg form.
- Idempotent-insert pattern for slot/unique-index endpoints: a CTE (`INSERT ... ON CONFLICT DO NOTHING RETURNING ... UNION ALL SELECT existing WHERE NOT EXISTS(inserted)`) with a `how` column returns the existing successor — double-submits get 200, no duplicate audit. For retry/cadence loops, RESET the attempt counter (and capability token) on re-queue — a step-dispatched sweep reads attempt_count, and a corrected row at count 1 dead-ends in the co-nudge step forever.
- When a one-cycle correction/retry loop exists, gate post-loop failures on the CORRECTION instant (a `corrected_at` column; compare the failing send's `at`): stale/redelivered pre-correction events must stand down, never fabricate a fraud signal. And extending a detail payload breaks existing strip-test NEGATIVE controls (rc4-1 asserted referee contact absent; RC4.3 legitimately added it — move the marker to a still-internal token).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-rc4-4.md
# Field notes — righttenantry-refcheck-rc4-4 (2026-08-13)

- RC4.4's "four codec variants" briefing count was the RC2.1 set; `reference_awaiting_correction` joined in RC3.6 and IS emitted — completeness demanded all FIVE variants or the dropdown stays decode-broken. Always grep the DB enum migrations, not the briefing, for the emitted set.
- The old client-side timeline sort (raw `at` string compare) silently mis-ordered same-day events: PG `::text` uses a space separator, the sweep stamps RFC3339 `T` — space (0x20) < 'T' (0x54) sorts the evening before the morning. Server-built timeline must normalise space→T before sorting (or the rc4-2 W4 "chronological" fix quietly regresses).
- Post-correction cadence restart: correct_reference_call resets attempt_count to 0, so batch index alone mislabels the re-invite as "Reminder N" — segment send batches by corrected_at boundary.
- Squirrel regen churns `application/sql.gleam` formatting hunks unrelated to new columns (reverted one) + `ai/sql.gleam` whitespace (revert whole file); verify each hunk before keeping.
- Integration suite on own container (:54328) — the sibling worktrees own 54321/54326/54327/54332-34; `TEST_DATABASE_URL=postgresql://test:test@localhost:54328/righttenantry_test gleam test -- --tag integration` after `TEST_DB_PORT=54328 bash scripts/reset-test-db.sh`.
- Gleam guards can't call functions — nested `case string.compare(...) { Gt if ... -> ... }` with `import gleam/order.{Gt}`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-v1-architecture.md
# Field notes: righttenantry-refcheck-v1-architecture

_2026-07-29 · recorded by Gru from the minion's badge-out report (seed
entry — shards are normally minion-written)._

- lavish HTML builds: piping large markdown through `marked` via
  subprocess stdout truncated the artifact at ~85KB (pipe-buffer issue).
  Build via a file write, then verify byte length + tail-section presence
  before serving. Found only after the user reviewed a page truncated
  around §7.3 — verify BEFORE serving.
- `npx -y lavish-axi <file>` opens the user's browser itself; there is no
  URL to discover or relay.
- Keep one foreground poll per lavish session; if it dies, re-run —
  queued feedback is never lost. Never `lavish-axi stop` (shared server,
  port 4387 — kills every minion's session).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-v1-epics.md
# Field notes: righttenantry-refcheck-v1-epics (2026-07-31)

- The refcheck v1 architecture and UX docs (both "final" 2026-07-29) contradict
  each other in 4+ places (correction mechanics, autosave/partial, link TTL,
  notification types) — when two same-day design docs both claim to be binding,
  diff them BEFORE writing stories; the UX §15 decisions record is the
  tiebreaker only where it explicitly names the decision.
- Working lavish HTML recipe for large markdown: `npx -y marked --gfm -o
  .lavish/_body.html <file>.md` (writes to file, no pipe truncation), then a
  python file-write wrapper for the brand CSS/hero — 88KB artifact, tail
  verified, no truncation (confirms the 2026-07-29 curated trap).
- User redirected the trigger mid-job (shortlist → new `viewed` status): check
  the actual status enum + stepper component in the repo before spec'ing a
  trigger story (`client/src/components/status_stepper.gleam`,
  `shared/src/shared/application.gleam` — enum value needs DB + shared +
  client + PATCH validation updates).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-v1-sprint-plan.md
# Field notes: righttenantry-refcheck-v1-sprint-plan

- 2026-07-31: `lavish-axi poll` DOM snapshot exposed a Mermaid render failure my own eyes never saw ("Syntax error in text" — likely HTML entities like `&amp;` inside quoted labels). Read the dom_snapshot on poll return, not just the prompts; it's the only self-check of what the user actually saw.
- 2026-07-31: Feature-line sprint trackers sit beside the canonical `sprint-status.yaml` as `sprint-status-<slug>.yaml` in `_bmad-output/implementation-artifacts/` — bmad-sprint-planning's fixed `status_file` path needs overriding per the briefing, and story keys keep the epic prefix (`rc1-1-...`) to avoid canonical collisions.
- 2026-07-31: `_bmad/scripts/memlog.py` is per-worktree shared and append-only — it may already carry another job's entries; never prune them, just append with `--workspace . --text`.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-verification-rerun.md
# Field notes shard — righttenantry-refcheck-verification-rerun (2026-08-14)

- RT apply-form POST is MULTIPART (415 on urlencoded) and mandates PDF uploads for
  `landlord_ref_primary` + `employer_ref_primary` (reportlab on the machine); application
  status updates are **PATCH** `/api/v1/vacancies/:id/applications/:id/status`, not POST — the
  fastest way to arm the reference_checks scenarios is: submit via the real form (unique
  email per app, `_form_loaded_at` 5s back) → PATCH-walk to `viewed` (mints landlord_ref +
  employer_ref) → SQL per-scenario call states.
- agent-browser `click @ref` silently no-ops on Lustre refcheck buttons (row expand, Correct
  details, Substitute, stepper tabs) — the native `.click()` eval fallback is mandatory; the
  referee form's `reference-continue` clicks must be scoped to `[data-question="<id>"]` (the
  stacked-forms trap), and the success export toast needs a
  `navigator.clipboard.writeText` stub in headless (no clipboard permission).
- Sandbox: `.env` → gitignored `server/.env` copy (PORT=4100, DATABASE_URL→local Docker
  Postgres on a free port, Resend/Twilio/Stripe/AI blanked, Supabase GoTrue kept for login);
  `make build-client` reads the ROOT .env, not server/.env, so build first or the PostHog
  perl pass warns.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-security-audit.md
# righttenantry-security-audit — field notes

- 2026-08-18: mega-minion pane reclamation race is real — TWO lens dispatches lost to external pane closure (mid-hunt, no file written); before a third re-dispatch, check `herdr pane get` + consider finishing small residual scopes in-pane (parent completed authn+ssr solo faster than another spawn+reclaim cycle).
- 2026-08-18: the provider-cap pause protocol earns its keep — preserve artifacts + write resume-notes.md BEFORE parking; the resume rode glm-5.3's return cleanly with the 5 finished lens files as head-start.
- 2026-08-18: lavish triage pattern for big audits — per-finding native radio forms with `data-lavish-question=<id>` + one Queue button each + ONE batch question for the Low block; user triaged 47 findings in a single session, dom_snapshot verified the render, zero stranded prompts.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-self-employed-copy-fix.md
# Field notes — righttenantry-self-employed-copy-fix (2026-08-04)

- The apply-form stepper's Continue is `type=button` + JS validation; `agent-browser click` advanced silently and my re-snapshot read stale state — drive it via `eval` + read `Step N of 8` from `document.body.innerText`, and dump `[required]` controls per visible `.form-section` to find blockers (date inputs need value+input/change events).
- Dev server against a private Docker DB needs NO symlink surgery: tracked `.env.test` (placeholder secrets only) + `ENV=test gleam run`; temporarily repoint its DATABASE_URL port and `git checkout .env.test` after — but it is NOT gitignored, so never let real secrets land in it.
- Copy fix that touches a user-visible phrase: grep `_bmad-output/creative-campaign/*copy-sheet*` too — production copy sheets carry verbatim sentences and silently reintroduce the old copy downstream (edge-case hunter caught it; both hunters otherwise verified clean on a 12-file label-only diff).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantry-self-employed-sweep.md
# Field notes — righttenantry-self-employed-sweep (2026-08-04)

- **Rebasing copy PRs across a sibling merge:** when your change deliberately duplicates a merged PR's edit verbatim (audit-PDF label, error_summary label), git auto-merges it — zero friction. The conflicts land only where the texts genuinely differ (the sentence lines + their test pins). Watch for the *other* PR's negative assertions: #573's `string.contains("employer, if you") |> should.be_false` silently contradicts the new scoped text ("employer, if you're working") — negative pins from a superseded ruling must be re-pointed, not just conflict-resolved.
- **agent-browser `click` doesn't drive this app's stepper buttons** (agent-native click reported Done, nothing advanced) — `eval`-dispatched `el.click()` works. Radios/labels also need explicit `checked=true` + dispatched `change`/`input` events; date inputs take `value='YYYY-MM-DD'` + events.
- **Server-side evidence runs:** `make dev` parity needs `server/.env` (main checkout has it as a `../.env` symlink; worktrees get neither — bootstrap only links root-level env files). Copy, don't symlink, when repointing `DATABASE_URL` to a local Docker DB; run your own Postgres container on a free port (54321/54322 were both taken by sibling jobs).

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantryagents-boundary-gate-slot-clear.md
# boundary-gate-slot-clear — field notes

- The #172 residual's trigger window is REACHABLE, not just theoretical: ADK skips the `output_key` write on empty chunks / schema-validation-fail / tool-call-only responses (already documented at `agents/anonymizer.py:313`, `pii_reviewer.py:248`, `test_state_init_inline_cleanup.py`), while the judge's `after_agent_callback` (which writes the verdict stamp via `_stamp_review_verdict`) ALWAYS fires. So a clean attempt can leave the prior dirty review in the slot while stamping clean — finalize reads non-None dirty → fail-close. The per-attempt `pop` is necessary hygiene, not paranoia.
- The briefing named the WRONG state key for the final gate (`STATE_FINAL_OUTPUT` — that's the audited v4 payload the scrubber mutates). The final gate's review slot is `STATE_FINAL_COMPLIANCE_REVIEW` (what `finalize_final_gate` reads). Popping `STATE_FINAL_OUTPUT` would empty the reviewer's `{final_output}` placeholder. Verify against the code, don't blindly follow the briefing's key names.
- To reach attempt-1 in the gate-loop regression test, BOTH `scrub_*` (must return touched) AND `_run_compliance_repair` (must return True) must succeed on attempt 0 — there's no other continue path. The boundary scrub reads `ctx.state` (stale snapshot), so the `_DivergentCtx` test harness needed an optional `stale_seed` to carry a verifier output; the final scrub reads the live `final_output` dict directly.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantryagents-boundary-gate-state-fix.md
# righttenantryagents-boundary-gate-state-fix — field notes

- **ADK `ctx.state` is a per-node SNAPSHOT, not live.** A child agent's `output_key` write (via `ctx.run_node`) lands on the live `ctx.session.state` but is absent from the node's `ctx.state` snapshot → `ctx.state.get(child_key)` returns `None` right after `run_node`. The RightTenantry convention (documented at `agent.py:263`/:396) is raw `ctx.session.state` for ALL cross-node gate state — the compliance review reads violated it. When editing ADK Workflow gates: read child output via `ctx.session.state`, never `ctx.state`.
- **The InMemory recorder harness can't reproduce this.** `tests/unit/test_workflow_pipeline.py`'s `_Recorder` stubs share the live dict, so `ctx.state` sees child writes and the bug is invisible there. To regression-guard a state-view fix, build a divergent fake ctx (stale `State({}, {})` snapshot + live `session.state` dict) and assert the gate reads through `ctx.session.state` — see `tests/unit/test_gate_state_marshalling.py`.
- **The judge's own `after_agent_callback` IS a reliable independent witness.** It reads `callback_context.state` (the judge's delta, which has the output_key) — so telemetry (`compliance.review_completed`) correctly records `passed=true` even when the pipeline node's `ctx.state` reads `None`. That asymmetry is the clean signal for the blast-radius query: a `boundary_gate.exhausted{review_parseable=False, violations=0}` co-occurring with `compliance.review_completed{passed:true}` is the exact bug fingerprint.

## SOURCE /Users/moses/code/_bmad-output/field-notes/righttenantryagents-model-flash.md
# righttenantryagents-model-flash — field notes

- Briefing forensics can be STALE relative to merged work — this job's
  briefing said `config.py` default was still `gemini-3.5-flash`, but PR
  #164 had already moved `config.py` + the default-tier Terraform vars to
  `gemini-3.6-flash`. The real delta was only the 5 Pro-tier vars. Always
  `grep` disk for the current model strings before trusting a briefing's
  "current state" (ground-truth-first); also sweep `deployment/README.md`
  + `.env.example` — both carried the old tier and would've shipped stale.
- Isolated single-agent judge checks are fast BUT get confounded when the
  agent carries a `web_search` (Brave) tool and the dev env has no
  `BRAVE_API_KEY`: `consistency_checker` on Flash retried the failing
  tool in a slow loop while Pro tried once and moved on — a dev-env
  artifact, not a model-quality signal (prod has Brave). For judge
  sanity-checks, confirm Brave is present or pick a tool-free path.
- Don't attempt inline full-pipeline eval head-to-heads: each evalset case
  ran >10 min (anonymizer slow-mode + multi-agent) and the repo's own
  strategy routes full evals to **staging deploy** for that reason. The
  non-streaming Runner path works; the `StreamingMode.SSE` path hits an
  `httpx` `readline(max_line_length=...)` version mismatch in this venv —
  use default `run_config` (non-streaming).

## SOURCE /Users/moses/code/_bmad-output/field-notes/wire-aesthetics.md
# wire-aesthetics — field notes (badge-out)

- 2026-08-19 (wire-aesthetics): the ROUTED-look first pass was a big T2 golden churn, but the LAVISH GATE verdict ("ship pure straight, routing OFF, anchors OFF") turned the re-bless requirement into its opposite — the shipped flags-off render must be BYTE-IDENTICAL to pre-7.5, and the harness run on committed goldens is the proof. Structure every variant as a legacy-inline branch + a path-walk branch from the start (a shared path-walk that "should be equivalent" drifted 1 pixel in estate_surge — found only because the flags-off harness run must be fully green).
- 2026-08-19 (wire-aesthetics): Odin multi-return `X, t, ok := seg_cross(...)` with `X` unused compiles clean (tuple destructuring allows unused) — don't chase it as an error; use `_` only where the codebase's own style does.
- 2026-08-19 (wire-aesthetics): `direction16`/anchor math needs a LOCAL copy of the CIRCLE16 constant to index at runtime ("Cannot index a constant") — the same rule as PULSE16; also `#partial switch` for enums with unhandled cases, `inc[:]` to pass a dynamic as a slice, and `pc: i32` vs `pc := 4` (int) mismatch when assigning from an i32 struct field. `delete()` on a string LITERAL (not a clone) aborts — clone first.
