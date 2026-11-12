import pygame
from .components import Input, Button
from .config import config
import json
from pathlib import Path

class ScoreRecorder:
    def __init__(self, screen):
        # pygame.init()
        pygame.display.set_caption("Record Score --- Pac-Man")
        self.screen = screen
        self.input = Input((config.WIDTH // 2) - 200 / 2, (config.HEIGHT // 2) - 50 / 2, 200, 50)
        self.font = pygame.font.SysFont(None, 32)
        self.submit_button = Button((config.WIDTH // 2) - 100 / 2, (config.HEIGHT // 2) - 50 / 2 + 100, 100, 50, "Submit", "blue", "lightblue", "white")

    def draw(self, score):
        self.screen.fill("#001219")
        text_backgound_rect = pygame.draw.rect(self.screen, "white", ((config.WIDTH // 2) - 200 / 2, (config.HEIGHT // 2) - 50 / 2 - 100, 200, 50))
        text_surface = self.font.render(f"Your Score is {score}", True, "black")
        text_rect = text_surface.get_rect(center=text_backgound_rect.center)
        self.screen.blit(text_surface, text_rect)
        self.input.draw(self.screen)
        self.submit_button.draw(self.screen)


    def handle_event(self, event, score):
        if self.submit_button.handle_button_events(event):
            player_name = self.input.text
            if player_name:
                score_file = Path("high_scores.json")
                try:
                    with score_file.open("r", encoding="utf-8") as f:
                        high_scores = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    high_scores = {"scores": []}

                if not isinstance(high_scores, dict) or not isinstance(high_scores.get("scores"), list):
                    high_scores = {"scores": []}
                high_scores["scores"].append(
                    {
                        "player_name": player_name,
                        "score": score
                    }
                )
                with score_file.open("w", encoding="utf-8") as f:
                    json.dump(high_scores, f, indent=2)
                print(f"Score recorded for {player_name}")
                # stop the game or return to main menu after recording the score
                return "menu"
            else:
                print("Please enter a name before submitting.")
        self.input.handle_event(event)
        return None

