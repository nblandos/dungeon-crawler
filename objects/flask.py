from settings import *
from .object import Object


class Flask(Object):
    def __init__(self, game, name, room, pos, size):
        Object.__init__(self, game, name, room, pos, size)  # Inherits from the Object class

    def interact(self):
        pass


class AttackFlask(Flask):
    name = 'flask_big_green'
    size = (TILE_SIZE, TILE_SIZE)

    def __init__(self, game, room, pos):
        Flask.__init__(self, game, self.name, room, pos, self.size)

    def interact(self):
        self.game.player.attack_multiplier += 0.1
        self.remove()


class HealthFlask(Flask):
    name = 'flask_big_red'
    size = (TILE_SIZE, TILE_SIZE)

    def __init__(self, game, room, pos):
        Flask.__init__(self, game, self.name, room, pos, self.size)

    def interact(self):
        self.game.player.max_health += 25
        self.game.player.health += 25
        self.remove()


class SpeedFlask(Flask):
    name = 'flask_big_blue'
    size = (TILE_SIZE, TILE_SIZE)

    def __init__(self, game, room, pos):
        Flask.__init__(self, game, self.name, room, pos, self.size)

    def interact(self):
        self.game.player.speed += 30
        self.remove()
