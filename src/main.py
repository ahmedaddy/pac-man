import sys
from .utils import Utils
from mazegenerator import MazeGenerator
from .game import GameEngine


class Main:
    def run(self):
        # try:
        file_name = sys.argv[1]
        file = Utils.read_json_file(file_name)
        Maze = MazeGenerator(
            size=(file.get('width', 15), file.get('height', 15)),
            perfect=False,
            entry_cell=(10, 10),
            exit_cell=(-1, -1),
            seed=file.get('seed', 42)
            )
        Maze.generate(int(file.get('seed', 42)))
        game = GameEngine(Maze.maze)
        game.gameLoop()
        print(f"Processing file: {file.get('seed', 42)}")
        print(f"Generated maze: {Maze.maze}")
        # except Exception as e:
        #     print(f"An error occurred: {e}", file=sys.stderr)
        #     sys.exit(1)


if __name__ == "__main__":
    main = Main()
    main.run()
