import pygame
from settings import *


class Bullet:
    def __init__(self, game, room, user, x, y, target_pos):
        self.game = game
        self.room = room
        self.user = user
        self.image = None
        self.rect = None
        self.load_image()
        self.rect.x = x
        self.rect.y = y
        self.direction = None

    def load_image(self):
        self.image = pygame.Surface(self.hit_box_size)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def calculate_direction(self):
        pass

    def wall_collision(self):
        for wall in self.game.dungeon_manager.current_map.wall_list:
            if self.rect.colliderect(wall.rect):
                print("hit")

    def update_pos(self):
        pass

    def update(self):
        self.update_pos()

    def draw(self):
        pygame.draw.circle(self.room.tile_map.new_map_surface, BLACK, self.rect.center, self.radius)
        pygame.draw.circle(self.room.tile_map.new_map_surface, RED, self.rect.center, self.radius - 1)


class ImpBullet(Bullet):
    hit_box_size = (5, 5)
    radius = 5
    speed = 5

    def __init__(self, game, room, user, x, y, target_pos):
        Bullet.__init__(self, game, room, user, x, y, target_pos)
        self.damage = user.damage


class BulletManager:
    def __init__(self, game):
        self.game = game
        self.bullet_list = []

    def add_bullet(self, bullet):
        self.bullet_list.append(bullet)

    def remove_bullet(self, bullet):
        self.bullet_list.remove(bullet)

    def update(self):
        for bullet in self.bullet_list:
            if bullet.room is not self.game.dungeon_manager.current_room:
                self.remove_bullet(bullet)
            bullet.update()

    def draw(self):
        for bullet in self.bullet_list:
            bullet.draw()

