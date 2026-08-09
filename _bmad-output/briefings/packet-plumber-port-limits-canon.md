# Briefing: packet-plumber-port-limits-canon

- **Repo:** Packet-Plumber (`/Users/moses/code/packet-plumber`, remote: `solarity-services/Packet-Plumber`)
- **Worktree:** WORKTREE off `main` (GDD on main; coordinate with the running Odin-architecture pass — this edits the GDD's MECHANICS section, the Odin pass's touch-up is a light header note, different region). PR targets main.
- **Workflow:** targeted canon amendment (GDD design mechanic). Perkins: OFF (docs/canon). Self-review: bmad-review-edge-case-hunter (verify the amendment is precise — adds the mechanic + provenance, re-litigates nothing).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** OFF.

## Mission

**Canonize the tier-scaled router port-limits mechanic in the GDD.** The experiment (prototype-iterate-1 #12) proved it FUN — the minion's fun-read called it "the strongest feature of the four; creates topology decisions without frustration; add it to the GDD/architecture." The user merged it (#12) + said **"canonize it."** The GDD is the engine-agnostic design canon — this mechanic belongs in it so BOTH the Godot prototype and the Odin architecture inherit it.

## The mechanic (add to the GDD)

**Tier-scaled router port limits:**
- A router/junction has a **finite port count** scaling with tier: **basic = 4 ports, mid = 8, high = 16** (matching the capacity-scaled router visual — more ports = bigger router).
- **One port per connected pipe.** You can't exceed the router's port count.
- **Ports are GENERIC** (no uplink-vs-user port-type distinction — the user ruled: pipe tier handles the bandwidth distinction; ports stay simple).
- **Design intent:** a clean, intuitive topology constraint ("this router has 4 ports, choose wisely") that forces meaningful routing decisions WITHOUT frustration — the experiment proved it fun.

**Placement:** the GDD's mechanics — fit it in **M3 (Topology & nodes, the junction/router section)** as a junction property (like the LB mode + throughput-tier), OR a dedicated short mechanic entry. Match the GDD's structure/voice.

**Provenance note:** add a dated canon note (2026-08-08): port-limits was a prototype experiment (#12) that proved FUN + was canonized by user ruling. NOT originally in the GDD/architecture (it was the user's proposal) — now canon.

## Constraints
- ONLY add the port-limits mechanic + the provenance note. Don't re-litigate anything else (the pipe tiers, QoS, eras, buildings, the Dispatcher — all locked).
- **Engine-agnostic** — this is a design mechanic (both Godot + Odin implement it). Don't tie it to any engine.
- Em-dashes fine (PP copy, not RT).
- Coordinate: the running Odin-architecture pass touches the GDD lightly (a header note re: engine-agnostic survival). Your edit is the M3 mechanics section — different region. If a conflict arises, the conflict sensor will catch it.

## Acceptance
- gdd.md amended: tier-scaled router port limits as a canon junction mechanic (basic 4 / mid 8 / high 16, one port per pipe, generic ports, design intent + provenance).
- Nothing else changed (scope-verified).
- After user approval (or direct — focused canon amendment the user explicitly requested): commit, push, open PR targeting main. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set packet-plumber-port-limits-canon working` at start
- `/Users/moses/code/bin/ledger set packet-plumber-port-limits-canon in-review "PR <url>"` when PR opens
- `herdr notification show "port-limits-canon" --body "<one-line>"` on finish
- Final message: the mechanic + where it landed in the GDD, confirmation scope was tight, PR URL.

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: packet-plumber-port-limits-canon · base: main
