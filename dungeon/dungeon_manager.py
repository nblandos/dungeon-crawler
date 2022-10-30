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

    def update(self):
        pass

    def draw_map(self, surface):
        pass