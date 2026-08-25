# packet-plumber-v2-3.5-node-placement — field notes

- Catalog edits are GOLDEN-POISONED in PP v2: `cat.hash` folds every catalog byte and `replay_hashes` rejects on drift — any node_type/balance.json change invalidates ALL blessed goldens. Wire new rules as core consts (ported values + comment) until a legitimate re-bless; port counts read from the existing `port_capacity` field.
- LOG_VERSION bumps (serialize.odin) force a golden-log re-bless — do it as `harness save` for ALL demos, then byte-verify every `.log.bin` differs ONLY in the version field (python diff vs `git show HEAD:`) and every `.t1`/`.png` is untouched; that diff IS the "don't re-bless without checking" proof.
- The harness's `capture_frame` passes a ZERO `Drag_State` — any new ghost gated on a plain `>= 0` int field (e.g. `placing`) draws in every T2 golden; gate on `drag.active && placing >= 0` and reset `placing = -1` in `start_run` (a `{}` struct reads as type 0).
