import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, clock, scale=5):
        super().__init__()
        self.sheet_stop = pygame.image.load("assets/Dino_Stop.png")
        self.sheet_walk = pygame.image.load("assets/Dino_Walking.png")
        self.width, self.height = 24, 24
        sheet_width_stop, sheet_height_stop = self.sheet_stop.get_size()
        sheet_width_walk, sheet_height_walk = self.sheet_walk.get_size()
        num_frames_stop = sheet_width_stop // self.width
        num_frames_walk = sheet_width_walk // self.width

        self.clock = clock
        self.ground = y

        self.x = x
        self.y = y

        self.frames_stop = [self.sheet_stop.subsurface((i * self.width, 0, self.width, self.height)) for i in range(num_frames_stop)]
        self.frame_index_stop = 0

        self.frames_walk_right = [self.sheet_walk.subsurface((i * self.width, 0, self.width, self.height)) for i in range(num_frames_walk)]
        self.frame_index_walk_right = 0

        self.frames_walk_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_walk_right]
        self.frame_index_walk_left = 0

        self.time_passed_to_update = 0
        self.time_passed_to_draw = 0
        self.time_per_frame = 60
        self.scale = scale

        self.time_jump_passed = 0
        self.time_last_jump = 0
        self.time_per_jump = 1000

        self.image = pygame.transform.scale(self.frames_stop[self.frame_index_stop], (int(self.width * self.scale), int(self.height * self.scale)))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.is_walking = False
        self.is_jumping = False
        self.direction = "right"

        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.hitbox_rect = None

    def draw(self, screen):
        self.time_passed_to_draw += self.clock.get_rawtime()

        if self.time_passed_to_draw >= self.time_per_frame:
            if self.is_walking:
                if self.direction == "right":
                    self.frame_index_walk_right = (self.frame_index_walk_right + 1) % len(self.frames_walk_right)
                    self.image = self.frames_walk_right[self.frame_index_walk_right].copy()
                elif self.direction == "left":
                    self.frame_index_walk_left = (self.frame_index_walk_left + 1) % len(self.frames_walk_left)
                    self.image = self.frames_walk_left[self.frame_index_walk_left].copy()
            self.time_passed_to_draw = 0

        self.image = pygame.transform.scale(self.image, (int(self.width * self.scale), int(self.height * self.scale)))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.hitbox = (self.x - self.width - 10, self.y - self.height - 10, self.width * 3, self.height * 3)
        self.hitbox_rect = pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

    def update(self):
        self.time_passed_to_update += self.clock.get_rawtime()
        self.clock.tick()

        if self.time_passed_to_update >= self.time_per_frame:
            if self.is_walking:
                if self.direction == "right":
                    self.x = self.x + 12
                elif self.direction == "left":
                    self.x = self.x - 12
            self.time_passed_to_update = 0
        
        if self.is_jumping:
            self.time_jump_passed += self.clock.get_rawtime()

            if self.time_jump_passed <= self.time_per_jump / 2:
                self.y = self.y - 4
            elif self.time_jump_passed > self.time_per_jump / 2 and self.time_jump_passed <= self.time_per_jump:
                self.y = self.y + 4
            else:
                self.time_jump_passed = 0
                self.y = self.ground
                self.is_jumping = False
