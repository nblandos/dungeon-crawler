import pygame
import sys
from settings import *
from entities.player import Player
from entities.enemy_manager import EnemyManager
from dungeon.dungeon_manager import DungeonManager
from objects.object_manager import ObjectManager
from bullet import BulletManager
from menu import MainMenu, PauseMenu
from hud import Hud
from login_system import LoginSystem

# Initialises pygame modules
pygame.init()


class Game:
    # Initialises the game
    def __init__(self):
        # Sets up the game window
        self.login_system = LoginSystem()
        if self.login_system.logged_in:
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            self.screen = pygame.Surface((WIDTH, HEIGHT)).convert()
            pygame.display.set_caption(TITLE)
            pygame.mixer.music.load('assets/music/music.ogg')
            pygame.mixer.music.set_volume(0.01)
            self.clock = pygame.time.Clock()
            self.constant_dt = 1 / FPS
            # Creates instances of the necessary classes
            self.dungeon_manager = DungeonManager(self)
            self.enemy_manager = EnemyManager(self)
            self.bullet_manager = BulletManager(self)
            self.object_manager = ObjectManager(self)
            self.player = Player(self)
            self.main_menu = MainMenu(self)
            self.pause_menu = PauseMenu(self)
            self.hud = Hud(self)
            self.running = True

    def restart(self):
        # Restarts the game
        pygame.mixer.music.stop()
        self.__init__()
        self.run()

    def pause(self):
        # Pauses the game
        self.pause_menu.running = True

    def update_groups(self):
        # Updates all groups
        self.dungeon_manager.update()
        self.object_manager.update()
        self.enemy_manager.update()
        self.bullet_manager.update()
        self.player.update()
        self.hud.update()

    def draw_groups(self):
        # Draws all groups on the screen
        self.dungeon_manager.draw(self.screen)
        self.object_manager.draw()
        self.enemy_manager.draw()
        self.bullet_manager.draw()
        self.player.draw()
        self.hud.draw()

    def input(self):
        # Checks for user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause()
                if event.key == pygame.K_r:
                    self.restart()
            self.player.input()

    def run(self):
        self.enemy_manager.spawn_enemies()
        # Main game loop that is called every frame
        while self.running:
            self.main_menu.show()
            self.pause_menu.show()
            self.screen.fill(BLACK)
            self.update_groups()
            self.draw_groups()
            self.input()
            self.clock.tick(FPS)
            self.display.blit(self.screen, (0, 0))
            pygame.display.flip()
        pygame.quit()
        sys.exit()
