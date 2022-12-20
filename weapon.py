import pygame
import functions as f
from object import Object


class Weapon:
    def __init__(self, game, name, size):
        self.game = game
        self.name = name
        self.size = size
        self.player = self.game.player
        self.path = f'assets/frames/weapon_{self.name}.png'
        self.image = pygame.transform.scale(pygame.image.load(self.path), self.size).convert_alpha()
        self.rect = self.image.get_rect()
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)

    def draw(self):
        if self.player:
            surface = self.game.screen
        surface.blit(self.image, self.rect)


class RustySword(Weapon):
    name = 'rusty_sword'
    size = (36, 96)
    damage = 10

    def __init__(self, game):
        Weapon.__init__(self, game, self.name, self.size)
