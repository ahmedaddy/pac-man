from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Cell

from pathlib import Path

from .game import GameEngine
from .config import Config

import pygame
from .pacman import Player, Pacman
from collections import deque
import random
# row y, column x.


class Ghosts(Player):
    """Control ghost movement, pathfinding, collision state, and sprites."""

    def __init__(
        self, row: int, col: int, map_data: list[list[Cell]], Pacman: Pacman,
        speed: int, color: str, GameEngine: GameEngine,
        config: Config
            ) -> None:
        """Initialize a ghost with its target player,
        spawn, speed, and sprites.

        Args:
            row: Starting or target grid row.
            col: Starting or target grid column.
            map_data: Maze cells arranged in row-major order.
            Pacman: Pac-Man instance tracked by this ghost.
            speed: Movement distance in pixels per update.
            color: Rendering color.
            GameEngine: Engine providing shared game and cheat state.
            config: Game configuration settings.
        """
        super().__init__(row, col, map_data, color, config)
        self.Pacman = Pacman
        self.GameEngine: GameEngine = GameEngine
        self.start_position: list[int] = [row, col]
        self.speed: int = speed
        self.edible: bool = False
        self.is_eaten: bool = False
        self.normal_sprite: pygame.Surface | None = None
        self.edible_sprite: pygame.Surface | None = None
        self.waiting_sprite: pygame.Surface | None = None

    def ghost_move(self, row: int, col: int) -> None:
        """Move toward a target cell, avoiding nearby Pac-Man while edible.

        Args:
            row: Starting or target grid row.
            col: Starting or target grid column.
        """
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
            self.move_random_direction()
            return

        self.direction = direction
        self.move()

    def tracking_pacman(self) -> None:
        """Move toward the cell currently occupied by Pac-Man."""
        pacman_position = self.Pacman.get_current_cell()
        row, col, _ = pacman_position
        self.ghost_move(row, col)

    def go_next_pacman(self) -> None:
        """Move toward a randomly selected neighbor of Pac-Man."""
        pacman_position = self.Pacman.get_current_cell()
        pac_row, pac_col, _ = pacman_position
        possible_positions = self.get_neighbors((pac_row, pac_col))
        pac_row, pac_col = random.choice(possible_positions)
        self.ghost_move(pac_row, pac_col)

    def move_random_direction(self) -> None:
        """Sample the current direction and open non-reversing directions,
        then move."""
        directions: list[str | None] = [self.direction]
        if self.is_aligned():
            if (
                self.can_move(self.config.UP) and
                self.direction != self.config.DOWN
                    ):
                directions.append(self.config.UP)

            if (
                self.can_move(self.config.DOWN) and
                self.direction != self.config.UP
                    ):
                directions.append(self.config.DOWN)

            if (
                self.can_move(self.config.LEFT) and
                self.direction != self.config.RIGHT
                    ):
                directions.append(self.config.LEFT)

            if (
                self.can_move(self.config.RIGHT) and
                self.direction != self.config.LEFT
                    ):
                directions.append(self.config.RIGHT)

        self.direction = random.choice(directions)
        self.move()

    def open_way(self, direction: str, position: tuple[int, int]) -> bool:
        """Check the supplied cell boundary and wall for an open passage.

        Args:
            direction: Movement direction to inspect or request.
            position: Grid position as a row and column pair.

        Returns:
            True if the supplied cell has an in-bounds passage
            in that direction.
        """
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

    def get_neighbors(
        self, current_position: tuple[int, int]
            ) -> list[tuple[int, int]]:
        """Return adjacent cells reachable through open passages.

        Args:
            current_position: Cell to explore, as a row and column pair.

        Returns:
            Reachable neighboring row and column pairs.
        """
        neighbors: list[tuple[int, int]] = []
        directions = [
            self.config.RIGHT,
            self.config.LEFT,
            self.config.DOWN,
            self.config.UP]

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

    def short_path(
        self, target: tuple[int, int],
        blocked: set[tuple[int, int]] | None = None
            ) -> list[tuple[int, int]]:
        """Find a shortest route to the target while excluding blocked cells.

        Args:
            target: Destination row and column.
            blocked: Cells excluded from the search, or None for no exclusions.

        Returns:
            Cells from start to target; empty if already there or unreachable.
        """
        if blocked is None:
            blocked = set()

        row, col, _ = self.get_current_cell()
        start = (row, col)
        if start == target:
            return []
        neighbors = self.get_neighbors(start)
        visited: set[tuple[int, int]] = set()
        visited.add(start)
        queue: deque[tuple[int, int]] = deque([start])
        parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        path: list[tuple[int, int]] = []

        current: tuple[int, int] | None
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

    def bfs_distances(
        self, start: tuple[int, int]
            ) -> dict[tuple[int, int], int]:
        """Compute shortest corridor distances from a starting cell using BFS.

        Args:
            start: Starting row and column.

        Returns:
            Reachable positions mapped to their distance in corridor steps.
        """
        queue: deque[tuple[int, int]] = deque([start])
        distances: dict[tuple[int, int], int] = {start: 0}

        while queue:
            current = queue.popleft()

            for neighbor in self.get_neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        return distances

    def reset_ghost_position(self) -> None:
        """Place the ghost at its original spawn coordinates."""
        self.x = self.start_position[1] * self.config.CELL_SIZE
        self.y = self.start_position[0] * self.config.CELL_SIZE

    def ghost_in_edible(self) -> None:
        """Resolve a ghost collision with Pac-Man according to edible
        and cheat state."""
        pac_man_rect = pygame.Rect(
                    self.Pacman.x,
                    self.Pacman.y,
                    self.config.CELL_SIZE,
                    self.config.CELL_SIZE
                )

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

    def load_ghosts_image(
        self, normal_image_path: str | Path, edible_path: str | Path,
        waiting_path: str | Path
            ) -> None:

        """Load and scale the normal, edible, and waiting ghost sprites.

        Args:
            normal_image_path: Path to the normal ghost image.
            edible_path: Path to the edible ghost image.
            waiting_path: Path to the waiting ghost image.
        """
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

    def draw(
        self, screen: pygame.Surface, offset_x: int, offset_y: int
            ) -> None:
        """Render the current state on the game surface.

        Args:
            screen: Pygame surface receiving the rendered content.
            offset_x: Horizontal rendering offset in pixels.
            offset_y: Vertical rendering offset in pixels.
        """
        sprite: pygame.Surface | None = None
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

        if sprite:
            sprite_rect = sprite.get_rect(
                center=(center_x, center_y)
            )

            screen.blit(sprite, sprite_rect)
