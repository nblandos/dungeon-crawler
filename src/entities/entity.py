import random
from .entity_animation import EntityAnimation
from objects.portal import Portal
from objects.flask import AttackFlask, HealthFlask, SpeedFlask


class Entity:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.path = f'../assets/frames/{self.name}'
        self.dead = False
        self.can_move = True
        self.direction = 'right'
        self.entity_animation = EntityAnimation(self)
        self.velocity = [0, 0]

    def set_velocity(self, new_velocity):
        # Sets the velocity of the entity to the argument
        self.velocity = new_velocity

    def wall_collision(self):
        # Creates a rect of where the hit_box will be after moving
        move_rect = self.hit_box.move(*self.velocity)
        collide_points = (
            move_rect.midbottom, move_rect.bottomleft,
            move_rect.bottomright)  # Creates a tuple of the points of the rect
        for wall in self.game.dungeon_manager.current_map.wall_list:
            # Loops through all the walls in the current map and checks if the hit_box will collide with any of them
            if any(wall.hit_box.collidepoint(point) for point in collide_points):
                # If the hit_box will collide with any of the walls, the velocity is set to 0
                self.velocity = [0, 0]

    def update_hit_box(self):
        # Updates the hit_box to the position of the rect
        self.hit_box.midbottom = self.rect.midbottom

    def detect_death(self):
        # Checks if the entity is dead
        if self.health <= 0 and not self.dead:
            self.dead = True
            self.entity_animation.animation_frame = 0
            self.can_move = False
            self.velocity = [0, 0]
            if self.room:
                # The dead entity is removed from the room
                self.room.enemy_list.remove(self)
                if self.room.type == 'boss':
                    # The portal to the next room is spawned if the boss is dead
                    self.room.object_list.append(
                        Portal(self.game, self.room, (640, 416)))
                    # Some health is restored if the room is cleared
                    self.game.player.health += self.game.player.max_health * \
                        (1 / 10)
                    if self.game.player.health > self.game.player.max_health:
                        self.game.player.health = self.game.player.max_health
                elif not self.room.enemy_list:
                    # Some health is restored if the room is cleared
                    self.game.player.health += self.game.player.max_health * \
                        (1 / 20)
                    if self.game.player.health > self.game.player.max_health:
                        self.game.player.health = self.game.player.max_health
                    if random.randint(0, 2) == 1:
                        # 1 in 3 chance of spawning a flask when all enemies are dead in a room
                        flask_list = [AttackFlask(self.game, self.room, (640, 408)),
                                      HealthFlask(
                                          self.game, self.room, (640, 408)),
                                      SpeedFlask(self.game, self.room, (640, 408))]
                        random_flask = random.choice(flask_list)
                        self.room.object_list.append(random_flask)

    def basic_update(self):
        # Updates the rect, hit_box and animations of the entity and checks if the entity is dead
        self.detect_death()
        self.update_hit_box()
        self.entity_animation.update()
        self.rect.move_ip(*self.velocity)
        self.hit_box.move_ip(*self.velocity)
