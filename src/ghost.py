import pygame
from .pacman import Player, Pacman
from .config import config
from collections import deque
import random
# row y, column x.


class Ghosts(Player):
    def __init__(
        self, row, col, map_data, Pacman: Pacman, speed, color, GameEngine
            ):
        super().__init__(row, col, map_data, color)
        self.Pacman = Pacman
        self.GameEngine = GameEngine
        self.start_position = [row, col]
        self.speed = speed
        self.edible = False
        self.is_eaten = False

    def ghost_move(self, row, col):
        if self.is_aligned():
            path = self.path_to_pacman((row, col))
            if len(path) == 1:
                direction = None
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

    def tracking_pacman(self):
        pacman_position = self.Pacman.get_current_cell()
        row, col, _ = pacman_position
        self.ghost_move(row, col)

    def go_next_pacman(self):
        pacman_position = self.Pacman.get_current_cell()
        pac_row, pac_col, _ = pacman_position
        possible_positions = self.get_neighbors((pac_row, pac_col))
        pac_row, pac_col = random.choice(possible_positions)
        self.ghost_move(pac_row, pac_col)

    def move_random_direction(self):
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

    def reset_ghost_position(self):
        self.x = self.start_position[1] * config.CELL_SIZE
        self.y = self.start_position[0] * config.CELL_SIZE

    def ghost_in_edible(self):
        pac_man_rect = pygame.Rect(
                    self.Pacman.x,
                    self.Pacman.y,
                    config.CELL_SIZE,
                    config.CELL_SIZE
                )
        for ghost in self.GameEngine.ghosts:
            ghost_rect = pygame.Rect(
                ghost.x,
                ghost.y,
                config.CELL_SIZE,
                config.CELL_SIZE
            )
            if ghost_rect.colliderect(pac_man_rect):
                if ghost.edible:
                    ghost.reset_ghost_position()
                else:
                    self.Pacman.lose_life()
