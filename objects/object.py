import pygame
import functions as f


class Object:
    def __init__(self, game, name, room, pos, size):
        self.game = game
        self.name = name
        self.room = room
        self.pos = pos
        self.size = size
        self.path = f'assets/frames/{self.name}.png'
        self.image = pygame.transform.scale(pygame.image.load(self.path), self.size).convert_alpha()
        self.rect = self.image.get_rect()
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.interaction = False

    def detect_interaction(self):
        if self.game.player.hit_box.colliderect(self.hit_box):
            self.interaction = True
        else:
            self.interaction = False

    def remove(self):
        self.room.object_list.remove(self)

    def update(self):
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)
        self.hit_box.midbottom = self.rect.midbottom

    def draw(self):
        self.room.tile_map.new_map_surface.blit(self.image, self.rect)

