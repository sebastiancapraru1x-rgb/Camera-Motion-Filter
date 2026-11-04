"""RTSP source — for any camera exposing RTSP (future-proof)."""
from .base import VideoSource, Clip


class RtspSource(VideoSource):
    name = "rtsp"

    def __init__(self, url: str, camera_id: str = "rtsp"):
        self.url = url
        self.camera_id = camera_id

    def list_clips(self):
        yield Clip(id="rtsp_clip", path=None, camera_id=self.camera_id, timestamp="")  # type: ignore

    def download(self, clip: Clip):
        raise NotImplementedError("record via cv2.VideoCapture(RTSP) in Phase 1")