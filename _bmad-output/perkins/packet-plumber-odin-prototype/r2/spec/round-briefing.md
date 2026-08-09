# Perkins briefing — round 2 (fix-audit): packet-plumber-odin-prototype

- **PR:** https://github.com/solarity-services/Packet-Plumber/pull/17 (targets `main`)
- **Reviewed sha:** `ea678a8acc2ae60b51b96ae56ca186e2f39ef185` (the FRESHEST head — NOT the r1's 0118cc0)
- **repo_root:** `/Users/moses/code/packet-plumber`
- **Round:** 2 of 3 (FIX-AUDIT — verify the r1 fixes + find new issues)
- **Your cwd:** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-odin-prototype-r2` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/packet-plumber-odin-prototype.md` + `_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (THE canon spec — determinism-native) + the GDD.
- **prior_findings:** the r1's consolidated findings at `/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r1/consolidated.json`. The r1 verdict was **CHANGES_REQUESTED** (2 blockers + 20 warnings + 34 notes) on sha `0118cc0`. **Your job: audit each r1 finding — fixed? still open? — then find NEW issues in the code that landed since (the head is now `ea678a8`, 10+ commits ahead).**
- **Owner (for `bin/perkins-token`):** `solarity-services`

## The r1 findings to audit (sha 0118cc0 → now ea678a8)

The minion has pushed 10+ commits since the r1. **Audit each r1 finding's status:**

**Blockers (2):**
- **B1 — committed `app.bin` (2MB Mach-O build artifact).** r1 said: `git rm --cached app.bin` + add to `.gitignore`. **AUDIT: is app.bin now untracked (.gitignore'd) or still committed?** (The commits don't obviously address this — verify.)
- **B2 — left-click DEMOLISH is UI-dead** (`handle_click_select` gated on `drag.active`; pipes unselectable, popovers undismissable, demolish unreachable; full routers soft-lock). r1 said: run `handle_click_select` on every left release regardless of `drag.active`. **AUDIT: is demolish now reachable? can you select a pipe / dismiss a popover / demolish?** (The commits don't obviously address this — verify. This is a GAMEPLAY blocker.)

**Warnings the minion appears to have addressed (verify the fix is CORRECT, not just present):**
- **W4/W5** — node-health + queue-overflow test coverage (the Godot r1 "node_health_states untested" lesson). Commit `ea678a8` "test: pin node-health transitions + queue-overflow shedding". **AUDIT: are the new tests REAL (pin the behavior, not tautologies)?**
- **W7** — `context.allocator` left as the run arena after `core.step()` (pollution + leaks). Commit `6b84abc` "allocator ownership". **AUDIT: is the arena save/restore correct? the snapshot allocator param actually used?**
- **W8 / the MSAA crash** — fixed (the A/B playtesting found + fixed these).

**Warnings likely still open (verify + re-flag if so):**
- **W1** — T1 fingerprint omits `Health_Meter.in_breach` + `.healthy_streak` (completeness gap). **AUDIT: are these fields now in the T1 hash?** (Relates to the catalog drift the minion re-blessed for.)
- **W2/W3** — vacuous/can't-distinguish tests (E7 WRR-floor, severance-reroute). **AUDIT: fixed or still vacuous?**
- **W6** — router triage popover labels swapped ("stream" button sets triage=email). **AUDIT: labels fixed?**

**The determinism spine (THE hard blocker) — VERIFY it now holds CROSS-PLATFORM:**
The r1 verified the determinism at `0118cc0` (3250 ticks bit-for-bit). Since then the minion fixed the **T2 cross-platform pixel mismatch** (`c052208` — `-ffp-contract=off` on the rlsw build; FMA contraction was rounding differently per-platform → pixel drift). **AUDIT: run the harness on your worktree — do the T1 state-hash + T2 pixel goldens now match bit-exact? Is the `-ffp-contract=off` fix correct + complete (no other float-contraction paths)? The CI is GREEN on both macOS + ubuntu at `ea678a8` — confirm the determinism holds.**

## NEW code to review (landed since the r1)

- **`0b92fa4` — Mini-Motorways hardware inventory replaces the budget** (a USER RULING from the A/B). This is a significant gameplay-system change. Review it for correctness (the inventory system, the port/budget semantics) — but **do NOT re-litigate the ruling itself** (the user ruled the budget → hardware inventory; it's the design now).
- The crash fixes (`650683d` hint-buffer, `6b84abc` allocator ownership, `2d99afd` MSAA drop + soak mode) — verify they're correct (the r1 noted some were already landing).

## ⚠️ CRITICAL lens-guard (read before any lens)

- **The determinism spine is the ONE hard blocker.** A seeded run MUST reproduce byte-identical state-hash (T1) + pixel (T2) goldens, cross-platform. If it's compromised, that's a blocker. (The r1 verified it; the T2 cross-platform fix landed — re-verify.)
- **Do NOT re-litigate the USER RULINGS** — the Mini-Motorways hardware inventory replacing the budget (`0b92fa4`), the desktop-first launch, the mouse-only prototype, the root layout — these are user decisions from the A/B, NOT defects. Review their CORRECTNESS, not their existence.
- **Do NOT re-litigate the Godot #11 findings.** The Odin prototype was built to APPLY those lessons (e.g., the field-wise canonical serialization, never raw bytes). Verify the lessons hold; don't re-raise the Godot bugs.
- **Prototype-rigor, not production-grade.** Don't flag missing full-game features (the era tree, leaderboards, mobile, save system) — this is the early A/B prototype.
- **Do NOT flag the choice of Odin/Raylib.** The Odin pivot is the user's ruling.

### Legitimate findings here would be
- **B1/B2 still open** (app.bin still committed; demolish still UI-dead) — re-flag as blockers (the audit's job).
- **A warning's fix is INCORRECT** (e.g., the W4/W5 tests are still tautological; the W7 arena fix has a new leak; the W1 T1 fingerprint still incomplete).
- **The determinism spine regressed** (the T2 cross-platform fix broke something; a new float-contraction path; the T1 hash drifted).
- **A NEW bug in the hardware inventory feature** (the inventory system, the port/budget semantics).
- **A NEW crash** (the A/B playtesting might have found more).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 17 --repo solarity-services/Packet-Plumber` → `/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2/diff.patch`. (LARGE diff — the full prototype + the A/B iterations. Headless mode handles big-diff chunking.)
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the Odin architecture + the GDD, `out_dir` = `/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2`, `prior_findings` = the r1's consolidated.json. Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r2`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 17 --repo solarity-services/Packet-Plumber --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 17 --repo solarity-services/Packet-Plumber --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 2 of 3 (fix-audit)
  **Job:** packet-plumber-odin-prototype · **Reviewed sha:** ea678a8 (r1 was 0118cc0) · **Reviewers:** <x>/7 completed
  **r1 audit:** <n>/<m> findings fixed — <k> still open
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive
  ### Blockers (<n>) / ### Warnings (<n>) / ### Notes (<n>)
  ```
- Close out: `bin/ledger note <your-round-row> "verdict ..."` (Silas owns the row status); remove your worktree; close lens panes. Final message: verdict + the r1-audit summary (fixed/still-open counts) + the report path.
