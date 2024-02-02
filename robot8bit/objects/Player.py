import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 720
PLAYER_SIZE = 50


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite, walls_group, waters_group, aqua_suits_group):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.health = 10
        self.has_suit = False
        self.is_wearing_suit = False
        self.score = 0
        self.walls_group = walls_group
        self.waters_group = waters_group
        self.aqua_suits_group = aqua_suits_group
        self.is_on_wall = False
        self.is_in_water = False
        self.last_water_position = None

    def update(self, dx, dy):
        next_x = self.rect.x + dx
        next_y = self.rect.y + dy

        for aqua_suit in pygame.sprite.spritecollide(self, self.aqua_suits_group, True):
            self.has_suit = True
            print("¡Has recogido un traje acuático!")

        for wall in self.walls_group:
            if wall.rect.collidepoint(next_x, next_y):
                self.health -= 1
                if self.health >= 0:
                    print("¡Te has chocado con un muro, acabas de perder 1 de vida! Vida restante:", self.health)
                return

        self.rect.x = min(max(next_x, 0), SCREEN_WIDTH - PLAYER_SIZE)
        self.rect.y = min(max(next_y, 0), SCREEN_HEIGHT - PLAYER_SIZE)

        for water in self.waters_group:
            if water.rect.collidepoint(self.rect.center):
                if not self.is_wearing_suit:
                    if not self.is_in_water or self.last_water_position != self.rect.topleft:
                        self.health -= 3
                        if self.health >= 0:
                            print("Estás en el agua sin el traje acuático, acabas de perder 3 de vida. Vida restante:",
                                  self.health)
                        self.is_in_water = True
                        self.last_water_position = self.rect.topleft
                return
        self.is_in_water = False

    def toggle_suit(self):
        if self.has_suit:
            self.is_wearing_suit = not self.is_wearing_suit
            if self.is_wearing_suit:
                self.image = pygame.transform.scale(pygame.image.load('../assets/player_front_aqua_suit.png'), (30, 30))
                print("Te has COLOCADO el traje acuático")
            else:
                self.image = pygame.transform.scale(pygame.image.load('../assets/player_front.png'), (30, 30))
                print("Te has QUITADO el traje acuático")