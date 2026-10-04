from .config import config


class Pacman:
    def __init__(self, row, col, map_data):
        self.x = col * config.CELL_SIZE
        self.y = row * config.CELL_SIZE
        self.map = map_data

        self.speed = 2
        self.direction = None
        self.desired_direction = None

        self.lives = 3
        self.score = 0

    def is_aligned(self):
        return (
            self.x % config.CELL_SIZE == 0
            and self.y % config.CELL_SIZE == 0
        )

    def get_current_cell(self):
        row = self.y // config.CELL_SIZE
        col = self.x // config.CELL_SIZE
        return row, col, self.map[row][col]

    def can_move(self, direction):
        row, col, cell = self.get_current_cell()
        # print(cell.up, cell.right, cell.down, cell.left)
        if direction == config.UP:
            return row > 0 and not cell.up
        if direction == config.DOWN:
            return row < len(self.map) - 1 and not cell.down
        if direction == config.LEFT:
            return col > 0 and not cell.left
        if direction == config.RIGHT:
            return col < len(self.map[0]) - 1 and not cell.right
        return False

    def set_direction(self, direction):
        self.desired_direction = direction

    def move(self):
        if self.is_aligned():
            if (self.desired_direction is not None
                    and self.can_move(self.desired_direction)):
                self.direction = self.desired_direction
            elif (self.direction is not None
                    and not self.can_move(self.direction)):
                self.direction = None
        # print(self.direction, self.can_move(self.direction))
        # print(self.direction, self.can_move(self.direction))
        if self.direction == config.UP:
            self.y -= self.speed
        elif self.direction == config.DOWN:
            self.y += self.speed
        elif self.direction == config.LEFT:
            self.x -= self.speed
        elif self.direction == config.RIGHT:
            self.x += self.speed
