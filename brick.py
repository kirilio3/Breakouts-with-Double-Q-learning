import pygame

# Brick class for each individual brick
class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.intact = True  # Flag to check if the brick is still there

    def draw(self, screen):
        if self.intact:
            pygame.draw.rect(screen, self.color, self.rect)