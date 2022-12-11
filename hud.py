import pygame


class Hud:
    def __init__(self, game):
        self.game = game
        self.health_bar = HealthBar(self.game, self.game.player)

    def draw(self):
        self.health_bar.draw()


class HealthBar:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def draw(self):
        pass

