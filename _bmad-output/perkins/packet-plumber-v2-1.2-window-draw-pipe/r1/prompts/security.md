# LENS: Security (source = `security`)

First load the shared context: read `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/prompts/_shared.md` (lens-guards, output schema + contract, empirical gate status, canonical input paths). Follow it exactly.

## YOUR LENS — OWASP-oriented security review of the diff
This is an offline single-player desktop game (Odin + raylib), NOT a web service — calibrate accordingly. There are no HTTP endpoints, auth, or DB. Still evaluate:
- **Input validation at system boundaries:** the action-log binary reader (`log_read` — untrusted bytes from a file), the JSON catalog parser (`catalogs_load` — `data/*.json`), the demo parser (`parse_demo` — `demos/*.dem` text), the rlsw image readback + PNG decode/encode (`LoadImage`, `ExportImage`, `LoadImageColors`). Bounds checks on length-prefixed records? Trust of `header.count` / `len` fields? Integer overflow in offsets?
- **Unsafe deserialization / memory safety:** the `node_slot_raw` "unreachable" fallback returning slot 0 (out-of-bounds risk if ever hit), the `make_drift_mutations` byte-offset assumptions, `compare_images` trusting `width*height`, the `swizzle_rb` pointer/image-aliasing (`UnloadImage(img^)` then `img^ = new_img` keeping `px`).
- **Unsafe defaults / silent acceptance:** a malformed log that should reject but is accepted (the W1 gate's whole point — verify the rejections are real, not cosmetic).
- **Path traversal / arbitrary file writes:** `drift_check` writes to `/tmp/pp-drift-...` (name from a demo name — injection?); `golden_path`/`save_diff_bundle` build paths from demo names.
- **Secret/credential handling:** none expected — confirm none leaked.
- **Determinism-as-security:** for THIS project, a replay gate that silently accepts drift is a correctness/security defect (cheating / desync). The lens-guards #1/#4/#5 are the relevant "security" surface.

## OUTPUT
Write ONE valid JSON array (schema + contract in `_shared.md`) to:
`/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/security.json`

`source` = `"security"`. Only the JSON array in the file. `[]` is valid. Verify every claim by reading the actual code; quote exact lines in `evidence`. When done, stop.
