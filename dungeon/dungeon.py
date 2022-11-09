import pygame
from settings import *
import functions as f
from collections import namedtuple


class SpriteSheet(object):
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, size):
        image = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, spritesheet, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = spritesheet.get_image(x, y, self.size)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hit_box = f.get_hit_box(self.image, *self.rect.topleft)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def swap_image(self, spritesheet, x, y, size):
        self.image = spritesheet.get_image(x, y, size)
        self.image = pygame.transform.scale(self.image, self.size)


class TileMap:
    def __init__(self, spritesheet, file, room):
        self.spritesheet = spritesheet
        self.file = file
        self.room = room
        self.map_size = (WIDTH, HEIGHT)
        self.tile_list = []
        self.wall_list = []
        self.map_surface = pygame.Surface(self.map_size).convert()
        self.map_surface.set_colorkey((0, 0, 0, 0))
        self.new_map_surface = None
        self.x, self.y = 0, 0  # position of map surface on screen surface
        self.load_tiles()
        self.load_map()

    def fix_map_position(self):
        if self.y != 0:
            self.y = 0
        if self.x != 0:
            self.x = 0

    def clear_map(self):
        self.new_map_surface = self.map_surface.copy()

    def load_map(self):
        self.map_surface.fill(BLACK)
        for layer in self.tile_list:
            for tile in layer:
                tile.draw(self.map_surface)
        self.clear_map()

    def load_tiles(self):
        for layer in self.file:
            tiles = []
            x = TILE_SIZE
            y = TILE_SIZE / 2
            for row in layer:
                for tile in row:
                    tiles.append(Tile(self.spritesheet, x, y, (TILE_SIZE, TILE_SIZE)))
                    if int(tile) in WALL_LIST:
                        self.wall_list.append(tiles[-1])
                    x += TILE_SIZE
                y += TILE_SIZE
            self.tile_list.append(tiles)

    def draw_map(self, surface):
        surface.blit(self.new_map_surface, (self.x, self.y))
        self.clear_map()
        for wall in self.wall_list:
            pygame.draw.rect(surface, (255, 255, 255), wall.rect, 2)
