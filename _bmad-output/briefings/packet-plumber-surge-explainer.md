# Briefing — packet-plumber-surge-explainer (lavish interactive explainer: surge drops, telegraph, player levers, UX gaps)

- **Job id:** `packet-plumber-surge-explainer`
- **Repo:** packet-plumber · **Base:** `v2` (READ-ONLY reference work — no product PR) · **Slug:** `pp-surge-explainer`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `lavish` (PRIMARY — the deliverable is a rich interactive HTML
  artifact reviewed in-browser by the user) + `gds-investigate` (forensic reading of
  the mechanics — evidence-graded, no guessing).
- **Perkins:** `pr_review: 0` — **no PR expected.** Deliverable: the lavish artifact.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders.
- **NO-PR COMPLETION SIGNAL (mandatory):** when done, run
  `herdr notification show "packet-plumber-surge-explainer" --body "<artifact path +
  one-line summary>"`. Then report to the bosses.

## Mission — build a LAVISH INTERACTIVE EXPLAINER for the user's screenshot questions

The user hit a confusing game state (screenshot:
`/Users/moses/Desktop/Screenshot 2026-08-15 at 10.04.24.png` — COPY it into the
artifact's assets; it is the case study) and asked, verbatim:

1. "why are there still drops, without the links congesting?"
2. "why do the buildings have circles and exclamation around them? what does that mean?"
3. "since what we control are routers and links — in this case how would we improve
   the situation as a player??"
4. "this needs to be visible to the player to see what's happening"
5. "the font is hard to read"
6. "i can't seem to be able to resize the window. prototype could"

Your artifact answers ALL SIX, with images + an interactive simulation, grounded in
the REAL code (cite file + line evidence per section — the gds-investigate standard).

### Section A — the mechanics, explained with an interactive simulation

Cover (from the code, all verifiable):
- **The surge:** the screenshot's `streaming_surge x10 -26s` weather report — the
  4.2 crisis set-piece; demand ×10 (core/demand.odin, crisis.odin).
- **Why drops without link congestion:** the two invisible chokepoints —
  **E22 pool exhaustion** (global in-flight pool cap at SPAWN time; ladder sheds the
  newest LOWEST-priority packet: BE → Standard → Express — core/flow.odin
  `flow_try_spawn`) and **node contention** (3.3 serialization at node throughput —
  packets resident + failing to forward). Links stay clean because the choke is
  upstream of the pipes.
- **Why email drops MORE than streaming (99% vs 95%):** priority ladder — email
  (lowest class) pays first. Show the ladder.
- **The rings + `!`/`!!`:** the 4.1 warning telegraph (app/render/view.odin
  `draw_health_ring`): amber ring + `!` slow pulse = strained (~30s lead); red +
  `!!` fast = critical (~10s). Node strain = Σ bandwidth of resident failing-forward
  packets ÷ throughput. Ring+glyph+pulse, never color alone.
- **THE SIMULATION (interactive, in-artifact):** a small JS/canvas sim where the user
  can crank a demand dial, watch the pool fill, see priority shedding hit email
  first, see nodes strain + rings light — the invisible mechanics made visible.
  Simple, deterministic, labeled. This is the centerpiece.

### Section B — the player's levers for THIS exact state (routers + links only)

Grounded in catalog/balance reality (read `core/catalog.odin`, `data/balance.json`,
tier tables): what ACTUALLY relieves the screenshot state? Cover, with numbers:
- Does adding a router / upgrading tier (mid 8 / high 16) raise throughput or pool
  headroom? Where does pool_max_packets come from?
- Parallel bundles + ECMP (2.1/2.2) as capacity levers; wide tiers.
- The 5.8 QoS panel + auto-reservation: protecting email's SLA (never-drop floors,
  E6) while streaming floods — the tool the screenshot player isn't using.
- Demolish/redraw (2.3) under pause (5.3) to re-architect mid-surge.
- Rank the moves: "if you're in THIS screenshot, do X first" — a concrete playbook
  with expected effect per move (cite the numbers that prove it).

### Section C — visibility design proposals (finding #4)

The user is right: pool exhaustion + spawn-time drops are INVISIBLE by design today.
Propose concrete HUD surfaces (with mock renders embedded — you can screenshot the
harness/goldens for base imagery): e.g. a pool-pressure gauge, drop-site markers at
spawn nodes, a "why dropped" breakdown line, ring tooltips. Keep proposals small +
canon-coherent (telegraph-not-hint doctrine; readability canon). These PROPOSALS are
for the user's verdict in review — do NOT implement in the game.

### Section D — UX findings (font + window resize)

- **Font:** v2 renders the raylib DEFAULT font (view.odin says so) — audit legibility
  (size, contrast on light canvas, letter spacing) vs the prototype's rendering
  (`/Users/moses/code/packet-plumber-prototype-ref` — check what it used). Propose a
  readable bitmap font + sizes (tied to the a11y canon, 7.3 adjacency).
- **Window resize:** VERIFY in code — v2's raylib window flags vs the prototype's
  (the prototype resized; find the ConfigFlags difference — likely
  FLAG_WINDOW_RESIZABLE + resize handling). Document the cost to restore (render
  scale handling, WIN_W/WIN_H constants — how deep does fixed-size go?).

Both are findings + proposals with evidence — implementation comes AFTER the user's
lavish verdict.

### Lavish protocol (load-bearing)

- Follow the `lavish` skill exactly: build the HTML artifact, serve it for in-browser
  review, the user annotates. The artifact IS the deliverable.
- Structure for skimming: visual TOC, section cards, images embedded (the user's
  screenshot + harness/goldens captures), the interactive sim inline.
- Everything plain + precise in the artifact (no persona) — but make it beautiful;
  this is a teaching document.

**Scope guard:** NO product code changes, no commits to v2, no game implementation.
Read-only investigation + the artifact. Asset copies + the artifact live under
`_bmad-output/implementation-artifacts/surge-explainer/`.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: pp-surge-explainer
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 0
```
