import pygame

import utils
from PetsAndUtilities.PetEntity import PetEntity
from settings import *
from widgets import Button

def choice_screen(screen):

    font_size = int(HEIGHT * 0.037)
    font = pygame.font.Font('assets/milk.ttf', font_size)

    buttons = []
    labels = ["Rabbit", "HEADGEHOG", "beer", "zwierz"]

    for i, label in enumerate(labels):

        btn = Button(
            WIDTH * 0.5 - WIDTH * 0.07,                 # środek ekranu - offset
            HEIGHT * 0.2 + i * (HEIGHT * 0.139),
            WIDTH * 0.182,
            HEIGHT * 0.074,
            label,
            font
        )
        buttons.append(btn)

    back_button = Button(
        WIDTH * 0.5 - WIDTH * 0.07,
        HEIGHT * 0.9,
        WIDTH * 0.182,
        HEIGHT * 0.074,
        "BACK",
        font
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(PINK)


        title_font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.046))
        title = title_font.render("Wybierz:", True, BLACK)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, HEIGHT * 0.028))

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

                        match(btn.text):

                            case "Rabbit":
                                utils.set_pet_data("rabbit", 7)
                                print("CHANGE")
                            case "HEADGEHOG":
                                utils.set_pet_data("hedgehog", 5)
                                print("CHANGE HEADGEHOG")
                            case "beer":
                                utils.set_pet_data("beer", 3)
                                print("CHANGE SARENKA")


                        return "gameplay_screen"

        pygame.display.flip()
        clock.tick(60)
