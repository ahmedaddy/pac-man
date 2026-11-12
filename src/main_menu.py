import pygame
from .config import config
# from .components import Button
from .utils import Utils

height = config.HEIGHT
width = config.WIDTH


class Mainmenu:
    def __init__(self, screen):
        pygame.init()
        pygame.display.set_caption("Pac-man menu")
        self.screen = screen
        self.background = pygame.image.load(
            "src/assets/home_pacman.png"
        ).convert()
        self.background = pygame.transform.smoothscale(
            self.background,
            self.screen.get_size()
        )
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.start_game_rect = pygame.Rect(
            int(screen_width * 0.04),
            int(screen_height * 0.26),
            int(screen_width * 0.30),
            int(screen_height * 0.075)
        )
        self.quit_game_rect = pygame.Rect(
            int(self.screen.get_width() * 0.04),
            int(self.screen.get_height() * 0.52),
            int(self.screen.get_width() * 0.30),
            int(self.screen.get_height() * 0.075)
            )
        self.highscores_rect = pygame.Rect(
            int(self.screen.get_width() * 0.04),
            int(self.screen.get_height() * 0.35),
            int(self.screen.get_width() * 0.30),
            int(self.screen.get_height() * 0.075)
            )
        self.instructions_rect = pygame.Rect(
            int(self.screen.get_width() * 0.04),
            int(self.screen.get_height() * 0.44),
            int(self.screen.get_width() * 0.30),
            int(self.screen.get_height() * 0.075)
        )
        self.menu_buttons = {
            "game": self.start_game_rect,
            "quit": self.quit_game_rect
        }

        self.page = "menu"

        self.back_rect = pygame.Rect(
            30,
            self.screen.get_height() - 70,
            140,
            45
        )
        self.scores = Utils.read_json_file("./high_scores.json")
        self.font = pygame.font.SysFont(None, 36)

    def draw(self):
        self.screen.fill("black")
        # (x, y, width, height)
        self.screen.blit(self.background, (0, 0))
        if self.page == "menu":
            self.draw_hover(self.start_game_rect)
            self.draw_hover(self.highscores_rect)
            self.draw_hover(self.instructions_rect)
            self.draw_hover(self.quit_game_rect)

        elif self.page == "highscores":
            self.draw_highscores()

    def handle_event(self, event):

        if self.page == "highscores":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.page = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_rect.collidepoint(event.pos):
                        self.page = "menu"

            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.start_game_rect.collidepoint(event.pos):
                    return "game"

                if self.highscores_rect.collidepoint(event.pos):
                    self.scores = (
                        Utils.read_json_file("./high_scores.json")
                        or {"score": []}
                    )
                    self.page = "highscores"
                    return None

                if self.quit_game_rect.collidepoint(event.pos):
                    return "quit"

        return None

    def draw_highscores(self):

        width, height = self.screen.get_size()

        # Dark transparent overlay
        overlay = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 230))
        self.screen.blit(overlay, (0, 0))

        # Title
        title_font = pygame.font.SysFont(None, 50)

        title = title_font.render(
            "TOP 10 HIGHSCORES",
            True,
            config.YELLOW
        )

        title_rect = title.get_rect(
            center=(width // 2, 70)
        )

        self.screen.blit(title, title_rect)

        # Read and sort scores
        scores = self.scores.get("scores", [])

        scores = sorted(
            scores,
            key=lambda score: score["score"],
            reverse=True
        )[:10]

        # Display scores
        if not scores:
            empty_text = self.font.render(
                "No highscores yet!",
                True,
                config.CYAN
            )

            self.screen.blit(
                empty_text,
                empty_text.get_rect(
                    center=(width // 2, height // 2)
                )
            )

        for i, score in enumerate(scores):

            name = score["player_name"]
            points = score["score"]

            text = f"{i + 1}. {name} - {points}"

            text_surface = self.font.render(
                text,
                True,
                config.CYAN
            )

            text_rect = text_surface.get_rect(
                center=(width // 2, 140 + i * 35)
            )

            self.screen.blit(text_surface, text_rect)

        # Back button
        pygame.draw.rect(
            self.screen,
            config.DARK_BLUE,
            self.back_rect,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            config.YELLOW,
            self.back_rect,
            width=2,
            border_radius=8
        )

        back_text = self.font.render(
            "BACK",
            True,
            config.YELLOW
        )

        self.screen.blit(
            back_text,
            back_text.get_rect(
                center=self.back_rect.center
            )
        )

    def draw_hover(self, rect):
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):

            hover = pygame.Surface(
                (rect.width, rect.height),
                pygame.SRCALPHA
            )

            hover.fill((255, 255, 255, 40))

            self.screen.blit(
                hover,
                rect.topleft
            )
