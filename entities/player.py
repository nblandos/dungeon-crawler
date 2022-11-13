import pygame
from .entity import Entity


class Player(Entity):
    name = 'knight'
    speed = 500
    max_health = 100

    def __init__(self, game):
        Entity.__init__(self, game, self.name)
        self.rect = self.image.get_rect(center=(512 + 2.5 * 64, 400))
        self.hit_box_image = pygame.Surface((self.rect.width, self.rect.height))
        self.hit_box_image.fill((255, 0, 0))
        self.room = None

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = 'down'

        constant_dt = 0.016
        vel_up = [0, -self.speed * constant_dt]
        vel_up = [i * keys[pygame.K_w] for i in vel_up]
        vel_down = [0, self.speed * constant_dt]
        vel_down = [i * keys[pygame.K_s] for i in vel_down]
        vel_left = [-self.speed * constant_dt, 0]
        vel_left = [i * keys[pygame.K_a] for i in vel_left]
        vel_right = [self.speed * constant_dt, 0]
        vel_right = [i * keys[pygame.K_d] for i in vel_right]
        vel = zip(vel_up, vel_down, vel_left, vel_right)
        vel_list = [sum(item) for item in vel]

        x = (pow(vel_list[0], 2) + pow(vel_list[1], 2)) ** 0.5

        if 0 not in vel_list:
            z = x / (abs(vel_list[0]) + abs(vel_list[1]))
            vel_list_fixed = [item * z for item in vel_list]
            self.set_velocity(vel_list_fixed)
        else:
            self.set_velocity(vel_list)

    def draw(self, surface):
        surface.blit(self.hit_box_image, self.hit_box)
        surface.blit(self.image, self.rect)

    def update(self):
        self.wall_collision()
        self.basic_update()


