from .pacman import Player
from .config import config


class Ghosts(Player):
    def __init__(self, row, col, map_data):
        super().__init__(row, col,  map_data)
        self.speed = 2
        self.edible = False
        self.is_eaten = False
        self.visited = None

    def first_move(self):
        print(self.speed)
        self.direction = self.get_random_direction()
        self.move()

    def get_random_direction(self):
        import random
        directions = [self.direction]
        if self.is_aligned():
            if self.can_move(config.UP) and self.direction != config.DOWN:
                directions.append(config.UP)
            if self.can_move(config.DOWN) and self.direction != config.UP:
                directions.append(config.DOWN)
            if self.can_move(config.LEFT) and self.direction != config.RIGHT:
                directions.append(config.LEFT)
            if self.can_move(config.RIGHT) and self.direction != config.LEFT:
                directions.append(config.RIGHT)
        return random.choice(directions)
