from __future__ import annotations

from .config import Config

import pygame
from .utils import Utils


class Mainmenu:
    """Render and handle the main menu, instructions, and highscores."""

    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        """Load menu artwork and initialize navigation controls.

        Args:
            screen: Pygame surface receiving the rendered content.
            config: Game configuration settings.
        """
        pygame.display.set_caption("Pac-man menu")
        self.screen: pygame.Surface = screen
        self.config: Config = config
        self.background = pygame.image.load(
            "src/assets/home_pacman.png"
        ).convert()
        self.background = pygame.transform.smoothscale(
            self.background,
            self.screen.get_size()
        )

        self.instruction_img = pygame.image.load(
            "src/assets/pac_strike_instructions.png"
        ).convert()
        self.screen_size = self.screen.get_size()
        self.instruction_img = pygame.transform.smoothscale(
            self.instruction_img,
            (self.screen_size[0] // 1.3, self.screen_size[1] // 1.3))

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

        self.menu_buttons: dict[str, pygame.Rect] = {
            "game": self.start_game_rect,
            "quit": self.quit_game_rect
        }

        self.page: str = "menu"

        self.back_rect = pygame.Rect(
            30,
            self.screen.get_height() - 70,
            140,
            45
        )

        self.scores = Utils.read_json_file(self.config.HIGH_SCORE_FILENAME)
        self.font: pygame.font.Font = pygame.font.SysFont(None, 36)

    def draw(self) -> None:

        """Render the current state on the game surface."""
        self.screen.fill("black")
        self.screen.blit(self.background, (0, 0))

        if self.page == "menu":
            self.draw_hover(self.start_game_rect)
            self.draw_hover(self.highscores_rect)
            self.draw_hover(self.instructions_rect)
            self.draw_hover(self.quit_game_rect, True)

        elif self.page == "highscores":
            self.draw_highscores()

        elif self.page == "instruction":
            self.draw_instruction()

    def handle_event(self, event: pygame.event.Event) -> str | None:

        """Process input events and return any
        requested screen transition or text.

        Args:
            event: Pygame input event to process.

        Returns:
            The requested game or quit action, or None for menu navigation.
        """
        if self.page == "highscores" or self.page == "instruction":

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
                        Utils.read_json_file(self.config.HIGH_SCORE_FILENAME)
                        or {"scores": []}
                    )
                    self.page = "highscores"

                    return None

                elif self.instructions_rect.collidepoint(event.pos):
                    self.page = "instruction"

                if self.quit_game_rect.collidepoint(event.pos):
                    return "quit"

        return None

    def init_inst_scr_page(self, title: str) -> pygame.Surface:
        """Draw a titled overlay and back button for a menu subpage.

        Args:
            title: Heading text for the overlay.

        Returns:
            The rendered translucent overlay surface.
        """
        width, height = self.screen.get_size()

        overlay = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 230))
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont(None, 50)

        title = title_font.render(
            title,
            True,
            self.config.YELLOW
        )

        title_rect = title.get_rect(
            center=(width // 2, 60)
        )

        self.screen.blit(title, title_rect)

        pygame.draw.rect(
            self.screen,
            self.config.DARK_BLUE,
            self.back_rect,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            self.config.YELLOW,
            self.back_rect,
            width=2,
            border_radius=8
        )

        back_text = self.font.render(
            "BACK",
            True,
            self.config.YELLOW
        )

        self.screen.blit(
            back_text,
            back_text.get_rect(
                center=self.back_rect.center
            )
        )

        return overlay

    def draw_highscores(self) -> None:

        """Render the ten highest stored scores in descending order."""
        self.init_inst_scr_page("TOP 10 HIGHSCORES")

        scores = self.scores.get("scores", [])

        scores = sorted(
            scores,
            key=lambda score: score["score"],
            reverse=True
        )[:10]

        if not scores:
            empty_text = self.font.render(
                "No highscores yet!",
                True,
                self.config.CYAN
            )

            self.screen.blit(
                empty_text,
                empty_text.get_rect(
                    center=(self.config.WIDTH // 2, self.config.HEIGHT // 2)
                )
            )

        for i, score in enumerate(scores):

            name = score["player_name"]
            points = score["score"]

            text = f"{i + 1}. {name} - {points}"

            text_surface = self.font.render(
                text,
                True,
                self.config.CYAN
            )

            text_rect = text_surface.get_rect(
                center=(self.config.WIDTH // 2, 140 + i * 35)
            )

            self.screen.blit(text_surface, text_rect)

    def draw_hover(self, rect: pygame.Rect, is_quit: bool = False) -> None:
        """Draw a translucent highlight over a hovered menu rectangle.

        Args:
            rect: Rectangle to highlight.
            is_quit: Whether to use the quit-button highlight.
        """
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):

            hover = pygame.Surface(
                (rect.width, rect.height),
                pygame.SRCALPHA
            )
            if is_quit:
                hover.fill((255, 25, 25, 40))
            else:
                hover.fill((255, 255, 255, 40))

            self.screen.blit(
                hover,
                rect.topleft
            )

    def draw_instruction(self) -> None:
        """Render the instructions image over the menu overlay."""
        self.init_inst_scr_page("Game Instruction")
        self.screen.blit(self.instruction_img, self.instruction_img.get_rect(
            center=(
                self.screen.get_width() // 2, self.screen.get_height() // 2
                )))
