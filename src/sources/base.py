"""Source adapters. Each implements VideoSource."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional


@dataclass
class Clip:
    id: str
    path: Path
    camera_id: str
    timestamp: str


class VideoSource(ABC):
    """Abstract camera/file source. Implement to add a new input type."""

    name: str = "base"

    @abstractmethod
    def list_clips(self) -> Iterator[Clip]:
        ...

    @abstractmethod
    def download(self, clip: Clip) -> Path:
        ...

    def metadata(self, clip: Clip) -> dict:
        return {"id": clip.id, "camera_id": clip.camera_id, "timestamp": clip.timestamp}