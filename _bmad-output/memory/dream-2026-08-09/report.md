# Dream report — 2026-08-09

Material: **19 field-note shards**, **3 journal files** (Gru 08-08: 1 entry;
Silas 08-08: 56 entries; Silas 08-07: ~31 post-marker of 38), **~400 ledger
events across 35 jobs** (14 `ledger show`s) — since **2026-08-07T11:43:30Z**.
Sheep: sheep-shards (w1T:pJA), sheep-journals (w1T:pJB), sheep-ledger
(w1T:pJC) — findings in sibling files; all badged out and closed before this
report (verified via `herdr agent list`).

Store copies with all **auto** edits applied, diff-ready:
`_bmad-output/memory/dream-2026-08-09/store/` (diff vs live: field-notes
+55 lines — 5 new entries + 7 amendments; AGENTS.md +64 lines — 3 new
gotchas + 8 amendments; zero deletions, zero contradictions found).

## Proposal summary

| # | Title | Target | Class | Sightings |
|---|---|---|---|---|
| P1 | `gh pr create`: always `--body-file` | field-notes (Tooling) | auto ✓ | 4 jobs, 2 repos |
| P2 | briefing ground-truth: claim-type checklist | field-notes (amend) | auto ✓ | 5 jobs |
| P3 | atomic-edit: 3 new preventions | field-notes (amend) | auto ✓ | 4 jobs |
| P4 | canon-doc amendment craft (grep radius / house style / surface calls) | field-notes (Conventions) | auto ✓ | 4+2+3 |
| P5 | negative-control: prove the test BITES | field-notes (Conventions) | auto ✓ | 2 jobs, 2 days (promoted watch) |
| P6 | Perkins late blockers are process gates — run CI gates locally | field-notes (Recurring) | auto ✓ | 3 jobs, 2 days |
| P7 | lavish ground truth = `state.json sessions.<id>.chat[]` | field-notes (amend) | auto ✓ | 2 confirmations |
| P8 | Godot captures: movie mode for sequences; compositor freeze | field-notes (amend) | auto ✓ | 2 jobs |
| P9 | Squirrel regen churns BOTH sql.gleam files | field-notes (amend) | auto ✓ | 2 jobs |
| P10 | "no worktree" briefings still dispatch one — pane cwd is truth | field-notes (amend) | auto ✓ | 2 jobs |
| P11 | pane-chat approval (2nd sighting of provenance entry) | field-notes (amend) | auto ✓ | 2 jobs |
| P12 | provider-qualified labels generalized + defaultProvider | field-notes (amend glm §) | auto ✓ | kimi saga + glm |
| P13 | 5th provider-incident class: transient blocked/cache-miss needs NOTHING | AGENTS.md (amend) | auto ✓ | 4 panes |
| P14 | Model dispatch & correction ops (`/model` mid-session; walls; labels) | AGENTS.md (new gotcha) | auto ✓ | odin saga + doc-verified |
| P15 | boot-transition watcher noise on fresh dispatches | AGENTS.md (amend) | auto ✓ | 4 sightings |
| P16 | Perkins self-close NOT uniform + sweep-list drift + token-mint `$?` | AGENTS.md (amend) | auto ✓ | counter-sightings |
| P17 | moot-on-merge: FYI verdicts need a named routing target | AGENTS.md (amend) | auto ✓ | 2 sightings |
| P18 | `ledger json` drops done rows + round-row naming | AGENTS.md (amend) | auto ✓ | verified live |
| P19 | `herdr tab create` also has no `--json` | AGENTS.md (amend) | auto ✓ | 1 + sibling gotcha |
| P20 | pane-id gotcha: 6th slip post-doc + job ids + tab_id race | AGENTS.md (amend) | auto ✓ | 3 new slips |
| P21 | orchestrator-root jobs ALWAYS worktree + occupied-tree base sync | AGENTS.md (amend) | auto ✓ | 2 + 4 sightings |
| P22 | user mid-flight reversals kill work, spawn canon cascades | AGENTS.md (new gotcha) | auto ✓ | 4 sightings, 2 days |
| P23 | cross-job impact = flag, never act across the boundary | AGENTS.md (new gotcha) | auto ✓ | 2 sightings, 2 days |

**23 proposals, all auto.** Plus 4 user-ack items (UA1–UA4), 1 immediate ops
flag (UA5), and a watch list.

---

## Proposals (all applied to the store copies)

### P1 — `gh pr create --body "$(heredoc)"` keeps breaking → always `--body-file`
- Target: `docs/minion-field-notes.md` (Tooling traps) · Class: **auto** (applied)
- Change: new entry — three fresh failure mechanisms (backticks
  command-substituted, trailing `| tail` breaks quoting, apostrophe-heavy
  bodies EOF early → a wrong test count shipped and needed `gh pr edit`).
  Always `--body-file <file>`; grep-verify claimed counts before pushing.
- Evidence: orchestrator-docs-ua1-ua2 08-07, orchestrator-perkins-ops-codify
  08-07, righttenantry-refcheck-rc3-2 08-09 + the dream-2026-08-07 watch
  item (packet-plumber-setup 08-06). **Promotes last dream's watch item.**
- Reasoning: 4 sightings, 2 repos, 3 distinct shell mechanisms — the idiom
  itself is the trap; `--body-file` is robust to all of it.

### P2 — Briefing ground-truth: the claim types keep diversifying
- Target: `docs/minion-field-notes.md` (amend ground-truth-first) · Class: **auto** (applied)
- Change: 2026-08-09 addendum — checklist of newly-bitten claim types:
  proper nouns vs canon (`RTenTRY` committed before Gru caught it),
  migration state (already-done "skipped" ADD VALUE), CI-guard EXISTENCE
  (banned "CI-guarded" em-dashes, no such guard), PR/sha citations (#169
  had no r2), MCP tool inventory (no `capture_screenshot`). Grep any
  briefing-supplied proper noun against canon BEFORE the first commit.
- Evidence: refcheck-ad5-amend 08-08, refcheck-rc2-3 08-08,
  packet-plumber-narrative-messaging 08-07, perkins-ops-codify 08-07,
  prototype-build 08-08.
- Reasoning: the 08-07 addendum established "briefings can be stale/wrong";
  this window shows the failure MODES diversifying — a concrete claim-type
  checklist is the actionable form.

### P3 — Atomic-multi-edit: three new preventions
- Target: `docs/minion-field-notes.md` (amend 2026-08-03 atomicity entry) · Class: **auto** (applied)
- Change: addendum — check each oldText's TARGET FILE in cross-file
  batches; after a sed/python bulk rename grep the renamed tokens (new
  stale texts appear); for fragile multi-site blocks a short python
  `.replace()`-with-asserts script beats the edit tool.
- Evidence: port-limits-canon 08-08, odin-architecture 08-08,
  sprint-plan-v1 08-09, refcheck-rc3-2 08-09 (formatter reflow, 2nd
  sighting).
- Reasoning: 4 sightings each adding a distinct, non-obvious prevention.
  (Bob himself was bitten this pass: one bad oldText silently rejected a
  7-edit batch — the lesson is load-bearing.)

### P4 — Canon-doc amendment craft
- Target: `docs/minion-field-notes.md` (Conventions) · Class: **auto** (applied)
- Change: new entry, three parts — (a) grep-bound the FULL blast radius
  (every occurrence, headings/siblings of the named target, downstream
  `FORGE #<n>` citations) — guessed section numbers are always wrong;
  (b) MATCH the doc's house style + established amendment format;
  (c) surface judgment calls + out-of-scope consequences in the PR's
  Decisions & rationale — never silently drop/expand/leave-the-gap.
- Evidence: art-direction-amend, forge6-desktop-first-amend,
  port-limits-canon, refcheck-ad5/-ad6 amends (all 08-08, 2 repos;
  4+2+3 sightings for the three parts).
- Reasoning: this window was amendment-heavy (canon cascades per P22);
  the failures were uniform — non-exhaustive sweeps and silent judgment
  calls.

### P5 — Negative control: prove the test/guard actually BITES
- Target: `docs/minion-field-notes.md` (Conventions) · Class: **auto** (applied)
- Change: new entry — flip one assertion (or inject the violation),
  confirm exactly the expected failure at your path, revert. Terse
  runners (gleeunit dots) and no-op-via-byte-diff pass silently
  otherwise.
- Evidence: csp-posthog-allowlist 08-06 (prior watch item), 
  per-applicant-remind 08-08. **Promotes last dream's watch item** ("likely
  promote next dream" — the 2nd sighting arrived).
- Reasoning: 2 jobs, 2 days, same principle from two angles (invariant
  test + runner-output skepticism).

### P6 — Perkins late-round blockers are PROCESS gates — run CI gates locally pre-push
- Target: `docs/minion-field-notes.md` (Recurring review findings) · Class: **auto** (applied)
- Change: new entry — `gleam format --check` failures and unpinned
  headline ACs each burn a full Perkins round; run the repo's CI gates
  LOCALLY before opening/updating the PR (cross-references the
  durable-tests convention).
- Evidence: rc2-2-perkins-r2 08-08 (format gate, 4-lens agreement),
  rc2-3-perkins-r1 08-08 (headline AC zero coverage),
  per-applicant-remind-perkins-r1 08-07 (W4 test-gate concerns).
- Reasoning: 3 jobs, 2 days, same class — free local checks vs a burned
  review round.

### P7 — Lavish verdict ground truth = `~/.lavish-axi/state.json` → `sessions.<id>.chat[].text`
- Target: `docs/minion-field-notes.md` (amend 2026-08-03 stranded-prompts entry) · Class: **auto** (applied)
- Change: addendum — the exact lookup path, attested twice; verify BEFORE
  acting on any load-bearing verdict.
- Evidence: packet-plumber-narrative-messaging 08-07 ("read good." +
  Send&End, confirmed via state.json), packet-plumber-blender-art 08-08
  (session-end stranding re-observed).
- Reasoning: the 08-03 entry said "check state.json"; the exact path is
  now attested — removes the last ambiguity.

### P8 — Godot captures: movie mode for sequences; macOS compositor freeze
- Target: `docs/minion-field-notes.md` (amend 2026-07-31 windowed-offscreen entry) · Class: **auto** (applied)
- Change: addendum — `-32000` is outside the renderable desktop
  (`-3000,-3000` stands); offscreen windows FREEZE their compositor
  (captures repeat the first frame — diff frame hashes to detect); movie
  mode (`--write-movie --fixed-fps` + ffmpeg) for anything
  sequence/verification-grade; windowed offscreen remains right for
  one-shots.
- Evidence: prototype-build 08-08, prototype-iterate-1 08-08.
- Reasoning: refinement, not contradiction — the windowed lesson stays,
  scoped to one-shots.

### P9 — Squirrel regen churns BOTH `sql.gleam` files; `gleam format` is the arbiter
- Target: `docs/minion-field-notes.md` (amend Squirrel triple-trap) · Class: **auto** (applied)
- Change: addendum — churn hits `application/sql.gleam` AND
  `ai/sql.gleam`; revert ALL churn not yours; `gleam format` arbitrates
  (it reverted a bogus pog.array hunk).
- Evidence: per-applicant-remind 08-08, refcheck-rc2-2 08-08.
- Reasoning: the triple-trap entry's churn point named one file; both
  packages churn.

### P10 — "No worktree" briefings still dispatch a worktree — ground truth = pane cwd
- Target: `docs/minion-field-notes.md` (amend relative-paths entry) · Class: **auto** (applied)
- Change: addendum — a "work in the root, no worktree" briefing can still
  arrive as a standard worktree dispatch; `pwd` + `git branch
  --show-current` FIRST, run git/edits from the actual cwd.
- Evidence: orchestrator-docs-ua1-ua2 08-07, perkins-ops-codify 08-07
  (hit `fatal: branch already used by worktree` against the main
  checkout).
- Reasoning: 2 jobs, same day, identical mismatch; the ops-side rule is
  P21 (root jobs ALWAYS get worktrees — the briefings were wrong, the
  dispatches were right).

### P11 — Pane-chat approval: 2nd sighting of the provenance entry
- Target: `docs/minion-field-notes.md` (amend 2026-08-04 gate-drill entry) · Class: **auto** (applied)
- Change: half-line addendum — sprint-plan-v1 08-07: a lavish-gate
  APPROVED arrived via direct pane chat (not Send&End), provenance
  unambiguous, same protocol followed.
- Reasoning: keeps the evidence trail current on a load-bearing protocol.

### P12 — Provider-qualified labels generalized + defaultProvider resolution
- Target: `docs/minion-field-notes.md` (amend glm-5.2 section) · Class: **auto** (applied)
- Change: 2026-08-09 generalization — only a `provider/model` path naming
  an AUTHED provider works: bare `kimi-coding` fails (provider, not a
  model — label is `kimi-coding/k3`); `moonshotai/kimi-k3` misroutes via
  openrouter. pi's defaultProvider is now kimi-coding → UNSET-model
  dispatches resolve to kimi-coding/k3.
- Evidence: Silas journal 08-08 (the odin-architecture model saga), as a
  2nd-provider instance of the in-store glm failure shape.
- Reasoning: the glm entry was single-provider; the rule is general.

### P13 — 5th provider-incident class: transient `blocked` + cache-miss needs NOTHING
- Target: `AGENTS.md` (amend provider-incidents gotcha) · Class: **auto** (applied)
- Change: addendum — a `blocked` alert on a >5h-old minion with a "Cache
  miss after ~Xm idle -> re-billed" transcript line is transient
  cache-expiry noise; it recovers to working on its own. Classify by
  transcript + pane age BEFORE acting; distinct from errored-turn
  (`stopReason:"error"` → one `continue`).
- Evidence: Silas 08-08 — 3 panes in one batch (light-cascade,
  blender-art, prototype; ~884k tokens re-billed) + rc2-3 (PR opened 17
  min later, zero action).
- Reasoning: prevents false escalations + `continue`-spam; also explains
  sudden token cost spikes.

### P14 — Model dispatch & correction ops
- Target: `AGENTS.md` (new gotcha, Provider incidents) · Class: **auto** (applied)
- Change: new gotcha — (a) provider-qualified labels only (kimi instance;
  minion-facing glm in field-notes); (b) `/model <provider>/<model>` typed
  to a RUNNING pi switches mid-session, context preserved (observed 08-08;
  pi README: `/model` = Switch models) — kills the kill-and-relaunch
  reflex that discarded the odin deepseek draft; (c) a model wall
  shouldn't stall a dispatch — launch on the proven fallback + flag Gru
  (Gru ratified: "deepseek for docs, kimi for code after the wall");
  accept a user mid-run override; (d) defaultProvider is now kimi-coding —
  the flip side of the `PI_MODEL`-override gotcha.
- Evidence: the odin-architecture saga 08-08 (kill + resurrection + wall +
  override), doc-verified `/model`.
- Reasoning: one operational saga but four distinct durable rules, one of
  them doc-verified; the kill-reflex cost ~1h + a discarded draft this
  window.

### P15 — Boot-transition watcher noise on fresh dispatches
- Target: `AGENTS.md` (amend settle-transitions gotcha) · Class: **auto** (applied)
- Change: addendum — `gone -> idle (ledger dispatched)` fires when the
  watcher polls a new pane mid-boot; a fresh dispatch's first alert is
  usually the boot, not a problem.
- Evidence: 4 sightings named in Silas 08-08 spanning 08-06..08-08
  (agent-model-flash, per-applicant-remind, prototype-iterate-1, rc3-2).
- Reasoning: another classify-away noise class, same doctrine.

### P16 — Perkins self-close is NOT uniform + sweep-list drift + token-mint root cause
- Target: `AGENTS.md` (amend self-close gotcha) · Class: **auto** (applied)
- Change: three addenda — (a) counter-sighting: rc3-1's pane closed with
  the row left at `working` → VERIFY the row state at close-out, don't
  assume either direction; (b) the deepseek leftover drifted: 08-08 rounds
  left NO lens panes; the new residual is the lingering ROUND PANE (pHT
  swept 08-09) — sweep list = worktree / branch / round pane / lenses;
  (c) token-mint root cause diagnosed: a shell `$?` bug (rc3-2 r1);
  fallback-comment posts but APPROVED-by-comment ≠ formal approve.
- Evidence: rc3-1 08-08 note, Silas 08-08 round sweep, rc3-2 08-09.
- Reasoning: the 08-07 "10/10 norm" overgeneralized in one window; the
  sweep list and the token-mint cause are concrete.

### P17 — Moot-on-merge: FYI verdicts need a named routing target
- Target: `AGENTS.md` (amend moot-on-merge gotcha) · Class: **auto** (applied)
- Change: addendum — the doctrine's first two clean sightings worked
  ONLY because findings were explicitly routed (Odin prototype +
  foundation-audit); without a named intake FYI findings evaporate.
- Evidence: prototype-build-perkins-r1 (verdict 18 min post-merge, 3B
  incl. 2 headless-reproduced REAL bugs), model-flash N-series (tracked a
  day past merge).
- Reasoning: turns the doctrine from theory into observed practice, adding
  the routing-target requirement.

### P18 — `ledger json` drops done rows + Perkins round-row naming
- Target: `AGENTS.md` (amend lossy-table gotcha) · Class: **auto** (applied)
- Change: addendum — `ledger json` shows only NON-DONE jobs (**verified
  this pass**: 4 rows, 0 done); query the DB for done round rows. Round
  ids are `<job-id>-perkins-rN`, NOT `perkins-<job>-rN`.
- Evidence: Silas 08-08 journal + Bob's live verification 08-09.
- Reasoning: extends the lossy-view gotcha to the other direction; the
  naming rule prevents dedup-lookup misses (see the phantom id in P20).

### P19 — `herdr tab create` also has no `--json` (prints JSON anyway)
- Target: `AGENTS.md` (amend pane-move gotcha) · Class: **auto** (applied)
- Change: one-line extension.
- Evidence: Silas 08-08 11:46Z.
- Reasoning: sibling of the stored pane-move behavior; same parse-stdout
  rule.

### P20 — Pane-id gotcha: 6th slip post-documentation + job ids + tab_id race
- Target: `AGENTS.md` (amend Extensions pane-id gotcha) · Class: **auto** (applied)
- Change: addenda — a 6th slip happened AFTER the gotcha was written
  (documentation alone doesn't stop it; the variable-capture habit is the
  only fix); the rule covers JOB ids (a hand-typed phantom
  `perkins-<job>-r1` event id lives in the stream forever); new race —
  `herdr agent list` lags a beat after a new-tab move (StopIteration) →
  `herdr tab list` by label; a mangled move-output subshell caused a
  DUPLICATE worktree create — capture once, never re-parse.
- Evidence: Silas 08-08 (23:4xZ 6th slip, 20:26Z duplicate create,
  23:5xZ/00:21Z tab race) + sheep-ledger phantom-id finding 08-09.
- Reasoning: the gotcha exists but slips continue — the amendment converts
  it from documentation to habit-change instruction.

### P21 — Orchestrator-root jobs ALWAYS get a worktree + occupied-tree base sync
- Target: `AGENTS.md` (amend in-repo follow-up gotcha) · Class: **auto** (applied)
- Change: addendum — the orchestrator root is the PERMANENT exception to
  in-repo work (its tree is Gru+Silas' live home, never free); and when a
  sibling minion holds a repo's main checkout on its own branch, sync the
  base with `git fetch origin <base>:<base>` (no checkout).
- Evidence: both 08-07 UA follow-ups deviated from "no worktree" briefings
  (correctly — Silas 08-07 12:0xZ); the fetch-into-ref move was used 4×
  on packet-plumber close-outs 08-07/08 (different days).
- Reasoning: convergent evidence from both sides (minions bit, Silas
  ruled); the sync mechanics were unwritten.

### P22 — User mid-flight reversals kill in-flight work and spawn canon-cascade jobs
- Target: `AGENTS.md` (new gotcha, Dispatch & handover) · Class: **auto** (applied)
- Change: new gotcha — 4 reversals in 2 days (84s dev-auto flip killed
  pF1; LIGHT verdict → light-cascade + art-direction-amend; lavish Odin
  verdict reversed the LOCKED engine choice → odin-architecture + forge6 +
  port-limits). Rules: locked decisions are PROVISIONAL until the user
  reacts at a lavish gate; prefer in-place correction (`/model`, relayed
  redirect) over kill-and-redispatch; every direction reversal needs an
  explicitly ROUTED cascade job.
- Evidence: rc2-2 08-08, blender-art 08-08, odin-architecture 08-08,
  odin-vs-godot-lavish 08-08 (sheep-ledger P1, two sheep converged).
- Reasoning: the strongest ops cluster of the window; the
  "locks-are-provisional" reframing changes dispatch expectations.

### P23 — Cross-job impact = flag, never act across the boundary
- Target: `AGENTS.md` (new gotcha, Dispatch & handover) · Class: **auto** (applied)
- Change: new gotcha — the two-layer relay (minion flags in its PR →
  Silas surfaces → Gru relays scope → the OWNING minion applies) is how
  multi-minion canon stays consistent.
- Evidence: art-direction → prototype packet_types.json mismatch 08-07;
  blender-art A1-A7 trail → light-cascade scope expansion 08-08.
- Reasoning: 2 sightings, 2 days, both clean loops; unwritten until now.

---

## User-ack items (NOT applied — structural/policy)

- **UA1 — Lavish-default rule: refine the root AGENTS.md review-loop
  sentence.** Gru ruled 08-07: a minion DEFAULTS to direct PR for
  targeted edits; lavish gates big visual/creative deliverables; briefings
  should say "lavish not needed, PR directly" when that's intended. The
  current root text ("DOCS deliverables … get a lavish in-browser review
  before the PR opens") caused a ~7h ambiguity park
  (perkins-ops-codify). Proposed refinement: add the targeted-edit
  exemption + the briefing phrasing rule. (Evidence: perkins-ops-codify
  park 08-07; narrative-messaging correct gate 08-07;
  art-direction-amend correct direct 08-08.) *Root AGENTS.md beyond
  gotcha appends → user-ack.*
- **UA2 — Lens-guards as standard Perkins-briefing content (playbook
  edit).** Name the deliberate decisions as DON'T-FLAG in the round
  briefing (playbook 'Silas dispatch sequence' step 4 / standing orders).
  Evidence: ~6 rounds across #586/#590/#591/#594 held their guards
  (08-07..08-08); Perkins spent findings on real gaps instead of
  relitigating intent. (dream-2026-08-03 declined to codify this in
  MEMORY as over-codification; the playbook is the right home, and the
  practice is now validated at scale.)
- **UA3 — Fresh-minion-per-story is the standing sprint pattern (playbook
  edit).** Gru journal 08-08 records the user ruling: sprint execution =
  Gru manual dispatch, one fresh minion per story (the per-story field
  notes feed the learning/memory loop); bmad-dev-auto is reserved for
  mechanical work / fun-test prototypes. Not currently in the playbook;
  any future "just loop dev-auto" instinct contradicts the ruling.
- **UA4 (note) — Perkins token-mint shell `$?` bug wants a fix task.**
  Root cause diagnosed (P16); fallback-comment posts but ≠ formal
  approve. A small minion job on the Perkins tooling closes it.

## Immediate ops flag (not memory)

- **UA5 — packet-plumber-foundation-audit: dropped thread.** Recalled
  08-08 15:18 (dispatched off origin/main, which had NO game code —
  prototype stranded on a local branch). The re-dispatch precondition
  (PR #11 merged 08-08 17:58) is MET, and the prototype-build FYI verdict
  (08-09 07:16) explicitly routes findings to the foundation-audit — but
  NO re-dispatch row exists post-marker. Silas/Gru: re-dispatch or
  explicitly abandon.

## Prior-dream closures (verified this pass)

- dream-2026-08-07 **UA1** (gotcha-section growth): DONE — gotchas are now
  themed (orchestrator-docs-ua1-ua2, PR #4 merged 08-07).
- dream-2026-08-07 **UA2** (playbook node_modules symlink): DONE —
  verified at Dispatch step 4 (lines 408-420).
- dream-2026-08-07 **UA3** (Perkins-ops codification): PARTIAL — 3
  patterns codified (orchestrator-perkins-ops-codify, PR #5); the
  lens-guard remainder is this pass's UA2.
- **Gru journal gap**: CLOSED — `2026-08-03-08-07-backfill.md` exists +
  Gru journaled 08-08.

## Watch items (anecdotes — tracked, not proposed)

**New this window (single sightings):**
- New dead-agent class: the PANE VANISHES (no detected agent, plain
  session tail — not idle, not errored) → relaunch in a new pane +
  sqlite re-point the ledger row (pF1, rc2-2 08-08; recovery confirmed).
  Note: the sqlite re-point is already codified for Perkins round rows in
  the playbook — minion panes lack the doc.
- Creative-iteration loop: `continue` on the minion's COMMITTED,
  user-approved default is safe (keeps render loops hot) — 2 sightings,
  same night (blender-art); Silas-judgement territory.
- Verify the audit/review TARGET exists on the base branch BEFORE
  dispatch (foundation-audit recall 08-08); HOLD-before-launch made the
  recall zero-cost (dispatch = worktree+move+ledger, launch LAST).
- Don't flip ops process on an ambiguous user remark — confirm first
  (Silas MISREAD self-correction 08-07: user reflecting on THEIR OWN
  process ≠ a directive).
- Enum/status additions: grep the WHOLE tree for string→enum maps +
  match arms (rc2-2 r1 B1: a third decode copy in
  application_list_handler; two status pills had DRIFTED — the brand doc
  is the arbiter) — 1 job, 2 writers.
- BlenderMCP: NEVER `bpy.ops.wm.read_factory_settings()` — reloads the
  addon, kills the :9876 listener (user must toggle); clear scenes via
  `bpy.data.objects.remove` loop + purge. Blender 5.2: compositor =
  node-GROUP API, Eevee has no bloom (Compositor Glare), Standard view
  transform keeps canon hex. Will bite any future Blender-MCP job.
- Ledger row resurrection (done → dispatched on the SAME row) blurs
  forensics (odin-architecture kill+revive) — a fresh row per re-dispatch
  keeps rounds auditable.
- Perkins DOUBLE-POSTED two identical APPROVED reviews (same sha/content,
  per-applicant-remind 08-07) — benign, likely a retry; uninvestigated.
- Toolchain pre-flight for first-of-kind stacks: Silas `brew install odin
  raylib` BEFORE the minion builds (08-08).
- Harness-supplied config masks production bootstrap gaps
  (prototype-iterate-1: explicit balance masked `PacketFlow.new()`'s
  missing knob).
- Link scanners/preview fetchers GET every URL — terminal actions need
  GET-renders-confirm + POST-mutates, never GET-mutates (ad6-stoplink).
- Amendment registers supersede WITHOUT rewriting in place — read the
  register FIRST, resolve briefing compressions against source sections
  (rc3-2).
- Lavish mid-form freeform QUESTION → answer in the next `--agent-reply`
  AND rebuild the form with the new options (odin-architecture).
- Terse lavish verdicts: paraphrase back BEFORE a sweeping change — a
  misread one-liner cost a flip across 8 locations + full revert
  (sprint-plan-v1).
- `marked --gfm` emits NO heading ids — inject slugged ids before a TOC
  (sprint-plan-v1); bash tool cwd resets to repo root EVERY call — `cd`
  in the same command.
- gleam `uri.percent_encode` leaves `+` unencoded (means space in form
  bodies) → re-encode `+`→`%2B` for E.164 (rc3-1; latent same bug in
  stripe_client.form_encode).
- Dream auto-apply guard (applies to THIS close-out): before copying
  store → live, grep the store for concurrent live edits — a blind copy
  can clobber a same-day Silas gotcha (verified-in-practice 08-07; Bob
  diffed store==live at pass start today, Silas re-verifies at apply).
- Godot/game-feel/RT-domain one-offs (rolling-window SLA, snapshot
  re-entrancy, pg casting, test-DB :54324 3rd-sighting, etc.) retained in
  the sheep-shards shard.

**Promoted this window:** `gh --body-file` (→P1); negative-control test
probe (→P5).

**Previous watch items checked — NO 2nd sighting (still watching):**
clarify-halt stand-Gru-down (3 sightings 08-06, demoted for growth
control); Perkins lens cascade on parent close; co-touch merge rebase
heads-up (adjacent: the conflict sensor was validated end-to-end once on
PR #593 08-08); `gh repo delete` scope; diverged-main close-out;
sed-tamper `checkout --`; stale `HERDR_*` env; linked-worktree
rebase-merge test; lavish mid-review cache (dom_snapshot); wrong-repo
reframe; `rg` masks `gemini-*`; Perkins lenses spawn at ~/code;
`custom_message`==0 ≠ unarmed; `gh pr diff` 406; Supabase
security-definer RLS.

## Pruned / rejected candidates (with why)

- **"Perkins arcs are shortening (3→2→1)"** (sheep-ledger P3) — real
  trend evidence (codified ops bedding in), but it prescribes no memory
  change; recorded here as narrative only.
- **"Sensor stale echoes continue"** (sheep-ledger P5) — already in
  memory (2026-08-01/02 echo gotcha); 5 confirmations this window, zero
  double actions — durability confirmed, no edit.
- **Token-mint fallback as a standalone** — merged into P16 (the existing
  gotcha already covered fallback; only the root cause was new).
- **No outright contradictions found** — first pass where every "stale"
  candidate was a refinement, not an error. The store is aging well.

*End of dream report — 2026-08-09. Store copies diff-ready at
`_bmad-output/memory/dream-2026-08-09/store/`. Silas close-out: apply the
23 auto edits (diff the store copies against live FIRST — see the
auto-apply-guard watch item), escalate UA1–UA5 to Gru, write the
`last-dream` marker, `ledger set dream-2026-08-09 done`, commit
`dream 2026-08-09: <one-liner>`.*
