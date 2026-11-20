import pygame
from .pacman import Player, Pacman
from collections import deque
import random
# row y, column x.


class Ghosts(Player):
    def __init__(
        self, row, col, map_data, Pacman: Pacman, speed, color, GameEngine,
        config
            ):
        super().__init__(row, col, map_data, color, config)
        self.Pacman = Pacman
        self.GameEngine = GameEngine
        self.start_position = [row, col]
        self.speed = speed
        self.edible = False
        self.is_eaten = False
        self.normal_sprite = None
        self.edible_sprite = None
        self.waiting_sprite = None

    def ghost_move(self, row, col):
        if self.is_aligned():
            current = self.get_current_cell()[:2]
            target = (row, col)

            path = self.short_path((row, col))

            if self.edible and not self.is_eaten:

                pac_position = self.Pacman.get_current_cell()[:2]
                distance = self.bfs_distances(pac_position)
                danger_in = 3
                is_arrive = current == target

                danger_cell = {
                    pos for pos, distance in distance.items()
                    if danger_in >= distance
                }
                is_pac_near = (
                    distance.get(current, float("inf")) <= danger_in
                )

                if is_arrive and is_pac_near:
                    # print("heeeeeeeeeeeeeeeeeeeeeeeer")
                    neighbors = self.get_neighbors(current)
                    next_cell = max(
                        neighbors, key=lambda pos: distance.get(pos, -1))
                    path = [current, next_cell]

                elif any(pos in danger_cell for pos in path[1:]):
                    safe_path = self.short_path(target, danger_cell)

                    if len(safe_path) > 2:
                        path = safe_path
                    else:
                        neighbors = self.get_neighbors(current)
                        next_cell = max(
                            neighbors, key=lambda pos: distance.get(
                                pos, float("inf"))
                        )
                        path = [current, next_cell]

            if len(path) < 2:
                direction = None
                return
            else:
                row_c, col_c = path[0]
                row_n, col_n = path[1]
                if row_c < row_n:
                    direction = self.config.DOWN
                elif row_c > row_n:
                    direction = self.config.UP
                elif col_c < col_n:
                    direction = self.config.RIGHT
                else:
                    direction = self.config.LEFT

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
            if self.can_move(self.config.UP) and self.direction != self.config.DOWN:
                directions.append(self.config.UP)
            if self.can_move(self.config.DOWN) and self.direction != self.config.UP:
                directions.append(self.config.DOWN)
            if self.can_move(self.config.LEFT) and self.direction != self.config.RIGHT:
                directions.append(self.config.LEFT)
            if self.can_move(self.config.RIGHT) and self.direction != self.config.LEFT:
                directions.append(self.config.RIGHT)
        self.direction = random.choice(directions)
        self.move()

    def open_way(self, direction, position):
        row, col = position
        cell = self.map[row][col]
        if direction == self.config.UP:
            return row > 0 and not cell.up
        if direction == self.config.DOWN:
            return row < len(self.map) - 1 and not cell.down
        if direction == self.config.LEFT:
            return col > 0 and not cell.left
        if direction == self.config.RIGHT:
            return col < len(self.map[0]) - 1 and not cell.right
        return False

    def get_neighbors(self, current_position: tuple[int, int]):
        neighbors = []
        directions = [self.config.RIGHT, self.config.LEFT, self.config.DOWN, self.config.UP]
        row, col = current_position
        for direction in directions:
            if self.open_way(direction, current_position):
                if direction == self.config.UP:
                    position = (row - 1, col)
                elif direction == self.config.DOWN:
                    position = (row + 1, col)
                elif direction == self.config.LEFT:
                    position = (row, col - 1)
                else:
                    position = (row, col + 1)
                neighbors.append(position)
        return neighbors

    def short_path(self, target: tuple[int, int], blocked=None):
        if blocked is None:
            blocked = set()

        row, col, _ = self.get_current_cell()
        start = (row, col)
        if start == target:
            return []
        neighbors = self.get_neighbors(start)
        visited = set()
        visited.add(start)
        queue = deque([start])
        parent = {start: None}
        path = []

        while queue:
            current = queue.popleft()

            if current == target:
                while current is not None:
                    path.append(current)
                    current = parent[current]

                return path[::-1]

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor in blocked:
                    continue

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        return []

    def bfs_distances(self, start):
        queue = deque([start])
        distances = {start: 0}

        while queue:
            current = queue.popleft()

            for neighbor in self.get_neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        return distances

    def reset_ghost_position(self):
        self.x = self.start_position[1] * self.config.CELL_SIZE
        self.y = self.start_position[0] * self.config.CELL_SIZE

    def ghost_in_edible(self):
        pac_man_rect = pygame.Rect(
                    self.Pacman.x,
                    self.Pacman.y,
                    self.config.CELL_SIZE,
                    self.config.CELL_SIZE
                )
        # for ghost in self.GameEngine.ghosts:
        ghost_rect = pygame.Rect(
            self.x,
            self.y,
            self.config.CELL_SIZE,
            self.config.CELL_SIZE
        )
        if ghost_rect.colliderect(pac_man_rect):
            if self.edible:
                self.is_eaten = True
                self.Pacman.score += self.config.POINTS_PER_GHOST
                self.reset_ghost_position()
            elif not self.GameEngine.cheat.flags["invincibility"]:
                self.Pacman.lose_life()

    def load_ghosts_image(self, normal_image_path, edible_path, waiting_path):

        size = self.config.BALL_SIZE * 2
        try:
            normal = pygame.image.load(
                str(normal_image_path)
            ).convert_alpha()

            edible = pygame.image.load(
                str(edible_path)
            ).convert_alpha()
            waiting = pygame.image.load(
                str(waiting_path)
            ).convert_alpha()

            self.normal_sprite = pygame.transform.smoothscale(
                normal, (size, size)
            )

            self.edible_sprite = pygame.transform.smoothscale(
                edible, (size, size)
            )
            self.waiting_sprite = pygame.transform.smoothscale(
                waiting, (size, size)
            )

        except (pygame.error, OSError) as error:
            print(f"Error loading ghost sprites: {error}")
            self.normal_sprite = None
            self.edible_sprite = None

    def draw(self, screen, offset_x, offset_y):
        if self.is_eaten:
            sprite = self.waiting_sprite

        elif self.edible:
            sprite = self.edible_sprite
        else:
            sprite = self.normal_sprite

        # if sprite is None:
        #     super().draw(screen, offset_x, offset_y)
        #     return

        center_x = offset_x + self.x + self.config.CELL_SIZE // 2
        center_y = offset_y + self.y + self.config.CELL_SIZE // 2

        sprite_rect = sprite.get_rect(
            center=(center_x, center_y)
        )

        screen.blit(sprite, sprite_rect)
