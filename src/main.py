from mazegenerator import MazeGenerator
from .config import Config
from .game import GameEngine
from .cli import CLI
from .utils import Utils


def create_levels():
    levels = []
    for settings in Config.LEVEL_SETTINGS:
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
    def run(self):
        cli_command = CLI()
        cli_command.load_json_file()
        config_dict = cli_command.config_dict
        if not Utils.check_config(config_dict):
            return
        config_dict = {
            key.upper(): value for key, value in config_dict.items()}
        config = Config()
        config.load_config(config_dict)
        levels = create_levels()
        game = GameEngine(config, levels)
        game.gameLoop()


if __name__ == "__main__":
    main = Main()
    main.run()
