import pygame

pygame.display.set_caption("G3")

width = 1280     # Largura Janela
height = 720  # Altura Janela

def load():
    global clock
    clock = pygame.time.Clock()

def update(dt):
    pass

def draw_screen(screen):
    pass

def main_loop(screen):
    global clock, selected_option, show_texts

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:  # fechamento do prog
                running = False
                break

        clock.tick(60)
        draw_screen(screen)
        pygame.display.update()

# Programa principal
pygame.init()
screen = pygame.display.set_mode((width, height))
load()
main_loop(screen)
pygame.quit()