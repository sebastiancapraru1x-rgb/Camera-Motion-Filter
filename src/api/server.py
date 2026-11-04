"""FastAPI webhook receiver (Phase 3)."""
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import Optional
from pydantic import BaseModel

from src.pipeline.detector import Detector
from src.pipeline.pipeline import Pipeline
from src.storage.paths import paths
from src.storage.events import log_event

load_dotenv()

app = FastAPI(title="AI Camera Receiver")


class MotionPayload(BaseModel):
    camera_id: str = "default"
    video_path: Optional[str] = None
    video_url: Optional[str] = None


def _run_pipeline(payload: MotionPayload):
    p = paths()
    for d in p.values():
        if isinstance(d, Path):
            d.mkdir(parents=True, exist_ok=True)

    if payload.video_url:
        from src.sources.url_source import UrlSource
        src = UrlSource([payload.video_url], inbox_dir=str(p["inbox"]))
        clip = next(src.list_clips())
        video_path = src.download(clip)
    elif payload.video_path:
        video_path = Path(payload.video_path)
    else:
        return {"error": "no video provided"}

    stem = Path(video_path).stem
    thumb_path = p["alerts"] / f"{stem}.jpg"

    import yaml
    cfg = {}
    cp = Path("config/cameras.yaml")
    if cp.exists():
        with open(cp) as f:
            cfg_all = yaml.safe_load(f) or {}
        for c in cfg_all.get("cameras", []):
            if c["id"] == payload.camera_id:
                cfg = c
                break

    target_classes = cfg.get("target_classes", ["person", "car", "truck", "motorcycle", "dog", "cat", "bicycle"])
    conf = cfg.get("conf_threshold", 0.6)
    min_frames = cfg.get("min_consecutive_frames", 3)
    every = cfg.get("frame_sample_every", 4)
    ignore_zones = cfg.get("ignore_zones", [])
    active_hours = cfg.get("active_hours")

    detector = Detector(conf=conf)
    pipeline = Pipeline(
        detector=detector,
        target_classes=target_classes,
        conf=conf,
        min_consecutive=min_frames,
        every=every,
        ignore_zones=ignore_zones,
        active_hours=active_hours,
        use_tracking=True,
    )
    result = pipeline.run(video_path, camera_id=payload.camera_id, thumbnail_path=str(thumb_path))

    if result["status"] == "TRUE":
        from src.alerts.discord import send_alert
        webhook = os.getenv("DISCORD_WEBHOOK_URL", "")
        label = ", ".join(f"{d['class']} ({d['conf']:.0%})" for d in result["detections"]) or "unknown"
        conf_val = result["detections"][0]["conf"] if result["detections"] else 0.0
        send_alert(webhook, payload.camera_id, label, conf_val, result["thumbnail"])
        if "data" in Path(video_path).parts and Path(video_path).parent != p["alerts"]:
            dest = p["alerts"] / Path(video_path).name
            try:
                shutil.move(str(video_path), str(dest))
            except Exception:
                pass
    else:
        if "data" in Path(video_path).parts:
            try:
                Path(video_path).unlink(missing_ok=True)
            except Exception:
                pass
        try:
            thumb_path.unlink(missing_ok=True)
        except Exception:
            pass

    log_event(p["logs"], {
        "camera_id": payload.camera_id,
        "status": result["status"],
        "detections": result["detections"],
        "video": result["video"],
        "source": "webhook",
    })
    return result


@app.post("/motion")
def motion(payload: MotionPayload, bg: BackgroundTasks):
    bg.add_task(_run_pipeline, payload)
    return {"status": "queued", "camera_id": payload.camera_id}


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi.middleware.cors import CORSMiddleware
from src.api.stats import router as stats_router
app.include_router(stats_router)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Serve built React dashboard in production
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

_dashboard_dist = Path(__file__).resolve().parent.parent / "dashboard" / "dist"
if _dashboard_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(_dashboard_dist / "assets")), name="assets")

    @app.get("/")
    async def _serve_dashboard():
        return FileResponse(str(_dashboard_dist / "index.html"))

    @app.get("/{full_path:path}")
    async def _spa_fallback(full_path: str):
        if full_path.startswith(("api", "docs", "openapi.json", "favicon.ico")):
            raise HTTPException(status_code=404)
        return FileResponse(str(_dashboard_dist / "index.html"))
