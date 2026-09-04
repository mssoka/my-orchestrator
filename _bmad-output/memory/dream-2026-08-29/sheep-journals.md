# Sheep shard — journals (dream-2026-08-29)

Read (fully unless noted):
- gru-journal/2026-08-25-pi-restoration-handover.md (253 lines)
- gru-journal/2026-08-27-evening.md (141 lines)
- gru-journal/2026-08-29.md (114 lines)
- silas-journal/2026-08-27.md (55 lines)
- silas-journal/2026-08-28.md (137 lines)
- silas-journal/2026-08-29.md (5 lines)
- silas-journal/2026-08-26.md — TAIL ONLY, last 40 lines of 101 (backfill caveat)

Store greps: AGENTS.md (moot / close-out drift / connection-class / external
input / evidence-job / interactive-sessions / vision / model policy),
playbook Model policy + VISION ROUTING + briefing `_template.md`,
minion-field-notes.md (heredoc class), dream-2026-08-27 report (watch items).

## Candidates

### C1 — Moot-sweeps and round close-outs miss LIVE panes: the lens wave outlives the main, and the main outlives the sweep
- Example: silas 2026-08-28 ~19:3xZ — "w85:t1K held SEVEN orphaned lens panes
  - from #106's r2 round (moot-swept mid-flight when the user merged; I closed
  the round row + worktree but missed its live lens panes)… LESSON for the
  moot-sweep doctrine: a moot round sweep must close LENS PANES TOO, not just
  row+worktree - the lens wave outlives the main (as today proved twice) and
  outlives sloppy sweeps." AND silas 2026-08-28 ~00:5xZ(+1d) — "DEBRIS p3V
  (#106 r1 main - round swept but pane survived my close-out), DEBRIS p5E
  (#107 r5 main - same miss)… LESSON: round close-outs must close the MAIN
  pane too (row + worktree + pane) - two sweeps today missed their own
  mains."
- Novel? NOVEL as stated. Adjacent: close-out-drift gotcha (debris sweeps at
  merge close-outs) + the Perkins self-close "Sweep list: worktree / branch /
  round pane / lenses" — but the MOOT-sweep path (not merge close-out) is
  where the 7 lenses leaked, and the two main-pane misses show the checklist
  fails in practice even where doctrine exists. Best shape: one addendum on
  the "moot at scale" text (moot sweep = row + worktree + MAIN + ALL lens
  panes, cwd-exact) + a pointer from the close-out-drift gotcha.
- Target: AGENTS.md

### C2 — A blocker CARRIED 2+ rounds = a pipeline defect until proven otherwise; review BYTES not claims
- Example: silas 2026-08-28 ~18:1xZ — "carried-blocker pattern flagged (2
  rounds same B2/B3 = pipeline defect, not luck)"; ~18:45Z r5 briefing — "B2
  carried 3 rounds - blob-forensics the 11 named goldens FIRST, bytes not
  claims; if they still diverge, the rlsw pipeline blesses the wrong renders
  and that is the finding." Paid off: r5 APPROVED — "B2 finally answered (the
  11 goldens byte-match the merged tree - the rlsw pipeline fix was real)".
  Root-cause flavor: "two blessing machines with R/B-swapped conventions" and
  "the 'one-machine settle' was the minion machine agreeing with itself"
  (r4). The-box arc: r1 2B → r3 4B → r4 3B (2 carried) → r5 APPROVED.
- Novel? NOVEL — nothing in the store names the carried-blocker escalation
  (claim-check → byte-forensics after the 2nd carry).
- Target: AGENTS.md (Perkins round-ops gotcha)

### C3 — Flash-tier Perkins rounds: connection deaths ~1x/round mid-wave + blind-lens output-cap truncation are EXPECTED and cheap
- Example: silas 2026-08-28 ~14:2xZ — "4th connection-class round death today
  - all salvaged via durable artifacts. Pattern note for the next docs pass:
  flash long-context lens waves die ~1x/round mid-wave; one continue + disk
  state = full recovery every time." Blind-lens output-cap flavor ×3: #105 r1
  "blind lens truncated twice on flash long-context, diff covered by 6
  lenses" (silas 08-27 ~17:25Z); #107 r1 "blind output-cap failed 2x,
  disclosed; degraded guard not forced" (silas 08-28 ~08:5xZ). Day total: 4-5
  round deaths across #106/#107, zero lens work lost.
- Novel? PARTIALLY covered — dream-2026-08-27 addendum (d) covers
  connection-class waves killing mains (one continue + re-drive; degraded
  disclosure). NEW facets: the QUANTIFIED flash-tier expectation (~1x/round —
  budget for it, don't alarm) and the blind-lens output-cap failure mode
  (distinct from connection class; disclose 6-lens coverage, never force the
  guard).
- Target: AGENTS.md (addendum to the connection-class / round-ops doctrine)

### C4 — Self-inflicted external input: placeholder `pane run` commands in dispatch chains type into LIVE panes
- Example: silas 2026-08-28 ~00:25Z — "SLIP OWNED: my launch chain carried a
  stray `pane run w85:p3R 'placeholder...'` before the real handover —
  literal junk landed as user input in the LIVE A1 minion pane (the 08-26
  external-input class, self-inflicted). Corrected in place with an explicit
  disregard note… LESSON: never leave placeholder pane-run commands in
  dispatch chains — one bad target in a && chain types into a live agent."
- Novel? NOVEL facet — AGENTS.md's external-input entry (08-27 (c)) covers
  HUMAN keystrokes; this is the automation-self-inflicted variant (Silas' own
  && chain).
- Target: AGENTS.md (one-line addendum on the external-input class)

### C5 — Evidence/read-only job worktree rule: the main-checkout default yields when the checkout is HELD or the job must build at 2+ commits
- Example: silas 2026-08-27 ~19:45Z — "Worktree call: DETACHED at 03dd6f8
  (briefing default was main checkout, but it is HELD by mechanics-quinn —
  the audit must build at two commits and a HEAD move under quinn is the
  catastrophic class; BEFORE sha 088cf00 via minion-owned scratch worktree,
  briefed in handover)."
- Novel? NOVEL refinement — the 08-27 look-lane addendum says "main checkout,
  NO branch/worktree = parallel-safe" with no exception clause. Exception
  conditions: (a) main checkout held by another minion, (b) the job builds at
  multiple commits (a HEAD move under a live minion = catastrophic).
- Target: AGENTS.md (addendum to the evidence-job doctrine line)

### C6 — Interactive-pane pi deaths are invisible; salvage the composed content from the session jsonl BEFORE relaunch
- Example: silas 2026-08-27 ~19:55Z — "mechanics-quinn's pi died ~18:36Z
  right after its OPENING TURN COMPLETED (stopReason=stop, full Dr. Quinn
  diagnosis composed) — nobody watches minion panes, 44min dead; recovered:
  extracted the composed opening to
  _bmad-output/briefs/…-opening-recovered.md, relaunched glm-5.3-flash
  +thinking max same pane w85:p3P, chained handover VERIFIED (quinn
  re-presented + idle-awaiting user ruling)."
- Novel? NOVEL facet — the interactive-sessions doctrine (08-27)
  pre-classifies watcher alerts on interactive rows as noise, which makes a
  DEATH on an idle-awaiting pane doubly invisible (the census/startup sweep
  is the only detector). The salvage-composed-content-first recovery step is
  new and generalizes to any pane that died post-completion pre-delivery.
- Target: AGENTS.md (addendum to the interactive design sessions doctrine)

### C7 — Census/sweep safety: bare-shell no-agent panes are USER SPACE — classify and spare, never sweep
- Example: silas 2026-08-27 ~20:05Z — "w8D:p1/w8E:p1 classified USER
  TERMINALS (bare zsh, untracked, one user-focused) — NOT Perkins debris
  despite Gru's flag; left untouched." AND silas 2026-08-28 ~00:5xZ(+1d) —
  "p63 (~/Downloads, no agent) left alone = user space."
- Novel? NOVEL as a stated rule (2 sightings this window); kin to the 08-17
  id-proximity/label burns (never close by proximity) but this is the
  positive classification rule that protects user terminals during
  debris/cull sweeps.
- Target: AGENTS.md (close-out drift / census doctrine addendum)

### C8 — Live-tree dedup under open sessions: SWAP-NOW (stale aside + symlink to canonical), REMOVE-LATER at lane close; a deferred trigger keyed on a never-closing pane is a broken trigger
- Example: silas 2026-08-28 ~00:47Z(+1d) — "packet-plumber/.agents/skills
  (stale Aug-5) moved to .agents/skills.stale-aug5; symlink to
  /Users/moses/code/.agents/skills (canonical) in its place - Sally's live
  session keeps resolving through the link, zero breakage (verified)… The
  deferred-trigger conflict (Sally pane never closes by design) is dissolved
  by the swap." Procedure from the phase-1 sweep (same day ~21:5xZ): capture
  the only-in-repo list to ledger notes FIRST, verify zero live panes, then
  rm; sessions resolve via ~/.pi/agent/skills symlinks (spot-checked).
- Novel? NOVEL. Single exercise, but the swap trick (inert now, remove later)
  + the broken-trigger diagnosis generalize beyond skills dirs.
- Target: AGENTS.md (ops) — or watch item if judged too single-sighting.

### C9 — Gru: ground pending-claims and ambiguous user acks against live pane/lavish state before reporting or acting
- Example: gru 2026-08-27-evening (night wrap) — "LESSON for Gru: check
  pane/lavish state before telling the user what is pending — both 'pending'
  prompts were already answered (stale-board x2 one night)." AND silas
  2026-08-28 ~09:55Z + ~14:2xZ — a bare user "go" was GROUNDED in Gru's
  session against live state both times (Sally already held the pill
  question) → interpreted as continue-acknowledgment, no new dispatch, one
  confirm queued.
- Novel? NOVEL (Gru-facing). Durable-routing and verify-delivery gotchas are
  adjacent, but this is about the ACCURACY of Gru's board as presented to
  the user: "pending" is a claim about pane state — verify the pane first.
- Target: AGENTS.md (Gru gotchas)

### C10 — A user ruling can supersede an APPROVED verdict: merge stays HELD, the loop re-arms on ruling-defined acceptance
- Example: silas 2026-08-28 ~08:3xZ — "USER RULING reverses A1-as-implemented
  (mid-flight, healthy amend-and-relay)… #106 merge HELD (no keystroke on
  df14785; the r1 APPROVED is superseded)… NOTED pattern: r1's APPROVED on
  the width implementation is now moot-by-ruling - the loop does its job; the
  width re-bless inventory (33 PNGs) is throwaway, the pulse rework
  re-blesses again." Cadence note ~09:0xZ: "4 user rulings across 2 PRs, all
  mid-flight, all amend-and-relay - zero re-dispatches."
- Novel? FACET of the existing reversal doctrine (locked decisions
  provisional until the lavish gate; mid-flight AMENDMENTS are the healthy
  path). The new bit: the reversal can land AFTER Perkins APPROVED — the
  verdict blessed the spec, the user rules the spec; prior re-bless
  inventories become throwaway without complaint.
- Target: AGENTS.md (one-line addendum to the user-reversal gotcha)

### C11 — Journal/notes write integrity: heredoc+fallback chains eat notes silently — verify the write landed
- Example: silas 2026-08-29 ~21:35Z — "the 08:25Z r3-recovery note had been
  lost to a bash heredoc/fallback subtlety (first cat created the typo file
  2028-08-28.md empty and exited 0, so the fallback never fired); note
  restored verbatim to 2026-08-28.md with a BACKFILL header, typo file
  removed." Caught by pre-dream hygiene, ~13h later.
- Novel? SIBLING of field-notes 549 (capture rc UN-PIPED; byte-check
  generated artifacts) — that entry covers rewrites/compares, not
  append-with-fallback chains where the FIRST command fails creating a
  typo'd path but exits 0. Borderline: small candidate or watch item.
- Target: AGENTS.md (ops hygiene one-liner) or field-notes 549 addendum.

## Stale/duplicate live entries this supersedes

1. **Playbook Model policy, final paragraph** — "The provider default is
   `settings.json` `defaultProvider` = `deepseek` (→ v4-flash), so
   UNSET-model dispatches land on flash — briefings ALWAYS name
   `deepseek/deepseek-v4-flash` explicitly … Silas is pinned to
   deepseek/deepseek-v4-flash by `.pi/extensions/silas.ts`." SUPERSEDED by
   the 08-27 ops flip (silas 08-27 ~12:45Z: "ALL NEW dispatches ride
   glm-5.3-flash… Config synced by Gru (bf09e39: silas.ts auto-set…)"). The
   same section's own "Execution — glm-5.3-flash (ops tier since 2026-08-27)"
   paragraph contradicts it.
2. **Playbook VISION ROUTING section** — "glm-4.6v is the standing vision
   model" + the blind-model list "(glm-5.3, deepseek flash — no image
   input)" lacks the glm-5.3-flash native-multimodal case. SUPERSEDED by the
   08-27 ruling (silas 08-27 ~13:0xZ: flash reads images INLINE; KYLE ops pin
   = glm-5.3-flash, 4.6v demoted to fallback). AGENTS.md + vision-read
   SKILL.md carry the amendment (3085281); the playbook section does not.
3. **Briefing template `_template.md` (Model policy + Standing orders
   lines)** — "close every one when done ('badge out')" / "close any panes
   you spawn" — still NO own-pane exclusion. dream-2026-08-27 watch item #1
   ("minions NEVER close their own pane — promote on 2nd sighting") had no
   2nd failure this window, but the template fix is still pending and the
   clause only rides ad hoc in hand-authored briefs (this sheep's own brief
   carries it). Flag as PENDING, not failed.
4. **managed-repos.txt comment block** (gru 08-29, Stale) — mentions
   "youtube (isaacharrisholt/youtube)" which no longer exists under ~/code.
   Minor repo-hygiene stale line.

## Anecdotes (single-sighting — watch items)

- **r1 disconfirming the briefed hypothesis on evidence = the loop working**
  (#108, silas 08-28 ~21:4xZ): briefed "2->4 array grow double-free"
  (verify-not-assume); real chain = shadow_clone value-copy aliased the LIVE
  heap allocator in slice headers → destroy freed live buffers →
  topology.gen re-predict double-freed. Mutation gate machine-proven
  RED→GREEN.
- **URGENT fun-test-unblock flow** (#108): .ips in hand → merged in ~3.5h;
  URGENT framing in the brief ("a wrong APPROVE re-crashes the playtest
  mid-session"); CI-invisible class — zero golden demos run box-on; playtest
  = the only box-on × telegraph-lead surface (PP project fact).
- **User-ordered per-job model exception** (silas 08-28 ~21:4xZ):
  lang-safety-research dispatched on glm-5.3 PRO for the minion AND every
  spawn, explicitly not flash — the model-pin doctrine carries it, just
  noting the exception path exists by user order.
- **Deferred trigger keyed on a SIM EVENT** (gru 08-27-evening): shape-vocab
  "defer to first era-4 third-class wave (auto re-trigger)" — a new trigger
  substrate beyond merge/pane/probe.
- **Watchman rode a full herdr SERVER outage** (silas 08-27 ~19:55Z):
  DEATH silas 19:17:37Z + DEATH gru 19:18:59Z, both relaunched with handovers
  verified — the layer's biggest live test since the 08-21 kill test.
- **k3 weekly-cap return practice** (silas 08-29): DOUBLE-PROBED OK twice
  before routing Bob back to k3 ("the flip guard") — consistent with the
  re-probe doctrine; noting the double-probe-before-routing-back habit.
- **Picker-wedge recovery** (silas 08-27 ~13:0xZ): Esc+redo recovers a
  relay/dialog race in-pane.
- **youtube-channel lane facts** (gru 08-29): Gru-direct repo (intentionally
  NOT in managed-repos); pi MCP via pi-mcp-adapter + user-global
  ~/.config/mcp/mcp.json; higgsfield bridge accepts the Blender plugin's
  auth.json token as plain Bearer; Blender 5.2 craft (slotted actions,
  volume-needs-transparent-surface, scale = half-extents, headless EEVEE
  works); Seedance retention doctrine (3-6s cuts on the drop, A/B/C cameras,
  previz OBJ as reference slot, prompts carry LOOK only — no camera
  language). Gru-journal craft for that lane; not orchestration memory.
