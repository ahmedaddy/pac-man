from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config
    from .game import Cell

from .player import Player


class Pacman(Player):

    """
    A class representing the Pacman player in the game.
    """
    def __init__(
            self,
            row: int,
            col: int,
            map_data: list[list[Cell]],
            color: str,
            config: Config
            ) -> None:
        """
        Initialize the Pacman player.
        """
        super().__init__(row, col, map_data, color, config)
        self.pacman_starts_positions = (0, 0)
        self.lives = self.config.PLAYER_LIVES
        self.score = 0

    def lose_life(self) -> None:
        """
        Decrease the player's lives by one
        and reset the position to the starting point.
        """
        self.lives -= 1
        self.x = self.pacman_starts_positions[1] * self.config.CELL_SIZE
        self.y = self.pacman_starts_positions[0] * self.config.CELL_SIZE
        self.set_direction(None)
