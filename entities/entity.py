import pygame
from settings import *
import functions as f
from .entity_animation import EntityAnimation


class Entity:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.path = f'assets/frames/{self.name}'
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}_idle_anim_f3.png'),
                                            (TILE_SIZE, PLAYER_HEIGHT)).convert_alpha()
        self.direction = 'right'
        self.entity_animation = EntityAnimation(self)
        self.rect = self.image.get_rect()
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.velocity = [0, 0]

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def wall_collision(self):
        move_rect = self.hit_box.move(*self.velocity)
        collide_points = (move_rect.midbottom, move_rect.bottomleft, move_rect.bottomright)
        for wall in self.game.dungeon_manager.current_map.wall_list:
            if any(wall.hit_box.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]

    def update_hit_box(self):
        self.hit_box.midbottom = self.rect.midbottom

    def basic_update(self):
        self.update_hit_box()
        self.entity_animation.update()
        self.rect.move_ip(*self.velocity)
        self.hit_box.move_ip(*self.velocity)
