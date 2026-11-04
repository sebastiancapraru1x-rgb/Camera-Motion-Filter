"""Evaluate detection pipeline on labeled clips.

Labels by folder: eval/data/true  -> ground truth TRUE
                  eval/data/false -> ground truth FALSE
"""
import argparse
import json
import csv
import json
from pathlib import Path

from src.pipeline.detector import Detector
from src.pipeline.pipeline import Pipeline


def collect_labeled(root: Path):
    items = []
    for label, truth in [("true", True), ("false", False)]:
        d = root / label
        if not d.exists():
            continue
        for p in sorted(d.glob("*.mp4")):
            items.append((p, truth))
    return items


def evaluate(items, conf, min_frames, every, target_classes):
    detector = Detector(conf=conf)
    pipeline = Pipeline(
        detector=detector,
        target_classes=target_classes,
        conf=conf,
        min_consecutive=min_frames,
        every=every,
        use_tracking=True,
    )
    tp = fp = tn = fn = 0
    rows = []
    for path, truth in items:
        res = pipeline.run(path, camera_id="eval")
        pred = (res["status"] == "TRUE")
        if truth and pred:
            tp += 1
        elif (not truth) and pred:
            fp += 1
        elif (not truth) and (not pred):
            tn += 1
        elif truth and (not pred):
            fn += 1
        rows.append({
            "file": str(path),
            "truth": truth,
            "pred": pred,
            "status": res["status"],
            "detections": str(res["detections"]),
        })
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    accuracy = (tp + tn) / len(items) if items else 0.0
    metrics = {
        "total": len(items),
        "TP": tp, "FP": fp, "TN": tn, "FN": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
    }
    return metrics, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="eval/data")
    ap.add_argument("--conf", type=float, default=0.6)
    ap.add_argument("--min-frames", type=int, default=3)
    ap.add_argument("--every", type=int, default=4)
    ap.add_argument("--out", default="eval/results.csv")
    args = ap.parse_args()

    target_classes = ["person", "car", "truck", "motorcycle", "dog", "cat", "bicycle"]
    items = collect_labeled(Path(args.data))
    if not items:
        print("No labeled clips found in", args.data)
        print("Put clips in eval/data/true and eval/data/false")
        return
    metrics, rows = evaluate(items, args.conf, args.min_frames, args.every, target_classes)
    print(json.dumps(metrics, indent=2))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("Wrote", out)


if __name__ == "__main__":
    main()