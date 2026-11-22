import json


class FileStore:
    """Saves a dictionary to a JSON file and loads it back."""

    def __init__(self, path: str):
        self.path = path

    def save(self, data: dict) -> None:
        with open(self.path, "w") as fh:
            json.dump(data, fh)

    def load(self) -> dict:
        """Load the dictionary. Returns {} if the file does not exist.

        Raises json.JSONDecodeError if the file exists but is corrupted
        (not valid JSON).
        """
        try:
            with open(self.path, "r") as fh:
                return json.load(fh)
        except FileNotFoundError:
            return {}
