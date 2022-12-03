import pygame
import sys
from settings import *
from button import PlayButton, SettingsButton, QuitButton


class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('assets/fonts/main_font.ttf', 140)
        self.running = True
        self.title = self.font.render("Roguelike NEA", True, WHITE)
        self.play_button = PlayButton(self, 10.5 * TILE_SIZE, 4 * TILE_SIZE)
        self.settings_button = SettingsButton(self, 10.5 * TILE_SIZE, 6.75 * TILE_SIZE)
        self.quit_button = QuitButton(self, 10.5 * TILE_SIZE, 9.5 * TILE_SIZE)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.title, (6.5 * TILE_SIZE, 50))
        self.play_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()

    def update(self):
        self.play_button.update()
        self.settings_button.update()
        self.quit_button.update()

    def show(self):
        while self.running:
            self.input()
            self.draw()
            self.update()
            self.game.clock.tick(FPS)
            self.game.display.blit(self.game.screen, (0, 0))
            self.play_button.update()
            pygame.display.flip()

