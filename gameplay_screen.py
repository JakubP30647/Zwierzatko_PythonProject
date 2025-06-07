import random
import sys
import pygame.transform

import utils
from settings import *
from utils import FUN
from widgets import *

# Stałe dla rozmiaru królika
PET_WIDTH = int(WIDTH * 0.05)
PET_HEIGHT = int(HEIGHT * 0.08)


def gameplay_screen(screen):
    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.037))

    loveImg = pygame.image.load('assets/love.png')
    loveList = []

    petImg = pygame.image.load('assets/rabbit/Idle.png')
    pet = PetEntity(WIDTH * 0.5, HEIGHT * 0.5, petImg)

    back_button = Button(WIDTH * 0.8, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "BACK", font)
    petButton = Button(WIDTH * 0.20, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "PET", font)
    foodButton = Button(WIDTH * 0.40, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "Feed", font)

    funBar = Bar(WIDTH * 0.005, HEIGHT * 0.02, WIDTH * 0.15, HEIGHT * 0.05, 100)
    funBar.ratio = utils.FUN
    funBar.color1 = GRAY
    funBar.color2 = GREEN

    foodBar = Bar(WIDTH * 0.005, HEIGHT * 0.10, WIDTH * 0.15, HEIGHT * 0.05, 100)
    foodBar.ratio = utils.FOOD
    foodBar.color1 = GRAY
    foodBar.color2 = BLUE

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    last_drop_time_fun = 0
    last_drop_time_food = 0

    pet_dx = 1
    last_direction_change = pygame.time.get_ticks()
    last_standing = pygame.time.get_ticks()
    direction_change_interval = 6000
    timeOfStand = 5000
    walking = False
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background, (0, 0))
        clock.tick(60)
        currentTime = pygame.time.get_ticks()

        standingTimer = pygame.time.get_ticks()

        if funBar.ratio < 1 or foodBar.ratio < 1:
            print("KONIEC GRY")

        if currentTime - last_direction_change > direction_change_interval:
            pet_dx = random.choice([-1, 1])
            last_direction_change = currentTime

        if standingTimer - last_standing > timeOfStand:
            walking = not walking
            last_standing = standingTimer

        if walking:
            if pet_dx > 0 and pet.x < WIDTH * 0.8:
                pet.x += pet_dx
            if pet_dx < 0 and pet.x > WIDTH * 0.2:
                pet.x += pet_dx

        for heart in loveList[:]:
            heart.move_towards(pet.x, pet.y)
            if pet.get_rect().colliderect(heart.get_rect()):
                loveList.remove(heart)
            else:
                heart.draw(screen)

        if currentTime - last_drop_time_fun > 1000:
            funBar.ratio -= 1

            last_drop_time_fun = currentTime

        if currentTime - last_drop_time_food > 750:
            foodBar.ratio -= 1
            last_drop_time_food = currentTime

        funBar.draw(screen)
        foodBar.draw(screen)

        petButton.draw(screen)
        foodButton.draw(screen)
        back_button.draw(screen)

        pet.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return "main_menu"
                if petButton.is_clicked(event.pos):
                    riseRatio(funBar)
                    loveList.append(
                        LoveEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            loveImg
                        )
                    )
                if foodButton.is_clicked(event.pos):
                    riseRatio(foodBar)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"
                if event.key == pygame.K_SPACE:
                    riseRatio(funBar)
                    loveList.append(
                        LoveEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            loveImg
                        )
                    )
                if event.key == pygame.K_e:
                    riseRatio(foodBar)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def riseRatio(bar):
    if bar.ratio < 90:
        bar.ratio += 10
    else:
        bar.ratio += 100 - bar.ratio


class LoveEntity:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.speed = 3

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.image.get_rect(center=(self.x, self.y)))

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance != 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed


class PetEntity:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y

        self.image = pygame.transform.scale(image, (PET_WIDTH, PET_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.image.get_rect(center=(self.x, self.y)))

    def draw(self, screen):
        screen.blit(self.image,
                    (self.image.get_rect(center=(self.x, self.y)).x, self.image.get_rect(center=(self.x, self.y)).y))
