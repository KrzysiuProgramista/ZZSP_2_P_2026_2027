import json


class FileStore:
    """Save and load dictionaries using JSON files."""

    def save(self, data: dict, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def load(self, filename: str) -> dict:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)