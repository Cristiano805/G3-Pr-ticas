import pygame

class Obstacle:
    def __init__(self, x, y, screen_width):
        super().__init__()
        self.width, self.height = 50, 50
        self.border = 2
        self.color = (255, 0, 0)

        self.x = x
        self.y = y
        self.screen_width = screen_width

        self.count = 0

        self.image = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.image, self.border)

    def update(self):
        if self.x > -self.width:
            self.x -= 2
        else:
            self.count += 1
            self.x = self.screen_width + self.width
        self.image = pygame.Rect(self.x, self.y, self.width, self.height)