from mazegenerator import MazeGenerator
from .game import GameEngine
from .config import config
from .cli import CLI


def create_levels() -> list:
    """
    Create levels for the game based on the configuration settings.
    returns:
        list: A list of generated levels.
    """
    levels = []
    for settings in config.LEVEL_SETTINGS:
        maze = MazeGenerator(
            size=(settings['size']),
            perfect=False,
            entry_cell=(1, 1),
            exit_cell=(-1, -1),
            seed=settings["seed"]
        )
        levels.append(maze.maze)

    return levels


class Main:
    def run(self) -> None:
        # try:
        cli_command = CLI()
        cli_command.load_json_file()
        config_dict = cli_command.config_dict
        for key in config_dict:
            key = key.upper()
        # config = config(**config_dict)
        levels = create_levels()
        # print(levels[0])
        game = GameEngine(levels)
        game.gameLoop()
        # except Exception as e:
        #     print(f"An error occurred: {e}", file=sys.stderr)
        #     sys.exit(1)


if __name__ == "__main__":
    main = Main()
    main.run()
