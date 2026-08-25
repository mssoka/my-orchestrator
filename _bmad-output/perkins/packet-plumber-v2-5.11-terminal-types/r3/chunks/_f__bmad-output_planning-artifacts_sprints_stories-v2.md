diff --git a/_bmad-output/planning-artifacts/sprints/stories-v2.md b/_bmad-output/planning-artifacts/sprints/stories-v2.md
index f5097e1..4a94fae 100644
--- a/_bmad-output/planning-artifacts/sprints/stories-v2.md
+++ b/_bmad-output/planning-artifacts/sprints/stories-v2.md
@@ -810,6 +810,11 @@ one fresh minion, dispatched in order 5.9 → 5.12 (the invariant first, the pay
   alone. **Golden:** T1/T2 re-bless + a T2 frame with all three types visible.
 - **Launchable increment:** run the app — homes trickle, campuses flood; the terminal roster reads
   as a spectrum.
+- **Status:** implemented 2026-08-18 — PR open (the class analogues wired: `Terminal_Role` gains
+  `Small_Biz`/`Campus` (`core/catalog.odin:22`) + `role_from_name`; `node_types.json` gains the
+  per-type profile entries (throughput/demand_weight/era) + the era-3 demand entries sourcing from
+  them; the #65 sprites wired per role in the render (never color alone `[E9.1]`); the all-three-types
+  T2 golden (`terminal_types.dem`); the slice's deliberate T1/T2 re-bless, fold-proofed + byte-verified).
 
 ### Story 5.12 — Aggregation groups (congestion lives at the shared uplink)
 
