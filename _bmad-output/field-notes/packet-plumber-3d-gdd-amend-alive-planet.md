# Field notes — packet-plumber-3d-gdd-amend-alive-planet (2026-09-05)

- The core-loop ASCII box in gdd.md is visual-width-69 (emoji count 2): after editing box lines, re-measure ALL box lines with a python east-asian-width script — my first pad math used inner=65 (real: 64) and every replaced line came out 70; a one-line assert script caught and fixed it.
- The `gh pr create --body "$(cat <<'EOF'…)"` trap is real even for carefully quoted heredocs (×3 now) — went straight to `--body-file /tmp/…` on the second attempt; should have been the FIRST attempt.
- Canon-amendment pattern that worked: grep the OLD phrasings before editing ("building→building", "connect two houses", "no junctions", "L1 has no routers") — caught two non-obvious stragglers (tutorial seed line, L1 remediation "direct pipe") that the section-level plan missed.
