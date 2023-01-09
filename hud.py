import pygame
from settings import *


class Hud:
    def __init__(self, game):
        self.game = game
        # Initialises every hud element
        self.health_bar = HealthBar(self.game, self.game.player)
        self.minimap = Minimap(self.game)

    def draw(self):
        # Draws every hud element
        self.health_bar.draw()
        self.minimap.draw()
        self.draw_level()

    def draw_level(self):
        level_text = f'Level {int(self.game.dungeon_manager.level)}'
        text_surface = pygame.font.Font(FONT, 50).render(level_text, True, WHITE)
        self.game.screen.blit(text_surface, (620, 0))

    def update(self):
        # Updates every hud element that needs to be updated
        self.minimap.update()


class HealthBar:
    def __init__(self, game, player):
        # Initialises the health bar by loading the frame image
        self.game = game
        self.player = player

    def draw(self):
        # Draws the players current health in the health bar frame
        line_pos = 15
        section_count = 0
        num_sections = int(self.player.health) // 15
        for i in range(num_sections):
            section_count += 1
            pygame.draw.rect(self.game.screen, DARK_RED, (15 + section_count * 15, line_pos, 10, 15))
            if section_count > 15:
                line_pos += 20
                section_count = 0


class Minimap:
    # Defines values for the minimap
    room_height = 25
    room_width = 36
    room_dimensions = (room_width, room_height)
    offset_x = 1000
    offset_y = 0

    def __init__(self, game):
        self.game = game
        self.current_room = None  # The room the player is currently in
        self.current_x, self.current_y = None, None # The coordinates of the current room in the dungeon array
        self.visited_rooms = []  # Rooms that the player has visited

    def add_room(self, room):
        # Adds a room to the list of visited rooms
        if [room.pos[1], room.pos[0]] not in self.visited_rooms:
            self.visited_rooms.append([room.pos[1], room.pos[0]])  # x, y

    def set_current_room(self, room):
        # Updates attributes to reflect the current room
        self.add_room(room)
        if self.current_room is not room:
            self.current_room = room
            self.current_x = self.current_room.pos[1]
            self.current_y = self.current_room.pos[0]

    def reset_visited_rooms(self):
        # Resets the list of visited rooms
        self.visited_rooms = []

    def update(self):
        # Updates the current room to the room the player is currently in
        self.set_current_room(self.game.dungeon_manager.current_room)

    def draw(self):
        # Draws the minimap and the player's position on it
        surface = self.game.screen
        for room in self.visited_rooms:
            position = (self.offset_x + room[0] * self.room_width * 1.2,
                        self.offset_y + room[1] * self.room_height * 1.2)
            pygame.draw.rect(surface, DARK_GREY, (*position, *self.room_dimensions), 4)
        position = (self.offset_x + self.current_x * self.room_width * 1.2,
                    self.offset_y + self.current_y * self.room_height * 1.2)
        pygame.draw.rect(surface, GREY, (*position, *self.room_dimensions))





