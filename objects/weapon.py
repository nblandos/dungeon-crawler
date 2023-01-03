import pygame
import math
from .object import Object


class Weapon(Object):
    def __init__(self, game, name, room, pos, size):
        Object.__init__(self, game, name, room, pos, size)
        self.angle = 0

    def interact(self):
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
        self.angle = (180 / math.pi) * -math.atan2(dy, dx)
        self.image = pygame.transform.rotozoom(self.image_copy, self.angle - 90, 1)
        self.rect = self.image.get_rect(center=player_pos)

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
    damage = 10

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)
