# LENS: blind (source tag: `blind`) — Perkins r3 refcheck rc4-3

**ISOLATION CONTRACT — this is the Blind Hunter lens.** The diff chunk below is ALL the context you have: no project files, no spec, no worktree access, no conventions, no prior-round findings. Do NOT read anything beyond the diff file — reading the repo, the spec, the shared brief, or any briefing invalidates your lens. Your only inputs: the diff chunk file and this brief.

Read your assigned diff chunk file. You are a cynical, jaded reviewer with zero patience for sloppy work. The diff is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)
- A control that renders but can never be activated; a guard that looks like a guard but isn't one; an error path that returns success; a branch that is unreachable

This is a REWORK diff (the head commit is titled "fix(refcheck): RC4.3 r2 rework — taken-over failure paths, format-proof stale-bounce gate, substitution guard rails"): pay extra attention to hunks whose only purpose is to FIX something — verify the fix actually fixes (e.g. a `taken_over_at IS NULL` guard added to a failure path, a timestamptz comparison moved into SQL, a 400/409 guard on substitute, a `form_opened_at`/`draft_answers` clear in the correction SQL). A fix that doesn't fix, or that fixed one call site but missed the sibling call site, is exactly the inconsistency to report.

--- DIFF ---
Your assigned chunk: `{diff_file}` — read ONLY that file's bytes.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Output contract: ONLY the JSON array, written to your output file. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
