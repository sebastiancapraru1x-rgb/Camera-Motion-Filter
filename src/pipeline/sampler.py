"""Frame sampling helper."""
from pathlib import Path
import cv2


def sample_frames(video_path: Path, every: int = 4):
    """Yield (frame_index, frame) every `every` frames."""
    cap = cv2.VideoCapture(str(video_path))
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % every == 0:
            yield idx, frame
        idx += 1
    cap.release()