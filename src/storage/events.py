"""Structured event logging."""
import csv
import json
from pathlib import Path
from datetime import datetime


def log_event(logs_dir: Path, event: dict):
    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    event = {"ts": datetime.now().isoformat(), **event}
    with open(logs_dir / "events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")


def log_false_alarm(logs_dir: Path, row: dict):
    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / "false_alarms.csv"
    new = not path.exists()
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if new:
            w.writeheader()
        w.writerow(row)