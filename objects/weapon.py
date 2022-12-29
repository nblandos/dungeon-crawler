import pygame
from .object import Object


class Weapon(Object):
    def __init__(self, game, name, room, pos, size):
        Object.__init__(self, game, name, room, pos, size)

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

    def draw(self):
        # Overrides the draw method from the Object class
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
