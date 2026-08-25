## 🤖 Perkins automated review — round 1 of 3

**Job:** `packet-plumber-v2-qos-default-standard` · **PR:** #73 · **Reviewed sha:** `1a1a175` (head of `v2-qos-default-standard`, base `v2`; merge-base `f162ba6`)
**Reviewers:** 7/7 completed · **Verification:** 23/23 lens findings confirmed against the code — 0 discarded as false-positive (several had claims corrected / severities adjusted during re-verification)

**Method note (big-diff policy):** the 50,631-line diff was chunked — the 1,030-line code+script+docs chunk ran the full 7-lens wave; the 49,450-line goldens chunk (151 files) was verified **mechanically**: `tools/ci-local.sh --mac` **10/10 gates PASS** (incl. golden harness T1+T2+replay); `harness fold-check 5f86ef16ca1c0ece 0e1e1afe9129ff2f` **PASS** (boot's tick-1 shift is the catalog fold alone); **32/35** `log.bin` byte-identical except exactly the 8 `catalog_hash` bytes (offsets 17–24, the documented header field); the **3 behavioral demos** (`sla`, `qos_contention`, `audio_throttle`) differ only by the inserted `Cmd_Set_Weights` records matching their `.dem` additions (+25/+25/+50 bytes; later-record offsets shift from the mid-log insert); `data/balance.json` change is **comment-only** (the fold source); PNG capture diffs are stripe-shaped connected components (aspect 63–85 on straight pipes) with ~zero scattered small components — lane-band re-renders, no packet-sprite movement. The re-bless discipline holds; single-lane sim identity is explained by the work-conserving gap-fill (flow.odin:942–952), which the untouched-default change correctly leaves intact. `odin test core` 209/209 at the reviewed sha.

The QoS canon is correctly implemented at every read site (`apply_draw`, `qos_pipe_weights` fallback, `qos_auto_weights` zero-assignment path, serialization absent-when-empty default, E5 allocator fallback) — no missed site, no balanced-preset resurface, no held capacity on unused lanes.

### Blockers (0)

None.

### Warnings (4)

1. **E6 guard: dead auto-pipe check + duplicated ladder walk** — `core/qos.odin:235-275`, `core/topology.odin:443-449` — `qos_auto_weights_after` unconditionally marks the candidate lane in-play and the loader forces ladder rows into 1..MAX_WEIGHT, so `w[c.lane]==0` is unreachable on auto pipes (the promised bus rejection can't fire there); the ~40-line in-play/fold/ladder walk duplicates `qos_auto_weights` (and the `class` param is never read). *[architecture, blind, codebase]*
2. **E6 guard trusts a non-core auto-follow actor** — `core/topology.odin:443-449`, `app/input/exec.odin:534-537,589-595` — core validates against hypothetical post-follow weights it never writes; the app skips the follow-up while the QoS editor is open (keyboard lane keys bypass the panel's zeroed-lane skip), and any command source omitting the follow-up strands a never-drop class on a zero lane (flow-floor backstop only). This PR itself proves the coupling: 3 demos + 2 fixtures had to mirror the app. MVP-unreachable today (email/streaming are both droppable); note the pre-diff bus also allowed these edits — the zero-lane exposure is new, not the permission. *[architecture, blind, edge]*
3. **Stale "documented-as-canon" comments survive the fix** — `data/balance.json:2` (the `lane_presets` clause still says `default_lane_preset` is "the resting position every pipe starts on + the E5 all-zero fallback" — both halves now false), `core/topology.odin:35`, `core/serialize.odin:66,332`, `core/qos.odin:51`, `core/determinism_test.odin:92`, `app/render/wire_path_test.odin:58` (fixture also omits `auto_ladder` → inert `{0,0,0}` weights, benign). The PR's own root cause was drift documented as canon — leaving six stale phrases re-creates the hazard. *[acceptance, blind, edge, codebase]*
4. **Committed spec under-documents the change** — `_bmad-output/implementation-artifacts/spec-v2-qos-default-standard.md` — zero mentions of `validate_set_lane` (E6 semantics changed to settled weights), `qos_auto_weights_after`, or `harness/palcheck.odin`; empty Spec Change Log; table row claims "never-drop bus guard unchanged". The PR body is accurate; the durable in-repo spec is not. *[blind, acceptance]*

### Notes (7)

1. Era-advance survival of the default lacks a dedicated unit pin (tier is pinned; save/load **is** pinned via the sparse round-trip test `qos_test.odin:209`; era covered by `era_advance.dem` replay). *[acceptance, tests]*
2. Demos hardcode app-mirroring ladder splits (50/30/20, 70/30/0) — a playtest ladder re-tune silently desyncs demos from app behavior; consider a `weights-auto` directive. *[architecture]*
3. Panel never-drop cycle guard still checks CURRENT weights while the bus checks settled weights — under-offers legal lanes on auto pipes (MVP-unreachable). `app/qos_panel.odin:118-126`. *[codebase]*
4. `assigned` flag is sticky across full reversion (override entries persist via in-place replace) — MVP-invisible; worth pinning as intended once never-drop content lands. *[edge]*
5. Defensive fallback branches (`qos.odin:149,319`) re-sourced to the helper but unpinned (bus-unreachable). *[tests]*
6. `default_preset_idx` is now write-only config (loader-only; comment claims an app role nothing performs). *[codebase]*
7. **Advisory test gate: PASS** — P0 100%, P1 100%, overall ~97%; 209/209 executed at the reviewed sha. *[tests]*

### Reviewer agreement

Four multi-source findings, all verified independently: the dead-check/duplication (3 sources), the external-actor coupling (3 sources), the stale-canon-comment class (4 sources), and the spec under-documentation (2 sources). No lens disagreed on any fact after verification; security found nothing (offline game — deserialization surface unchanged).

**Verdict:** READY TO MERGE

The warnings are maintainability/doc-debt (dead branch, duplication, stale comments, stale spec) plus a future-content coupling — none change MVP allocation behavior, and the canon + fold discipline verify mechanically. Addressing them in a follow-up (or a small doc-commit before merge) is recommended but not required.

_Address findings and push — I re-review automatically on the new sha._
