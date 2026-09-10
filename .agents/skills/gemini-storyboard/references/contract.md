# Storyboard contract v1

## Manifest

[Template](../templates/video.json) and [helper](../scripts/storyboard.py) are the
canonical local interface. JSON rejects duplicate keys and nonfinite constants.
Unknown structural fields are rejected; no silent configuration defaults.

| Field | Required value |
|---|---|
| `schema_version` | integer `1` |
| `video` | `id`, nonempty `title`, nonempty `story` direction object |
| `run_id`, `revision` | safe ID and nonempty revision text respectively |
| `approval` | `approved: true`, nonempty `reviewer`, `reviewed_at` (human-supplied timestamp text) |
| `style` | required nonempty `medium`, `shape_language`, `palette`, `materials`, `lighting`, `camera`, `composition`, `mood`, `continuity`, `exclusions` |
| `references` | nonempty array; unique `id`, `role`, `path`, `mime_type`, `provenance`, boolean `external_use_allowed` |
| `shots` | nonempty array; unique `id`, `status`, boolean `selected`, `direction`, `section`, `timing`, `reference_ids` |
| `config` | `model`, `aspect_ratio`, `image_size`, `max_output_tokens`, `timeout_ms`; all explicit |
| `budget` | nonnegative finite decimal **string** (positive for execution) `limit_usd`, positive integer `max_attempts` |
| `sampling` | `stage: sample` and `review_path: null`, OR `stage: expansion` and absolute `review_path` |

Safe IDs match `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`. IDs are case-sensitive; use
case-distinct IDs only on a case-sensitive filesystem. `video.story`, `style`,
and `shots[].direction` permit nested objects, lists and nonempty text leaves under
the required keys. Shot direction requires `story_beat`, `subjects`, `action`,
`location`, `framing`, `lighting`; optional `emotion` and `transformation`.
The video story object is extensible (for example `song` metadata); `section` is
explicit supplied section text or the literal `unknown`. Every supplied field in these objects, the title, revision, shot
(including timing/start/end frames), and selected reference provenance reaches
the actual SDK text parts as canonical JSON. Direction objects contain no nulls,
empty leaves, numbers or booleans; express creative numeric directions as text.
Administrative approvals, budgets and excluded shot directions are not prompts.

Reference role is `character`, `environment`, `style`, `object` or `revision`.
Per request: maximum 14 images, up to 4 character and 10 other images. Roles and
provenance are included in the actual conditioning prompt, not just a local list.

Shot status is `not_started`, `started` or `unknown`; **only explicitly selected
`not_started` shots are eligible**. At least one selected shot is required.
An excluded shot is recorded with its status and `not selected` reason, never
requested. Selected references must grant external use; every reference must
supply provenance even if excluded. `reference_ids` is a nonempty unique list of
existing reference IDs. Optional `start_frame` and `end_frame` must name IDs
already in that shot's reference list; they are conditioning images, not generated
animation frames. To request optional transformation start/end illustrations, use
two explicitly named shot-card IDs (for example `turn-start`, `turn-end`) with
`illustration: start` / `end`, explicit state in `direction.transformation`, and
the source shot's truthful eligibility/timing. Each illustration is a distinct
budgeted request; the tool never invents intermediate frames.

Timing is exactly `{"status":"unknown"}`, or
`{"status":"explicit","start_seconds":0,"end_seconds":2.5}` with finite
nonnegative values and end > start. No audio is read or timing inferred.

Selected images are read relative to the manifest (absolute paths also allowed),
then verified with Pillow `verify()` and full pixel decode, including MIME match.
Allowed MIME: `image/png`, `image/jpeg`, `image/webp`. Limit: 20 MiB per image;
Pillow decompression-bomb warnings fail validation. Encoded selected inputs and
prompt must fit under 19 MiB (reserve overhead below the 20 MiB inline API limit). Unselected images are never
read/uploaded. Missing/malformed selected images or missing cloud permission
fail before SDK client creation. Plan caches the exact verified bytes; subsequent
changes to source files do not silently change a run. Revise via a new plan/run.

Config pins `gemini-3.1-flash-image`. Ratios: `1:1`, `1:4`, `1:8`, `2:3`, `3:2`,
`3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`.
Sizes: `512`, `1K`, `2K`, `4K`. `max_output_tokens`: integer 1..32768;
`timeout_ms`: integer 1..3600000. These are SDK-shape-verified settings, not a
claim that every cross-product or token cap yields a usable live image.

## CLI and paths

```text
plan --manifest FILE --output-root DIR
  -> prints absolute DIR/VIDEO_ID/RUN_ID; exclusive namespace creation

generate --run RUN --budget-dir ABS_DIR (--mock | --live)
  [--approved-by AUTHORIZED_EXECUTOR --approval-id RECORD --accept-cost]
  [--resume | --retry-attempt ID --allow-transient-retry]
  -> JSON list of new receipts; no work yields []

review --run RUN --reviewer NAME --decision approve|reject --notes TEXT
  --human-look-confirmed
  -> immutable review.json plus JSON stdout
```

Exit status: 0 successful command/no unattempted work, 1 recorded non-success
request outcome, 2 validation/storage failure. Ctrl-C/crash may leave no final
receipt: the budget reservation is authoritative and remains unknown. A
`--retry-attempt` invocation processes **only** the retried shot; any remaining
unattempted shots still need their own later `--resume`.

```text
OUTPUT_ROOT/VIDEO_ID/RUN_ID/
  manifest.json             canonical immutable manifest
  plan.json                 deterministic prompts/config/hashes/exclusions/cost
  plan.html                 dry-run prompt cards, NOT generated images
  seal.json                 manifest + plan SHA-256 (canonical JSON)
  references/ID.png|jpg|webp exact selected input bytes, SHA-256 in plan
  execution.json            immutable mode/authorization/shared budget binding
  .lock                     persistent POSIX flock file, auto-unlocked on death
  attempts/ATTEMPT_ID/
    reservation.json        copy of shared reservation (can be absent on crash)
    request.json            exact prompt/config/reference hash receipt
    final.png|jpg|webp      exact final bytes, ONLY for successful extraction
    receipt.json            result/usage/output hash/reservation, never replaced
    card.html               escaped text, exact relative image link, MOCK/LIVE
  review.json               actual human look decision, successful LIVE sample
SHARED_BUDGET/
  .lock
  policy.json               immutable cap/max_attempts/mode/reserve policy
  attempts.jsonl            append-only fsynced reservations across ALL runs
```

Hashes use SHA-256. Manifest/plan/prompt hashes are canonical UTF-8 JSON/text
hashes, not hashes of the original JSON whitespace; image hashes bind exact bytes.
Journal rows are re-validated on every read: exact key set, integer sequence and
fixed reserve per row — a tampered or partial row fails closed.
Each reservation records sequence, UUID, run path, manifest hash, shot ID, mode,
time, retained reserve, unknown initial usage and optional prior attempt ID.
Receipts never replace reservations. A crash between reservation and local writes
still consumes budget and blocks retry of that shot. A partial write fails closed;
it must not be erased to regain budget. Run locks serialize generate/review;
budget locks serialize shared admission. No lock is held during network transport
except the owning run lock. Only one request per turn, no SDK chat/history or
thought-signature replay.

## Response and expansion semantics

Only one candidate, `STOP`, and exactly one non-thought validated inline image
succeed. Thought image/text parts are discarded (only a count is retained);
final text, finish/block reason and raw SDK usage metadata are retained. Refusal,
no image, malformed/MIME mismatch, multiple images and incomplete finish are
non-success. Bytes are never re-encoded. Failure cards have no output board.
Missing usage remains **unknown**, never zero. API/transport errors retain only
exception type and HTTP code, not exception strings that might expose secrets.
All non-success outcomes stop the current invocation, without automatic retries.

Initial sample: at most three selected illustrations, subject to approved budget
and actual selection. Fixed reserve permits two attempts under US$5. Review requires every sample shot's
latest attempt to have a successful LIVE receipt and matching stored output hash.
Mock/dry/missing evidence cannot authorize expansion. Expansion binds the review
against the exact sample manifest, receipts, outputs and common reference bytes,
and the complete video/style/revision/config/reference declarations/shot inventory
(except selection). Changed scope needs a fresh small sample. An approved review
is never editable; rejection or direction changes need a new run. A review is a
human assertion, not a machine aesthetic evaluation.

## Safety/trust limits

This is a local trusted-operator tool, **not a billing service or tamper-proof
approval authority**. Names/approval IDs cannot authenticate an executor or a human;
external operator controls and an actual approval process are required. Hashes
catch accidental mutation, not an attacker rewriting files and all their hashes.
Keep manifests, budgets, reviews and outputs in operator-owned directories; do
not use adversarial symlinks, untrusted shared directories, NFS or sync folders.
Back up the entire run/budget tree; do not move active runs (journal binds absolute
paths), delete journals, reset caps in another directory, or manually convert
MOCK evidence to LIVE. Pricing/rate changes invalidate the spending assumptions.
The tool does not inspect other workspaces to detect existing production; the
caller must supply truthful shot status and approved direction. Unknown
interruption charges require human/provider reconciliation, never an implicit
retry or reserve refund. No live/aesthetic acceptance is asserted by offline tests.
