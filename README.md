# AI Camera — Blink False-Motion Filter

Source-agnostic computer-vision pipeline that filters false motion alerts
(wind, shadows, trees) from Blink cameras and only notifies you (Discord) when
a real object (person, car, etc.) is detected.

> Status: **Complete**. All 5 phases implemented — file/URL/webcam/Blink sources, detection, tracking, filtering, Discord alerts, FastAPI receiver, React dashboard, Docker, CI, and launchd.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.cli analyze --source file --path data/inbox/sample.mp4
```

## Run dashboard (React + Vite)
```bash
cd dashboard
npm install
npm run dev          # dev server at http://localhost:5173
npm run build        # production build
npm run preview      # preview production build
```
The React dashboard proxies `/api` to the FastAPI backend at `http://localhost:8000`.
Start the backend first: `uvicorn src.api.server:app --host 0.0.0.0 --port 8000`

## Run API receiver (required for dashboard)
```bash
uvicorn src.api.server:app --host 0.0.0.0 --port 8000
```

## Run with Blink cameras (Phase 5)
```bash
# 1. Add to .env
BLINK_USERNAME=your-email@example.com
BLINK_PASSWORD=your-password

# 2. Add to config/cameras.yaml
# cameras:
#   - id: front_door
#     source: blink
#     target_classes: [person, car, truck, motorcycle, dog]

# 3. Run
python -m src.cli analyze --source blink --camera-id front_door
```
> Requires `pip install blinkpy`. Blink cloud clip access may require a subscription
> for extended retention beyond the free tier.

## Project layout
```
AI camera/
├── data/            # inbox, processing, alerts, false_alarms, archive
├── logs/            # events.jsonl, false_alarms.csv
├── models/          # YOLOv8n weights (~12MB, downloaded on first run)
├── config/          # per-source YAML
├── src/             # pipeline code
├── dashboard/       # React + Vite app
├── eval/            # labeled data + metrics
├── tests/           # pytest
├── docker-compose.yml
├── launchd/         # macOS daemon plist
└── README.md
```

## Free-only stack
- Detection: YOLOv8n (CPU) via `ultralytics`
- Tracking: ByteTrack
- Alerts: Discord webhook (+ best-frame thumbnail)
- Dashboard: React + Vite (LAN, no auth, 60s auto-refresh, proxies to FastAPI)
- Daemon: macOS `launchd`

## Phases
1. Core pipeline (File/URL/Webcam sources)
2. Tracking + filtering + Discord alerts
3. FastAPI receiver + offline evaluation
4. Dashboard + Docker + CI + launchd
5. Blink adapter (when home)

## Storage (all inside this folder)
- Retention: alerts 7 days, false alarms 3 days
- Disk cap: 3GB total for clips (oldest-first eviction)

## License
MIT