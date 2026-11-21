from __future__ import annotations
from typing import Any

import argparse
import json


class CLI():
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.config_content: str | None = None
        self.config_dict: dict[str, Any] | None = None

    def load_cli(self) -> str:
        self.parser.add_argument(
            "config_file",
            type=str,
            help="path to json file that contain all config of the game")

        arg = self.parser.parse_args()

        return str(arg.config_file)

    def load_json_file(self) -> None:
        config_path = self.load_cli()

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_content = file.read()
        except FileNotFoundError:
            print("Error: Config file not found.")
            exit(1)
        except PermissionError:
            print("Error: Permission denied to read config file.")
            exit(1)
        except Exception as e:
            print(f"Error: An unexpected error occurred - {e}")
            exit(1)

        self.config_content = config_content
        self.remove_comment()

        config_dict = json.loads(self.config_content)
        self.config_dict = config_dict

    def remove_comment(self) -> None:
        """Strip comment lines after load_json_file has populated the text."""
        clean_content = ""

        for line in str(self.config_content).split('\n'):
            if line.lstrip().startswith('#'):
                continue

            clean_content += line + '\n'

        self.config_content = clean_content
