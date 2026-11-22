from __future__ import annotations
from typing import Any, ClassVar, TypedDict

import dataclasses


class LevelSettings(TypedDict):
    """Describe a level's grid dimensions and generation seed."""

    size: tuple[int, int]
    seed: int


@dataclasses.dataclass
class Config:
    HIGH_SCORE_FILENAME: str = "high_scores.json"
    YELLOW: str = "#FFFF00"
    RED: str = "#F62217"
    BLINKY: str = "#FF0000"
    PINK: str = "#EA82E5"
    CYAN: str = "#46BFEE"
    ORANGE: str = "#DB851C"
    DARK_BLUE: str = "#0a9396"

    CELL_SIZE: int = 32

    LEFT: str = "LEFT"
    RIGHT: str = "RIGHT"
    UP: str = "UP"
    DOWN: str = "DOWN"
    WIDTH: int = 1080
    HEIGHT: int = 720
    BALL_SIZE: int = 15

    PLAYER_SPEED: int = 4
    PLAYER_LIVES: int = 3

    GUM_SIZE: int = 5
    SUPER_GUM_SIZE: int = 10
    SUPER_GUM_DURATION: int = 5000
    LEVEL_SETTINGS: ClassVar[list[LevelSettings]] = [
        {"size": (15, 15), "seed": 42},
        {"size": (14, 17), "seed": 1},
        {"size": (11, 17), "seed": 1},
        {"size": (15, 18), "seed": 1},
        {"size": (12, 20), "seed": 1},
        {"size": (10, 18), "seed": 1},
        {"size": (18, 14), "seed": 1},
        {"size": (11, 20), "seed": 1},
        {"size": (13, 22), "seed": 1},
        {"size": (16, 25), "seed": 1},
    ]
    LEVEL_TIMER: int = 90
    POINTS_PER_GUM: int = 10
    POINTS_PER_SUPER_GUM: int = 50
    POINTS_PER_GHOST: int = 200
    NUMBERS_OF_GUMS: int = 0

    def load_config(self, config_dict: dict[str, Any]) -> None:
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
