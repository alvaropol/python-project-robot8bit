import pygame

BOMB_SIZE = 30
PLAYER_SIZE = 50
WALL_SIZE = 50


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/bomb.png'), (BOMB_SIZE, BOMB_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def explode(self, walls_group, aqua_suits_group, player_x, player_y):
        bomb_x, bomb_y = self.rect.x, self.rect.y
        player_tile_x, player_tile_y = player_x // WALL_SIZE, player_y // WALL_SIZE

        adjacent_coords = [
            (player_tile_x, player_tile_y),
            (player_tile_x, player_tile_y - 1),
            (player_tile_x, player_tile_y + 1),
            (player_tile_x - 1, player_tile_y),
            (player_tile_x + 1, player_tile_y)
        ]

        for coord in adjacent_coords:
            tile_x, tile_y = coord
            for wall in walls_group.sprites():
                if wall.rect.collidepoint(tile_x * WALL_SIZE, tile_y * WALL_SIZE):
                    walls_group.remove(wall)
                    wall.kill()
                    break

        for coord in adjacent_coords:
            tile_x, tile_y = coord
            for aqua_suit in aqua_suits_group.sprites():
                if aqua_suit.rect.collidepoint(tile_x * WALL_SIZE, tile_y * WALL_SIZE):
                    aqua_suits_group.remove(aqua_suit)
                    aqua_suit.kill()
                    break
