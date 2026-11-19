from .player import Player
from .config import config


class Pacman(Player):
    """
    A class representing the Pacman player in the game.
    """
    def __init__(
            self,
            row: int,
            col: int,
            map_data: list,
            color: tuple
            ) -> None:
        """
        Initialize the Pacman player.
        """
        super().__init__(row, col, map_data, color)
        self.pacman_starts_positions = (0, 0)
        self.lives = config.PLAYER_LIVES
        self.score = 0

    def lose_life(self) -> None:
        """
        Decrease the player's lives by one
        and reset the position to the starting point.
        """
        self.lives -= 1
        self.x = self.pacman_starts_positions[1] * config.CELL_SIZE
        self.y = self.pacman_starts_positions[0] * config.CELL_SIZE
        self.set_direction(None)
