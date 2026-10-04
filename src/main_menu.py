import pygame
from .config import config
from .components import Button

height = 800
width = 600

class Mainmenu:
    def __init__(self, screen):
        pygame.init()
        pygame.display.set_caption("Pac-man menu")
        self.running = True
        self.screen = screen
        self.background = pygame.image.load(
            "src/assets/pixel-raining-background.jpg"
        )
        self.play_button = Button((self.screen.get_width() / 2) - 150 / 2,((self.screen.get_height() / 2) - 40 / 2) + height*0.08,150,40, "Play", config.CYAN, config.DARK_BLUE, config.YELLOW)
        self.quit_button = Button((self.screen.get_width() / 2) - 150 / 2,((self.screen.get_height() / 2) - 40 / 2) + height*0.14,150,40, "Quit", config.CYAN, config.DARK_BLUE, config.YELLOW)

    
    def draw(self):
        self.screen.fill("blue")
        # (x, y, width, height)
        self.screen.blit(self.background, (0, 0))
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.play_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def handle_menu_event(self, event):
        if self.play_button.handle_button_events(event):
            return "game"
        if self.quit_button.handle_button_events(event):
            return "quit"
        # if event.type == pygame.KEYDOWN:
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if self.play_button.collidepoint(event.pos):
        #         return "game"
        return None
