# packet-plumber-3d-gdd-amend-cumulative — field notes

- 2026-09-05: GDD amendment — supersede chains must be DATE-STAMPED at every amended canon site (M2/M3/OQ9/E10.7), not just in the decision log, or readers meet the old claim first and trust it (D5's retirement clause had propagated to 4 sites).
- 2026-09-05: `gh pr create --body "$(cat <<'EOF' ...)"` with apostrophe-rich markdown dies on quoting — write the body to a temp file and use `--body-file` instead.
- 2026-09-05: scope guard pays off twice — stale canon found ADJACENT to the named sections (Risks row 2 "constellation... re-scope an open question") gets flagged in the decision log + PR body, never silently fixed; keeps the diff reviewable and the ruling trail honest.
