title:	[PLAYTEST-FUN] Era 3 arrival starts an ~17s unwinnable death clock — the surge is unreachable
state:	OPEN
author:	mssoka (MSS)
labels:	enhancement, playtest
comments:	0
assignees:	
projects:	
milestone:	
number:	118
--
## The moment
All four playtest strategy runs (RUSH / GREEDY / BALANCED / QoS-TRIAGE, scripted golden-harness demos, seed 2026, dublin board, box+health+advance-gate on) die **16.7–28.4 s after era 3 fires** — at ~47 s wall time, **12 s before the marquee streaming_surge x10 even opens at 60 s**. The surge was never reached in 8 runs.

## Evidence (per-tick stats, `--stats-out`)
- Era 3 arrival (first streaming demand): **t≈30.1 s** (healthy meshes advance fastest; GREEDY's weaker mesh: 34.8 s).
- Meter first dip: **41.9–42.6 s**; dead: **46.8–47.5 s**. First dip → death is only **2.5–5.0 s** of drain.
- Deaths happen with **zero packet drops** (BALANCED/QoS: 0 drops) — the breach is the windowed **delivery ratio**: at the freeze tick streaming had delivered 17/68 demanded (~25%), packets alive but stuck in multi-second queues (avg latency 4.7–6.5 s).
- Learned-run iteration: modernizing the host legs + bridges to **wide at 32 s** (2 s after era 3) still dies at the same tick — scores improve (39 vs 32) but the ratio breach has already latched the drain.
- Diagnostic: pre-era-3 wide conversion is **economically impossible** (fiber spool = 0 until era 3's box grant) — the player physically cannot have fiber before the threat exists. Wide transit is 1 tick vs standard 8 (post `packet_bandwidth 800` real-ladder), so pre-era-3 standard networks structurally cannot hold the streaming delivery ratio.
- GREEDY's near-empty mesh survived LONGER (28.4 s post-era-3) than healthy meshes — the advance gate rewards good play with earlier death.

## Why it deflates
The game's climax (the surge, the forecast panel, the crisis banner) sits behind a wall no era-1/2 play can climb. Every system that makes this game distinctive is never reached: QoS lanes, crisis naming, the surge win. "One more run" dies after two identical losses.

## Proposal (tunables, not a rewrite)
Any one of these reopens the middle game:
1. **Ramp era-3 streaming credit rate** over ~60 s (the 5.9 credit-gate already bounds per-terminal rates — add an era-3 entry ramp).
2. **Extend streaming `health_grace_ticks`** to cover a realistic modernize sprint (~45 s), so the first breach is survivable while the player converts to fiber.
3. **Forecast the era, not just the surge**: the weather report already counts down the surge with a 600-tick lead; give era-3's arrival the same treatment ("Streaming era approaching — fiber unlocks").
Expected effect: the surge becomes reachable; the tension curve gains its middle act; strategy differentiation (rush vs balanced vs greedy) becomes meaningful because survival stops being binary at t=47.

## Strategy-run context
pp-playtest-fun job, runs `fun_rush`/`fun_greedy`/`fun_balanced`/`fun_qos` (+v2 learned iterations, `fun_scout` growth run, `fun_cheat` diagnostic). Build sha: 61ea014. Perf note: none of the above is GPU-contention-tainted (sim-level stats, headless harness).

