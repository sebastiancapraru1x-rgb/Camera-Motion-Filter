"""Orchestrates: sample -> track/detect -> filter -> decide -> thumbnail."""
from pathlib import Path
import cv2

from .sampler import sample_frames
from .rules import is_true_alarm, in_ignore_zone, is_active_hour


class Pipeline:
    def __init__(self, detector, target_classes, conf=0.6, min_consecutive=3, every=4,
                 ignore_zones=None, active_hours=None, use_tracking=True):
        self.detector = detector
        self.target_classes = target_classes
        self.conf = conf
        self.min_consecutive = min_consecutive
        self.every = every
        self.ignore_zones = ignore_zones or []
        self.active_hours = active_hours
        self.use_tracking = use_tracking

    def run(self, video_path: Path, camera_id: str = "default", thumbnail_path=None):
        if self.active_hours and not is_active_hour(self.active_hours):
            return {
                "camera_id": camera_id,
                "video": str(video_path),
                "frames_sampled": 0,
                "status": "FALSE",
                "detections": [],
                "thumbnail": None,
                "reason": "outside active hours",
            }

        frames = list(sample_frames(video_path, self.every))
        frames_dets = []
        best_frame = None
        best_score = -1.0
        for idx, frame in frames:
            dets = self.detector.track(frame) if self.use_tracking else self.detector.detect(frame)
            valid = []
            for d in dets:
                if d["class"] not in self.target_classes:
                    continue
                if d["conf"] < self.conf:
                    continue
                if in_ignore_zone(d["bbox"], self.ignore_zones):
                    continue
                valid.append(d)
            frames_dets.append(valid)
            score = sum(d["conf"] for d in valid)
            if score > best_score:
                best_score = score
                best_frame = frame.copy()

        true, labels = is_true_alarm(frames_dets, self.min_consecutive)
        thumb = None
        if true and thumbnail_path is not None and best_frame is not None:
            tp = Path(thumbnail_path)
            tp.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(tp), best_frame)
            thumb = str(tp)

        return {
            "camera_id": camera_id,
            "video": str(video_path),
            "frames_sampled": len(frames),
            "status": "TRUE" if true else "FALSE",
            "detections": [{"class": c, "conf": round(float(cf), 3)} for c, cf in labels],
            "thumbnail": thumb,
        }