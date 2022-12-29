import pygame
from settings import *
import functions as f
from .entity import Entity


class Player(Entity):
    # Creates the player which is a child class of Entity
    name = 'knight_m'
    speed = 400
    max_health = 100
    health = max_health

    def __init__(self, game):
        Entity.__init__(self, game, self.name)  # Inherits from Entity
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}_idle_anim_f3.png'),
                                            (TILE_SIZE, PLAYER_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect()  # Creates a rect of the size of the image
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.rect = self.image.get_rect(center=(512 + 2.5 * 64, 400))  # Changes the position of the rect
        self.hit_box = self.hit_box.inflate(-25, -20)
        self.room = None
        self.weapon = None

    def input(self):
        # Sets the direction of the player based on the key pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 'right'
        if keys[pygame.K_e]:
            self.game.object_manager.interact()
        if keys[pygame.K_q]:
            if self.weapon:
                self.weapon.drop()

        # Calculates the velocity of the player based on the key pressed
        vel_up = [0, -self.speed * self.game.constant_dt]
        vel_up = [i * keys[pygame.K_w] for i in vel_up]
        vel_down = [0, self.speed * self.game.constant_dt]
        vel_down = [i * keys[pygame.K_s] for i in vel_down]
        vel_left = [-self.speed * self.game.constant_dt, 0]
        vel_left = [i * keys[pygame.K_a] for i in vel_left]
        vel_right = [self.speed * self.game.constant_dt, 0]
        vel_right = [i * keys[pygame.K_d] for i in vel_right]
        vel = zip(vel_up, vel_down, vel_left, vel_right)
        vel_list = [sum(item) for item in vel]

        if 0 not in vel_list:
            # Calculates the velocity if the player is moving diagonally
            x = (pow(vel_list[0], 2) + pow(vel_list[1], 2)) ** 0.5
            z = x / (abs(vel_list[0]) + abs(vel_list[1]))
            vel_list_fixed = [item * z for item in vel_list]
            self.set_velocity(vel_list_fixed)
        else:
            self.set_velocity(vel_list)

        if pygame.mouse.get_pressed()[0]:
            # attack
            pass

    def take_damage(self, amount):
        # Removes the specified amount of health from the player
        if not self.dead:
            self.health -= amount

    def draw(self):
        # Draws the player
        self.game.screen.blit(self.image, self.rect)
        '''if self.weapon:
            self.weapon.draw()'''

    def update(self):
        # Check if the player is colliding with a wall and updates the rect and hit_box
        self.wall_collision()
        self.basic_update()


