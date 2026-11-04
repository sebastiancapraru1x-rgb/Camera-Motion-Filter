"""Storage paths + retention helpers."""
from pathlib import Path
import os


def project_root() -> Path:
    return Path(os.getenv("STORAGE_ROOT", ".")).resolve()


def paths(root: Path = None):
    root = root or project_root()
    return {
        "inbox": root / "data" / "inbox",
        "processing": root / "data" / "processing",
        "alerts": root / "data" / "alerts",
        "false_alarms": root / "data" / "false_alarms",
        "archive": root / "data" / "archive",
        "logs": root / "logs",
        "models": root / "models",
    }