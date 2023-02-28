import pygame
import random
import functions as f
from settings import *
from .entity import Entity
from bullet import ImpBullet, BigZombieBullet


class Enemy(Entity):
    # Enemy class is the parent class for all enemies
    def __init__(self, game, name, room, max_health):
        Entity.__init__(self, game, name)  # Inherits from Entity
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}_idle_anim_f3.png'),
                                            (TILE_SIZE, TILE_SIZE)).convert_alpha()
        self.rect = self.image.get_rect()  # Creates a rect of the size of the image
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.room = room
        self.max_health = max_health
        self.health = max_health
        self.attack_cooldown = pygame.time.get_ticks()
        self.cooldown = None
        self.destination = None  # The position of a destination for the enemy to move to

    def spawn(self):
        # Spawns boss enemies in the middle of the room
        # Spawns normal enemy in a random position within the room
        if self.room.type == 'boss':
            self.rect.center = (650, 400)
        else:
            self.rect.x = random.randint(200, 1000)
            self.rect.y = random.randint(200, 550)

    def move(self):
        # Method that makes the enemy move towards the player
        if self.can_move and not self.dead:
            self.follow_player()
        else:
            self.velocity = [0, 0]

    def can_attack(self):
        # Checks if the enemy can attack based on a cooldown
        if f.time_passed(self.attack_cooldown, self.cooldown):
            self.attack_cooldown = pygame.time.get_ticks()
            return True

    def attack(self):
        # If the enemy is touching the player and is not an attack cooldown, the player takes damage
        if self.hit_box.colliderect(self.game.player.hit_box) and self.can_attack():
            self.game.player.take_damage(self.damage)

    def follow_player(self):
        # Calculates the distance and direction between the enemy and the player
        distance_to_player = pygame.math.Vector2(self.game.player.hit_box.x - self.hit_box.x,
                                                 self.game.player.hit_box.y - self.hit_box.y)
        if distance_to_player.length_squared() > 0:
            distance_to_player.normalize_ip()
            distance_to_player.scale_to_length(self.speed * self.game.constant_dt)
        # Sets the velocity to based on the direction from the player to the enemy and the speed of the enemy
        self.set_velocity(distance_to_player)

    def move_away_from_player(self, radius):
        # Moves the enemy to a random positiion within the room if the player is within a certain radius
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
        min_x, max_x, min_y, max_y = 196, 1082, 162, 586  # The bounds of the room
        pos = [random.randint(min_x, max_x), random.randint(min_y, max_y)]
        vector = pygame.math.Vector2(self.game.player.hit_box.x - pos[0], self.game.player.hit_box.x - pos[1])
        while vector.length() < radius:
            pos = [random.randint(min_x, max_x), random.randint(min_y, max_y)]
            vector = pygame.math.Vector2(self.game.player.hit_box.x - pos[0], self.game.player.hit_box.x - pos[1])
        self.destination = pos

    def update(self):
        # Adds movement to the enemy and lets it attack the player if it can
        self.basic_update()
        self.move()
        self.attack()
        self.rect.midbottom = self.hit_box.midbottom

    def draw_health(self, surface):
        # Draws the health bar of the enemy
        if self.health < self.max_health:
            health_rect = pygame.Rect(0, 0, 25, 6)
            health_rect.midbottom = self.rect.centerx, self.rect.top
            health_rect.midbottom = self.rect.centerx, self.rect.top
            pos = health_rect.topleft
            size = health_rect.size
            pygame.draw.rect(surface, DARK_RED, (*pos, *size))
            rect = (pos[0], pos[1], (size[0]) * (self.health / self.max_health), size[1])
            pygame.draw.rect(surface, LIME_GREEN, rect)

    def draw(self):
        # Draws the enemy
        self.room.tile_map.new_map_surface.blit(self.image, self.rect)
        self.draw_health(self.room.tile_map.new_map_surface)


class RangedEnemy(Enemy):
    # Parent class for every type of ranged enemy
    def __init__(self, game, room, max_health):
        Enemy.__init__(self, game, self.name, room, max_health)  # Inherits from Enemy

    def attack(self):
        # Overrides the attack method from Enemy as ranged enemies shoot bullets at the player
        # Shoots a bullet at the player if the enemy is not on cooldown
        if f.time_passed(self.attack_cooldown, self.cooldown) and not self.dead and not self.game.player.dead and sum(
                self.velocity) == 0:
            if self.name == 'imp':
                self.game.bullet_manager.add_bullet(
                    ImpBullet(self.game, self.room, self, self.rect.center[0], self.rect.center[1],
                              (self.game.player.hit_box.centerx, self.game.player.hit_box.centery + 25)))
            elif self.name == 'big_zombie':
                self.game.bullet_manager.add_bullet(
                    BigZombieBullet(self.game, self.room, self, self.rect.center[0], self.rect.center[1],
                                    (self.game.player.hit_box.centerx, self.game.player.hit_box.centery + 25)))
            self.attack_cooldown = pygame.time.get_ticks()

    def move(self):
        # Overrides the move method from Enemy as ranged enemies moves away from the player
        # Moves the enemy away from the player if the player is within a certain radius
        if self.can_move and not self.dead:
            self.move_away_from_player(self.radius)


class Goblin(Enemy):
    # Goblin class is a child class of Enemy
    # The goblin is a melee enemy that moves towards the player and attacks it
    # Defines the stats of the goblin enemy
    name = 'goblin'
    speed = 225
    damage = 2

    def __init__(self, game, room, max_health):
        Enemy.__init__(self, game, self.name, room, max_health)  # Inherits from Enemy
        self.cooldown = 1500


class Imp(RangedEnemy):
    # Imp class is a child class of RangedEnemy
    # The imp is a ranged enemy that moves away from the player and shoots bullets at it
    # Defines the stats of the imp enemy
    name = 'imp'
    speed = 175
    damage = 3
    radius = 200

    def __init__(self, game, room, max_health):
        RangedEnemy.__init__(self, game, room, max_health)  # Inherits from RangedEnemy
        self.cooldown = 1200


class BigDemon(Enemy):
    # BigDemon class is a child class of Enemy
    # The big demon is a melee enemy that moves towards the player and attacks it
    # Defines the stats of the big demon enemy
    name = 'big_demon'
    speed = 150
    damage = 20

    def __init__(self, game, room, max_health):
        Enemy.__init__(self, game, self.name, room, max_health)  # Inherits from Enemy
        self.cooldown = 1200
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}_idle_anim_f3.png'),
                                            (32 * SCALE_FACTOR, 36 * SCALE_FACTOR)).convert_alpha()
        self.rect = self.image.get_rect()
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)


class BigZombie(RangedEnemy):
    # BigZombie class is a child class of RangedEnemy
    # The big zombie is a ranged enemy that moves away from the player and shoots bullets at it
    # Defines the stats of the big zombie enemy
    name = 'big_zombie'
    speed = 250
    damage = 5
    radius = 100

    def __init__(self, game, room, max_health):
        RangedEnemy.__init__(self, game, room, max_health)  # Inherits from RangedEnemy
        self.cooldown = 150
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}_idle_anim_f3.png'),
                                            (32 * SCALE_FACTOR, 34 * SCALE_FACTOR)).convert_alpha()
        self.rect = self.image.get_rect()  # Creates a rect of the size of the image
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
