# Briefing: packet-plumber-art-direction-amend

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (the main tree is occupied by the prototype-build minion — must isolate). PR targets main.
- **Workflow:** quick targeted doc edit (canon amendment). Perkins: OFF (docs). Self-review: bmad-review-edge-case-hunter (verify the amendment is precise — only the 2 changes + a note, nothing else re-litigated).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

Amend the merged art-direction doc (PR #7) to reflect TWO user decisions made during the Blender-art render review (2026-08-08). The canon drifted from the user's intent; this corrects it so future work reads the right direction.

## The file
`_bmad-output/planning-artifacts/art-direction/art-direction-v1.md` (from PR #7, on main). Read it first to find the exact spots.

## The TWO amendments (ONLY these — everything else is locked, do NOT re-litigate)

### Amendment 1: Nodes = LITERAL BUILDINGS (reverses "abstract nodes")
The art-direction §3 ("What Packet Plumber adapts") + the node-identity section currently specify **abstract glowing nodes (rounded-rect/hexagon/octagon + role icon), NOT literal buildings**. The user reviewed the renders + OVERRODE this:
> "we need the buildings instead of boring shapes" / "it has to be beautiful art, not abstract shapes" / "we want to copy what we know works"

**Change:** nodes are now **LITERAL BUILDINGS** — Mini Motorways-style little houses/destinations, beautiful + representational + readable. Residential = a little house; Content host = a server/building; etc. Copy the proven MM building aesthetic. Keep the glowing treatment + role icons WITHIN the building forms (lit buildings, not bare shapes). Reverse every "abstract nodes, not literal buildings" statement in the doc.

### Amendment 2: Canvas palette = PENDING light/dark A/B (unlocks "dark internet at night")
The art-direction currently LOCKS the dark "internet at night" canvas. The user is **on the fence about light vs dark** — the Blender-art minion is rendering an A/B comparison (same scene, dark + light palettes) for the user to decide visually.
**Change:** mark the canvas-palette decision as **PENDING the A/B render verdict** (do NOT lock either light or dark — the user decides from the visuals). Note: dark is the current draft; light (MM-daytime) is the alternative under evaluation. Once the user picks, a follow-up amendment finalizes it.

### Amendment note (add to the doc)
Add a clear amendment block (dated 2026-08-08) at the top or in a decision-log section noting: (1) nodes reversed abstract→buildings per user render-review; (2) canvas palette pended pending the light/dark A/B; (3) everything else in the canon unchanged/locked. Cite the user quotes for provenance.

## Constraints
- ONLY the 2 amendments + the note. Do NOT touch anything else (packets blue/grey, pipe pulse/wear, 6 eras, the identity thesis, colorblind-safety — all LOCKED per user).
- Em-dashes are fine in PP copy (not RT).
- The amendment is a CORRECTION toward the user's intent, not a re-litigation of the forge (Mini Motorways style stays; buildings ARE MM style).

## Acceptance
- Art-direction doc amended: nodes = buildings; palette = pending A/B; amendment note added.
- Nothing else changed (diff = the 2 amendments + note only).
- After user approval (or direct if low-risk — it's a canon correction the user explicitly requested): commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-art-direction-amend working` at start
- `/Users/moses/code/bin/ledger set packet-plumber-art-direction-amend in-review "PR <url>"` when PR opens
- `herdr notification show "art-direction-amend" --body "<one-line>"` on finish
- Final message: the 2 amendments + where they landed, confirmation nothing else changed, PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-art-direction-amend · base: main
