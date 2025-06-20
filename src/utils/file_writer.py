import json
from typing import Any

class FileWriter:
    """Utility class for writing files. Supports JSON."""

    @staticmethod
    def write_json(path: str, data: Any) -> None:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
