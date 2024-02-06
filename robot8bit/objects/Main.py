import sys

import pygame

from Button import Button
from Game import Game

game = Game()
screen = pygame.display.set_mode((1280, 720))

background = pygame.image.load("../assets/menu_background.png")


def get_font(size):
    return pygame.font.Font("../assets/font.ttf", size)


class Main:
    while True:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MENÚ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        boton_jugar = Button(image=pygame.image.load("../assets/option.png"), pos=(640, 300),
                             text_input="JUGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        boton_salir = Button(image=pygame.image.load("../assets/option.png"), pos=(640, 450),
                             text_input="SALIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [boton_jugar, boton_salir]:
            button.changue_color(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.check_for_input(MENU_MOUSE_POS):
                    game.run()
                if boton_salir.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
