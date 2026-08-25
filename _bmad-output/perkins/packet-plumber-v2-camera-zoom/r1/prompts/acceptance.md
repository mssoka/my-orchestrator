--- YOUR LENS (source tag: acceptance) ---

Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

The job briefing's "Scope" (1-6), "Rules (hard)" (1-4) and "Acceptance" sections are the acceptance criteria. The round briefing's 'Lens-guards' section defines the hard blocker bar AND the user rulings on what NOT to re-litigate — a finding that re-litigates a settled user ruling (wheel zoom-to-point + drag pan as the directive, the [1.0 fit, 4.0] clamp, the empty-ground-drag conflict-free design with draw gestures starting only on a node press, the 8 new pins as acceptance evidence) will be discarded.

Hard blocker bar (from the round briefing — verify these, do not assume): (a) the sim never sees the camera (ODN-1 — camera is pure render/input; core/ untouched); (b) ZERO golden drift — the harness pins the default camera, no golden file may change in this diff; (c) NOC wheel ownership — wheel = map zoom, the log scrolls only with the pointer over the panel (one consumer, effect_zoom); (d) HUD/overlays stay screen-space at all zooms.
