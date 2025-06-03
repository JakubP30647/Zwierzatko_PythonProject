import sys

import utils
from settings import *
from utils import FUN
from widgets import *

def gameplay_screen(screen):

    font = pygame.font.Font('assets/milk.ttf', 40)


    back_button = Button(WIDTH // 2 - int(WIDTH * 0.07), HEIGHT * 0.9, 350, 80, "BACK", font)


    FunBar = Bar(WIDTH * 0.005, HEIGHT * 0.02, WIDTH * 0.15, HEIGHT * 0.05, 100)
    FunBar.ratio = utils.FUN
    FunBar.color1 = GRAY
    FunBar.color2 = GREEN


    FoodBar = Bar(WIDTH * 0.005, HEIGHT * 0.10, WIDTH * 0.15, HEIGHT * 0.05, 100)
    FoodBar.ratio = utils.FOOD
    FoodBar.color1 = GRAY
    FoodBar.color2 = BLUE

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    last_drop_time_fun = 0
    last_drop_time_food = 0

    clock = pygame.time.Clock()

    running = True
    while running:


        screen.blit(background, (0, 0))

        clock.tick(60)

        currentTime = pygame.time.get_ticks()


        if currentTime - last_drop_time_fun > 1000:
            FunBar.ratio -= 1

            last_drop_time_fun = currentTime


        if currentTime - last_drop_time_food > 750:
            FoodBar.ratio -= 1

            last_drop_time_food = currentTime


        FunBar.draw(screen)
        FoodBar.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return "main_menu"

        pygame.display.flip()

    pygame.quit()
    sys.exit()