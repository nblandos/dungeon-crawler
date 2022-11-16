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
        # Creates a dungeon between a range of 8-12 rooms and where the spawn room only has one path
        self.dungeon = Dungeon(self, DUNGEON_SIZE, self)
        while len(self.dungeon.rooms[self.dungeon.start_pos[0]][self.dungeon.start_pos[1]].paths) != 1 \
                or self.dungeon.num_rooms < MIN_ROOMS or self.dungeon.num_rooms > MAX_ROOMS:
            self.dungeon = Dungeon(self, DUNGEON_SIZE, self)
        print(self.dungeon.num_rooms)
        self.current_room = self.dungeon.rooms[self.dungeon.start_pos[0]][self.dungeon.start_pos[1]]
        self.current_map = self.current_room.tile_map
        self.y, self.x = self.current_room.pos[0], self.current_room.pos[1]
        self.room_change = False

    def set_current_room(self, room):
        # Sets the current room the argument room
        self.current_room = room
        self.current_map = room.tile_map

    def set_next_room(self, room=None):
        # Sets the next room to the argument room
        # The next room is the room that the player is switching to
        self.next_room = room
        if room:
            self.next_room_map = room.tile_map

    def move_rooms(self, direction, speed=70):
        # Moves the map surfaces of the rooms and player so that the new room will be in the centered on the screen
        if direction == 'N':
            self.current_map.y += speed
            self.next_room_map.y += speed
            self.game.player.rect.y += speed
        elif direction == 'S':
            self.current_map.y -= speed
            self.next_room_map.y -= speed
            self.game.player.rect.y -= speed
        elif direction == 'E':
            self.current_map.x -= speed
            self.next_room_map.x -= speed
            self.game.player.rect.x -= speed
        elif direction == 'W':
            self.current_map.x += speed
            self.next_room_map.x += speed
            self.game.player.rect.x += speed
        # Stops moving when the next room is centered on the screen
        self.check_end_room_change()

    def initialise_room_change(self, direction):
        # Sets the room change to true which will start the room change process
        self.direction = direction
        self.initialise_next_room(direction)
        self.room_change = True

    def initialise_next_room(self, direction):
        # Sets the next room to the one being moved to
        # Sets the positions of the player and the next room after the room change
        if direction == 'N':
            self.set_next_room(self.dungeon.rooms[self.y - 1][self.x])
            self.next_room_map.y = -13 * TILE_SIZE
            self.game.player.rect.y = -3.5 * TILE_SIZE
        elif direction == 'S':
            self.set_next_room(self.dungeon.rooms[self.y + 1][self.x])
            self.next_room_map.y = HEIGHT
            self.game.player.rect.y = 16 * TILE_SIZE
        elif direction == 'E':
            self.set_next_room(self.dungeon.rooms[self.y][self.x + 1])
            self.next_room_map.x = WIDTH
            self.game.player.rect.x = WIDTH + 3.5 * TILE_SIZE
        elif direction == 'W':
            self.set_next_room(self.dungeon.rooms[self.y][self.x - 1])
            self.next_room_map.x = -19 * TILE_SIZE
            self.game.player.rect.x = -2.5 * TILE_SIZE

    def detect_room_change(self):
        # Detects if the player is at the edge of a path and if so initiates a room change
        if not self.room_change and self.game.player:
            player = self.game.player
            if player.rect.y <= 1.5 * TILE_SIZE:
                self.initialise_room_change('N')
            elif player.rect.y >= 11 * 64:
                self.initialise_room_change('S')
            elif player.rect.x <= 3 * 64:
                self.initialise_room_change('W')
            elif player.rect.x >= 18 * 64:
                self.initialise_room_change('E')

    def end_room_change(self):
        # Ends the room change process and sets the new room to the current room
        self.room_change = False
        self.y, self.x = self.next_room.pos[0], self.next_room.pos[1]
        self.current_map.fix_map_position()
        self.next_room_map.fix_map_position()
        self.set_current_room(self.dungeon.rooms[self.y][self.x])
        self.set_next_room()

    def check_end_room_change(self):
        # Checks if the room change process has ended
        if self.next_room_map.x <= 0 and self.direction == 'E':
            self.end_room_change()
        if self.next_room_map.x >= 0 and self.direction == 'W':
            self.end_room_change()
        if self.next_room_map.y <= 0 and self.direction == 'S':
            self.end_room_change()
        if self.next_room_map.y >= 0 and self.direction == 'N':
            self.end_room_change()

    def update(self):
        # Checks if a room change has occurred
        self.detect_room_change()
        if self.room_change:
            self.move_rooms(self.direction)

    def draw_map(self, surface):
        # Draws the rooms to the screen
        self.current_map.draw_map(surface)
        if self.next_room:
            self.next_room_map.draw_map(surface)
