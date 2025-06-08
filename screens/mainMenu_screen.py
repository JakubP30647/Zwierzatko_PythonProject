import pygame
import sys
from settings import *
from widgets import Button


def main_menu(screen):

    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.042))


    start_button = Button(0, 0, WIDTH * 0.208, HEIGHT * 0.083, "Start Game", font)
    start_button.center(offset_y=-HEIGHT * 0.093)  # -100 / 1080 ≈ -0.093

    settings_button = Button(0, 0, WIDTH * 0.208, HEIGHT * 0.083, "Settings", font)
    settings_button.center(offset_y=0)

    exit_button = Button(0, 0, WIDTH * 0.208, HEIGHT * 0.083, "EXIT", font)
    exit_button.center(offset_y=HEIGHT * 0.093)

    font_size = HEIGHT * 0.044  # 48 / 1080
    growing = True
    size_top = HEIGHT * 0.056   # 60 / 1080
    size_bottom = HEIGHT * 0.046  # 50 / 1080
    speed = 5.0

    fly_font = pygame.font.Font('assets/Minecraft.ttf', int(HEIGHT * 0.031))  # 33 / 1080
    fly_text = "try also s30580"
    fly_color = YELLOW
    fly_x = 0
    fly_y = HEIGHT * 0.18
    fly_speed = WIDTH * 0.182

    fly_direction = 1

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(PINK)

        dt1 = clock.tick(60) / 1000
        dt2 = clock.tick(60) / 300

        # pulsowania
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
        screen.blit(title, (
            screen.get_width() // 2 - title.get_width() // 2,
            HEIGHT * 0.1
        ))


        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)


        fly_surface = fly_font.render(fly_text, True, fly_color)
        screen.blit(fly_surface, (fly_x, fly_y))
        fly_x += fly_speed * fly_direction * dt1
        if fly_x <= 0:
            fly_x = 0
            fly_direction = 1
        elif fly_x + fly_surface.get_width() >= WIDTH:
            fly_x = WIDTH - fly_surface.get_width()
            fly_direction = -1

        # Obsługa zdarzeń
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
