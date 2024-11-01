import pygame

class Ball:
    def __init__(self, posx, posy, radius, speed, color, screen, WIDTH, HEIGHT):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        # Set fixed initial direction (for example, moving up-right)
        self.xFac = 1  # Move right
        self.yFac = -1  # Move up

    def display(self):
        pygame.draw.circle(self.screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac
        # Screen boundary collision checks
        if self.posx <= 0 or self.posx >= self.WIDTH:
            self.xFac *= -1    
        if self.posy <= 0:
            self.yFac *= -1
        elif self.posy > self.HEIGHT - self.radius:  # Signal game over if the ball goes below the screen
            return -1

        return 0

    def reset(self):
        self.posx = self.WIDTH // 2
        self.posy = self.HEIGHT // 2
        # Reset the direction to fixed values upon reset
        self.xFac = 1  # Move right
        self.yFac = -1  # Move up

    def hit(self):
        # Reverse vertical direction
        self.yFac *= -1
        # Only move the ball up slightly if it’s not near the top edge
        if self.posy - self.radius > 0:     # Ensure the ball won't go off the top screen
            self.posy -= self.radius
        else:
            self.posy = self.radius         # Keep it within the top boundary

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)
