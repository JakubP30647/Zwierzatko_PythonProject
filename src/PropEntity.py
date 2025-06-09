import pygame

class PropEntity:
    """Reprezentuje ruchomy obiekt (rekwizyt) w świecie gry, który dąży do określonego celu.

    Ta klasa jest fundamentalnym elementem dla wszelkiego rodzaju interaktywnych,
    zbieralnych lub przemieszczających się rekwizytów w grze, takich jak jedzenie
    czy ikony reprezentujące interakcje (np. serduszka po głaskaniu). Jej głównym
    zadaniem jest zarządzanie pozycją obiektu na ekranie, jego wyglądem graficznym
    oraz logicznym zachowaniem, takim jak poruszanie się w kierunku wyznaczonego
    punktu docelowego.

    Klasa `PropEntity` jest zaprojektowana tak, aby być elastyczną i łatwą do
    ponownego wykorzystania dla różnych typów rekwizytów, które charakteryzują się
    ruchem w stronę określonego celu. Zapewnia podstawowe funkcjonalności renderowania,
    wykrywania kolizji oraz dynamicznego przemieszczania.

    **Typowe przypadki użycia:**
    * Wizualizacja jedzenia, które porusza się w kierunku zwierzątka.
    * Wyświetlanie "serduszek", które unoszą się lub podążają do zwierzątka po interakcji.
    * Implementacja innych zbieralnych przedmiotów, które gracz lub zwierzątko może "złapać".

    """
    def __init__(self, x: float, y: float, image: pygame.Surface):
        """Inicjalizuje nową instancję obiektu PropEntity.

        Konstruktor ustawia początkową pozycję obiektu, przypisuje mu grafikę
        do wyświetlania oraz definiuje jego domyślną prędkość poruszania się.
        Wszystkie te parametry są kluczowe dla wizualizacji i interakcji z rekwizytem.

        :param x: Początkowa współrzędna X środka obiektu na ekranie gry.
                  Określa horyzontalne położenie, od którego obiekt rozpocznie swój ruch.
                  Wartość powinna być zmiennoprzecinkowa dla precyzyjnego pozycjonowania.
        :type x: float
        :param y: Początkowa współrzędna Y środka obiektu na ekranie gry.
                  Określa wertykalne położenie, od którego obiekt rozpocznie swój ruch.
                  Wartość powinna być zmiennoprzecinkowa dla precyzyjnego pozycjonowania.
        :type y: float
        :param image: Obiekt `pygame.Surface` (obraz) reprezentujący grafikę rekwizytu.
                      Ten obraz zostanie narysowany na ekranie. Powinien być już załadowany
                      i, w razie potrzeby, przeskalowany do odpowiedniego rozmiaru
                      przed przekazaniem do konstruktora, aby zapewnić optymalną wydajność.
        :type image: pygame.Surface

        :ivar x: Aktualna współrzędna X obiektu. Jest to dynamicznie aktualizowana
                 wartość podczas ruchu obiektu.
        :vartype x: float
        :ivar y: Aktualna współrzędna Y obiektu. Podobnie jak `x`, jest aktualizowana
                 w czasie rzeczywistym.
        :vartype y: float
        :ivar image: Obiekt `pygame.Surface` - graficzna reprezentacja rekwizytu.
                     Pozostaje stały przez cały cykl życia obiektu, chyba że zostanie
                     manualnie zmieniony.
        :vartype image: pygame.Surface
        :ivar speed: Szybkość poruszania się obiektu w pikselach na klatkę.
                     Jest to wartość domyślna, którą można modyfikować, aby
                     dostosować dynamikę ruchu rekwizytu.
        :vartype speed: int

        :raises TypeError: Jeśli `image` nie jest obiektem `pygame.Surface`.
                           (Dodatkowa uwaga: typowanie Python nie wymusza tego, ale
                           można by dodać walidację w implementacji, jeśli konieczne).
        """
        self.x = x # Ustawienie początkowej pozycji X
        self.y = y # Ustawienie początkowej pozycji Y
        # Sprawdzenie, czy image jest poprawnym obiektem PyGame Surface (opcjonalna walidacja)
        if not isinstance(image, pygame.Surface):
            raise TypeError("Parametr 'image' musi być obiektem pygame.Surface.")
        self.image = image # Przypisanie obiektu graficznego rekwizytu
        self.speed = 3 # Domyślna prędkość obiektu w pikselach na klatkę. Może być dostosowana.


    def draw(self, screen: pygame.Surface):
        """Rysuje aktualny obraz obiektu PropEntity na określonej powierzchni ekranu.

        Ta metoda jest odpowiedzialna za wizualne przedstawienie rekwizytu w grze.
        Obraz jest rysowany bezpośrednio na współrzędnych `(self.x, self.y)`,
        co oznacza, że lewy górny róg obrazu znajduje się w tej pozycji.

        :param screen: Obiekt powierzchni PyGame (główny ekran gry lub inna powierzchnia),
                       na której obiekt ma zostać narysowany. Jest to kluczowy parametr
                       do renderowania grafiki w PyGame.
        :type screen: pygame.Surface

        :raises TypeError: Jeśli `screen` nie jest obiektem `pygame.Surface`.
        """
        if not isinstance(screen, pygame.Surface):
            raise TypeError("Parametr 'screen' musi być obiektem pygame.Surface.")
        screen.blit(self.image, (self.x, self.y)) # Rysowanie obrazu rekwizytu na ekranie

    def get_rect(self) -> pygame.Rect:
        """Zwraca obiekt `pygame.Rect` reprezentujący prostokąt kolizji rekwizytu.

        Ten prostokąt jest używany do wykrywania kolizji z innymi obiektami w grze,
        takimi jak zwierzątko. Prostokąt jest tworzony na podstawie rozmiaru obrazu
        rekwizytu i jest wyśrodkowany na jego aktualnych współrzędnych `(self.x, self.y)`.
        Jest to niezbędna metoda do implementacji interakcji w grze.

        :returns: Obiekt `pygame.Rect`, który precyzyjnie opisuje obszar, jaki zajmuje
                  rekwizyt na ekranie i jest używany do sprawdzania kolizji.
        :rtype: pygame.Rect
        """
        # Pobranie prostokąta obrazu i ustawienie jego środka na pozycji (self.x, self.y)
        # To zapewnia, że kolizje są obliczane względem centralnego punktu obiektu.
        return pygame.Rect(self.image.get_rect(center=(self.x, self.y)))

    def move_towards(self, target_x: float, target_y: float):
        """Przesuwa obiekt PropEntity w kierunku określonych współrzędnych docelowych.

        Metoda oblicza wektor kierunku do celu, normalizuje go, a następnie przesuwa
        obiekt o wartość `self.speed` wzdłuż tego wektora. Obiekt będzie poruszał
        się w linii prostej do momentu osiągnięcia celu lub przekroczenia go.
        Ruch jest płynny i niezależny od odległości.

        **Algorytm ruchu:**
        1.  Obliczenie różnic w współrzędnych (dx, dy) między aktualną pozycją a celem.
        2.  Obliczenie odległości Euklidesowej do celu.
        3.  Normalizacja wektora kierunku (dx, dy) poprzez podzielenie go przez odległość.
            To tworzy wektor jednostkowy, który ma długość 1.
        4.  Pomnożenie wektora jednostkowego przez `self.speed` i dodanie go do
            aktualnych współrzędnych obiektu, co powoduje ruch o stałą prędkość.
        5.  Jeśli obiekt jest już w celu (distance == 0), ruch zostaje zatrzymany,
            aby zapobiec dzieleniu przez zero i niepotrzebnym obliczeniom.

        :param target_x: Docelowa współrzędna X, do której obiekt ma się poruszyć.
                         Reprezentuje horyzontalną pozycję celu.
        :type target_x: float
        :param target_y: Docelowa współrzędna Y, do której obiekt ma się poruszyć.
                         Reprezentuje wertykalną pozycję celu.
        :type target_y: float
        """
        # Obliczenie różnic w współrzędnych między celem a aktualną pozycją obiektu
        dx = target_x - self.x
        dy = target_y - self.y

        # Obliczenie odległości Euklidesowej (prostej linii) do celu
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Sprawdzenie, czy obiekt nie jest już w celu, aby uniknąć dzielenia przez zero
        if distance != 0:
            # Normalizacja wektora kierunku. Dzielenie przez 'distance' sprawia,
            # że 'dx' i 'dy' stają się składowymi wektora jednostkowego (długości 1).
            dx /= distance
            dy /= distance
            # Przesunięcie obiektu o wartość 'self.speed' w kierunku celu.
            # Dzięki normalizacji, ruch odbywa się ze stałą prędkością.
            self.x += dx * self.speed
            self.y += dy * self.speed