## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-local-ci-suite · **Reviewed sha:** `a6e3b2b` · **Reviewers:** 7/7 completed
**Verification:** 25/25 findings confirmed against the code — 0 discarded as false-positive (1 downgraded warning→note on impact grounds: the pipefail mechanism is real but no current gate command uses a pipeline)

**The one hard blocker holds:** `.github/workflows/ci.yml` is byte-identical to base (zero diff re-verified at the reviewed sha), and the local suite implements all **8** gates — lint → `odin test core` → app.bin build → harness run → drift-check → preview-check → PP_DEBUG builds → stats-check pause+qos_contention — in CI order, stop-on-fail, with step names quoted verbatim in the GATES array. The lens-guard specifics all verified in code: pinned Odin (arm64+amd64) from `.odin-version`, the workflow's X11 deps + the clang parity gap, rlsw shadow baked at build time, artifact isolation via `.dockerignore` + the single `goldens/_reports/` bind-mount (with a write pre-flight probe), the windows-cross gate checks `-s app-win.exe` rather than trusting the exit code (the exact lie the swarm caught), and docker-down is a plain-language error. The `--windows-cross` probe result (pinned Odin exits 0 with NO binary; gate detects it) is correctly documented in the PR body, as are the gate-mapping table, isolation design, timings, and the zero-diff proof.

### Blockers (0)

None.

### Warnings (6)

1. **Dead `--windows-cross` forwarding** — `tools/ci-local.sh:182` appends `--windows-cross` to the container invocation, but dispatch (220-223) exits on `WIN_CROSS=1` before `run_container` is ever reached. The container-leg probe is only reachable via a manual `docker run … --in-container --windows-cross` — document that or route the flag through `run_container`.
2. **`--windows-cross --mac` silently discards the native suite** — only 2 of the 3 conflicting flag pairs exit 2, despite the "Flag conflicts fail loudly — never silently redefined" comment and the spec artifact's promise. Add the `WIN_CROSS+NATIVE` guard.
3. **`Dockerfile.ci` odin-locate pipeline dropped the workflow's `|| true`** — under `set -euo pipefail`, an empty `find` result aborts the RUN before the designed "odin binary not found; artifact layout:" diagnostic can print. The build still fails (no silent pass), but the mirrored-from-CI diagnostics are lost exactly when needed. One-word fix: append `|| true` like the workflow line it mirrors.
4. **README gate-mapping table is not 1:1 with the workflow** — 9 rows vs 11 non-checkout steps: `Install Odin` + `Linux GUI link deps` are prose-only (the spec artifact claims "all 11 workflow steps"), and 4 rows paraphrase step names the script itself quotes verbatim. Add the 2 setup rows; quote the step names exactly.
5. **Replica↔workflow equivalence is comment-anchored only** — verified exact today, but with GH billing-blocked this suite is the only running CI, and a future ci.yml gate not mirrored into `GATES` silently weakens it. A `--self-test` (or lint gate) asserting the 1:1 mapping would pin it.
6. **Advisory test gate: CONCERNS** — every verification claim is a green run; the stop-on-fail ❌/⏭/exit-1 path (the tool's core contract — code read, straightforwardly correct) and the docker-down path were never demonstrated. Capture one seeded-failure run in the Verification section.

### Notes (11)

- **Host-side `--in-container` mislabels reality**: the usage hint sends users to a flag that only changes message text — the windows-cross probe runs the HOST toolchain yet would print "in-container; the --rm container discards it", and the summary LEG label claims "linux container" for host-executed runs. Derive the label from a container marker, or reject the flag outside the image.
- **README's x64-parity recipe** (raw `docker run --platform linux/amd64`) bypasses the `--user`/`--rm`/bind-mount wiring that only `ci-local.sh` applies — show it through the script instead.
- **Empty `.odin-version`** passes the readability guard → false warning natively, misattributed curl 404 in the container. Check non-empty, not just `-r`.
- **`_pr_body.md` deletion** is housekeeping outside the briefing's deliverables — benign orphan cleanup, but surface it in the PR body.
- **Supply-chain posture is parity with the workflow** (no checksums on base image / Odin tarball / raylib clone) — no gap beyond CI, but the local fetch is layer-cached so upstream drift persists; optional digest/SHA-256 hardening.
- **`.dockerignore` "TRACKED tree" claim overstates**: untracked files and 18MB of tracked `_bmad-output` ship into the image; the gitignored `_charter` scratch pattern isn't mirrored (none present here — conditional exposure; no secrets found; artifact isolation itself is intact).
- **uid-0 invoker** runs the suite as root and leaves root-owned debris in the host bind-mount — warn or refuse.
- **`.dockerignore` ⊂ `.gitignore`** for artifact patterns (export/, *.dmg, .godot/… unmirrored) — no live hole (all current gate outputs verified excluded), but the guarantee rests on the two lists never drifting.
- **windows-cross exit-0-with-warning is comment-pinned only** — the `-s app-win.exe` check is correct today; nothing durable would catch its removal.
- **docker-down message** (verified in code, plain-language ✓) has no demonstrated run in the Verification section.
- **Gates run via plain `bash -c`, not GH's `bash -eo pipefail`** — latent only: no current gate uses a pipeline, the `&&` chains match `-e` semantics, and the gate scripts carry their own set-flags. `bash -eo pipefail -c` would make parity exact for future gates.

### Reviewer agreement

Highest-confidence findings (independent lenses converging):
- README table not 1:1 — **edge + acceptance + codebase**
- Host `--in-container` mislabeling — **blind + edge + architecture**
- Dead windows-cross forwarding — **blind + acceptance**
- Comment-only workflow drift guard — **architecture + tests**
- Green-runs-only verification evidence — **tests (advisory gate) + tests (stop-on-fail path)**

**Verdict:** READY TO MERGE

The hard contract — byte-identical workflow, all 8 gates in CI order with CI failure semantics, artifact-poisoning impossibility, and honest experimental-gate reporting — holds under adversarial review. The warnings are polish on a dev tool (dead line, one flag-pair guard, one `|| true`, docs precision), none of which compromise the suite's trustworthiness as the CI replica. Recommend addressing W1–W4 in a follow-up since they're cheap, but they don't gate this merge.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
