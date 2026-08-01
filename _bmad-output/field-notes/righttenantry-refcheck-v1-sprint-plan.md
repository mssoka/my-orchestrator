# Field notes: righttenantry-refcheck-v1-sprint-plan

- 2026-07-31: `lavish-axi poll` DOM snapshot exposed a Mermaid render failure my own eyes never saw ("Syntax error in text" — likely HTML entities like `&amp;` inside quoted labels). Read the dom_snapshot on poll return, not just the prompts; it's the only self-check of what the user actually saw.
- 2026-07-31: Feature-line sprint trackers sit beside the canonical `sprint-status.yaml` as `sprint-status-<slug>.yaml` in `_bmad-output/implementation-artifacts/` — bmad-sprint-planning's fixed `status_file` path needs overriding per the briefing, and story keys keep the epic prefix (`rc1-1-...`) to avoid canonical collisions.
- 2026-07-31: `_bmad/scripts/memlog.py` is per-worktree shared and append-only — it may already carry another job's entries; never prune them, just append with `--workspace . --text`.
