"""Webcam source — instant local testing."""
from pathlib import Path

from .base import VideoSource, Clip


class WebcamSource(VideoSource):
    name = "webcam"

    def __init__(self, device_index: int = 0, seconds: int = 5, inbox_dir="data/inbox"):
        self.device_index = device_index
        self.seconds = seconds
        self.inbox_dir = Path(inbox_dir)

    def list_clips(self):
        yield Clip(id="webcam_clip", path=None, camera_id="webcam", timestamp="")  # type: ignore

    def download(self, clip: Clip):
        import cv2
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        dest = self.inbox_dir / "webcam_clip.mp4"
        cap = cv2.VideoCapture(self.device_index)
        if not cap.isOpened():
            raise RuntimeError("Cannot open webcam")
        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(dest), fourcc, fps, (w, h))
        for _ in range(int(fps * self.seconds)):
            ok, frame = cap.read()
            if not ok:
                break
            out.write(frame)
        cap.release()
        out.release()
        clip.path = dest
        return dest