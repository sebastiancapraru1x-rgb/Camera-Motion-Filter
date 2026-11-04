"""Local file source — dev default."""
from pathlib import Path
from .base import VideoSource, Clip


class FileSource(VideoSource):
    name = "file"

    def __init__(self, root: str):
        self.root = Path(root)

    def list_clips(self):
        for p in sorted(self.root.glob("*.mp4")):
            yield Clip(id=p.stem, path=p, camera_id="file", timestamp="")

    def download(self, clip: Clip) -> Path:
        return clip.path  # already local