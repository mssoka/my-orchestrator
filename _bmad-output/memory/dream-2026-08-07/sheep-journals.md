# Sheep findings — Gru + Silas journals

Material: **8 journal files** read (Gru: 07-31, 08-01, 08-02; Silas: 08-03 →
08-07). ~95 timestamped entries total. Undreamed window = entries newer than
**2026-08-03T11:12:13Z** → all of Silas 08-04/05/06/07 + Silas 08-03 from
~11:35Z onward; Gru 08-01/08-02 are pre-marker but were re-edited 08-05, so I
mined them for patterns the dream-2026-08-03 pass may not have promoted. Gru
has **NO 08-03..08-07 files** (gap — see bottom).

Notation: "gotcha #N" refers to the numbered gotchas in the AGENTS.md store
(the 17 I was briefed on). "Pre-marker" = on or before 2026-08-03T11:12:13Z
(should already have been consolidated by dream-2026-08-03 — if absent from
the store, that pass skipped it).

---

## Candidate patterns (NEW — not in gotchas)

### 1. `ledger set <id> in-review "<url>"` does NOT populate the `pr` field
A minion's self-report puts the URL only in the note; the `pr` field (what the
PR watcher needs to poll merge/review/CI/conflict) stays empty → sensors skip
the job silently. Always follow with `bin/ledger pr <id> <url>`.
- Sightings:
  - Silas 08-06 00:51 (packet-plumber-setup #1): "`set in-review "<url>"` does NOT populate the `pr` field — always follow with `bin/ledger pr`"
  - Silas 08-06 00:12 Aug-7 (packet-plumber-gdd-v1 #2): "the minion ran `set in-review "<url>"` but NOT `ledger pr` -> pr field was EMPTY -> I set it"
  - Silas 08-06 01:53 / 08-07 08:55: csp + architecture minions ran `ledger pr` themselves → "the GDD field-note lesson propagated" (confirms the pattern is teachable)
- Already in store? **no** (gotcha #1 is about the *table view* being lossy; this is a distinct field-population gap)
- Candidate memory target: **AGENTS.md gotchas** (3+ sightings, silent-failure class, every in-review transition risks it)

### 2. glm-5.2 bare label → opencode provider (no key); use full `zai-coding-cn/glm-5.2` path; failure is SILENT on agent_status
Bare `glm-5.2` resolves to the wrong provider with no API key. PI_MODEL env
beats the `--model` flag. The failure shows idle + pi UI up with a red "No API
key" line in the pane; the session jsonl never exists.
- Sightings:
  - Gru 08-02: "bare label → 'opencode' provider (no key); sprint-plan used full 'zai-coding-cn/glm-5.2'… Future glm dispatches: use full provider path."
  - Silas 08-04 23:45/23:50: "glm-5.2 -> opencode provider, no API key… The error was silent on agent_status (idle with pi UI up)… the session jsonl never existed."
  - Silas 08-05 09:50 prep + 18:46: "PI_MODEL=glm-5.2 in env overrides --model flag"; "GLM reliability issues: 3 sightings"; glm-5.2 429 (4th) on finlit rebase
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (model-routing + silent-failure; recurred 4× this window)

### 3. deepseek Perkins self-closes the round ROW but leaves the worktree (+ sometimes lens panes) behind
Unlike kimi, deepseek rounds mark the ledger row `done` reliably but do NOT
tear down the worktree/branch/lenses. Always: note the verdict (not `set` —
same-status no-op), sweep worktree + branch, verify gone.
- Sightings:
  - Silas 08-04 23:35: "deepseek Perkins self-closes its ROW reliably but leaves panes/worktree behind more often than kimi did — always verify+ sweep at round close-out, don't assume"
  - Silas 08-06 02:19: "LESSON reaffirmed (3rd sighting): deepseek Perkins self-closes the round ROW… leaves the WORKTREE behind"
  - Silas 08-06 03:04 + 08-07 01:01: same close-out sweep applied again
- Already in store? **partial** — gotcha #14 (Perkins self-closes round row → use `ledger note`) is the ledger half; the **worktree/lens-leftover** half is not in the store
- Candidate memory target: **AGENTS.md gotchas** (extend #14) — model-specific close-out discipline

### 4. Perkins self-creates its ledger round row when Silas hasn't (leaves pane_id/tab_id empty)
Standing-orders `set working` falls back to `add`+`set`, writing a row with
empty pane_id/tab_id. Full sha WAS in the note so sensor dedup held, but the
row is malformed. Fix: write the round row BEFORE handover (pane_id + sha
complete).
- Sightings:
  - Silas 08-05 18:35 (oauth r1): "Perkins self-creates its ledger round row when Silas hasn't written it yet… leaving pane_id/tab_id empty — backfill via sqlite UPDATE (CLI has no pane-set)… Future: write the round row BEFORE handover to avoid the race."
  - Silas 08-05 18:46: "wrote the round row BEFORE handover (pane_id+sha complete) — no self-create race this time"
  - Silas 08-06 01:54 / 02:42: "ledger round row written FIRST with full sha in note (durable dedup)" — the fix became standard
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (ledger-hygiene race at dispatch)

### 5. Killing a stuck/403-dead pi: `exit` text fails; C-c isn't uniform → `herdr pane process-info` → kill the node PID
`exit` typed into a 403-dead pi does nothing. C-c sometimes leaves the TUI
alive. Reliable path: `herdr pane process-info --pane <p>` → `kill <pid>`
(node) from bash → pane drops to shell.
- Sightings:
  - Silas 08-04 22:50: "kill via send-keys C-c — 'exit' text can't kill a 403-dead pi; session file verified"
  - Silas 08-04 23:00: "C-c isn't uniform — when the TUI survives it, `herdr pane process-info --pane <p>` → kill the pi PID (node) from bash; pane drops to shell cleanly"
  - Silas 08-04 23:15: "Third OS-kill relaunch… C-c surviving the TUI is now the dominant pattern on these panes"
- Already in store? **no** (gotcha #4 is about *detecting* a dead pi; this is the *kill* mechanics)
- Candidate memory target: **AGENTS.md gotchas**

### 6. `gh pr diff` 406s on huge rename diffs → generate the canonical diff locally
On a 777-file rename, `gh pr diff` 406'd. Perkins fell back to
`git diff <base>...<sha>` locally.
- Sightings:
  - Silas 08-03 15:15: "gh pr diff 406'd on the 777-file rename — Perkins generated the canonical diff locally (9480ec9..sha)."
  - Silas 08-04 recent-lessons: "gh pr diff 406s on huge rename diffs -> Perkins generates the canonical diff locally (git diff <base>...<sha>)."
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (or minion-field-notes — Perkins-specific tool fallback)

### 7. `gh repo delete` needs the `delete_repo` scope — not grantable non-interactively from a pane
The mssoka gh token lacked `delete_repo`; `gh auth refresh -s delete_repo`
opens a browser flow. So repo deletion = web UI or interactive scope refresh,
never a pane command.
- Sightings:
  - Silas 08-06 00:59 (stray mssoka/packet-plumber): "GOTCHA (reusable): `gh repo delete` needs the `delete_repo` scope, which the mssoka gh token LACKS; it can't be granted non-interactively from a pane… So repo deletion = web UI or an interactive scope refresh, never a pane command."
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (single sighting but a clean, reusable, destructive-op guard — the user hit it directly)

### 8. `custom_message` count == 0 does NOT mean the extension is unarmed
silas.ts injects standing orders via `before_agent_start` systemPrompt
augmentation and the checklist via `sendUserMessage` (role=user) — **neither**
is a `custom_message` entry. So a 0 custom_message count is normal for a live
Silas. This **refines** gotcha #15 (pane forensics = session jsonl).
- Sightings:
  - Silas 08-05 23:40: "a `custom_message` count of 0 in the session jsonl does NOT mean silas.ts is unarmed — it injects standing orders via `before_agent_start` systemPrompt augmentation… neither of which is custom_message."
  - (Contrast Gru 08-01 Addendum 3 used custom_message presence as the armed-signal — that Gru inference is correct for gru.ts but NOT generalizable to silas.ts.)
- Already in store? **partial** — gotcha #15 says "ground truth = session jsonl entry types"; this corrects an over-broad reading of that test
- Candidate memory target: **AGENTS.md gotchas** (refine #15 with the caveat)

### 9. Perkins headless lenses spawn at ~/code (not the worktree) → sessions land in Gru's session dir
The code-review headless mode parents lenses to the round pane but spawns them
at cwd ~/code, so their session files land in Gru's `--Users-moses-code--`
session dir. Benign (lenses cd into the worktree to read code; no
custom_message so no Gru orders injected) — but it's the exact trigger the
pseudo-Gru gotcha (#10) warns about. Real failure = a lens ever ACTS on Gru
standing orders.
- Sightings:
  - Silas 08-05 19:05: "the code-review headless mode spawns lenses at ~/code (not the worktree) → their sessions land in Gru's session DIR… Benign here… but it's the exact trigger the pseudo-Gru gotcha warns about. If a future lens ever ACTS on Gru standing orders (dispatches), that's the real failure."
- Already in store? **no** (gotcha #10 is about a full pi at the root cwd; this is the lens-spawn variant)
- Candidate memory target: **AGENTS.md gotchas** (extend the pseudo-Gru gotcha)

### 10. Closing a Perkins parent pane cascades its lens children → don't error-loop on the children
Headless code-review parents lens panes to the round pane; closing the parent
tears down children, so closing each child *afterward* returns
`pane_not_found`. Either close lenses first then the round pane, OR rely on
the cascade and don't error-loop.
- Sightings:
  - Silas 08-05 19:24: "closing a Perkins pane cascades its lens child panes (headless code-review mode parents them to the round pane) — closing lenses individually AFTER the parent returns pane_not_found. Either close lenses first, then the round pane, OR rely on the cascade and don't error-loop on the children."
  - Silas 08-06 02:19: "NO lens panes left (Perkins badge-out'd them cleanly)" — the sweep-vs-cascade discipline held
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (2 sightings; this is the "watcher pane-vanished self-inflicted" item — confirmed self-inflicted)

### 11. Linked-worktree: `test -d .git/rebase-merge` is WRONG (.git is a gitfile); `git status` is the authority
In a worktree `.git` is a file, not a dir, so the rebase-in-progress probe
fails silently. Use `git status` (`## HEAD (no branch)`, `UU <file>`).
- Sightings:
  - Silas 08-05 18:46 (finlit-e2-7 rebase): "`test -d .git/rebase-merge` is WRONG in a worktree (.git is a gitfile) — `git status` (`## HEAD (no branch)`, `UU .memlog.md`) is the authority."
- Already in store? **no**
- Candidate memory target: **minion-field-notes.md** (git/worktree mechanics — useful to any minion, not orchestration-specific)

### 12. Close-out `pull --ff-only origin <base>` ASSUMES the main checkout sits on `<base>`
When the main checkout is on another branch, or the local base ref has
diverged from origin, the ff-only pull aborts. Don't force; report — a
diverged local base ref is the user's to reconcile, not Silas's.
- Sightings:
  - Silas 08-07 07:16 (RT-Agents #169): "`git pull --ff-only origin develop` FAILED — the main RT-Agents checkout is on `fix/156-…`… Tried `git fetch origin develop:develop`… REJECTED as non-fast-forward (local develop has DIVERGED)… Left BOTH untouched per the no-force caveat… A diverged local base ref is the user's to reconcile, not Silas's."
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (close-out discipline; "don't force" pairs with the existing no-force gotcha)

### 13. Lavish verdict can strand in `state.json`; minion-steward is the PRIMARY pattern, herdr-wake the fallback
Lavish foreground-poll exits nonzero on session-end → an `&&`-chained
herdr-wake never fires, and a verdict typed at session-end can fail to cross.
`~/.lavish-axi/state.json` prompts are ground truth before any "no verdict"
declaration. Structural fix: always dispatch a minion to OWN the lavish
session (minions foreground-poll naturally; orchestrators stay free).
- Sightings:
  - Gru 08-01 20:3xZ: "lavish poll exits nonzero on ended session → '&&' wake never fires. Playbook fixed to ';'"
  - Gru 08-02 14:40Z + 08-02 ~15:0xZ: "Privacy PR #565 open (verdict recovery worked — lavish dropped the user's 'Approve' prompt; state.json was ground truth)"; "minion-steward is now the PRIMARY pattern for Gru/Silas-originated lavish; herdr-wake demoted to fallback"
  - Silas 08-03 13:55: "Gru found the user's verdict stranded in lavish state.json (uid 1, 'Approve — open the PR')… state.json prompts are ground truth before any 'no verdict' declaration… The herdr-wake pattern needs a drain-then-exit poll."
- Already in store? **no** (the gotchas cover handover/buffer races, not lavish verdict stranding)
- Candidate memory target: **AGENTS.md gotchas** (3 sightings; silent verdict loss is high-value)

### 14. Clarify-halt relay protocol + direct-to-pane user turn can stale the escalation
When a minion halts with numbered questions, escalate verbatim to Gru and
leave the minion parked. BUT if the user then types a follow-up **directly in
the minion pane**, the original Gru escalation is stale — stand Gru down on
relaying it (would dirty the user's channel with a redundant Q).
- Sightings:
  - Silas 08-06 00:38 → 00:40 (packet-plumber): first clarify-halt escalated; "Second working→idle alert… NOT a settle echo: the user typed a follow-up directly in the minion pane… Flagged Gru to STAND DOWN on relaying the 00:38 escalation (stale — user is driving in-pane)"
  - Silas 08-06 01:25 (csp-posthog): minion "DISPROVED the briefing's CSP rationale" → 3 numbered Qs → "Escalated verbatim to Gru"
  - Silas 08-06 13:02 (agent-model-flash): minion found work is in a *different repo* → 3 numbered Qs → "Escalated verbatim to Gru"
- Already in store? **partial** — gotcha #15 (pane forensics) covers the related "phantom approved = the user" case (Gru 08-02, Silas 08-03 18:20); the **stand-down-on-stale-escalation** half is new
- Candidate memory target: **AGENTS.md gotchas** (3+ sightings; channel-hygiene)

### 15. Hold-release for pane capacity (serialize-hold) — pre-create the round row to dedup the sensor
When the valve is near capacity, hold the next Perkins round: pre-create its
ledger row (status dispatched, full sha in note) so the Perkins sensor doesn't
re-fire, then release when another round's close-out frees panes. Trigger =
close-out of the in-flight round.
- Sightings (this is the brief's "hold-release" watch item — **≥2nd sighting, propose**):
  - Silas 08-03 18:15/18:50/18:50: "Second serialize-hold: r1 on #570 queued behind #569's round… pre-created row dedupes the sensor; trigger = #569's round close-out frees 8 panes"; "Third serialize-hold: r1 on #571 behind nojs's round… The hold-release rhythm is now standard ops"
  - Silas 08-04 00:25/00:45/01:05: e2-1 r1 released, then e2-7 r1 released — "Third clean serialize hold/release of the night"
  - Silas 08-05 18:35/18:46: oauth r1 dispatched under the same mechanics
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (≥5 sightings; this is now standard ops but undocumented in the store)

### 16. Dual-gate echo: launching Gru with BOTH PI_GRU=1 AND PI_SILAS=1 → watcher alerts duplicate into Gru
With both gate vars set, gru.ts AND nefario-watch both fire in Gru's pane →
watcher alerts duplicate. Recovery: relaunch Gru with
`env -u PI_SILAS PI_GRU=1 pi` (PI_SILAS unset). **Was this journaled? — YES,
Gru 08-01 Addendum 3**, but it is NOT in the gotchas.
- Sightings:
  - Gru 08-01 Addendum 3: "This Gru process has BOTH PI_GRU=1 AND PI_SILAS=1 in env; gru.ts AND nefario-watch are both live here. Watcher alerts WILL duplicate into Gru — treat them as echoes… relaunch Gru's pane as `PI_GRU=1 pi` with PI_SILAS UNSET (`env -u PI_SILAS PI_GRU=1 pi`)"
- Already in store? **no** (gotcha #10 "pi at cwd=/Users/moses/code IS Gru" is a different gate — cwd vs env-vars)
- Candidate memory target: **AGENTS.md gotchas** (distinct from #10; the brief explicitly flagged this for verification — confirmed journaled-but-unfiled)

### 17. "Moot on merge" is NOT the default — check for deliberate-audit-intent before sweeping a mid-flight round
A normal terminal merge of an APPROVED PR → sweep the in-flight round as moot,
no re-dispatch. But a *deliberate pre-verdict* merge (user merges to peek at
findings) → dispatch a FRESH post-merge audit round. When unsure: sweep fast +
re-dispatch (costs one worktree add).
- Sightings:
  - Silas 08-03 14:45 (#564): "Lesson: 'moot on merge' is NOT the default — check whether the merge was deliberate-with-audit-intent before sweeping a mid-flight round (or sweep fast and re-dispatch — costs one worktree add)."
  - Silas 08-05 19:24 (finlit#11): "Perkins r2 mooted… no audit-intent signal (unlike the #564 deliberate-pre-verdict case), so swept as moot, no re-dispatch." (2nd sighting — the distinction was *applied*)
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (2 sightings; cap/round-budget practice)

### 18. Proactive r2+ dispatch (round-budget ops) vs let-the-sensor-fire for r1
On a fix-push to an already-open PR, dispatch the next Perkins round
**proactively** (don't wait for the 5-min sensor tick). For r1, let the sensor
fire (canonical flow). Skip-row docs-only heads (badge-out/memlog on an
APPROVED sha) to avoid wasting a round on noise.
- Sightings:
  - Silas 08-06 02:42: "Perkins r2 dispatched PROACTIVELY (round-budget ops — fix-push landed, don't wait for the sensor tick)… the proactive pattern is reserved for r2+ re-reviews"
  - Silas 08-04 01:05 (skip-row): "skip-rowed the docs-only head to avoid a wasteful r2 on noise" (skip-row itself predates this window — 08-01 — so likely already field-noted; the r2+-proactive framing is the new part)
- Already in store? **partial** — skip-row is a known practice (pre-marker); the proactive-vs-sensor r1/r2+ distinction is not in the store
- Candidate memory target: **AGENTS.md gotchas** (round-budget practice)

### 19. In-repo (no-worktree) job sequencing: Gru's fresh dispatch = signal the prior pane is done
An in-repo follow-up job needs the repo's working tree free. Gru dispatching
the next job IS the signal the prior pane is done being used → close that
pane + sync the base first. In-repo pane creation = `herdr tab create --cwd
<repo>` (no worktree create). Close-out: close the pane BEFORE deleting the
branch (the pane shares the working tree).
- Sightings:
  - Silas 08-06 01:2xZ: "an in-repo follow-up job (no worktree) on a repo whose working tree is occupied by a prior job's pane requires closing that pane + syncing the base first — Gru's fresh dispatch is the signal the prior pane is done being used. `herdr tab create --cwd <repo>` is the in-repo pane-creation path"
  - Silas 08-06 00:57: "in-repo jobs (no worktree) make close-out's git step share the pane's working tree — close the pane before deleting the branch, and mind an active user before closing."
  - Silas 08-07 08:55/09:3xZ: packet-plumber GDD/architecture/sprint-plan all dispatched in-repo with this pattern
- Already in store? **no**
- Candidate memory target: **AGENTS.md gotchas** (recurring — packet-plumber pipeline is entirely in-repo)

### 20. Stale-premise / stale-forensics: a briefing's "current state" can be wrong — verify disk before trusting
Briefing premises can be wrong (minion disproves) OR stale vs merged work
(forensics pre-date a recent PR). Verify-then-widen on security controls;
grep disk for current state; escalate beats duplicating on a stale
instruction.
- Sightings:
  - Silas 08-04 23:05: "Held a stale-premise model switch (verify-then-flag)… don't improvise on a stale instruction; the work was done, escalating beats duplicating."
  - Silas 08-06 01:25 (csp-posthog): minion "DISPROVED the briefing's CSP rationale… the verify-before-widening mandate saved a needless CSP relaxation."
  - Silas 08-07 00:45 (RT-Agents): "STALE-FORENSICS FINDING: the briefing's forensics pre-dated PR #164… the minion ground-truth-grepped… Lesson: briefing forensics can be STALE vs merged work — always grep disk for current state before trusting a briefing's 'current state'"
- Already in store? **no**
- Candidate memory target: **minion-field-notes.md** (a minion-side self-review discipline; 3 sightings)

### 21. `edit` tool aborts ALL edits for a file atomically when one oldText mismatches
One mismatch rolls back the whole batch wholesale. Verify multi-line oldText
line-break positions with grep before submitting multi-edit batches.
- Sightings:
  - Gru 08-01 (Silas-instituted addendum): "`edit` tool aborts ALL edits for a file atomically when one oldText mismatches — two playbook attempts rolled back wholesale. Verify multi-line oldText line-break positions with grep before submitting batches."
- Already in store? **no** (pre-marker — dream-2026-08-03 may have skipped it; it's a tool-behavior note useful to every minion)
- Candidate memory target: **minion-field-notes.md**

### 22. Provider-instability clustering this window — count + recovery map
- **2× quota 403 waves** (Gru 08-02 ~05:14Z killed Perkins r2 on #563; Gru 08-02 ~19:5xZ killed grace-Perkins startup; Silas 08-03 19:40Z "Quota wall #2") — recovery: **user purchased/refreshed quota** both times; 403-dead turns ARE continue-able ONCE the quota is back.
- **3× connection-error waves** (Gru 08-02 ~12:0xZ fleet-wide; ~13:0xZ finlit; Silas 08-03 same day) — recovery: **one `continue` per pane** (gotcha #12 doctrine), zero context loss.
- **1× glm-5.2 429 rate-limit** (Silas 08-05 18:46 finlit rebase) — recovery: one `continue` after the ~10-min rate window reset.
- **kimi weekly limit hit** (Silas 08-04 onward) — recovery: **wall kimi until 08-08T21:57Z reset**, switch Perkins + minions to deepseek/glm.
- Quota-403 nuance (Silas 08-03 19:50): "the doctrine's nuance confirmed: 403-dead turns are continue-able ONCE the quota is back (the earlier 'continue does nothing' note was about the quota being ACTIVE)."
- Already in store? **partial** — gotcha #12 covers the 3 classes; this window's contribution is the **quota-restored-then-continue** nuance + the model-redirect contingency (deepseek as the reliable non-kimi default)
- Candidate memory target: **AGENTS.md gotchas** (refine #12 with the quota-restored nuance)

---

## Watch items recurring (2nd sighting this window)

- **Hold-release / serialize-hold for pane capacity** — promoted to candidate #15 above (≥5 sightings). ✅ propose.
- **Watcher "pane vanished" self-inflicted** (parent-close cascades children) — promoted to candidate #10 above (2 sightings). ✅ propose.
- **Moot-on-merge vs deliberate-audit-merge** — promoted to candidate #17 above (2 sightings). ✅ propose.
- **dual-gate echo (PI_GRU+PI_SILAS relaunch)** — promoted to candidate #16 above; confirmed **journaled** (Gru 08-01 Addendum 3) but unfiled. ✅ propose.
- **non-blocking clarify halt** — promoted to candidate #14 above (3+ sightings). ✅ propose.
- **ledger event text strips `$`** — **not strongly sighted this window.** The only `\$` occurrences are journal-prose escaping (e.g. Silas 08-06 13:0xZ "cost \$1.16 v \$1.74/Mtok"), not ledger-event-strip evidence. Cannot confirm a 2nd sighting; leave as watch-only.

---

## One-off anecdotes (single sighting — watch items)

- **Pane-run-during-compaction queues cleanly** (Silas 08-06 00:59): a `herdr pane run` to Gru delivered *post-compaction* (Gru compacted mid-relay) — "my msg queued, crossed once compaction finished… don't re-send; verify after." Watch: if it recurs → propose.
- **Verify-then-report, especially when the report is "nothing happened"** (Silas 08-03 18:25 gate-drill): "when checking gate drift, check the LEDGER and gh FIRST, not just the visible transcript tail — the incriminating actions were already behind the scroll fold; I reported 'no commit/push' from a stale read and had to correct within minutes." Watch.
- **Co-touch heads-up protocol** (Silas 08-03 18:40): "verify overlap first; if a round is mid-flight and overlap is real, hold the relay until close-out" (a reflex rebase relay would have skewed #570's mid-flight Perkins sha). Watch.
- **`herdr worktree open` rejects a manually-created detached worktree** (Silas 08-05 18:35): fell back to `herdr worktree create --base <sha>`; functionally equivalent for an unpushed review branch. Watch.
- **`herdr pane move` mid-flight** — no new sighting this window (already gotcha #5). No-op.
- **Missing local feature branch at close-out** (Silas 08-07 09:26): "local packet-plumber-architecture-v1 was ALREADY gone… unclear when it was deleted… no harm — main has the content via the merge… always verify main has the merge commit before treating a missing branch as 'clean.'" One-off; low value to store.

---

## Gru journal gap (08-03..08-07 missing) — any signal?

**Gru has NO journal files for 08-03, 08-04, 08-05, 08-06, 08-07** — a 5-day
hole in the CEO's episodic memory. The Silas (COO) journals 08-04..08-07 are
the only continuous record for that span (which is exactly why this sheep was
told to read BOTH).

Signal / risk:
- **User rulings + strategic decisions in that window live ONLY in Silas's journal + the ledger.** Examples with no Gru counterpart: the cap-override r4 on #563 (closed 08-03 11:35 — Gru journaled the *ordering* 08-02 but not the payoff); the entire **packet-plumber** arc (repo creation → setup #1 → GDD #2 → architecture #3 → sprint-plan, 08-06..07); the **RightTenantryAgents allow-list adoption + model-flash re-dispatch** (08-06, incl. the AA upgrade data justifying Pro→Flash); the **dream-2026-08-07 dispatch** (08-07 10:16); the **dual-gate-echo relaunch resolution** (executed, but only journaled as a 08-01 open loop — no closure entry).
- **A future dream consolidating from Gru journals alone would MISS 5 days of rulings.** The dream template already mitigates this by having the journals-sheep read both, but the asymmetry means Gru's *strategic-intent* layer (why the user ruled X) is thinner than Silas's *ops* layer for this window.
- **Actionable for Gru:** backfill at least ruling-level entries for 08-03..08-07 (the material exists in Silas's journal + `bin/ledger events`), or accept that Silas's journal is the system of record for ops and Gru's is for strategy — and keep the dual-read dream sheep pattern permanent.

---

*End of sheep-journals findings. Shard only — no live files touched.*
