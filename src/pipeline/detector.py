"""YOLOv8n detector wrapper (CPU)."""
from pathlib import Path


class Detector:
    def __init__(self, model_name: str = "models/yolov8n.pt", conf: float = 0.6):
        self.model_name = model_name
        self.conf = conf
        self._model = None

    def load(self):
        from ultralytics import YOLO
        self._model = YOLO(self.model_name)

    def track(self, frame):
        if self._model is None:
            self.load()
        results = self._model.track(frame, conf=self.conf, persist=True, verbose=False)
        out = []
        for r in results:
            if r.boxes is None:
                continue
            names = r.names
            for b in r.boxes:
                tid = int(b.id[0]) if b.id is not None else None
                cls_id = int(b.cls[0])
                out.append({
                    "id": tid,
                    "class": names[cls_id],
                    "conf": float(b.conf[0]),
                    "bbox": [float(x) for x in b.xyxy[0].tolist()],
                })
        return out
    def detect(self, frame):
        if self._model is None:
            self.load()
        results = self._model(frame, conf=self.conf, verbose=False)
        out = []
        for r in results:
            names = r.names
            if r.boxes is None:
                continue
            for b in r.boxes:
                cls_id = int(b.cls[0])
                out.append({
                    "class": names[cls_id],
                    "conf": float(b.conf[0]),
                    "bbox": [float(x) for x in b.xyxy[0].tolist()],
                })
        return out