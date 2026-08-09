# Field notes — packet-plumber-odin-architecture (2026-08-08)

- Lavish question-forms pay off: all 4 rulings came back as queued prompts in
  ONE poll cycle (one Queue button per question + "which rulings I need most"
  in the first --agent-reply). A user QUESTION mid-form (not a radio) means:
  answer in the next --agent-reply AND rebuild the form with the new options —
  they answered from the rebuilt form immediately.
- Multi-edit `edit` batches reject ATOMICALLY (one bad oldText kills all) —
  and a sed/python bulk path-rename afterwards will silently create NEW stale
  texts (`harness//`, misaligned ASCII diagrams, renumbered lists); always
  grep the renamed tokens + re-read touched regions before committing.
- raylib 6.0 (2026-04) ships rlsw software renderer + PLATFORM_MEMORY headless
  backend — bit-exact pixel goldens with no GPU/Xvfb; Odin dev-2026-07a fixed
  vendor:raylib 6.0 bindings; Odin mobile = `-subtarget:android`, emerging
  (odin-lang/Odin#6759); "PCG64-XSH-RR" doesn't exist (PCG32 XSH-RR = 64-bit
  state; PCG64 = 128-bit, XSL-RR/DXSM) — reviewers WILL check.
