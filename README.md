*This project has been created as part of the 42 curriculum by aaddy, jgaadi*
# Pac-Man

## Decription
A playable Pac-Man-style game written in Python with Pygame.
Mazes are created with the supplied `mazegenerator` package and the game uses a modular, object-oriented design.

## Features

- Main menu, instructions, persistent highscores, and end-of-game name entry.
- Ten generated maze levels with four ghosts, scoring, lives, timer, and pause support.
- Pac-gums, super pac-gums, edible ghosts, and reviewer-oriented cheats.

## Requirements

Python 3.10+, Pygame 2.6+, and the included `mazegenerator` package.

## Installation

```sh
python3 -m pip install -r requirements.txt
```

## Run the game

```sh
python3 -m src.pac-man config.json
make run
```

Run from the repository root; the included `config.json` is a working starting configuration.

## Controls

| Action | Control |
| --- | --- |
| Move Pac-Man | Arrow keys or `W` `A` `S` `D` or `Arrow` keys |
| Pause / resume | `Escape` |
| Open or close cheats | `C` or the **CHEATS** button |
| Menu navigation | Left mouse button |
| Quit during a game | `Q` |

When the game ends, enter a player name and click **Submit** to return to the main menu.

## How to play

Eat every regular and super pac-gum to clear a level; super pac-gums temporarily make ghosts edible.
Normal ghost collisions cost a life, and the game ends at zero lives or when the timer expires; score and lives carry between levels.

## Configuration

Configuration is JSON; lines whose first non-space character is `#` are ignored.
Unknown keys are ignored, while missing required keys produce a clear error and stop the launcher.

| Key | Type | Example | Purpose |
| --- | --- | --- | --- |
| `high_score_filename` | string | `"high_scores.json"` | JSON file used for saved scores |
| `player_speed` | integer | `4` | Pac-Man movement speed |
| `player_lives` | integer | `3` | Starting lives |
| `level_timer` | integer | `40` | Seconds available for each level |
| `numbers_of_gums` | integer | `20` | Regular pac-gums in level one |
| `points_per_gum` | integer | `10` | Points per regular pac-gum |
| `points_per_super_gum` | integer | `50` | Points per power pellet |
| `points_per_ghost` | integer | `200` | Configured ghost-score value |

The game increases `numbers_of_gums` by five after every completed level. Levels are in `src/config.py`; the first uses seed `42`, and generation uses `perfect=False`.

Example configuration:

```json
{
  "high_score_filename": "high_scores.json",
  "player_speed": 4,
  "player_lives": 3,
  "level_timer": 40,
  "numbers_of_gums": 20,
  "points_per_gum": 10,
  "points_per_super_gum": 50,
  "points_per_ghost": 200
}
```

## Cheat mode

Open cheat mode with `C` or the **CHEATS** button:

- **Invincibility** prevents normal ghost collisions from costing a life.
- **Freeze Ghosts** stops ghost movement.
- **Skip This Level** immediately completes the active level.
- **High Speed 300km/h** multiplies Pac-Man's configured speed by four.

## Highscores

Scores are stored as JSON at `high_score_filename`, which defaults to `high_scores.json`.
An absent or invalid score file is recreated on submission; the menu displays the ten highest scores first.

## Project layout

```text
src/pac-man.py       Application entry point and maze creation
src/game.py          Game loop, levels, collisions, HUD, and pause state
src/player.py        Grid-aware player movement and rendering
src/ghost.py         Ghost AI, pathfinding, and edible state
src/main_menu.py     Menu, instructions, and highscore display
src/score_recorder.py  End-of-game score entry and persistence
src/cheat_mode.py    Cheat-panel UI and feature flags
src/assets/          Sprites and instruction artwork
mazegenerator/       Supplied external maze-generator package
config.json          Example runtime configuration
```

## Development commands

```sh
make lint
make clean
```
