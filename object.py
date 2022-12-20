import pygame


class Object:
    def __init__(self, game, name, room, pos, size, player):
        self.game = game
        self.name = name
        self.room = room
        self.pos = pos
        self.size = size
        self.player = player
