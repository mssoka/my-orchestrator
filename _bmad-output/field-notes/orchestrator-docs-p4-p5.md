# Field notes — orchestrator-docs-p4-p5 (2026-08-31)

- 2026-08-31 (orchestrator-docs-p4-p5): "already in managed-repos.txt" in a briefing can mean the ORCHESTRATOR ROOT'S LIVE TREE (uncommitted) — youtube-channel's adoption line was in /Users/moses/code/managed-repos.txt, NOT in the worktree's committed copy; verify the live checkout before treating it as a missing record, and phrase doc references as "recorded in managed-repos.txt" (not "committed").
- 2026-08-31 (orchestrator-docs-p4-p5): `herdr notification show` returns `{"id":"cli:notification:show","result":{"reason":"shown","shown":true,"type":"notification_show"}}` — the exact paste-shape for the new P5 self-notify checklist gate (playbook Minion standing orders); `shown:false` = relay busy → retry once, then escalate.
