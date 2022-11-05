import pygame
import random
from settings import *
from .dungeon_generator import Dungeon


class DungeonManager:
    level = 1

    def __init__(self, game):
        self.game = game
        self.dungeon = None
        self.current_room = None
        self.next_room = None
        self.next_room_map = None
        self.current_map = None
        self.room_change = None
        self.direction = None
        self.x, self.y = None, None
        self.load_dungeon_manager()

    def load_dungeon_manager(self):
        self.dungeon = Dungeon(self.game, DUNGEON_SIZE, self)
        self.current_room = self.dungeon.rooms[self.dungeon.start_pos[0]][self.dungeon.start_pos[1]]
        self.current_map = self.current_room.tile_map
        self.y, self.x = self.current_room.pos[0], self.current_room.pos[1]
        self.room_change = False

    def set_room(self, room):
        self.current_room = room
        self.current_map = room.tile_map

    def set_next_room(self, room):
        self.next_room = room
        self.next_room_map = room.tile_map

    def initialise_room_change(self, direction):
        self.direction = direction
        self.initialise_next_room(direction)
        self.room_change = True

    def initialise_next_room(self, direction):
        if direction == 'N':
            self.set_next_room(self.dungeon.rooms[self.y - 1][self.x])
            self.next_room_map.y = -13 * TILE_SIZE
            self.game.player.rect.y = -3.3 * 64
        elif direction == 'S':
            self.set_next_room(self.dungeon.rooms[self.y + 1][self.x])
            self.next_room_map.y = HEIGHT
            self.game.player.rect.y = 16 * 64
        elif direction == 'E':
            self.set_next_room(self.dungeon.rooms[self.y][self.x + 1])
            self.next_room_map.x = WIDTH
            self.game.player.rect.x = WIDTH + 3.3 * 64
        elif direction == 'W':
            self.set_next_room(self.dungeon.rooms[self.y][self.x - 1])
            self.next_room_map.x = -19 * TILE_SIZE
            self.game.player.rect.x = -2.3 * 64

    def detect_room_change(self):
        if self.room_change and self.game.player:
            player = self.game.player
            if player.rect.y <= 96:
                self.initialise_room_change('N')
            elif player.rect.y >= 11 * 64:
                self.initialise_room_change('S')
            elif player.rect.x <= 3 * 64:
                self.initialise_room_change('W')
            elif player.rect.x > 17 * 64:
                self.initialise_room_change('E')

    def update(self):
        self.detect_room_change()
        if self.room_change:
            pass

    def draw_map(self, surface):
        self.current_map.draw_map(surface)
        if self.next_room:
            self.next_room_map.draw_map(surface)
