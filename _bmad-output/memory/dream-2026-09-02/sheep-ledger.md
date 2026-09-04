# Sheep shard — sheep-ledger (dream-2026-09-02)

Source: `bin/ledger events 200` + `bin/ledger show` on the 5 window jobs.
Window: events >= 2026-08-31T22:13:41Z, dream-2026-09-02 rows excluded.
Live-store checks: read-only greps of `AGENTS.md` (line refs as of this pass).

## Candidates

- **NEW — `gh pr create` silently targets the repo default branch; PP minions must pin `--base v2`; recovery = `gh pr edit --base v2` (no rebase when the branch descends cleanly from origin/v2).**
  Example: pp-funfix-118-124, 2026-09-01T00:45:08Z — "minion opened the PR vs MAIN (gh pr create default) instead of v2 - permanently DIRTY against the wrong lane; FIXED by retargeting (gh pr edit --base v2), now OPEN+MERGEABLE v2<-7b109d3, no rebase needed (branch descends cleanly from 61ea014=origin/v2)". Silas then wrote the rule down in-row at 00:50:48Z: "standing rule: packet-plumber PRs always --base v2". The briefing gap: the base branch lived in dispatch context, not in a place the minion's `gh pr create` could inherit it.
  Proposed target: AGENTS.md gotcha (Dispatch & handover, or folded into the briefing-template line that names the base) + PP briefing template ("open with `gh pr create --base v2`").
  Already-recorded check: NOT recorded — grep `base v2|--base|gh pr create` across AGENTS.md + field-notes hits only an unrelated heredoc example (field-notes:270). First sighting of this class.

- **EXTENDS (line 1103) — self-created rows, 3rd sighting, NEW canonical-flip flavor + a root cause: the handover never pinned the row id.**
  Example: pp-funfix-118-124, 2026-09-01T00:08:38Z — "row self-registered by minion (dispatch add was missing)". The dispatch add was NOT missing: Silas' real row was `packet-plumber-funfix-118-124` (added 2026-08-31T23:54:13Z); the minion looked up the short id, found nothing, and self-created. The self-created row then carried the ENTIRE live lifecycle (pr → in-review → done-merged) while Silas' row "kept a stale working + pane pointer that fed the 07:38 watcher echo" (packet-plumber-funfix-118-124, 2026-09-01T07:43:09Z, reconciled per the 08-14 doctrine, canonical = the minion's row). Two new sub-facts: (a) self-created rows default `base=main` on a v2-lane repo (pp-funfix-118-124 shows base: main vs the dispatch row's base: v2) — the missing-fields flavor now includes a WRONG-lane base; (b) the durable fix is dispatch-side: name the canonical row id IN the handover so the minion's first `ledger show/set` lands on it.
  Proposed target: 2026-09-01 addendum on the line-1103 gotcha (canonical-flip + wrong-base-default + pin-row-id-in-handover).
  Already-recorded check: class recorded (1103, plus 08-17/08-19 addenda); all three sub-facts new.

- **CONFIRMS + extends (line 543) — stale model lines rot in HAND-AUTHORED briefings too, not just templates.**
  Example: packet-plumber-funfix-118-124, 2026-08-31T23:54:22Z — "MODEL NOTE: brief's deepseek line is stale (retired from ops 08-27) - dispatched on the standing ops tier glm-5.3-flash"; minion side corrected identically (pp-funfix-118-124, 2026-09-01T00:08:38Z — "model corrected to zai-coding-cn/glm-5.3-flash per Silas ops note"). The brief was authored 2026-08-31 naming deepseek ops four days after the 08-27 retirement. The dispatch-time correction layer (Silas overrides + flags in the dispatch note) worked as designed — no wrong-model launch resulted.
  Proposed target: one-line addendum to the line-543 gotcha (hand-authored lines rot too; correction-at-dispatch is the working safety net).
  Already-recorded check: template-rot recorded (543); the fresh-briefing flavor is new.

- **EXTENDS (line 893, the 2026-08-31 addendum) — the P5 self-notify checklist gate has SHIPPED and produced its first two compliant fires; "compliance gap is the DEFAULT" is no longer the observed state.**
  Examples: pp-funtest-r2, 2026-09-01T08:19:59Z — "Self-notify EXECUTED shown:true pasted (the P5 gate working)"; orchestrator-docs-p4-p5, 2026-08-31T23:45:14Z — "notification gate EXECUTED with shown:true pasted - the P5 pattern demonstrated in its own close-out". The gate itself shipped in PR #16 (orchestrator-docs-p4-p5, in-review, lavish-exempt small docs). Both window no-PR completions self-notified with pasted proof — 2/2 vs 0/3 the day before.
  Proposed target: 2026-09-01 addendum on the line-893 no-PR gotcha (P5 landed PR #16; first compliance ×2; keep Silas verify-and-fire until the trend holds).
  Already-recorded check: line 893 still reads "template hardening rides as a dream user-ack … Until it lands: Silas verify-and-fire … is the only reliable guard" — now superseded-in-part.

- **CONFIRMS (trigger graph + line 1132 + fun-test gate block ~1415-1440) — the fix-first-then-re-test verdict cycle closed END-TO-END for the first time; the held row's amendment lived entirely on the row note and fired on cue.**
  Example: pp-funtest-r2 — paneless HELD row added 2026-08-31T23:55:31Z with blocked_by=pp-funfix-118-124 and the full amendment in the note ("release trigger = the pp-funfix-118-124 PR MERGE … THE GATE METRIC = does era-3 become winnable-with-good-play AND health recoverable"); released 2026-09-01T07:39:59Z ("RELEASED per the trigger (funfix #125 merged, fresh head e50e9a8)"), done 08:19:59Z with the gate metric YES on both — "5/7 runs won the surge … RECOVERY RIDER run troughed 46% -> healed 100% -> won". Full arc this window: squad verdict 3.5/10 (08-31) → #118/#124 → fix PR #125 → Perkins r1 APPROVED → user merge → r2 re-test confirms both metrics + 3 new issues #126-#128.
  Proposed target: one-line 2026-09-01 addendum to the fun-test gate block (the 08-31 "fix-first-then-re-test" intent is now a completed cycle; gate metric defined up-front in the held-row note is the shape that worked).
  Already-recorded check: doctrine recorded; this is its first full completion, worth the dated confirmation.

- **CONFIRMS (line 949/955 flash-era Perkins block) with TWO new sub-flavors — pp-funfix-118-124-perkins-r1 hit the expected connection-class death, and the blind retry failed on a PROVIDER ERROR, compensated by line-by-line hunk verification.**
  Examples: 2026-09-01T01:05:25Z — "main died 4x errored turns (connection class - 6th today) ~8min in, 5/7 lens JSONs on disk … ONE continue revived it" (matches the ~1×/round budget, line 949; salvage worked). 2026-09-01T01:29:27Z — "6/7 lenses (blind degraded: length cap then provider error on retry; compensating line-by-line hunk verification disclosed)". New sub-flavors: (a) the single blind retry can fail on a provider error rather than a second truncation — still close 6/7 degraded-disclosed; (b) "line-by-line hunk verification" is a named, disclosed compensation technique for the missing blind lens (distinct from "diff covered by the remaining lenses"). Also confirmed on the same round: MEGA-DIFF on a corpus-re-bless delta (00:46:13Z — "MEGA-DIFF 93959L … corpus re-bless dominated" → "737L code chunk full lens; golden/PNG bulk mechanical") per the 08-29 fix-delta-mega addendum; and claims-mutation verification reached DOC surfaces — W4: "era3_surge_survivable header 'pre-fix this mesh died' false by mutation", W1: tuning-table measured-effect claim disproven (4-lens convergence + mutation proof).
  Proposed target: small 2026-09-01 addenda on the line-949/955 block (provider-error retry sub-flavor + hunk-verification compensation; mutation-checking demo headers / tuning tables extends bytes-not-claims to doc surfaces).
  Already-recorded check: parent classes recorded; the two sub-flavors and the doc-surface mutation checks are new.

- **MINOR NEW — Perkins close-out wrote an EMPTY review URL into the permanent ledger record.**
  Example: pp-funfix-118-124-perkins-r1, 2026-09-01T01:29:27Z — "r1 posted as formal review: . 6/7 lenses …" (URL missing entirely); the done note reads "review: posted-on-PR-125" with no anchor. The anchor is fetchable (`gh api … /reviews --jq '.[-1].id'` per the line-~1283 gotcha) but the durable record lost it. Sibling trivia on the minion row: identical double "pr:" note events at 00:39:16Z and 00:39:21Z (5s apart) — harmless double-write.
  Proposed target: one-line addendum to the never-guess-anchors gotcha (close-out notes must carry the FETCHED review id/URL; a placeholder is a record-loss, not caution).
  Already-recorded check: guess/truncation flavors recorded (1283 + 08-15 addendum); the empty-URL flavor is new.

- **CONFIRMATION ONLY — the lavish-exempt small-docs path + minion self-report hygiene ran clean.**
  Example: orchestrator-docs-p4-p5, 2026-08-31T23:43:42Z — "PR #16 open vs main … lavish-exempt small docs, user-ruled dream-2026-08-31", with "pr field set by minion" (23:45:14Z) — the NULL-pr self-report class did not recur this window, and the review-loop exemption (PR directly, no lavish) executed exactly as briefed.
  Proposed target: none (healthy-window note; supports no change).
  Already-recorded check: recorded (review-loop exemption; ledger guard P2).

---
In-window count: 34 material events across 5 jobs (orchestrator-docs-p4-p5, packet-plumber-funfix-118-124, pp-funfix-118-124, pp-funfix-118-124-perkins-r1, pp-funtest-r2) — plus 2 boundary events at the marker ts itself (dream-2026-08-31 close) and 2 excluded (dream-2026-09-02, this pass); 38 total at/after the marker.
