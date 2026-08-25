diff --git a/core/catalog_test.odin b/core/catalog_test.odin
index b89c157..a41a81a 100644
--- a/core/catalog_test.odin
+++ b/core/catalog_test.odin
@@ -28,7 +28,9 @@ NT_VALID :: `{"entries": [
   {"id": "content_host", "kind": "terminal", "terminal_role": "content_host", "throughput_units": 80, "demand_weight": 1, "era_introduced": 3, "port_capacity": 0},
   {"id": "router_basic", "kind": "junction", "terminal_role": "none", "throughput_units": 40, "era_introduced": 1, "port_capacity": 4},
   {"id": "router_mid", "kind": "junction", "terminal_role": "none", "throughput_units": 80, "era_introduced": 3, "port_capacity": 8},
-  {"id": "router_high", "kind": "junction", "terminal_role": "none", "throughput_units": 160, "era_introduced": 3, "port_capacity": 16}
+  {"id": "router_high", "kind": "junction", "terminal_role": "none", "throughput_units": 160, "era_introduced": 3, "port_capacity": 16},
+  {"id": "small_biz", "kind": "terminal", "terminal_role": "small_biz", "throughput_units": 20, "demand_weight": 2, "era_introduced": 2, "port_capacity": 0},
+  {"id": "campus", "kind": "terminal", "terminal_role": "campus", "throughput_units": 150, "demand_weight": 4, "era_introduced": 3, "port_capacity": 0}
 ]}`
 
 TIER_VALID :: `{"entries": [
