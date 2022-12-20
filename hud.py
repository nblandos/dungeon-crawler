import pygame
from settings import *


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
        self.path = 'assets/hud/health_bar.png'
        self.health_bar = pygame.transform.scale(pygame.image.load(self.path), (195, 45)).convert_alpha()

    def draw(self):
        pygame.draw.rect(self.game.screen, DARK_RED, (0, 0, 195, 45))
        num_sections = self.player.health // 10
        for i in range(num_sections):
            pygame.draw.rect(self.game.screen, RED, (25 + i * 15, 15, 10, 15))
        self.game.screen.blit(self.health_bar, (0, 0))



