# Dream report — 2026-09-04

Material: 8 shards (7 job shards + dream-2026-09-02's own, which landed
post-marker), 3 journal files mined (gru 09-04 full; silas 09-03 full;
silas 09-02 post-22:38Z entries) + 1 backfill check NEGATIVE (gru 09-01
tail — all pre-marker CHARGE/rig content, nothing undreamed), 132 ledger
events across 18 distinct jobs (independent count by sheep-ledger), since
2026-09-02T22:38:03Z.

Sheep: 3 (fieldnotes / journals / ledger), all zai-coding-cn/glm-5.3,
provenance verified (modelId=glm-5.3 ×3 in session jsonls), shards on
disk, panes closed.

The window: the **Packet Plumber 3D lane born and ran a full belt** (repo
birth → GDD → E1 slice → asset-scout lavish picks → E2 → art-integration,
6 Perkins rounds, 5 closed APPROVED), the **k3 weekly 7-day cap** knocked
kimi out (user: "we are out of kimi"), glm-5.3 proved as the full
reasoning fallback, one RT lane (rt-643 merged; prod-scale-to-zero's
post-merge FYI verdict caught a LIVE base-red), docs-p4-p5 merged.

## Proposals — AUTO (applied to store copies; mirrored to live per the
dispatch's apply-autos mandate)

### P1 — k3 WEEKLY 7-DAY CAP: fourth kimi cap flavor + "we are out of kimi" regime
- Target: `AGENTS.md` (Provider incidents, dated addendum) · Class: auto
- Change: new dated addendum — weekly cap is calendar-bound, continue =
  waste, only window reset/plan upgrade heals; user ruled NO upgrade;
  reasoning rides glm-5.3 probe-gated; policy durably at
  `_bmad-output/memory/quota-regime-policy.md`; glm-5.3 PROVEN full
  Perkins fallback (5 clean rounds, vision caveat enforced); E1
  precedent (user-play gate IS the look verdict); chatty-OK false-DOWN
  ×2 more (intermittent same-day; matcher hardening owed).
- Evidence: e1-r2 04:06:30Z ("kimi k3 WEEKLY 7-DAY CAP (403 … new
  incident class - not 1302/1308)"); user ruling e1 09:18:23Z ("we are
  out of kimi"); e2-r1 12:08:54Z ("probe returned DOWN x3 on chatty
  replies"); quota-regime.json shows glm-5.3 `ok:false` with error "OK —
  ready to help…" (the false-DOWN, live in the record).
- Reasoning: standing model regime until the window resets — every
  reasoning dispatch gates on it; the recovery recipe (sweep +
  regenerate on glm-5.3 + vision caveat) is proven 5×.

### P2 — Capability probes ≠ liveness probes (the thinking saga)
- Target: `AGENTS.md` (probe doctrine, dated addendum) · Class: auto
- Change: one trivial-prompt probe is never a capability verdict;
  long-lived session jsonls first; models.json `reasoning: true`
  registration gap made `--thinking max` a silent no-op (ZAI emits
  reasoning by default) — registration flags gate pi features like
  vision's `input` types; patch the flag, don't re-diagnose the provider.
- Evidence: gru 09-04 correction section ("Gru wrong, then right" —
  17×23 probe showed no thinking; session forensics showed thinking
  daily since 08-27; re-probe returned ['thinking','text']).
- Reasoning: prevents both a false capability verdict AND a false
  provider-blame; the models.json-flag class recurs (vision hit it
  08-21).

### P3 — Phantom checks + the EXPECTED_CHECKS triple
- Target: `AGENTS.md` (vacuous-pins gotcha, dated addendum) · Class: auto
- Change: the phantom-check flavor (test aborts, harness prints PASS);
  counting discipline (printed checks vs check() calls); `is int` abort
  guards useless on Godot 4.7.1; accepted fix = per-file EXPECTED_CHECKS
  pins + completion flag + final-line guard, copy-forwarded into every
  new PP3D epic harness; fix-audit mutation leg = abort-must-FAIL.
- Evidence: e2-r2 14:32:54Z (B1 "3/5 checks PHANTOM… dead null guard
  beneath"; B2 "PASS printed over the crashed test"); e2-r3 15:27:52Z
  (the gate "converts it to 'ran 23, expected 26' -> SUITE FAIL");
  silas 09-04 15:1xZ (the gate caught 4 files the flag-patch missed);
  e1-r1 03:11:01Z (dead-code separation floor, 13 overlapping hitboxes).
- Reasoning: dominant blocker class on homegrown harnesses; the fix
  standard is now proven to catch even the fixer's own misses.

### P4 — Post-merge FYI verdicts catch LIVE base-reds; ordered-click recovery
- Target: `AGENTS.md` (moot-on-merge gotcha, dated addendum) · Class: auto
- Change: FYI verdicts can find base-breaking defects (test pins + CI
  path-filter blindness); recovery = fix PR vs base → ordered user
  clicks → promote HELD until all-green; row holds open on the
  dependency; census ALL encodings of a value before flipping it.
- Evidence: rta-prod-scale-to-zero 11:59:15Z ("B1 REAL + LIVE — … suite
  RED on develop, showing RED on promote PR #177's checks") + 13:1xZ
  (fix #178, ordered clicks); cross-repo twin: tie-deconflict 08-25
  (a11y mode tables reintroduced a fixed collision).
- Reasoning: user pre-verdict merges are routine; the FYI round is the
  only safety net path-filtered CI can't provide — Silas: "the doctrine
  earned its keep."

### P5 — clear-pane ≠ pane close
- Target: `AGENTS.md` (close-out sweep gotcha, dated addendum) · Class: auto
- Change: one line — clear-pane NULLs the ledger pointer only; the pane
  needs explicit `herdr pane close`; startup reconciles catch survivors.
- Evidence: silas 09-03 midday cull (p6C/p6E survived done close-outs +
  lang-safety tab; "the 08-28 cull caught 2, today 3 more").
- Reasoning: names the mechanism behind the recurring pane-leak class.

### P6 — Stale herdr agent_session registry pointer
- Target: `AGENTS.md` (pane-forensics ground-truth bullet, addendum) ·
  Class: auto
- Change: the registry pointer rots while the pi lives; pane read is the
  functional probe; session greps use newest-mtime files containing the
  relay text, excluding your own session.
- Evidence: silas 09-04 00:2xZ ("pointer went STALE… pane read showed
  Gru processed the relay fine") + 12:3xZ ("grep must disambiguate
  files, newest-first, and never trust a single-file hit").
- Reasoning: delivery verification and liveness checks otherwise
  false-negative on long-lived panes.

### P7 — "Deferred" = a dispatched row; button-folds carry click steps; lavish halt gates for pick lanes
- Target: `AGENTS.md` (Dispatch & handover, dated addendum) · Class: auto
- Change: deferred work gets a ledger row at defer-time; a folded QoL
  shipping as a BUTTON carries its exact click steps in the relay;
  creative/pick lanes dispatch pr_review=0 + lavish HALT gate as the
  review (verdicts verified in ~/.lavish-axi/state.json).
- Evidence: gru 09-04 ("Miss owned: art integration never dispatched…
  'deferred' must mean a DISPATCHED follow-up row, not vibes"; the
  Regenerate-Preview click step never relayed → "no world");
  asset-scout 11:22:39Z ("SPEC LOCKED via lavish gate… Verdicts
  verified in state.json"), gdd-v1 (2 lavish rounds pre-PR),
  gdd-amend-levels (lavish gate in flight).
- Reasoning: 1 owned miss + ledger corroboration + the pick-gate shape
  ×3 lanes — the miss class is user-visible and cheap to kill.

### P8 — Field-note promotions (minion craft)
- Target: `docs/minion-field-notes.md` (dated entries) · Class: auto
  - Tooling traps: PP3D/Godot 4.7.1 block (editor surface class,
    screenshot-verify-pose, SceneTree lifecycle, fresh-clone --import,
    deficit credit, micro-traps); keywalled-API scouting fallbacks +
    bbox normalization; `ledger pr` before `set in-review` (2 crews
    same day); pi `edit` atomicity (re-grep after multi-edit).
  - Conventions: MEASURE, don't trust metadata or competing quotes
    (bbox + max_span cases).
  - Recurring review findings: PROVE THE RED (deliberate-fail probes +
    negative controls + abort-must-FAIL); GATE ON THE REAL OUTPUT
    SURFACE (palcheck/screenshot/probe, not predicates); A VALUE LIVES
    IN ≥2 PLACES (test pins + mode tables census before flips).
- Evidence: as quoted by sheep-fieldnotes candidates #1–#6 (each ≥2
  cross-lane sightings except the craft one-liners, promoted per
  shard-promotion precedent).
- Reasoning: the PP3D belt continues (gdd-amend, L1, art passes) —
  these are the next minions' first-day traps.

### P9 — The ledger guard's URL-in-note escape
- Target: `AGENTS.md` (ledger pr-field gotcha, one-clause addendum) ·
  Class: auto
- Change: the guard accepts a URL in the note, so the `pr` COLUMN can
  stay NULL under it (3rd+ sighting; 7/8 self-set this window) —
  `ledger pr` remains the only column-writer.
- Evidence: art-integration 23:09:39Z ("pr field was NULL on
  self-report… the guard passed on URL-in-note").

### P10 — Gates are deferrable; gate NOTES are a dispatch queue
- Target: `AGENTS.md` (fun-test gate block, dated addendum) · Class: auto
- Change: a user-play gate can be re-targeted to a later, richer
  artifact (E2 → 'level 1 playable', row waits, no re-dispatch) because
  the metric is up-front; PASSED-WITH-NOTES routes each note to a named
  fold/lane at verdict time.
- Evidence: e2 22:38:54Z ("GATE AMENDMENT… the L1 play session doubles
  as the E2 engine ruling"); e1 10:32:13Z ("PASSED-WITH-NOTES… Notes
  routed: editor-preview -> E2 fold; bigger world -> E3; art ->
  asset lane" — all 3 landed); fun-r2 09-01 (verdict → issues → fix
  lane, the 2nd sighting of verdict-routing).
- Reasoning: the gate canon's natural completion — deferral is free
  BECAUSE metrics are up-front; unrouted notes evaporate.

## Proposals — USER-ACK (staged; NOT applied)

### U1 — Dream template + close-out hardening
- Target: `_bmad-output/briefings/_template-dream.md` (playbook-adjacent)
- Change: (a) Silas close-out adds "PUSH the doc commit immediately"
  (dream-09-02's repair: 4 unpushed dream commits diverged main behind
  PR #16); (b) sheep-spawn line notes `herdr pane split` REQUIRES
  `--direction` and the JSON key `result.pane.pane_id` (dream-09-02
  shard: 3 "failed" splits, zero panes, RC masked by pipes); (c) briefs
  glob-resolve shard paths before handing to sheep (this dream's
  deconflect/deconflict typo was caught by the sheep, not the brief).
- Evidence: silas 09-02 23:0xZ; dream-2026-09-02.md shard; this pass.

### U2 — Playbook Model-policy/probe refresh (reference)
- The P1/P2 material (weekly-cap regime + capability-probe doctrine)
  belongs in the playbook's Model policy + probe sections — the
  standing `orchestrator-playbook-consolidation` row already scopes
  exactly this; no new dispatch needed, just carry these two into it.

### U3 — quota-probe matcher hardening (Silas tooling task)
- The strict `^OK$` matcher false-DOWNs on chatty coherent replies,
  third window running (08-20, 08-27, 09-04 ×2; intermittent
  same-day). The regime json currently records glm-5.3 as `ok:false`
  with error "OK — ready to help…". A content-aware matcher (coherent
  non-empty reply + no error code = UP) kills the class; until then
  every DOWN verdict needs a content read.

### U4 — PP3D Godot side-file policy (question for the user)
- User play sessions rewrite tracked `.import` files and generate
  `.uid`/`.png.import` side-files that collide with the next
  captures/assets merge (e2 close-out: aside-move → verify → drop;
  "they WILL collide future merges"). Silas flagged "longer-term maybe
  .gitignore policy ruling" — a user call, cheap to make now.

## Watch items (anecdotes — tracked, not proposed)

- **KYLE screening drove a spec deviation needing ratification**
  (art-integration: frozen spec said dithered-alpha; KYLE proved
  dither=TV-static at tube pixel sizes → fresnel shipped, disclosed +
  test-pinned; USER ratifies at merge). Vision-as-spec-amendment-driver
  — watch the ratification outcome.
- **Godot .import/.uid churn** — see U4; aside-move is the practiced
  fix meanwhile.
- **Stray-keystroke retirement** (silas 10:4xZ): delivery-verify
  auto-Enter RETIRED (read-only checks; "fragments = void, wait for
  full sentences") — recorded here so no future session reinstates the
  reflex.
- **Deleted remote staging base** (rta promote: staging branch restored
  at b657417) — check base liveness before cross-branch PRs.
- **Blind-lens FP trio on small view diffs** (rt-643: 3 rejected)
  — watch blind's FP rate on <400L diffs.
- **No-Perkins skip on test-only fix PRs** (#178 judgment call,
  documented) — sanctioned shape; watch for scope creep of the
  exemption.
- **Mid-session model flip flash→k3** (gdd-v1, doc-authoring upgrade,
  row noted, benign) — provenance stays per-pane at verdict time.
- **gdd-amend briefing pipeline**: grep-after-generate gate caught a
  sed-fragment briefing (art r1 23:2xZ) — keep the marker-count gate
  on every machine-derived briefing; add-then-update ledger order
  (rta r1 12:4xZ).
- **rt-643 mandate-verification style** (per-mandate PASS lines in the
  verdict) — good small-feature review shape, single sighting.
- **h3 lane parked on the Metal-pivot ruling** (documented hold) —
  don't let it sit past the next pivot conversation.
- **Fast user merges** (PR #1 ~5min; #4 ~40min post-approval) — keep
  gates/rows ready before escalation goes out.

## Pruned / rejected candidates (with why)

- **1302 census+one-continue, connection-class ~1×/round** — already
  canon (08-19 concentration, 08-27 wait-then-nudge, 08-29 g); this
  window only confirmed it (e2-r3, art-r1, rt-643-r1). No new facet.
- **Same-sha APPROVED stale echo / loop-terminal-on-approve** — the
  08-17 "only a NEW sha earns a round" doctrine already covers it;
  4 more note-only sightings, zero new rule.
- **Unstable-target hold/release** — textbook execution of the 08-11
  doctrine (e1-r1); nothing to add.
- **Chunked mega-diff protocol** — canon since 08-27; the new facet
  (cross-wave corroboration: tests lens flagged the same blocker in
  BOTH waves) is nice-to-have, folded into the report narrative only.
- **Dream sheep must read the ledger DB** — already the dream
  procedure (mandated ledger sheep); the 09-02 shard's confirmation
  adds no rule.
- **PP3D engine-choice / tiny-planet ruling** — project history, not
  an operational pattern; lives in the GDD decision log where it
  belongs.
- **Shared-Blender / RT-bootstrap repo facts** — repo-specific craft,
  already carried in the shards + briefings that need them.

## Application status

Store copies edited (AGENTS.md +9 dated addenda; minion-field-notes.md
+3 section blocks). Per the dispatch's apply-autos mandate, the same
diffs were mirrored to the LIVE files (byte-identical, verified by
diff against the store copies) and the marker written at completion;
the commit/push stays with Silas per close-out convention — **commit +
PUSH immediately** (U1's lesson).
