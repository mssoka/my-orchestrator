title:	[PLAYTEST-FUN] The health meter is a one-way drain — no recovery path makes every breach a countdown
state:	OPEN
author:	mssoka (MSS)
labels:	enhancement, playtest
comments:	0
assignees:	
projects:	
milestone:	
number:	124
--
## The moment
In every strategy run, once the meter starts draining it runs to 0 in **2.5–5.0 s** and never comes back. BALANCED (the intended-fun path) went from a healthy 100% network to **dead with zero packet drops**: first meter dip 42.5 s, dead 47.5 s.

## Evidence
- `core/health.odin`: the drain is one-way. The "gradual refill / never-lose guard" only re-arms `grace_left` after a healthy streak — **`meter_pct` itself has no recovery path** (only stops draining when breaches clear).
- Drain rate measured ~1%/tick once latched (100% → 0 in ~99 ticks; GREEDY died in 2.45 s once both classes breached — drain takes the max across breached classes).
- Health-win/lose asymmetry: the win condition (`win surge 90`) measures uptime over a 90 s window, but any single ~5 s ratio breach episode permanently scars the run toward loss; combined with the era-3 death clock (sibling issue) the meter is a countdown, not a resource.

## Why it deflates
A one-way meter converts every mistake into run-death, so mid-run experimentation is punished with a full restart. The classic "one more run" loop needs recoverable states — Mini Motorways' overload heals when you fix the cause, and that forgiveness is what makes its disasters fun.

## Proposal (tunable, not a rewrite)
Mirror the existing grace-refill machinery onto the meter: when no class has breached for `meter_refill_streak_ticks` (suggest ~200 ticks / 10 s), refill `meter_pct` at `meter_refill_per_tick` (suggest 0.25%/tick, capped at 100). Two new balance.json knobs; no new systems.
Expected effect: the fiber sprint can cost 40–60% meter and recover; death requires *sustained* failure; the sprint window from the sibling issue becomes a fight-back story instead of a countdown.

## Strategy-run context
pp-playtest-fun: all 8 scripted runs. Build sha: 61ea014.

