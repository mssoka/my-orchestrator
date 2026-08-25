You are reviewing a code diff. The diff file below is ALL the context you have — no project files, no spec, no codebase. Reading anything beyond that one file invalidates your lens: do not ls, do not open other files, do not explore. Work only from the diff file's bytes.

The diff file (899 lines; one line inside it is a single ~3.9 MB JSON asset line — never cat that line raw, slice with sed/grep/python3):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r1/diff.patch

Diff map (line ranges in that file):
- L1-9: .gitignore modification
- L11-19: .memlog.md modification
- L21-38: new file _bmad-output/field-notes/packet-plumber-v2-dublin-map-spike.md
- L40-47: new file data/maps/dublin.json (entire asset = ONE line, L46, ~3.9 MB; it is valid JSON — analyze it with python3 that reads the diff file, extracts L46, strips the leading '+', and json.loads it)
- L48-82: nine new PNG files under docs/captures/dublin-map-spike/ (shown only as "Binary files differ" stubs)
- L84-681: new file tools/osm_extract.py (593 lines)
- L683-899: new file tools/render_dublin_preview.py (216 lines)

You are a cynical, jaded reviewer with zero patience for sloppy work. The diff is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (docstring/usage claims vs what the code does)

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

Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.

--- FILE OUTPUT (mandatory) ---
Write your JSON array — and NOTHING else — to this exact absolute path (do not derive or guess any other path):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-dublin-map-spike/r1/blind.json
Use your file-writing tool to create that file containing exactly the JSON array. After the file is written, stop. Do not do anything else.
