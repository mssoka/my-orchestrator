# orchestrator-vision-tooling — field notes

- 2026-08-22: glm-4.6v needs NO ~/.pi/agent/models.json entry — the
  auto-fetched models-store.json catalog already declares
  `input: ["text","image"]` and the E2E proved the attachment passes
  (model_change modelId=glm-4.6v + image/png part + stopReason stop);
  only add a user-level override when a target model genuinely lacks the
  declaration.
- 2026-08-22: a `--no-session` run writes NO session jsonl — for a
  provenance check run without it; pin the session by its exact prompt or
  file-attachment TEXT PART, never by grepping the model name (the
  AGENTS.md canon puts "glm-4.6v" into EVERY session's context).
- 2026-08-22: ~/.pi/agent/skills/vision-read symlink is MISSING
  (pre-existing — every other skill is symlinked there); the skill ships
  repo-only at .agents/skills/vision-read and agents in other cwds may
  not resolve it. Flagged in PR; the role-skills job owns skill wiring.
