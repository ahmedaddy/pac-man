import pygame

from .pacman import Pacman
from .components import Button
from .main_menu import Mainmenu
from .score_recorder import ScoreRecorder
import random
from pathlib import Path
from .cheat_mode import CheatMode


class Cell:
    """
    Represents a cell in the maze, with walls in four directions.
    """
    def __init__(self, value: int) -> None:
        """
        Initialize the cell with walls based on the given value.
        The value is expected to be an integer
        where each bit represents a wall:
        - Bit 0 (1): Up wall
        - Bit 1 (2): Right wall
        - Bit 2 (4): Down wall
        - Bit 3 (8): Left wall
        """
        self.up = bool(value & 1)
        self.right = bool(value & 2)
        self.down = bool(value & 4)
        self.left = bool(value & 8)


class Pacgum:

    """
    Represents a pacgum in the game, which can be eaten by Pacman.
    """
    def __init__(
        self, x: int, y: int, size: int, score: int = 10, config=None
            ) -> None:
        """
        Initialize the pacgum with its position, size, and score value.
        """
        self.x = x
        self.y = y
        self.score = score
        self.is_eaten = False
        self.size = size
        self.config = config

    def draw(
            self,
            screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        """
        Draw the pacgum on the screen if it has not been eaten.
        params:
        - screen: The Pygame surface to draw on.
        - offset_x: The x-offset to apply when
            drawing (for centering the maze).
        - offset_y: The y-offset to apply when
            drawing (for centering the maze).
        returns: None
        """
        if not self.is_eaten:

            pygame.draw.circle(
                screen, self.config.ORANGE,
                (self.x + offset_x, self.y + offset_y),
                self.size
                )


class GameEngine:
    """
    The main game engine that handles the game loop, events, and rendering.
    """
    def __init__(self, config, levels: list) -> None:
        """
        Initialize the game engine with the given levels.
        params:
        - levels: A list of level data to load and play.
        returns: None
        """
        pygame.init()
        pygame.display.set_caption("PAC MAN")
        self.config = config
        self.screen = pygame.display.set_mode((
            self.config.WIDTH, self.config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu = Mainmenu(self.screen, self.config)
        self.level = 1
        self.score_recorder = ScoreRecorder(self.screen, self.config)
        self.state = "menu"
        self.levels = levels
        self.pause = False
        self.pause_started_at: int | None = None

        self.load_level(self.levels[0])

        self.cheat = CheatMode(self.screen)
        self.stop_timer: int | None = None
        self.remaining_supergum_effect = None
        # 1 = Win, 2 = lose
        self.game_state = 1

    def load_level(self, map_data: list) -> None:
        """
        Load the level from the given map data.
        params:
        - map_data: A 2D list representing the maze layout.
        returns: None
        """
        from .ghost import Ghosts
        old_pacman = getattr(self, "pacman", None)
        saved_score = old_pacman.score if old_pacman else 0
        saved_lives = old_pacman.lives if old_pacman else 3
        self.map = [
            [Cell(cell) for cell in row]
            for row in map_data
        ]
        self.maze_width = len(self.map[0]) * self.config.CELL_SIZE
        self.maze_height = len(self.map) * self.config.CELL_SIZE
        self.offset_x = (self.config.WIDTH - self.maze_width) // 2
        self.offset_y = (self.config.HEIGHT - self.maze_height) // 2
        self.corners = [
            self.corrdinates_to_pixels(0, 0),
            self.corrdinates_to_pixels(len(self.map[0]) - 1, 0),
            self.corrdinates_to_pixels(0, len(self.map) - 1),
            self.corrdinates_to_pixels(
                len(self.map[0]) - 1,
                len(self.map) - 1
            )
        ]
        self.pacman_starts_positions = self.find_pacman_start_position()
        # spawn pacman at the center of the maze
        self.pacman = Pacman(
            self.pacman_starts_positions[0],
            self.pacman_starts_positions[1],
            self.map,
            self.config.YELLOW,
            self.config
        )
        self.pacman.pacman_starts_positions = (
            self.pacman_starts_positions[0],
            self.pacman_starts_positions[1]
        )
        self.pacman.score = saved_score
        self.pacman.lives = saved_lives
        self.ghosts = [

            Ghosts(
                1, 0, self.map, self.pacman, 2,
                self.config.RED, self, self.config),
            Ghosts(
                len(self.map) - 1, 1, self.map,
                self.pacman, 2, self.config.PINK, self, config=self.config),
            Ghosts(
                1, len(self.map[0]) - 1, self.map,
                self.pacman, 2, self.config.ORANGE, self, config=self.config),
            Ghosts(
                len(self.map) - 2, len(self.map[0]) - 1,
                self.map, self.pacman, 1, self.config.CYAN, self, self.config)
        ]

        assets = Path(__file__).resolve().parent / "assets"
        self.pacman.set_sprite(assets / "pac_man.png")

        ghost_images = [
            "red.png",
            "pink.png",
            "orange.png",
            "cyan.png"
        ]

        edible_name = "edible_ghost.png"
        waiting_name = "waiting_ghost.png"

        for ghost, image_name in zip(self.ghosts, ghost_images):
            ghost.load_ghosts_image(
                assets / image_name, assets / edible_name,
                assets / waiting_name
                )

        self.gums = self.generate_pacgums(1)
        self.super_gums = self.generate_supergums()
        self.gums_state = False
        self.super_gum_timer: int | None = None
        self.start_time = pygame.time.get_ticks()
        self.resume_button = Button(
            self.config.WIDTH // 2 - 140 // 2,
            self.config.HEIGHT // 2 - 40 // 2 + 25,
            140, 40,
            "Resume", "black", "red", "white"
        )

        self.quit_button = Button(
            self.config.WIDTH // 2 - 140 // 2,
            self.config.HEIGHT // 2 - 40 // 2 + 75,
            140, 40,
            "Quit", "black", "red", "white"
        )

    def next_level(self) -> None:
        """
        Move to the next level or end the game if all levels are completed.
        """
        if self.level >= len(self.levels):
            self.state = "score"
            self.level = 1
        else:
            self.level += 1
            self.load_level(self.levels[self.level - 1])
        self.cheat.flags['skip'] = False

    def start_new_game(self) -> None:
        """
        Start a new game by resetting the level, score, and lives.
        """
        self.level = 1
        self.pacman.score = 0
        self.pacman.lives = 3
        self.load_level(self.levels[0])
        self.state = "game"

    def time_remaining(self) -> int:
        """Calculate the remaining time for the current level."""
        limit: int = self.config.LEVEL_TIMER
        ticks: int = pygame.time.get_ticks()
        elapsed: int = ticks - self.start_time
        return max(0, limit - elapsed // 1000)

    def exit(self) -> None:
        """Stop the game."""
        self.running = False

    def gameLoop(self) -> None:
        """Run the main game loop."""

        while self.running:
            if not self.pause:
                if self.state == "menu":
                    self.menu.draw()
                elif self.state == "game":
                    self.screen.fill("#001219")
                    if self.cheat.flags["increase_speed"]:
                        self.pacman.speed = self.config.PLAYER_SPEED * 4
                    else:
                        self.pacman.speed = self.config.PLAYER_SPEED
                    self.pacman.move()
                    if not self.gums_state:
                        for gum in self.gums:
                            gum.draw(
                                screen=self.screen,
                                offset_x=self.offset_x,
                                offset_y=self.offset_y)
                    for gum in self.super_gums:
                        gum.draw(
                            screen=self.screen,
                            offset_x=self.offset_x,
                            offset_y=self.offset_y)
                    for info in self.infos():
                        info.draw(screen=self.screen)
                    self.handle_gums()
                    self.handle_super_pacgums()
                    self.update_super_gum_timer()
                    self.draw_walls()
                    self.pacman.draw(self.screen, self.offset_x, self.offset_y)
                    for ghost in self.ghosts:
                        ghost.draw(self.screen, self.offset_x, self.offset_y)
                        if ghost.is_eaten:
                            continue
                        ghost.ghost_in_edible()
                    if self.cheat.flags['skip']:
                        self.next_level()
                    if not self.cheat.flags["freeze"]:
                        if not ghost.edible:
                            self.ghosts[0].tracking_pacman()
                            self.ghosts[1].move_random_direction()
                            self.ghosts[2].move_random_direction()
                            self.ghosts[3].go_next_pacman()
                        else:
                            for ghost in self.ghosts:
                                ghost.ghost_move(
                                    ghost.start_position[0],
                                    ghost.start_position[1])
                    self.cheat.draw()
                    self.handle_death()
                if self.state == "score":
                    self.score_recorder.draw(
                        self.pacman.score, self.game_state)
            else:
                self.screen.fill("#001219")
                pause_text = Button(
                    self.config.WIDTH // 2 - 40,
                    self.config.HEIGHT // 2 - 70,
                    80, 20,
                    "Game Paused", "black", "black", "white"
                )
                pause_text.draw(self.screen)
                self.resume_button.draw(self.screen)
                self.quit_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(40)
            self.handleEvents()

        pygame.quit()

    def handleEvents(self) -> None:
        """Handle keyboard and window events."""
        for event in pygame.event.get():
            if self.state != "score":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.exit()
                    if event.key == pygame.K_ESCAPE and self.state == "game":
                        self.handle_pause()
                        if self.pause:
                            self.stop_timer = pygame.time.get_ticks()
                        else:
                            if self.stop_timer is not None:
                                self.start_time += (
                                    pygame.time.get_ticks() - self.stop_timer)
                            self.stop_timer = None
            if self.pause:
                if self.resume_button.handle_button_events(event):
                    self.pause = False
                if self.quit_button.handle_button_events(event):
                    self.running = False
            if event.type == pygame.QUIT:
                self.exit()
            if self.state == "game":
                if self.cheat.hundle_event(event):
                    continue
                self.handle_game_event(event)
            elif self.state == "menu":
                res = self.menu.handle_event(event)
                if res == "game":
                    self.start_new_game()
                if res == "quit":
                    self.running = False
            elif self.state == "score":
                rest = self.score_recorder.handle_event(
                    event, self.pacman.score)
                if rest == "menu":
                    self.state = "menu"
            if self.state == "score":
                self.state = "score"

    def handle_game_event(self, event: pygame.event.Event) -> None:
        """
        Handle game-specific events, such as key presses for Pacman's movement.
        params:
        - event: The Pygame event to handle.
        returns: None
        # """
        if event.type == pygame.KEYDOWN:
            directions = {

                pygame.K_UP: self.config.UP,
                pygame.K_DOWN: self.config.DOWN,
                pygame.K_LEFT: self.config.LEFT,
                pygame.K_RIGHT: self.config.RIGHT,
                pygame.K_w: self.config.UP,
                pygame.K_s: self.config.DOWN,
                pygame.K_a: self.config.LEFT,
                pygame.K_d: self.config.RIGHT
            }
            if event.key in directions:
                self.pacman.set_direction(directions[event.key])

    def corrdinates_to_pixels(self, x: int, y: int) -> tuple[int, int]:
        """
        Convert grid coordinates to pixel coordinates for rendering.
        params:
        - x: The x-coordinate in the grid.
        - y: The y-coordinate in the grid.
        returns: A tuple of (pixel_x, pixel_y) coordinates.
        """
        ret_x = (x * self.config.CELL_SIZE) + self.config.CELL_SIZE // 2
        ret_y = (y * self.config.CELL_SIZE) + self.config.CELL_SIZE // 2
        return ret_x, ret_y

    def draw_walls(self) -> None:
        """
        Draw the walls of the maze based on the cell data.
        Each cell has boolean attributes indicating the presence of walls
        in the up, right, down, and left directions.
        """
        for row, cells in enumerate(self.map):
            for col, cell in enumerate(cells):
                x = self.offset_x + col * self.config.CELL_SIZE
                y = self.offset_y + row * self.config.CELL_SIZE
                if cell.up:
                    pygame.draw.line(
                        self.screen,
                        self.config.DARK_BLUE,
                        (x, y),
                        (x + self.config.CELL_SIZE, y),
                        5
                    )
                if cell.right:
                    pygame.draw.line(
                        self.screen,
                        self.config.DARK_BLUE,
                        (x + self.config.CELL_SIZE, y),
                        (x + self.config.CELL_SIZE, y + self.config.CELL_SIZE),
                        5
                    )
                if cell.down:
                    pygame.draw.line(
                        self.screen,
                        self.config.DARK_BLUE,
                        (x, y + self.config.CELL_SIZE),
                        (x + self.config.CELL_SIZE, y + self.config.CELL_SIZE),
                        5
                    )

                if cell.left:
                    pygame.draw.line(
                        self.screen,
                        self.config.DARK_BLUE,
                        (x, y),
                        (x, y + self.config.CELL_SIZE),
                        5
                    )

    def infos(self) -> list[Button]:
        """
        Create and return a list of Button objects displaying game information:
        - Score
        - Lives
        - Level
        - Time remaining
        """
        infos = []

        score = Button(
            self.config.WIDTH // 2, 0, 40, 20,
            f"Score: {self.pacman.score}", "black", "black", "white")
        infos.append(score)
        lives = Button(
            self.config.WIDTH // 2 + 120, 0, 40, 20,
            f"lives: {self.pacman.lives}",
            "black", "black", "white")
        infos.append(lives)
        levels = Button(
            self.config.WIDTH // 2 - 120, 0, 40, 20,
            f"Level: {self.level}", "black", "black", "white")
        infos.append(levels)
        timer = Button(
            self.config.WIDTH // 2 - 240, 0, 40, 20,
            f"Time: {self.time_remaining()}", "black", "black", "white")
        infos.append(timer)
        return infos

    def generate_pacgums(self, number_of_gums: int) -> list[Pacgum]:
        """
        Generate a list of Pacgum objects
        placed at valid positions in the maze.
        params:
        - number_of_gums: The number of pacgums to generate.
        returns: A list of Pacgum objects.
        """
        pac_gums = []
        valid_positions = []
        for row, c in enumerate(self.map):
            for col, i in enumerate(c):
                if self.corrdinates_to_pixels(col, row) in self.corners:
                    continue
                if not all([i.up, i.down, i.left, i.right]):
                    valid_positions.append((col, row))
        if len(valid_positions) < number_of_gums:
            print("Not enough valid positions to place all gums. Placing gums \
in all valid positions.")

        chose_positions = random.sample(valid_positions, min(
            number_of_gums, len(valid_positions)))

        for pos in chose_positions:
            gum_x = (
                pos[0] * self.config.CELL_SIZE
                ) + self.config.CELL_SIZE // 2

            gum_y = (
                pos[1] * self.config.CELL_SIZE
                ) + self.config.CELL_SIZE // 2

            pac_gums.append(Pacgum(
                gum_x, gum_y, self.config.GUM_SIZE,
                self.config.POINTS_PER_GUM, self.config
                )
            )

        return pac_gums

    def generate_supergums(self) -> list[Pacgum]:
        """
        Generate a list of super pacgums placed at the corners of the maze.
        returns: A list of Pacgum objects representing super pacgums.
        """
        super_pacgums = []
        for corner in self.corners:
            super_pacgums.append(
                Pacgum(
                    corner[0], corner[1], self.config.SUPER_GUM_SIZE,
                    self.config.POINTS_PER_SUPER_GUM, config=self.config
                )
            )

        return super_pacgums

    def handle_gums(self) -> None:
        """
        Check for collisions between Pacman and pacgums.
        If Pacman collides with a pacgum, mark it
        as eaten and increase the score.
        If all pacgums are eaten, set the gums_state to True.
        """
        all_done = 0
        for gum in self.gums:
            if not gum.is_eaten:
                all_done += 1
                pac_man_rect = pygame.Rect(
                    self.pacman.x,
                    self.pacman.y,
                    self.config.CELL_SIZE,
                    self.config.CELL_SIZE
                )
                gum_rect = pygame.Rect(
                    gum.x - self.config.GUM_SIZE // 2,
                    gum.y - self.config.GUM_SIZE // 2,
                    self.config.GUM_SIZE,
                    self.config.GUM_SIZE
                )
                if gum_rect.colliderect(pac_man_rect):
                    gum.is_eaten = True
                    self.pacman.score += gum.score
        if all_done == 0:
            self.gums_state = True

    def handle_super_pacgums(self) -> None:
        """
        Check for collisions between Pacman and super pacgums.
        If Pacman collides with a super pacgum, mark it as eaten,
        increase the score, and set all ghosts to edible state.
        """
        for gum in self.super_gums:
            if not gum.is_eaten:
                pac_man_rect = pygame.Rect(
                    self.pacman.x,
                    self.pacman.y,
                    self.config.CELL_SIZE,
                    self.config.CELL_SIZE
                )
                gum_rect = pygame.Rect(
                    gum.x - self.config.GUM_SIZE // 2,
                    gum.y - self.config.GUM_SIZE // 2,
                    self.config.GUM_SIZE,
                    self.config.GUM_SIZE
                )
                if gum_rect.colliderect(pac_man_rect):
                    gum.is_eaten = True
                    self.pacman.score += gum.score
                    for ghost in self.ghosts:
                        ghost.edible = True
                        self.remaining_supergum_effect = self.config.SUPER_GUM_DURATION

                    self.super_gum_timer = pygame.time.get_ticks()

    def update_super_gum_timer(self) -> None:
        """
        Update the timer for the super pacgum effect.
        If the effect duration has passed,
        reset the ghosts to non-edible state.
        """
        if self.super_gum_timer is None or self.pause:
            return
        current_time = pygame.time.get_ticks()
        spent_time = current_time - self.super_gum_timer

        if (self.remaining_supergum_effect is not None
                and spent_time >= self.remaining_supergum_effect):
            for ghost in self.ghosts:
                ghost.edible = False
                ghost.is_eaten = False
            self.super_gum_timer = None

    def handle_death(self) -> None:
        """
        Handle the death of Pacman.
        If Pacman has no lives left or time has run out,
        set the game state to game over.
        If all pacgums are eaten, proceed to the next level.
        """
        if (self.pacman.lives == 0
                or self.time_remaining() == 0 and not self.pause):
            self.game_state = 2
            self.state = "score"
        elif (self.gums_state and
                all(gum.is_eaten for gum in self.super_gums)):
            self.next_level()

    def find_pacman_start_position(self) -> tuple[int, int]:
        """
        Find the starting position for Pacman in the maze.
        Returns the position as a tuple of (row, col).
        """
        center_row = len(self.map) // 2
        center_col = len(self.map[0]) // 2
        valid_cells = [
            (row, col)
            for row, cells in enumerate(self.map)
            for col, cell in enumerate(cells)
            if not (cell.up and cell.right and cell.down and cell.left)
        ]
        return min(
            valid_cells,
            key=lambda pos: abs(pos[0] - center_row) + abs(pos[1] - center_col)
        )

    def handle_pause(self) -> None:
        """
        Handle the pause functionality.
        """
        current_time = pygame.time.get_ticks()

        if not self.pause:
            self.pause = True
            self.pause_started_at = current_time

        else:
            self.pause = False
            if self.pause_started_at is not None:
                paused_duration = (
                    current_time - self.pause_started_at
                )
                if self.super_gum_timer is not None:
                    self.super_gum_timer += paused_duration

                self.pause_started_at = None
