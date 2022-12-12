import pygame
import random
import functions as f
from .entity import Entity
from bullet import ImpBullet


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

    def attack(self):
        if self.hit_box.colliderect(self.game.player.hit_box) and self.can_attack():
            self.game.player.take_damage(self.damage)

    def follow_player(self):
        distance_to_player = pygame.math.Vector2(self.game.player.hit_box.x - self.hit_box.x,
                                                 self.game.player.hit_box.y - self.hit_box.y)
        if distance_to_player.length_squared() > 0:
            distance_to_player.normalize_ip()
            distance_to_player.scale_to_length(self.speed * self.game.constant_dt)
        self.set_velocity(distance_to_player)

    def move_away_from_player(self, radius):
        distance_to_player = pygame.math.Vector2(self.game.player.hit_box.x - self.hit_box.x,
                                                 self.game.player.hit_box.y - self.hit_box.y)
        if self.destination:
            len_player_to_destination = pygame.math.Vector2(self.game.player.hit_box.x - self.destination[0],
                                                            self.game.player.hit_box.y - self.destination[1]).length()
            if len_player_to_destination < radius:
                self.choose_random_pos(radius)

        if distance_to_player.length() < radius:
            if not self.destination:
                self.choose_random_pos(radius)
            distance_to_destination = pygame.math.Vector2(self.destination[0] - self.hit_box.x,
                                                          self.destination[1] - self.hit_box.y)
            if distance_to_destination.length_squared() > 0:
                distance_to_destination.normalize_ip()
                distance_to_destination.scale_to_length(self.speed * self.game.constant_dt)
                self.set_velocity(distance_to_destination)
            else:
                self.destination = None
        else:
            self.set_velocity([0, 0])

    def choose_random_pos(self, radius):
        # Finds a random destination within the room for ranged enemies (imps) to move to
        min_x, max_x, min_y, max_y = 196, 1082, 162, 586
        pos = [random.randint(min_x, max_x), random.randint(min_y, max_y)]
        vector = pygame.math.Vector2(self.game.player.hit_box.x - pos[0], self.game.player.hit_box.x - pos[1])
        while vector.length() < radius:
            pos = [random.randint(min_x, max_x), random.randint(min_y, max_y)]
            vector = pygame.math.Vector2(self.game.player.hit_box.x - pos[0], self.game.player.hit_box.x - pos[1])
        self.destination = pos

    def update(self):
        self.basic_update()
        self.move()
        self.attack()

    def draw(self):
        self.room.tile_map.new_map_surface.blit(self.image, self.rect)


class Goblin(Enemy):
    name = 'goblin'
    speed = 150
    damage = 12

    def __init__(self, game, room, max_health):
        Enemy.__init__(self, game, self.name, room, max_health)


class Imp(Enemy):
    name = 'imp'
    speed = 200
    damage = 8
    radius = 200

    def __init__(self, game, room, max_health):
        Enemy.__init__(self, game, self.name, room, max_health)
        self.destination = None

    def shoot(self):
        if f.time_passed(self.attack_cooldown, 800) and not self.dead and not self.game.player.dead:
            self.attack_cooldown = pygame.time.get_ticks()
            self.game.bullet_manager.add_bullet(
                ImpBullet(self.game, self.room, self, self.hit_box.midbottom[0], self.hit_box.midbottom[1],
                          (self.game.player.hit_box.centerx, self.game.player.hit_box.centery)))

    def move(self):
        if self.can_move and not self.dead:
            self.move_away_from_player(self.radius)

    def update(self):
        self.basic_update()
        self.move()
        self.shoot()
