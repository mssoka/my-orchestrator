# Briefing: packet-plumber-light-cascade

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (main tree occupied by the prototype minion — isolate). PR targets main.
- **Workflow:** targeted canon amendments (the light-cascade). Perkins: OFF (docs). Self-review: bmad-review-edge-case-hunter (verify scope — only the light-cascade changes, nothing else re-litigated) + bmad-editorial-review-prose on the narrative reconciliation.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

The user's lavish A/B verdict (2026-08-08, PR #9 Blender-art) chose **LIGHT canvas (Mini Motorways daytime)**, superseding the "dark internet at night" direction. This ripples through THREE canon docs that assumed darkness. Amend all three so the canon is consistent end-to-end.

## The cascade (3 docs)

### 1. Forge #5 — dark backdrop → light
**File:** `_bmad-output/planning-artifacts/forge-packet-plumber-2026-08-05/forged-idea.md` (decision #5: "Mini Motorways style — 2D/isometric, clean, readable").
- The forge locked "dark backdrop, glowing pipes." Amend: the visual is now **light/daytime Mini Motorways canvas** (clean, readable, cheerful), NOT dark. Glowing elements still used for emphasis/packets but on a light canvas. Add an amendment note (2026-08-08: user A/B verdict chose light over dark).

### 2. Art-direction #7 — finalize palette→light + router = capacity-scaled infrastructure
**File:** `_bmad-output/planning-artifacts/art-direction/art-direction-v1.md` (amended once by #8).
- **Palette:** the #8 amendment left it "pending A/B." FINALIZE → **light/daytime canvas** (the A/B verdict). Drop the "dark internet at night" framing throughout. Glowing packet-flow still reads on light (use saturated packet colors + subtle glow, not bloom-on-black).
- **Router/junction:** SUPERSEDE the #8 "switching-substation building" decision. Routers are now **capacity-scaled infrastructure** (stylized switch/hub hardware that varies by tier — port-count/bulk/indicator-lights scale with capacity), distinct from terminals (buildings) and not boring-abstract. Parallels the pipe-tier visual language.
- Add an amendment note (2026-08-08: palette finalized light per A/B; router = capacity-scaled infrastructure per user).

### 3. Narrative #5 — reconcile the night/dark imagery to always-on/light
**File:** `_bmad-output/planning-artifacts/narrative/narrative-v1.md` (merged #5).
- The narrative assumed darkness: "internet at night," the Dispatcher's "3am control room," "Error 404 / the internet goes dark." In a LIGHT world these need reconciling. This is a **targeted reconciliation, NOT a full rewrite**:
  - **"internet at night"** → the internet is **always-on** (day + night); the fantasy is "keep it alive" regardless of time. Reframe, don't just delete.
  - **Dispatcher's "3am control room"** → an **always-on ops center** (no specific time); the weary-but-game veteran watching the world's traffic 24/7. The voice (dry-witty, urgent-warm) is UNAFFECTED — only the time/darkness setting changes.
  - **"the internet goes dark"** → "the internet goes **silent/down**" or "goes 404" (darkness not required). **"Error 404" stays** — it's a status code, not a light metaphor.
  - Keep the era beats, the satirical brands, the tone — only adjust the darkness-specific imagery.
- Add an amendment note (2026-08-08: reconciled night/dark imagery to always-on/light per the canvas verdict).

## Constraints
- ONLY the light-cascade changes + amendment notes. Do NOT re-litigate anything else (buildings for terminals, packet colors, pipe tiers, 6 eras, the Dispatcher's voice/personality, satirical brands — all LOCKED).
- The narrative reconciliation is targeted (adjust darkness imagery), not a voice/tone rewrite.
- Em-dashes fine in PP copy.
- The dark alt render (01a-vista-dark.png from PR #9) is RETAINED as reference — note it in the art-direction amendment (dark remains an option if light ever needs re-evaluating).

## Acceptance
- Forge #5, art-direction #7, narrative #5 all amended for light.
- Router = capacity-scaled infrastructure in art-direction.
- Amendment notes with provenance (2026-08-08, user A/B verdict).
- Nothing else changed (scope-verified).
- After user approval: commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-light-cascade working` at start
- `/Users/moses/code/bin/ledger set packet-plumber-light-cascade in-review "PR <url>"` when PR opens
- `herdr notification show "light-cascade" --body "<one-line>"` on finish
- Final message: the 3 amendments + where, the router decision, confirmation scope was tight, PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-light-cascade · base: main
