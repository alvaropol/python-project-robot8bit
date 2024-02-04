import pygame
from pygame import mixer

from objects.AquaSuit import AquaSuit
from objects.Bomb import Bomb
from objects.Diamond import Diamond
from objects.Map import Map
from objects.Player import Player
from objects.Potion import Potion
from objects.Wall import Wall
from objects.Water import Water

pygame.init()


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
        bombs_collected = []
        walls_group = pygame.sprite.Group()
        waters_group = pygame.sprite.Group()
        aqua_suits_group = pygame.sprite.Group()
        potions_group = pygame.sprite.Group()
        map_info = Map.load_map("../assets/map.txt")
        diamond_icon = pygame.transform.scale(pygame.image.load('../assets/diamond.png'), (30, 30))
        bomb_icon = pygame.transform.scale(pygame.image.load('../assets/bomb.png'), (30, 30))
        heart_icon = pygame.image.load('../assets/heart.png')
        inventory_bg = pygame.transform.scale(pygame.image.load('../assets/inventory_bg.png'), (90, 40))
        aqua_suit_icon = pygame.transform.scale(pygame.image.load('../assets/aqua_suit.png'), (30, 30))
        potion_icon = pygame.transform.scale(pygame.image.load('../assets/potion.png'), (30, 30))

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

        diamonds_coords, bombs_coords, potions_coords, _, aqua_suits_coords = Map.generate_objects(map_info)

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

        for coords in potions_coords:
            potion = Potion(*coords)
            potions_group.add(potion)
            all_sprites.add(potion)

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
                        if player.is_wearing_suit:
                            player.image = pygame.transform.scale(
                                pygame.image.load('../assets/player_up_aqua_suit.png'),
                                (30, 30))
                        else:
                            player.image = pygame.transform.scale(pygame.image.load('../assets/player_up.png'),
                                                                  (30, 30))
                    elif event.key == pygame.K_DOWN:
                        dy = player_size
                        if player.is_wearing_suit:
                            player.image = pygame.transform.scale(
                                pygame.image.load('../assets/player_down_aqua_suit.png'),
                                (30, 30))
                        else:
                            player.image = pygame.transform.scale(pygame.image.load('../assets/player_down.png'),
                                                                  (30, 30))
                    elif event.key == pygame.K_LEFT:
                        dx = -player_size
                        if player.is_wearing_suit:
                            player.image = pygame.transform.scale(
                                pygame.image.load('../assets/player_left_aqua_suit.png'),
                                (30, 30))
                        else:
                            player.image = pygame.transform.scale(pygame.image.load('../assets/player_left.png'),
                                                                  (30, 30))
                    elif event.key == pygame.K_RIGHT:
                        dx = player_size
                        if player.is_wearing_suit:
                            player.image = pygame.transform.scale(
                                pygame.image.load('../assets/player_right_aqua_suit.png'),
                                (30, 30))
                        else:
                            player.image = pygame.transform.scale(pygame.image.load('../assets/player_right.png'),
                                                                  (30, 30))
                    if event.key == pygame.K_b:
                        if bombs_collected:
                            bomb = bombs_collected.pop(0)
                            bomb.explode(walls_group, aqua_suits_group, player.rect.x, player.rect.y)
                            bombs_group.remove(bomb)
                            print("¡BOOOM! HAS EXPLOTADO UNA BOMBA")
                        else:
                            print("No tienes ninguna bomba para explotar")
                    elif event.key == pygame.K_t:
                        if player.has_suit:
                            player.toggle_suit()
                        else:
                            print("No tienes ningún traje acuático para equipar")
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        exit_screen(screen, screen_width, screen_height)
                        confirm_quit = waiting_response()
                        if confirm_quit.lower() == "y":
                            running = False
            for bomb in pygame.sprite.spritecollide(player, bombs_group, True):
                print("Has recogido una bomba")
                bombs_collected.append(bomb)

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

            for potion in pygame.sprite.spritecollide(player, potions_group, False):
                if player.health < 10:
                    player.health += potion.healing_points
                    if player.health > 10:
                        player.health = 10
                    print(f"¡Te has tomado una poción de {potion.healing_points} de vida! Vida: {player.health}")
                    potion.kill()

            screen.blit(screen_background, screen_background.get_rect())
            all_sprites.draw(screen)

            font = pygame.font.Font(None, 36)

            screen.blit(heart_icon, (10, 10))
            heart_text = font.render(f"x {player.health}", True, (255, 255, 255))
            screen.blit(heart_text, (60, 10))

            screen.blit(diamond_icon, (170, 10))
            diamond_text = font.render(f"x {diamonds_group.__len__()}", True, (255, 255, 255))
            screen.blit(diamond_text, (220, 10))

            screen.blit(bomb_icon, (280, 10))
            bomb_text = font.render(f"x {bombs_group.__len__()}", True, (255, 255, 255))
            screen.blit(bomb_text, (330, 10))

            screen.blit(aqua_suit_icon, (390, 10))
            aqua_suit_text = font.render(f"x {aqua_suits_group.__len__()}", True, (255, 255, 255))
            screen.blit(aqua_suit_text, (440, 10))

            screen.blit(potion_icon, (500, 8))
            potion_text = font.render(f"x {potions_group.__len__()}", True, (255, 255, 255))
            screen.blit(potion_text, (550, 10))

            screen.blit(inventory_bg, (920, 3))
            screen.blit(font.render(f"{player.score}", True, (0, 0, 0)), (936, 12))
            screen.blit(diamond_icon, (972, 8))

            screen.blit(inventory_bg, (1050, 3))
            screen.blit(font.render(f"{bombs_collected.__len__()}", True, (0, 0, 0)), (1066, 12))
            screen.blit(bomb_icon, (1104, 8))

            screen.blit(inventory_bg, (1180, 3))
            screen.blit(font.render("T", True, (0, 0, 0)), (1196, 12))

            if player.has_suit:
                screen.blit(aqua_suit_icon, (1233, 8))

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


def exit_screen(screen, screen_width, screen_height):
    font = pygame.font.Font(None, 36)
    confirm_text = font.render("¿Quieres salir del juego? (Y:SÍ / N:NO)", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(confirm_text,
                ((screen_width - confirm_text.get_width()) // 2, (screen_height - confirm_text.get_height()) // 2))
    pygame.display.flip()


def waiting_response():
    response = True
    while response:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting_confirmation = False
                    return "y"
                elif event.key == pygame.K_n:
                    waiting_confirmation = False
                    return "n"
        pygame.time.Clock().tick(30)
