# Game Design Reference Videos

Curated design references for all game projects. These shaped key decisions across FinLit Street and Packet Plumber.

## Strategy & Commercial Viability

### [What Sells on Steam: You Don't Need a Hook — Jonas Tyroller](https://www.youtube.com/watch?v=uiBDyZ-Pf2M)

**Core thesis:** Players don't care about mechanics (hooks); they care about **experiences**. Start from the experience; the mechanics serve it.

**Four pillars of game dev success:**
1. **Fun** (keeping players) — relatively easy once you have skill
2. **Appeal** (gaining players) — HARD; the "I want THAT" reaction before playing
3. **Scope** (being efficient) — HARD; don't drag on for a decade
4. **Monetization** (paying rent) — straightforward; defer to end

**Appeal strategies:** start with a fantasy, iterate on proven formulas, find a market gap, translate successful media, design the trailer/capsule first, leverage tech advantage. Hooks work as a BONUS, not a standalone strategy.

**Applied to our projects:**
- FinLit: the experience is "start with nothing, build your street, watch it grow" — not "idle-lite economy builder with 4 asset classes"
- Packet Plumber: the experience is "save the internet" — not "routing puzzle with QoS prioritization"

**The capsule-art test:** show one screenshot. Does the player say "I want THAT"? If not, the appeal isn't there yet.

---

## Game Feel & Juice

### [The Trick To Instantly Make Your Game FUN — Thomas Brush](https://www.youtube.com/watch?v=U0a-IE5xawo)

**Core thesis:** Reactive = every input gets an instant, sensory answer. That IS game feel.

**Six juice lenses:**
1. **Measurement** — world sized precisely to the character (jump heights, grid units)
2. **Color theory** — palette + fog/bloom; lowest-hanging polish fruit
3. **Reactive sound** — every action gets an audio answer; 3-4 variants per recurring sound
4. **Animation curves** — gravity-shaped curves; weighty, not flat
5. **Reactive particles** — dust bursts, collectible bursts, celebration bursts
6. **Music & ambience** — the most-skipped, highest-value; never ship silence

**Applied to our projects:**
- FinLit: juice checklist banked at `_bmad-output/planning-artifacts/juice-checklist-game-feel-2026-08-03.md` (6 lenses mapped to FinLit mechanics)
- Packet Plumber: pipe-flow pulse, packet bounce on arrival, leak spray particles, router blink colors, crisis alert sounds
- Both: audio must be custom/original (no stock licenses) so streamers can monetize let's-plays

---

## Key Takeaways (cross-project)

| Principle | Source | Application |
|---|---|---|
| Start from the experience, not the mechanics | Tyroller | Every capsule art, every pitch, every prototype |
| Appeal + Scope are the hard problems | Tyroller | Audit sprint plans: which stories serve the experience? Which are scope bloat? |
| Every input gets a reaction | Brush | The juice checklist; "every pixel must react" (FinLit design anchor) |
| No stock audio — custom/original only | Brush (streamer monetization) | project-context.md rule for all game projects |
| Design the capsule/trailer before the game | Tyroller (strategy #6) | The prototype IS the trailer material |
