Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (core sim vs app vs render vs harness)?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
- Key architectural contracts in this codebase: Command_Bus single authority validate→apply (topology_apply_edit), edit fast-path ODN-2, action log replay determinism E10 (arrays-only + seeded rng, no map iteration in core — lint-gated), catalogs JSON single source ODN-5 with cat.hash fold (ANY catalog field change shifts every golden), LOG_VERSION bump discipline. Check: does placement flow through the single authority? Is the tray rect math single-sourced between app hit-testing and render? Does the new const PLACEMENT_MIN_SEP_TILES (instead of balance.json) respect ODN-5 (documented rationale in the diff)? Is state duplicated (App.placing vs Drag_State.placing — sync hazards)? Are the new Edit_Error variants consistent with the existing error model?
