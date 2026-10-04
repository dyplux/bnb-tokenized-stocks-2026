#!/usr/bin/env python3
"""Observe the frozen collector; restart only after its process exits."""

import argparse
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "data/market_hours"
COLLECTOR = ROOT / "scripts/rwa_research.py"
PID = MARKET / "watchdog.pid"
LOCK = MARKET / "watchdog.lock"
LOG = MARKET / "watchdog.log"
EVENTS = MARKET / "watchdog-events.jsonl"
STATUS = MARKET / "watchdog-status.json"
INTERVAL = 300
CHECK_EVERY = 60


def now_utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def process_command(pid):
    if not isinstance(pid, int) or pid < 1:
        return ""
    result = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True,
                            text=True, timeout=5, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def event(kind, **fields):
    record = {"at": now_utc(), "kind": kind, **fields}
    with EVENTS.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps(record, sort_keys=True), flush=True)


def write_status(payload):
    temporary = STATUS.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, STATUS)


def probe():
    try:
        result = subprocess.run([sys.executable, str(COLLECTOR), "health"], cwd=ROOT,
                                capture_output=True, text=True, timeout=20, check=False)
        health = json.loads(result.stdout)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return "UNKNOWN", None
    if health.get("process_alive") is False:
        return "DEAD", health
    pid = health.get("pid")
    command = process_command(pid)
    if not command or str(COLLECTOR) not in command or " loop --interval 300" not in command:
        return "PID_MISMATCH", health
    if result.returncode != 0:
        return "DEGRADED", health
    return "HEALTHY", health


def restart_collector():
    result = subprocess.run([sys.executable, str(COLLECTOR), "start", "--interval", str(INTERVAL),
                             "--keep-awake"], cwd=ROOT, capture_output=True, text=True,
                            timeout=20, check=False)
    if result.returncode != 0:
        event("RESTART_FAILED", exit_code=result.returncode)
        return False
    event("RESTART_REQUESTED", interval_seconds=INTERVAL, keep_awake=True)
    return True


def loop():
    MARKET.mkdir(parents=True, exist_ok=True)
    lock_fd = os.open(str(LOCK), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("watchdog already running")
    PID.write_text(str(os.getpid()) + "\n", encoding="utf-8")
    event("WATCHDOG_STARTED", pid=os.getpid(), check_every_seconds=CHECK_EVERY,
          restart_budget=1)
    prior_state = None
    restart_budget = 1
    while True:
        state, health = probe()
        if state != prior_state:
            event("COLLECTOR_STATE", state=state,
                  collector_pid=health.get("pid") if health else None)
            prior_state = state
        if state == "DEAD" and restart_budget:
            restart_budget -= 1
            if restart_collector():
                time.sleep(5)
                state, health = probe()
                event("POST_RESTART_CHECK", state=state,
                      collector_pid=health.get("pid") if health else None)
                prior_state = state
        write_status({"checked_at": now_utc(), "watchdog_pid": os.getpid(),
                      "watchdog_state": "RUNNING", "collector_state": state,
                      "restart_budget_remaining": restart_budget, "collector_health": health})
        time.sleep(CHECK_EVERY)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("start", "loop", "status", "stop"))
    command = parser.parse_args().command
    MARKET.mkdir(parents=True, exist_ok=True)
    pid = int(PID.read_text()) if PID.exists() else None
    current = process_command(pid)
    ours = bool(current and str(Path(__file__).resolve()) in current and " loop" in current)
    if command == "status":
        saved = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
        print(json.dumps({"watchdog_alive": ours, **saved}, sort_keys=True))
        if not ours or saved.get("collector_state") != "HEALTHY":
            raise SystemExit(1)
        return
    if command == "stop":
        if ours:
            os.kill(pid, signal.SIGTERM)
            print(json.dumps({"stopped_watchdog_pid": pid, "collector_untouched": True}))
        else:
            print(json.dumps({"watchdog_alive": False, "collector_untouched": True}))
        return
    if command == "start":
        if ours:
            print(json.dumps({"watchdog_already_running": True, "pid": pid}))
            return
        if current:
            raise SystemExit("watchdog PID belongs to a different process")
        with LOG.open("a", encoding="utf-8") as stream:
            child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "loop"],
                                     cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stream,
                                     stderr=subprocess.STDOUT, start_new_session=True)
        print(json.dumps({"watchdog_started_pid": child.pid,
                          "status_command": "python3 scripts/collector_watchdog.py status"}))
        return
    loop()


if __name__ == "__main__":
    main()
