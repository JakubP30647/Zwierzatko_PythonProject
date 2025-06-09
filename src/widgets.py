"""
widgets.py - Moduł definiujący interaktywne elementy interfejsu użytkownika (GUI) dla gry "ZWIERZE".

Ten moduł zawiera implementacje podstawowych, wizualnych komponentów GUI,
które są kluczowe dla interakcji użytkownika z grą. W szczególności definiuje
klasy `Button` (przycisk) i `Bar` (pasek statusu/postępu).

Celem tego modułu jest dostarczenie elastycznych i łatwych w użyciu elementów,
które można wdrożyć na różnych ekranach gry, takich jak menu główne, ekran ustawień,
czy podczas samej rozgrywki. Każdy widżet został zaprojektowany z myślą o:

1.  **Wizualnej reprezentacji:** Renderowanie graficzne na ekranie gry.
2.  **Interaktywności:** Reagowanie na działania użytkownika (np. kliknięcia myszą).
3.  **Łatwości konfiguracji:** Możliwość dostosowania pozycji, rozmiaru, tekstu
    i kolorów.

Widżety w tym module ściśle współpracują z globalnymi ustawieniami i kolorami
zdefiniowanymi w module `settings`, co zapewnia spójny wygląd i zachowanie
w całej aplikacji.
"""

import pygame  # Główna biblioteka PyGame, niezbędna do rysowania, obsługi zdarzeń i zarządzania powierzchniami.
import \
    settings  # Importuje moduł `settings` w całości, aby mieć dostęp do globalnych stałych, takich jak kolory (np. settings.GRAY).
from settings import *  # Importuje wszystkie symbole (stałe) z modułu `settings` bezpośrednio do bieżącej przestrzeni nazw


# (np. WIDTH, HEIGHT, PINK, BLACK), co pozwala na ich użycie bez prefiksu `settings.`.

class Button:
    """Reprezentuje interaktywny przycisk graficzny w interfejsie użytkownika (GUI) gry.

    Klasa `Button` jest fundamentalnym elementem nawigacji i interakcji,
    pozwalającym użytkownikowi na wyzwalanie określonych akcji poprzez kliknięcie.
    Przycisk jest wizualnie reprezentowany przez prostokąt, który może zawierać tekst,
    i reaguje na interakcje kursora myszy, zmieniając swój wygląd (np. kolor)
    po najechaniu (`hover effect`).

    **Główne atrybuty i funkcjonalności:**
    * **Pozycja i rozmiar:** Definiowane przez prostokąt `pygame.Rect`.
    * **Tekst:** Dowolny ciąg znaków wyświetlany na przycisku.
    * **Styl:** Kolor tła przycisku zmienia się po najechaniu kursorem myszy,
        zapewniając wizualną informację zwrotną.
    * **Wykrywanie kliknięć:** Metoda `is_clicked()` pozwala łatwo sprawdzić,
        czy użytkownik kliknął przycisk.
    * **Centrowanie:** Metoda `center()` ułatwia precyzyjne pozycjonowanie przycisku
        względem środka ekranu.
    """

    def __init__(self, x, y, width, height, text, font):
        """Inicjalizuje nową instancję klasy `Button`.

        Konstruktor definiuje podstawowe właściwości wizualne i interaktywne przycisku,
        takie jak jego pozycja, wymiary, wyświetlany tekst oraz styl czcionki.

        :param x: Początkowa współrzędna X (horyzontalna) lewego górnego rogu prostokąta przycisku.
                  Wartość całkowita.
        :type x: int
        :param y: Początkowa współrzędna Y (wertykalna) lewego górnego rogu prostokąta przycisku.
                  Wartość całkowita.
        :type y: int
        :param width: Szerokość przycisku w pikselach. Musi być wartością całkowitą i dodatnią.
        :type width: int
        :param height: Wysokość przycisku w pikselach. Musi być wartością całkowitą i dodatnią.
        :type height: int
        :param text: Ciąg znaków, który zostanie wyświetlony na przycisku.
                     Powinien być zwięzły i jasno komunikować przeznaczenie przycisku.
        :type text: str
        :param font: Obiekt czcionki PyGame (`pygame.font.Font`), który zostanie użyty
                     do renderowania tekstu przycisku. Należy go zainicjalizować
                     przed przekazaniem do konstruktora.
        :type font: pygame.font.Font

        :ivar rect: Obiekt `pygame.Rect`, który precyzyjnie definiuje pozycję
                    i rozmiar prostokątnego obszaru zajmowanego przez przycisk.
                    Jest używany do rysowania i wykrywania kolizji/kliknięć.
        :vartype rect: pygame.Rect
        :ivar text: Tekst, który jest aktualnie wyświetlany na przycisku.
                    Można go dynamicznie zmieniać, aby odzwierciedlał stan.
        :vartype text: str
        :ivar font: Obiekt `pygame.font.Font` używany do renderowania tekstu na przycisku.
                    Zachowany do wewnętrznego użytku.
        :vartype font: pygame.font.Font
        """
        self.rect = pygame.Rect(x, y, width,
                                height)  # Inicjalizacja prostokąta, który definiuje fizyczny obszar przycisku na ekranie.
        self.text = text  # Przypisanie tekstu, który będzie renderowany na przycisku.
        self.font = font  # Przypisanie obiektu czcionki, używanego do stylizacji tekstu.

    def draw(self, surface):
        """Rysuje przycisk na określonej powierzchni PyGame, uwzględniając efekt najechania kursorem.

        Metoda ta jest odpowiedzialna za wizualne przedstawienie przycisku w grze.
        Najpierw rysuje prostokąt tła przycisku, zmieniając jego kolor, jeśli kursor
        myszy znajduje się nad nim (tzw. "hover effect"). Następnie renderuje tekst
        przycisku i umieszcza go centralnie na nim.

        :param surface: Powierzchnia PyGame (`pygame.Surface`), na której przycisk ma zostać narysowany.
                        Zazwyczaj jest to główny ekran gry, na której wyświetlane są wszystkie elementy.
        :type surface: pygame.Surface
        """
        mouse_pos = pygame.mouse.get_pos()  # Pobranie aktualnej pozycji kursora myszy. Jest to tupla (x, y).
        # Określenie koloru tła przycisku.
        # Jeśli kursor myszy (mouse_pos) koliduje z prostokątem przycisku (self.rect),
        # użyj koloru SZAREGO (settings.GRAY) jako efektu najechania.
        # W przeciwnym razie użyj domyślnego koloru RÓŻOWEGO (settings.PINK).
        color = settings.GRAY if self.rect.collidepoint(mouse_pos) else settings.PINK
        pygame.draw.rect(surface, color, self.rect)  # Rysowanie prostokąta tła przycisku na podanej powierzchni.

        # Renderowanie tekstu przycisku.
        # `render()` tworzy nową powierzchnię (`pygame.Surface`) zawierającą tekst.
        # `True` oznacza włączenie antyaliasingu (wygładzania krawędzi tekstu),
        # a `settings.BLACK` to kolor tekstu.
        text_surf = self.font.render(self.text, True, settings.BLACK)

        # Pobranie prostokąta otaczającego powierzchnię z tekstem i wyśrodkowanie go
        # w obrębie prostokąta przycisku (self.rect).
        text_rect = text_surf.get_rect(center=self.rect.center)

        # Rysowanie (blitting) powierzchni z tekstem na powierzchni głównej,
        # w miejscu wyśrodkowanym na przycisku.
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        """Sprawdza, czy określony punkt (zazwyczaj pozycja kliknięcia myszy)
        znajduje się w obrębie prostokąta przycisku.

        Ta metoda jest kluczowa do implementacji interakcji użytkownika z przyciskiem.
        Zazwyczaj jest wywoływana w pętli zdarzeń gry, gdy wykryto zdarzenie kliknięcia myszy.

        :param pos: Krotka (`tuple`) zawierająca współrzędne X i Y punktu do sprawdzenia.
                    Typowo jest to `event.pos` z obiektu zdarzenia PyGame.
        :type pos: tuple[int, int]
        :returns: `True`, jeśli punkt `pos` koliduje z prostokątem przycisku (`self.rect`),
                  co oznacza, że przycisk został kliknięty. W przeciwnym razie `False`.
        :rtype: bool
        """
        # Użycie wbudowanej metody `collidepoint()` obiektu `pygame.Rect`
        # do efektywnego sprawdzenia, czy dany punkt znajduje się w prostokącie.
        return self.rect.collidepoint(pos)

    def center(self, offset_x=0, offset_y=0):
        """Centruje przycisk na ekranie gry, z możliwością zastosowania dodatkowych przesunięć.

        Metoda ta dynamicznie ustawia środek przycisku w oparciu o globalne
        wymiary ekranu (WIDTH i HEIGHT, zaimportowane z `settings`).
        Pozwala to na łatwe i responsywne pozycjonowanie przycisków
        w różnych układach interfejsu użytkownika, bez konieczności ręcznego
        obliczania dokładnych współrzędnych dla każdego przycisku.

        :param offset_x: Opcjonalne przesunięcie horyzontalne (w pikselach) od centralnej
                         pozycji X ekranu. Dodatnia wartość przesuwa przycisk w prawo,
                         ujemna w lewo. Domyślnie `0` (brak przesunięcia horyzontalnego).
        :type offset_x: int
        :param offset_y: Opcjonalne przesunięcie wertykalne (w pikselach) od centralnej
                         pozycji Y ekranu. Dodatnia wartość przesuwa przycisk w dół,
                         ujemna w górę. Domyślnie `0` (brak przesunięcia wertykalnego).
        :type offset_y: int
        """
        # Ustawienie środka X przycisku na środku szerokości ekranu plus opcjonalne przesunięcie.
        # `WIDTH // 2` to środek ekranu w poziomie.
        self.rect.centerx = WIDTH // 2 + offset_x

        # Ustawienie środka Y przycisku na środku wysokości ekranu plus opcjonalne przesunięcie.
        # `HEIGHT // 2` to środek ekranu w pionie.
        self.rect.centery = HEIGHT // 2 + offset_y


class Bar:
    """Reprezentuje graficzny pasek statusu lub postępu w grze.

    Klasa `Bar` służy do wizualnego przedstawiania wartości liczbowej
    (np. zdrowia, poziomu głodu, paska doświadczenia, postępu ładowania)
    w stosunku do jej wartości maksymalnej. Pasek składa się z tła (kolor1)
    i wypełnienia (kolor2), którego długość jest proporcjonalna do bieżącej
    wartości. Jest to prosty, ale efektywny sposób na przekazanie stanu
    graczowi.

    **Główne atrybuty i funkcjonalności:**
    * **Wizualizacja:** Graficzne przedstawienie wartości jako wypełnionego prostokąta.
    * **Konfiguracja:** Możliwość dostosowania pozycji, rozmiaru oraz kolorów
        tła i wypełnienia paska.
    * **Dynamiczność:** Łatwa aktualizacja wartości paska w celu odzwierciedlenia zmian stanu.
    """

    def __init__(self, x, y, width, height, max):
        """Inicjalizuje nową instancję paska statusu.

        Definiuje pozycję i wymiary paska, jego maksymalną wartość,
        oraz domyślne kolory tła i wypełnienia.
        Początkowo pasek jest w pełni wypełniony (ratio = max).

        :param x: Współrzędna X lewego górnego rogu paska.
        :type x: int
        :param y: Współrzędna Y lewego górnego rogu paska.
        :type y: int
        :param width: Całkowita szerokość paska w pikselach.
        :type width: int
        :param height: Wysokość paska w pikselach.
        :type height: int
        :param max: Maksymalna wartość, jaką pasek może reprezentować.
                          Wartość bieżąca paska (`self.ratio`) będzie skalowana
                          proporcjonalnie do tej wartości. Musi być liczbą dodatnią.
        :type max: float

        :ivar x: Współrzędna X lewego górnego rogu paska.
        :vartype x: int
        :ivar y: Współrzędna Y lewego górnego rogu paska.
        :vartype y: int
        :ivar width: Całkowita szerokość paska.
        :vartype width: int
        :ivar height: Wysokość paska.
        :vartype height: int
        :ivar ratio: Aktualna wartość paska. Ta zmienna powinna być aktualizowana
                     zewnętrznie (np. przez logikę gry) w celu zmiany wypełnienia paska.
                     Domyślnie ustawiona na `max` podczas inicjalizacji.
        :vartype ratio: float
        :ivar max: Maksymalna wartość, jaką pasek może osiągnąć. Używana jako baza
                   do obliczania proporcji wypełnienia.
        :vartype max: float
        :ivar color1: Kolor tła paska (domyślnie czerwony), reprezentujący "pustą" część paska.
        :vartype color1: str
        :ivar color2: Kolor wypełnienia paska (domyślnie zielony), reprezentujący
                      aktualną wartość.
        :vartype color2: str
        """
        self.x = x  # Przypisanie pozycji X paska.
        self.y = y  # Przypisanie pozycji Y paska.
        self.width = width  # Przypisanie całkowitej szerokości paska.
        self.height = height  # Przypisanie wysokości paska.
        self.ratio = max  # 'ratio' reprezentuje aktualną wartość paska, początkowo jest ustawiona na wartość maksymalną.
        # Ta zmienna będzie zmieniana dynamicznie.
        self.max = max  # 'max' przechowuje stałą wartość maksymalną paska, do której odnosimy 'ratio'.
        self.color1 = "red"  # Domyślny kolor tła paska (np. puste miejsce).
        self.color2 = "green"  # Domyślny kolor wypełnienia paska (np. aktualna wartość).

    def draw(self, surface):
        """Rysuje pasek statusu na określonej powierzchni PyGame.

        Metoda renderuje dwa prostokąty: jeden jako tło paska (o pełnej szerokości,
        w kolorze `self.color1`) i drugi jako wypełnienie (o szerokości proporcjonalnej
        do bieżącej wartości `self.ratio`, w kolorze `self.color2`).

        :param surface: Powierzchnia PyGame (`pygame.Surface`), na której pasek ma zostać narysowany.
                        Zazwyczaj jest to główny ekran gry, na którym wyświetlane są wszystkie elementy.
        :type surface: pygame.Surface
        """
        # Obliczenie proporcji wypełnienia paska.
        # `self.ratio` jest bieżącą wartością, a `self.max` to maksymalna.
        # `max(0, min(1, ...))` zapewnia, że proporcja zawsze mieści się w zakresie [0, 1],
        # co zapobiega rysowaniu paska poza jego ramami, jeśli `self.ratio` jest poza zakresem.
        ratio = self.ratio / self.max

        # Rysowanie prostokąta tła paska. Ma on pełną szerokość i wysokość zdefiniowaną dla paska.
        pygame.draw.rect(surface, self.color1, (self.x, self.y, self.width, self.height))

        # Rysowanie prostokąta wypełnienia paska.
        # Jego szerokość jest obliczana jako proporcja `ratio` z całkowitej szerokości `self.width`.
        # To dynamicznie dostosowuje wypełnienie paska.
        pygame.draw.rect(surface, self.color2, (self.x, self.y, self.width * ratio, self.height))