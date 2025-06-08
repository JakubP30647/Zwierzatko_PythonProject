import sys

import pygame

from settings import HEIGHT, WIDTH


def game_over_screen(screen, font):
    game_over_text = font.render("KONIEC GRY", True, (255, 0, 0))
    instruction_text = font.render("Kliknij, aby wrocic do menu", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (
        WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height()))
    screen.blit(instruction_text, (
        WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + instruction_text.get_height()))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
