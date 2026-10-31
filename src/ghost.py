from .pacman import Player
from .config import config
from collections import deque
# row y, column x.


class Ghosts(Player):
    def __init__(self, row, col, map_data):
        super().__init__(row, col,  map_data)
        self.speed = 2
        self.edible = False
        self.is_eaten = False

    def ghost_move(self):
        if self.is_aligned():
            path = self.path_to_pacman((0, 0))
            if len(path) == 1:
                direction = None
            # print(f"path == {path}")
            # print(path[0])
            else:
                row_c, col_c = path[0]
                row_n, col_n = path[1]
                if row_c < row_n:
                    direction = config.DOWN
                elif row_c > row_n:
                    direction = config.UP
                elif col_c < col_n:
                    direction = config.RIGHT
                else:
                    direction = config.LEFT
        else:
            direction = self.move_random_direction()
            return

        self.direction = direction
        self.move()

    def move_random_direction(self):
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
        self.direction = random.choice(directions)
        self.move()

    def open_way(self, direction, position):
        row, col = position
        cell = self.map[row][col]
        if direction == config.UP:
            return row > 0 and not cell.up
        if direction == config.DOWN:
            return row < len(self.map) - 1 and not cell.down
        if direction == config.LEFT:
            return col > 0 and not cell.left
        if direction == config.RIGHT:
            return col < len(self.map[0]) - 1 and not cell.right
        return False

    def get_neighbors(self, current_position: tuple[int, int]):
        neighbors = []
        directions = [config.RIGHT, config.LEFT, config.DOWN, config.UP]
        row, col = current_position
        for direction in directions:
            if self.open_way(direction, current_position):
                if direction == config.UP:
                    position = (row - 1, col)
                elif direction == config.DOWN:
                    position = (row + 1, col)
                elif direction == config.LEFT:
                    position = (row, col - 1)
                else:
                    position = (row, col + 1)
                neighbors.append(position)
        return neighbors

    def path_to_pacman(self, pacman_position: tuple[int, int]):
        row, col, _ = self.get_current_cell()
        start = (row, col)
        if start == pacman_position:
            return [start]
        neighbors = self.get_neighbors(start)
        visited = set()
        visited.add(start)
        queue = deque([start])
        parent = {start: None}
        path = []

        while queue:
            current = queue.popleft()
            if current == pacman_position:
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
