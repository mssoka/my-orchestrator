# packet-plumber-v2-estate-spawning

## Task

Replace random node spawn placement with estate-style clustering.
User ruling (2026-08-21 ~23:5xZ play session): nodes spinning up
randomly produce "not so great looking topology" — the user builds
proper access/distribution/core topologies when placement cooperates.
Wanted: most nodes spawn NEXT TO each other, like an estate; after
~5 nodes, go to a new area. Two acceptable shapes (minion picks the
simpler one that satisfies both acceptance maps):

- (a) STRICT ESTATE: a new node spawns adjacent to an existing
  cluster; when a cluster reaches the cap (default 5), seed a new
  area elsewhere.
- (b) EMERGENT: first node of a cluster may land anywhere, but
  subsequent spawns are weighted to grow existing clusters — the
  board ends up reading as distinct clustered sections even if
  early placement looked random.

Either way the end state is: distinct clusters on different sections
of the map, no lone-node scatter, room left for the player to wire
between them.

## Rules (hard)

1. READ THE CANON FIRST: the repo carries a spatial-lane canon
   (dream-2026-08-13, commits 2e3acab/8ece056 — check GDD/architecture
   docs in-repo for placement/lane rules). Do not violate it; if
   estate clustering tensions with it, flag in the PR rather than
   silently rewriting doctrine.
2. Named tunables, never magic numbers: cluster cap (default 5),
   new-area seed distance / spacing, adjacency radius (strict mode) or
   cluster-growth weight (emergent mode). The user fun-tests and will
   iterate on these.
3. Placement must not fight the player: don't spawn on top of
   existing wires/infrastructure; keep inter-cluster space for
   routing lanes (that's the point of estates).
4. Spawn TIMING (cadence) and node-type visual identity are OUT of
   scope — pace-tuning owns cadence, the design-audit owns looks.
   Spatial policy only.
5. No routing-semantics/serialization/LOG_VERSION changes.

## Acceptance

- Before/after spawn maps in the PR body (rendered captures or a
  coordinate dump) at identical simulation steps: before = scatter,
  after = distinct clusters, no lone nodes far from any cluster.
- Tunables exist with the defaults above; a one-line change moves the
  cap (show it in the PR body).
- Local test suite green; any spawn-related tests updated to the new
  policy (not deleted).
- pr_review: 1 (gameplay-surface).

## HOLD / release (dispatch mechanics)

- Spawn-code overlap with packet-plumber-v2-pace-tuning (in flight on
  its own branch): this job is HELD, PANELESS, until that PR MERGES.
- Release trigger = pace-tuning merge close-out → resolve the fresh
  v2 head, THEN dispatch (rebase not expected — fresh worktree from
  the new head).
- Row note must carry the named trigger at add time.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max. Mega-minions (if any): same.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-estate-spawning
- base: v2 (resolve fresh head at release)
- model: deepseek-v4-flash
- worktree: yes (at release)
- pr_review: 1
- blocked_by: packet-plumber-v2-pace-tuning (release = its merge
  close-out)
