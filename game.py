import pygame
import sys
from settings import *
from entities.player import Player
from entities.enemy_manager import EnemyManager
from dungeon.dungeon_manager import DungeonManager
from objects.object_manager import ObjectManager
from bullet import BulletManager
from menu import Menu
from hud import Hud

# Initialises pygame modules
pygame.init()


class Game:
    # Initialises the game
    def __init__(self):
        # Sets up the game window
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.Surface((WIDTH, HEIGHT)).convert()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.constant_dt = 1 / FPS
        # Creates instances of the necessary classes
        self.dungeon_manager = DungeonManager(self)
        self.enemy_manager = EnemyManager(self)
        self.bullet_manager = BulletManager(self)
        self.object_manager = ObjectManager(self)
        self.player = Player(self)
        self.menu = Menu(self)
        self.hud = Hud(self)
        self.running = True

    def refresh(self):
        # Restarts the game
        self.__init__()
        pygame.display.flip()
        self.run()

    def update_groups(self):
        # Updates all groups
        self.dungeon_manager.update()
        self.enemy_manager.update()
        self.object_manager.update()
        self.bullet_manager.update()
        self.player.update()

    def draw_groups(self):
        # Draws all groups on the screen
        self.dungeon_manager.draw(self.screen)
        self.enemy_manager.draw()
        self.object_manager.draw()
        self.bullet_manager.draw()
        self.player.draw()
        self.hud.draw()

    def input(self):
        # Checks for user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.player.input()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.refresh()

    def run(self):
        self.enemy_manager.spawn_enemies()
        # Main game loop that is called every frame
        while self.running:
            self.menu.show()
            self.screen.fill(BLACK)
            self.update_groups()
            self.draw_groups()
            self.input()
            self.clock.tick(FPS)
            self.display.blit(self.screen, (0, 0))
            pygame.display.flip()
        pygame.quit()
        sys.exit()
