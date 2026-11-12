import pygame

class Button:
    def __init__(self, x, y, width, height, text, base_color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 36)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color 
        self.is_hovered = False
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=7)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_button_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
                self.is_hovered = True
            else:
                self.current_color = self.base_color
                self.is_hovered = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                return True
        return False


class Input:
    def __init__(self, x, y, width, height):
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(x, y, width, height)
        self.is_open = False
        self.text = ""

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect, border_radius=4)
        text_surface = self.font.render(self.text, True, "black")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_open = self.rect.collidepoint(event.pos)

        elif self.is_open and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif event.unicode.isprintable():
                self.text += event.unicode

        return None