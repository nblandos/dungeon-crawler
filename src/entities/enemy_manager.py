import random
from dungeon.dungeon_generator import Room
from .enemy import Goblin, Imp, BigZombie, BigDemon


# As there are many enemies belonging to different rooms, this class manages which ones to draw and update
class EnemyManager:
    def __init__(self, game):
        # Initializes the enemy manager
        self.game = game
        self.multiplier_value = 0.3

    def draw(self):
        # Draws all enemies in the current room
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            enemy.draw()
        # If the player is switching rooms, draws the enemies in the room they are switching to
        if self.game.dungeon_manager.next_room:
            for enemy in self.game.dungeon_manager.next_room.enemy_list:
                enemy.draw()

    def update(self):
        # Updates all enemies in the current room
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            enemy.update()

    def spawn_enemies(self):
        # Spawns enemies in every room of the dungeon
        for row in self.game.dungeon_manager.dungeon.rooms:
            for room in row:
                if isinstance(room, Room) and room.type == 'normal':
                    self.spawn_normal_enemies(room)
                elif isinstance(room, Room) and room.type == 'boss':
                    self.spawn_boss(room)

    def spawn_normal_enemies(self, room):
        # Spawns enemies in a given room
        level = self.game.dungeon_manager.level
        # The multiplier scales the enemies' stats based on the level of the dungeon
        multiplier = 1 + (level - 1) * self.multiplier_value
        if level > 6:
            level = 6
        # Number of enemies to spawn, scales with the dungeon level
        num_goblins = random.randint(1, 2 + level)
        num_imps = random.randint(0, 1 + level)
        for _ in range(num_goblins):
            # Creates the specified number of goblins
            enemy = Goblin(self.game, room, 25 * multiplier)
            enemy.damage *= multiplier
            room.enemy_list.append(enemy)
            room.enemy_list[-1].spawn()
        for _ in range(num_imps):
            # Creates the specified number of imps
            enemy = Imp(self.game, room, 20 * multiplier)
            enemy.damage *= multiplier
            room.enemy_list.append(enemy)
            room.enemy_list[-1].spawn()

    def spawn_boss(self, room):
        # Spawns the boss in the boss room
        multiplier = 1 + (self.game.dungeon_manager.level -
                          1) * self.multiplier_value
        boss_list = [BigZombie(self.game, room, 150 * multiplier),
                     BigDemon(self.game, room, 200 * multiplier)]
        enemy = random.choice(boss_list)
        enemy.damage *= multiplier
        room.enemy_list.append(enemy)
        room.enemy_list[-1].spawn()
