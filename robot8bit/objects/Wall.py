import pygame

WALL_SIZE = 50


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/wall.jpg'), (WALL_SIZE, WALL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y