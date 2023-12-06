import pygame
import sys
from random import choice

from components import background, button, character, obstacle

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND = SCREEN_HEIGHT - 80
pygame.display.set_caption("Dino Adventures")
FILENAME = 'scoreboard.txt'
difficulty = [1, 2, 4]
difficulty_index = 0

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    global clock
    clock = pygame.time.Clock()

    hero_mode = False

    player = character.Player(SCREEN_WIDTH - 800, GROUND, clock, SCREEN_WIDTH, scale=4)

    speed = difficulty[difficulty_index]
    
    # obstaculos terrestres
    obstacle1 = obstacle.Obstacle(SCREEN_WIDTH - 400, GROUND, SCREEN_WIDTH, speed)
    obstacle2 = obstacle.Obstacle(SCREEN_WIDTH, GROUND, SCREEN_WIDTH, speed)
    obstacle3 = obstacle.Obstacle(SCREEN_WIDTH + 400, GROUND, SCREEN_WIDTH, speed)
    
    # obstaculo aereo
    obstacle4 = obstacle.Obstacle(SCREEN_WIDTH + 800, GROUND - 280, SCREEN_WIDTH, speed)

    scrolling_bg = background.ScrollingBackground("assets/bg.jpg", SCREEN_WIDTH, SCREEN_HEIGHT, clock, position=(0, 100))

    scrolling_bg.change_scale(2.0)

    while True:
        SCREEN.fill("black")

        scrolling_bg.update(SCREEN)
        obstacle1.update()
        obstacle2.update()
        obstacle3.update()
        obstacle4.update()
        player.update()

        SCREEN.blit(player.image, player.rect.topleft)

        scrolling_bg.draw(SCREEN)
        player.draw(SCREEN)
        obstacle1.draw(SCREEN)
        obstacle2.draw(SCREEN)
        obstacle3.draw(SCREEN)
        obstacle4.draw(SCREEN)

        list_of_obstacles = [obstacle1.image, obstacle2.image, obstacle3.image, obstacle4.image]
        colision = player.hitbox_rect.collidelist(list_of_obstacles)

        if player.hitbox != None and colision != -1 and not hero_mode:
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
                elif event.key == pygame.K_h:
                    hero_mode = not hero_mode
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.is_walking = False
                    if event.key == pygame.K_LEFT:
                        player.direction = "left"

        pygame.display.update()

def options():
    global difficulty_index
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(45).render("Tela de configurações", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        BUTTON_WIDTH, BUTTON_HEIGHT = 1000, 109

        OPTIONS_BUTTON_IMAGE = pygame.image.load("assets/Options Rect.png")
        OPTIONS_BUTTON_IMAGE = pygame.transform.scale(OPTIONS_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))


        EASY_DIFICULTY_BUTTON = button.Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 150),
                            text_input="FÁCIL", font=get_font(40), base_color="#d7fcd4", hovering_color="Green",
                            selected_color="Green")
        NORMAL_DIFICULTY_BUTTON = button.Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 300),
                                    text_input="NORMAL", font=get_font(40), base_color="#d7fcd4", hovering_color="Green",
                                    selected_color="Green")
        HARD_DIFICULTY_BUTTON = button.Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 450),
                                    text_input="DIFÍCIL", font=get_font(40), base_color="#d7fcd4", hovering_color="Green",
                                    selected_color="Green")

        OPTIONS_BACK = button.Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 600),
                            text_input="Voltar", font=get_font(40), base_color="White", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        
        EASY_DIFICULTY_BUTTON.changeColor(OPTIONS_MOUSE_POS, difficulty_index == 0)
        EASY_DIFICULTY_BUTTON.update(SCREEN)
        
        NORMAL_DIFICULTY_BUTTON.changeColor(OPTIONS_MOUSE_POS, difficulty_index == 1)
        NORMAL_DIFICULTY_BUTTON.update(SCREEN)
        
        HARD_DIFICULTY_BUTTON.changeColor(OPTIONS_MOUSE_POS, difficulty_index == 2)
        HARD_DIFICULTY_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return "menu"
                elif EASY_DIFICULTY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    difficulty_index = 0
                elif NORMAL_DIFICULTY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    difficulty_index = 1
                elif HARD_DIFICULTY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    difficulty_index = 2

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
        PLAY_BUTTON = button.Button(image=PLAY_BUTTON_IMAGE, pos=(640, 250),
                            text_input="JOGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        OPTIONS_BUTTON_IMAGE = pygame.image.load("assets/Options Rect.png")
        OPTIONS_BUTTON_IMAGE = pygame.transform.scale(OPTIONS_BUTTON_IMAGE, (1000, 109))
        OPTIONS_BUTTON = button.Button(image=OPTIONS_BUTTON_IMAGE, pos=(640, 400),
                            text_input="CONFIGURAÇÕES", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        QUIT_BUTTON_IMAGE = pygame.image.load("assets/Quit Rect.png")
        QUIT_BUTTON_IMAGE = pygame.transform.scale(QUIT_BUTTON_IMAGE, (1000, 109))
        QUIT_BUTTON = button.Button(image=QUIT_BUTTON_IMAGE, pos=(640, 550),
                            text_input="SAIR", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for btn in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            btn.changeColor(MENU_MOUSE_POS)
            btn.update(SCREEN)

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
    scores = []

    # Abre o arquivo no modo de leitura ('r' para ler)
    with open(FILENAME, 'r') as file:
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

    with open(FILENAME, 'w') as file:
        # Escreve a string desejada seguida de uma quebra de linha
        for elem in sorted_scores:
            file.write(str(elem) + '\n')

if __name__ == "__main__":
    main_menu()
