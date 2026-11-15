import pygame


class CheatMode():
    def __init__(self, screen):
        self.screen = screen
        self.open = None

        self.flags = {
            "invincibility": False,
            "freeze": False,
            "skip": False
        }

        self.font = pygame.font.Font(None, 26)

        # Button that opens the panel
        self.button_rect = pygame.Rect(
            screen.get_width() - 140, 10, 125, 38
        )

        # Main panel
        self.panel_rect = pygame.Rect(
            screen.get_width() - 290, 55, 275, 180
        )

        # Clickable rows
        self.rows = {}

        for i, key in enumerate(self.flags):
            self.rows[key] = pygame.Rect(
                self.panel_rect.x + 15,
                self.panel_rect.y + 45 + i * 42,
                245,
                34
            )

        self.labels = {
            "invincibility": "Invincibility",
            "freeze": "Freeze Ghosts",
            "skip": "Skip This Level"
        }

    def hundle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.open = not self.open
                return True

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        # Open / close panel
        if self.button_rect.collidepoint(event.pos):
            self.open = not self.open
            return True

        if not self.open:
            return False

        # Toggle the clicked checkbox
        for key, rect in self.rows.items():
            if rect.collidepoint(event.pos):
                self.flags[key] = not self.flags[key]
                return True

        # Consume clicks inside the panel
        if self.panel_rect.collidepoint(event.pos):
            return True

        return False

    def draw(self):
        screen = self.screen

        pygame.draw.rect(
            screen, "#14263A",
            self.button_rect,
            border_radius=6
        )

        self.draw_text(
            "CHEATS",
            self.button_rect.center,
            "#FFD700"
        )

        if not self.open:
            return

        pygame.draw.rect(
            screen, "#0B1524",
            self.panel_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen, "#00E5FF",
            self.panel_rect,
            2,
            border_radius=8
        )

        self.draw_text(
            "CHEAT MODE",
            (self.panel_rect.centerx,
             self.panel_rect.y + 22),
            "#FFD700"
        )

        for key, rect in self.rows.items():

            # Checkbox
            checkbox = pygame.Rect(
                rect.x + 5,
                rect.y + 6,
                22, 22
            )

            enabled = self.flags[key]

            color = "#00E5FF" if enabled else "#64748B"

            pygame.draw.rect(
                screen, color, checkbox, 2,
                border_radius=3
            )

            if enabled:
                pygame.draw.line(
                    screen, "#00FF88",
                    (checkbox.x + 5, checkbox.y + 11),
                    (checkbox.x + 10, checkbox.y + 16),
                    3
                )
                pygame.draw.line(
                    screen, "#00FF88",
                    (checkbox.x + 10, checkbox.y + 16),
                    (checkbox.x + 18, checkbox.y + 5),
                    3
                )

            label = self.font.render(
                self.labels[key],
                True,
                "#FFFFFF"
            )

            screen.blit(
                label,
                (rect.x + 38, rect.y + 7)
            )

    def draw_text(self, text, center, color):
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(center=center)
        self.screen.blit(surface, rect)
