import pygame

from .config import config
from .pacman import Pacman
from .ghost import Ghosts
from .components import Button
from .main_menu import Mainmenu
import random


class Cell:
    def __init__(self, value):
        self.up = bool(value & 1)
        self.right = bool(value & 2)
        self.down = bool(value & 4)
        self.left = bool(value & 8)


class Pacgum:
    def __init__(self, x, y, size, score=10):
        self.x = x
        self.y = y
        self.score = score
        self.is_eaten = False
        self.size = size

    def draw(self, screen, offset_x, offset_y):
        if not self.is_eaten:
            pygame.draw.circle(screen, config.ORANGE, (self.x + offset_x, self.y + offset_y), self.size)


class GameEngine:
    def __init__(self, map_data):
        """Initialize the game."""
        pygame.init()
        pygame.display.set_caption("PAC MAN")
        self.clock = pygame.time.Clock()
        self.map = [
            [Cell(cell) for cell in row]
            for row in map_data
        ]
        self.maze_width = len(self.map[0]) * config.CELL_SIZE
        self.maze_height = len(self.map) * config.CELL_SIZE
        self.offset_x = (config.WIDTH - self.maze_width) // 2
        self.offset_y = (config.HEIGHT - self.maze_height) // 2
        self.corners = [
            self.corrdinates_to_pixels(0, 0),
            self.corrdinates_to_pixels(0, len(self.map[0]) - 1),
            self.corrdinates_to_pixels(len(self.map) - 1, 0),
            self.corrdinates_to_pixels(len(self.map) - 1, len(self.map[0]) - 1)
        ]
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        # spawn pacman at the center of the maze
        self.pacman = Pacman(
            len(self.map) // 2,
            len(self.map[0]) // 2,
            self.map
        )
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.red_ghost = Ghosts(
            1,
            0,
            self.map
        )
        self.pink_ghost = Ghosts(
            self.rows - 1,
            1,
            self.map
        )
        self.orange_ghost = Ghosts(
            1,
            self.cols - 1,
            self.map
        )
        self.cyan_ghost = Ghosts(
            self.rows - 2,
            self.cols - 1,
            self.map
        )
        self.running = True
        self.state = "menu"
        self.menu = Mainmenu(self.screen)
        self.gums = self.generate_pacgums()
        self.super_gums = self.generate_supergums()
        self.gums_state = False

    def exit(self):
        """Stop the game."""
        self.running = False

    def gameLoop(self):
        """Run the main game loop."""

        while self.running:
            if self.state == "menu":
                self.menu.draw()
            elif self.state == "game":
                self.screen.fill("#001219")
                self.pacman.move()
                if not self.gums_state:
                    for gum in self.gums:
                        gum.draw(screen=self.screen, offset_x=self.offset_x, offset_y=self.offset_y)
                for gum in self.super_gums:
                    gum.draw(screen=self.screen, offset_x=self.offset_x, offset_y=self.offset_y)
                for info in self.infos():
                    info.draw(screen=self.screen)
                self.handle_gums()
                self.draw_walls()
                self.pacman.draw(self.screen, self.offset_x, self.offset_y, config.YELLOW)
                self.red_ghost.draw(self.screen, self.offset_x, self.offset_y, config.RED)
                self.pink_ghost.draw(self.screen, self.offset_x, self.offset_y, config.PINK)
                self.orange_ghost.draw(self.screen, self.offset_x, self.offset_y, config.ORANGE)
                self.cyan_ghost.draw(self.screen, self.offset_x, self.offset_y, config.CYAN)
                # self.red_ghost.ghost_move()
                self.pink_ghost.move_random_direction()
                # self.orange_ghost.move_random_direction()
                self.cyan_ghost.ghost_move(self.pacman.get_current_cell())
                # self.drawPacman()
            pygame.display.flip()
            self.clock.tick(60)
            self.handleEvents()

        pygame.quit()

    def handleEvents(self):
        """Handle keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.exit()

            if event.type == pygame.QUIT:
                self.exit()
            if self.state == "game":
                self.handle_game_event(event)
            elif self.state == "menu":
                res = self.menu.handle_menu_event(event)
                if res == "game":
                    self.state = "game"
                if res == "quit":
                    self.running = False

    def handle_game_event(self, event):
        if event.type == pygame.KEYDOWN:
            directions = {
                pygame.K_UP: config.UP,
                pygame.K_DOWN: config.DOWN,
                pygame.K_LEFT: config.LEFT,
                pygame.K_RIGHT: config.RIGHT,
            }
            if event.key in directions:
                self.pacman.set_direction(directions[event.key])
    
    def corrdinates_to_pixels(self, x, y):
        ret_x = (x * config.CELL_SIZE) + config.CELL_SIZE // 2
        ret_y = (y * config.CELL_SIZE) + config.CELL_SIZE // 2
        return ret_x, ret_y

    def draw_walls(self):
        """Draw the maze walls."""
        for row, cells in enumerate(self.map):
            for col, cell in enumerate(cells):
                x = self.offset_x + col * config.CELL_SIZE
                y = self.offset_y + row * config.CELL_SIZE
                if cell.up:
                    pygame.draw.line(
                        self.screen,
                        config.DARK_BLUE,
                        (x, y),
                        (x + config.CELL_SIZE, y),
                        5
                    )
                if cell.right:
                    pygame.draw.line(
                        self.screen,
                        config.DARK_BLUE,
                        (x + config.CELL_SIZE, y),
                        (x + config.CELL_SIZE, y + config.CELL_SIZE),
                        5
                    )
                if cell.down:
                    pygame.draw.line(
                        self.screen,
                        config.DARK_BLUE,
                        (x, y + config.CELL_SIZE),
                        (x + config.CELL_SIZE, y + config.CELL_SIZE),
                        5
                    )

                if cell.left:
                    pygame.draw.line(
                        self.screen,
                        config.DARK_BLUE,
                        (x, y),
                        (x, y + config.CELL_SIZE),
                        5
                    )

    def drawPacman(self):
        center_x = self.offset_x + self.pacman.x + config.CELL_SIZE // 2
        center_y = self.offset_y + self.pacman.y + config.CELL_SIZE // 2

        pygame.draw.circle(
            self.screen,
            config.YELLOW,
            (center_x, center_y),
            config.BALL_SIZE
        )

    def infos(self):
        infos = []
        score = Button(config.WIDTH // 2, 0, 40, 20, f"Score: {self.pacman.score}", "black", "black", "white")
        infos.append(score)
        return infos

    def generate_pacgums(self):
        pac_gums = []
        for row, c in enumerate(self.map):
            for col, i in enumerate(c):
                if self.corrdinates_to_pixels(col, row) in self.corners:
                    continue
                if not all([i.up, i.down, i.left, i.right]):
                    chosen_number = random.choices(
                        [0, 1],
                        weights=[0, 1.0])[0]
                    if chosen_number:
                        gum_x = (col * config.CELL_SIZE) + config.CELL_SIZE // 2
                        gum_y = (row * config.CELL_SIZE) + config.CELL_SIZE // 2
                        pac_gums.append(Pacgum(gum_x, gum_y, config.GUM_SIZE, 10))
        return pac_gums

    def generate_supergums(self):
        super_pacgums = []
        for corner in self.corners:
            super_pacgums.append(Pacgum(corner[0], corner[1], config.SUPER_GUM_SIZE, 50))
        return super_pacgums

    def handle_gums(self):
        all_done = 0
        for gum in self.gums:
            if not gum.is_eaten:
                all_done += 1
                pac_man_rect = pygame.Rect(
                    self.pacman.x,
                    self.pacman.y,
                    config.CELL_SIZE,
                    config.CELL_SIZE
                )
                gum_rect = pygame.Rect(
                    gum.x - config.GUM_SIZE,
                    gum.y - config.GUM_SIZE,
                    config.GUM_SIZE,
                    config.GUM_SIZE
                )
                if gum_rect.colliderect(pac_man_rect):
                    gum.is_eaten = True
                    self.pacman.score += 10
        if all_done == 0:
            self.gums_state = True
