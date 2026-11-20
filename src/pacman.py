from .player import Player


class Pacman(Player):
    def __init__(self, row, col, map_data, color, config):
        super().__init__(row, col, map_data, color, config)
        self.pacman_starts_positions = (0, 0)
        self.lives = self.config.PLAYER_LIVES
        self.score = 0

    def lose_life(self):
        self.lives -= 1
        self.x = self.pacman_starts_positions[1] * self.config.CELL_SIZE
        self.y = self.pacman_starts_positions[0] * self.config.CELL_SIZE
        self.set_direction(None)
