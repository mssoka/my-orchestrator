# Field notes — packet-plumber-v2-6.2-advance-trigger (r1 rework)

- The drift-check flip classes' temp-arena clobber (B2): a temp-allocated `lpath` held across `replay_hashes`' per-tick `free_all(context.temp_allocator)` reads garbage → `accepted=false` → a VACUOUS "rejected (OK)". Any future flip/divergence class must re-call `log_path(name)` at its site.
- `harness save <demo>` does NOT cover the input-parity T1s — `harness input-parity save` is a separate verb; a catalog_hash fold re-bless must include it or gate 10 fails on "catalog drift".
- GH CI has been billing-blocked ("recent account payments have failed... spending limit") since the 7.3 rounds — v2 merged the a11y T2 goldens (blessed with the WRONG palette state — remap not applied) and a stale QoS-era parity expectation, both never CI-verified; reproduced on pristine v2. The local container leg (`tools/ci-local.sh`) is the only working CI ground truth right now.
