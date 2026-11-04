"""Stats/events endpoints for the dashboard."""
import json
import os
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.storage.paths import paths

router = APIRouter()


def _read_events():
    p = paths()["logs"] / "events.jsonl"
    if not p.exists():
        return []
    out = []
    with open(p) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


@router.get("/stats")
def stats():
    events = _read_events()
    total = len(events)
    true = sum(1 for e in events if e.get("status") == "TRUE")
    false = total - true
    by_camera = {}
    for e in events:
        cid = e.get("camera_id", "default")
        by_camera.setdefault(cid, {"true": 0, "false": 0})
        if e.get("status") == "TRUE":
            by_camera[cid]["true"] += 1
        else:
            by_camera[cid]["false"] += 1
    # disk usage of clips
    disk_bytes = 0
    for sub in ("alerts", "inbox", "processing", "false_alarms"):
        d = paths()[sub]
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file():
                    disk_bytes += p.stat().st_size
    alerts_dir = paths()["alerts"]
    alert_files = sorted([p.name for p in alerts_dir.glob("*.jpg")]) if alerts_dir.exists() else []
    return {
        "total": total,
        "true": true,
        "false": false,
        "false_rate": round(false / total, 4) if total else 0.0,
        "by_camera": by_camera,
        "disk_usage_mb": round(disk_bytes / (1024 * 1024), 2),
        "disk_cap_gb": 3.0,
        "alerts": alert_files,
    }


@router.get("/events")
def events(limit: int = 50):
    ev = _read_events()
    return list(reversed(ev))[:limit]


@router.get("/alerts")
def alerts():
    d = paths()["alerts"]
    if not d.exists():
        return []
    return sorted([p.name for p in d.glob("*.jpg")])


@router.get("/alerts/{filename}")
def alert_image(filename: str):
    f = paths()["alerts"] / filename
    if not f.exists():
        return {"error": "not found"}
    return FileResponse(f)