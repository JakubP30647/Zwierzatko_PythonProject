import random
import sys
import pygame.transform
from gif_pygame import gif_pygame

import utils
from PetEntity import PetEntity
from PropEntity import PropEntity
from game_over_screen import game_over_screen
from widgets import *


def gameplay_screen(screen):
    """Główna pętla ekranu rozgrywki, gdzie odbywa się interakcja z wirtualnym zwierzątkiem.

    Funkcja inicjalizuje wszystkie niezbędne zasoby gry, takie jak czcionki, obrazy,
    obiekty zwierzątka i interfejsu użytkownika. Zarządza główną logiką gry,
    w tym poruszaniem się zwierzątka, reakcjami na interakcje gracza (karmienie, głaskanie),
    aktualizacją wskaźników głodu i zabawy, wykrywaniem kolizji oraz przejściem
    do ekranu końca gry w przypadku przegranej. Pętla gry działa z szybkością 60 klatek na sekundę.

    :param screen: Obiekt powierzchni PyGame (pygame.Surface), na którym odbywa się cała rozgrywka.
                   Jest to główna powierzchnia, na której renderowane są wszystkie elementy wizualne gry,
                   w tym tło, zwierzątko, obiekty interaktywne (jedzenie, serca) oraz paski stanu
                   i przyciski.
    :type screen: pygame.Surface

    :returns: Ciąg znaków określający następny stan gry ("main_menu" do powrotu do menu głównego,
              "quit" do zakończenia aplikacji).
    :rtype: str
    """
    utils.foodInstall() # Upewnia się, że lista jedzenia jest załadowana

    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.037)) # Inicjalizacja czcionki dla tekstu w grze

    loveImg = pygame.image.load('assets/love.png') # Ładowanie obrazka symbolizującego miłość/szczęście
    loveList = [] # Lista przechowująca obiekty "serc" pojawiające się po głaskaniu

    foodImg = utils.foodList[random.randint(0, len(utils.foodList) - 1)] # Wybór losowego obrazka jedzenia
    foodList = [] # Lista przechowująca obiekty "jedzenia"

    deathGif = gif_pygame.load('assets/death.gif') # Ładowanie animacji GIF przedstawiającej śmierć zwierzątka

    pet = PetEntity(WIDTH * 0.5, HEIGHT * 0.5) # Inicjalizacja obiektu wirtualnego zwierzątka na środku ekranu

    # Inicjalizacja przycisków interfejsu użytkownika
    back_button = Button(WIDTH * 0.8, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "BACK", font)
    petButton = Button(WIDTH * 0.20, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "PET", font)
    foodButton = Button(WIDTH * 0.40, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "Feed", font)

    # Inicjalizacja paska zabawy (funBar)
    funBar = Bar(WIDTH * 0.005, HEIGHT * 0.02, WIDTH * 0.15, HEIGHT * 0.05, 100)
    funBar.ratio = utils.FUN # Początkowy poziom zabawy
    funBar.color1 = GRAY
    funBar.color2 = GREEN

    # Inicjalizacja paska jedzenia (foodBar)
    foodBar = Bar(WIDTH * 0.005, HEIGHT * 0.10, WIDTH * 0.15, HEIGHT * 0.05, 100)
    foodBar.ratio = utils.FOOD # Początkowy poziom jedzenia
    foodBar.color1 = GRAY
    foodBar.color2 = BLUE

    # Ładowanie i skalowanie tła gry
    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Zmienne kontrolujące spadki statystyk
    last_drop_time_fun = 0
    last_drop_time_food = 0

    # Zmienne kontrolujące ruch zwierzątka
    pet_dx = 1 # Kierunek ruchu zwierzątka (1 dla prawo, -1 dla lewo)
    last_direction_change = pygame.time.get_ticks() # Czas ostatniej zmiany kierunku
    last_standing = pygame.time.get_ticks() # Czas ostatniego postoju/ruchu
    direction_change_interval = 6000 # Interwał zmiany kierunku (6 sekund)
    timeOfStand = 3000 # Czas postoju/ruchu (3 sekundy)
    walking = False # Czy zwierzątko aktualnie się porusza
    clock = pygame.time.Clock() # Obiekt zegara PyGame do kontroli FPS
    running = True # Flaga kontrolująca główną pętlę gry


    death_animation_start_time = None # Czas rozpoczęcia animacji śmierci
    DEATH_ANIMATION_DURATION = 3000 # Czas trwania animacji śmierci (3 sekundy)

    while running:
        screen.blit(background, (0, 0)) # Rysowanie tła
        clock.tick(60) # Ograniczenie klatek na sekundę do 60
        currentTime = pygame.time.get_ticks() # Aktualny czas w milisekundach

        standingTimer = pygame.time.get_ticks() # Aktualny czas do kontroli postoju/ruchu

        # Logika zmiany kierunku ruchu zwierzątka
        if currentTime - last_direction_change > direction_change_interval:
            pet_dx = random.choice([-1, 1]) # Losowa zmiana kierunku
            pet.changeSide(pet_dx) # Zmiana strony wyświetlanego zwierzątka
            last_direction_change = currentTime

        # Logika przełączania między chodzeniem a staniem
        if standingTimer - last_standing > timeOfStand:
            walking = not walking # Zmiana stanu chodzenia
            last_standing = standingTimer

        # Aktualizacja pozycji zwierzątka, jeśli idzie
        if walking:
            if pet_dx > 0 and pet.x < WIDTH * 0.8: # Ruch w prawo z ograniczeniem
                pet.x += pet_dx
            if pet_dx < 0 and pet.x > WIDTH * 0.2: # Ruch w lewo z ograniczeniem
                pet.x += pet_dx

        pet.update(walking) # Aktualizacja animacji zwierzątka

        # Obsługa obiektów "serc" (efekt głaskania)
        for heart in loveList[:]: # Iteracja po kopii listy, aby umożliwić usuwanie elementów
            heart.move_towards(pet.x, pet.y) # Serce porusza się w kierunku zwierzątka
            if pet.get_rect().colliderect(heart.get_rect()): # Wykrywanie kolizji serca ze zwierzątkiem
                loveList.remove(heart) # Usunięcie serca po kolizji
            else:
                heart.draw(screen) # Rysowanie serca

        # Obsługa obiektów "jedzenia"
        for food in foodList[:]: # Iteracja po kopii listy
            food.move_towards(pet.x, pet.y) # Jedzenie porusza się w kierunku zwierzątka
            if pet.get_rect().colliderect(food.get_rect()): # Wykrywanie kolizji jedzenia ze zwierzątkiem
                if pet.PET_WIDTH <= WIDTH * 0.31: # Sprawdzenie, czy zwierzątko nie jest za duże
                    pet.PET_HEIGHT += 2 # Zwiększenie rozmiaru zwierzątka po zjedzeniu
                    pet.PET_WIDTH += 3
                pet.refresh() # Odświeżenie stanu zwierzątka (np. obrazka)
                foodList.remove(food) # Usunięcie jedzenia po zjedzeniu
            else:
                food.draw(screen) # Rysowanie jedzenia

        # Logika spadku wskaźników zabawy i głodu
        if currentTime - last_drop_time_fun > 1000: # Co sekundę spada zabawa
            funBar.ratio -= 1
            last_drop_time_fun = currentTime

        if currentTime - last_drop_time_food > 750: # Co 0.75 sekundy spada głód
            foodBar.ratio -= 1
            last_drop_time_food = currentTime



        if funBar.ratio < 1 or foodBar.ratio < 1:
            game_over_screen(screen, font)  # Przejście do ekranu końca gry
            return "main_menu"  # Powrót do menu głównego



        # Rysowanie pasków stanu i przycisków
        funBar.draw(screen)
        foodBar.draw(screen)
        petButton.draw(screen)
        foodButton.draw(screen)
        back_button.draw(screen)

        pet.draw(screen) # Rysowanie zwierzątka

        # Logika animacji śmierci i przejścia do ekranu końca gry
        if pet.PET_WIDTH > WIDTH * 0.3: # Warunek śmierci (zwierzątko zbyt duże)
            if death_animation_start_time is None:
                death_animation_start_time = pygame.time.get_ticks() # Rozpoczęcie animacji śmierci

            if pygame.time.get_ticks() - death_animation_start_time < DEATH_ANIMATION_DURATION:
                deathGif.render(screen, # Wyświetlanie animacji śmierci
                                (
                                    (pet.currentVisiableImg.get_rect(center=(pet.x, pet.y)).x ),
                                    (pet.currentVisiableImg.get_rect(center=(pet.x, pet.y)).y) )
                                )
            else:
                death_animation_start_time = None # Zresetowanie timera animacji
                game_over_screen(screen, font) # Przejście do ekranu końca gry
                return "main_menu" # Powrót do menu głównego

        else:
            death_animation_start_time = None # Resetowanie timera animacji śmierci, jeśli zwierzątko nie umiera

        # Obsługa zdarzeń PyGame (kliknięcia myszy, naciśnięcia klawiszy, zamknięcie okna)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Zamknięcie okna
                running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN: # Kliknięcie myszy
                if back_button.is_clicked(event.pos): # Kliknięcie przycisku "BACK"
                    return "main_menu"
                if petButton.is_clicked(event.pos): # Kliknięcie przycisku "PET"
                    riseRatio(funBar) # Zwiększenie paska zabawy
                    loveList.append( # Dodanie serca
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            loveImg
                        )
                    )
                if foodButton.is_clicked(event.pos): # Kliknięcie przycisku "Feed"
                    foodList.append( # Dodanie jedzenia
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            pygame.transform.scale(utils.foodList[random.randint(0, len(utils.foodList) - 1)],
                                                   (WIDTH * 0.05, HEIGHT * 0.08)).convert_alpha()
                        )
                    )
                    riseRatio(foodBar) # Zwiększenie paska głodu

            elif event.type == pygame.KEYDOWN: # Naciśnięcie klawisza
                if event.key == pygame.K_ESCAPE: # Klawisz ESC
                    return "main_menu"
                if event.key == pygame.K_SPACE: # Klawisz SPACJA
                    riseRatio(funBar)
                    loveList.append(
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            loveImg
                        )
                    )
                if event.key == pygame.K_e: # Klawisz 'E'
                    riseRatio(foodBar)
                    foodList.append(
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            pygame.transform.scale(utils.foodList[random.randint(0, len(utils.foodList) - 1)],
                                                   (WIDTH * 0.05, HEIGHT * 0.08)).convert_alpha()
                        )
                    )

        pygame.display.flip() # Odświeżenie ekranu

    pygame.quit() # Zamknięcie PyGame
    sys.exit() # Zakończenie aplikacji


def riseRatio(bar):
    """Zwiększa wartość proporcji paska stanu (np. zabawy lub jedzenia).

    Funkcja bezpiecznie zwiększa wartość `ratio` obiektu paska (`Bar`).
    Jeśli aktualna wartość `ratio` jest mniejsza niż 90, zostaje zwiększona o 10.
    W przeciwnym wypadku, zostaje zwiększona do maksymalnej wartości 100,
    zapobiegając przekroczeniu limitu.

    :param bar: Obiekt paska stanu, który ma zostać zmodyfikowany. Oczekuje, że obiekt
                posiada atrybut `ratio` (liczbę całkowitą lub zmiennoprzecinkową),
                który będzie reprezentował bieżący poziom paska.
    :type bar: Bar
    """
    if bar.ratio < 90:
        bar.ratio += 10
    else:
        bar.ratio += 100 - bar.ratio