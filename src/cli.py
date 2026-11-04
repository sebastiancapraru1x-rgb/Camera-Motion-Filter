"""CLI entry point (Phase 2)."""
import argparse
import json
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

from src.pipeline.detector import Detector
from src.pipeline.pipeline import Pipeline
from src.alerts.discord import send_alert
from src.storage.paths import paths
from src.storage.retention import purge_older_than, enforce_disk_cap
from src.storage.events import log_event, log_false_alarm

load_dotenv()

DEFAULT_CLASSES = ["person", "car", "truck", "motorcycle", "dog", "cat", "bicycle"]


def load_camera_config(config_path, camera_id):
    if not config_path:
        return {}
    import yaml
    with open(config_path) as f:
        cfg = yaml.safe_load(f) or {}
    for c in cfg.get("cameras", []):
        if c["id"] == camera_id:
            return c
    return {}


def main():
    parser = argparse.ArgumentParser(prog="aicamera")
    sub = parser.add_subparsers(dest="cmd")

    a = sub.add_parser("analyze")
    a.add_argument("--source", default="file", choices=["file", "url", "webcam", "blink"])
    a.add_argument("--path", help="file path or url")
    a.add_argument("--camera-id", default="default")
    a.add_argument("--config", help="path to cameras.yaml")
    a.add_argument("--classes", nargs="*", default=None)
    a.add_argument("--conf", type=float, default=None)
    a.add_argument("--min-frames", type=int, default=None)
    a.add_argument("--every", type=int, default=None)
    a.add_argument("--seconds", type=int, default=5)
    a.add_argument("--no-alert", action="store_true", help="disable Discord alert")

    args = parser.parse_args()
    if args.cmd != "analyze":
        parser.print_help()
        return

    p = paths()
    for d in p.values():
        if isinstance(d, Path):
            d.mkdir(parents=True, exist_ok=True)

    cam_cfg = load_camera_config(args.config, args.camera_id)
    target_classes = args.classes or cam_cfg.get("target_classes", DEFAULT_CLASSES)
    conf = args.conf if args.conf is not None else cam_cfg.get("conf_threshold", 0.6)
    min_frames = args.min_frames if args.min_frames is not None else cam_cfg.get("min_consecutive_frames", 3)
    every = args.every if args.every is not None else cam_cfg.get("frame_sample_every", 4)
    ignore_zones = cam_cfg.get("ignore_zones", [])
    active_hours = cam_cfg.get("active_hours")

    if args.source == "file":
        video_path = Path(args.path)
    elif args.source == "url":
        from src.sources.url_source import UrlSource
        src = UrlSource([args.path], inbox_dir=str(p["inbox"]))
        clip = next(src.list_clips())
        video_path = src.download(clip)
    elif args.source == "webcam":
        from src.sources.webcam_source import WebcamSource
        src = WebcamSource(seconds=args.seconds, inbox_dir=str(p["inbox"]))
        clip = next(src.list_clips())
        video_path = src.download(clip)
    elif args.source == "blink":
        import os
        username = os.getenv("BLINK_USERNAME", "")
        password = os.getenv("BLINK_PASSWORD", "")
        if not username or not password:
            raise ValueError("Set BLINK_USERNAME and BLINK_PASSWORD in .env")
        from src.sources.blink_source import BlinkSource
        src = BlinkSource(username=username, password=password, inbox_dir=str(p["inbox"]))
        clip = next(src.list_clips())
        video_path = src.download(clip)
    else:
        raise ValueError(args.source)

    stem = Path(video_path).stem
    thumb_path = p["alerts"] / f"{stem}.jpg"

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
    result = pipeline.run(video_path, camera_id=args.camera_id, thumbnail_path=str(thumb_path))

    print(json.dumps(result, indent=2))
    if result["detections"]:
        labels = ", ".join(f"{d['class']} ({d['conf']:.0%})" for d in result["detections"])
        print(f"\n{'REAL MOTION' if result['status']=='TRUE' else 'FALSE ALARM'}: {labels}")
    else:
        print(f"\n{'REAL MOTION' if result['status']=='TRUE' else 'FALSE ALARM'}: no target objects")

    video_path = Path(video_path)
    under_data = "data" in video_path.parts
    if result["status"] == "TRUE":
        if under_data and video_path.parent != p["alerts"]:
            dest = p["alerts"] / video_path.name
            try:
                shutil.move(str(video_path), str(dest))
                result["video"] = str(dest)
            except Exception:
                pass
        if not args.no_alert:
            webhook = os.getenv("DISCORD_WEBHOOK_URL", "")
            label = ", ".join(f"{d['class']} ({d['conf']:.0%})" for d in result["detections"]) or "unknown"
            conf_val = result["detections"][0]["conf"] if result["detections"] else 0.0
            send_alert(webhook, args.camera_id, label, conf_val, result["thumbnail"])
    else:
        if under_data:
            try:
                video_path.unlink(missing_ok=True)
            except Exception:
                pass
        try:
            Path(thumb_path).unlink(missing_ok=True)
        except Exception:
            pass
        log_false_alarm(p["logs"], {
            "camera_id": args.camera_id,
            "video": str(video_path),
            "detections": str(result["detections"]),
        })

    log_event(p["logs"], {
        "camera_id": args.camera_id,
        "status": result["status"],
        "detections": result["detections"],
        "video": result["video"],
    })

    purge_older_than(p["alerts"], 7)
    purge_older_than(p["false_alarms"], 3)
    enforce_disk_cap([p["alerts"], p["inbox"], p["processing"], p["false_alarms"]], 3.0)


if __name__ == "__main__":
    main()