"""
settings_screen.py - Moduł odpowiedzialny za ekran ustawień w grze "ZWIERZE".

Ten moduł definiuje funkcję `settings_screen`, która renderuje interfejs
użytkownika dla zarządzania globalnymi ustawieniami gry. Umożliwia użytkownikowi
modyfikowanie kluczowych parametrów, takich jak poziom głodu i zabawy
(reprezentowanych przez suwaki), które bezpośrednio wpływają na rozgrywkę.

Ekran ustawień zapewnia intuicyjny sposób konfiguracji gry, a także pozwala
na powrót do głównego menu. Wykorzystuje bibliotekę `pygame_widgets`
do interaktywnych elementów GUI.
"""

import pygame
import utils # Moduł zawierający globalne zmienne pomocnicze, np. dla ustawień gry
from settings import * # Importuje wszystkie stałe globalne, takie jak WIDTH, HEIGHT, kolory
from widgets import Button # Klasa do tworzenia interaktywnych przycisków

import pygame_widgets # Główny moduł biblioteki pygame_widgets
from pygame_widgets.slider import Slider # Specyficzna klasa do tworzenia suwaków


def settings_screen(screen: pygame.Surface) -> str:
    """Wyświetla ekran ustawień gry, umożliwiając użytkownikowi modyfikację parametrów.

    Funkcja ta tworzy i zarządza interfejsem użytkownika dla ekranu ustawień,
    włączając w to przycisk "Back" (Powrót) oraz suwaki do regulacji parametrów
    takich jak "Food" (Głód) i "Fun" (Zabawa). Odpowiada za renderowanie tych
    elementów, ich interaktywność oraz aktualizację odpowiednich zmiennych
    globalnych w module `utils` na podstawie danych z suwaków.
    Pętla główna funkcji czeka na interakcję użytkownika (kliknięcia przycisków,
    przesunięcia suwaków) i odpowiednio reaguje, zwracając status nawigacji.

    **Funkcjonalności:**
    * Wyświetlanie tytułu "Settings".
    * Przycisk "Back" do powrotu do menu głównego.
    * Suwaki do regulacji wartości globalnych (np. poziomy głodu i zabawy).
    * Dynamiczne aktualizowanie wartości w module `utils`.

    :param screen: Obiekt powierzchni PyGame (`pygame.Surface`), na której ma być
                   wyświetlany ekran ustawień. Jest to główna powierzchnia okna gry,
                   na której rysowane są wszystkie elementy interfejsu.
    :type screen: pygame.Surface

    :returns: Ciąg znaków (`str`) określający następny ekran gry po wyjściu
              z ekranu ustawień. Możliwe wartości to:
              * `"main_menu"`: Powrót do głównego menu gry.
              * `"quit"`: Zakończenie działania aplikacji.
    :rtype: str

    :raises TypeError: Jeśli `screen` nie jest obiektem `pygame.Surface`.
    """
    # Walidacja parametru wejściowego
    if not isinstance(screen, pygame.Surface):
        raise TypeError("Parametr 'screen' musi być obiektem pygame.Surface.")

    # Inicjalizacja czcionki dla tekstów i przycisków na ekranie ustawień.
    # Rozmiar czcionki jest skalowany proporcjonalnie do wysokości ekranu.
    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.042))

    # --- Inicjalizacja przycisku "Back" ---
    # Tworzenie instancji przycisku "Back" z jego rozmiarem i tekstem.
    back_button = Button(0, 0, WIDTH * 0.13, HEIGHT * 0.056, "Back", font)
    # Wyśrodkowanie przycisku na dole ekranu z określonym przesunięciem w górę.
    back_button.center(offset_y=HEIGHT * 0.185) # Przesunięcie o około 18.5% wysokości ekranu

    # --- Inicjalizacja suwaka dla "Food" (Głodu) ---
    # Obliczanie przesunięć dla suwaka Food względem środka ekranu.
    # Wartości te są dostosowane, aby suwak był umieszczony w odpowiednim miejscu wizualnie.
    offset_x_FOOD = int(-1 * 0.12 * WIDTH) # Przesunięcie w lewo
    offset_y_FOOD = int(-1 * 0.22 * HEIGHT) # Przesunięcie w górę
    # Tworzenie instancji suwaka. Parametry obejmują powierzchnię rysowania, pozycję, rozmiar,
    # oraz zakres wartości (min=0, max=100) i krok (step=1).
    slider_Food = Slider(screen, WIDTH // 2 + offset_x_FOOD, HEIGHT // 2 + offset_y_FOOD, int(WIDTH * 0.234375), int(HEIGHT * 0.0173),
                         min=0, max=100, step=1)

    # --- Inicjalizacja suwaka dla "Fun" (Zabawy) ---
    # Obliczanie przesunięć dla suwaka Fun względem środka ekranu.
    offset_x_FUN = int(-1 * 0.12 * WIDTH) # Przesunięcie w lewo
    offset_y_FUN = int(-1 * 0.08 * HEIGHT) # Przesunięcie w górę
    # Tworzenie instancji suwaka dla Fun, analogicznie do suwaka Food.
    slider_Fun = Slider(screen, WIDTH // 2 + offset_x_FUN, HEIGHT // 2 + offset_y_FUN, int(WIDTH * 0.234375), int(HEIGHT * 0.0173),
                    min=0, max=100, step=1)

    # Obiekt zegara PyGame do kontroli liczby klatek na sekundę (FPS)
    clock = pygame.time.Clock()

    # Flaga kontrolująca główną pętlę ekranu ustawień.
    running = True
    while running:
        # Pobieranie wszystkich zdarzeń z kolejki PyGame.
        events = pygame.event.get()
        for event in events:
            # Obsługa zdarzenia zamknięcia okna (kliknięcie 'X').
            if event.type == pygame.QUIT:
                return "quit" # Zwraca "quit", aby zakończyć grę
            # Obsługa zdarzeń kliknięcia myszy.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Sprawdzenie, czy kliknięto przycisk "Back".
                if back_button.is_clicked(event.pos):
                    return "main_menu" # Zwraca "main_menu", aby wrócić do menu głównego

        # Wypełnienie ekranu kolorem tła (różowym, zdefiniowanym w settings.py).
        screen.fill(PINK)

        # --- Renderowanie tytułu ekranu "Settings" ---
        title = font.render("Settings", True, BLACK)
        # Wyświetlanie tytułu na górze ekranu, wyśrodkowanego.
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT * 0.037))

        # --- Renderowanie i aktualizacja suwaka "Food" ---
        # Tworzenie tekstu wyświetlającego aktualną wartość suwaka Food.
        food_text = font.render(f"Food: {slider_Food.getValue()}", True, BLACK)
        # Aktualizacja globalnej zmiennej w module 'utils' na podstawie wartości suwaka.
        # Jest to kluczowe dla przenoszenia ustawień z ekranu do logiki gry.
        utils.FOOD = slider_Food.getValue()
        # Wyświetlanie tekstu wartości Food na ekranie.
        screen.blit(food_text, (WIDTH // 2 - food_text.get_width() // 2, int(HEIGHT * 0.228)))


        # --- Renderowanie i aktualizacja suwaka "Fun" ---
        # Tworzenie tekstu wyświetlającego aktualną wartość suwaka Fun.
        fun_text = font.render(f"Fun: {slider_Fun.getValue()}", True, BLACK)
        # Aktualizacja globalnej zmiennej w module 'utils' na podstawie wartości suwaka.
        utils.FUN = slider_Fun.getValue()
        print(utils.FUN) # Logowanie wartości Fun do konsoli (dla celów debugowania)
        # Wyświetlanie tekstu wartości Fun na ekranie.
        screen.blit(fun_text, (WIDTH // 2 - fun_text.get_width() // 2, int(HEIGHT * 0.37)))


        # Rysowanie przycisku "Back".
        back_button.draw(screen)

        # Aktualizacja wszystkich widżetów z biblioteki pygame_widgets.
        # Należy to wywołać po przetworzeniu zdarzeń, aby widżety mogły reagować na interakcje.
        pygame_widgets.update(events)
        # Odświeżenie całego ekranu, aby wyświetlić wszystkie zmiany.
        pygame.display.update()