import pygame


class ObjectManager:
    def __init__(self, game):
        self.game = game

    def interact(self):
        for obj in self.game.dungeon_manager.current_room.object_list:
            if obj.interaction:
                obj.interact()

    def draw(self):
        # Draws all objects in the current room
        for obj in self.game.dungeon_manager.current_room.object_list:
            obj.draw()
        # If the player is switching rooms, draws the objects in the room they are switching to
        if self.game.dungeon_manager.next_room:
            for obj in self.game.dungeon_manager.next_room.object_list:
                obj.draw()

    def update(self):
        # Updates all objects
        for obj in self.game.dungeon_manager.current_room.object_list:
            obj.detect_interaction()
            obj.update()
        if self.game.player.weapon:
            self.game.player.weapon.update()




