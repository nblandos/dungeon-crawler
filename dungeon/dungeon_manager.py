import pygame
import random
from settings import *
from .dungeon_generator import Dungeon


class DungeonManager:
    num_rooms = random.randint(MIN_ROOMS, MAX_ROOMS)
    level = 1

    def __init__(self, game):
        self.game = game
        self.dungeon = None
        self.current_room = None
        self.current_map = None
        self.load_dungeon_manager()

    def load_dungeon_manager(self):
        self.dungeon = Dungeon(self.game, DUNGEON_SIZE, self)
        self.current_room = self.dungeon.rooms[self.dungeon.start_pos[0]][self.dungeon.start_pos[1]]
        self.current_map = self.current_room.tile_map

    def update(self):
        pass

    def draw_map(self, surface):
        pass