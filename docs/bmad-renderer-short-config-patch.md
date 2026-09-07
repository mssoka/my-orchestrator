# BMad renderer equivalent-short-config patch

## Ownership and provenance

`_bmad/scripts/render_skill.py` is installer-managed and gitignored. The local
install was produced by `bmad-method` v6.12.0 (tag commit
`05bfbd46d00766ec88eb9b42e76be2c575d64d7b`) with upstream renderer SHA-256
`8496d0d8b449d64c21b42a9aab3b13fc8a813a430c0695ffd84ad75bb1da7942`.

The tracked patch owner is `bin/patch-bmad-renderer-short-config`; the patched
renderer SHA-256 is
`6b8752a0a0552c4d24221912c2ef5cf0a37539e060b19425e7433574d589738d`.
The patcher only accepts those exact upstream bytes, writes atomically, and is
idempotent only on the exact reviewed patched bytes. It refuses every unknown
renderer hash so a BMad update cannot inherit the patch accidentally.

## Why the renderer is patched

A combined BMM+GDS install legitimately contains both
`modules.bmm.implementation_artifacts` and
`modules.gds.implementation_artifacts`. `bmad-build` v6.12.0 uses the short
`{{.implementation_artifacts}}` token. The upstream renderer rejects every
multi-match even when all candidates resolve to the same project-root-bound
path. The same shared-contract shape exists for `planning_artifacts`, so a
single-token workaround only moves the failure.

Central config customization cannot remove one installed key, and per-skill
`bmad-build` customization exposes no config-binding field. Editing the tracked
installer-owned skill would be overwritten on update. The local repair instead
makes the existing short-token contract explicit:

- zero candidates still HALT as missing config;
- one candidate resolves unchanged;
- multiple candidates resolve only when every value is identical after
  `{project-root}` expansion;
- differing values still HALT as ambiguous and list every conflicting path;
- every equivalent source path is recorded in `manifest.json` under
  `inputs.resolved_values`; no first-match choice is made or hidden.

Project-root resolution, immutable generation identity, source loading,
customization, and publication are unchanged.

## Apply and verify

From the orchestrator root:

```bash
bin/patch-bmad-renderer-short-config
bin/patch-bmad-renderer-short-config --check
uv run --python 3.11 test/test_bmad_renderer_short_config.py
```

The regression suite exercises the real tracked `bmad-build` skill through a
copy of the installed renderer. It covers equivalent mixed BMM+GDS bindings,
conflicting duplicates, missing config, single-module compatibility, absolute
project-root metadata and paths, source-path receipts, compile-token removal,
and preservation of the plan/implementation/review/verification workflow
instructions.

After every BMad install or update, run `--check`. If it reports the known
v6.12.0 upstream hash, reapply and rerun the regression suite. If it reports any
other hash, do not force the patch: inspect the new upstream renderer and tests,
then retire or rebase this patch deliberately.
