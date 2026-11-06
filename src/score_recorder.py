import pygame
from .components import Input
from .config import config

class ScoreRecorder:
    def __init__(self, screen):
        # pygame.init()
        pygame.display.set_caption("Record Score --- Pac-Man")
        self.screen = screen
        self.input = Input((config.WIDTH // 2) - 200 / 2, (config.HEIGHT // 2) - 50 / 2, 200, 50)
        self.font = pygame.font.SysFont(None, 32)

    def draw(self, score):
        self.screen.fill("#001219")
        text_backgound_rect = pygame.draw.rect(self.screen, "white", ((config.WIDTH // 2) - 200 / 2, (config.HEIGHT // 2) - 50 / 2 - 100, 200, 50))
        text_surface = self.font.render(f"Your Score is {score}", True, "black")
        text_rect = text_surface.get_rect(center=text_backgound_rect.center)
        self.screen.blit(text_surface, text_rect)
        self.input.draw(self.screen)

    def handle_event(self, event):
        self.input.handle_event(event)
        return None

