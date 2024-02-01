import pygame
from pygame import mixer

from objects.AquaSuit import AquaSuit
from objects.Bomb import Bomb
from objects.Diamond import Diamond
from objects.Map import Map
from objects.Player import Player
from objects.Wall import Wall
from objects.Water import Water


class Game:

    @staticmethod
    def run():
        screen_width = 1280
        screen_height = 720
        player_size = 50
        screen = pygame.display.set_mode((screen_width, screen_height))
        screen_background = pygame.transform.scale(pygame.image.load('../assets/grass.jpg'), (1280, 720))
        pygame.display.set_caption("Robot Game")
        sprite_not_scaled = pygame.image.load('../assets/player_front.png')
        sprite_image = pygame.transform.scale(sprite_not_scaled, (30, 30))
        mixer.init()
        mixer.music.load('../assets/music.wav')
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)
        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        diamonds_group = pygame.sprite.Group()
        bombs_group = pygame.sprite.Group()
        walls_group = pygame.sprite.Group()
        waters_group = pygame.sprite.Group()
        aqua_suits_group = pygame.sprite.Group()
        map_info = Map.load_map("../assets/map.txt")
        diamond_icon = pygame.transform.scale(pygame.image.load('../assets/diamond.png'), (30, 30))
        bomb_icon = pygame.transform.scale(pygame.image.load('../assets/bomb.png'), (30, 30))
        heart_icon = pygame.image.load('../assets/heart.png')
        inventory_bg = pygame.transform.scale(pygame.image.load('../assets/inventory_bg.png'), (90, 40))
        aqua_suit_icon = pygame.transform.scale(pygame.image.load('../assets/aqua_suit.png'), (30, 30))

        pygame.init()

        for y, row in enumerate(map_info[1:]):
            for x, tile in enumerate(row):
                if tile == 'W':
                    wall = Wall(x * player_size, y * player_size)
                    walls_group.add(wall)
                    all_sprites.add(wall)
                elif tile == 'A':
                    water = Water(x * player_size, y * player_size)
                    waters_group.add(water)
                    all_sprites.add(water)

        diamonds_coords, bombs_coords, _, _, aqua_suits_coords = Map.generate_objects(map_info)

        for coords in diamonds_coords:
            diamond = Diamond(*coords)
            diamonds_group.add(diamond)
            all_sprites.add(diamond)

        for coords in bombs_coords:
            bomb = Bomb(*coords)
            bombs_group.add(bomb)
            all_sprites.add(bomb)

        for coords in aqua_suits_coords:
            aqua_suit = AquaSuit(*coords)
            aqua_suits_group.add(aqua_suit)
            all_sprites.add(aqua_suit)

        player = Player(sprite_image, walls_group, waters_group, aqua_suits_group)
        all_sprites.add(player)
        dx, dy = 0, 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        dy = -player_size
                        player.image = pygame.transform.scale(pygame.image.load('../assets/player_up.png'), (30, 30))
                    elif event.key == pygame.K_DOWN:
                        dy = player_size
                        player.image = pygame.transform.scale(pygame.image.load('../assets/player_down.png'), (30, 30))
                    elif event.key == pygame.K_LEFT:
                        dx = -player_size
                        player.image = pygame.transform.scale(pygame.image.load('../assets/player_left.png'), (30, 30))
                    elif event.key == pygame.K_RIGHT:
                        dx = player_size
                        player.image = pygame.transform.scale(pygame.image.load('../assets/player_right.png'), (30, 30))
                    elif event.key == pygame.K_b:
                        if len(bombs_group) > 0:
                            bomb = bombs_group.sprites()[0]
                            bombs_group.remove(bomb)
                            all_sprites.remove(bomb)
                            print("¡Has denotado una bomba!.")
                    elif event.key == pygame.K_t:
                        if player.has_suit:
                            player.toggle_suit()
                        else:
                            print("No tienes ningún traje acuático para equipar")
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

            font = pygame.font.Font(None, 36)

            screen.blit(heart_icon, (10, 10))
            heart_text = font.render(f"x {player.health}", True, (255, 255, 255))
            screen.blit(heart_text, (60, 10))

            screen.blit(diamond_icon, (120, 10))
            diamond_text = font.render(f"x {player.score}", True, (255, 255, 255))
            screen.blit(diamond_text, (170, 10))

            screen.blit(bomb_icon, (230, 10))
            bomb_text = font.render(f"x {bombs_group.__len__()}", True, (255, 255, 255))
            screen.blit(bomb_text, (280, 10))

            screen.blit(inventory_bg, (1180, 3))
            screen.blit(font.render("T", True, (0, 0, 0)), (1196, 12))
            screen.blit(aqua_suit_icon, (1233, 8))

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
