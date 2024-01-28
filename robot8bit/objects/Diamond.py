import pygame


PLAYER_SIZE = 50


class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE // 2, PLAYER_SIZE // 2])
        self.image.fill((200, 229, 235))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y