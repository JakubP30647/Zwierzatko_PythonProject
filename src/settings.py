"""
settings.py - Konfiguracja globalnych ustawień i stałych dla gry "ZWIERZE".

Ten moduł definiuje kluczowe parametry środowiska gry, takie jak rozdzielczość ekranu,
tytuł okna, oraz paleta kolorów używanych w całej aplikacji.
Jest to centralne miejsce do zarządzania wszystkimi wartościami, które mogą być
potrzebne w wielu różnych modułach gry, zapewniając spójność i łatwość modyfikacji.
"""

import pygame

# Inicjalizacja PyGame jest wykonywana tutaj, aby upewnić się, że moduł 'display'
# jest gotowy do pobierania informacji o ekranie. Jest to kluczowe dla dynamicznego
# ustawiania rozdzielczości ekranu.
pygame.init()

# --- Ustawienia ekranu ---
# Pobieranie informacji o aktualnym trybie wyświetlania systemu.
# Pozwala to na dostosowanie rozdzielczości gry do rozdzielczości monitora użytkownika.
info = pygame.display.Info()

# Szerokość okna gry, ustawiona na aktualną szerokość ekranu użytkownika.
# Zapewnia to, że gra działa w trybie pełnoekranowym lub z maksymalną dostępną przestrzenią.
WIDTH = info.current_w

# Wysokość okna gry, ustawiona na aktualną wysokość ekranu użytkownika.
# Podobnie jak szerokość, dostosowuje się do rozdzielczości monitora.
HEIGHT = info.current_h

# Tytuł okna gry, wyświetlany w pasku tytułowym.
TITLE = "ZWIERZE"

# --- Definicje kolorów ---
# Definicje kolorów w formacie RGB (Red, Green, Blue).
# Używanie nazwanych stałych ułatwia zarządzanie paletą kolorów
# i poprawia czytelność kodu w całej aplikacji.

WHITE = (255, 255, 255) # Czysta biel
GRAY = (200, 200, 200)  # Jasnoszary
DARK_GRAY = (160, 160, 160) # Ciemniejszy odcień szarości
BLACK = (0, 0, 0)       # Czysta czerń
PINK = (255,112,180)    # Żywy róż, często używany jako tło
YELLOW = (255,235,0)    # Jasny żółty
BLUE = (0,0,255)        # Czysty niebieski
GREEN = (0,255,0)       # Czysty zielony