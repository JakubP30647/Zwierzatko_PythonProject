from choice_screen import choice_screen
from gameplay_screen import gameplay_screen
from settings import *
from mainMenu_screen import main_menu
from settings_screen import settings_screen
import pygame # Dodaj import pygame, jeśli jeszcze go nie ma

def main():
    """Główna funkcja aplikacji zarządzająca przepływem między różnymi ekranami gry.

    Odpowiada za inicjalizację biblioteki PyGame, ustawienie trybu wyświetlania
    oraz tytułu okna. Funkcja `main` działa w nieskończonej pętli,
    przełączając się między ekranami takimi jak menu główne, ekran wyboru,
    ekran rozgrywki i ekran ustawień, w zależności od wartości zwracanych
    przez każdą funkcję ekranu. Pętla kończy działanie, gdy jakikolwiek ekran
    zwróci status "quit".
    """
    pygame.init() # Inicjalizacja wszystkich modułów PyGame
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Ustawienie rozmiaru okna gry
    pygame.display.set_caption(TITLE) # Ustawienie tytułu okna

    current_screen = "main_menu" # Początkowy ekran, od którego startuje gra

    # Główna pętla aplikacji, zarządzająca przełączaniem ekranów
    while True:
        if current_screen == "main_menu":
            result = main_menu(screen) # Wywołuje ekran menu głównego
        elif current_screen == "choice_screen":
            result = choice_screen(screen) # Wywołuje ekran wyboru zwierzątka/trybu
        elif current_screen == "gameplay_screen":
            result = gameplay_screen(screen) # Wywołuje ekran głównej rozgrywki
        elif current_screen == "settings":
            result = settings_screen(screen) # Wywołuje ekran ustawień
        elif current_screen == "quit":
            break # Przerywa pętlę i kończy grę, jeśli ekran zwróci "quit"


        current_screen = result # Aktualizuje bieżący ekran na podstawie zwróconego rezultatu

    pygame.quit() # Deinicjalizacja PyGame po zakończeniu pętli

if __name__ == "__main__":
    main() # Uruchamia funkcję main() tylko, gdy skrypt jest uruchamiany bezpośrednio