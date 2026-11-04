"""Decision rules + helpers for zones/time."""
from pathlib import Path
import yaml
from datetime import datetime


def load_rules(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def point_in_polygon(point, poly):
    x, y = point
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def in_ignore_zone(bbox, zones):
    if not zones:
        return False
    cx = (bbox[0] + bbox[2]) / 2
    cy = (bbox[1] + bbox[3]) / 2
    for zone in zones:
        if point_in_polygon((cx, cy), zone):
            return True
    return False


def is_active_hour(active_hours):
    if not active_hours:
        return True
    if active_hours == ["00:00", "23:59"]:
        return True
    now = datetime.now().strftime("%H:%M")
    start, end = active_hours[0], active_hours[1]
    if start <= end:
        return start <= now <= end
    return now >= start or now <= end


def is_true_alarm(frames_detections, min_consecutive):
    max_run = 0
    run = 0
    collected = []
    for dets in frames_detections:
        if dets:
            run += 1
            max_run = max(max_run, run)
            collected.extend(dets)
        else:
            run = 0
    true = max_run >= min_consecutive
    best = {}
    for d in collected:
        name = d["class"]
        c = d["conf"]
        if name not in best or c > best[name]:
            best[name] = c
    labels = [(k, v) for k, v in best.items()]
    return true, labels