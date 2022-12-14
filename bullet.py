import pygame
from settings import *


class Bullet:
    def __init__(self, game, room, user, x, y, target_pos):
        self.game = game
        self.room = room
        self.user = user
        self.target_pos = target_pos
        self.image = None
        self.rect = None
        self.load_image()
        self.rect.x = x
        self.rect.y = y
        self.direction = None
        self.calculate_direction()

    def load_image(self):
        # Creates a rect for the bullet
        self.image = pygame.Surface(self.hit_box_size)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def calculate_direction(self):
        # Calculates the direction of the target so the bullet can move towards it
        distance_to_target = pygame.math.Vector2(self.target_pos[0] - self.rect.x, self.target_pos[1] - self.rect.y)
        self.direction = distance_to_target.normalize()

    def wall_collision(self):
        # Checks if the bullet has collided with a wall
        collide_points = (self.rect.midbottom, self.rect.bottomleft, self.rect.bottomright)
        for wall in self.game.dungeon_manager.current_map.wall_list:
            if any(wall.hit_box.collidepoint(point) for point in collide_points):
                self.game.bullet_manager.remove_bullet(self)

    def player_collision(self):
        # Checks if the bullet has collided with a player and deals damage if it has
        if self.rect.colliderect(self.game.player.hit_box):
            self.game.player.health -= self.damage
            self.game.bullet_manager.remove_bullet(self)

    def move(self):
        # Moves the bullet at a constant speed
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def update(self):
        # Moves the bullet and checks for collisions
        self.move()
        if self.rect.y < 0 or self.rect.y > 1000 or self.rect.x < 0 or self.rect.x > 1300:
            self.game.bullet_manager.remove_bullet(self)  # Removes bullet if it goes off-screen
        self.player_collision()
        self.wall_collision()

    def draw(self):
        # Draws the bullet
        pygame.draw.circle(self.room.tile_map.new_map_surface, DARK_RED, self.rect.center, self.radius)
        pygame.draw.circle(self.room.tile_map.new_map_surface, BURGUNDY, self.rect.center, self.radius - 1)


class ImpBullet(Bullet):
    # A bullet that is fired by the Imp enemy
    # Defines the stats of the bullet
    hit_box_size = (7, 7)
    radius = 5
    speed = 5

    def __init__(self, game, room, user, x, y, target_pos):
        Bullet.__init__(self, game, room, user, x, y, target_pos)  # Inherits from the Bullet class
        self.damage = user.damage


class BulletManager:
    def __init__(self, game):
        self.game = game
        self.bullet_list = []  # List of all bullets in the game

    def add_bullet(self, bullet):
        # Adds a bullet to the bullet list
        self.bullet_list.append(bullet)

    def remove_bullet(self, bullet):
        # Removes a bullet from the bullet list
        if bullet in self.bullet_list:
            self.bullet_list.remove(bullet)

    def update(self):
        # Updates all bullets in the bullet list
        for bullet in self.bullet_list:
            if bullet.room is not self.game.dungeon_manager.current_room:
                self.remove_bullet(bullet)
            bullet.update()

    def draw(self):
        # Draws all bullets in the bullet list
        for bullet in self.bullet_list:
            bullet.draw()

