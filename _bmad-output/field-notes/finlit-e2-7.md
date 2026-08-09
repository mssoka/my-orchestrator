# Field notes — finlit-e2-7 (touch-target rules, A29)

- Relative-path edit/write tools resolved to the MAIN checkout, not the worktree — one `git commit` ran with `cd /Users/moses/code/kids-finlit-game` and landed on local main (recovered via stash + branch move; ALWAYS use absolute worktree paths for file tools and git).
- Headless `push_input` routing: the root window is 64×64 while content space is 1280×1280 (stretch) — resize the window to the content size or routed taps never land; delivery is deferred one frame (assert a frame later).
- The leaderboard card's first layout pass sizes it ~8x tall from unwrapped labels — measure popup targets only after a bounded settle loop (rect stable across frames), never `await resized` alone.
