import pygame
from settings import *
from button import Button


def choice_screen(screen):
    font = pygame.font.Font('assets/milk.ttf', 40)
    buttons = []
    labels = ["Zwierze", "ZWIERZYNIEC", "ZwIeRzYsKo", "zwierz"]

    for i, label in enumerate(labels):
        btn = Button(WIDTH // 2 - int(WIDTH * 0.07), (HEIGHT * 0.2) + i * 150, 350, 80, label, font)
        buttons.append(btn)



    back_button = Button(WIDTH // 2 - int(WIDTH * 0.07), HEIGHT*0.9, 350, 80, "BACK", font)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(PINK)

        title_font = pygame.font.Font('assets/milk.ttf', 50)
        title = title_font.render("Wybierz:", True, BLACK)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))

        for btn in buttons:
            btn.draw(screen)

        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "main_menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if back_button.is_clicked(event.pos):
                    return "main_menu"

                for i, btn in enumerate(buttons):
                    if btn.is_clicked(event.pos):
                        return "main_menu"

        pygame.display.flip()
        clock.tick(60)
