# Playbook annex — history, incidents & full procedures

Relocated from `docs/orchestration-playbook.md` on 2026-08-21 by the
playbook diet (orchestrator-playbook-diet, PR docs-only). The playbook
core states CURRENT rules; this annex holds what moved: incident
narratives, case-by-case supersede histories, war stories, sensor
failure modes, and full procedures that are too long for the core.
Nothing was deleted — every doctrine keyword greps to a hit in core or
this annex (the diet's acceptance test). When the core says "see
playbook-annex.md", this file is the operative detail.

## What moved where

| Core section | Annex section |
|---|---|
| Memory system → Dreaming | 'Memory system — the dream pass (full procedure)' |
| Tracking — review sensor | 'Tracking — review-sensor failure modes' |
| Tracking — sensors | 'Tracking — sensor noise classes (classify before acting)' |
| Tracking — PR watcher | 'Tracking — the no-PR completion gap' |
| Perkins — standing orders | 'Perkins — the lens run (full standing-orders paste-block)' |
| Perkins — round-budget ops | 'Perkins — round-budget evidence & incidents' |
| Perkins — when fires | 'Perkins — the #585 no-op round' |
| Dispatch — chain discipline | 'Dispatch — handover incidents (chain, wait, delivery)' |
| Dispatch — bootstrap | 'Dispatch — bootstrap war stories' |
| Concurrency | 'Concurrency — serialize, valve & throttle history' |
| Model policy | 'Model policy — provider incident history' |
| HTML artifact review (lavish) | 'Lavish — the review flow (mechanics) & incidents' |
| Skills availability | 'Skills availability — self-containment history' |

## Memory system — the dream pass (full procedure)

(Relocated verbatim from the playbook's 'Dreaming' section. Core keeps
the trigger + dispatch essentials and a pointer here.)

The pass maps the Anthropic "dreaming" diagram (cloned memory store, one
reader per source, proposals with reasoning):

1. **Clone ($MEM → $MEM_OUT):** snapshot the mutable memory —
   `docs/minion-field-notes.md`, the `AGENTS.md` gotchas section — into
   `_bmad-output/memory/dream-<yyyy-mm-dd>/store/`. Bob and the sheep
   NEVER edit the live store.
2. **Sheep, one per source:** (a) field-note shards newer than the
   marker, (b) journal entries (Gru + Silas journals, one sheep reads
   both) newer than the marker, (c) ledger events
   since the marker (`bin/ledger events 200`, `bin/ledger show` on jobs
   with activity), (d) optional: pane transcripts of jobs that churned
   (repeated clarify loops, errors). **Backfill caveat (user-approved
   2026-08-19, U1):** files dated AT/before the marker are tail-read
   (last ~40 lines), not skipped — the marker/mtime filter silently
   drops late-written material (the 08-03→08-07 gru-journal backfill;
   the 08-17 dream recovered the 5.2 20h arc only by tail-reading).
   **Content-dating (user-approved 2026-08-29, U1 APPROVED):** dream
   inputs are dated by CONTENT — the entry's own date headers — never
   by file mtimes (mtimes drift with restores/edits; the 08-28 tree
   restore normalized ~200 files). The marker gates which FILES enter
   the pass; within a file, read and shard by content dates.
   Each sheep writes findings to its OWN shard in the dream dir —
   shard-by-writer, same as the live memory.
3. **Bob consolidates:** reads the sheep findings, hunts patterns —
   recurring tooling traps, recurring review findings, conventions that
   saved time, user-interaction patterns, stale entries to prune — and
   writes the **dream report** + the proposed updated memory state
   (edited copies under `store/`). Evidence bar: a pattern needs ≥2
   independent sightings (job ids + dates); a pattern of one is an
   anecdote and goes in the report as a *watch item*, not a proposal.
4. **Proposals, never silent mutation.** Every proposal carries: target
   file, the change, **evidence** (examples, job ids, dates),
   **reasoning**, and a risk class — **auto** (Gru applies immediately:
   shard promotions, duplicate pruning) vs **user-ack** (structural:
   new sections, playbook edits, policy/persona changes). Pattern
   verification pass: challenge each candidate against the evidence
   (**bmad-review-adversarial-general**) before proposing it.
5. **Silas closes the pass:** reviews the report, applies auto-class
   edits, escalates the user-ack list to Gru (who relays to the user),
   writes the `last-dream` marker (ISO timestamp), sets the ledger job
   `done`. Commit doc changes as `dream <date>: <one-liner>`.

**Concurrency:** the dream works on a cloned store plus per-sheep
shards — the same avoidance rules as the live memory; zero locks.

## Tracking — review-sensor failure modes

(Relocated from the playbook's review-sensor description. The core keeps
the action conventions + the catch-up cover; these are the known
failure modes that motivate them.)

- Review bodies are capped (~1500 chars — full text at the review URL).
- PRs with >100 reviews can fall back to the bare PR URL.
- Baselines are in-memory, so a Gru restart silently re-baselines (no
  catch-up — "no alert" ≠ "no reviews while Gru was down").
- The cover is the startup ritual's catch-up step: a fresh Silas runs a
  direct `gh pr view` sweep on every in-review PR (reviews, CI, merge
  state) and re-escalates anything unacked — a fresh session cannot
  verify an earlier escalation reached the user, and the escalation
  matrix prices a duplicate reminder at one line.
- Standalone PR conversation comments are ignored in v1.

## Tracking — sensor noise classes (classify before acting)

(Relocated from the playbook's pane-watcher + tracking narrative. Core
keeps the classification verb (clarify halt vs finished vs error vs
settle-noise); these are the recurring noise classes that have been
observed and their classification keys.)

- **Settle transitions:** after a minion finishes a turn, the watcher
  often reports `done -> idle` (or `working -> idle`) minutes later with
  zero new transcript content. Most of these are noise needing no ledger
  write and no user relay.
- **Fresh-dispatch boot:** `gone -> idle (ledger dispatched)` fires when
  the watcher polls a new pane mid-boot (shell -> pi registration)
  before the minion self-reports working. A fresh dispatch's first alert
  is usually the boot, not a problem.
- **Herdr server restart:** the watcher fires "pane no longer has a
  detected agent" for EVERY tracked pane — false alarm; pane ids and pi
  processes survive (verify via lsof on the pane cwd BEFORE any
  relaunch).
- **Dead-pi relaunch:** produces the same gone→idle alert as a fresh
  dispatch — classification key = alert-ts == new-session-file ts.
- **Pre-emptive classification:** Silas writes a "settle (working->done
  after clean completion): <summary>" note at close-out BEFORE the
  inevitable settle echo fires — the note IS the classification, so the
  echo that follows is note-only (and doubles as the human-readable
  completion summary: PR + suite counts + what was proven).

## Tracking — the no-PR completion gap

(Relocated from the playbook's fresh-session board-check. Core keeps the
board-check procedure; this is the incident that motivated it.)

A no-PR job (analysis / lavish+md+script deliverables / in-repo commits
with NO merge) falls through BOTH watchers: the pane watcher only tracks
NON-done jobs — the instant the minion runs `ledger set <id> done`, the
job becomes done -> untracked -> the pane's working->done/idle
transition fires NO alert — and the PR watcher has no PR/merge to catch.
So the completion can go unseen indefinitely. The intended durable
completion signal for no-PR jobs is the briefing-mandated
`herdr notification show "<id>" --body "..."` on finish — NOT ledger
reconciliation, NOT the watchers. Two failure modes to distinguish when
a no-PR completion slips: (a) NOTIFICATION-SENSOR gap — the minion fired
the notification but Silas missed it; (b) MINION-COMPLIANCE gap — the
minion skipped the notification step. VERIFY by checking the minion's
session jsonl for a `cli:notification:show` RESULT (not just the command
string in its text) — 0 results = compliance gap. No-PR jobs must NEVER
rely on pane/PR watchers alone. (2026-08-07: righttenantry-gcp-cost-
analysis — minion CONSTRUCTED `herdr notification show "gcp-cost-
analysis"` but did NOT execute it [0 cli:notification:show results] ->
compliance gap; the deliverable still reached the user via Gru's
independent check. 2026-08-15: bughunt2 was the SENSOR-gap flavor
(minion DID fire `cli:notification:show` ×2 at 00:22Z; the completion
was still unseen for 8.5h). Preserve no-PR deliverables to
`_bmad-output/implementation-artifacts/` BEFORE the worktree sweep.)

## Perkins — the lens run (full standing-orders paste-block)

(Relocated from the playbook's 'Perkins standing orders'. Silas pastes
this block verbatim into every Perkins round briefing; the core keeps
the essentials.)

- You are Perkins. You review; you never fix, push, or merge. You never
  touch the implementing minion's worktree or pane.
- Context: PR URL + number, reviewed sha, repo_root, the **original job
  briefing** and **GitHub issue** (your spec), and your cwd — a detached
  worktree at exactly the reviewed sha. Trust it, not `origin/<base>`.
- Save the canonical diff first:
  `gh pr diff <pr>` →
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>/diff.patch`.
  Every lens reviews these identical bytes. (Absolute path — the round
  worktree is destroyed at close-out, so artifacts live in the
  orchestrator's `_bmad-output`.)
- Run the lenses per the `code-review` skill's **Headless / Automated
  Mode** with: `diff_file` = the canonical diff just saved, `worktree` =
  your cwd (the detached round worktree), `spec_files` = the original job
  briefing + the GitHub issue (dump it with `gh issue view <n> --json
  title,body,comments` into the round dir first), `out_dir` =
  `/Users/moses/code/_bmad-output/perkins/<job-id>/r<N>`, and
  `prior_findings` = the previous round's `consolidated.json` when N > 1
  (re-review: fix audit first, carry-forward markers). The headless mode
  owns: pane mechanics (dedicated tab, `mm-<lens>-r<N>` labels), the
  `<lens>.json` output contract + existence check, one retry per failed
  lens, big-diff chunking, the mandatory verification pass, consolidation,
  and writing `consolidated.json`. Its verdict thresholds are yours
  below.
  **Lens-spawn rooting (user-approved 2026-08-18):** the headless spawn
  template pins `--cwd <worktree>` on every lens tab FOREVER — a lens
  pane whose cwd is not the round worktree is mis-rooted: close +
  relaunch with `--cwd`.
  **Empty-lens doctrine (2026-08-18/19):** acceptance/architecture
  lenses back 3-byte-EMPTY a THIRD straight generation → sweep those
  lens panes + regenerate (intervene — an empty-lens verdict never
  ships); a g-wave COMPENSATION verdict (a subset of lenses delivering a
  valid verdict) counts as valid.
  Visual checks (goldens, sprites): verify MECHANICALLY first
  (byte/hash/capture-diff). Perkins rides Astra (`openai-codex/gpt-6-astra`,
  2026-09-07 GPT ruling) — natively multimodal, so inline image reads are
  allowed, but mechanical-first stands and the USER remains the aesthetic
  verdict (their look rulings supersede any model opinion); a visual claim
  the user has not seen is flagged, never blessed. On a legacy blind-model
  session the `vision-read` skill routes the read. The describe_image
  auto-delegation stays retired (2026-08-18); never trust a text-only
  model's eye.
  You MUST close every lens pane before finishing.
- **Verdict → review event:**
  - 0 blockers → `--approve`
  - 1–3 blockers → `--request-changes`
  - 4+ blockers → `--request-changes`, body leads with "MAJOR REWORK"
  - **Degraded guard:** any lens failed AND zero findings remain → do NOT
    approve; `--comment` instead and flag Gru ("incomplete review").
- Post as the app (owner parsed from the PR URL). Mint first, then
  review — never run gh with an empty GH_TOKEN (a failed command
  substitution would fall through to the ambient `mssoka` credential and
  422 on our own PRs):
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner <owner>)` —
     capture STDOUT ONLY. NEVER append `2>&1`: the script writes cache
     warnings to stderr, which would corrupt the token and make a good
     mint look like a failure.
  2. Check for an EMPTY token, NOT `$?` (an intervening command can
     clobber `$?`, and a `2>&1` capture makes it lie — the 2026-08-09
     rc3-2 round posted a fallback-comment instead of a formal approve
     on exactly this):
     `if [ -z "$TOKEN" ]` -> the mint failed; fall back to `gh pr comment
     <pr> --body-file <body.md>`, note `fallback-comment` in your ledger
     note, and call it out in your final message.
  3. Otherwise (token non-empty): `GH_TOKEN=$TOKEN gh pr review <pr>
     --<event> --body-file <body.md>`
- Body format:
  ```
  ## 🤖 Perkins automated review — round <N>
  **Job:** <job-id> · **Reviewed sha:** <short> · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed against the code — <rejected> discarded as false-positive[, <u> kept as [unverified]]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Address findings and push — I re-review automatically on the new sha.
  The loop runs until an APPROVED verdict._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post
  anyway but note "reviewed `<old>`, head now `<new>` — a fresh round
  will follow" in the body.
- Self-report: `/Users/moses/code/bin/ledger set <round-id> working` at
  start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely —
  fixing is the implementing minion's job, triggered by the review relay.

## Perkins — round-budget evidence & incidents

(Relocated from the playbook's round-budget ops; the core keeps the
practices, this holds the field evidence and incident history.)

- **Skip-row payoff:** stepper-f1's r3 APPROVED 0B because two skips
  kept the final round for the merge candidate.
- **Proactive r2 on a fold-in — evidence:** RightTenantry #585 — r1
  APPROVED with N1 "no test asserts eu.posthog.com stays absent"; the
  user asked for N1 folded in pre-merge; r2 ran fix-audit with
  `prior_findings=r1/consolidated.json`. (dream-2026-08-07 UA3.)
- **Loop-until-APPROVED — precedents:** the 5.4 arc r1→r4 (r1 2B → r2
  2 new delta blockers → r3 1 → r4 APPROVED 0B); rc4-3 #606 r4+r5 under
  the old override.
- **Round close-out drift (2026-08-19/21):** the badge-out step fails
  SYSTEMATICALLY — round mains hang post-post (×2 on 08-20:
  demo-polish-2 r1/r2) and self-close-with-empty-result recovered-at-
  close-out covers ~2/3 of rounds in this window (UE bootstrap r2,
  slice-1 r1/r2/r3 — 5 recovered-verdict events + 2 badge-hangs).
  Expect to reconstruct every verdict from review artifacts (the
  pre-emptive verdict-note + durable lens JSONs save it; the Perkins
  tooling still owes the badge/token-mint fix task).
- **The W3 spawn-turn stall (3 clean sightings):** the round main's
  spawn-turn ends mid-lens-wave leaving it at prompt with NO error
  (toolUse stops only) — classify `main idle + lenses working` → ONE
  continue-nudge when the wave finishes; don't wait for an alert.
- **Machine-wide death (Mac reboot) ≠ lost work:** durable lens JSONs +
  diff.patch in `_bmad-output/perkins/<round>/` salvage the round —
  relaunch SAME row SAME sha, regenerate only the missing lenses (5/7
  JSONs survived the reboot; the verdict posted intact).
- **Perkins can self-close its round row:** closing the Perkins pane
  writes `working -> done` before Silas' close-out `set done`, which
  then no-ops (same-status) and eats the verdict detail. Write the
  verdict as a pre-emptive `ledger note` at close-out. NOT uniform —
  VERIFY the row state at close-out, don't assume either direction.
  Deepseek rounds leave the WORKTREE + lens panes behind more than kimi
  did — always verify + sweep worktree / branch / lenses at close-out.
  Close-sweeps scope to the round's OWN pane ids (from the round row /
  launch record) — NEVER id-proximity or label (08-17: a 5.9 close-out
  lens sweep killed dream sheep panes p1ZZ/p1Z0 adjacent to lens panes).

## Perkins — the #585 no-op round

(Relocated from 'When Perkins fires'; the rule stays in core.)

A docs-only / no-op head is **not** an automatic skip. RightTenantry PR
#585 (a CSP doc PR whose directives were byte-identical to `develop`)
still earned a useful r1 — Perkins APPROVED *READY TO MERGE*, i.e. it
confirmed the no-op, which is itself the verdict. (dream-2026-08-07
UA3.)

## Dispatch — handover incidents (chain, wait, delivery)

(Relocated from the playbook's dispatch step 6; the core keeps the
commands and rules, this holds the incidents that shaped them.)

- **Chain discipline — why pipes are banned on the wait:** `| head -1` /
  `| tail -1` mask the exit code — the chain continues even when the
  wait FAILED, delivering the handover to a still-booting pane (seen
  08-19 — the round silently launched on the default provider).
- **The sleep-3-after-idle is required:** `wait --status idle` returns
  the instant pi reports idle, but the TUI's input handler isn't always
  ready to accept keystrokes at that exact moment — without the sleep,
  the chained handover types into a not-yet-ready TUI and Enter is lost
  (buffer sits unsent; pane stays idle with an empty session). SEEN
  TWICE on 2026-08-06.
- **herdr 0.8.0 renamed the wait:** `herdr wait agent-status <pane>
  --status idle` is GONE; the 0.8.0 form is `herdr agent wait <pane>
  --until idle --timeout 90000`, and it RACES pi registration on fresh
  panes (`agent_not_found` while the agent entry doesn't exist yet) —
  sleep ~10 BEFORE the wait.
- **Verify delivery is a SEPARATE post-step:** `pane run` can leave text
  unsent when pi is mid-startup. Working within ~30s; else
  `herdr pane send-keys <pane> enter` for a stuck buffer. (2026-07-31:
  two handovers sat unsubmitted; the user spotted both. 2026-08-06:
  cost-analysis minion sat blank ~30s after boot because Silas ended
  the turn after the `wait` instead of chaining straight to the
  handover.)
- **An `idle` pane can hide a DEAD pi:** agent=pi, status=idle while no
  session file exists and pane reads return empty — the process died
  silently after launch. Verify via the session file
  (`ls ~/.pi/agent/sessions/<slug-dir>/`), then relaunch
  (`herdr pane run <pane> "pi"`), wait idle, re-hand over.
- **An `idle` pane can also hide a LIVE pi whose turn died on the
  provider:** kimi-coding stream returned `terminated` mid-rework, 3
  retries, turn errored out — pi stayed alive, the pane showed `idle`,
  and nobody noticed for 7.5h. The fix is one word —
  `herdr pane run <pane> "continue"` — with ~zero context loss. Before
  acting on an idle-mid-task pane: tail its session jsonl for
  `stopReason:"error"` / `errorMessage` — errored-turn → `continue`;
  no session file/process → relaunch.
- **Silent pi deaths:** a pi dies SILENTLY with the pane up (the 6.2
  minion's turn froze mid-tool-call, session silent 13.4h, an orphan
  core.bin spinning 99.9% CPU; Gru died silently ~00:38Z 08-21 and
  again ~10:52Z). The census/startup sweep is the detection layer. A
  WEDGED pi (continue + send-keys INERT) recovers only via the kill-pid
  path (`herdr pane process-info --pane <p>` → `kill <pid>`) → fresh
  relaunch + FULL context handover (blockers, rebase state, in-progress
  edits). Crash recovery must also RE-DELIVER undelivered escalations.
  The **night-watchman** (launchd, 5-min cadence, PRs #6/#7 08-21) is
  the standing out-of-pi liveness layer.

## Dispatch — bootstrap war stories

(Relocated from the playbook's dispatch step 4; the core keeps the
commands.)

- The env-symlink loop skips git-tracked files because symlinking
  tracked `.env.example`/`.env.test` in RightTenantry produced `T`
  typechanges waiting to be committed (2026-07-24).
- RT main-checkout worktree bootstrap: `cp -r` cycles on the
  self-referencing `_bmad` symlink — `rsync --exclude='_bmad'` is the
  standard copy (2026-08-13, ×2 same evening; recurs on every RT
  dispatch from the main checkout).
- A fresh RT worktree ships NO `node_modules`, so `make build` fails on
  `tailwindcss: command not found` — and `make test` never surfaces it
  (js-tests run on bare node). Symlink from the main checkout (07-24
  lesson: gitignored, never committed).
- **Identity tabs stay single-purpose:** a minion in Silas' tab
  auto-renames it `silas+<slug>` and looks like the COO doing the work.
  After any accidental split, move the minion out AND relabel the
  identity tab back to its bare owner name.

## Concurrency — serialize, valve & throttle history

(Relocated from the playbook's Perkins concurrency + top-level
concurrency; the core keeps the CURRENT rules, this holds the
superseded doctrines and the evidence.)

- **Serialize-on-quota (SUPERSEDED 2026-08-16):** two concurrent
  Perkins rounds (or a round + a fanned-out mega-minion wave) trip an
  account rate-limit 429 (a 13-pane glm-5.2 429 wave 08-09); serialize
  the bursts, one fan-out at a time. LIFTED by the user ruling
  2026-08-16: full throttle on all providers; a 429 wave = standard
  recovery (one continue per pane) + a note, never a hold. (The
  per-provider gate lived on: ZAI/glm-5.3 serializes one fan-out at a
  time — a 1302 burst hit the 5th glm-5.3 round of the day 08-14;
  ~5 rounds/day cumulative is the observed burst ceiling. k3 full
  throttle HELD clean through 3-concurrent + 2-round bursts 08-16/17.)
- **The ~20-pane valve (ADVISORY since 2026-08-19):** was a hard safety
  valve; the user ruled "dont hold... let them all run" (21 panes flew
  clean 08-19). Record valve-pressure as a row note and DISPATCH — the
  valve surfaces pressure, it no longer gates.
- **File-level disjointness — evidence:** 2026-08-13
  routing-bandwidth-cost held on `goldens/` overlap with #36's
  19-golden-file change; Jobs B+C verified disjoint → parallel.
- **Review-target stability (still gates):** don't dispatch on a sha
  about to be force-pushed away (rebase in flight = wait for the fresh
  sha). A fix-audit round is HELD on an UNSTABLE target: PR head still
  MOVING AND CI RED (real red only — CI PENDING is NOT red: #36 r1
  08-13, #28 08-12).
- **FULL THROTTLE chain pattern:** pre-author the downstream briefings,
  pre-stage the held worktree (rebase onto fresh `origin/<base>` at
  release), and pre-create the held ledger row with an explicit release
  trigger — zero idle time between links. (Serialize-hold practice for
  pane capacity: pre-create the round row so the Perkins sensor doesn't
  re-fire on the tick; release when the in-flight round's close-out
  frees panes. The held round's briefing NAMES the in-flight round it's
  behind and the RELEASE trigger. 6-deep held round chain seen 08-16:
  refcheck ← terminology ← … ← local-ci, all released cleanly.)

## Model policy — provider incident history

(Relocated from the playbook's Model policy narrative + changelog
context; the core + changelog state CURRENT truth, this holds the
incidents.)

- **The reasoning-tier saga:** kimi k3 RETIRED 08-12 → v4-pro primary
  → glm-5.3 primary 08-14 → k3 verified back 08-16 → HOLD regime
  08-18 → v4-pro BANNED 08-19 morning (cost) → glm-5.3 standing primary
  08-19 night (kimi cycle-cap) → U2 consolidation fixed the chain as
  k3 → glm-5.3 → HOLD. "X is back" is UNRELIABLE mid-cycle: k3
  flickered 22:35→01:41→02:41→03:40 in one night; a k3 403 recurred
  ~12 min after an apparent recovery.
- **Probe false-reads go BOTH directions:** k3 false-negative with empty
  error 08-19 08:10Z; glm false-DOWN 08-20 16:13Z (a chatty "OK — I'm
  here" reply vs the strict `^OK$` match) — re-probe once before acting
  on any surprising read.
- **Cap-reset times are estimates:** glm's 1308 rolling window freed
  ~11h EARLY vs the stated 20:43Z reset (08-20); a cap message's stated
  reset time lied (claimed 17:54Z vs actual 12:48Z) — never schedule a
  resume off the provider's stated time; only the probe decides.
- **1302 concentration:** with k3 cycle-capped, ALL reasoning rides glm
  and the account 1302-bursts EPISODICALLY (fleet-wide wave 17:53Z
  08-19: QoS-r1 + demo-mode-r4 + 7.3-r1 + dream panes together) — one
  continue per errored pane clears it; hold NEW glm dispatches until
  the wave settles; escalate only if continues stop clearing.
- **The 402 class (08-19):** deepseek 402 Insufficient Balance killed
  the always-live ops spare midday 08-19 (demo-mode + 7.3 turns errored
  402; the probe confirmed flash AND v4-pro dead account-wide) → user
  flipped ALL ops to glm-5.3, reverted to flash the same evening when
  the balance returned. An ACCOUNT wall (billing) — a user top-up fixes
  it; waiting does not.
- **Model dispatch & correction ops:** only a `provider/model` path
  naming an AUTHED provider works: bare `kimi-coding` fails (it's a
  PROVIDER, not a model — the label is `kimi-coding/k3`);
  `moonshotai/kimi-k3` MISROUTES via openrouter. `/model
  <provider>/<model>` typed to a RUNNING pi switches it MID-SESSION,
  context preserved. `PI_MODEL` env silently overrides the dispatched
  `--model`. Model flips apply to NEW dispatches only. Bare `pi`
  resolves to defaultProvider — which is deepseek-v4-flash since
  08-19 (wire-aesthetics r1 ran the WHOLE round on flash — sanctioned
  post-hoc as a one-off, NOT a precedent; pin `--model` + verify the
  session modelId after every launch). `/model` typed to a WORKING
  pane ends the current turn cleanly — ALWAYS pair with an explicit
  continue (6.2-r1 stalled 09:25Z→12:49Z on a bare mid-flight /model).
- **Vision provenance:** the describe_image silent lmstudio fallback
  ran 15+ invisible delegations in one day under a lying log identity
  (deleted same day 08-18). The LEFOU→KYLE rename (08-21) is a cast
  correction. **Current 2026-09-07 ruling:** GPT models are the native
  vision route — Astra/xhigh for 3D and Blender, Sol/xhigh for non-3D
  helpers, Luna/max for Silas; KYLE remains a role, not a hard-coded
  legacy GLM provider. Verify new models THROUGH pi (probe + session
  jsonl), never raw API curls or the reply's self-named id. Legacy visual
  models remain explicit, authorized fallbacks only (a "glm-4.7"
  self-report was model HALLUCINATION; a "ZAI balance 0" conclusion was a
  WRONG-ENDPOINT curl).

## Lavish — the review flow (mechanics) & incidents

(Relocated from the playbook's lavish section; the core keeps the
standing policy + a pointer here.)

**Mechanics:**

- **Minions:** build the artifact per the skill (open the matching
  playbooks first: `npx -y lavish-axi playbook <id>`), open the session
  (`npx -y lavish-axi <path>`), then foreground-poll
  (`npx -y lavish-axi poll <path>`, first poll with
  `--agent-reply "<what to review first>"`). Apply feedback, re-poll,
  until the user Send & Ends. Artifacts stay at their task-conventional
  paths (e.g. `_bmad-output/...`) — lavish is file-path-keyed, no
  `.lavish/` relocation needed. Never kill the poll; if it dies, re-run
  — queued feedback is never lost. One shared local server (default port
  4387, `LAVISH_AXI_PORT` to override) multiplexes all sessions by file
  path — end YOUR session with `npx -y lavish-axi end <path>`; NEVER
  `lavish-axi stop` (it kills the shared server for every minion's
  session).
- **Gru:** feedback goes straight to the polling minion — no relay, no
  ledger transition (the job stays `working`). Fallback: if the producing
  minion is gone (reclaimed pane), Gru polls himself
  (`npx -y lavish-axi poll <path>`) and relays, or dispatches a fresh
  minion with the artifact path. Watcher note: a polling minion shows
  `working` — that is waiting, not stuck.
- **Gru/Silas-originated sessions — MINION STEWARD:** when Gru or Silas
  needs a lavish artifact (ruling pages, capsule concepts, escalation
  clarifies), **dispatch a small minion to own the session end-to-end**
  rather than running the poll in Gru/Silas's own pane. The minion
  builds (or receives) the artifact, opens the session, foreground-polls
  per the skill's default — its pane blocks on the poll, which is NORMAL
  for a minion (it's working, not stuck). User annotates → minion
  receives feedback → applies → relays results via `herdr notification
  show` or pane message. **Fallback (herdr-wake poll):** if spawning a
  minion is too heavy for a tiny one-off artifact, run the poll in a
  scratch pane with a `;`-separated wake:
  ```bash
  herdr pane run <scratch-pane> \
    "npx -y lavish-axi poll <path> ; herdr pane run <gru-pane> '[LAVISH] feedback on <path>'"
  ```
  Separator MUST be `;` not `&&` — the poll exits NONZERO on user Send &
  End. But prefer the minion-steward pattern; it's cleaner and the
  minion can apply feedback + iterate without round-trips through Gru.

- **The minion-steward pattern (2026-08-05) replaced herdr-wake as the
  primary** for Gru/Silas-originated sessions: dispatches a small minion
  to own the session end-to-end; the orchestrators never run the poll in
  their own panes.
- **A lavish session-end can STRAND queued-but-undelivered prompts:** a
  poll that exits on session-end may miss the final queue — the user's
  verdict ('Approve — open the PR') sat in ~/.lavish-axi/state.json
  (session prompts, by uid) while the poll exited having delivered only
  the earlier rulings. Ground truth:
  `~/.lavish-axi/state.json` → `sessions.<id>.chat[].text` — verify it
  BEFORE acting on any load-bearing verdict. Drain-then-exit, or check
  state.json after exit.
- **HTML builds via piped subprocess stdout TRUNCATE at ~85KB**
  (pipe-buffer). Build via a file write, then verify byte length + tail
  section before serving. Read the poll's dom_snapshot — it is the only
  self-check of what the user actually saw (caught a Mermaid render
  failure the author's eyes missed).
- **Never `lavish-axi stop`** — one shared local server (default port
  4387) multiplexes all sessions by file path; `stop` kills every
  minion's session. End YOUR session with `lavish-axi end <path>`.
  One foreground poll per session; if killed, re-run (queued feedback
  is never lost).
- **Watcher note:** a polling minion shows `working` — that is waiting,
  not stuck.

## Skills availability — self-containment history

(Relocated from the playbook's Skills availability; the core keeps the
current state and the bmad-updates rules.)

- Skills became **git-tracked 2026-08-01 (self-containment)**: the repo
  carries its whole skill set — `bmad-*`, `gds-*`, `lavish`, `code-review`
  + `review-plan` (Perkins' review skills, imported from
  `~/.claude/skills`), and `herdr` (deduped from identical copies in
  `~/.agents/skills` and `~/.claude/skills`). Everything is symlinked
  into `~/.pi/agent/skills/` (and the three imports also into
  `~/.claude/skills/`, herdr also into `~/.agents/skills/`), so pi
  agents see them from any cwd (including worktrees).
- **bmad updates flow detail:** run the bmad installer/update (writes
  fresh vanilla `bmad-*`/`gds-*` skill files); check where it wrote —
  `~/.pi/agent/skills/bmad-*` are symlinks INTO the repo: if the
  installer wrote through them, the update already landed in
  `/Users/moses/code/.agents/skills`; if it REPLACED the symlinks with
  real dirs, copy the new skill dirs into `.agents/skills/` and
  re-create the symlinks; then `git diff .agents/skills` — review what
  bmad changed, commit, push. Never hand-edit skill files (clobbered on
  the next update) — overrides go in `_bmad/custom/`.
- **The bmad-build render failure (2026-08-21, still open):**
  `render_skill.py` HALTs with `ambiguous config value
  implementation_artifacts` (modules.bmm + modules.gds both define it).
  Sanctioned path (Silas ruling 08-21 06:10Z): skill WAIVED —
  self-contained briefing + the waiver carried as a canon note in the
  PR body; avoid naming bmad-build in briefings until upstream dedupes
  the token.

## Changelog continuation

The core playbook's `## Changelog (supersede history)` appendix is the
living dated one-liner list; entries older than the current cycle are
folded here rather than deleted:

- **2026-08-21** — playbook diet: core/annex split (relocation +
  tightening only, zero doctrine change). Superseded nothing.
- **2026-08-21** — vision mega-minion renamed LEFOU → KYLE (Despicable
  Me cast correction, user ruling; playbook commit 272984c).
- **2026-08-21** — Lefou/glm-5v-turbo downgraded → glm-4.6v (not
  subscription-available; probe-verified, playbook commit 90ea85a).

## Dispatch — worktree bootstrap (exact commands)

(Relocated from the playbook core's Dispatch step 4 on 2026-08-21; the
core keeps a one-line pointer. Worktrees only get git-tracked files.)

- Missing `<worktree>/_bmad` + `<repo_root>/_bmad` exists →
  `cp -R <repo_root>/_bmad <worktree>/_bmad`
- **Env files** (gitignored, absent from the worktree): **symlink**
  from the main checkout — single source of truth:
  ```bash
  for f in <repo_root>/.env <repo_root>/.env.*; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    # skip git-tracked files (symlinking .env.example/.env.test produced `T` typechanges)
    git -C <worktree> ls-files --error-unmatch "$base" >/dev/null 2>&1 && continue
    ln -sf "$f" "<worktree>/$base"
  done
  ```
  Subdir env files: list in the briefing, symlink the same way.
  Gitignore applies in the worktree too — never committed.
- **JS repos — `node_modules`** (gitignored): fresh worktrees ship
  none, so `make build` fails on `command not found`. **Symlink** from
  the main checkout (same base deps — safe, never committed):
  ```bash
  [ -d <repo_root>/node_modules ] && [ ! -e <worktree>/node_modules ] \
    && ln -s <repo_root>/node_modules <worktree>/node_modules
  ```
  (Deps changes → the minion runs its own `npm ci`.)
- Tell the minion in the briefing which env files were bootstrapped.
