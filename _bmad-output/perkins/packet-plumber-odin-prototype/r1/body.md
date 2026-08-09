## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-odin-prototype · **Reviewed sha:** `0118cc0` · **Reviewers:** 7/7 completed (6 chunks: core sim, core tests, app, harness+tools, goldens, misc; 42 lens runs)
**Head moved mid-review:** reviewed `0118cc0`, head is now `4d33c65` (7 new commits: hint-buffer fix, allocator-ownership fix, MSAA drop + soak mode, CI fixes). The new commits appear to address W7, W8, and the MSAA crash — a fresh round on the new sha will verify. Findings below describe `0118cc0`.
**Verification:** 56/209 findings confirmed against the code — 9 discarded as false-positive (incl. MSAA SIGTRAP, R-key SIGABRT, "45 tests inaccurate", cross-wired log). All 7 lenses completed; no degraded layers.

**Empirical checks run by Perkins at the reviewed sha (not just code reading):**
- `odin test core`: **40/40 pass** · `odin test app/run`: **5/5 pass** · `tools/lint.sh`: 4/4 gates green
- Built raylib 6.0 software renderer from source (`tools/build_raylib_sw.sh`) and built the harness against it
- `harness run`: **7/7 demos green** (T1 state-hash manifests + T2 pixel goldens + event windows + terminal states)
- Replay gate: **surge_basics 3000/3000 ticks bit-for-bit, error404 250/250 bit-for-bit** — the determinism spine is REAL
- `odin build app` clean; the game binary ran 6s+ without crashing (MSAA crash claim not reproduced)

### Blockers (2)

**B1 — Committed `app.bin` (2MB Mach-O arm64 build artifact) at the repo root**
`app.bin` (added `0df9135`, re-committed `0118cc0`) · evidence: `git ls-files app.bin` tracked; `file` = Mach-O arm64; `.gitignore` misses it; **the PR description never mentions it** — not declared deliberate. It churns on every rebuild, is platform-specific, and bloats the repo. Fix: `git rm --cached app.bin`, add to `.gitignore` (CI builds from source). Sources: acceptance/architecture/codebase/blind/edge/security/tests.

**B2 — Left-click can never select a pipe, open the pipe popover, or dismiss an open popover — demolish is UI-dead and full routers soft-lock**
`app/main.odin` `handle_input` release branch + `handle_click_select` · evidence: `handle_click_select` is called only inside `if rl.IsMouseButtonReleased(.LEFT) && app.drag.active`, and `drag.active` is set only when the press lands on a *node*. Presses on pipes/empty ground never reach the release branch, so: pipes cannot be selected (right-click priority still works, router select works), popovers cannot be dismissed by clicking away (ESC works), and **demolish — the GDD's "redesign is the game" verb and the only way to free ports/budget — is unreachable**. With canon #14 port limits, a full router is a permanent dead end. Fix: run `handle_click_select` on every left release regardless of `drag.active`, keeping the draw path gated on `press_node != 0`. Source: blind (edge/acceptance agree).

### Warnings (20)

**W1 — T1 fingerprint omits `Health_Meter.in_breach` + `.healthy_streak`** (`core/serialize.odin` health block) — the header claims "covers ALL sim state" but these two state-affecting fields (E30 hysteresis band, grace-refill streak) are never written. The spine is empirically intact (3000+250 ticks bit-for-bit), so this is a completeness gap, not a live break; a divergence would leak into hashed meter/grace/event fields within a tick or two. Fix: two `w_bool` lines + deliberate re-bless. [blind, edge, acceptance]

**W2 — E7 WRR-floor test is vacuous** (`core/flow_edge_test.odin:test_qos_wrr_floor_zero_share`) — weights `{100,1,1}` exceed `MAX_WEIGHT=64`, are silently rejected by `submit_c` (which swallows errors), and the zero-share premise never holds; the test passes for the wrong reason and the E7 floor is unpinned. [4 lenses]

**W3 — Severance-reroute test can't distinguish reroute-survival from fresh spawns** (`core/flow_edge_test.odin:test_severance_reroute_with_alternative`) — `sev_drops_before` is captured then discarded (`_ = sev_drops_before`); the assertion passes on 30/tick fresh spawns regardless of whether mid-edge packets survived. E1 branch-1 is claimed pinned but isn't. [4 lenses]

**W4 — Node-health warning surface (🟡/🔴, Ev_Warning_Raised/Cleared) has zero test coverage** — no `crisis_test.odin` exists; no demo asserts warning events. The Godot r1 lesson ("node_health_states untested") was **not applied**. [5 lenses]

**W5 — Queue-overflow shed + E9 drop-ladder combos untested** — `queue_drop_depth`/`Queue_Overflow` appear in zero tests; the newest-first shed order and the BE→Standard→Express ladder are unpinned. [4 lenses]

**W6 — Router triage popover labels swapped** (`app/main.odin:popover_click`) — labels `{"none","stream","email"}` with `triage := i-1` means the "stream" button sets triage=0 = **email**. The QoS differentiator surface labels its buttons opposite to what they promote. [edge, codebase]

**W7 — `context.allocator` left as the run arena after `core.step()`** (`core/run.odin:112`) — never restored; `snapshot_write` appends ride the polluted ambient allocator (its allocator param is unused), and `run_context_destroy` deletes `arena_buf` under the stale arena allocator (no-op → 16MB leak per R restart; UB under a tracking allocator). My 3-cycle create→run→destroy test did not crash — the SIGABRT claim is not reproduced, but the pollution and leaks are real. [codebase, architecture, edge]

**W8 — Dangling hint string UAF** (`app/main.odin:cycle_priority` → `set_hint` with `fmt.tprintf` temp-arena results) — `free_all(context.temp_allocator)` at the top of each frame frees the string while the hint TTL (2600ms) still references it. Real UAF; SIGTRAP not reproduced on this machine, but the text is stale/garbage and a tracking build could fault. [codebase, blind]

**W9 — `harness save` silently blesses demos whose expectations FAILED** (`harness/main.odin:run_demo` → `return ok || save`) — exits 0 and prints "blessed" even when intent/expect checks failed; a re-bless can mask a broken demo. [3 lenses]

**W10 — `demolish node` with no name reads `fields[2]` out of bounds** (`harness/demo_parse.odin`) — harness panics instead of returning a line-numbered parse error. [3 lenses]

**W11 — Cross-allocator free on the T2 mismatch path** (`harness/goldens.odin:save_diff_bundle`) — temp-arena `out` handed to `rl.UnloadImage(dimg)` (raylib frees Odin memory) — UB exactly when the harness is most needed. [3 lenses]

**W12 — `crises.json` parsed+hashed but never consumed** — no reader of `preventive_redesign`/`lead_time_ticks`/`failure_effect`; the engine hardcodes the root cause. Editing the file forces a golden re-bless with zero behavior change (a trap). [3 lenses]

**W13 — Committed self-review docs describe a pre-fix codebase** (`_bmad-output/reviews/odin-prototype-r1/`) — verification-gap.md claims "no step runs `odin build app`" (ci.yml:47 does), "upgrade unreachable from demos" (draw_and_upgrade.dem uses it), edge-case-hunter.md claims E30 hysteresis absent (balance.json ships `breach_exit_pct`). A fresh minion would chase ghosts. [5 lenses]

**W14 — Catalog loader silently truncates i64→i32, accepts unknown keys** (`core/catalog.odin:jint`) — ODN-5's fail-fast contract unmet; u64 tick fields ride through `i32`. Latent today (values are small) but a big tick/multiplier silently corrupts — and re-blesses the corruption. [3 lenses]

**W15 — Zero-traffic neutral ticks (uptime −1) during an open breach drain the meter at MAXIMUM severity** (`core/health.odin`) — `severity := win_uptime_pct − (−1)` → max drain, violating E24's neutral contract. [blind]

**W16 — `pick_dst` allocates two dynamic arrays per spawned packet on the run arena** (`core/flow.odin`) — arena frees are no-ops, so unbounded growth over a long run; ODN-18 churn rule violated in the hottest path. [architecture]

**W17 — `nearest_pipe` bezier hit-testing (the 0118cc0 flagship fix) has zero test coverage** — the head commit's headline change is unpinned. [tests]

**W18 — Grace countdown computes ticks×hz (inverted), discards it, and renders a static "!"** (`app/render/hud.odin:draw_health_meter`) — the countdown numeral never appears. [3 lenses]

**W19 — Grace-reset test passes even with the instant re-arm exploit it claims to pin** (`core/health_test.odin`) — only the end state after 100 healthy ticks is asserted; gradual refill vs instant re-arm are indistinguishable. [blind, tests]

**W20 — `draw_and_reject.dem` header overclaims** — claims ports + budget rejection classes, but the script never triggers `Router_Ports_Full` or `Over_Budget` (6 pipes on an 8-port mid router; budget never approached). [tests]

### Notes (34)
Selected: upgrade_pipe accepts silent downgrades (no tier-direction check) · replay gate hardcodes `bare=false` (dead flag, latent trap) · `expect hash stable` is decorative (T1 compare runs unconditionally anyway — benign) · error404's 8s T2 golden is byte-identical to boot's 1s golden (the mid-drain phase has no pixel pin) · standalone replay gate discards manifest demo identity (cross-wired logs undetectable — harmless today since boot/error404 logs are identical *inputs*) · dead code: `state_dump`, `run_destroy`, `PCG32_INC`, `TICK_SECONDS`, `App.mode`, `press_valid`, `cosmetic_rng` · severance reroute keeps stale `vis_q8` (cosmetic teleport) · action-log roundtrip compares 2 of 6 command kinds · `submit_c` swallows validation errors (the E7 footgun) · `test_rng_streams_independent` tests the opposite of its name · check_golden leaks the frame on both failure branches · write_file/write_log duplicate · raylib fetched by mutable tag; demo names unsanitized in paths (local CLI) · `fmt_bprintf` writes past fixed buffers unguarded (latent stack overflow) · `map_draw` grid loops forever at `tile == 0` (minimized window) · zero-terminal demand accrues with no event (E28 asymmetry) · pipes_between can return a count beyond the scratch buffer (>32 parallel pipes → OOB slice; unreachable under port limits) · BFS 64-neighbor cap unstated · Set_Pipe_Priority accepts < −1 · qos_allocate remainder loop unbound with negative weights (catalog not range-checked) · catalog hash mixes sources without length framing · surge_active cleared by whichever set piece resolves first (latent; one piece today) · demolished strained node never emits Warning_Cleared · bare capture lines accepted silently · stale comments: testkit "NOT used by the game" (autopilot uses it), replay_test.odin doesn't exist · tier_by_name drops `ok` · junction triage `labels` var unused · autowire retries {wide,wide} identically · tests bake catalog tunables into magic numbers · jarr_i leaks per load (tracking allocator noise).

### Reviewer agreement
Highest-confidence (3+ lenses): app.bin committed (7) · warning-surface test gap (5) · stale self-review docs (5) · E7 vacuous test (4) · severance test weakness (4) · drop-ladder gap (4) · triage label swap (2) · T1 fingerprint omission (3) · save-blesses-failures (3) · demolish parse OOB (3) · cross-allocator free (3) · crises.json dead data (3) · harness save exit-0 (3).

### Declared deviations the PR body already documents (accepted, not findings)
logic_hz=10 (proven-fun tuning, manifest-recorded) · work-conserving QoS over the reference's strict partition · gradual grace refill · route arrays inline, monotonic u64 ids (ODN-8 sketch deferred) · harness renders world+HUD into T2 goldens (§10.4 says world-only) · replay-as-stream vs atomic batch (E23 kept for UI batches) · no pan/zoom in PROTO.

**Verdict:** NEEDS CHANGES
The determinism spine — the ONE hard blocker per the briefing — is verified intact: 40/40 + 5/5 tests, 7/7 golden demos green on a fresh software-rendered build, replay bit-for-bit across 3250 ticks, canonical field-wise serialization with corrupt-log rejection. Two blockers remain: the accidental `app.bin` commit, and the dead left-click path that makes demolish/pipe-select/popover-dismiss unreachable in the mouse-only UI. Address the blockers, fix the W1 fingerprint gap + W2/W3 vacuous tests, and this is a merge candidate for the A/B gate.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
