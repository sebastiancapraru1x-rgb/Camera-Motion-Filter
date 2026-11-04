"""Threshold tuning: sweep conf and min_consecutive frames, report best F1."""
import argparse
import itertools
from pathlib import Path

try:
    from eval.evaluate import collect_labeled, evaluate
except Exception:
    from evaluate import collect_labeled, evaluate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="eval/data")
    ap.add_argument("--out", default="eval/tune_results.csv")
    args = ap.parse_args()

    items = collect_labeled(Path(args.data))
    if not items:
        print("No labeled clips found")
        return

    target_classes = ["person", "car", "truck", "motorcycle", "dog", "cat", "bicycle"]
    results = []
    for conf, mf in itertools.product([0.4, 0.5, 0.6, 0.7, 0.8], [1, 2, 3, 4, 5]):
        metrics, _ = evaluate(items, conf, mf, 4, target_classes)
        results.append((conf, mf, metrics["f1"], metrics["precision"], metrics["recall"], metrics["accuracy"]))
        print(f"conf={conf} min_frames={mf} -> F1={metrics['f1']} P={metrics['precision']} R={metrics['recall']}")

    results.sort(key=lambda r: r[2], reverse=True)
    print("\nBest:", results[0])
    import csv
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["conf", "min_frames", "f1", "precision", "recall", "accuracy"])
        w.writerows(results)
    print("Wrote", out)


if __name__ == "__main__":
    main()