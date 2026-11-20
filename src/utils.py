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
        except json.JSONDecodeError:
            print(f"Error: invalid JSON in file, path: {path}")
        except Exception:
            print(f"Error: an error occurred while reading the file, \
path: {path}")
        return None

    @staticmethod
    def check_config(config: dict) -> bool:
        required_keys = [
            "player_speed",
            "player_lives",
            "level_timer",
            "points_per_ghost",
            "points_per_super_gum",
            "points_per_gum"
        ]
        print("Checking configuration...")
        for key in required_keys:
            if key not in config:
                print(f"Error: missing required key in config: {key}")
                return False
            if key == "level":
                for each in ["level_number", "size", "level_name"]:
                    if each not in config[key]:
                        print(f"Error: missing required key in\
config['level']: {each}")
                        return False
        return True
