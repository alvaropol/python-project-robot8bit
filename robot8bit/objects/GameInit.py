import pygame

from objects.Bomb import Bomb
from objects.Diamond import Diamond
from objects.Player import Player
from objects.Wall import Wall
from objects.Water import Water

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SIZE = 50
WALL_SIZE = 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_background = pygame.transform.scale(pygame.image.load('../assets/grass.jpg'), (1280, 720))
pygame.display.set_caption("Robot Game")
sprite_not_scaled = pygame.image.load('../assets/player_front.png')
sprite_image = pygame.transform.scale(sprite_not_scaled, (30, 30))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
diamonds_group = pygame.sprite.Group()
bombs_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
waters_group = pygame.sprite.Group()


def load_map(filename):
    with open(filename, 'r') as f:
        map_info = f.readlines()
    return [line.strip() for line in map_info]


def generate_objects(map_info):
    diamonds = []
    bombs = []
    walls = []
    waters = []
    for y, row in enumerate(map_info):
        for x, tile in enumerate(row):
            if tile == 'D':
                diamonds.append((x * PLAYER_SIZE, y * PLAYER_SIZE))
            elif tile == 'B':
                bombs.append((x * PLAYER_SIZE, y * PLAYER_SIZE))
            elif tile == 'W':
                walls.append((x * WALL_SIZE, y * WALL_SIZE))
            elif tile == 'A':
                waters.append((x * WALL_SIZE, y * WALL_SIZE))
    return diamonds, bombs, walls, waters


map_info = load_map("../assets/map.txt")
diamonds_coords, bombs_coords, walls_coords, waters_coords = generate_objects(map_info)

pygame.init()

for coords in diamonds_coords:
    diamond = Diamond(*coords)
    diamonds_group.add(diamond)
    all_sprites.add(diamond)

for coords in bombs_coords:
    bomb = Bomb(*coords)
    bombs_group.add(bomb)
    all_sprites.add(bomb)

for coords in walls_coords:
    wall = Wall(*coords)
    walls_group.add(wall)
    all_sprites.add(wall)

for coords in waters_coords:
    water = Water(*coords)
    waters_group.add(water)
    all_sprites.add(water)

player = Player(sprite_image, walls_group, waters_group)
all_sprites.add(player)

dx, dy = 0, 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -PLAYER_SIZE
                player.image = pygame.transform.scale(pygame.image.load('../assets/player_up.png'), (30, 30))
            elif event.key == pygame.K_DOWN:
                dy = PLAYER_SIZE
                player.image = pygame.transform.scale(pygame.image.load('../assets/player_down.png'), (30, 30))
            elif event.key == pygame.K_LEFT:
                dx = -PLAYER_SIZE
                player.image = pygame.transform.scale(pygame.image.load('../assets/player_left.png'), (30, 30))
            elif event.key == pygame.K_RIGHT:
                dx = PLAYER_SIZE
                player.image = pygame.transform.scale(pygame.image.load('../assets/player_right.png'), (30, 30))
            elif event.key == pygame.K_b:
                if len(bombs_group) > 0:
                    bomb = bombs_group.sprites()[0]
                    bombs_group.remove(bomb)
                    all_sprites.remove(bomb)
                    print("¡Has denotado una bomba!.")
            elif event.key == pygame.K_t:
                player.has_suit = not player.has_suit
                print("Te has COLOCADO el traje acuático" if player.has_suit else "Te has QUITADO el traje acuático")
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                confirm_quit = input("¿Quieres salir del juego? (y/n): ")
                if confirm_quit.lower() == "y":
                    running = False

    player.update(dx, dy)
    dx, dy = 0, 0

    if player.health <= 0:
        print("¡Has perdido todos los puntos de vida, has muerto entre terribles sufrimientos!")
        running = False

    for diamond in pygame.sprite.spritecollide(player, diamonds_group, True):
        player.score += 1
        print("¡Has recogido un diamante! Diamantes en la mochila:", player.score)

    if len(diamonds_group) == 0:
        print("¡Enhorabuena has conseguido todos los diamantes, ahora es hora de venderlos!")
        running = False

    screen.blit(screen_background, screen_background.get_rect())
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
