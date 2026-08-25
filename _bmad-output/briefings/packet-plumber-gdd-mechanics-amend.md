# Briefing: packet-plumber-gdd-mechanics-amend

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`, base `main`).
- **Deliverable:** amend the canonical **GDD** to add six new mechanics (sourced from a game-mechanics inspiration pass), **integrated coherently** into the existing structure — NOT a separate doc, NOT a copy-paste dump. DOCS deliverable → **lavish review loop BEFORE the PR opens**.
- **Model:** `zai-coding-cn/glm-5.2` (kimi down; GDD amendment is capable-tier design-writing).
- **Perkins:** OFF (`pr_review=0`) — docs PR. Review surface = the lavish loop.
- **Skills:** **`gds-gdd`** (the GDD update workflow — read its step files) + **`lavish`** (REQUIRED — serve the amended GDD sections, foreground-poll, iterate before PR). Read the lavish playbooks first (`npx -y lavish-axi playbook <id>`).

## Mission

A "66 cool game mechanics" inspiration pass surfaced six mechanics worth **stealing into Packet Plumber**. The user has ratified **all six** — add them to the GDD as designed (full-game) mechanics, mapped to PP's existing systems, woven into the right sections so they read as part of the design (pillars / mechanics / progression / crisis / juice), not an appended list. The lavish review is the gate: the user signs off the integration before any PR.

## ⚠️ Integration principles (not a dump)
- Find each mechanic's **natural home** in the GDD (the section it belongs in) and write it there, in the GDD's voice + format.
- Ensure **no contradiction** with PP's core tenets: no-soft-locks, fair/readable crises, every-route-is-a-trade-off (P2), readable panic, "redesign is the game."
- Several of these **interact with the just-locked routing model** (per-hop forwarding + ECMP + **bundles** = parallel pipes pooled to summed capacity; redundancy = active capacity). Lean into that where relevant (e.g. the clutch + heatmap mechanics read naturally off bundles + severance-reroute).
- Mark scope: these are **full-game** mechanics; note where the current `[PROTO]` doesn't implement them yet (the prototype is BFS-based; full game is per-hop+ECMP+bundles per the canon — PR #18, may merge before/around this job).

## The six mechanics to add (source → PP mapping)

1. **Strain-heatmap persistence** ← *Lonely Mountain Snow Riders* (death leaves tracks in the snow; failure teaches the map).
   **PP:** persist a visual **strain trace** — pipes/junctions that dropped packets stay subtly marked, OR a **demand-vs-capacity heatmap overlay** — so repeated runs build a mental model and failure is educational, not punishing. Home: player-assistance / warning-surface / the inspect panel. Reinforces readable-panic + no-soft-lock.

2. **Bespoke per-scenario crisis thresholds** ← *Hades 2* (wave spawns at hand-tuned per-encounter thresholds — 50/70/90% — killing downtime, making breaks *relieving*).
   **PP:** the **demand director + crisis pacing is tuned by hand per scenario/era** for rhythm (tension peak → earned breath), NOT a flat difficulty curve. Home: the crisis/demand system (§M5 + the demand director). Each era's spikes get a bespoke rhythm.

3. **Failure teaches the specific counter** ← *Inscryption* (on death, craft a "death card" countering the exact thing that killed you).
   **PP:** at **Error 404**, a *specific* post-mortem — e.g. "the banking class failed at junction X; a bundle upgrade there or a redundant route via Y would've held it." Turns the loss screen into a lesson. Home: fail-state / Error 404 / player-assistance.

4. **Emergent clutch from constraints** ← *Ball Pit* (limited ammo + approaching enemies → fire-rate *emergently* accelerates into clutch moments the player feels but may not consciously see).
   **PP:** design the sim so **recovery compounds during peak crises** — one reroute unblocks a cascade → a visible, satisfying clutch. Lean on **severance-reroute + bundle dynamics** to *produce* those moments. Home: juice / crisis feel / cascade design.

5. **Costly always-available fallback** ← *Shroom & Gloom* (the "bash" card — opens any door, but costs health; prevents soft-locks + forces planning).
   **PP:** an **emergency escape with a cost** (e.g. an emergency overdrive / instant-reroute that burns a resource) — guarantees the no-soft-lock rule **but at a price**, so escapes stay tense instead of trivial. Home: the no-soft-lock rule / emergency mechanics. **Design the cost carefully so it doesn't trivialize crises.**

6. **Interconnected upgrades** ← *Spilled* (scoop/tank/speed upgrades interconnect — each makes the next desirable).
   **PP:** tune the **era-modernization ladder so upgrades compound** — bigger pipe → want a smarter junction → want QoS tuning. Make modernization a satisfying chain, not isolated unlocks. Home: progression / the era-modernization ladder.

## Source material (read)
1. **`_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md`** — the GDD you amend (pillars P1–P4, mechanics M1–M5, progression/eras, crises, juice, player-assistance).
2. **The just-locked routing model** (per-hop forwarding + ECMP + bundles) — now in canon via PR #18 (the GDD §M3/§M5 + arch amendments). Read the current GDD; if #18 has merged, its changes are in main. Several of the six mechanics interact with bundles/severance — write them consistent with that model.
3. **`docs/routing-explorer.html`** (in-repo, from the routing exploration) — context on the bundle/severance behavior the clutch + heatmap mechanics build on.

## Flow
1. Read the GDD + the routing-model context. Map each of the six mechanics to its natural GDD home.
2. **Integrate** them into the GDD (right sections, GDD voice/format, no tenet contradictions, bundle-consistent).
3. **Serve the amended sections via lavish**; foreground-poll for the user's annotations; iterate until they Send & End.
4. Only after lavish sign-off: commit, push, open PR targeting `main`. **Never merge.**
5. Badge out a field-note shard.

## ⚠️ Sequencing note (Silas manages)
PR #18 (the routing canon-amend, docs-only) is awaiting human merge and **also touches the GDD** (§M3/§M5). This job branches off `main` — if #18 merges first, branch off the updated main; if not, Silas rebases this job onto #18's merged state at PR time (the conflict sensor catches any §M5 overlap). Don't block on it.

## Acceptance
- All six mechanics integrated into the GDD (right homes, coherent, tenet-consistent, bundle-aware); full-game scope noted where the prototype doesn't yet do them.
- lavish sign-off captured before PR.
- No code changes (docs-only).

## Self-report
- `bin/ledger set packet-plumber-gdd-mechanics-amend working` at start (`clarifying` if you halt)
- `bin/ledger set packet-plumber-gdd-mechanics-amend in-review "PR <url>"` when PR opens
- `herdr notification show "gdd-mechanics-amend" --body "<one-line>"` on finish

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: gdd-mechanics-amend · base: main
- model: zai-coding-cn/glm-5.2 · pr_review: 0 · github_issue: (none)
