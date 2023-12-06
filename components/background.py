import pygame
import math

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

class ScrollingBackground:
    def __init__(self, image_path, screen_width, screen_height, clock, position=(0, 0), scale=1):
        self.bg = pygame.image.load(image_path).convert()
        self.original_width = self.bg.get_width()
        self.original_height = self.bg.get_height()
        self.scroll = 0
        self.position = pygame.Vector2(position)
        self.scale = scale
        self.update_size()
        self.clock = clock
        
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.count = 0
        self.time_per_count = 200
        self.time_passed_to_count = 0

    def draw(self, screen):
        text = "Pontuação: " + str(self.count)
        SCORE_TEXT = get_font(24).render(text, True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, 54))
        screen.blit(SCORE_TEXT, SCORE_RECT)

    def update_size(self):
        self.bg = pygame.transform.scale(self.bg, (int(self.original_width * self.scale), int(self.original_height * self.scale)))
        self.bg_width = self.bg.get_width()
        self.bg_height = self.bg.get_height()

    def update(self, screen):
        for i in range(0, math.ceil(self.screen_width / self.bg_width) + 1):
            screen.blit(self.bg, (i * self.bg_width + self.scroll + self.position.x, self.position.y))

        self.scroll -= 1
        
        self.time_passed_to_count += self.clock.get_rawtime()

        if self.time_passed_to_count >= self.time_per_count:
            self.count += 1
            self.time_passed_to_count = 0

        if self.scroll <= -self.bg_width:
            self.scroll = 0

    def change_scale(self, new_scale):
        self.scale = new_scale
        self.update_size()