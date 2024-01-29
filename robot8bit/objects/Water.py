import pygame

WATER_SIZE = 50


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/water.jpg'), (WATER_SIZE, WATER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
