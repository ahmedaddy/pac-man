import json
from typing import Any


class Utils:
    @staticmethod
    def read_json_file(path: str) -> Any:
        """
        Read a JSON file and return its contents.
        Args:
            path (str): The path to the JSON file.
        Returns:
            Any: The contents of the JSON file, or None if an error occurs.
        """
        try:
            with open(path, "r") as handle:
                return json.load(handle)
        except FileNotFoundError:
            print(f"Error: file not found, path: {path}")
        except Exception:
            print(f"Error: an error occurred while reading the file, \
path: {path}")
        return None
