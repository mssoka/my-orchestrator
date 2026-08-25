# packet-plumber-v2-qos-default-standard

- The 5.8 lane-only demos/tests (sla, qos_contention, audio_throttle, lane_pipe_setup, test_congested_run) were stale relative to the app's auto-follow — with the 08-19 100%-Standard default they MUST write the ladder weights (Cmd_Set_Weights) or their scenarios silently sit at E7-floor rates; grep lane-only setups when any default-allocation change lands.
- E6 guard check (validate_set_lane) must judge the pipe's SETTLED weights (auto-follow result for auto pipes), not its current default — otherwise the first never-drop assignment can never engage the ladder.
- Golden re-bless proof: `harness fold-check <prev-catalog-hash> <prev-tick1>` mechanically proves a fold-only shift (boot); `cmp -l` on .log.bin old-vs-new (8 differing bytes at 17-24 = catalog_hash only) classifies fold-only vs behavioral per demo.
