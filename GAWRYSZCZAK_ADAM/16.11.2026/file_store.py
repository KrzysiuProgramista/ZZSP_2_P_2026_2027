import json


class FileStore:
    def save(self, filename: str, data: dict) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def load(self, filename: str) -> dict:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)