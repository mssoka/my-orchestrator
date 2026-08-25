diff --git a/core/catalog.odin b/core/catalog.odin
index e7fd7fa..7efc55e 100644
--- a/core/catalog.odin
+++ b/core/catalog.odin
@@ -19,7 +19,13 @@ import "core:fmt"
 
 Node_Kind :: enum u8 { Terminal, Junction }
 
-Terminal_Role :: enum u8 { None, Residential, Content_Host }
+// Terminal_Role — the closed terminal-role enum (story 5.11 adds the class
+// analogues — a NEW role is a CODE change, Perkins r1 W7; catalog rows map
+// into it via role_from_name). Small_Biz + Campus are appended AFTER the
+// original pair so existing serialized role bytes (0/1/2) stay stable — the
+// enum VALUE is the T1-visible byte (ODN-11), adding at the end never shifts
+// an old golden.
+Terminal_Role :: enum u8 { None, Residential, Content_Host, Small_Biz, Campus }
 
 // --- catalog row types -------------------------------------------------------
 
@@ -1036,6 +1042,8 @@ role_from_name :: proc(name: string) -> Terminal_Role {
 	switch name {
 	case "residential":  return .Residential
 	case "content_host": return .Content_Host
+	case "small_biz":   return .Small_Biz
+	case "campus":      return .Campus
 	}
 	return .None
 }
