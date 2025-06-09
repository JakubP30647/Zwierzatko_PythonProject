import os

import pygame

from settings import HEIGHT

FUN = 50
FOOD = 50
SYSTEMpet = "rabbit"
SYSTEMamountOfFrame = 7

font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.037))

def set_pet_data(pet_name, frame_count):
    global SYSTEMpet
    global SYSTEMamountOfFrame
    SYSTEMpet = pet_name
    SYSTEMamountOfFrame = frame_count

foodList = []

def foodInstall():
    for filename in os.listdir('assets/food'):
        if filename.lower().endswith(".png"):
            full_path = os.path.join('assets/food', filename)
            try:
                image = pygame.image.load(full_path).convert_alpha()
                foodList.append(image)

            except pygame.error as e:
                print(f"Could not load {filename}: {e}")
