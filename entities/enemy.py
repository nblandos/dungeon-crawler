import pygame
import random
import functions as f
from .entity import Entity


class Enemy(Entity):
    def __init__(self, game, name, room, max_health):
        Entity.__init__(self, game, name)
        self.room = room
        self.max_health = max_health
        self.health = max_health
        self.attack_cooldown = pygame.time.get_ticks()

    def spawn(self):
        self.rect.x = random.randint(200, 1000)
        self.rect.y = random.randint(200, 550)

    def move(self):
        if self.can_move and not self.dead:
            self.follow_player()
        else:
            self.velocity = [0, 0]

    def can_attack(self):
        if f.time_passed(self.attack_cooldown, 1000):
            self.attack_cooldown = pygame.time.get_ticks()
            return True

    def attack_player(self):
        if self.hit_box.colliderect(self.game.player.hit_box) and self.can_attack():
            self.game.player.take_damage(self.damage)

    def follow_player(self):
        dir_vector = pygame.math.Vector2(self.game.player.hit_box.centerx - self.hit_box.centerx,
                                         self.game.player.hit_box.centery - self.hit_box.centery)
        if dir_vector.length_squared() > 0:
            dir_vector.normalize_ip()
            dir_vector.scale_to_length(self.speed * self.game.constant_dt)
        self.set_velocity(dir_vector)

    def update(self):
        self.basic_update()
        self.move()
        self.attack_player()

    def draw(self):
        self.room.tile_map.new_map_surface.blit(self.image, self.rect)


class Goblin(Enemy):
    name = 'goblin'
    speed = 200
    damage = 15

    def __init__(self, game, room, max_health):
        Enemy.__init__(self, game, self.name, room, max_health)
