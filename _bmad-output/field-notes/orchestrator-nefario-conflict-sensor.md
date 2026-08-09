# orchestrator-nefario-conflict-sensor — field-note shard

- 2026-08-05 (orchestrator-nefario-conflict-sensor): Node 22
  `--experimental-strip-types` REJECTS constructor parameter properties
  (`private x: T` in a constructor signature) — "TypeScript parameter
  property is not supported in strip-only mode". Declare the field
  explicitly and assign in the body. (Same flag also can't run a file
  with non-erasable runtime enums/`const enum` — stick to plain const
  Sets like the extension already does.)
- 2026-08-05 (orchestrator-nefario-conflict-sensor): testing a pi
  extension that self-registers `setInterval` callbacks — each `start()`
  (a fresh `nefarioWatch(pi)` instance) pushes TWO callbacks (pane tick +
  PR tick). A per-scenario tick handle MUST be captured at start time;
  a fixed `callbacks[1]` index silently runs SCENARIO 1's closure against
  every other scenario's data (ticks stay silent, assertions pass by luck
  until a re-arm/re-fire case exposes it).
- 2026-08-05 (orchestrator-nefario-conflict-sensor): ESM relative imports
  resolve against the SCRIPT's directory, not `cwd` — a /tmp scratch
  importing a worktree `.ts` needs the absolute path; keep scratch files
  inside the worktree instead.
