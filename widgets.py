# widgets.py

import pygame

import settings
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = settings.GRAY if self.rect.collidepoint(mouse_pos) else settings.PINK
        pygame.draw.rect(surface, color, self.rect)

        text_surf = self.font.render(self.text, True, settings.BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def center(self, offset_x=0, offset_y=0):
        self.rect.centerx = settings.WIDTH // 2 + offset_x
        self.rect.centery = settings.HEIGHT // 2 + offset_y

class Bar:
    def __init__(self, x, y, width, height, max):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ratio = max
        self.max = max
        self.color1 = "red"
        self.color2 = "green"


    def draw(self, surface):
        ratio = self.ratio / self.max
        pygame.draw.rect(surface, self.color1, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color2, (self.x, self.y, self.width * ratio, self.height))