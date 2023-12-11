import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, speed, image_path):
        super().__init__()

        self.screen_width = screen_width
        self.speed = speed

        self.sheet = pygame.image.load(image_path)
        self.width, self.height = 23, 24  # Ajuste a largura e altura conforme necessário
        sheet_width, sheet_height = self.sheet.get_size()

        # Certifique-se de que a largura da imagem é maior ou igual à largura do frame
        if sheet_width < self.width:
            raise ValueError("A largura da imagem é menor que a largura do frame.")

        num_frames = sheet_width // self.width

        # Lógica adicional para evitar o erro subsurface
        if num_frames <= 0:
            raise ValueError("Número de frames deve ser maior que zero.")

        # Ajuste para começar do início após 23 pixels
        self.frames = [self.sheet.subsurface((i * self.width % sheet_width, 0, self.width, self.height)) for i in range(num_frames)]
        self.frame_index = 0

        self.image = pygame.transform.scale(self.frames[self.frame_index], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.reset_obstacle()

    def reset_obstacle(self):
        self.rect.x = self.screen_width + random.randint(0, 200)

    def draw(self, screen, scale=1.0):
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)
        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        screen.blit(scaled_image, self.rect.topleft)

    def animate(self, clock):
        time_passed_to_update = clock.get_rawtime()
        time_per_frame = 20  # Ajuste este valor para controlar a velocidade da animação

        if time_passed_to_update > time_per_frame:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.frame_index], (self.width, self.height))
            clock.tick()  # Reset do relógio