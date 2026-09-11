# Offline verification — 2026-09-10

## Scope and environment

Worktree: `/Users/moses/.herdr/worktrees/my-orchestrator/gemini-storyboard-skill`.
Interpreter: `.scratch/gemini-venv/bin/python` (CPython 3.14.0, macOS arm64).
Installed: `google-genai 2.22.0`, `Pillow 12.3.0`, `pytest 9.1.1`.
All test data are synthetic, created in disposable directories. Two contrasting
projects: folded-paper harbor (diffuse, ochre/teal, orthographic) and neon desert
(chrome, hard rim, magenta/black, anamorphic). References are generated RGB PNGs.
Nothing is borrowed from a real film or treated as real look acceptance.

## Exact verification commands (from worktree root)

```bash
.scratch/gemini-venv/bin/python -m pytest .agents/skills/gemini-storyboard/tests -q
.scratch/gemini-venv/bin/python .agents/skills/gemini-storyboard/tests/mutations.py
git diff --check
```

Parent-corrected results after review round 1 (three glm-5.3 xhigh layers,
triaged in the spec's Review Triage Log; patches applied by the parent):
**151 passed**, **1 SDK deprecation warning**, no skipped tests. Mutation
runner: pristine **151 passed** before/after; **13/13 guards killed** by behavioral
test failures, no collection/import failures counted as kills. Working helper
bytes unchanged by mutation runner. `git diff --check`: no whitespace errors.
SDK warning: internal `_UnionGenericAlias` deprecated for Python 3.17; not a
transport request or test failure.

Guard mutations: eligibility, cloud permission, thought filtering, budget money,
attempt limit, SDK retries, resume skipping, expansion gate, snapshot hashes,
HTML escaping, explicit GOOGLE_AI_API_KEY mapping, pre-flight key presence,
required style fields. Each mutant lives in an automatically deleted temporary copy;
there is only one shipped implementation.

Autouse traps deny socket connect/connect_ex/create_connection/DNS and HTTPX
sync/async send. `create_client` is denied by default. LIVE-path tests substitute
`genai.Client` with a fake SDK boundary before construction; they never contact
transport. Their temporary LIVE-shaped receipts exist solely to exercise the
gate's positive branch and are **not genuine approval evidence**. Cross-cwd and
concurrent subprocess tests use a minimal environment (no copied keys) and a
network-denying `sitecustomize.py` created by the tests, not user startup files.

## Matrix audit (all ran)

| Spec row | Covering offline tests |
|---|---|
| Plan, no key/no transport | `test_plan_does_not_need_sdk`, `test_cross_cwd_cli`, `test_deterministic_plan_and_revision` |
| Eligibility fail closed | `test_required_omissions`, `test_invalid_manifest`, `test_small_sample` |
| Reference failures | `test_required_omissions`, `test_invalid_manifest`, `test_malformed_reference`, `test_duplicates_and_extra` |
| Final vs thought, MOCK | `test_final_not_thought`, `test_response_failures`, `test_contrasting_conditioning` |
| Timeout/transport/crash retained | `test_error_no_implicit_retry`, `test_crash_after_reservation`, `test_crash_before_local_attempt` |
| Resume/revision immutability | `test_deterministic_plan_and_revision`, `test_immutable_input`, `test_final_not_thought`, `test_manual_transient_retry` |
| Real look gate, reject mock/dry | `test_expansion_rejects_dry_mock_missing`, `test_real_shape_review_gate`, `test_review_tamper`, `test_live_positive_approval` |
| Shared money/attempt bounds | `test_shared_budget`, `test_two_processes_cannot_overspend`, `test_budget_binding_lock_corruption`, `test_lost_budget_fails_closed`, `test_run_lock_exclusion` |
| Request field/config propagation | `test_contrasting_conditioning`, `test_all_official_ratios_sizes`, `test_explicit_timing_reaches_request` |

Cross-cwd test executes absolute helper `--help`, `plan`, rejected unapproved
`generate --live` (exit 2 before client), and successful `generate --mock` from
a temporary cwd. Same helper, no key, denied transport.

## Exact offline SDK evidence command

```bash
.scratch/gemini-venv/bin/python - <<'PY'
import importlib.metadata as m
from google.genai import types
for x in ('google-genai','Pillow','pytest'): print(x,m.version(x))
for cls in (types.GenerateContentConfig,types.ImageConfig,types.HttpOptions,types.HttpRetryOptions,types.Part): print(cls.__name__, sorted(cls.model_fields))
print(types.HttpRetryOptions(attempts=1).model_dump(exclude_none=True))
PY
```

Observed: `GenerateContentConfig` has `response_modalities`, `image_config`,
`max_output_tokens`, `candidate_count`; **no `response_format`**. `Part` has
`inline_data`, `thought`, `text`. `HttpOptions` has `timeout`, `retry_options`;
retry options dump is `{'attempts': 1}`. Installed
`google/genai/_api_client.py:573-576` uses `tenacity.stop_after_attempt(1)` by
default and `stop_after_attempt(options.attempts ...)` when options are supplied.
Actual construction tests assert 120000 milliseconds, attempts 1, and
`vertexai=False`; every supported ratio/size is constructible locally. No client
was instantiated by the introspection command.

## Recovery integrity

The pre-existing successful render was followed from
`.scratch/bmad-binding/render-output.txt`; it points to the generated BMAD
snapshot, not a direct unrendered skill source. Recovery files stay ignored and
are excluded from the deliverable. Exact integrity command:

```bash
.scratch/gemini-venv/bin/python - <<'PY'
from pathlib import Path
import hashlib,json
rows=json.loads(Path('.scratch/bmad-binding/hashes.json').read_text())
for r in rows:
    src=(Path('/Users/moses/code/.agents/skills/bmad-build')/r['path']).read_bytes()
    cp=(Path('.scratch/bmad-binding/bmad-build')/r['path']).read_bytes()
    assert hashlib.sha256(src).hexdigest()==r['source_sha256']
    assert hashlib.sha256(cp).hexdigest()==r['copy_sha256']
    rev=cp.replace(b'{{config.modules.bmm.implementation_artifacts}}',b'{{.implementation_artifacts}}').replace(b'{{config.modules.bmm.planning_artifacts}}',b'{{.planning_artifacts}}')
    assert rev==src
print('16/16 canonical + recovery hashes unchanged; 16/16 reverse-equality checks passed')
PY
```

Result: **16/16 canonical + recovery hashes unchanged; 16/16 reverse-equality
checks passed**. No recovery, live root, channel, native or pre-existing skill
files were changed.

## Package manifest regeneration

Whenever package files change, regenerate
`_bmad-output/implementation-artifacts/gemini-storyboard-package-manifest.json`
from the final tree — never hand-edit its hashes:

```bash
.scratch/gemini-venv/bin/python - <<'PY'
from pathlib import Path
import hashlib, json, importlib.metadata as md, platform, sys
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
root = Path.cwd(); skill = root / '.agents/skills/gemini-storyboard'
data = {'status': 'offline-tested; independent review pending',
        'python': {'path': sys.executable, 'version': platform.python_version(), 'binary_sha256': h(Path(sys.executable))},
        'dependencies': {}, 'package_files': {str(p.relative_to(skill)): h(p) for p in sorted(skill.rglob('*')) if p.is_file() and not any(x in p.parts for x in ('__pycache__', '.pytest_cache'))}}
for name in ('google-genai', 'Pillow', 'pytest'):
    d = md.distribution(name)
    meta = next(d.locate_file(x) for x in d.files if str(x).endswith('.dist-info/METADATA'))
    data['dependencies'][name] = {'version': d.version, 'metadata_sha256': h(Path(meta))}
(root / '_bmad-output/implementation-artifacts/gemini-storyboard-package-manifest.json').write_text(json.dumps(data, indent=2) + '\n')
PY
```

## Review limitations and handoff

This evidence is implementer verification, **not prescribed independent review**.
The parent generated BMAD review phase must collect its independent layers,
triage findings and assess focused PR readiness before completion. No independent
review verdict, PR merge or pilot pass is claimed here. The stable interface
handoff was relayed via Silas (`herdr pane run w85:p2 ...`, successful CLI exit,
no structured delivery receipt); no direct pNS/channel communication or edits.

No keys/startup files were read, Gemini calls made, auth/quota probed, references
uploaded, real images generated or actual human look reviews conducted. The parent
used public documentation fetches and installed pinned SDK/test dependencies in
the isolated scratch venv. Runtime credential-mapping tests replace the entire
environment with synthetic values; they neither inspect nor copy an actual key.
No renderer/browser aesthetic judgment was performed; HTML was checked through
escaped-text and exact-byte-link assertions. Model availability, server-side
request acceptance, billing, prices, aesthetics and the real pilot remain
unverified. Trust/storage/operator limitations are explicit in
[contract.md](contract.md). Execution remains with the designated separately
authorized pilot owner; the generic package hard-codes no executor identity.
