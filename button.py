# button.py

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


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.value = start_val
        self.handle_width = 20
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                rel_x = max(self.rect.left, min(event.pos[0], self.rect.right))
                percent = (rel_x - self.rect.left) / self.rect.width
                self.value = self.min + percent * (self.max - self.min)

    def draw(self, surface):
        # Slider background
        pygame.draw.rect(surface, settings.GRAY, self.rect)
        # Slider fill
        fill_width = (self.value - self.min) / (self.max - self.min) * self.rect.width
        pygame.draw.rect(surface, settings.PINK, (self.rect.x, self.rect.y, fill_width, self.rect.height))
        # Handle
        pygame.draw.rect(surface, settings.WHITE, self.get_handle_rect())

    def get_handle_rect(self):
        percent = (self.value - self.min) / (self.max - self.min)
        handle_x = self.rect.left + percent * self.rect.width - self.handle_width / 2
        return pygame.Rect(handle_x, self.rect.y, self.handle_width, self.rect.height)
