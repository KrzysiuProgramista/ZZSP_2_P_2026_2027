import json


class FileStore:

    def save(self, data: dict, filename: str) -> None:
        with open(filename, "w") as file:
            json.dump(data, file)

    def load(self, filename: str) -> dict:
        with open(filename, "r") as file:
            return json.load(file)
