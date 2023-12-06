import pygame
from button import Button
import sys
import math
from random import choice

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND = SCREEN_HEIGHT - 80
pygame.display.set_caption("Dino Adventures")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

class ScrollingBackground:
    def __init__(self, image_path, screen_width, screen_height, position=(0, 0), scale=1):
        self.bg = pygame.image.load(image_path).convert()
        self.original_width = self.bg.get_width()
        self.original_height = self.bg.get_height()
        self.scroll = 0
        self.position = pygame.Vector2(position)
        self.scale = scale
        self.update_size()

        self.count = 0
        self.time_per_count = 200
        self.time_passed_to_count = 0

    def draw(self, screen):
        text = "Pontuação: " + str(self.count)
        SCORE_TEXT = get_font(20).render(text, True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, 160))
        screen.blit(SCORE_TEXT, SCORE_RECT)

    def update_size(self):
        self.bg = pygame.transform.scale(self.bg, (int(self.original_width * self.scale), int(self.original_height * self.scale)))
        self.bg_width = self.bg.get_width()
        self.bg_height = self.bg.get_height()

    def update(self, screen):
        for i in range(0, math.ceil(SCREEN_WIDTH / self.bg_width) + 1):
            screen.blit(self.bg, (i * self.bg_width + self.scroll + self.position.x, self.position.y))

        self.scroll -= 1
        
        self.time_passed_to_count += clock.get_rawtime()

        if self.time_passed_to_count >= self.time_per_count:
            self.count += 1
            self.time_passed_to_count = 0

        if self.scroll <= -self.bg_width:
            self.scroll = 0

    def change_scale(self, new_scale):
        self.scale = new_scale
        self.update_size()

class Obstacle:
    def __init__(self, x, y):
        super().__init__()
        self.width, self.height = 50, 50
        self.border = 2
        self.color = (255, 0, 0)

        self.x = x
        self.y = y

        self.count = 0

        self.image = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.image, self.border)

    def update(self):
        if self.x > -self.width:
            self.x -= 2
        else:
            self.count += 1
            self.x = SCREEN_WIDTH + self.width
        self.image = pygame.Rect(self.x, self.y, self.width, self.height)



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=5):
        super().__init__()
        self.sheet_stop = pygame.image.load("assets/Dino_Stop.png")
        self.sheet_walk = pygame.image.load("assets/Dino_Walking.png")
        self.width, self.height = 24, 24
        sheet_width_stop, sheet_height_stop = self.sheet_stop.get_size()
        sheet_width_walk, sheet_height_walk = self.sheet_walk.get_size()
        num_frames_stop = sheet_width_stop // self.width
        num_frames_walk = sheet_width_walk // self.width

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
        self.time_passed_to_draw += clock.get_rawtime()

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
        self.time_passed_to_update += clock.get_rawtime()
        clock.tick()

        if self.time_passed_to_update >= self.time_per_frame:
            if self.is_walking:
                if self.direction == "right":
                    self.x = self.x + 12
                elif self.direction == "left":
                    self.x = self.x - 12
            self.time_passed_to_update = 0
        
        if self.is_jumping:
            self.time_jump_passed += clock.get_rawtime()

            if self.time_jump_passed <= self.time_per_jump / 2:
                self.y = self.y - 4
            elif self.time_jump_passed > self.time_per_jump / 2 and self.time_jump_passed <= self.time_per_jump:
                self.y = self.y + 4
            else:
                self.time_jump_passed = 0
                self.y = GROUND
                self.is_jumping = False

        

def play():
    global clock
    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH - 800, GROUND, scale=4)
    obstacle1 = Obstacle(SCREEN_WIDTH - 400, GROUND)
    obstacle2 = Obstacle(SCREEN_WIDTH, GROUND)
    obstacle3 = Obstacle(SCREEN_WIDTH + 400, GROUND)

    scrolling_bg = ScrollingBackground("assets/bg.jpg", SCREEN_WIDTH, SCREEN_HEIGHT, position=(0, 100))

    scrolling_bg.change_scale(2.0)

    while True:
        SCREEN.fill("black")

        scrolling_bg.update(SCREEN)
        obstacle1.update()
        obstacle2.update()
        obstacle3.update()
        player.update()

        SCREEN.blit(player.image, player.rect.topleft)

        scrolling_bg.draw(SCREEN)
        player.draw(SCREEN)
        obstacle1.draw(SCREEN)
        obstacle2.draw(SCREEN)
        obstacle3.draw(SCREEN)

        list_of_obstacles = [obstacle1.image, obstacle2.image, obstacle3.image]
        colision = player.hitbox_rect.collidelist(list_of_obstacles)

        if player.hitbox != None and colision != -1:
            total_score = scrolling_bg.count
            save(total_score) # salva pontuação no arquivo txt
            print("Total score: " + str(total_score))
            return "menu"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_LEFT:
                    player.is_walking = True
                    player.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    player.is_walking = True
                    player.direction = "right"
                elif event.key == pygame.K_UP:
                    player.is_jumping = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.is_walking = False
                    if event.key == pygame.K_LEFT:
                        player.direction = "left"

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(45).render("Tela de configurações", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        BUTTON_WIDTH, BUTTON_HEIGHT = 1000, 109

        OPTIONS_BUTTON_IMAGE = pygame.image.load("assets/Options Rect.png")
        OPTIONS_BUTTON_IMAGE = pygame.transform.scale(OPTIONS_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))

        OPTIONS_BACK = Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 460), 
                            text_input="Voltar", font=get_font(75), base_color="White", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return "menu"

        pygame.display.update()

def main_menu():
    background_menu_image = pygame.image.load("assets/background_menu.png").convert()

    while True:
        SCREEN.blit(background_menu_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("Dino Adventures", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON_IMAGE = pygame.image.load("assets/Play Rect.png")
        PLAY_BUTTON_IMAGE = pygame.transform.scale(PLAY_BUTTON_IMAGE, (1000, 109))
        PLAY_BUTTON = Button(image=PLAY_BUTTON_IMAGE, pos=(640, 250),
                            text_input="JOGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        OPTIONS_BUTTON_IMAGE = pygame.image.load("assets/Options Rect.png")
        OPTIONS_BUTTON_IMAGE = pygame.transform.scale(OPTIONS_BUTTON_IMAGE, (1000, 109))
        OPTIONS_BUTTON = Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 400),
                            text_input="CONFIGURAÇÕES", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        QUIT_BUTTON_IMAGE = pygame.image.load("assets/Quit Rect.png")
        QUIT_BUTTON_IMAGE = pygame.transform.scale(QUIT_BUTTON_IMAGE, (1000, 109))
        QUIT_BUTTON = Button(image=QUIT_BUTTON_IMAGE, pos=(640, 550),
                            text_input="SAIR", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    result = play()
                    if result == "menu":
                        continue
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    result = options()
                    if result == "menu":
                        continue
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def save(score):
    filename = 'scoreboard.txt'
    scores = []

    # Abre o arquivo no modo de leitura ('r' para ler)
    with open(filename, 'r') as file:
        # Lê cada linha do arquivo
        lines = file.readlines()

        for line in lines:
            saved_score = int(line.strip())  # O método strip remove espaços em branco, quebras de linha, etc.
            scores.append(saved_score)
        
    scores.append(score)
    # Cria uma nova lista ordenada do maior para o menor usando a função sorted()
    sorted_scores = sorted(scores, reverse=True)

    if len(sorted_scores) > 10:
        sorted_scores.pop()

    with open(filename, 'w') as file:
        # Escreve a string desejada seguida de uma quebra de linha
        for elem in sorted_scores:
            file.write(str(elem) + '\n')

if __name__ == "__main__":
    main_menu()
