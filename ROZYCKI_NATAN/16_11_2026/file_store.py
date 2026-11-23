import json
from pathlib import Path


class FileStore:
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)

    def save(self, data: dict) -> None:
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f)

    def load(self) -> dict:
        with self.filepath.open("r", encoding="utf-8") as f:
            return json.load(f)