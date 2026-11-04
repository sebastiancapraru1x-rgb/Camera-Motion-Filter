"""Discord webhook alert with best-frame thumbnail."""
import os
import requests


def send_alert(webhook_url: str, camera_id: str, label: str, conf: float, thumbnail_path: str = None):
    content = f"🚨 Real motion on **{camera_id}**: {label} ({conf:.0%})"
    if not webhook_url:
        print("[alert skipped]", content)
        return
    files = {}
    if thumbnail_path and os.path.exists(thumbnail_path):
        files["file"] = open(thumbnail_path, "rb")
    requests.post(webhook_url, data={"content": content}, files=files or None)