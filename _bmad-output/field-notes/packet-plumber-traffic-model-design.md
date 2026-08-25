# Field notes — packet-plumber-traffic-model-design (2026-08-15/16)

- Source material can live as UNTRACKED files in the MAIN checkout (surge-explainer/ was untracked in /Users/moses/code/packet-plumber, absent from the worktree) — find untracked briefing sources there, not in the worktree.
- The GDD M1 tier table (narrow 10/standard 25/wide 50/backbone 120) is STALE vs the shipped catalogs (5/15/40) — design specs must cite the shipped data/*.json as ground truth and flag the drift (the terminology audit owns the GDD-table refresh).
- Design tension surfaced late: per-terminal caps + era-3 demand/×10 surge → the MVP surge can silently stop landing on 4–6-node maps; the fix is per-type caps (content_host caps vs its own throughput, not the residential cap) + re-validating era-3 demand with 5.1 growth pacing — put such consequences in the artifact's Risks, never hidden in the spec.
