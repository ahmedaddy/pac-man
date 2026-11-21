import pygame


class Button:
    """
    A class representing a button in the game.
    """
    def __init__(
            self, x: float,
            y: float,
            width: int,
            height: int,
            text: str,
            base_color: str,
            hover_color: str,
            text_color: str
            ):
        """
            Initialize the button with its position, size, text, and colors.

            :param x: The x-coordinate of the button's top-left corner.
            :param y: The y-coordinate of the button's top-left corner.
            :param width: The width of the button.
            :param height: The height of the button.
            :param text: The text displayed on the button.
            :param base_color: The base color of the button.
            :param hover_color: The color of the button when hovered over.
            :param text_color: The color of the text on the button.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 36)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.is_hovered = False
        self.text_color = text_color

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button on the given screen.
        params:
            screen: The pygame surface on which to draw the button.
        """
        pygame.draw.rect(
            screen, self.current_color, self.rect, border_radius=7)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_button_events(self, event: pygame.event.Event) -> bool:
        """
        Handle events for the button.
        params:
            event: The pygame event to handle.
        returns:
            bool: True if the button was clicked, False otherwise.
        """
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
    """
    A class representing an input field in the game.
    """
    def __init__(
            self,
            x: float,
            y: float,
            width: int,
            height: int
            ):
        """
        Initialize the input field with its position and size.
        params:
            x: The x-coordinate of the input field's top-left corner.
            y: The y-coordinate of the input field's top-left corner.
            width: The width of the input field.
            height: The height of the input field.
        """
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(x, y, width, height)
        self.is_open = False
        self.text = ""

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the input field on the given screen.
        params:
            screen: The pygame surface on which to draw the input field.
        """
        pygame.draw.rect(screen, "white", self.rect, border_radius=4)
        text_surface = self.font.render(self.text, True, "black")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """
        Handle events for the input field.
        params:
            event: The pygame event to handle.
        returns:
            str | None: The text entered in the input field,
            or None if no text was entered.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_open = self.rect.collidepoint(event.pos)

        elif self.is_open and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif (
                len(self.text) < 10 and
                    (event.unicode.isalnum() or event.unicode.isspace())):
                self.text += event.unicode

        return None
