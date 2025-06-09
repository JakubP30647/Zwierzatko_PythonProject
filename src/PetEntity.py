import pygame

import settings
import utils
from settings import WIDTH, HEIGHT


class PetEntity:
    """Reprezentuje wirtualne zwierzątko w grze, zarządzające jego wyglądem i animacjami.

    Klasa ta odpowiada za ładowanie i skalowanie obrazów zwierzątka, obsługę animacji
    ruchu (bieganie) oraz stanu spoczynku (idle). Przechowuje również informacje o
    pozycji, rozmiarze i kierunku, w którym zwrócone jest zwierzątko. Zapewnia metody
    do aktualizacji animacji, rysowania na ekranie, pobierania prostokąta kolizji
    oraz zmiany kierunku i odświeżania obrazów.
    """
    def __init__(self, x, y):
        """Inicjalizuje nową instancję PetEntity.

        Ładuje początkowe obrazy dla stanu spoczynku i animacji biegania,
        skaluje je do odpowiednich rozmiarów i ustawia początkowe parametry
        animacji.

        :param x: Początkowa pozycja X środka zwierzątka na ekranie.
        :type x: float
        :param y: Początkowa pozycja Y środka zwierzątka na ekranie.
        :type y: float

        :ivar x: Aktualna pozycja X środka zwierzątka.
        :vartype x: float
        :ivar y: Aktualna pozycja Y środka zwierzątka.
        :vartype y: float
        :ivar amountOfFrames: Całkowita liczba klatek w animacji biegania, pobrana z `utils.SYSTEMamountOfFrame`.
        :vartype amountOfFrames: int
        :ivar current_frame: Indeks aktualnie wyświetlanej klatki animacji.
        :vartype current_frame: int
        :ivar animation_speed: Szybkość przełączania klatek animacji. Wyższa wartość oznacza szybszą animację.
        :vartype animation_speed: float
        :ivar animation_timer: Timer używany do kontrolowania tempa animacji. Zwiększa się, aż osiągnie 1,
                              co sygnalizuje zmianę klatki.
        :vartype animation_timer: float
        :ivar frameSide: Kierunek, w którym zwrócone jest zwierzątko ("right" lub "left").
                        Wpływa na to, czy klatki animacji są odwracane.
        :vartype frameSide: str
        :ivar petName: Nazwa folderu, w którym znajdują się zasoby graficzne zwierzątka, pobrana z `utils.SYSTEMpet`.
        :vartype petName: str
        :ivar PET_WIDTH: Szerokość obrazka zwierzątka w pikselach, skalowana proporcjonalnie do szerokości ekranu.
        :vartype PET_WIDTH: int
        :ivar PET_HEIGHT: Wysokość obrazka zwierzątka w pikselach, skalowana proporcjonalnie do wysokości ekranu.
        :vartype PET_HEIGHT: int
        :ivar idle_image: Obrazek zwierzątka w stanie spoczynku (nieanimowany).
        :vartype idle_image: pygame.Surface
        :ivar running_frames: Lista obiektów `pygame.Surface` reprezentujących klatki animacji biegania.
        :vartype running_frames: list[pygame.Surface]
        :ivar currentVisiableImg: Aktualnie wyświetlany obrazek zwierzątka (może być klatką biegania lub obrazkiem idle).
        :vartype currentVisiableImg: pygame.Surface
        """
        self.x = x
        self.y = y
        self.amountOfFrames = utils.SYSTEMamountOfFrame
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.frameSide = "right" # Początkowy kierunek ustawiony na prawo
        self.petName = utils.SYSTEMpet
        self.PET_WIDTH = int(WIDTH * 0.05)
        self.PET_HEIGHT = int(HEIGHT * 0.08)

        # Ładowanie i skalowanie obrazka dla stanu "Idle" (spoczynku)
        self.idle_image = pygame.transform.scale(pygame.image.load(f'assets/{self.petName}/Idle.png'), (self.PET_WIDTH, self.PET_HEIGHT)).convert_alpha()

        # Ładowanie i skalowanie klatek animacji "Running" (biegania)
        self.running_frames = []
        for i in range(0,self.amountOfFrames):
            frame = pygame.image.load(f'assets/{self.petName}/{str(i).zfill(2)}_Running.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.PET_WIDTH, self.PET_HEIGHT))
            self.running_frames.append(frame)

        self.currentVisiableImg = self.idle_image.convert_alpha() # Ustawienie początkowego widocznego obrazka na idle

    def update(self, walking):
        """Aktualizuje animację zwierzątka w zależności od jego stanu ruchu.

        Jeśli zwierzątko się porusza (`walking` jest True), metoda cyklicznie
        przełącza klatki animacji biegania. W przeciwnym razie ustawia obrazek
        na stan spoczynku.

        :param walking: Flaga wskazująca, czy zwierzątko aktualnie się porusza.
                        Jeśli `True`, wyświetlana jest animacja biegania;
                        jeśli `False`, wyświetlany jest obrazek stanu spoczynku.
        :type walking: bool
        """
        if walking:
            self.animation_timer += self.animation_speed # Zwiększanie timera animacji
            if self.animation_timer >= 1:
                self.animation_timer = 0 # Resetowanie timera
                self.current_frame = (self.current_frame + 1) % len(self.running_frames) # Przejście do następnej klatki
            self.currentVisiableImg = self.running_frames[self.current_frame] # Ustawienie bieżącej klatki biegania
        else:
            self.currentVisiableImg = self.idle_image # Ustawienie obrazka stanu spoczynku

    def get_rect(self):
        """Zwraca obiekt `pygame.Rect` reprezentujący prostokąt kolizji zwierzątka.

        Prostokąt jest wyśrodkowany na aktualnej pozycji X i Y zwierzątka
        i ma rozmiar bieżąco wyświetlanego obrazka.

        :returns: Obiekt prostokąta PyGame, używany do wykrywania kolizji.
        :rtype: pygame.Rect
        """
        return pygame.Rect(self.currentVisiableImg.get_rect(center=(self.x, self.y)))

    def draw(self, screen):
        """Rysuje aktualnie wyświetlany obrazek zwierzątka na ekranie.

        Obrazek jest rysowany na swojej aktualnej pozycji (self.x, self.y),
        z uwzględnieniem jego środka.

        :param screen: Obiekt powierzchni PyGame, na której zwierzątko ma być narysowane.
        :type screen: pygame.Surface
        """
        screen.blit(self.currentVisiableImg,
                    (self.currentVisiableImg.get_rect(center=(self.x, self.y)).x,
                     self.currentVisiableImg.get_rect(center=(self.x, self.y)).y))

    def refresh(self):
        """Odświeża i ponownie ładuje wszystkie obrazy zwierzątka.

        Ta metoda jest przydatna, gdy rozmiar zwierzątka (PET_WIDTH, PET_HEIGHT)
        ulegnie zmianie (np. po zjedzeniu jedzenia), aby zapewnić, że wszystkie
        klatki animacji i obrazek idle są odpowiednio przeskalowane.
        Zachowuje również aktualny kierunek, w którym zwrócone jest zwierzątko.
        """
        # Ponowne ładowanie i skalowanie obrazka idle
        self.idle_image = pygame.transform.scale(pygame.image.load(f'assets/{self.petName}/Idle.png'), (self.PET_WIDTH, self.PET_HEIGHT)).convert_alpha()

        # Ponowne ładowanie i skalowanie klatek animacji biegania
        self.running_frames = []
        for i in range(self.amountOfFrames):
            frame = pygame.image.load(f'assets/{self.petName}/{str(i).zfill(2)}_Running.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.PET_WIDTH, self.PET_HEIGHT))
            if self.frameSide == "left": # Jeśli zwierzątko było skierowane w lewo, odwróć klatkę
                frame = pygame.transform.flip(frame, True, False).convert_alpha()
            self.running_frames.append(frame)

    def changeSide(self, pet_dx):
        """Zmienia kierunek, w którym zwierzątko jest zwrócone (lewo/prawo).

        Jeśli zwierzątko zmienia kierunek ruchu, ta metoda odwraca wszystkie
        klatki animacji biegania oraz bieżący widoczny obrazek, aby odzwierciedlić
        nowy kierunek.

        :param pet_dx: Kierunek ruchu zwierzątka. Dodatnia wartość oznacza ruch w prawo,
                       ujemna wartość oznacza ruch w lewo.
        :type pet_dx: int
        """
        # Zmiana z prawego na lewy
        if pet_dx < 0 and self.frameSide == "right":
            print("robie LEFT") # Debugging print
            # Odwracanie wszystkich klatek biegania
            for i in range(len(self.running_frames)):
                self.running_frames[i] = pygame.transform.flip(self.running_frames[i], True, False)
            # Odwracanie aktualnie widocznego obrazka
            self.currentVisiableImg = pygame.transform.flip(self.currentVisiableImg, True, False)
            self.frameSide = "left" # Zmiana stanu kierunku

        # Zmiana z lewego na prawy
        elif pet_dx > 0 and self.frameSide == "left":
            # Odwracanie wszystkich klatek biegania
            for i in range(len(self.running_frames)):
                self.running_frames[i] = pygame.transform.flip(self.running_frames[i], True, False)
            # Odwracanie aktualnie widocznego obrazka
            self.currentVisiableImg = pygame.transform.flip(self.currentVisiableImg, True, False)
            self.frameSide = "right" # Zmiana stanu kierunku