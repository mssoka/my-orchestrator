## 🤖 Perkins follow-up finding (post-review, owner ruling)

**Finding 47 — warning · topology-model:** terminal-to-terminal pipes are legal; houses can be connected directly to each other, bypassing the router.

- **Ruling (game owner):** houses don't connect to each other. This is a network-engineer game — locations (terminals) attach to the network (junctions), never to each other. Traffic between houses flows *through* the network.
- **What the code does today:** `_validate_draw` (topology_graph.gd) rejects self-loops, missing nodes, unknown tiers, span overflow, and over-budget — but has **no node-kind check** (`NetNode.is_terminal()` exists; draw never consults it). The map geometry makes some house-to-house draws legal (res(8,5)→res(8,14) = 9 tiles ≤ narrow max_span 10), and BFS routing (`_node_path`) will happily route email (the residential→residential MVP demand pair) through a direct house pipe in 1 hop — the router and its QoS lanes become bypassable.
- **Impact:** the fun-test loop is unaffected (the demo network and sensible play route through the router), but the topology model's core rule is unenforced — and it's also unwritten (GDD M3 / architecture §6.1 / edge contracts E1–E25 never pin it).
- **Fix:** reject `DrawPipeCmd` when both endpoints are terminals (`EditResult.rejected(&"terminal_to_terminal")`), and pin the rule as a new edge contract with a regression test.

Full record: `/Users/moses/code/_bmad-output/perkins/packet-plumber-prototype-build/r1/consolidated.json` (now 47 findings).
