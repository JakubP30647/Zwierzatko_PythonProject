import pygame
import sys
from settings import *
from widgets import Button


def main_menu(screen):
    """Wyświetla ekran menu głównego gry, umożliwiając nawigację do innych sekcji.

    Funkcja inicjalizuje i renderuje elementy interfejsu użytkownika, takie jak tytuł gry,
    przyciski "Start Game", "Settings" i "EXIT". Zarządza również prostą animacją
    pulsowania tytułu oraz ruchomym tekstem informacyjnym. Reaguje na interakcje
    użytkownika (kliknięcia myszą) i odpowiednio zmienia stan gry.

    :param screen: Obiekt powierzchni PyGame (pygame.Surface), na której ma być wyświetlane menu.
                   Jest to główna powierzchnia okna gry, na której rysowane są wszystkie elementy
                   wizualne menu głównego.
    :type screen: pygame.Surface

    :returns: Ciąg znaków określający następny ekran gry po wyjściu z menu ("choice_screen"
              dla rozpoczęcia nowej gry, "settings" dla przejścia do ustawień,
              lub "quit" do zakończenia aplikacji).
    :rtype: str
    """
    # Inicjalizacja czcionki dla przycisków
    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.042))

    # Inicjalizacja przycisków menu głównego
    start_button = Button(0, 0, WIDTH * 0.208, HEIGHT * 0.083, "Start Game", font)
    start_button.center(offset_y=-HEIGHT * 0.093)  # Pozycja wyśrodkowana z przesunięciem w górę

    settings_button = Button(0, 0, WIDTH * 0.208, HEIGHT * 0.083, "Settings", font)
    settings_button.center(offset_y=0) # Pozycja wyśrodkowana

    exit_button = Button(0, 0, WIDTH * 0.208, HEIGHT * 0.083, "EXIT", font)
    exit_button.center(offset_y=HEIGHT * 0.093) # Pozycja wyśrodkowana z przesunięciem w dół

    # Zmienne dla animacji pulsowania tytułu
    font_size = HEIGHT * 0.044
    growing = True
    size_top = HEIGHT * 0.056
    size_bottom = HEIGHT * 0.046
    speed = 5.0

    # Zmienne dla ruchomego tekstu informacyjnego
    fly_font = pygame.font.Font('assets/Minecraft.ttf', int(HEIGHT * 0.031))
    fly_text = "try also s30580"
    fly_color = YELLOW
    fly_x = 0
    fly_y = HEIGHT * 0.18
    fly_speed = WIDTH * 0.182
    fly_direction = 1 # Kierunek ruchu tekstu (1 dla prawo, -1 dla lewo)

    clock = pygame.time.Clock() # Obiekt zegara PyGame do kontroli FPS i czasu
    running = True # Flaga kontrolująca główną pętlę menu

    while running:
        screen.fill(PINK) # Wypełnienie ekranu różowym kolorem tła

        # Obliczanie delta time dla płynnej animacji
        dt1 = clock.tick(60) / 1000 # Delta time w sekundach dla animacji tekstu latającego
        dt2 = clock.tick(60) / 300  # Delta time w sekundach dla animacji pulsowania tytułu

        # Logika animacji pulsowania tytułu
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

        # Renderowanie i wyświetlanie tytułu
        title_font = pygame.font.Font('assets/milk.ttf', int(font_size))
        title = title_font.render("Zwierze wonderful LIFE", True, BLACK)
        screen.blit(title, (
            screen.get_width() // 2 - title.get_width() // 2,
            HEIGHT * 0.1
        ))

        # Rysowanie przycisków
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        # Renderowanie i animacja ruchomego tekstu
        fly_surface = fly_font.render(fly_text, True, fly_color)
        screen.blit(fly_surface, (fly_x, fly_y))
        fly_x += fly_speed * fly_direction * dt1 # Aktualizacja pozycji tekstu
        # Obsługa odbijania się tekstu od krawędzi ekranu
        if fly_x <= 0:
            fly_x = 0
            fly_direction = 1
        elif fly_x + fly_surface.get_width() >= WIDTH:
            fly_x = WIDTH - fly_surface.get_width()
            fly_direction = -1

        # Obsługa zdarzeń PyGame
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Zamknięcie okna gry
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # Kliknięcie myszy
                if start_button.is_clicked(event.pos):
                    print("Start Game")
                    return "choice_screen" # Zwraca "choice_screen" aby przejść do ekranu wyboru
                elif settings_button.is_clicked(event.pos):
                    print("Settings")
                    return "settings" # Zwraca "settings" aby przejść do ekranu ustawień
                elif exit_button.is_clicked(event.pos):
                    running = False # Ustawia flagę running na False, aby wyjść z pętli

        pygame.display.flip() # Odświeżenie ekranu

    pygame.quit() # Deinicjalizacja PyGame
    sys.exit() # Zakończenie aplikacji