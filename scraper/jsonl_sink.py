"""Append-only raw landing zone; keeps source evidence separate from warehouse tables."""
import json
from pathlib import Path

class JsonlSink:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def write(self, record: dict) -> None:
        with self.path.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, default=str) + "\n")
