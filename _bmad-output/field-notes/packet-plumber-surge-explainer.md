# field notes — packet-plumber-surge-explainer (2026-08-15)

- v2's `bandwidth_demand` is loaded into the catalog (catalog.odin:455) but NOT consumed by the flow service pass (flow.odin:405 serves flat `packet_bandwidth` 30 for every packet) — verify per-class transit claims against serve_bundle_lane, not the catalog comment.
- The drop "ladder" (BE → Standard → Express) is lane-ordered, not class-ordered, and BOTH MVP classes default to the Standard lane — "email pays first" is only true after 5.8 categorization; the 99-vs-95 screenshot gap is run arithmetic, not a priority rule.
- Multi-edit `edit` batches reject atomically: a duplicate oldText (accidentally included twice) fails the WHOLE batch silently — dedupe targets; lavish session-end can arrive with the verdict in the final prompt (check state.json chat if the poll seems to miss one).
