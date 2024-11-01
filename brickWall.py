from brick import Brick

# BrickWall class to create a grid of bricks
class BrickWall:
    def __init__(self, rows, cols, brick_width, brick_height, padding, color):
        self.bricks = []
        self.rows = rows
        self.cols = cols
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.padding = padding
        self.color = color
        self.score = 0
        self.create_wall()

    def create_wall(self):
        for row in range(self.rows):
            brick_row = []
            for col in range(self.cols):
                x = col * (self.brick_width + self.padding)
                y = row * (self.brick_height + self.padding)
                brick = Brick(x, y, self.brick_width, self.brick_height, self.color)
                brick_row.append(brick)
            self.bricks.append(brick_row)

    def draw(self, screen):
        for row in self.bricks:
            for brick in row:
                brick.draw(screen)

    def check_collision(self, ball_rect):
        # Detect collision with the ball and remove hit bricks
        for row in self.bricks:
            for brick in row:
                if brick.intact and brick.rect.colliderect(ball_rect):
                    brick.intact = False    # "Break" the brick
                    self.score += 1         # Increase score for each hit brick
                    return True             # Collision occurred
        return False

    def all_bricks_destroyed(self):
        return all(not brick.intact for row in self.bricks for brick in row)