import pygame
from .config import config

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
        self.font = pygame.font.SysFont(None, 36)
        # self.buttons = {
        #     "play":
        # }
        self.play_button = pygame.Rect(0, 0, 150, 40)
        self.play_text = self.font.render("Play", True, config.YELLOW)
    
    def draw(self):
        self.screen.fill("blue")
        # (x, y, width, height)
        self.screen.blit(self.background, (0, 0))
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        mouse = pygame.mouse.get_pos()
        # play_button = pygame.Rect(0, 0, 150, 40)
        self.play_button.center = self.screen.get_rect().center
        self.play_button.y += 100
        # print("mouse", mouse)
        # print(f"top left: {play_button.topleft}")
        if self.play_button.topleft[0] <= mouse[0] <= self.play_button.topleft[0] + self.play_button.width and self.play_button.topleft[1] <= mouse[1] <= self.play_button.topleft[1] + self.play_button.height:
            pygame.draw.rect(self.screen, config.DARK_BLUE, self.play_button, border_radius=7)
            text_surface = self.play_text.get_rect(center=self.play_button.center)
            self.screen.blit(self.play_text, text_surface)
        else:
            pygame.draw.rect(self.screen, config.CYAN, self.play_button, border_radius=7)
            text_surface = self.play_text.get_rect(center=self.play_button.center)
            self.screen.blit(self.play_text, text_surface)        

    def handle_menu_event(self, event):
        # if event.type == pygame.KEYDOWN:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                return "game"
        return None
