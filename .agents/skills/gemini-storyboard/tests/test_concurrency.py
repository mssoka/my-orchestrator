"""Real process lock/admission test; MOCK path with network denied in children."""
import json
from pathlib import Path
import subprocess
import sys

from conftest import SCRIPT, save, sb


def test_two_processes_cannot_overspend(project, tmp_path):
    runs = []
    for i in range(2):
        m, path = project(run_id=f"concurrent-{i}")
        m["budget"] = {"limit_usd": "2.031616", "max_attempts": 1}
        save(path, m)
        runs.append(sb.plan(path, tmp_path / "runs"))
    trap = tmp_path / "trap"
    trap.mkdir()
    (trap / "sitecustomize.py").write_text('import socket\ndef deny(*a,**k): raise RuntimeError("NETWORK FORBIDDEN")\nsocket.socket.connect=deny\nsocket.create_connection=deny\nsocket.getaddrinfo=deny\n')
    env = {"PATH": str(Path(sys.executable).parent), "PYTHONPATH": str(trap), "PYTHONNOUSERSITE": "1"}
    budget = tmp_path / "budget"
    processes = [subprocess.Popen([sys.executable, str(SCRIPT), "generate", "--run", str(run), "--mock", "--budget-dir", str(budget)], env=env, cwd=tmp_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for run in runs]
    try:
        outputs = [p.communicate(timeout=30) for p in processes]
        assert sorted(p.returncode for p in processes) == [0, 2], outputs
        rejected = next(err for p, (_, err) in zip(processes, outputs) if p.returncode == 2)
        assert "budget.max_attempts" in rejected or "lock: busy" in rejected
        rows = [json.loads(line) for line in (budget / "attempts.jsonl").read_text().splitlines()]
        assert len(rows) == 1 and rows[0]["reserve_usd"] == "2.031616"
        assert len(list((tmp_path / "runs").glob("*/*/attempts/*/final.png"))) == 1
    finally:
        for p in processes:
            if p.poll() is None:
                p.kill()
            p.wait()
