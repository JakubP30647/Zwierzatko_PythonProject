"""
utils.py - Globalne zmienne stanu gry i funkcje pomocnicze.

Ten moduł służy jako centralne repozytorium dla globalnych zmiennych, które
kontrolują stan gry oraz kluczowe ustawienia dotyczące zwierzątka i dostępnych
zasobów. Zawiera również funkcje pomocnicze, które są używane w różnych
częściach aplikacji, takie jak inicjalizacja listy obiektów jedzenia.

Zmienne globalne w tym module są dynamicznie aktualizowane przez inne ekrany
(np. ekran ustawień), co pozwala na elastyczne dostosowanie zachowania gry
bez konieczności przekazywania tych wartości przez wiele warstw funkcji.
"""

import os # Moduł do interakcji z systemem operacyjnym, np. do listowania plików
import pygame # Główna biblioteka PyGame, używana m.in. do ładowania obrazów
import settings # Importuje moduł settings dla dostępu do globalnych stałych, takich jak HEIGHT
from settings import HEIGHT # Bezpośredni import HEIGHT dla skalowania czcionki

# --- Globalne zmienne stanu gry ---

# FUN (Zabawa): Globalna zmienna przechowująca aktualny poziom zabawy zwierzątka.
# Wartość domyślna to 50. Może być modyfikowana przez ekran ustawień
# i wpływa na zachowanie zwierzątka oraz wymagania rozgrywki.
FUN = 50

# FOOD (Głód): Globalna zmienna przechowująca aktualny poziom głodu zwierzątka.
# Wartość domyślna to 50. Podobnie jak FUN, jest konfigurowalna w ustawieniach
# i ma wpływ na mechanikę gry.
FOOD = 50

# SYSTEMpet: Globalna zmienna przechowująca nazwę (ID) aktualnie wybranego zwierzątka.
# Jest to nazwa katalogu w 'assets/', w którym znajdują się grafiki dla danego zwierzątka.
# Domyślnie ustawiona na "rabbit" (królik).
SYSTEMpet = "rabbit"

# SYSTEMamountOfFrame: Globalna zmienna przechowująca liczbę klatek animacji
# dla wybranego zwierzątka (np. dla animacji biegania). Używana do cyklicznego
# odtwarzania animacji. Domyślnie ustawiona na 7.
SYSTEMamountOfFrame = 7

# --- Inicjalizacja zasobów GUI ---

# Czcionka używana w różnych miejscach interfejsu użytkownika.
# Skalowana dynamicznie na podstawie wysokości ekranu dla zachowania responsywności.
font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.037))

# --- Lista zasobów dla jedzenia ---

# Lista przechowująca załadowane obrazy jedzenia.
# Jest zapełniana przez funkcję `foodInstall()` podczas inicjalizacji gry.
foodList = []

# --- Funkcje pomocnicze ---

def set_pet_data(pet_name: str, frame_count: int):
    """Ustawia globalne dane dotyczące wybranego zwierzątka.

    Ta funkcja aktualizuje globalne zmienne `SYSTEMpet` i `SYSTEMamountOfFrame`,
    co pozwala na dynamiczną zmianę aktywnego zwierzątka w grze.
    Jest zazwyczaj wywoływana po dokonaniu wyboru zwierzątka (np. na ekranie wyboru).

    :param pet_name: Nazwa nowego zwierzątka (ciąg znaków), która odpowiada
                     nazwie katalogu z jego grafikami w folderze 'assets'.
                     Przykładowo: "rabbit", "cat", "dog".
    :type pet_name: str
    :param frame_count: Całkowita liczba klatek animacji dla nowego zwierzątka.
                        Jest to niezbędne do poprawnego odtwarzania animacji
                        biegania lub innych sekwencji ruchów.
    :type frame_count: int

    :global SYSTEMpet: Zmienna globalna, która jest aktualizowana na nową nazwę zwierzątka.
    :global SYSTEMamountOfFrame: Zmienna globalna, która jest aktualizowana na nową liczbę klatek.
    """
    global SYSTEMpet # Deklaracja globalna, aby móc modyfikować zmienną spoza zakresu funkcji
    global SYSTEMamountOfFrame # Deklaracja globalna, aby móc modyfikować zmienną spoza zakresu funkcji
    SYSTEMpet = pet_name # Przypisanie nowej nazwy zwierzątka
    SYSTEMamountOfFrame = frame_count # Przypisanie nowej liczby klatek animacji

def foodInstall():
    """Ładuje wszystkie obrazy jedzenia z katalogu 'assets/food' do listy `foodList`.

    Ta funkcja skanuje podkatalog 'assets/food' w poszukiwaniu plików PNG.
    Każdy znaleziony plik obrazu jest ładowany, konwertowany z kanałem alpha
    (przezroczystością) i dodawany do globalnej listy `foodList`.
    Funkcja jest krytyczna dla inicjalizacji zasobów graficznych jedzenia
    na początku działania gry. W przypadku błędu ładowania pliku, informuje
    o tym w konsoli, ale nie przerywa działania programu.

    :global foodList: Lista globalna, do której doładowywane są obrazy jedzenia.
                     Zawartość tej listy jest dostępna w innych modułach gry.

    :raises pygame.error: W przypadku problemów z ładowaniem obrazu (np. plik uszkodzony,
                          niepoprawny format), błąd jest wyłapywany i logowany.
    """
    for filename in os.listdir('assets/food'): # Iteracja przez wszystkie pliki w katalogu 'assets/food'
        # Sprawdzenie, czy plik jest obrazem PNG (ignorowanie wielkości liter)
        if filename.lower().endswith(".png"):
            full_path = os.path.join('assets/food', filename) # Konstruowanie pełnej ścieżki do pliku
            try:
                # Ładowanie obrazu i konwersja do formatu z kanałem alpha (przezroczystością).
                # convert_alpha() optymalizuje obraz pod kątem wyświetlania na tle z przezroczystością.
                image = pygame.image.load(full_path).convert_alpha()
                foodList.append(image) # Dodanie załadowanego obrazu do globalnej listy
            except pygame.error as e:
                # Obsługa błędu, jeśli obraz nie mógł zostać załadowany.
                # Wyświetla komunikat o błędzie, ale pozwala programowi kontynuować.
                print(f"Could not load {filename}: {e}")