import pygame
from settings import *


class Hud:
    def __init__(self, game):
        self.game = game
        self.health_bar = HealthBar(self.game, self.game.player)
        self.minimap = Minimap(self.game)

    def draw(self):
        self.health_bar.draw()
        self.minimap.draw_all()

    def update(self):
        self.minimap.update()


class HealthBar:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.path = 'assets/hud/health_bar.png'
        self.health_bar = pygame.transform.scale(pygame.image.load(self.path), (195, 45)).convert_alpha()

    def draw(self):
        pygame.draw.rect(self.game.screen, DARK_RED, (0, 0, 195, 45))
        num_sections = self.player.health // 10
        for i in range(num_sections):
            pygame.draw.rect(self.game.screen, RED, (25 + i * 15, 15, 10, 15))
        self.game.screen.blit(self.health_bar, (0, 0))


class Minimap:
    room_height = 25
    room_width = 36
    room_dimensions = (room_width, room_height)
    offset_x = 1000
    offset_y = 0

    def __init__(self, game):
        self.game = game
        self.current_room = None
        self.current_x, self.current_y = None, None
        self.rooms = []
        self.visited_rooms = []

    def add_room(self, room):
        if [room.pos[1], room.pos[0]] not in self.visited_rooms:
            self.visited_rooms.append([room.pos[1], room.pos[0]])  # x, y

    def set_current_room(self, room):
        self.add_room(room)
        if self.current_room is not room:
            self.current_room = room
            self.current_x = self.current_room.pos[1]
            self.current_y = self.current_room.pos[0]

    def update(self):
        self.set_current_room(self.game.dungeon_manager.current_room)

    def draw_all(self):
        surface = self.game.screen
        for room in self.visited_rooms:
            position = (self.offset_x + room[0] * self.room_width * 1.2,
                        self.offset_y + room[1] * self.room_height * 1.2)
            pygame.draw.rect(surface, DARK_GREY, (*position, *self.room_dimensions), 4)
        position = (self.offset_x + self.current_x * self.room_width * 1.2,
                    self.offset_y + self.current_y * self.room_height * 1.2)
        pygame.draw.rect(surface, GREY, (*position, *self.room_dimensions))





