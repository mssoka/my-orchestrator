# Briefing: packet-plumber-forge6-desktop-first-amend

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (isolate). PR targets main.
- **Workflow:** targeted canon amendment (forge doc). Perkins: OFF (docs/canon). Self-review: bmad-review-edge-case-hunter (verify scope — only the #6 amendment + provenance, nothing else re-litigated).
- **Model policy:** unset — pi default (or kimi if default resolves there).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

Amend the forge doc's **FORGE #6** to match the user's lavish ruling (Odin-architecture lavish, session ef5a2724, 2026-08-08): the launch is **DESKTOP-FIRST sequencing** (desktop first, mobile later), NOT the original "cross-platform same-game (Steam + mobile)" lock. This is a significant forge amendment — the forge is the foundational canon, and the doc must match the ruling.

## The file + the change

**File:** `_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md` (the forge output — FORGE #6 is the platform decision).

**Change FORGE #6** from (approximately):
> "Platform: Steam (controller + mouse) + mobile (touch) — the same game, cross-platform."

**to (the amended ruling):**
> "Platform: **DESKTOP-FIRST sequencing** — desktop (Steam, mouse + keyboard) first, mobile (touch) later. Amended from the original cross-platform same-game lock by user ruling (Odin-architecture lavish, 2026-08-08). The game is designed to be cross-platform-capable (the input model + layout support it), but the LAUNCH sequence is desktop-first; mobile is a follow-on, not a day-one requirement."

**Add a provenance note** (2026-08-08, user lavish ruling, session ef5a2724): FORGE #6 amended from "cross-platform same-game" to "desktop-first sequencing." Note this ripples to the go-to-market + the Odin prototype (desktop-first, mouse-only).

## Also check for ripples (don't rewrite, just note)
The forge #6 change affects: the go-to-market strategy section (free prototype → playtest → Steam page → full launch — was cross-platform), the Odin prototype (desktop-first, mouse-only — already applied). Note the ripples in the amendment (don't rewrite those sections — just flag that FORGE #6's sequencing now governs).

## Constraints
- ONLY the FORGE #6 amendment + the provenance note + the ripple flag. Do NOT re-litigate anything else (the other 7 forge decisions, the rejections, the MVP scope — all locked).
- Em-dashes fine (PP copy, not RT).

## Acceptance
- forged-idea.md amended: FORGE #6 = desktop-first sequencing + provenance note + ripple flag.
- Nothing else changed (scope-verified).
- After user approval (or direct — focused canon amendment matching the user's own ruling): commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-forge6-desktop-first-amend working` at start
- `/Users/moses/code/bin/ledger set packet-plumber-forge6-desktop-first-amend in-review "PR <url>"` when PR opens
- `herdr notification show "forge6-desktop-first" --body "<one-line>"` on finish
- Final message: the FORGE #6 amendment + where it landed, confirmation scope was tight, PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-forge6-desktop-first-amend · base: main
