# Edge Case Hunter review — /tmp/oss-selected-safety-fixes-20260912.diff (2026-09-12)

Scope: diff hunks only. Path enumeration + deletion check + claims check (spec Intent / Tasks & Acceptance read after tracing). Verified by execution where noted (all four suites re-run: PASS; Python suite run twice, identical).

```json
[
  {
    "location": "bin/pr_ready_core.py:300",
    "trigger_condition": "reviews list contains a non-object element (gh schema drift)",
    "guard_snippet": "if not all(isinstance(r, dict) for r in reviews): return blockers, [(\"EVIDENCE_MISSING\", \"reviews entry is not an object (schema)\")], info",
    "potential_consequence": "AttributeError traceback crashes CLI; exit 1 masks UNKNOWN, violating no-traceback contract",
    "kind": "claim",
    "confidence": "high",
    "note": "Verified by execution: core.evaluate(..., {\"reviews\": [\"oops\"]}, ...) raises AttributeError. Spec I/O matrix promises bad schema -> exit 2 TOOL_ERROR, no traceback."
  },
  {
    "location": "bin/pr_ready_core.py:460-475",
    "trigger_condition": "mergeable field has an unexpected type (e.g. number 5)",
    "guard_snippet": "elif not isinstance(mb, bool) and mb not in (\"MERGEABLE\", \"UNKNOWN\", False, \"CONFLICTING\"): res.unknowns.append((\"EVIDENCE_MISSING\", f\"mergeable={mb!r} unrecognized\"))",
    "potential_consequence": "Invalid schema value passes every branch; READY with unknown mergeability (verified: READY)"
  },
  {
    "location": "bin/pr_ready_core.py:487-492",
    "trigger_condition": "view.statusCheckRollup is JSON null (not missing, not [])",
    "guard_snippet": "if view.get(\"statusCheckRollup\") is None: res.unknowns.append((\"EVIDENCE_MISSING\", \"statusCheckRollup is null (sparse evidence)\"))",
    "potential_consequence": "Null evidence treated as no checks; READY possible with no-gates-established (verified: READY)"
  },
  {
    "location": "bin/check-pr-ready:305-308",
    "trigger_condition": "a check turns PENDING between first view and head re-read",
    "guard_snippet": "_rp, reread_pend, reread_fails, reread_unknowns, _rs = core.classify_rollup(...); if reread_fails or reread_unknowns or (reread_pend and not args.allow_pending): return 2",
    "potential_consequence": "READY printed while CI restarted at same head; phase-1 read would have blocked"
  },
  {
    "location": "bin/check-pr-ready:296-298",
    "trigger_condition": "re-read mergeable is null or \"UNKNOWN\"",
    "guard_snippet": "if reread.get(\"mergeable\") in (False, \"CONFLICTING\", None, \"UNKNOWN\"): print STALE; return 2",
    "potential_consequence": "READY although mergeability unestablished on final read; phase-1 blocks both values"
  },
  {
    "location": "bin/check-pr-ready:68-80",
    "trigger_condition": "child stdout contains bytes invalid as UTF-8",
    "guard_snippet": "except UnicodeDecodeError as e: raise ToolError(\"TOOL_ERROR\", f\"{cmd[0]} output undecodable: {e}\")",
    "potential_consequence": "subprocess text=True decode raises ValueError uncaught; traceback, exit 1"
  },
  {
    "location": "bin/pr_ready_core.py:515-533",
    "trigger_condition": "claim: --allow-pending tolerates pending checks (exit 0 qualified banner)",
    "guard_snippet": "code blocks instead: pending REQUIRED gate -> EVIDENCE_MISSING blocker, exit 1 (verified end-to-end)",
    "potential_consequence": "Flag semantics silently depend on branch protection; qualified exit 0 never reached",
    "kind": "claim",
    "confidence": "high",
    "note": "Falsifies spec I/O matrix row 'CheckRun pending, --allow-pending -> exit 0 READY-qualified banner'."
  },
  {
    "location": ".pi/extensions/nefario-watch.ts:250-256",
    "trigger_condition": "herdr inventory JSON with agents:null or a string",
    "guard_snippet": "if (!Array.isArray(env?.result?.agents)) return { ok: false, reason: \"agents not an array\" };",
    "potential_consequence": "ok:true with empty statuses; every tracked pane falsely alerted gone (N04 class re-entry)"
  },
  {
    "location": ".pi/extensions/nefario-watch.ts:502-524",
    "trigger_condition": "herdr agent list fails during roundDebrisCheck; row loop proceeds anyway",
    "guard_snippet": "on agents failure set perkinsPanes = null and skip row classification this tick (match liveQ/registry fail-closed)",
    "potential_consequence": "DEBRIS alert + sweep recipe emitted with unknown pane ownership; live panes unlisted"
  },
  {
    "location": ".pi/extensions/nefario-watch.ts:629",
    "trigger_condition": "claim: unexpected/relative roots never receive a cleanup instruction",
    "guard_snippet": "orphan loop does exists.get(cwd) ?? false — unchecked non-meaningful path reads as 'removed' and alerts",
    "potential_consequence": "1-segment /perkins-* cwd gets close-pane instruction though never stat'd",
    "kind": "claim",
    "confidence": "medium",
    "note": "Contradicts the meaningfulPath guard's own comment and spec N07 matrix row."
  },
  {
    "location": ".pi/extensions/nefario-watch.ts:1103-1122",
    "trigger_condition": "summary.json incidents entries missing id/name/status fields",
    "guard_snippet": "if (incidents.length !== incidentsRaw.length) throw new Error(\"incident entry schema invalid\") — treat as unknown, skip tick",
    "potential_consequence": "Dropped entries -> zero valid incidents + good indicator -> false CLEARED message"
  },
  {
    "location": ".pi/extensions/nefario-watch.ts:213",
    "trigger_condition": "system clock steps backward; now < stored last-emit timestamp",
    "guard_snippet": "if (now < prev) { healthLast.delete(kind); } else if (now - prev < 30 * 60 * 1000) return null;",
    "potential_consequence": "Negative elapsed suppresses all health notes until wall clock catches up"
  },
  {
    "location": "bin/test-model-policy:75-80",
    "trigger_condition": "SKILL.md absent while bin/vision-read regresses to legacy GLM default",
    "guard_snippet": "in the else branch also run: ! grep -q 'MODEL=\"zai-coding-cn/glm-5.3-flash\"' bin/vision-read || fail",
    "potential_consequence": "Vacuous pass; tracked-surface GLM regression uncaught in fresh worktrees"
  },
  {
    "location": ".pi/extensions/nefario-watch.ts:543-552",
    "trigger_condition": "debris path sits on a stalled/automounted network filesystem",
    "guard_snippet": "restore a bound existence probe (e.g. worker with per-path deadline) — removed bash call carried timeout 8000",
    "potential_consequence": "Synchronous statSync blocks sensor tick and host process indefinitely, no timeout",
    "kind": "deletion",
    "confidence": "medium"
  }
]
```

Verification evidence gathered during review (not findings):
- `python3 test/test_check_pr_ready.py` — 75 tests OK (run twice, identical).
- `node --experimental-strip-types test/nefario-sensor-safety.test.ts` — ALL PASS.
- `node --experimental-strip-types test/nefario-watch-conflict.test.ts` — ALL PASS (unmodified; its fake curl payload `{status:{description},incidents:[]}` is schema-INVALID for the new N05 parser and is silently skipped — compatible, claim holds).
- `bin/test-model-policy` — ALL PASS in this checkout (SKILL.md absent; else branches taken).
- Claims verified true (no findings): exact-actor policy, head re-read-before-READY, bare-number explicit-slug-or-skip on both surfaces, N04 rate-limited health note + no gone synthesis, N07 zero shell bytes, N08 live-owner exemption on done branch + fail-closed liveQ/registry, N05 multi-incident/partial-recovery/evidence-based clear at container level, exit-code mapping, flag>env>default precedence.
