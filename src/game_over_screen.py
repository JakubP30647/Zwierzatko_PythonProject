import sys

import pygame

from settings import HEIGHT, WIDTH


def game_over_screen(screen, font):
    """Wyświetla ekran "Koniec Gry" i czeka na interakcję użytkownika, aby powrócić do menu.

    Ten ekran jest prezentowany użytkownikowi po zakończeniu gry.
    Zawiera wyraźny komunikat o końcu gry oraz instrukcję, jak powrócić do głównego menu,
    zwiększając tym samym użyteczność aplikacji. Funkcja blokuje wykonywanie programu
    aż do momentu, gdy użytkownik kliknie myszką lub zamknie okno gry.
    Obsługuje również standardowe zdarzenie zamknięcia okna PyGame (przycisk 'X').

    :param screen: Obiekt powierzchni PyGame (pygame.Surface), na którym ma być wyświetlany ekran.
                   Jest to główna powierzchnia rysowania gry, na której renderowane są wszystkie elementy
                   graficzne, takie jak tło i tekst. Musi być to zainicjalizowana powierzchnia
                   PyGame, zazwyczaj tworzona za pomocą `pygame.display.set_mode()`.
    :type screen: pygame.Surface
    :param font: Obiekt czcionki PyGame (pygame.font.Font) używany do renderowania tekstu
                 "KONIEC GRY" oraz "Kliknij, aby wrocic do menu".
                 Czcionka musi być wstępnie załadowana i zainicjalizowana (np. `pygame.font.Font(None, 74)`
                 lub `pygame.font.SysFont('Arial', 50)`), aby umożliwić wyświetlanie tekstu
                 w określonym stylu i rozmiarze.
    :type font: pygame.font.Font
    """
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