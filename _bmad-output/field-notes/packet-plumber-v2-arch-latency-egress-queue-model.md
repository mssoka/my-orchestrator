# packet-plumber-v2-arch-latency-egress-queue-model — field notes (2026-08-26)

- Reality-check lens caught a spine assertion the code contradicts: `bandwidth_demand` is catalog-loaded but UNWIRED (zero consumers) — never cite a catalog knob in a formula without grepping consumers; "documented in the loader comment" ≠ consumed.
- Serialization-conflict blockers (adversarial AV-2) often dissolve against EXISTING tag-conditional payload slots + derived scratch (the Event.direction reuse kept LOG_VERSION at 6) — enumerate existing payload slots before declaring a bump unavoidable.
- Edit-tool trap: mermaid label strings contain LITERAL `\n` two-char sequences — in edit oldText they must be `\\n`-escaped (a raw `\n` in the JSON silently becomes a newline, the match fails, and the whole multi-edit call atomically no-ops).
