import random
from dungeon.dungeon_generator import Room
from .enemy import Goblin


class EnemyManager:
    def __init__(self, game):
        self.game = game

    def draw_enemies(self):
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            if not self.game.dungeon_manager.room_change:
                enemy.draw()


    def update_enemies(self):
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            enemy.update()

    def spawn_enemies(self):
        # Spawns enemies in every room of the dungeon
        for row in self.game.dungeon_manager.dungeon.rooms:
            for room in row:
                if isinstance(room, Room) and room.type == 'normal':
                    self.spawn_normal_enemies(room)

    def spawn_normal_enemies(self, room):
        # Spawns enemies in a given room
        level = self.game.dungeon_manager.level
        num_enemies = random.randint(2 + level, 5 + level)  # Number of enemies to spawn, scales with the dungeon level
        for _ in range(num_enemies):
            enemy = Goblin(self.game, room, 100)
            room.enemy_list.append(enemy)
            room.enemy_list[-1].spawn()

