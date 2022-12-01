import pygame
import random
from .entity import Entity

class Enemy(Entity):
    def __init__(self, game, name, room, max_health):
        Entity.__init__(self, game, name)
        self.room = room
        self.health = max_health

    def spawn(self):
        self.rect.x = random.randint(200, 1000)
        self.rect.y = random.randint(250, 600)

    def move(self):
        pass

    def follow_player(self):
        distance_to_player = pygame.math.Vector2(self.game.player.hit_box.centerx - self.hit_box.centerx,
                                                 self.game.player.hit_box.centery - self.hit_box.centery).length()


