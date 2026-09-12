#!/usr/bin/env python3
"""Regression suite for bin/check-pr-ready + bin/pr_ready_core.py (packet A).

Ports the 2026-09-12 readiness audit's 85-case characterization matrix
(/Users/moses/code/_bmad-output/implementation-artifacts/
orchestrator-nefario-pr-readiness-audit-20260912/fixtures/readiness.json)
to UPDATED expectations: the selected defects (R01 CI classification,
R02 head binding, R03 canonical Perkins actor, R04 identity/boundary
contracts) must now be fixed; preserved-correct controls (positive
controls, same-reviewer CR→APPROVED, mixed-reviewer veto, MERGED, …)
must stay correct.

Runs the REAL CLI end-to-end: only the subprocess boundary is faked
(ledger / gh / git argv routing, like the audit's inert harness). No
network, no ledger, no GitHub. Pure-core unit cases run the evaluator
directly.

Run: python3 test/test_check_pr_ready.py   (from the repo root or anywhere)
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD_A = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
HEAD_B = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def load_cli():
    from importlib.machinery import SourceFileLoader
    loader = SourceFileLoader("check_pr_ready_cli", os.path.join(REPO, "bin", "check-pr-ready"))
    spec = importlib.util.spec_from_loader("check_pr_ready_cli", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def load_core():
    spec = importlib.util.spec_from_file_location("pr_ready_core", os.path.join(REPO, "bin", "pr_ready_core.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CLI = load_cli()
CORE = load_core()


def check_run(name, status="COMPLETED", conclusion="SUCCESS", **over):
    d = {"__typename": "CheckRun", "name": name, "status": status, "conclusion": conclusion}
    d.update(over)
    return d


def status_context(name, state, **over):
    d = {"__typename": "StatusContext", "context": name, "state": state}
    d.update(over)
    return d


def review(state, login="perkins-review[bot]", at=HEAD_A, submitted="2026-09-12T00:00:00Z", rid=None):
    return {
        "id": rid or f"review-{state}-{login}-{submitted}",
        "state": state,
        "author": {"login": login} if login is not None else None,
        "submittedAt": submitted,
        "commit": {"oid": at} if at is not None else None,
    }


def view(over=None, **kv):
    d = {
        "state": "OPEN",
        "mergeable": "MERGEABLE",
        "isDraft": False,
        "reviewDecision": "APPROVED",
        "headRefOid": HEAD_A,
        "baseRefName": "main",
        "statusCheckRollup": [check_run("required-ci")],
    }
    if over:
        d.update(over)
    d.update(kv)
    return d


def job(over=None, **kv):
    d = {
        "id": "fixture",
        "status": "in-review",
        "pr": "https://github.com/example/demo/pull/7",
        "pr_review": 1,
        "repo_root": "/FAKE/repo",
        "repo": "example/demo",
    }
    if over:
        d.update(over)
    d.update(kv)
    return d


class Res:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FakeRunner:
    """Routes subprocess.run by argv[0]: fake ledger / gh / git. Replaces
    subprocess.run so the REAL CLI run() logic (timeout/missing-binary
    conversion) still executes."""

    def __init__(self, world):
        self.world = world  # {jobs, view(s), reviews, remote, api, reread, fail}
        self.calls = []

    def __call__(self, cmd, cwd=None, capture_output=False, text=False, timeout=None):
        self.calls.append(cmd)
        w = self.world
        tool = os.path.basename(cmd[0])
        if w.get("fail_tool") == tool:
            raise subprocess.TimeoutExpired(cmd, timeout or 0)
        if cmd[1:3] == ["json", "all"]:  # ledger CLI (any binary name)
            if w.get("ledger_rc", 0) != 0:
                return Res(w["ledger_rc"], "", "ledger exploded")
            if w.get("ledger_raw") is not None:
                return Res(0, w["ledger_raw"], "")
            return Res(0, json.dumps(w.get("jobs", [job()])), "")
        if cmd[:2] == ["git", "-C"]:  # remote get-url origin
            return Res(0, w["remote"], "") if w.get("remote") else Res(1, "", "")
        if tool in ("gh", "fake-gh", "custom-gh"):
            gh_calls = sum(1 for c in self.calls if os.path.basename(c[0]) in ("gh", "fake-gh", "custom-gh"))
            if w.get("fail_gh_after") is not None and gh_calls > w["fail_gh_after"]:
                raise subprocess.TimeoutExpired(cmd, timeout or 30)
            if w.get("gh_rc", 0) != 0:
                return Res(w["gh_rc"], "", "gh exploded")
            if w.get("gh_raw") is not None:
                return Res(0, w["gh_raw"], "")
            args = cmd[1:]
            if args[0] == "api":
                path = args[1]
                api = w.get("api", {})
                if w.get("__all_forbidden__"):
                    return Res(1, "", "Forbidden")
                if path in api:
                    status, payload = api[path]
                    if status != "ok":
                        errmap = {"not-found": "Not Found", "forbidden": "Forbidden"}
                        return Res(1, "", errmap.get(status, "error"))
                    return Res(0, json.dumps(payload), "")
                return Res(1, "", "Not Found")
            # pr view — route by the --json payload
            jidx = args.index("--json") if "--json" in args else -1
            fields = args[jidx + 1] if jidx >= 0 else ""
            seq = w.get("view_seq") or [w.get("view", view())]
            if fields == "reviews":
                payload = w.get("reviews", {"reviews": [review("APPROVED")]})
                if callable(payload):
                    payload = payload()
            else:
                idx = w.get("_view_i", 0)
                w["_view_i"] = idx + 1
                payload = seq[min(idx, len(seq) - 1)]
            return Res(0, json.dumps(payload), "")
        raise AssertionError("unexpected tool: " + tool)


def run_cli(world, argv=("fixture",), env=None):
    """Run the real CLI main() with fakes. Returns (rc, stdout, calls)."""
    runner = FakeRunner(world)
    real_run = subprocess.run
    real_which = CLI.shutil.which
    CLI.subprocess.run = runner
    CLI.shutil.which = lambda p: f"/fake/bin/{os.path.basename(p)}"
    old_env = {k: os.environ.get(k) for k in ("GH", "LEDGER_BIN")}
    for k in ("GH", "LEDGER_BIN"):
        os.environ.pop(k, None)
    if env:
        os.environ.update(env)
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            rc = CLI.main() if not argv else CLI.main_with(argv)
    finally:
        CLI.subprocess.run = real_run
        CLI.shutil.which = real_which
        for k, v in old_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return rc, buf.getvalue(), runner.calls


class CLITest(unittest.TestCase):
    def setUp(self):
        if not hasattr(CLI, "main_with"):
            def main_with(argv):
                sys.argv = ["check-pr-ready", *argv]
                return CLI.main()
            CLI.main_with = staticmethod(main_with)

    # ── positive controls (preserved current behavior) ────────────────

    def test_baseline_ready(self):
        rc, out, calls = run_cli({})
        self.assertEqual(rc, 0, out)
        self.assertIn("READY to merge", out)

    def test_done_status_ok(self):
        rc, out, _ = run_cli({"jobs": [job(status="done")]})
        self.assertEqual(rc, 0, out)

    def test_same_reviewer_cr_then_approved(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [
                review("CHANGES_REQUESTED", login="human", submitted="2026-09-12T00:00:00Z"),
                review("APPROVED", login="human", submitted="2026-09-12T01:00:00Z"),
            ]},
        })
        self.assertEqual(rc, 0, out)

    def test_mixed_reviewers_veto(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [
                review("APPROVED", login="human"),
                review("CHANGES_REQUESTED", login="other", submitted="2026-09-12T02:00:00Z"),
            ]},
        })
        self.assertEqual(rc, 1, out)
        self.assertIn("CHANGES_REQUESTED", out)

    def test_pr_merged_not_ready(self):
        rc, out, _ = run_cli({"view": view(state="MERGED")})
        self.assertEqual(rc, 1, out)

    def test_pr_closed_not_ready(self):
        rc, out, _ = run_cli({"view": view(state="CLOSED")})
        self.assertEqual(rc, 1, out)

    def test_neutral_and_skipped_pass(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[
            check_run("n", conclusion="NEUTRAL"), check_run("s", conclusion="SKIPPED")])})
        self.assertEqual(rc, 0, out)

    # ── job row ────────────────────────────────────────────────────────

    def test_missing_job(self):
        rc, out, _ = run_cli({"jobs": []})
        self.assertEqual(rc, 1, out)

    def test_job_working_not_ready(self):
        for st in ("working", "blocked", "clarifying", "dispatched"):
            rc, out, _ = run_cli({"jobs": [job(status=st)]})
            self.assertEqual(rc, 1, msg=f"{st}: {out}")

    def test_missing_pr(self):
        rc, out, _ = run_cli({"jobs": [job(pr=None)]})
        self.assertEqual(rc, 1, out)

    # ── R01: CI classification ─────────────────────────────────────────

    def test_statuscontext_failure_blocks(self):  # was READY (R01 core)
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[status_context("legacy", "FAILURE")])})
        self.assertEqual(rc, 1, out)
        self.assertIn("CI_FAILED", out)

    def test_statuscontext_error_blocks(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[status_context("legacy", "ERROR")])})
        self.assertEqual(rc, 1, out)

    def test_statuscontext_success_passes(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[status_context("legacy", "SUCCESS")])})
        self.assertEqual(rc, 0, out)

    def test_statuscontext_pending_blocks(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[status_context("legacy", "PENDING")])})
        self.assertEqual(rc, 1, out)
        self.assertIn("CI_PENDING", out)

    def test_statuscontext_unknown_unknown(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[status_context("legacy", "WEIRD")])})
        self.assertEqual(rc, 2, out)
        self.assertIn("CI_UNKNOWN", out)

    def test_checkrun_pending_blocks_without_flag(self):  # was warning+READY
        for st in ("QUEUED", "PENDING", "IN_PROGRESS", "WAITING", "REQUESTED"):
            rc, out, _ = run_cli({"view": view(statusCheckRollup=[check_run("ci", status=st, conclusion=None)])})
            self.assertEqual(rc, 1, msg=f"{st}: {out}")
            self.assertIn("CI_PENDING", out, msg=st)

    def test_allow_pending_qualified_never_green(self):
        rc, out, _ = run_cli(
            {"view": view(statusCheckRollup=[check_run("ci", status="IN_PROGRESS", conclusion=None)])},
            argv=("fixture", "--allow-pending"),
        )
        self.assertEqual(rc, 0, out)
        self.assertIn("QUALIFIED", out)
        self.assertIn("NOT established", out)

    def test_allow_pending_required_gate_qualified(self):
        # a REQUIRED gate that is pending is the flag's exact use case:
        # exit 0 with an explicit qualification banner (I/O matrix row),
        # never a silent EVIDENCE_MISSING blocker (review finding B1)
        rc, out, _ = run_cli(
            {
                "view": view(statusCheckRollup=[check_run("required-ci", status="IN_PROGRESS", conclusion=None)]),
                "api": {"repos/example/demo/branches/main/protection": (
                    "ok", {"required_status_checks": {"contexts": ["required-ci"]}})},
            },
            argv=("fixture", "--allow-pending"),
        )
        self.assertEqual(rc, 0, out)
        self.assertIn("QUALIFIED", out)
        self.assertIn("required-ci", out)
        self.assertIn("NOT established", out)

    def test_mergeable_unrecognized_type_unknown(self):
        rc, out, _ = run_cli({"view": view(mergeable=7)})
        self.assertEqual(rc, 2, out)
        self.assertIn("unrecognized", out)

    def test_null_rollup_unknown(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=None)})
        self.assertEqual(rc, 2, out)
        self.assertIn("statusCheckRollup", out)

    def test_reviews_nonobject_entry_unknown(self):
        rc, out, _ = run_cli({"reviews": {"reviews": ["boom"]}})
        self.assertEqual(rc, 2, out)
        self.assertIn("non-object", out)

    def test_bare_number_non_github_remote_refused(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr="7", repo="example/demo")],
            "remote": "git@ghe.corp:example/demo.git",
        })
        self.assertEqual(rc, 2, out)
        self.assertIn("non-github host", out)

    def test_checkrun_action_required_blocks(self):  # was READY
        for concl in ("ACTION_REQUIRED", "STARTUP_FAILURE", "STALE"):
            rc, out, _ = run_cli({"view": view(statusCheckRollup=[check_run("ci", conclusion=concl)])})
            self.assertEqual(rc, 1, msg=f"{concl}: {out}")
            self.assertIn("CI_FAILED", out, msg=concl)

    def test_checkrun_failure_cancelled_timedout_error_block(self):
        for concl in ("FAILURE", "CANCELLED", "TIMED_OUT", "ERROR"):
            rc, out, _ = run_cli({"view": view(statusCheckRollup=[check_run("ci", conclusion=concl)])})
            self.assertEqual(rc, 1, msg=f"{concl}: {out}")

    def test_checkrun_unknown_conclusion_unknown(self):
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[check_run("ci", conclusion="GIBBERISH")])})
        self.assertEqual(rc, 2, out)
        rc, out, _ = run_cli({"view": view(statusCheckRollup=[check_run("ci", conclusion=None)])})
        self.assertEqual(rc, 2, out)

    def test_no_checks_with_gates_established_none_ready(self):
        rc, out, _ = run_cli({
            "view": view(statusCheckRollup=[]),
            "api": {},  # 404 both channels → positively no gates
        })
        self.assertEqual(rc, 0, out)

    def test_no_checks_gates_unreadable_unknown(self):
        rc, out, _ = run_cli({
            "view": view(statusCheckRollup=[]),
            "__all_forbidden__": True,
        })
        self.assertEqual(rc, 2, out)
        self.assertIn("CI_UNKNOWN", out)

    def test_missing_required_check_blocks(self):
        rc, out, _ = run_cli({
            "view": view(statusCheckRollup=[check_run("other-check")]),
            "api": {
                "repos/example/demo/branches/main/protection":
                    ("ok", {"required_status_checks": {"contexts": ["required-ci"]}}),
            },
        })
        self.assertEqual(rc, 1, out)
        self.assertIn("required check", out)

    def test_required_check_present_and_passing_ready(self):
        rc, out, _ = run_cli({
            "api": {
                "repos/example/demo/branches/main/protection":
                    ("ok", {"required_status_checks": {"contexts": ["required-ci"]}}),
            },
        })
        self.assertEqual(rc, 0, out)

    def test_ruleset_required_checks_honored(self):
        rc, out, _ = run_cli({
            "api": {
                "repos/example/demo/branches/main/protection": ("not-found", None),
                "repos/example/demo/rules/branches/main":
                    ("ok", [{"type": "required_status_checks",
                             "parameters": {"required_status_checks": [{"context": "gate-x"}]}}]),
            },
        })
        self.assertEqual(rc, 1, out)
        self.assertIn("gate-x", out)

    # ── R02: head binding ──────────────────────────────────────────────

    def test_stale_head_approval_blocks(self):  # was READY
        rc, out, _ = run_cli({"reviews": {"reviews": [review("APPROVED", at=HEAD_B)]}})
        self.assertEqual(rc, 1, out)
        self.assertIn("REVIEW_STALE", out)

    def test_review_decision_required_blocks(self):
        rc, out, _ = run_cli({"view": view(reviewDecision="REVIEW_REQUIRED")})
        self.assertEqual(rc, 1, out)

    def test_review_decision_changes_blocks(self):
        rc, out, _ = run_cli({"view": view(reviewDecision="CHANGES_REQUESTED")})
        self.assertEqual(rc, 1, out)

    def test_head_moves_between_calls_unknown(self):
        rc, out, _ = run_cli({"view_seq": [view(), view(headRefOid=HEAD_B)]})
        self.assertEqual(rc, 2, out)
        self.assertIn("STALE", out)

    def test_ci_fails_between_two_calls_unknown(self):
        rc, out, _ = run_cli({"view_seq": [view(), view(statusCheckRollup=[check_run("required-ci", conclusion="FAILURE")])]})
        self.assertEqual(rc, 2, out)
        self.assertIn("STALE, never READY", out)

    def test_closed_between_two_calls_unknown(self):
        rc, out, _ = run_cli({"view_seq": [view(), view(state="CLOSED")]})
        self.assertEqual(rc, 2, out)

    def test_reread_gh_error_unknown(self):
        # first view+reviews succeed (2 gh calls), api 404s (2 more), the
        # head re-read (5th gh call) dies -> UNKNOWN, never READY
        rc, out, _ = run_cli({"view_seq": [view()], "fail_gh_after": 4})
        self.assertEqual(rc, 2, msg=out)
        self.assertIn("UNKNOWN", out)

    # ── R03: canonical Perkins actor ───────────────────────────────────

    def test_human_approval_with_pr_review_1_mismatch(self):
        rc, out, _ = run_cli({"reviews": {"reviews": [review("APPROVED", login="human")]}})
        self.assertEqual(rc, 1, out)
        self.assertIn("REVIEWER_MISMATCH", out)

    def test_substring_impostor_rejected(self):
        for login in ("not-perkins-bot", "perkins-impostor", "Perkins-Review[bot]", "the-perkins-review-bot"):
            rc, out, _ = run_cli({"reviews": {"reviews": [review("APPROVED", login=login)]}})
            self.assertEqual(rc, 1, msg=f"{login}: {out}")
            self.assertIn("REVIEWER_MISMATCH", out, msg=login)

    def test_exact_perkins_actor_passes(self):
        rc, out, _ = run_cli({})
        self.assertEqual(rc, 0, out)

    def test_missing_author_not_approval(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [review("APPROVED", login=None)]},
        })
        self.assertEqual(rc, 1, out)
        self.assertIn("missing author", out)

    def test_perkins_flag_enforced_when_pr_review_0(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [review("APPROVED", login="human")]},
        }, argv=("fixture", "--require-perkins"))
        self.assertEqual(rc, 1, out)
        self.assertIn("REVIEWER_MISMATCH", out)

    def test_human_route_still_works_when_pr_review_0(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [review("APPROVED", login="human")]},
        })
        self.assertEqual(rc, 0, out)

    def test_pr_review_string_value(self):
        rc, out, _ = run_cli({"jobs": [job(pr_review="1")]})
        self.assertEqual(rc, 0, out)

    # ── review-stance semantics preserved ─────────────────────────────

    def test_approved_then_cr_same_reviewer_blocks(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [
                review("APPROVED", login="human", submitted="2026-09-12T00:00:00Z"),
                review("CHANGES_REQUESTED", login="human", submitted="2026-09-12T01:00:00Z"),
            ]},
        })
        self.assertEqual(rc, 1, out)

    def test_commented_does_not_clear_stance(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [
                review("APPROVED", login="human", submitted="2026-09-12T00:00:00Z"),
                review("COMMENTED", login="human", submitted="2026-09-12T01:00:00Z"),
            ]},
        })
        self.assertEqual(rc, 0, out)

    def test_no_reviews_blocks(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)], "reviews": {"reviews": []}})
        self.assertEqual(rc, 1, out)

    def test_missing_timestamps_input_order(self):
        rc, out, _ = run_cli({
            "jobs": [job(pr_review=0)],
            "reviews": {"reviews": [
                review("APPROVED", login="human", submitted=""),
                review("CHANGES_REQUESTED", login="human", submitted=""),
            ]},
        })
        self.assertEqual(rc, 1, out)

    # ── R04: identity / boundary contracts ────────────────────────────

    def test_remote_parsing_all_common_forms(self):
        for remote in (
            "git@github.com:example/demo.git",
            "https://github.com/example/demo.git",
            "https://github.com/example/demo",
            "ssh://git@github.com/example/demo.git",
            "git://github.com/example/demo.git",
        ):
            rc, out, _ = run_cli({"remote": remote, "jobs": [job(pr="7", repo="")]})
            self.assertNotIn("IDENTITY_MISMATCH", out, msg=remote)
            self.assertIn("repo slug: example/demo", out, msg=remote)

    def test_bare_number_with_https_remote_proceeds(self):
        rc, out, calls = run_cli({"remote": "https://github.com/example/demo.git", "jobs": [job(pr="7", repo="")]})
        self.assertEqual(rc, 0, out)
        self.assertTrue(any("--repo" in c and "example/demo" in c for c in calls))

    def test_bare_number_explicit_slug(self):
        rc, out, calls = run_cli({"remote": None, "jobs": [job(pr="7", repo="example/demo")]})
        self.assertEqual(rc, 0, out)

    def test_bare_number_no_repo_refuses_ambient(self):
        rc, out, calls = run_cli({"remote": None, "jobs": [job(pr="7", repo="")]})
        self.assertEqual(rc, 2, out)
        self.assertIn("ambient", out)
        self.assertFalse(any(c[1:3] == ["pr", "view"] for c in calls))

    def test_wrong_owner_full_url_rejected(self):
        rc, out, _ = run_cli({"remote": "git@github.com:example/OTHER.git"})
        self.assertEqual(rc, 2, out)
        self.assertIn("identity conflict", out)

    def test_ledger_url_conflict_rejected(self):
        rc, out, _ = run_cli({"jobs": [job(repo="example/OTHER")]})
        self.assertEqual(rc, 2, out)
        self.assertIn("identity conflict", out)

    def test_non_github_url_host_rejected(self):
        rc, out, _ = run_cli({"jobs": [job(pr="https://ghe.example.com/example/demo/pull/7")]})
        self.assertEqual(rc, 2, out)
        self.assertIn("not github.com", out)

    def test_malformed_url_rejected(self):
        rc, out, _ = run_cli({"jobs": [job(pr="not-a-url")]})
        self.assertEqual(rc, 2, out)

    def test_gh_override_env_honored(self):
        rc, out, calls = run_cli({}, env={"GH": "custom-gh"})
        self.assertEqual(rc, 0, out)
        self.assertTrue(any(os.path.basename(c[0]) == "custom-gh" for c in calls))

    def test_ledger_override_env_honored(self):
        rc, out, calls = run_cli({}, env={"LEDGER_BIN": "/fake/bin/fake-ledger"})
        self.assertEqual(rc, 0, out)
        self.assertTrue(any("fake-ledger" in c[0] for c in calls))

    def test_ledger_flag_wins_env(self):
        rc, out, calls = run_cli({}, argv=("fixture", "--ledger", "/fake/bin/flag-ledger"), env={"LEDGER_BIN": "/fake/bin/env-ledger"})
        self.assertEqual(rc, 0, out)
        self.assertTrue(any("flag-ledger" in c[0] for c in calls))
        self.assertFalse(any("env-ledger" in c[0] for c in calls))

    def test_ledger_command_error(self):
        rc, out, _ = run_cli({"ledger_rc": 1})
        self.assertEqual(rc, 2, out)

    def test_ledger_non_json(self):
        rc, out, _ = run_cli({"ledger_raw": "NOT JSON{"})
        self.assertEqual(rc, 2, out)

    def test_ledger_invalid_schema(self):
        rc, out, _ = run_cli({"ledger_raw": "{\"a\": 1}"})
        self.assertEqual(rc, 2, out)

    def test_bad_pr_review_value(self):
        rc, out, _ = run_cli({"jobs": [job(pr_review="abc")]})
        self.assertEqual(rc, 2, out)

    def test_gh_command_error(self):
        rc, out, _ = run_cli({"gh_rc": 1})
        self.assertEqual(rc, 2, out)

    def test_gh_non_json(self):
        rc, out, _ = run_cli({"gh_raw": "}{ not json"})
        self.assertEqual(rc, 2, out)

    def test_gh_invalid_schema(self):
        rc, out, _ = run_cli({"gh_raw": "[1,2,3]"})
        self.assertEqual(rc, 2, out)

    def test_reviews_invalid_schema(self):
        w = {"gh_raw": "[1,2,3]"}
        # gh_raw applies to ALL gh calls incl. view — expect UNKNOWN
        rc, out, _ = run_cli(w)
        self.assertEqual(rc, 2, out)

    def test_missing_gh_executable(self):
        real = CLI.shutil.which
        CLI.shutil.which = lambda p: None
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                sys.argv = ["check-pr-ready", "fixture"]
                rc = CLI.main()
        finally:
            CLI.shutil.which = real
        self.assertEqual(rc, 2, buf.getvalue())
        self.assertIn("gh tool not found", buf.getvalue())

    def test_hung_call_bounded(self):
        rc, out, _ = run_cli({"fail_tool": "ledger"})
        self.assertEqual(rc, 2, out)
        self.assertIn("timed out", out)

    def test_sparse_pr_unknown(self):
        rc, out, _ = run_cli({"view": {"state": "OPEN"}})
        self.assertEqual(rc, 2, out)
        self.assertIn("EVIDENCE_MISSING", out)

    def test_null_mergeability_not_ready(self):
        rc, out, _ = run_cli({"view": view(mergeable=None)})
        self.assertEqual(rc, 1, out)

    def test_unknown_mergeability_not_ready(self):
        rc, out, _ = run_cli({"view": view(mergeable="UNKNOWN")})
        self.assertEqual(rc, 1, out)

    def test_conflicting_not_ready(self):
        rc, out, _ = run_cli({"view": view(mergeable="CONFLICTING")})
        self.assertEqual(rc, 1, out)

    def test_draft_not_ready(self):
        rc, out, _ = run_cli({"view": view(isDraft=True)})
        self.assertEqual(rc, 1, out)


class CoreUnitTest(unittest.TestCase):
    """Direct pure-evaluator unit cases (no CLI/collection involved)."""

    def test_parse_remote_forms(self):
        for url, slug in [
            ("git@github.com:example/demo.git", "example/demo"),
            ("https://github.com/example/demo.git", "example/demo"),
            ("ssh://git@github.com/example/demo.git", "example/demo"),
            ("git://github.com/example/demo", "example/demo"),
            ("example/demo", "example/demo"),
            ("https://github.com/example/demo/", "example/demo"),
        ]:
            r = CORE.parse_remote(url)
            self.assertIsNotNone(r, url)
            self.assertEqual(f"{r[1]}/{r[2]}", slug, url)
        self.assertIsNone(CORE.parse_remote("https://github.com/onlyrepo"))
        self.assertIsNone(CORE.parse_remote(""))
        self.assertIsNone(CORE.parse_remote(None))

    def test_parse_remote_host(self):
        self.assertEqual(CORE.parse_remote("git@ghe.corp:example/demo.git")[0], "ghe.corp")

    def test_result_precedence_blocker_over_unknown(self):
        r = CORE.Result()
        r.unknowns.append(("CI_UNKNOWN", "gap"))
        r.blockers.append(("CI_FAILED", "boom"))
        self.assertEqual(r.status, "NOT_READY")
        self.assertEqual(r.exit_code(), 1)

    def test_result_unknown_beats_ready(self):
        r = CORE.Result()
        r.unknowns.append(("CI_UNKNOWN", "gap"))
        self.assertEqual(r.status, "UNKNOWN")

    def test_classify_check_shape_fallbacks(self):
        # no __typename: shape heuristics
        self.assertEqual(CORE.classify_check({"state": "FAILURE", "context": "x"})[1], "FAIL")
        self.assertEqual(CORE.classify_check({"status": "IN_PROGRESS", "name": "x"})[1], "PENDING")
        self.assertEqual(CORE.classify_check("garbage")[1], "UNKNOWN")

    def test_missing_review_commit_not_counted(self):
        res = CORE.evaluate(
            job(),
            view(),
            {"reviews": [{"state": "APPROVED", "author": {"login": "perkins-review[bot]"},
                          "submittedAt": "2026-09-12T00:00:00Z", "commit": None}]},
            "git@github.com:example/demo.git", [], False, False,
        )
        self.assertIn("EVIDENCE_MISSING", res.reasons)
        self.assertNotEqual(res.status, "READY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
