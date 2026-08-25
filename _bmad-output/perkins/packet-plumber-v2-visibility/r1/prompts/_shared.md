You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

MANDATORY FIRST READS (in this order):
1. The canonical diff: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-visibility/r1/diff.patch — review EXACTLY these bytes. Never re-fetch or regenerate the diff (no `gh pr diff`, no `git diff`).
2. Project conventions: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1/project-context.md
3. The spec (the original job briefing — this is what the diff is meant to do): /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-visibility.md
4. Context: the implementation spec at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1/_bmad-output/implementation-artifacts/spec-v2-visibility.md and the PR body at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1/_pr_body.md

Your worktree (ALL verification reads happen here — a detached checkout at exactly the reviewed sha 857516479dbcc7116933417b37fe893d6ba89ad7): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-visibility-r1

--- ROUND-SPECIFIC GUARDS (from the review owner — these bound your lens) ---
- The ONE hard blocker is the determinism spine: T1 byte-identical, zero T2 shift. All five new surfaces must be app-layer in `draw_hud`, never in the harness capture path (the harness T2 capture calls only `draw_world` + `draw_forecast_panel` + `draw_health_meter` + `draw_crisis_banner` — never `draw_hud`). Any golden/T1/T2 change in this diff is a BLOCKER. No LOG_VERSION bump, no serialization change — a wire-format or version change is a BLOCKER.
- Verify specifically: (a) the "why-dropped" split always sums to the gauge's drop N (the 2.3 severed-cull drops an SLA drop with NO drop event and NO Drop_Site — the split must name that residual or it undercounts); (b) drop-site markers anchor on the canonical (lo,hi) node pair, not the renumbered bundle slot (bundle slots renumber on every topology change); (c) the claim that T2-invisible app-layer rendering was verified PROGRAMMATICALLY (scratch pixel-scan of gauge fill / SHEDDING tag / marker anchors), not eyeballed — check the PR body and spec for that evidence.
- Do NOT re-litigate: the 08-15 terminology rulings (congestion / drop precedence / lane-split — canon amendment is section-additive); the merged 5.2 node-health tri-state surface; the font-resize T2-fold discipline precedent; the post-rebase rename adoption hunks (state_strain -> state_congested — the terminology canon, already merged to base via #55).
- The GDD decision-log canon amendment is intentionally additive (legibility in-game is a design requirement; invisible chokepoints are defects) — verify it landed additively; it is not a defect.
