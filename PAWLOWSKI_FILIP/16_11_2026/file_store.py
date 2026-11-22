import json


class FileStore:
    
    def save(self, data: dict, path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)

    def load(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
