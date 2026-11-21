from __future__ import annotations

from .config import Config

import pygame
from .components import Input, Button
import json
from pathlib import Path


class ScoreRecorder:
    """
    A class to handle the score recording functionality in the game.
    """
    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        """
        Initialize the score recorder.
        """
        pygame.display.set_caption("Record Score --- Pac-Man")
        self.config = config
        self.screen = screen
        self.input = Input(
            (self.config.WIDTH // 2) - 200 / 2,
            (self.config.HEIGHT // 2) - 50 / 2, 200, 50)
        self.font = pygame.font.SysFont(None, 32)
        self.submit_button = Button(
            (self.config.WIDTH // 2) - 100 / 2,
            (self.config.HEIGHT // 2) - 50 / 2 + 100, 100, 50,
            "Submit", "blue", "lightblue", "white")

    def draw(self, score: int, state: int) -> None:
        """
        Draw the score recording interface on the screen.
        params:
            score: The score to display.
            state: The game state (1 for win, 2 for game over).
        """
        self.screen.fill("#001219")

        text_backgound_rect = pygame.draw.rect(
            self.screen,
            "white",
            (
                (self.config.WIDTH // 2) - 200 / 2,
                (self.config.HEIGHT // 2) - 50 / 2 - 100,
                200,
                50,
            ),
        )
        text_surface = self.font.render(
            f"Your Score is {score}", True, "black")
        text_rect = text_surface.get_rect(center=text_backgound_rect.center)
        self.screen.blit(text_surface, text_rect)
        self.input.draw(self.screen)
        self.submit_button.draw(self.screen)
        if state == 2:
            game_over_surface = self.font.render(
                "Game Over", True, "red")
            game_over_rect = game_over_surface.get_rect(
                center=(
                    self.config.WIDTH // 2,
                    (self.config.HEIGHT // 2) - 50 / 2 - 150))
            self.screen.blit(game_over_surface, game_over_rect)
        elif state == 1:
            win_surface = self.font.render(
                "You Win!", True, "green")
            win_rect = win_surface.get_rect(
                center=(
                    self.config.WIDTH // 2,
                    (self.config.HEIGHT // 2) - 50 / 2 - 150))
            self.screen.blit(win_surface, win_rect)

    def handle_event(
            self,
            event: pygame.event.Event,
            score: int
            ) -> str | None:
        """
        Handle events for the score recorder.
        params:
            event: The pygame event to handle.
            score: The score to record.
        returns:
            str | None: "menu" if the score was successfully recorded,
            or None if no action was taken.
        """
        if self.submit_button.handle_button_events(event):
            player_name = self.input.text
            if player_name:
                score_file = Path(self.config.HIGH_SCORE_FILENAME)
                try:
                    with score_file.open("r", encoding="utf-8") as f:
                        high_scores = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    high_scores = {"scores": []}

                if (not isinstance(high_scores, dict) or
                        not isinstance(high_scores.get("scores"), list)):
                    high_scores = {"scores": []}
                if score < 0:
                    score = 0
                high_scores["scores"].append(
                    {
                        "player_name": player_name,
                        "score": score
                    }
                )
                with score_file.open("w", encoding="utf-8") as f:
                    json.dump(high_scores, f, indent=2)
                self.input.text = ""
                return "menu"
            else:
                dialog_surface = self.font.render(
                    "Please enter a name before submitting.", True, "red")
                dialog_rect = dialog_surface.get_rect(
                    center=(
                        self.config.WIDTH // 2,
                        (self.config.HEIGHT // 2) - 50 / 2 + 200))
                self.screen.blit(dialog_surface, dialog_rect)
                print("Please enter a name before submitting.")
        self.input.handle_event(event)
        return None
