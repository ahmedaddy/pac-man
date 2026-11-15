import sys
from .utils import Utils
from mazegenerator import MazeGenerator
from .game import GameEngine
from .config import config

def create_levels():
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
    def run(self):
        # try:
        file_name = sys.argv[1]
        file = Utils.read_json_file(file_name)
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
