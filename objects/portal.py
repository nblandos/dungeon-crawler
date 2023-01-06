from settings import *
from .object import Object


class Portal(Object):
    name = 'hole'

    def __init__(self, game, room, pos):
        super().__init__(game, self.name, room, pos, (TILE_SIZE, TILE_SIZE))

    def interact(self):
        # Loads the next level
        self.game.dungeon_manager.next_level()

