import pygame
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((800, 600))
sprite_not_scaled = pygame.image.load('../assets/robot.gif')
sprite = pygame.transform.scale(sprite_not_scaled, (30, 30))

pygame.display.set_caption("Robot8bit game")


class Robot:
    def __init__(self, sprite):
        self.position = [0, 0]
        self.sprite = sprite
        self.speed = 10
        self.size = [20, 20]
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def position_update(self):
        if self.moving_right:
            self.move_right()
        elif self.moving_left:
            self.move_left()
        elif self.moving_up:
            self.move_up()
        elif self.moving_down:
            self.move_down()


class Obstacle:
    def __init__(self):
        self.position = [100, 100]
        self.size = [20, 20]


robot = Robot(sprite)
obstacle = Obstacle()

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                robot.move_right()
            if event.key == pygame.K_LEFT:
                robot.move_left()
            if event.key == pygame.K_UP:
                robot.move_up()
            if event.key == pygame.K_DOWN:
                robot.move_down()
        if event.type == pygame.QUIT:
            game_running = False

    screen.fill((0, 0, 0))
    screen.blit(sprite, (robot.position[0], robot.position[1]))
    pygame.draw.rect(screen, (255, 0, 0),
                     (obstacle.position[0], obstacle.position[1], obstacle.size[0], obstacle.size[1]))

    pygame.display.flip()
    pygame.time.delay(10)
