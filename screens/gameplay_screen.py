import random
import sys
import pygame.transform
from gif_pygame import gif_pygame

import utils
from PetsAndUtilities.PetEntity import PetEntity
from PetsAndUtilities.PropEntity import PropEntity
from screens.game_over_screen import game_over_screen
from settings import *
from utils import FUN
from widgets import *


def gameplay_screen(screen):

    utils.foodInstall()

    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.037))

    loveImg = pygame.image.load('assets/love.png')
    loveList = []

    foodImg = utils.foodList[random.randint(0, len(utils.foodList) - 1)]
    foodList = []

    deathGif = gif_pygame.load('assets/death.gif')

    pet = PetEntity(WIDTH * 0.5, HEIGHT * 0.5)

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
    timeOfStand = 3000
    walking = False
    clock = pygame.time.Clock()
    running = True


    death_animation_start_time = None
    DEATH_ANIMATION_DURATION = 3000

    while running:
        screen.blit(background, (0, 0))
        clock.tick(60)
        currentTime = pygame.time.get_ticks()

        standingTimer = pygame.time.get_ticks()




        if currentTime - last_direction_change > direction_change_interval:
            pet_dx = random.choice([-1, 1])

            pet.changeSide(pet_dx)

            last_direction_change = currentTime

        if standingTimer - last_standing > timeOfStand:
            walking = not walking
            last_standing = standingTimer

        if walking:
            if pet_dx > 0 and pet.x < WIDTH * 0.8:
                pet.x += pet_dx
            if pet_dx < 0 and pet.x > WIDTH * 0.2:
                pet.x += pet_dx

        pet.update(walking)

        for heart in loveList[:]:
            heart.move_towards(pet.x, pet.y)
            if pet.get_rect().colliderect(heart.get_rect()):
                loveList.remove(heart)

            else:
                heart.draw(screen)

        for food in foodList[:]:
            food.move_towards(pet.x, pet.y)
            if pet.get_rect().colliderect(food.get_rect()):

                if pet.PET_WIDTH <= WIDTH * 0.31:
                    pet.PET_HEIGHT += 2
                    pet.PET_WIDTH += 3

                pet.refresh()
                foodList.remove(food)

            else:
                food.draw(screen)


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

        if pet.PET_WIDTH > WIDTH * 0.3:
            if death_animation_start_time is None:
                death_animation_start_time = pygame.time.get_ticks()

            if pygame.time.get_ticks() - death_animation_start_time < DEATH_ANIMATION_DURATION:
                deathGif.render(screen,
                                (
                                    (pet.currentVisiableImg.get_rect(center=(pet.x, pet.y)).x ),
                                    (pet.currentVisiableImg.get_rect(center=(pet.x, pet.y)).y) )
                                )
            else:
                death_animation_start_time = None
                game_over_screen(screen, font)
                return "main_menu"
        else:

            death_animation_start_time = None

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
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            loveImg
                        )
                    )
                if foodButton.is_clicked(event.pos):
                    foodList.append(
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            pygame.transform.scale(utils.foodList[random.randint(0, len(utils.foodList) - 1)],
                                                   (WIDTH * 0.05, HEIGHT * 0.08)).convert_alpha()
                        )
                    )

                    riseRatio(foodBar)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"
                if event.key == pygame.K_SPACE:
                    riseRatio(funBar)
                    loveList.append(
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            loveImg
                        )
                    )
                if event.key == pygame.K_e:
                    riseRatio(foodBar)
                    foodList.append(
                        PropEntity(
                            random.randint(0, int(WIDTH * 0.99)),
                            random.randint(0, int(HEIGHT * 0.99)),
                            pygame.transform.scale(utils.foodList[random.randint(0, len(utils.foodList) - 1)],
                                                   (WIDTH * 0.05, HEIGHT * 0.08)).convert_alpha()
                        )
                    )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def riseRatio(bar):
    if bar.ratio < 90:
        bar.ratio += 10
    else:
        bar.ratio += 100 - bar.ratio