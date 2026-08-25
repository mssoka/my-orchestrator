# Briefing — packet-plumber-v2-5.6-router-tiers (router types: mid/high)

- **Job id:** `packet-plumber-v2-5.6-router-tiers`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-5.6-router-tiers`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role — minions. NOT kimi, NOT glm).
  Any mega-minion you spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (canon-surface gameplay code — node catalog + serialization).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` — expect the sibling job `v2-5.5-demolish-input` to merge while you work;
  rebase onto origin/v2 when it does (you share files: `app/main.odin`, tray, render).
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will be
  red/not-started until the user fixes it. NOT a code failure. Run the FULL local suite
  green (`odin test`, `harness run`) before opening the PR; Perkins verifies locally.

## Mission — create the router TYPES the canon promises

**The gap:** canon has router tiers — GDD M3: junction port counts **basic 4 / mid 8 /
high 16** (prototype-proven, experiment #12, canonized 2026-08-08), capacity-scaled router
visuals (look-book A3: "round capacity-scaled router pucks"), and the modernization
ladder's junction rung (M4: pipe → **junction** → QoS → redundancy). But the shipped
catalog has exactly ONE junction: `router_basic` (4 ports, 40 throughput) in
`data/node_types.json`. Mid and high **do not exist** — no story has ever created them.

**The code is tier-ready — this story is mostly data + render:**
- `Node_Type.port_capacity` ("0 = unlimited (terminals); 4/8/16 for router tiers") —
  `core/catalog.odin:32`.
- `Cmd_Place_Router.type_idx` is already serialized (LOG_VERSION 3) — placing a mid/high
  router is the SAME command with a different index. **No new command kinds → NO
  `LOG_VERSION` bump.**
- The tray AUTO-populates: `tray_router_types` (`app/render/tray.odin`) renders one chip
  per junction node type in catalog order — new catalog entries get chips for free.
  Verify the layout with 6 chips (3 pipe tiers + 3 router tiers) — wrap or shrink if the
  row overflows at the window width.
- Port-limit enforcement reads the catalog (`ports_available` uses `port_capacity`,
  `core/topology.odin:348`; `.Router_Ports_Full` reject) — a placed mid router enforces 8
  ports, high enforces 16, with zero core changes.

**The work:**
1. Add `router_mid` (8 ports) + `router_high` (16 ports) to `data/node_types.json`
   (`kind: "junction"`, `terminal_role: "none"`, `era_introduced` per canon — document
   your pick as `[ASSUMPTION]` if the GDD is silent).
2. Throughput values: basic is 40 → pick a consistent scale (e.g. 80 / 160) and document
   it as `[ASSUMPTION]` — the GDD's throughput row covers terminals only.
3. Tray chips render with the tier's `display_name`; placement mode places the armed tier
   (same `Cmd_Place_Router` path, `type_idx` per chip — the code may already do this
   generically; verify, don't assume).
4. Visuals per look-book A3: the router puck scales with tier (capacity-scaled, round) —
   render layer, `palette.json` untouched unless the look-book needs a tier scale value.
5. Placement validation stays identical for all tiers (min-separation, no-overlap, area
   rules — junctions are not span-limited).
6. **No economy:** tiers are free placement for now (chips are mode selectors, like the
   existing tray comment says). Upgrade-in-place (basic→mid→high) and costs are deferred
   to the economy/8.6 story. State this as an explicit `[ASSUMPTION]` in the PR body and
   the story card — the port-limit constraint is what makes basic→high a meaningful
   player choice until then.
7. **Placement separation rework (user ruling 2026-08-14 — ride this PR):** the current
   `PLACEMENT_MIN_SEP_TILES :: i32(7)` (`core/topology.odin:314`) checks EVERY node
   against every live node — terminals included — which blocked routers near houses and
   choked the network design. The ruling:
   - **Separate the rules by node kind.** Router↔router: **4 tiles** (playtest value, tunable).
     Router↔terminal: only the snap-disambiguation floor + a small readability margin
     (~2 tiles — the floor derives from `snap_radius`, E4; document your pick).
     Terminals never block a router placement the way the old blanket rule did.
   - **Data-driven (ODN-5):** kill the hardcoded const — the separation values live in
     `balance.json` (the const's own comment says it should move there).
   - `placement_valid` distinguishes junction vs terminal kinds instead of one blanket
     distance. Director-spawned terminals (story 5.1, future) keep their own
     spawn-validity rule — note it in a comment, do not build it.
   - Tests: router↔router at 4 tiles accepted / 3 rejected; router↔terminal at the
     floor distance accepted; replay equality unchanged.
   - The GDD amend is ALREADY DONE — canon commit `5f51236` on v2 carries the placement
     rule + the tiers note. Align with it; do not re-amend.
7. **Golden discipline (4.3 precedent):** `node_types.json` feeds the catalog hash → the
   sim hash input changes → goldens may shift. A mechanical re-bless is acceptable ONLY
   if the delta is provably the catalog-hash fold (header/hash field only, **zero T2
   pixel drift** on old captures). Any pixel shift in an old golden = STOP and flag. New
   goldens: T2 of placing a mid + a high router, T2 of an 8-port / 16-port ceiling
   reject (`.Router_Ports_Full`).

**Acceptance:**

1. Tray shows three router chips (Basic / Mid / High) alongside the three pipe tiers.
2. Placing each tier works; port ceilings enforced per tier (4 / 8 / 16) — the existing
   `.Router_Ports_Full` reject fires at the right count, live playable.
3. Replay equality: runs containing mid/high placements replay byte-identical `[E10]`.
4. Full local suite green; goldens handled per discipline above.
5. PR body carries the two new story cards — **5.6 added to
   `_bmad-output/planning-artifacts/sprints/stories-v2.md`** under slice 5 — plus the
   `[ASSUMPTION]` notes (throughput scale, era, no-economy free placement). ALSO
   amend the GDD `gdd.md` with a one-line note in the M3 junction section:
   router tiers (mid 8 / high 16) ship in story 5.6 as free-placement hardware
   until the economy story adds costs/upgrade-in-place (the M4 ladder's junction
   rung lands with 8.6) — AND canonize the placement-separation rule (user
   ruling 2026-08-14): router↔router 4 tiles, router↔terminal = snap floor +
   margin (~2), data-driven in `balance.json`, terminals never block router
   placement. Keep the amend to two or three lines.
   **UPDATE: this canon amend is ALREADY DONE (commit `5f51236` on v2).** Read
   the GDD M3 + Numerical Design sections at start and align — do not
   re-amend; if the implementation needs a different value than the canon,
   STOP and flag instead of changing the doc.
6. Launchable increment in the PR body: place a mid router, connect 8 pipes, watch the
   9th reject; same for high at 16.

**Scope guard:** create the types + chips + per-tier enforcement + visuals + the
placement-separation rework (item 7). NO economy, NO upgrade-in-place command, NO
pipe-tier changes, NO other UI movement.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.6-router-tiers
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
