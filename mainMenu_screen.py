import pygame
import sys
from settings import *
from button import Button, Slider


def main_menu(screen):
    font = pygame.font.Font('assets/milk.ttf', 45)

    start_button = Button(0, 0, 400, 90, "Start Game", font)
    start_button.center(offset_y=-100)

    settings_button = Button(0, 0, 400, 90, "Settings", font)
    settings_button.center(offset_y=0)

    exit_button = Button(0, 0, 400, 90, "EXIT", font)
    exit_button.center(offset_y=100)

    font_size = 48
    growing = True
    size_top = 60
    size_bottom = 50
    speed = 5.0

    fly_font = pygame.font.Font('assets/Minecraft.ttf', 33)
    fly_text = "try also s30580"
    fly_color = YELLOW
    fly_x = 0
    fly_y = HEIGHT - 0.82 * HEIGHT
    fly_speed = 350
    fly_direction = 1

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(PINK)
        dt1 = clock.tick(60) / 1000
        dt2 = clock.tick(60) / 300

        # Pulsing title effect
        if growing:
            font_size += speed * dt2
            if font_size >= size_top:
                font_size = size_top
                growing = False
        else:
            font_size -= speed * dt2
            if font_size <= size_bottom:
                font_size = size_bottom
                growing = True

        title_font = pygame.font.Font('assets/milk.ttf', int(font_size))
        title = title_font.render("Zwierze wonderful LIFE", True, BLACK)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, (HEIGHT - 0.9 * HEIGHT)))

        # Draw buttons
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        # Animate flying text
        fly_surface = fly_font.render(fly_text, True, fly_color)
        screen.blit(fly_surface, (fly_x, fly_y))
        fly_x += fly_speed * fly_direction * dt1
        if fly_x <= 0:
            fly_x = 0
            fly_direction = 1
        elif fly_x + fly_surface.get_width() >= WIDTH:
            fly_x = WIDTH - fly_surface.get_width()
            fly_direction = -1

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    print("Start Game")
                    return "choice_screen"
                elif settings_button.is_clicked(event.pos):
                    print("Settings")
                    return "settings"
                elif exit_button.is_clicked(event.pos):
                    running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()
