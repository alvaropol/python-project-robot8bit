import pygame

DIAMOND_SIZE = 25


class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/diamond.png'), (DIAMOND_SIZE, DIAMOND_SIZE))
        self.image.fill((200, 229, 235))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
