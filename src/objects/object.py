import pygame
import functions as f


class Object:
    # This is the base class for all objects in the game.
    def __init__(self, game, name, room, pos, size):
        # Initializes the object with attributes common to all objects
        self.game = game
        self.name = name
        self.room = room
        self.pos = pos
        self.size = size
        self.path = f'../assets/frames/{self.name}.png'
        self.image = pygame.transform.scale(
            pygame.image.load(self.path), self.size).convert_alpha()
        self.image_copy = self.image
        self.rect = self.image.get_rect()
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.interaction = False

    def detect_interaction(self):
        # Detects if the player's hit box is touching the object's hit box
        if self.game.player.hit_box.colliderect(self.hit_box):
            self.interaction = True
        else:
            self.interaction = False

    def remove(self):
        # Removes the object from the object list of the room it is in
        self.room.object_list.remove(self)
        self.room = None

    def update(self):
        # Updates the hit box of the object
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.hit_box.midbottom = self.rect.midbottom

    def draw(self):
        # Draws the object
        self.room.tile_map.new_map_surface.blit(self.image, self.rect)
