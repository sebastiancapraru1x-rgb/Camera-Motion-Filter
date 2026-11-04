# Evaluation (Phase 3)

Label ~200 clips by dropping them into:
- `eval/data/true/`  (real motion)
- `eval/data/false/` (wind/shadows/etc.)

Data folders are gitignored.

## Run evaluation
```bash
python -m eval.evaluate --data eval/data --conf 0.6 --min-frames 3
```
Prints Precision/Recall/F1/Accuracy and writes `eval/results.csv`.

## Tune thresholds
```bash
python -m eval.tune --data eval/data
```
Sweeps conf (0.4-0.8) and min_frames (1-5), writes `eval/tune_results.csv`.