import pygame
from settings import *
from button import Button

import pygame_widgets
from pygame_widgets.slider import Slider


def settings_screen(screen):
    font = pygame.font.Font('assets/milk.ttf', 45)
    back_button = Button(0, 0, 250, 60, "Back", font)
    back_button.center(offset_y=200)

    offset_x_FOOD = int(-1 * 0.12 * WIDTH)
    offset_y_FOOD = int(-1 * 0.22 * HEIGHT)
    slider_Food = Slider(screen, WIDTH // 2 + offset_x_FOOD, HEIGHT // 2 + offset_y_FOOD, int(WIDTH * 0.234375), int(HEIGHT * 0.0173), min=0,
                    max=100, step=1)

    offset_x_FUN = int(-1 * 0.12 * WIDTH)
    offset_y_FUN = int(-1 * 0.08 * HEIGHT)
    slider_Fun = Slider(screen, WIDTH // 2 + offset_x_FUN, HEIGHT // 2 + offset_y_FUN, int(WIDTH * 0.234375), int(HEIGHT * 0.0173),
                    min=0,
                    max=100, step=1)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return "main_menu"

        screen.fill(PINK)

        title = font.render("Settings", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        # print(slider.getValue())

        food_text = font.render(f"Food: {slider_Food.getValue()}", True, BLACK)
        screen.blit(food_text, (WIDTH // 2 - food_text.get_width() // 2, int(HEIGHT * 0.228)))

        fun_text = font.render(f"Fun: {slider_Fun.getValue()}", True, BLACK)
        screen.blit(fun_text, (WIDTH // 2 - fun_text.get_width() // 2, int(HEIGHT * 0.37)))


        back_button.draw(screen)

        pygame_widgets.update(events)
        pygame.display.update()
