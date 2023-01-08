FPS = 60
SCALE_FACTOR = 4
TILE_SIZE = 16 * SCALE_FACTOR
PLAYER_HEIGHT = 28 * SCALE_FACTOR
WIDTH = 21 * TILE_SIZE
HEIGHT = 13 * TILE_SIZE
TITLE = "Roguelike NEA"
FONT = "assets/fonts/main_font.ttf"
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 32)
BURGUNDY = (128, 0, 32)
WHITE = (255, 255, 255)
GREY = (210, 210, 210)
DARK_GREY = (150, 148, 153)
LIME_GREEN = (0, 255, 0)
MIN_ROOMS = 8
MAX_ROOMS = 12
DUNGEON_SIZE = (8, 8)
POSSIBLE_ROOMS = {
        'N': [['N', 'E', 'S', 'W'], ['S'], ['N', 'S'], ['S', 'W'], ['E', 'S'], ['E', 'S', 'W'], ['N', 'S', 'W'], ['N', 'E', 'S']],
        'E': [['N', 'E', 'S', 'W'], ['W'], ['E', 'W'], ['N', 'W'], ['S', 'W'], ['E', 'S', 'W'], ['N', 'S', 'W'], ['N', 'E', 'W']],
        'S': [['N', 'E', 'S', 'W'], ['N'], ['N', 'S'], ['N', 'W'], ['N', 'E'], ['N', 'E', 'W'], ['N', 'S', 'W'], ['N', 'E', 'S']],
        'W': [['N', 'E', 'S', 'W'], ['E'], ['N', 'E'], ['E', 'S'], ['E', 'W'], ['E', 'S', 'W'], ['N', 'E', 'W'], ['N', 'E', 'S']],
        }
WALL_LIST = (1, 2, 3, 33, 34, 35, 67, 99, 224, 227, 225, 226, 256, 257, 258, 259, 288, 289)
FLOOR_TILES = [129, 130, 131, 161, 162, 163, 193, 194]
