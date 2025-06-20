import json
from typing import Any


class FileReader:
    """Utility class for reading files. Supports JSON."""

    @staticmethod
    def read_json(path: str) -> Any:
        with open(path, 'r') as f:
            return json.load(f)
