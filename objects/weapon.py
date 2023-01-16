import pygame
import math
from settings import *
from .object import Object
from bullet import GreenMagicStaffBullet, RedMagicStaffBullet


class Weapon(Object):
    # Inherits from the Object class
    # Object that the player can pick up and use to attack enemies
    def __init__(self, game, name, room, pos, size):
        Object.__init__(self, game, name, room, pos, size)  # Inherits from the Object class
        self.angle = 0
        self.swing_counter = 0
        self.offset = pygame.math.Vector2(0, -40)
        self.rotated_offset = None
        self.swing_side = 1

    def interact(self):
        # The player picks up the weapon when they interact with it
        self.swing_counter = 0
        if self.game.player.weapon:
            self.game.player.weapon.drop()
        self.game.player.weapon = self
        self.remove()

    def drop(self):
        # Drops the weapon on the ground and removes it from the player
        self.room = self.game.dungeon_manager.current_room
        self.room.object_list.append(self)
        self.game.player.weapon = None
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y

    def rotate(self):
        # Rotates the weapon to face the mouse
        player_pos = self.game.player.hit_box.center
        mx, my = pygame.mouse.get_pos()
        dx = mx - player_pos[0]
        dy = my - player_pos[1]
        self.angle = (180 / math.pi) * -math.atan2(dy, dx) - 90
        self.image = pygame.transform.rotozoom(self.image_copy, self.angle, 1)
        self.rotated_offset = self.offset.rotate(-self.angle)
        self.rect = self.image.get_rect(center=player_pos + self.rotated_offset)

    def swing(self):
        # Swings the weapon in an arc
        self.angle += 10 * self.swing_side
        player_pos = self.game.player.hit_box.center
        self.image = pygame.transform.rotozoom(self.image_copy, self.angle, 1)
        self.rotated_offset = self.offset.rotate(-self.angle)
        self.rect = self.image.get_rect(center=player_pos + self.rotated_offset)
        self.swing_counter += 60 * self.game.constant_dt

    def enemy_collision(self):
        # Damages the enemy if the weapon is touching them
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            if self.rect.colliderect(enemy.hit_box):
                enemy.health -= self.damage * self.game.player.attack_multiplier

    def held_update(self):
        # Updates the weapon when it is being held by the player
        if self.swing_counter == 12:
            self.game.player.attacking = False
            self.swing_counter = 0
        if self.game.player.attacking and self.swing_counter <= 12:
            self.swing()
        else:
            self.rotate()

    def shoot(self):
        pass

    def draw(self):
        # Overrides the draw method from the Object class
        # Draws the weapon on the correct surface
        if self.room:
            surface = self.room.tile_map.new_map_surface
        else:
            surface = self.game.screen
        surface.blit(self.image, self.rect)


class RustySword(Weapon):
    # Inherits from the Weapon class
    # A type of weapon that the player starts with
    # Defines the stats of the weapon
    name = 'weapon_rusty_sword'
    size = (10 * SCALE_FACTOR, 21 * SCALE_FACTOR)
    damage = 15
    cooldown = 500

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon


class Katana(Weapon):
    # Inherits from the Weapon class
    # Defines the stats of the weapon
    name = 'weapon_katana'
    size = (6 * SCALE_FACTOR, 29 * SCALE_FACTOR)
    damage = 25
    cooldown = 300

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon


class AnimeSword(Weapon):
    # Inherits from the Weapon class
    # Defines the stats of the weapon
    name = 'weapon_anime_sword'
    size = (12 * SCALE_FACTOR, 30 * SCALE_FACTOR)
    damage = 60
    cooldown = 850

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon


class Knife(Weapon):
    # Inherits from the Weapon class
    # Defines the stats of the weapon
    name = 'weapon_knife'
    size = (6 * SCALE_FACTOR, 13 * SCALE_FACTOR)
    damage = 15
    cooldown = 150

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon


class Mace(Weapon):
    # Inherits from the Weapon class
    # Defines the stats of the weapon
    name = 'weapon_mace'
    size = (10 * SCALE_FACTOR, 24 * SCALE_FACTOR)
    damage = 35
    cooldown = 500

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon


class GreenMagicStaff(Weapon):
    # Inherits from the Weapon class
    # Defines the stats of the weapon
    name = 'weapon_green_magic_staff'
    size = (8 * SCALE_FACTOR, 30 * SCALE_FACTOR)
    damage = 0
    cooldown = 300

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon

    def shoot(self):
        # Shoots a bullet from the weapon
        mouse_pos = pygame.mouse.get_pos()
        self.game.bullet_manager.add_bullet(GreenMagicStaffBullet(self.game, self.game.dungeon_manager.current_room,
                                                                  self.rect.midtop[0], self.rect.midtop[1], mouse_pos))


class RedMagicStaff(Weapon):
    # Inherits from the Weapon class
    # Defines the stats of the weapon
    name = 'weapon_red_magic_staff'
    size = (8 * SCALE_FACTOR, 30 * SCALE_FACTOR)
    damage = 0
    cooldown = 900

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)  # Inherits from Weapon

    def shoot(self):
        # Shoots a bullet from the weapon
        mouse_pos = pygame.mouse.get_pos()
        self.game.bullet_manager.add_bullet(RedMagicStaffBullet(self.game, self.game.dungeon_manager.current_room,
                                                                self.rect.midtop[0], self.rect.midtop[1], mouse_pos))
