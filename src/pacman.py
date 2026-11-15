from .player import Player
from .config import config


class Pacman(Player):
    def __init__(self, row, col, map_data, color):
        super().__init__(row, col, map_data, color)
        self.pacman_starts_positions = (0, 0)
        self.lives = 3
        self.score = 0

    def lose_life(self):
        self.lives -= 1
        self.x = self.pacman_starts_positions[1] * config.CELL_SIZE
        self.y = self.pacman_starts_positions[0] * config.CELL_SIZE
        self.set_direction(None)
