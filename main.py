import pygame

from choice_screen import choice_screen
from settings import *
from mainMenu_screen import main_menu
from settings_screen import settings_screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    current_screen = "main_menu"

    while True:
        if current_screen == "main_menu":
            result = main_menu(screen)
        elif current_screen == "choice_screen":
            result = choice_screen(screen)
        elif current_screen == "settings":
            result = settings_screen(screen)
        elif current_screen == "quit":
            break


        current_screen = result

    pygame.quit()

if __name__ == "__main__":
    main()