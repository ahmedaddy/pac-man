from .pacman import Player


class Ghosts(Player):
    def __init__(self, row, col, map_data):
        super().__init__(row, col,  map_data)
        self.speed = 2
        self.direction = None
        self.next_direction = None
        self.edible = False
        self.is_eaten = False
