import pygame

# Striker class
class Player:
    def __init__(self, posx, posy, width, height, speed, color, screen, WIDTH, font20):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.WIDTH = WIDTH
        self.height = height
        self.font = font20
        self.speed = speed
        self.color = color
        self.screen = screen
        self.geekRect = pygame.Rect(posx, posy, width, height)

    def display(self):
        pygame.draw.rect(self.screen, self.color, self.geekRect)
    
    def update(self, xFac):
        self.posx += self.speed * xFac
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= self.WIDTH:
            self.posx = self.WIDTH - self.width
        self.geekRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text_surface = self.font.render(text + str(score), True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)