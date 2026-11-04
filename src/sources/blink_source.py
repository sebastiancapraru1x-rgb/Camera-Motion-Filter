"""Blink adapter — fetches motion clips from Blink cloud.

Requires: pip install blinkpy
Free to use, but Blink cloud clip access may require a subscription
for extended retention beyond the free tier.
"""
import asyncio
from pathlib import Path

import requests

from .base import VideoSource, Clip


class BlinkSource(VideoSource):
    name = "blink"

    def __init__(self, username: str, password: str, inbox_dir="data/inbox"):
        self.username = username
        self.password = password
        self.inbox_dir = Path(inbox_dir)
        self._blink = None
        self._clip_urls = {}  # clip_id -> download URL

    async def _connect(self):
        if self._blink is None:
            try:
                from blinkpy.blinkpy import Blink
            except ImportError:
                raise ImportError(
                    "blinkpy is not installed. Run: pip install blinkpy"
                )
            self._blink = Blink({"username": self.username, "password": self.password})
            await self._blink.start()
        return self._blink

    def list_clips(self):
        """Yield recent motion clips from all Blink cameras."""
        blink = asyncio.run(self._connect())
        for camera_name, camera in blink.cameras.items():
            try:
                activity = camera.recent_activity() or []
                for event in activity:
                    if isinstance(event, dict):
                        clip_url = event.get("video", "") or event.get("clip", "")
                        ts = event.get("time", "") or event.get("created_at", "")
                    else:
                        clip_url = getattr(event, "video", "") or getattr(event, "clip", "")
                        ts = getattr(event, "time", "") or getattr(event, "created_at", "")

                    if not clip_url:
                        continue

                    clip_id = f"blink_{camera_name}_{str(ts).replace(' ', '_').replace(':', '')}"
                    self._clip_urls[clip_id] = clip_url

                    yield Clip(
                        id=clip_id,
                        path=None,
                        camera_id=camera_name,
                        timestamp=str(ts),
                    )
            except Exception as e:
                print(f"[blink] Skipping camera {camera_name}: {e}")
                continue

    def download(self, clip: Clip) -> Path:
        """Download a Blink clip to the local inbox."""
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        dest = self.inbox_dir / f"{clip.id}.mp4"

        url = self._clip_urls.get(clip.id, "")
        if not url:
            raise RuntimeError(f"No download URL found for clip {clip.id}")

        r = requests.get(url, stream=True, timeout=120)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        clip.path = dest
        return dest