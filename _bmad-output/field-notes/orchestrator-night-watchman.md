# orchestrator-night-watchman — field notes

- **bmad-build render HALT on this install (upstream 6.11.0, not repo
  drift):** `ambiguous config value implementation_artifacts` (bmm + gds
  both define it; the fresh skill uses the `{{.implementation_artifacts}}`
  short-token). No in-repo fix exists (config.toml installer-managed;
  overrides still leave 2 matches). Waived by Silas ruling — briefings
  should avoid bmad-build until upstream fixes the template; carry the
  canon note in PR bodies.
- **launchd StartInterval jobs self-heal across a merge:** bootstrapping
  a plist whose ProgramArguments path doesn't exist yet just logs exit-78
  failures per tick and starts succeeding once the merge materializes the
  file — no plist edit, no re-bootstrap, no untracked-file hazard in the
  live tree (the git-overwrite refusal makes copying the script there a
  trap).
- **Agent liveness = herdr detection AND session-file existence; env
  correctness = extension marker grep:** herdr can report a stale idle
  agent with the session file gone (dead pi class 07-30) — only the file
  check catches it. And the silas/gru extensions only inject their
  "Silas/Gru startup checklist" text when the right PI_* env is set, so
  grepping the fresh session jsonl proves `PI_SILAS=1`/`PI_GRU=1`
  end-to-end without trusting any pane-side report.
