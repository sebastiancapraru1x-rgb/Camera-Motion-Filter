"""Direct video URL source (Pexels/CC0/etc.)."""
import requests
from pathlib import Path

from .base import VideoSource, Clip


class UrlSource(VideoSource):
    name = "url"

    def __init__(self, urls, inbox_dir="data/inbox"):
        self.urls = list(urls)
        self.inbox_dir = Path(inbox_dir)

    def list_clips(self):
        for i, u in enumerate(self.urls):
            yield Clip(id=f"url_{i}", path=None, camera_id="url", timestamp="")  # type: ignore

    def download(self, clip: Clip) -> "Path":
        target_url = url or self.urls[int(clip.id.split("_")[1])]
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        dest = self.inbox_dir / f"{clip.id}.mp4"
        r = requests.get(target_url, stream=True, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        clip.path = dest
        return dest