import pygame

from settings import WIDTH, HEIGHT
import utils


class PetEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.amountOfFrames = utils.SYSTEMamountOfFrame
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.frameSide = "right"
        self.petName = utils.SYSTEMpet
        self.PET_WIDTH = int(WIDTH * 0.05)
        self.PET_HEIGHT = int(HEIGHT * 0.08)
        self.idle_image = pygame.transform.scale(pygame.image.load(f'assets/{self.petName}/Idle.png'), (self.PET_WIDTH, self.PET_HEIGHT)).convert_alpha()

        self.running_frames = []
        for i in range(0,self.amountOfFrames):
            frame = pygame.image.load(f'assets/{self.petName}/{str(i).zfill(2)}_Running.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.PET_WIDTH, self.PET_HEIGHT))
            self.running_frames.append(frame)

        self.currentVisiableImg = self.idle_image.convert_alpha()

    def update(self, walking):


        if walking:

            self.animation_timer += self.animation_speed

            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.running_frames)
            self.currentVisiableImg = self.running_frames[self.current_frame]
        else:
            self.currentVisiableImg = self.idle_image

    def get_rect(self):
        return pygame.Rect(self.currentVisiableImg.get_rect(center=(self.x, self.y)))

    def draw(self, screen):

        screen.blit(self.currentVisiableImg,
                    (self.currentVisiableImg.get_rect(center=(self.x, self.y)).x,
                     self.currentVisiableImg.get_rect(center=(self.x, self.y)).y))

    def refresh(self):
        self.idle_image = pygame.transform.scale(pygame.image.load(f'assets/{self.petName}/Idle.png'), (self.PET_WIDTH, self.PET_HEIGHT))

        self.running_frames = []
        for i in range(self.amountOfFrames):
            frame = pygame.image.load(f'assets/{self.petName}/{str(i).zfill(2)}_Running.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.PET_WIDTH, self.PET_HEIGHT))
            if self.frameSide == "left":
                frame = pygame.transform.flip(frame, True, False).convert_alpha()
            self.running_frames.append(frame)

    def changeSide(self, pet_dx):
        if pet_dx < 0 and self.frameSide == "right":
            print("robie LEFT")
            for i in range(len(self.running_frames)):
                self.running_frames[i] = pygame.transform.flip(self.running_frames[i], True, False)
            self.currentVisiableImg = pygame.transform.flip(self.currentVisiableImg, True, False)
            self.frameSide = "left"

        elif pet_dx > 0 and self.frameSide == "left":
            for i in range(len(self.running_frames)):
                self.running_frames[i] = pygame.transform.flip(self.running_frames[i], True, False)
            self.currentVisiableImg = pygame.transform.flip(self.currentVisiableImg, True, False)
            self.frameSide = "right"
