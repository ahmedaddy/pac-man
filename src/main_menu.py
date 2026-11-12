import pygame
from .config import config
from .components import Button
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
# <<<<<<< HEAD
        # self.play_button = Button((self.screen.get_width() / 2) - 150 / 2,((self.screen.get_height() / 2) - 40 / 2) + height*0.08,150,40, "Play", config.CYAN, config.DARK_BLUE, config.YELLOW)
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
        # self.quit_button = Button((self.screen.get_width() / 2) - 150 / 2,((self.screen.get_height() / 2) - 40 / 2) + height*0.14,150,40, "Quit", config.CYAN, config.DARK_BLUE, config.YELLOW)
        self.scores = Utils.read_json_file("./high_scores.json")
# =======
#         self.play_button = Button((self.screen.get_width() / 2) - 150 / 2,((self.screen.get_height() / 2) - 40 / 2) + height*0.08,150,40, "Play", config.CYAN, config.DARK_BLUE, config.YELLOW)
#         self.quit_button = Button((self.screen.get_width() / 2) - 150 / 2,((self.screen.get_height() / 2) - 40 / 2) + height*0.14,150,40, "Quit", config.CYAN, config.DARK_BLUE, config.YELLOW)
#         self.scores = Utils.read_json_file("./high_scores.json") or {"scores": []}
# >>>>>>> b274d6acd49e7774a79b409df8c784ea72b37e9f
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
            self.draw_hover(self.draw_highscores())

    # def handle_event(self, event):
    #     if self.play_button.handle_button_events(event):
    #         return "game"
    #     if self.quit_button.handle_button_events(event):
    #         return "quit"
    #     # if event.type == pygame.KEYDOWN:
    #     # if event.type == pygame.MOUSEBUTTONDOWN:
    #     #     if self.play_button.collidepoint(event.pos):
    #     #         return "game"
    #     return None
    # def handle_event(self, event):
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if event.button == 1:
    #             for action, rect in self.menu_buttons.items():
    #                 if rect.collidepoint(event.pos):
    #                     return action

    #     return None
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
                        or {"scores": []}
                    )
                    self.page = "highscores"
                    return None

                if self.quit_game_rect.collidepoint(event.pos):
                    return "quit"

        return None
# <<<<<<< HEAD

    # def draw_highscore(self):
    #     text_surface = self.font.render("High Scores", True, "red")
    #     text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2 + self.screen.get_width() * 0.25, (self.screen.get_height() / 2) - self.screen.get_height() * 0.25))
    #     self.screen.blit(text_surface, text_rect)
    #     # print(self.scores['scores'])
    #     for i, score in enumerate(self.scores['scores']):
    #         score_surface = self.font.render(score['player_name'] + ": " + str(score["high_score"]), True, "red")
    #         score_rect = score_surface.get_rect(center=((self.screen.get_width() / 2 + self.screen.get_width() * 0.25) , (self.screen.get_height() / 2) - self.screen.get_height() * 0.25 + (i + 1) * 30))
    #         self.screen.blit(score_surface, score_rect)
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
            key=lambda score: score["high_score"],
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
            points = score["high_score"]

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
# =======
    
#     def draw_highscore(self):
#         text_surface = self.font.render("High Scores", True, "red")
#         text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2 + self.screen.get_width() * 0.25, (self.screen.get_height() / 2) - self.screen.get_height() * 0.25))
#         self.screen.blit(text_surface, text_rect)
#         # print(self.scores['scores'])
#         for i, score in enumerate(self.scores['scores']):
#             score_surface = self.font.render(score['player_name'] + ": " + str(score["score"]), True, "red")
#             score_rect = score_surface.get_rect(center=((self.screen.get_width() / 2 + self.screen.get_width() * 0.25) , (self.screen.get_height() / 2) - self.screen.get_height() * 0.25 + (i + 1) * 30))
#             self.screen.blit(score_surface, score_rect)
# >>>>>>> b274d6acd49e7774a79b409df8c784ea72b37e9f
