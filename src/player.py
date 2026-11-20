import pygame


class Player():
    def __init__(self, row, col, map_data, color, config):
        self.config = config
        self.x = col * self.config.CELL_SIZE
        self.y = row * self.config.CELL_SIZE
        self.map = map_data
        self.GameEngine = None

        self.speed = self.config.PLAYER_SPEED
        self.direction = None
        self.desired_direction = None
        self.color = color

    def is_aligned(self):
        return (
            self.x % self.config.CELL_SIZE == 0
            and self.y % self.config.CELL_SIZE == 0
        )

    def get_current_cell(self):
        row = self.y // self.config.CELL_SIZE
        col = self.x // self.config.CELL_SIZE
        return row, col, self.map[row][col]

    def can_move(self, direction):
        row, col, cell = self.get_current_cell()
        # print(cell.up, cell.right, cell.down, cell.left)
        if direction == self.config.UP:
            return row > 0 and not cell.up
        if direction == self.config.DOWN:
            return row < len(self.map) - 1 and not cell.down
        if direction == self.config.LEFT:
            return col > 0 and not cell.left
        if direction == self.config.RIGHT:
            return col < len(self.map[0]) - 1 and not cell.right
        return False

    def set_direction(self, direction):
        self.desired_direction = direction

    def move(self):
        if self.is_aligned():
            if (self.desired_direction is not None
                    and self.can_move(self.desired_direction)):
                self.direction = self.desired_direction
            elif (self.direction is not None
                    and not self.can_move(self.direction)):
                self.direction = None
        if self.direction is None:
            return
        if self.direction == self.config.UP:
            dist_to_center = self.y % self.config.CELL_SIZE
            if dist_to_center == 0:
                dist_to_center = self.config.CELL_SIZE
            self.y -= min(self.speed, dist_to_center)

        elif self.direction == self.config.DOWN:
            dist_to_center = self.config.CELL_SIZE - (self.y % self.config.CELL_SIZE)
            if self.y % self.config.CELL_SIZE == 0:
                dist_to_center = self.config.CELL_SIZE
            self.y += min(self.speed, dist_to_center)

        elif self.direction == self.config.LEFT:
            dist_to_center = self.x % self.config.CELL_SIZE
            if dist_to_center == 0:
                dist_to_center = self.config.CELL_SIZE
            self.x -= min(self.speed, dist_to_center)

        elif self.direction == self.config.RIGHT:
            dist_to_center = self.config.CELL_SIZE - (self.x % self.config.CELL_SIZE)
            if self.x % self.config.CELL_SIZE == 0:
                dist_to_center = self.config.CELL_SIZE
            self.x += min(self.speed, dist_to_center)

    def draw(self, screen, offset_x, offset_y):
        center_x = offset_x + self.x + self.config.CELL_SIZE // 2
        center_y = offset_y + self.y + self.config.CELL_SIZE // 2

        sprite = self.sprite

        sprite_rect = sprite.get_rect(
            center=(center_x, center_y)
        )
        screen.blit(sprite, sprite_rect)

    def set_sprite(self, image_path):
        try:
            image = pygame.image.load(image_path).convert_alpha()

            size = self.config.BALL_SIZE * 2

            self.sprite = pygame.transform.smoothscale(
                image,
                (size, size)
            )

        except (pygame.error, OSError) as error:
            print(f"Could not load sprite: {error}")
            self.sprite = None
