# Imports necessary modules
import pygame
import random
import csv
import copy
# Settings contains the constants used in the game
from settings import *
from .dungeon_graphics import TileMap, SpriteSheet
from objects.weapon import RustySword


class Room:
    def __init__(self, game, paths, pos, room_type='normal'):
        # Initializes the Room class
        self.game = game
        self.paths = paths
        self.free_paths = []
        self.pos = pos
        self.type = room_type
        self.room_map = []  # csv file of tile identifiers
        self.tile_map = None
        self.enemy_list = []
        self.object_list = []


class Dungeon:
    def __init__(self, game, size, dm):
        # Initializes the Dungeon class
        self.level = dm.level
        self.game = game
        self.size = pygame.math.Vector2(size)
        w = int(self.size.x)
        h = int(self.size.y)
        self.num_rooms = 0
        # Creates an empty 2D array that will store the rooms
        self.rooms = [[None for _ in range(w)] for _ in range(h)]
        self.start_pos = [h // 2, w // 2]
        self.new_pos = None
        self.new_room = None
        self.depth = 0  # Used to limit the number of recursive calls
        self.generate_dungeon()
        self.num_rooms = self.count_rooms()

    def generate_dungeon(self):
        # Creates the spawn room
        self.rooms[self.start_pos[0]][self.start_pos[1]] = Room(self.game, ['N'], self.start_pos, 'spawn')
        # Calls the necessary functions to create the dungeon
        self.create_room(self.rooms[self.start_pos[0]][self.start_pos[1]])
        self.create_connections()
        self.add_room_map('mapa4')
        self.add_room_map('mapa3')
        self.add_room_map('floor_layer')
        self.add_room_map('wall_layer')
        self.add_graphics()
        self.add_objects()

    def create_room(self, room):
        # Main function that creates the rooms of the dungeon
        free_paths = self.find_free_paths(room)
        # Uses a set to remove the paths that have been randomly chosen but are not free
        available_paths = (list(set(free_paths).intersection(room.paths)))
        random.shuffle(available_paths)

        if available_paths and self.depth < 6:
            # Loops through the available generated paths and assigns the new room coordinates
            self.depth += 1
            for path in available_paths:
                if path == 'N':
                    self.new_pos = [room.pos[0] - 1, room.pos[1]]
                elif path == 'E':
                    self.new_pos = [room.pos[0], room.pos[1] + 1]
                elif path == 'S':
                    self.new_pos = [room.pos[0] + 1, room.pos[1]]
                elif path == 'W':
                    self.new_pos = [room.pos[0], room.pos[1] - 1]
                # Instantiates the new room and adds it to the 2D array 'rooms'
                self.new_room = Room(self.game, random.choice(POSSIBLE_ROOMS[path]), self.new_pos)
                self.rooms[self.new_pos[0]][self.new_pos[1]] = self.new_room
                # Recursively calls the function to explore the newly created room and create its neighbours
                self.create_room(self.new_room)

    def count_rooms(self):
        # Returns the number of rooms in the dungeon
        num_rooms = 0
        for row in self.rooms:
            for room in row:
                if room:
                    num_rooms += 1
        return num_rooms

    def create_connections(self):
        """Loops through the 2D array and re-assigns the connections for each room.
        This is done to connect rooms that have been generated next to each other from different paths."""
        for row in self.rooms:
            for room in row:
                if room:
                    room.paths = ''
                    if room.pos[0] - 1 < 0:
                        pass
                    elif self.rooms[room.pos[0] - 1][room.pos[1]] is not None:
                        room.paths += 'N'

                    if room.pos[1] + 1 > self.size.x - 1:
                        pass
                    elif self.rooms[room.pos[0]][room.pos[1] + 1] is not None:
                        room.paths += 'E'

                    if room.pos[0] + 1 > self.size.y - 1:
                        pass
                    elif self.rooms[room.pos[0] + 1][room.pos[1]] is not None:
                        room.paths += 'S'

                    if room.pos[1] - 1 < 0:
                        pass
                    elif self.rooms[room.pos[0]][room.pos[1] - 1] is not None:
                        room.paths += 'W'

    def find_free_paths(self, room):
        free_paths = []
        # Returns a list of free paths for the current room
        if room.pos[1] + 1 > self.size.x - 1:
            pass
        elif self.rooms[room.pos[0]][room.pos[1] + 1] is None:
            free_paths.append('E')
        if room.pos[1] - 1 < 0:
            pass
        elif self.rooms[room.pos[0]][room.pos[1] - 1] is None:
            free_paths.append('W')
        if room.pos[0] + 1 > self.size.y - 1:
            pass
        elif self.rooms[room.pos[0] + 1][room.pos[1]] is None:
            free_paths.append('S')
        if room.pos[0] - 1 < 0:
            pass
        elif self.rooms[room.pos[0] - 1][room.pos[1]] is None:
            free_paths.append('N')
        return free_paths

    @staticmethod
    def close_paths(paths, room_map, file):
        # Closes the paths that are not available for the current room
        if 'W' not in paths:
            room_map[5][2] = 257
            room_map[6][2] = 257
            room_map[4][1] = -1
            room_map[5][1] = -1
            room_map[6][1] = -1
            room_map[7][1] = -1
            if file == 'floor_layer':
                room_map[5][2] = 130
                room_map[6][2] = 130
        if 'E' not in paths:
            room_map[5][16] = 256
            room_map[6][16] = 256
            room_map[5][17] = -1
            room_map[6][17] = -1
            room_map[4][17] = -1
            room_map[7][17] = -1
            if file == 'floor_layer':
                room_map[5][16] = 130
                room_map[6][16] = 130
        if 'N' not in paths:
            room_map[1][9] = 2
            room_map[2][9] = 33
            room_map[1][10] = 1
            room_map[1][9] = 1
            room_map[1][8] = 1
        if 'S' not in paths:
            room_map[9][9] = 2
            room_map[10][9] = 33
            room_map[10][8] = 33
            room_map[10][10] = 33
            room_map[11][8] = -1
            room_map[11][9] = -1
            room_map[11][10] = -1
            if file == 'floor_layer':
                room_map[9][9] = 130

    @staticmethod
    def randomise_floor_layout(room_map):
        # Randomises the floor tiles displayed in a room
        w = [10, 1, 1, 1, 1, 0.2, 0.2, 0.2]
        for x in range(len(room_map)):
            for y in range(len(room_map[0])):
                if int(room_map[x][y]) in FLOOR_TILES:
                    room_map[x][y] = random.choices(FLOOR_TILES, w, k=1)[0]

    def add_room_map(self, file):
        # Adds layers of csv files to every room in the dungeon
        # The number in the csv files correspond to tile image identifiers
        with open(f'assets/maps/{file}.csv', newline='') as f:
            reader = csv.reader(f)
            basic_map = list(reader)

        for row in self.rooms:
            for room in row:
                if isinstance(room, Room):
                    room_map = copy.deepcopy(basic_map)
                    if file == 'floor_layer':
                        self.randomise_floor_layout(room_map)
                    self.close_paths(room.paths, room_map, file)
                    room.room_map.append(room_map)

    def add_graphics(self):
        # Creates an instance of TileMap for each room in the dungeon which will display the room
        for row in self.rooms:
            for room in row:
                if isinstance(room, Room):
                    room.tile_map = TileMap(SpriteSheet('assets/spritesheet.png'), room.room_map, room)

    def add_objects(self):
        # Adds objects to the rooms
        for row in self.rooms:
            for room in row:
                if isinstance(room, Room):
                    if room.type == 'spawn':
                        # Adds the beginner weapon to the spawn room
                        room.object_list.append(RustySword(self.game, room, (650, 300)))
