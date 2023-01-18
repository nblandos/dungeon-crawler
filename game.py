import pygame
import sys
import os
import random
import sqlite3
from settings import *
from entities.player import Player
from entities.enemy_manager import EnemyManager
from dungeon.dungeon_manager import DungeonManager
from objects.object_manager import ObjectManager
from sound_manager import SoundManager
from bullet import BulletManager
from menu import MainMenu, PauseMenu, HighscoreMenu
from hud import Hud

# Initialises pygame modules
pygame.init()


class Game:
    # Initialises the game
    def __init__(self, username):
        self.username = username
        # Sets up the game window
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.Surface((WIDTH, HEIGHT)).convert()
        pygame.display.set_caption(TITLE)
        # Sets up the game clock
        self.clock = pygame.time.Clock()
        self.constant_dt = 1 / FPS
        # Loads the music
        self.randomise_music()
        # Creates instances of the necessary classes
        self.dungeon_manager = DungeonManager(self)
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.spawn_enemies()
        self.bullet_manager = BulletManager(self)
        self.object_manager = ObjectManager(self)
        self.player = Player(self)
        self.main_menu = MainMenu(self)
        self.pause_menu = PauseMenu(self)
        self.highscore_menu = HighscoreMenu(self)
        self.hud = Hud(self)
        self.running = True

    def restart(self):
        # Restarts the game
        self.save_score()
        pygame.mixer.music.stop()
        self.__init__(self.username)
        self.run()

    def save_score(self):
        # Saves a score to the database if it is a highscore
        score = self.dungeon_manager.level
        con = sqlite3.connect('users.db')
        cursor = con.cursor()
        highscore = cursor.execute(f'SELECT highscore FROM users WHERE username = "{self.username}"').fetchone()[0]
        print(highscore)
        if score > highscore:
            cursor.execute(f'UPDATE users SET highscore = {score} WHERE username = "{self.username}"')
            con.commit()

    def pause(self):
        # Pauses the game
        self.pause_menu.running = True

    @staticmethod
    def randomise_music():
        # Changes the music to a different random track
        music = random.choice(os.listdir("assets/music"))
        while music == pygame.mixer.music.get_busy():
            music = random.choice(os.listdir("assets/music"))
        pygame.mixer.music.load(f"assets/music/{music}")
        pygame.mixer.music.set_volume(0.01)

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
            self.player.input()

    def run(self):
        # Main game loop that is called every frame
        while self.running:
            self.main_menu.show()
            self.pause_menu.show()
            self.highscore_menu.show()
            self.screen.fill(BLACK)
            self.update_groups()
            self.draw_groups()
            self.input()
            self.clock.tick(FPS)
            self.display.blit(self.screen, (0, 0))
            pygame.display.flip()
        pygame.quit()
        sys.exit()
