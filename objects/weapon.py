import pygame
import math
from .object import Object


class Weapon(Object):
    def __init__(self, game, name, room, pos, size):
        Object.__init__(self, game, name, room, pos, size)
        self.angle = 0
        self.swing_counter = 0
        self.offset = pygame.math.Vector2(0, -40)
        self.rotated_offset = None
        self.swing_side = 1

    def interact(self):
        self.swing_counter = 0
        if self.game.player.weapon:
            self.game.player.weapon.drop()
        self.game.player.weapon = self
        self.remove()

    def drop(self):
        self.room = self.game.dungeon_manager.current_room
        self.room.object_list.append(self)
        self.game.player.weapon = None
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y

    def rotate(self):
        player_pos = self.game.player.hit_box.center
        mx, my = pygame.mouse.get_pos()
        dx = mx - player_pos[0]
        dy = my - player_pos[1]
        self.angle = (180 / math.pi) * -math.atan2(dy, dx) - 90
        self.image = pygame.transform.rotozoom(self.image_copy, self.angle, 1)
        self.rotated_offset = self.offset.rotate(-self.angle)
        self.rect = self.image.get_rect(center=player_pos + self.rotated_offset)

    def swing(self):
        self.angle += 20 * self.swing_side
        player_pos = self.game.player.hit_box.center
        self.image = pygame.transform.rotozoom(self.image_copy, self.angle, 1)
        self.rotated_offset = self.offset.rotate(-self.angle)
        self.rect = self.image.get_rect(center=player_pos + self.rotated_offset)
        self.swing_counter += 1

    def enemy_collision(self):
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            if self.rect.colliderect(enemy.hit_box):
                enemy.health -= self.damage
                print(enemy.health)

    def held_update(self):
        if self.swing_counter == 6:
            self.image_copy = pygame.transform.flip(self.image_copy, True, False)
            self.game.player.attacking = False
            self.swing_counter = 0
        if self.game.player.attacking and self.swing_counter <= 6:
            self.swing()
        else:
            self.rotate()

    def draw(self):
        # Overrides the draw method from the Object class
        if self.room:
            surface = self.room.tile_map.new_map_surface
        else:
            surface = self.game.screen
        surface.blit(self.image, self.rect)


class RustySword(Weapon):
    name = 'weapon_rusty_sword'
    size = (36, 90)
    damage = 15
    cooldown = 500

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)




