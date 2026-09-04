🔬 **Moses.** Dr. Quinn, at your service — aerospace-reject, puzzle devotee, and a man who has never met a system he didn't immediately want to put under glass. You can summon `bmad-help` at any time if you want a second opinion on me.

I've done my homework before knocking: the GDD's cost model, the span tables, the no-soft-lock escape doctrine, the forge locks, and the shipped `balance.json`. And Moses — I see exactly why you called. Let me show you the patient before we prescribe.

## The diagnosis

Your shipped v2 has a **one-sided difficulty ledger**. The *react* layer is beautifully burdened: congestion, QoS triage, crises, the health meter. But the *build* layer — the draw verb itself — is priced at zero. Routers: free. Pipes: free, any length the span cap allows, as many bundles as ports permit.

The consequence is structural, not cosmetic: **the only interesting question your topology asks today is "*where?*" — never "*whether?*" or "*which, at the expense of what?*"** Planning regret, build-order pressure, opportunity cost — those feelings live entirely in the build layer's price tag, and you've removed the price tag. Your instinct — "we shouldn't have unlimited routers and links" — is the correct diagnosis of a real hole, not a balance whim.

But here is the contradiction we must crack (TRIZ would insist I name it):

> **Scarcity must bind the builder without taxing the tinkerer.** The draw verb must stay fluid and joyful (FORGE #2 — this is NOT Factorio; no inventory spreadsheet), yet every draw must *cost something the player wanted elsewhere*. And the whole apparatus must stay asleep in Eras 1–2 (the discovery curve is sacred — that gentle diorama is where QoS gets *learned by consequence*, not crushed by budgets), while no-soft-lock survives intact ("always available, never free").

AHA — and there's the elegant part: **you already own the shape of the solution.** The load-shed escape is "always available, never free." Scarcity wants to be the same doctrine with its polarity flipped: drawing is always *possible*, never *free*.

## The map of the territory

The candidate mechanism families I see (GDD-sourced + genre-native), with my lean:

| # | Mechanism family | What it buys | Risk | My lean |
|---|---|---|---|---|
| **A** | **Budget/inventory — MM-style** (routers + pipe-length budget, refills on era advance / score milestones) | Genre-native (Mini Motorways' dots ARE this); scarcity without bookkeeping; one glance = readable | Refill pacing *is* the difficulty curve — tune wrong and it's either starvation or noise | ⭐ **Strong** — the genre's native grammar |
| **B** | **Priced draws** (GDD cost model: length × tier per pipe, port/junction costs) | Exact GDD canon; makes span and tier one combined decision | Nearest to an economy sim; heaviest UI surface; drifts toward FORGE #2's forbidden drudgery | Full-game material, not next |
| **C** | **Router count caps** (hard cap per era, grows with era) | Simplest possible scarcity; directly answers "unlimited routers" | Crude — a cap that binds is a wall, and walls make soft-lock-shaped shadows | Too blunt alone; fine as A's skeleton |
| **D** | **Legacy/maintenance decay** (GDD M1 upgrade lifecycle — old infra bleeds, must be modernized) | Makes the PAST a resource drain; powers era-suffocation (P4) | Punishes without a visual language yet; deep system | Later-era seasoning, not the lever |
| **E** | **Opportunity-cost soft scarcity** (land/right-of-way, placement separation as the scarce resource) | Zero new UI — the map itself is the budget | Weakest pain signal; players barely feel it | Already partially shipped (separation rules); ambient, not binding |

## The fork I put to you first

Before we design a single number — the **failure feeling**. Scarcity is an instrument; I want to know what song you're buying. When a player fails (or nearly fails) in the game you're imagining, which ache should throb?

1. **Planning regret** — "I sprawled cheap standard lines everywhere and now I can't afford the fiber where it matters." *(build-layer regret → points at A/B)*
2. **Build-order pressure** — "I spent my early budget on the wrong district and the surge caught me mid-rebuild." *(temporal pressure → points at A with refill pacing)*
3. **Economic triage beside QoS triage** — "I can afford the fat pipe OR the redundant loop, not both — same choice, hardware flavor." *(parallel decision space → points at B)*
4. **Modernization squeeze** — "my Era-1 web is now a liability, and upgrading it all costs more than I have." *(P4 suffocation → points at D)*

My lean, stated plainly: **1 and 2 together** — that's what Mini Motorways' budget actually produces, it rides the era ladder naturally (bigger refills = growing scarcity that never crushes the early diorama), and it leaves QoS as the *sole* occupant of the react layer instead of muddying it with currency.

Which ache — and feel free to say "a blend, weighted thus." I'll wait. 🔬