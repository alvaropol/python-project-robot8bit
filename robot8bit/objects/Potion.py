import pygame
import random

POTION_SIZE = 30


class Potion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/potion.png'), (POTION_SIZE, POTION_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.healing_points = random.randint(1, 5)
