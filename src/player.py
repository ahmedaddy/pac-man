from .config import config
import pygame


class Player:
    """
    A class representing the player in the game.
    """
    def __init__(
            self,
            row: int,
            col: int,
            map_data: list,
            color: tuple
            ) -> None:
        """
        Initialize the player with its position, map data, and color.
        params:
            row: The row index of the player's starting position.
            col: The column index of the player's starting position.
            map_data: The map data representing the game environment.
            color: The color of the player.
        """
        self.x = col * config.CELL_SIZE
        self.y = row * config.CELL_SIZE
        self.map = map_data
        self.GameEngine = None

        self.speed = config.PLAYER_SPEED
        self.direction = None
        self.desired_direction = None
        self.color = color

    def is_aligned(self):
        """
        Check if the player is aligned with the grid.
        returns:
            bool: True if the player is aligned with the grid, otherwise False.
        """
        return (
            self.x % config.CELL_SIZE == 0
            and self.y % config.CELL_SIZE == 0
        )

    def get_current_cell(self):
        """
        Get the current cell of the player based on its position.
        returns:
            tuple: A tuple containing the row index, column index,
            and the cell data of the player's current position.
        """
        row = self.y // config.CELL_SIZE
        col = self.x // config.CELL_SIZE
        return row, col, self.map[row][col]

    def can_move(self, direction: str) -> bool:
        """
        Check if the player can move in the specified direction.
        params:
            direction: The direction to check for movement.
        returns:
            bool: True if the player can move in the specified direction,
            otherwise False.
        """
        row, col, cell = self.get_current_cell()
        # print(cell.up, cell.right, cell.down, cell.left)
        if direction == config.UP:
            return row > 0 and not cell.up
        if direction == config.DOWN:
            return row < len(self.map) - 1 and not cell.down
        if direction == config.LEFT:
            return col > 0 and not cell.left
        if direction == config.RIGHT:
            return col < len(self.map[0]) - 1 and not cell.right
        return False

    def set_direction(self, direction: str) -> None:
        """
        Set the desired direction for the player to move.
        params:
            direction: The desired direction for the player to move.
        """
        self.desired_direction = direction

    def move(self) -> None:
        """
        Move the player based on its current direction and desired direction.
        The player will move in the desired direction if possible,
        otherwise it will continue moving in the current direction if possible.
        """
        if self.is_aligned():
            if (self.desired_direction is not None
                    and self.can_move(self.desired_direction)):
                self.direction = self.desired_direction
            elif (self.direction is not None
                    and not self.can_move(self.direction)):
                self.direction = None
        if self.direction is None:
            return
        if self.direction == config.UP:
            dist_to_center = self.y % config.CELL_SIZE
            if dist_to_center == 0:
                dist_to_center = config.CELL_SIZE
            self.y -= min(self.speed, dist_to_center)

        elif self.direction == config.DOWN:
            dist_to_center = config.CELL_SIZE - (self.y % config.CELL_SIZE)
            if self.y % config.CELL_SIZE == 0:
                dist_to_center = config.CELL_SIZE
            self.y += min(self.speed, dist_to_center)

        elif self.direction == config.LEFT:
            dist_to_center = self.x % config.CELL_SIZE
            if dist_to_center == 0:
                dist_to_center = config.CELL_SIZE
            self.x -= min(self.speed, dist_to_center)

        elif self.direction == config.RIGHT:
            dist_to_center = config.CELL_SIZE - (self.x % config.CELL_SIZE)
            if self.x % config.CELL_SIZE == 0:
                dist_to_center = config.CELL_SIZE
            self.x += min(self.speed, dist_to_center)

    def draw(
            self,
            screen: pygame.Surface,
            offset_x: int,
            offset_y: int
            ) -> None:
        """
        Draw the player on the given screen at its current position.
        params:
            screen: The pygame surface on which to draw the player.
            offset_x: The x-coordinate offset for drawing the player.
            offset_y: The y-coordinate offset for drawing the player.
        """
        center_x = offset_x + self.x + config.CELL_SIZE // 2
        center_y = offset_y + self.y + config.CELL_SIZE // 2

        sprite = self.sprite

        sprite_rect = sprite.get_rect(
            center=(center_x, center_y)
        )
        screen.blit(sprite, sprite_rect)

    def set_sprite(self, image_path: str) -> None:
        """
        Set the sprite for the player.
        params:
            image_path: The path to the image file for the player's sprite.
        """
        try:
            image = pygame.image.load(image_path).convert_alpha()

            size = config.BALL_SIZE * 2

            self.sprite = pygame.transform.smoothscale(
                image,
                (size, size)
            )

        except (pygame.error, OSError) as error:
            print(f"Could not load sprite: {error}")
            self.sprite = None
