# packet-plumber-v2-6.3-upgrade-lifecycle — field notes

- 6.3 era-3 decay re-stages EVERY rate-sensitive era-3 test: the crisis/health fixtures
  were tuned on narrow@10 u/s pre-6.3; decayed narrows (5) + standards (7) push them into
  the marginal regime (attribution chatter — the resolve-margin dips cross). Re-stage the
  ENGINE-mechanic tests on the tier that keeps their staging (crisis: legacy narrows with
  per-test tier knobs; W10/W11 access contracts: WIDE — the era-3 modern tier; at era 3
  STANDARD is legacy too, "modern" means wide only).
- `test_catalog`'s `make_era_row` (determinism_test) builds era rows WITHOUT the decay
  factor → defaults to 0 → `pipe_effective_capacity` silently zeroes EVERY era-1+ pipe's
  capacity (the whole suite collapses). Any new Era_Row field MUST mirror in BOTH the
  catalog_test fixtures AND determinism_test's make_era_row (the load contract's mirror).
- The 6.2 gate's "era-3 standard pipes are legacy" is real: era-3 test fixtures drawn
  standard now decay 15→7 u/s — grep `s.era = 3` + standard/narrow draws when touching
  era-3 scenarios; the stats surface (cap_units) pins the decay in the stats test.
