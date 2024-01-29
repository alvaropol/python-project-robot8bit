import pygame

BOMB_SIZE = 30


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/bomb.png'), (BOMB_SIZE, BOMB_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
