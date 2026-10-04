import pygame

from .config import config
from .pacman import Pacman
from .main_menu import Mainmenu

class Cell:
    def __init__(self, value):
        self.up = bool(value & 1)
        self.right = bool(value & 2)
        self.down = bool(value & 4)
        self.left = bool(value & 8)


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
        map_width = len(self.map[0]) * config.CELL_SIZE
        map_height = len(self.map) * config.CELL_SIZE
        self.screen = pygame.display.set_mode((800, 600))
        self.pacman = Pacman(
            1,
            1,
            self.map
        )
        self.running = True
        self.state = "menu"
        self.menu = Mainmenu(self.screen)


    def exit(self):
        """Stop the game."""
        self.running = False

    def gameLoop(self):
        """Run the main game loop."""

        while self.running:
            if self.state == "menu":
                self.menu.draw()
            elif self.state == "game":
                self.pacman.move()
                self.screen.fill("#001219")
                self.draw_walls()
                self.drawPacman()
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

            # elif event.type == pygame.KEYDOWN:
            #     directions = {
            #         pygame.K_UP: config.UP,
            #         pygame.K_DOWN: config.DOWN,
            #         pygame.K_LEFT: config.LEFT,
            #         pygame.K_RIGHT: config.RIGHT,
            #     }
            #     if event.key in directions:
            #         self.pacman.set_direction(directions[event.key])
            #     if event.key == pygame.K_q:
            #         self.exit()

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

    def draw_walls(self):
        """Draw the maze walls."""
        for row, cells in enumerate(self.map):
            for col, cell in enumerate(cells):
                x = col * config.CELL_SIZE
                y = row * config.CELL_SIZE
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
        center_x = self.pacman.x + config.CELL_SIZE // 2
        center_y = self.pacman.y + config.CELL_SIZE // 2

        pygame.draw.circle(
            self.screen,
            config.YELLOW,
            (center_x, center_y),
            10
        )
