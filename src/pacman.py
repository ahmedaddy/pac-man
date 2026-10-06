from .config import config


class Pacman:
    def __init__(self, row, col, map_data):
        self.x = col * config.CELL_SIZE
        self.y = row * config.CELL_SIZE
        self.map = map_data

        self.speed = 7
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
        if self.direction == None:
            return
        # print(self.direction, self.can_move(self.direction))
        # print(self.direction, self.can_move(self.direction))
        if self.direction == config.UP:
            dist_to_center = self.y % config.CELL_SIZE
            if dist_to_center == 0:
                dist_to_center = config.CELL_SIZE
            self.y -= min(self.speed, dist_to_center)

        elif self.direction == config.DOWN:
            dist_to_center = config.CELL_SIZE - (self.y % config.CELL_SIZE)
            if self.y % config.CELL_SIZE == 0:
                dist_to_center = config.CELL_SIZE
            self.y += min(self.speed, dist_to_center)

        elif self.direction == config.LEFT:
            dist_to_center = self.x % config.CELL_SIZE
            if dist_to_center == 0:
                dist_to_center = config.CELL_SIZE
            self.x -= min(self.speed, dist_to_center)

        elif self.direction == config.RIGHT:
            dist_to_center = config.CELL_SIZE - (self.x % config.CELL_SIZE)
            if self.x % config.CELL_SIZE == 0:
                dist_to_center = config.CELL_SIZE
            self.x += min(self.speed, dist_to_center)
