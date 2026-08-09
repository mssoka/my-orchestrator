# Field notes — finlit-architecture-v1 (2026-08-03)

- Mega-minion review swarms EARN their panes on big docs: the R1 swarm caught a schema that silently violated a locked pillar (KID-persists) and a sync-over-HTTP seam that wasn't buildable; R2 caught a defective rounding formula I'd written to fix R1 (the GDD's own $24→$2 tax example was the disproof) — budget an R2 pass, R1 fixes introduce their own bugs.
- HERDR_* env vars go STALE across Herdr restarts (mine pointed at a dead workspace) — always re-resolve with `herdr pane current --current` before splitting; layout JSON gives the real ids.
- Lavish end-session: poll returns queued rulings but the VERDICT may be absent even when the user is done — check `~/.lavish-axi/state.json` session (prompts/pending_prompts) as ground truth before deciding whether to ask for the verdict in-pane (it was absent → asked → approved).
