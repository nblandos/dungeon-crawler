import pygame
from .object import Object


class Weapon(Object):
    def __init__(self, game, name, room, pos, size):
        Object.__init__(self, game, name, room, pos, size)

    def interact(self):
        print('interact')
        self.game.player.weapon = self
        self.remove()

    def draw(self):
        surface = self.room.tile_map.new_map_surface
        if self.game.player.weapon == self:
            surface = self.game.screen
        surface.blit(self.image, self.rect)


class RustySword(Weapon):
    name = 'weapon_rusty_sword'
    size = (36, 96)
    damage = 10

    def __init__(self, game, room, pos):
        Weapon.__init__(self, game, self.name, room, pos, self.size)
