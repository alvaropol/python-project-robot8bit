import pygame

AQUA_SUIT_SIZE = 30


class AquaSuit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/aqua_suit.png'),
                                            (AQUA_SUIT_SIZE, AQUA_SUIT_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
