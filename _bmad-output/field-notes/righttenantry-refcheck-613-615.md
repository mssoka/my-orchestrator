# righttenantry-refcheck-613-615

- 2026-08-14: toast.gleam's header comment ("fixed top-right") was stale since birth — the code was always `bottom-4 right-4`. Trust the class string, not the module comment, when reasoning about toast position.
- 2026-08-14: Lustre houdini-escapes apostrophes in serialized attributes (`&#39;`) — pin `title=`/`aria-*` assertions with the escaped form; a bare `'` assertion fails while the DOM is correct.
- 2026-08-14: evidence screenshots must be captured INSIDE the element's lifetime window and pixel-verified before shipping — the first corner-case shot was taken after the 0.8–5.8s toast window and depicted nothing (caught by a reviewer, recaptured).
