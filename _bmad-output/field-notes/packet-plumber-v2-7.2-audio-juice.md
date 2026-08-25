# Field notes — packet-plumber-v2-7.2-audio-juice (2026-08-17)

- Worktree-trap, THE expensive one: I did the whole job with file-tool paths +
  bash `cd`s at the MAIN checkout (`/Users/moses/code/packet-plumber`) despite
  starting with `pwd` in the worktree — the briefing's `repo_root` param reads
  like a work path. Recovery: `cp` the changed/new files byte-identical into
  the worktree (`cmp`-verified), rebuild + full CI there, `git checkout --` +
  `rm` in main. Pin the worktree path ONCE and use it for every cd AND every
  file-tool path.
- The harness CAN import `app/audio` (a raylib-importing app package): Odin
  DCEs the unused raudio procs, so the rlsw shadow (which builds NO raudio.o)
  links clean — no `build_raylib_sw.sh` change needed. Verified on macOS +
  the CI container (gate 4).
- Odin specifics that bit: relative imports resolve from the PACKAGE ROOT
  (app/audio needs `../../core`, not `../core`); constant arrays can't be
  indexed with a variable index (copy to a local first); `fmt.bprintf` returns
  a string VIEW (ideal for fixed-buffer captions); a constant f32→int cast
  that truncates is a compile error (precompute an int constant like
  `SYNTH_RAMP_SAMPLES = 110`).
