"""Retention + disk-cap enforcement."""
from pathlib import Path
import time


def purge_older_than(folder: Path, days: int):
    folder = Path(folder)
    if not folder.exists():
        return
    cutoff = time.time() - days * 86400
    for p in folder.iterdir():
        if p.is_file() and p.stat().st_mtime < cutoff:
            p.unlink()


def enforce_disk_cap(folders, cap_gb: float):
    files = []
    for f in folders:
        f = Path(f)
        if not f.exists():
            continue
        for p in f.rglob("*.mp4"):
            files.append(p)
    files.sort(key=lambda p: p.stat().st_mtime)
    cap_bytes = cap_gb * 1024 ** 3
    total = sum(p.stat().st_size for p in files)
    for p in files:
        if total <= cap_bytes:
            break
        try:
            total -= p.stat().st_size
            p.unlink()
        except OSError:
            pass