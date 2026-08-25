# Briefing — righttenantry-refcheck-bughunt2 (round 2 exploratory bug hunt over reference_checks)

- **Job id:** `righttenantry-refcheck-bughunt2`
- **Repo:** RightTenantry · **Base:** `develop` @ 7675c81 (post-#620) · **Slug:** `rt-refcheck-bughunt2`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** the repo's bug-hunt skill (`.pi/skills/bug-hunt/SKILL.md` + its
  `guides/`) for the hunt itself; `bmad-quick-dev` for investigate/run workflow only.
- **Perkins:** `pr_review: 0` — **no PR expected.** Deliverables: issues filed +
  hunt report + runlog + the preserved scenario suite. No product code changes.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start (the
  stacked-forms + timing-gate lessons are load-bearing); badge-out your field-notes
  shard per standing orders.
- **NO-PR COMPLETION SIGNAL (mandatory):** no watcher tracks a no-PR job. When done,
  run `herdr notification show "righttenantry-refcheck-bughunt2" --body "<one-line
  result: N scenarios driven, M issues filed (#ids)>"`. Then report to the bosses.
- **Base:** `develop` @ 7675c81. The repo is otherwise quiet — no sibling contention.

## Mission — bug-hunt ROUND 2 over reference_checks, on the now-clean develop

Round 1 (this morning) found #611/#612/#613/#615 — all fixed, merged, and
verification-verified on develop @ ce999eb. The em-dash + metadata lines have also
shipped. **Round 2's value is NEW bugs** — the known prey is gone; anything you find
now is a genuine survivor.

### Phase 1 — rebuild the scenario suite, run it as a regression gate

The `reference_checks` scenario suite has been swept TWICE with its worktrees — only
the spec survives. Re-create it (third time, so do it right):

- Source: `.pi/skills/bug-hunt/SKILL.md` + `guides/scenario-format.md`, plus the
  re-creation spec in `/Users/moses/code/_bmad-output/implementation-artifacts/
  refcheck-verification-rerun-report.md` (§Scenario suite re-application — 5 scenarios:
  `panel-renders`, `panel-correct`, `panel-substitute`, `panel-export`,
  `referee-form-complete`).
- Apply the field-notes lessons verbatim: every click/fill scoped to
  `[data-question][data-current="true"]` (stacked-forms trap); timing gates before
  submits; reload-don't-retry on flake; the fixture protocol from the report.
- Run all 5 scenarios. **A failure here is a REGRESSION** (these all passed at
  ce999eb) — highest-priority finding, file immediately with before/after evidence.

### Phase 2 — EXPAND the hunt (round 2's real purpose)

Beyond the five, author NEW scenarios probing what round 1 never touched. Draw from
the feature surface (form pages, consent, lookup/messages/result/fraud, webhooks,
sweep, landlord panel, attempt log, row actions, export/notifications). Candidate
axes — pick and add your own:

- **Referee-side edge cases:** invalid/expired tokens, re-submit after completion,
  back-button mid-form, consent declined then re-attempted.
- **Panel edge cases:** empty states, very long names/notes, unicode + emoji in
  inputs, rapid repeated row-actions (double-submit), export with zero + huge logs.
- **Timing/state:** sweep running while a landlord edits; notification triggers at
  boundaries; session expiry mid-flow.
- **Layout:** narrow widths (mobile-class), keyboard-only navigation through the
  edit-trio + row actions, screen-reader labels on new surfaces ("Viewing held").
- **Copy consistency:** the new #619 metadata live on the SSR pages; the "Viewing
  held" pill on detail pages (advisory W1 from 618-r1 is UNPINNED — if you see the
  old label anywhere, that's a find).

### Filing rules

1. NEW issues only: labels `bug`, `bug-hunt`, `priority:<sev>`,
   `scenario:reference_checks/<name>` where applicable. Evidence: DOM geometry +
   screenshots (the PNG pattern in `refcheck-verification-rerun-evidence/` is the
   house style). Severity honestly: priority:high only for data-loss/consent/
   money-adjacent.
2. Do NOT re-file #611/#612/#613/#615 (fixed + verified) unless you have REGRESSION
   evidence on current develop — then it's urgent, say so loudly.
3. Known-open and OUT of this hunt's scope: #617/#568 (analytics attribution),
   #587 (auto-reminder feature), #549/#529 (content). If a scenario brushes them,
   note in the report — don't file duplicates.
4. Suite-artifact bugs you find in your OWN scenarios: fix the scenario, note it in
   the runlog (round-1 convention — 2 such fixes were normal).

### Phase 3 — durability (fixes the twice-swept-suite waste)

At wrap, COPY the finished suite + fixtures to:
`/Users/moses/code/_bmad-output/implementation-artifacts/bug-hunt-suites/reference_checks/`
so round 3 starts from a preserved suite, not a re-creation.

### Interactive protocol (load-bearing)

The user may drop into your pane at any moment and drive — when he chats with you,
you speak minion (light, eager, facts unburred). His word overrides this plan
mid-hunt. Say what you're about to run and what it proves before each stage; show
results after. Ask before anything destructive (db reset, port kill, fixture wipes).

**Scope guard:** testing + issue-filing + scenario authoring ONLY. No product code
changes, no commits to `develop`, no fixes for bugs you find (file them — the bosses
decide). Worktree-local test artifacts are fair game.

**Wrap deliverables:** hunt report (scenarios driven, PASS/FAIL, issues filed with
ids, smells + untested gaps) + runlog into
`_bmad-output/implementation-artifacts/` (`refcheck-bughunt2-report.md`,
`refcheck-bughunt2-runlog.md`), suite preserved per Phase 3, notification fired.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: rt-refcheck-bughunt2
base: develop
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 0
```
