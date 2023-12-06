import pygame
import random

class Obstacle:
    def __init__(self, x, y, screen_width, speed):
        super().__init__()
        self.width, self.height = 50, 50
        self.border = 2
        self.color = (255, 0, 0)

        self.x = x
        self.y = y
        self.screen_width = screen_width

        self.speed = speed

        self.image = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.image, self.border)

    def update(self):
        if self.x > -self.width:
            self.x -= self.speed
        else:
            self.x = self.screen_width + random.randint(0, 200)
        self.image = pygame.Rect(self.x, self.y, self.width, self.height)