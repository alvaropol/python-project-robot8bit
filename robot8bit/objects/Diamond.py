import pygame

DIAMOND_SIZE = 30


class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/diamond.png'), (DIAMOND_SIZE, DIAMOND_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
